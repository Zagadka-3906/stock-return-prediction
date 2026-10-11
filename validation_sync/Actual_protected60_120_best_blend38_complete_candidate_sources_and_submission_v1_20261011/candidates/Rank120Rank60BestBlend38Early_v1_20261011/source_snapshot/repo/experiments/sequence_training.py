"""Training and evaluation for the sequence-model feasibility probe.

Imported by experiments.sequence_model; the protocol is frozen there before any
of this runs. Source hash is re-verified at every stage so the frozen protocol
cannot be paired with edited code.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import polars as pl
import torch
import torch.nn as nn
from scipy.stats import rankdata, spearmanr

from run import ROOT, feature_names
from experiments.bonus_extension import FOLD, file_hash, load_panel
from experiments.official_seed_development import official_score
from experiments.sequence_model import (ARCHITECTURES, BATCH_DAYS, CLIP_STD, HIDDEN,
                                        INNER_CUTOFF_EXCLUSIVE, INNER_VAL_YEAR, LEARNING_RATE,
                                        MAX_EPOCHS, MIN_VALID_PER_DAY, OUTER_YEAR, OUT, PATIENCE,
                                        SEED, WEIGHT_DECAY, WINDOWS, apply_scaler, file_hash_of_array,
                                        fit_scaler, load_panel as load_sequence_panel, log)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DROPOUT = 0.0
SENTINEL = -1e6


class FeedForward(nn.Module):
    """Control: the same 63 daily features with no temporal structure."""

    def __init__(self, n_features: int, hidden: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_features, hidden), nn.GELU(), nn.Linear(hidden, 1))

    def forward(self, window: torch.Tensor) -> torch.Tensor:
        return self.net(window[:, -1, :]).squeeze(-1)


class Recurrent(nn.Module):
    """GRU over the trailing window; gru_cat also sees the current day directly."""

    def __init__(self, n_features: int, hidden: int, concatenate: bool):
        super().__init__()
        self.gru = nn.GRU(n_features, hidden, batch_first=True)
        self.concatenate = concatenate
        if concatenate:
            self.head = nn.Sequential(nn.Linear(hidden + n_features, hidden), nn.GELU(),
                                      nn.Linear(hidden, 1))
        else:
            self.head = nn.Linear(hidden, 1)

    def forward(self, window: torch.Tensor) -> torch.Tensor:
        output, _ = self.gru(window)
        last = output[:, -1, :]
        features = torch.cat([last, window[:, -1, :]], dim=1) if self.concatenate else last
        return self.head(features).squeeze(-1)


def build_model(architecture: str, n_features: int, hidden: int) -> nn.Module:
    if architecture == "mlp":
        return FeedForward(n_features, hidden)
    if architecture == "gru":
        return Recurrent(n_features, hidden, concatenate=False)
    if architecture == "gru_cat":
        return Recurrent(n_features, hidden, concatenate=True)
    raise ValueError(f"Architecture not in the frozen protocol: {architecture}")


def config_key(architecture: str, hidden: int, window: int) -> str:
    return f"{architecture}_h{hidden}_w{window}" if architecture != "mlp" else f"mlp_h{hidden}"


def enumerate_grid() -> list[tuple[str, int, int]]:
    grid = []
    for architecture in ARCHITECTURES:
        for hidden in HIDDEN:
            if architecture == "mlp":
                grid.append((architecture, hidden, 1))
            else:
                for window in WINDOWS:
                    grid.append((architecture, hidden, window))
    return grid


class Tensors:
    """Panel held on the accelerator so windows are gathered without host transfers."""

    def __init__(self, dates, codes, z, y, valid):
        self.dates = list(dates)
        self.codes = list(codes)
        self.index_of = {date: position for position, date in enumerate(self.dates)}
        self.z = torch.from_numpy(z).to(DEVICE)
        self.y = torch.from_numpy(np.nan_to_num(y, nan=0.0).astype(np.float32)).to(DEVICE)
        # The loss needs a label; prediction output needs only a valid price, because the
        # official turnover Top is formed without any label filter.
        self.price_valid = torch.from_numpy(valid.copy()).to(DEVICE)
        self.mask = torch.from_numpy((valid & np.isfinite(y))).to(DEVICE)
        self.days = len(self.dates)
        self.stocks = self.z.shape[1]
        self.features = self.z.shape[2]

    def usable_days(self, day_indices: list[int], window: int) -> list[int]:
        counts = self.mask.sum(dim=1)
        return [t for t in day_indices
                if t >= window - 1 and int(counts[t]) >= MIN_VALID_PER_DAY]

    def windows(self, day_indices: np.ndarray, window: int) -> torch.Tensor:
        index = torch.as_tensor(day_indices, device=DEVICE)
        offsets = torch.arange(-(window - 1), 1, device=DEVICE)
        gathered = self.z[index[:, None] + offsets[None, :]]
        return gathered.permute(0, 2, 1, 3).reshape(-1, window, self.features)

    def batch_targets(self, day_indices: np.ndarray):
        index = torch.as_tensor(day_indices, device=DEVICE)
        return self.y[index], self.mask[index]


def daily_pearson_ic(prediction: torch.Tensor, target: torch.Tensor,
                     mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Differentiable proxy for the competition's Rank IC.

    The target is already a daily cross-sectional percentile, so Pearson against
    it approximates Spearman against raw returns while staying differentiable.
    Rows outside the mask contribute to neither mean, product nor norm.
    """
    zero = torch.zeros_like(target)
    count = mask.sum(dim=1).float()
    usable = count >= MIN_VALID_PER_DAY
    safe = count.clamp(min=1.0)[:, None]
    masked_target = torch.where(mask, target, zero)
    masked_prediction = torch.where(mask, prediction, zero)
    centered_target = torch.where(mask, target - masked_target.sum(1, keepdim=True) / safe, zero)
    centered_prediction = torch.where(mask, prediction - masked_prediction.sum(1, keepdim=True) / safe, zero)
    covariance = (centered_prediction * centered_target).sum(dim=1)
    scale = centered_prediction.norm(dim=1) * centered_target.norm(dim=1)
    return covariance / (scale + 1e-8), usable


