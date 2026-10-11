"""Final sweep, extra suite: the two remaining learner families as backbones.

XGBoost and a tabular transformer are the only model families not covered by any
frozen failure record and not in the T2 retrain suite. Both replace the LightGBM
backbone raw signal and are then scored through the released post-processing and
pooled blend unchanged, exactly like every other sweep candidate.

The transformer is an FT-Transformer-lite: one learned token per feature plus a
CLS token, two encoder layers, CLS readout, trained with the same per-day
cross-sectional IC loss the GRU used. Epochs are fixed in advance; there is no
inner validation split in this suite because nothing is selected between the two
candidates -- both are reported and the standing three-year gate decides.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import polars as pl
import torch
import torch.nn as nn

from run import FEATURE_FILE, ROOT, feature_names, fold_cutoff, to_matrix
from experiments.bonus_extension import (BASE_BONUS, BLEND_WEIGHT, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.final_sweep import blend_top_only, retention_scores, RELEASED
from experiments.official_seed_development import official_score
from experiments.sequence_model import apply_scaler, fit_scaler, load_panel as load_seq_panel
import experiments.sequence_training as st

OUT = ROOT / "experiments" / "final_sweep_eval"
KEYS = ["ts_code", "trade_date"]
FOLD_YEARS = (2022, 2023, 2024)
DEVELOPMENT_YEARS = (2022, 2023)
NUMERIC_TOLERANCE = 1e-12
SEED = 2026
XGB_ROUNDS = 180
TR_EPOCHS = 30
TR_DIM = 32
TR_LAYERS = 2
TR_HEADS = 4
TR_BATCH_DAYS = 4

CANDIDATES = [
    {"key": "T2f_xgboost_backbone", "variant": "xgboost"},
    {"key": "T2g_tabular_transformer", "variant": "transformer"},
]

PROTOCOL = {
    "experiment": "final_sweep_extra_learner_families",
    "candidates": CANDIDATES,
    "postprocess": "the released stack exactly: alpha 0.9, bonus 0.3, protected-block restoration "
                   "with top_current_weight 1.0, then the 25% top-only pooled blend",
    "scorer": "Unmodified evaluate.py via official_score",
    "development_years": list(DEVELOPMENT_YEARS),
    "diagnostic_year": 2024,
    "adoption_gate": "strict improvement over the released composite in 2022 AND 2023, then 2024; "
                     "identical to the T1 and T2 suites",
    "baseline_anchor": "the released backbone raw prediction through the same code path must "
                       "reproduce the released composite to 1e-12 in every scored year",
    "xgboost": {"rounds": XGB_ROUNDS, "max_depth": 7, "learning_rate": 0.05, "subsample": 0.85,
                "colsample_bytree": 0.85, "reg_lambda": 5.0, "tree_method": "hist",
                "device": "cuda if available else cpu", "seed": SEED},
    "transformer": {"dim": TR_DIM, "layers": TR_LAYERS, "heads": TR_HEADS, "epochs": TR_EPOCHS,
                    "batch_days": TR_BATCH_DAYS, "loss": "negative mean daily cross-sectional "
                    "Pearson correlation", "optimizer": "Adam lr 1e-3 weight_decay 1e-6",
                    "normalization": "nonfinite-aware per-feature mean/std on price-valid rows "
                                     "before the fold cutoff, clip +/-5, nonfinite to zero",
                    "seed": SEED},
    "prohibited_after_results": [
        "Retuning any hyper-parameter of either learner",
        "Selecting between the two candidates on development years and reporting only the winner",
        "Refitting the pooled auxiliary or the post-processing",
        "Modifying the release or any frozen source",
    ],
    "limitations": [
        "Both backbones are scored through a post-processing stack tuned on the LightGBM signal.",
        "2022-2024 are repeatedly examined historical years.",
        "The transformer has no inner validation split; its epoch count is fixed in advance.",
    ],
}


class TabularTransformer(nn.Module):
    def __init__(self, n_features: int, dim: int = TR_DIM, layers: int = TR_LAYERS,
                 heads: int = TR_HEADS):
        super().__init__()
        self.embed = nn.Linear(1, dim)
        self.cls = nn.Parameter(torch.zeros(1, 1, dim))
        nn.init.normal_(self.cls, std=0.02)
        encoder = nn.TransformerEncoderLayer(d_model=dim, nhead=heads, dim_feedforward=dim * 2,
                                             dropout=0.0, batch_first=True,
                                             activation="gelu")
        self.body = nn.TransformerEncoder(encoder, num_layers=layers)
        self.head = nn.Linear(dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch = x.shape[0]
        tokens = self.embed(x.unsqueeze(-1))                     # (B, F, D)
        cls = self.cls.expand(batch, -1, -1)
        tokens = torch.cat([cls, tokens], dim=1)                 # (B, F+1, D)
        out = self.body(tokens)
        return self.head(out[:, 0]).squeeze(-1)


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def write_protocol() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "protocol_extra.json"
    if path.exists():
        raise SystemExit("Extra protocol already frozen")
    payload = {**PROTOCOL, "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source_sha256": file_hash(Path(__file__))}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("Froze extra-suite protocol before any training")


def verify_protocol() -> dict:
    path = OUT / "protocol_extra.json"
    if not path.exists():
        raise SystemExit("Run the protocol stage first")
    protocol = json.loads(path.read_text(encoding="utf-8"))
    if protocol["source_sha256"] != file_hash(Path(__file__)):
        raise SystemExit("final_sweep_extra.py changed after its protocol was frozen; stop")
    return protocol


def train_transformer(z: np.ndarray, y: np.ndarray, valid: np.ndarray, dates: list[int],
                      cutoff: int) -> nn.Module:
    tensors = st.Tensors(dates, [str(i) for i in range(z.shape[1])], z, y, valid)
    train_days = [t for t, d in enumerate(dates) if d < cutoff and t >= 0]
    counts = tensors.mask.sum(dim=1)
    train_days = [t for t in train_days if int(counts[t]) >= 100]
    torch.manual_seed(SEED)
    model = TabularTransformer(tensors.features).to(st.DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-6)
    generator = np.random.default_rng(SEED)
    started = time.monotonic()
    for epoch in range(TR_EPOCHS):
        model.train()
        order = generator.permutation(np.asarray(train_days, dtype=np.int64))
        for start in range(0, len(order), TR_BATCH_DAYS):
            chunk = order[start:start + TR_BATCH_DAYS]
            if len(chunk) < 2:
                continue
            index = torch.as_tensor(chunk, device=st.DEVICE)
            x = tensors.z[index].reshape(-1, tensors.features)
            target = tensors.y[index]
            mask = tensors.mask[index]
            prediction = model(x).view(len(chunk), -1)
            ic, usable = st.daily_pearson_ic(prediction, target, mask)
            if not bool(usable.any()):
                continue
            loss = -ic[usable].mean()
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 10 == 0 or epoch + 1 == TR_EPOCHS:
            log(f"  transformer epoch {epoch + 1}/{TR_EPOCHS} elapsed {time.monotonic()-started:.0f}s")
    del tensors
    return model


def predict_transformer(model: nn.Module, z: np.ndarray, day_indices: list[int],
                        stocks: int, features: int) -> np.ndarray:
    model.eval()
    out = np.full((len(day_indices), stocks), np.nan, dtype=np.float32)
    device = next(model.parameters()).device
    with torch.no_grad():
        for start in range(0, len(day_indices), 8):
            chunk = day_indices[start:start + 8]
            x = torch.from_numpy(z[chunk]).to(device).reshape(-1, features)
            prediction = model(x).view(len(chunk), -1).float().cpu().numpy()
            out[start:start + len(chunk)] = prediction
    return out


def train() -> None:
    protocol = verify_protocol()
    result_path = OUT / "training_extra.json"
    if result_path.exists():
        raise SystemExit("Extra training results already recorded; preserving them")
    features = feature_names()
    dates, codes, x, y, valid, _ = load_seq_panel(features, 2024)
    record = {"generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "protocol_sha256": file_hash(OUT / "protocol_extra.json"), "candidates": {}}
    lazy = pl.scan_parquet(FEATURE_FILE)
    for candidate in CANDIDATES:
        variant = candidate["variant"]
        record["candidates"][candidate["key"]] = {}
        for year in FOLD_YEARS:
            cutoff = fold_cutoff(year)
            if variant == "xgboost":
                import xgboost as xgb
                train_frame = (lazy.filter(pl.col("is_train") & (pl.col("trade_date") < cutoff)
                                           & pl.col("y_rank").is_not_null() & pl.col("price_valid"))
                               .select(KEYS + features + ["y_rank"])
                               .sort("trade_date", "ts_code").collect())
                valid_frame = (lazy.filter(pl.col("trade_date").is_between(
                    year * 10000 + 101, year * 10000 + 1231))
                    .select(KEYS + features + ["price_valid"])
                    .sort("trade_date", "ts_code").collect())
                x_train = to_matrix(train_frame, features)
                label = train_frame["y_rank"].to_numpy().astype(np.float32)
                cfg = protocol["xgboost"]
                device = "cuda" if torch.cuda.is_available() else "cpu"
                model = xgb.XGBRegressor(n_estimators=XGB_ROUNDS, max_depth=cfg["max_depth"],
                                         learning_rate=cfg["learning_rate"],
                                         subsample=cfg["subsample"],
                                         colsample_bytree=cfg["colsample_bytree"],
                                         reg_lambda=cfg["reg_lambda"],
                                         tree_method=cfg["tree_method"], device=device,
                                         seed=SEED, n_jobs=16)
                started = time.monotonic()
                model.fit(x_train, label)
                elapsed = time.monotonic() - started
                matrix = to_matrix(valid_frame, features)
                raw = model.predict(matrix).astype(np.float64)
                raw[~valid_frame["price_valid"].to_numpy()] = -1e6
                del x_train, label, matrix, model
            else:
                mean, std, stats = fit_scaler(x, valid, dates, cutoff)
                z = apply_scaler(x, mean, std)
                model = train_transformer(z, y, valid, dates, cutoff)
                outer_days = [t for t, d in enumerate(dates)
                              if year * 10000 + 101 <= d <= year * 10000 + 1231]
                started = time.monotonic()
                raw_days = predict_transformer(model, z, outer_days, z.shape[1], z.shape[2])
                elapsed = time.monotonic() - started
                raw = raw_days.reshape(-1).astype(np.float64)
                raw[~valid[np.asarray(outer_days)].reshape(-1)] = -1e6
                raw[~np.isfinite(raw)] = -1e6
                del z, model
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                valid_frame = (lazy.filter(pl.col("trade_date").is_between(
                    year * 10000 + 101, year * 10000 + 1231))
                    .select(KEYS + ["price_valid"]).sort("trade_date", "ts_code").collect())
            cache = OUT / f"{candidate['key']}_{year}.parquet"
            valid_frame.select(KEYS).with_columns(pl.Series("pred_raw", raw)).write_parquet(
                cache, compression="zstd")
            record["candidates"][candidate["key"]][str(year)] = {
                "rows": int(len(raw)), "elapsed_seconds": elapsed,
                "cache": cache.relative_to(ROOT).as_posix(), "cache_sha256": file_hash(cache)}
            log(f"{candidate['key']} {year}: {len(raw):,} rows, {elapsed:.0f}s")
            del valid_frame, raw
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Wrote {result_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("protocol", "train", "develop"))
    arguments = parser.parse_args()
    if arguments.stage == "protocol":
        write_protocol()
    elif arguments.stage == "train":
        train()
    else:
        from experiments.final_sweep_extra_score import develop_extra
        develop_extra()