def predict_days(tensors: Tensors, model: nn.Module, day_indices: list[int], window: int,
                 chunk_days: int = 8) -> np.ndarray:
    """Raw predictions on the (day, stock) grid for every price-valid row.

    Rows without a valid price become NaN so the caller can sentinel them; rows
    that merely lack a label keep their prediction, matching the backbone.
    """
    model.eval()
    out = np.full((len(day_indices), tensors.stocks), np.nan, dtype=np.float32)
    with torch.no_grad():
        for start in range(0, len(day_indices), chunk_days):
            chunk = np.asarray(day_indices[start:start + chunk_days], dtype=np.int64)
            prediction = model(tensors.windows(chunk, window)).view(len(chunk), tensors.stocks)
            values = prediction.float().cpu().numpy()
            keep = tensors.price_valid[torch.as_tensor(chunk, device=DEVICE)].cpu().numpy()
            values[~keep] = np.nan
            out[start:start + len(chunk)] = values
    return out


def spearman_by_day(prediction: np.ndarray, target: np.ndarray, mask: np.ndarray) -> float:
    """Mean daily Spearman over valid rows, matching the evaluator's definition."""
    values = []
    for day in range(prediction.shape[0]):
        keep = mask[day] & np.isfinite(prediction[day])
        if keep.sum() < 30:
            continue
        ic = spearmanr(prediction[day][keep], target[day][keep]).statistic
        if np.isfinite(ic):
            values.append(float(ic))
    if not values:
        raise AssertionError("No day had enough valid rows to compute Spearman IC")
    return float(np.mean(values))


def train_configuration(tensors: Tensors, train_days: list[int], val_days: list[int],
                        architecture: str, hidden: int, window: int,
                        y_all: np.ndarray, valid_all: np.ndarray) -> dict:
    torch.manual_seed(SEED)
    model = build_model(architecture, tensors.features, hidden).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    usable_train = tensors.usable_days(train_days, window)
    usable_val = tensors.usable_days(val_days, window)
    if len(usable_train) < 100 or not usable_val:
        raise AssertionError(f"{architecture}: insufficient usable days "
                             f"({len(usable_train)} train, {len(usable_val)} val)")
    rows = np.asarray(usable_val, dtype=int)
    y_val = y_all[rows]
    val_mask = valid_all[rows] & np.isfinite(y_all[rows])
    best = {"val_ic": -np.inf, "epoch": -1, "state": None}
    curve = []
    started = time.monotonic()
    generator = np.random.default_rng(SEED)
    for epoch in range(MAX_EPOCHS):
        model.train()
        order = generator.permutation(np.asarray(usable_train, dtype=np.int64))
        running, batches = 0.0, 0
        for start in range(0, len(order), BATCH_DAYS):
            chunk = order[start:start + BATCH_DAYS]
            if len(chunk) < 2:
                continue
            prediction = model(tensors.windows(chunk, window))
            target, mask = tensors.batch_targets(chunk)
            ic, usable = daily_pearson_ic(prediction.view(len(chunk), -1), target, mask)
            if not bool(usable.any()):
                continue
            loss = -ic[usable].mean()
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            running += float(loss.detach())
            batches += 1
        raw = predict_days(tensors, model, usable_val, window)
        val_ic = spearman_by_day(raw, y_val, val_mask)
        curve.append({"epoch": epoch, "train_loss": running / max(batches, 1), "val_ic": val_ic})
        if val_ic > best["val_ic"]:
            best = {"val_ic": val_ic, "epoch": epoch,
                    "state": {k: v.detach().clone() for k, v in model.state_dict().items()}}
        elif epoch - best["epoch"] >= PATIENCE:
            break
    elapsed = time.monotonic() - started
    return {"architecture": architecture, "hidden": hidden, "window": window,
            "key": config_key(architecture, hidden, window),
            "best_val_ic": best["val_ic"], "best_epoch": best["epoch"],
            "epochs_run": len(curve), "train_days": len(usable_train), "val_days": len(usable_val),
            "parameters": sum(p.numel() for p in model.parameters()),
            "elapsed_seconds": elapsed, "curve": curve, "state": best["state"]}


def verify_protocol() -> dict:
    path = OUT / "protocol.json"
    if not path.exists():
        raise SystemExit("Run the protocol stage first")
    protocol = json.loads(path.read_text(encoding="utf-8"))
    source = file_hash(Path(__file__).parent / "sequence_model.py")
    if protocol["source_sha256"] != source:
        raise SystemExit("sequence_model.py changed after the protocol was frozen; "
                         "stop rather than run edited code against a frozen rule")
    return protocol


def build_tensors(features, cutoff, end_year=OUTER_YEAR):
    dates, codes, x, y, valid, _ = load_sequence_panel(features, end_year)
    mean, std, stats = fit_scaler(x, valid, dates, cutoff)
    z = apply_scaler(x, mean, std)
    del x
    tensors = Tensors(dates, codes, z, y, valid)
    del z
    return tensors, y, valid, mean, std, stats, dates, codes


def run_stage(stage: str) -> None:
    features = feature_names()
    protocol = verify_protocol()
    if stage == "search":
        search(protocol, features)
    else:
        fold(protocol, features)


def search(protocol: dict, features: list[str]) -> None:
    result_path = OUT / "search.json"
    if result_path.exists():
        raise SystemExit("Search results already recorded; preserving them instead of rerunning")
    log(f"Device {DEVICE}; building panel normalized on trade_date < {INNER_CUTOFF_EXCLUSIVE}")
    tensors, y, valid, mean, std, stats, dates, codes = build_tensors(
        features, INNER_CUTOFF_EXCLUSIVE)
    inner_train = [t for t, d in enumerate(dates) if d < INNER_CUTOFF_EXCLUSIVE]
    inner_val = [t for t, d in enumerate(dates)
                 if INNER_VAL_YEAR * 10000 + 101 <= d <= INNER_VAL_YEAR * 10000 + 1231]
    if not inner_train or not inner_val:
        raise AssertionError("Inner split is empty")
    log(f"Inner train {len(inner_train)} days ({dates[inner_train[0]]}..{dates[inner_train[-1]]}), "
        f"inner val {len(inner_val)} days ({dates[inner_val[0]]}..{dates[inner_val[-1]]})")

    grid = enumerate_grid()
    results = {}
    for architecture, hidden, window in grid:
        key = config_key(architecture, hidden, window)
        record = train_configuration(tensors, inner_train, inner_val, architecture, hidden,
                                     window, y, valid)
        state = record.pop("state")
        results[key] = record
        log(f"{key}: val_ic={record['best_val_ic']:.6f} @epoch {record['best_epoch']} "
            f"({record['epochs_run']} run, {record['parameters']:,} params, "
            f"{record['elapsed_seconds']:.0f}s)")
        del state
        if DEVICE.type == "cuda":
            torch.cuda.empty_cache()

    selected = min(results, key=lambda k: (-results[k]["best_val_ic"], results[k]["hidden"],
                                           results[k]["window"],
                                           ARCHITECTURES.index(results[k]["architecture"])))
    output = {
        "stage": "search",
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol_sha256": file_hash(OUT / "protocol.json"),
        "device": str(DEVICE),
        "gpu": torch.cuda.get_device_name(0) if DEVICE.type == "cuda" else None,
        "torch_version": torch.__version__,
        "dropout": DROPOUT,
        "clip_std": CLIP_STD,
        "batch_days": BATCH_DAYS,
        "seed": SEED,
        "inner_split": {"train_days": len(inner_train), "val_days": len(inner_val),
                        "train_first": dates[inner_train[0]], "train_last": dates[inner_train[-1]],
                        "val_first": dates[inner_val[0]], "val_last": dates[inner_val[-1]]},
        "normalization": stats,
        "normalization_mean_sha256": file_hash_of_array(mean),
        "normalization_std_sha256": file_hash_of_array(std),
        "grid": [config_key(a, h, w) for a, h, w in grid],
        "results": results,
        "selected_key": selected,
        "selected_configuration": {k: results[selected][k]
                                   for k in ("architecture", "hidden", "window", "best_val_ic",
                                             "best_epoch", "epochs_run", "parameters")},
        "selection_rule": protocol["selection_rule"],
        "caveat": "Architecture selected on 2021 only. The 2022 outer year has not been scored.",
    }
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"SELECTED {selected} (val IC {results[selected]['best_val_ic']:.6f}); "
        f"2022 not yet scored")


def rank_average_ensemble(panel, backbone_raw: np.ndarray, other_raw: np.ndarray) -> np.ndarray:
    """Equal-weight average of daily cross-sectional percentile ranks."""
    shape = panel.valid_price.shape
    backbone = np.asarray(backbone_raw, dtype=np.float64).reshape(shape)
    other = np.asarray(other_raw, dtype=np.float64).reshape(shape)
    out = np.full(shape, -10.0, dtype=np.float64)
    for day in range(shape[0]):
        keep = panel.valid_price[day] & np.isfinite(backbone[day]) & np.isfinite(other[day])
        count = int(keep.sum())
        if not count:
            continue
        left = rankdata(backbone[day][keep], method="average") / count
        right = rankdata(other[day][keep], method="average") / count
        out[day][keep] = 0.5 * left + 0.5 * right
    return out.reshape(-1)


def fold(protocol: dict, features: list[str]) -> None:
    search_path = OUT / "search.json"
    if not search_path.exists():
        raise SystemExit("Run the search stage first")
    decision_path = OUT / "decision.json"
    if decision_path.exists():
        raise SystemExit("Decision already recorded; preserving it instead of rescoring 2022")
    search_record = json.loads(search_path.read_text(encoding="utf-8"))
    if search_record["protocol_sha256"] != file_hash(OUT / "protocol.json"):
        raise SystemExit("Search results were produced under a different protocol")
    configuration = search_record["selected_configuration"]
    bars = json.loads((OUT / "reference_bars.json").read_text(encoding="utf-8"))
    bar = bars["years"][str(OUTER_YEAR)]["backbone_raw_no_postprocess"]["ic_mean"]

    cutoff = protocol["outer_fold_cutoff_exclusive"]
    log(f"Final fold: normalize and train on trade_date < {cutoff}, score {OUTER_YEAR} once")
    tensors, y, valid, mean, std, stats, dates, codes = build_tensors(features, cutoff)
    train_days = [t for t, d in enumerate(dates) if d < cutoff]
    outer_days = [t for t, d in enumerate(dates)
                  if OUTER_YEAR * 10000 + 101 <= d <= OUTER_YEAR * 10000 + 1231]
    usable_train = tensors.usable_days(train_days, configuration["window"])
    usable_outer = tensors.usable_days(outer_days, configuration["window"])
    log(f"Fold train {len(usable_train)} days, outer {len(usable_outer)}/{len(outer_days)} days")

    fold_panel = load_panel(OUTER_YEAR)
    if list(fold_panel.codes) != codes:
        raise AssertionError("Sequence panel stock order differs from the released fold panel")
    fold_dates = [int(d) for d in fold_panel.dates]
    outer_positions = [dates.index(d) for d in fold_dates]
    if outer_positions != list(range(outer_days[0], outer_days[0] + len(outer_days))):
        raise AssertionError("Outer year is not contiguous in the sequence panel")

    epochs = configuration["best_epoch"] + 1
    torch.manual_seed(SEED)
    model = build_model(configuration["architecture"], tensors.features,
                        configuration["hidden"]).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    generator = np.random.default_rng(SEED)
    started = time.monotonic()
    for epoch in range(epochs):
        model.train()
        order = generator.permutation(np.asarray(usable_train, dtype=np.int64))
        for start in range(0, len(order), BATCH_DAYS):
            chunk = order[start:start + BATCH_DAYS]
            if len(chunk) < 2:
                continue
            prediction = model(tensors.windows(chunk, configuration["window"]))
            target, mask = tensors.batch_targets(chunk)
            ic, usable = daily_pearson_ic(prediction.view(len(chunk), -1), target, mask)
            if not bool(usable.any()):
                continue
            loss = -ic[usable].mean()
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 10 == 0 or epoch + 1 == epochs:
            log(f"  epoch {epoch + 1}/{epochs} elapsed {time.monotonic() - started:.0f}s")
    train_seconds = time.monotonic() - started

    raw_days = predict_days(tensors, model, usable_outer, configuration["window"])
    nn_prediction = np.full((len(fold_dates), tensors.stocks), SENTINEL, dtype=np.float64)
    covered = [d in set(usable_outer) for d in outer_positions]
    if not all(covered):
        missing = [fold_dates[i] for i, c in enumerate(covered) if not c]
        raise AssertionError(f"Outer days missing a full window: {missing[:5]}")
    for row, position in enumerate(outer_positions):
        slot = usable_outer.index(position)
        values = raw_days[slot].astype(np.float64)
        values[~np.isfinite(values)] = SENTINEL
        nn_prediction[row] = values
    nn_prediction = nn_prediction.reshape(-1)
    if not np.isfinite(nn_prediction).all():
        raise AssertionError("Sequence model emitted a nonfinite prediction")

    backbone_raw = fold_panel.frame["pred_raw"].to_numpy().astype(np.float64)
    nn_metrics, nn_daily = official_score(fold_panel, nn_prediction, OUTER_YEAR)
    ensemble = rank_average_ensemble(fold_panel, backbone_raw, nn_prediction)
    ensemble_metrics, ensemble_daily = official_score(fold_panel, ensemble, OUTER_YEAR)
    backbone_metrics, _ = official_score(fold_panel, backbone_raw, OUTER_YEAR)
    if abs(backbone_metrics["ic_mean"] - bar) > 1e-12:
        raise AssertionError(f"Backbone raw IC {backbone_metrics['ic_mean']:.12f} does not "
                             f"reproduce the frozen bar {bar:.12f}")

    strong_pass = nn_metrics["ic_mean"] >= bar
    ensemble_pass = ensemble_metrics["ic_mean"] > bar
    decision = "strong_pass" if strong_pass else ("pass" if ensemble_pass else "fail")
    nn_daily.write_csv(OUT / f"sequence_{OUTER_YEAR}_daily.csv")
    ensemble_daily.write_csv(OUT / f"ensemble_{OUTER_YEAR}_daily.csv")

    output = {
        "stage": "fold",
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol_sha256": file_hash(OUT / "protocol.json"),
        "search_sha256": file_hash(search_path),
        "selected_configuration": configuration,
        "outer_year": OUTER_YEAR,
        "epochs_applied": epochs,
        "train_days": len(usable_train),
        "train_seconds": train_seconds,
        "normalization": stats,
        "backbone_raw_ic_bar": bar,
        "results": {
            "backbone_raw": {k: float(v) for k, v in backbone_metrics.items()},
            "sequence_raw": {k: float(v) for k, v in nn_metrics.items()},
            "rank_average_ensemble": {k: float(v) for k, v in ensemble_metrics.items()},
        },
        "deltas": {
            "sequence_minus_backbone_ic": nn_metrics["ic_mean"] - bar,
            "ensemble_minus_backbone_ic": ensemble_metrics["ic_mean"] - bar,
            "sequence_relative_ic": nn_metrics["ic_mean"] / bar - 1,
            "ensemble_relative_ic": ensemble_metrics["ic_mean"] / bar - 1,
        },
        "gate": {"strong_pass": bool(strong_pass), "ensemble_pass": bool(ensemble_pass),
                 "decision": decision,
                 "rule": protocol["gate"]},
        "recommended_for_next_version": decision != "fail",
        "deployed_to_production": False,
        "official_submission_or_report_changed": False,
        "score_first_rule_changed_after_results": False,
        "device": str(DEVICE),
        "torch_version": torch.__version__,
        "source_and_input_sha256": {
            "experiments/sequence_model.py": file_hash(OUT.parent / "sequence_model.py"),
            "experiments/sequence_training.py": file_hash(Path(__file__)),
            "evaluate.py": file_hash(ROOT / "evaluate.py"),
            FOLD.format(year=OUTER_YEAR): file_hash(ROOT / FOLD.format(year=OUTER_YEAR)),
        },
        "caveats": protocol["limitations"] + [
            "Raw IC only; the released post-processing stack was not applied, so no composite "
            "score is claimed at this stage.",
            "A single outer year cannot separate model improvement from regime luck.",
            "cuDNN recurrent backward is not bitwise deterministic; the epoch count came from the "
            "inner split and was applied unchanged.",
        ],
    }
    decision_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"{OUTER_YEAR} backbone raw IC={bar:.6f} | sequence raw IC={nn_metrics['ic_mean']:.6f} "
        f"({output['deltas']['sequence_relative_ic']:+.2%}) | "
        f"ensemble IC={ensemble_metrics['ic_mean']:.6f} "
        f"({output['deltas']['ensemble_relative_ic']:+.2%})")
    log(f"GATE: {decision.upper()}")
