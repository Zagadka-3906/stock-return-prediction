"""Fixed, paired feature-identity repair experiment; never publishes a release."""
from __future__ import annotations

import argparse
import copy
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import time

os.environ.setdefault("POLARS_MAX_THREADS", "6")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import polars as pl
import torch
from torch import nn
from loguru import logger

from run import FEATURE_FILE, feature_names, fold_cutoff
from src.scoring import Panel, make_scores
from experiments.final_sweep_extra import TabularTransformer
from experiments.sequence_model import load_panel, fit_scaler, apply_scaler
from experiments.sequence_training import daily_pearson_ic
from experiments.cached_recheck import make_prediction
from experiments.revalidate_fold_local import score_official
from experiments.optimize_r5_models import load_year

OUT = ROOT / "experiments/r6_transformer_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
KEYS = ["ts_code", "trade_date"]
DEVELOPMENT = (2020, 2021, 2022)
CONFIRMATION = (2023, 2024)
VARIANTS = ("shared", "feature_identity")
CONFIG = {"seed": 2026, "epochs": 30, "batch_days": 4,
          "dim": 32, "layers": 2, "heads": 4, "learning_rate": .001,
          "weight_decay": 1e-6, "alpha": .9, "bonus": .3, "pooled": .25,
          "precision": "float32; TF32 disabled", "threads": 4}
GATES = {
    "development": {"mean_score_delta_min": .001, "worst_year_score_delta_min": -.005, "mean_ic_delta_min": -.002},
    "confirmation": {"mean_score_delta_min": .0005, "worst_year_score_delta_min": -.003, "mean_ic_delta_min": -.002},
    "bootstrap": {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share": .8},
}


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("x", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)


class FeatureIdentity(nn.Module):
    def __init__(self, original, features):
        super().__init__()
        # Same initial function and encoder/readout; independent column updates.
        self.weight = nn.Parameter(original.embed.weight.detach().T.repeat(features, 1))
        self.bias = nn.Parameter(original.embed.bias.detach().repeat(features, 1))
        self.cls = nn.Parameter(original.cls.detach().clone())
        self.body = copy.deepcopy(original.body)
        self.head = copy.deepcopy(original.head)

    def forward(self, x):
        tokens = x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)
        tokens = torch.cat([self.cls.expand(x.shape[0], -1, -1), tokens], dim=1)
        return self.head(self.body(tokens)[:, 0]).squeeze(-1)


def build_model(variant, features):
    torch.manual_seed(CONFIG["seed"])
    old = TabularTransformer(features, CONFIG["dim"], CONFIG["layers"], CONFIG["heads"])
    return old if variant == "shared" else FeatureIdentity(old, features)


def configure():
    torch.set_num_threads(CONFIG["threads"])
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    # Same eager inference path at all batch sizes; no nested tensor conversion.
    torch.backends.mha.set_fastpath_enabled(False)
    logger.disable("evaluate")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def tests():
    device = configure()
    old = build_model("shared", 63).double()
    new = build_model("feature_identity", 63).double()
    assert all(torch.equal(v, new.body.state_dict()[k]) for k, v in old.body.state_dict().items())
    assert torch.equal(old.cls, new.cls)
    assert all(torch.equal(v, new.head.state_dict()[k]) for k, v in old.head.state_dict().items())
    rng = np.random.default_rng(2026)
    x = torch.from_numpy(rng.normal(size=(128, 63)))
    y = torch.from_numpy(rng.normal(size=(2, 64)))
    mask = torch.ones_like(y, dtype=torch.bool)
    old.eval(); new.eval()
    with torch.no_grad():
        initial = float((old(x) - new(x)).abs().max())
        assert initial < 1e-12
        permutation = torch.arange(62, -1, -1)
        assert float((old(x) - old(x[:, permutation])).abs().max()) < 1e-12
    # Train only synthetic data: symmetry must break after a real optimizer step.
    optimizer = torch.optim.Adam(new.parameters(), lr=.001, weight_decay=1e-6)
    prediction = new(x).view(2, 64)
    loss = ((prediction - y) ** 2).mean()
    optimizer.zero_grad(); loss.backward()
    assert (new.weight.grad[1:] - new.weight.grad[:1]).abs().max() > 1e-8
    optimizer.step()
    assert torch.isfinite(new.weight.grad).all()
    with torch.no_grad():
        symmetry_difference = float((new(x) - new(x[:, permutation])).abs().max())
        assert symmetry_difference > 1e-7
        jointly_permuted = copy.deepcopy(new)
        jointly_permuted.weight.copy_(new.weight[permutation])
        jointly_permuted.bias.copy_(new.bias[permutation])
        joint_difference = float((new(x) - jointly_permuted(x[:, permutation])).abs().max())
        assert joint_difference < 1e-12
    # Actual scaler must ignore all later rows when fitting.
    a = rng.normal(size=(30, 80, 3)).astype(np.float32)
    a[0, 0] = np.nan
    valid = np.ones(a.shape[:2], bool)
    dates = list(range(30))
    mean, std, _ = fit_scaler(a, valid, dates, 20)
    changed = a.copy(); changed[20:] = 1e10
    m2, s2, _ = fit_scaler(changed, valid, dates, 20)
    assert np.array_equal(mean, m2) and np.array_equal(std, s2)
    # Hardware-only smoke uses the exact full batch shape, never market data.
    model = build_model("feature_identity", 63).to(device)
    large = torch.zeros((4 * 4650, 63), device=device)
    target = torch.linspace(-.5, .5, 4650, device=device).repeat(4, 1)
    usable = torch.ones_like(target, dtype=torch.bool)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(); torch.cuda.synchronize()
    start = time.monotonic()
    output = model(large).reshape(4, 4650)
    # Nonconstant X so the IC gradient represents the training path.
    del output
    large[:, 0] = target.reshape(-1)
    output = model(large).reshape(4, 4650)
    ic, keep = daily_pearson_ic(output, target, usable)
    (-ic[keep].mean()).backward()
    assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
    if device.type == "cuda":
        torch.cuda.synchronize()
    result = {"status": "passed", "same_initial_function_max_abs": initial,
              "source_sha256": sha(Path(__file__)), "identical_body_cls_head": True,
              "feature_gradients_differ": True, "joint_value_identity_permutation_max_abs": joint_difference,
              "repair_breaks_symmetry_after_synthetic_step": symmetry_difference,
              "scaler_future_invariance": True, "full_shape_smoke_seconds": time.monotonic()-start,
              "device": str(device), "peak_gpu_bytes": torch.cuda.max_memory_allocated() if device.type == "cuda" else None}
    write_new(OUT / "tests.json", result)
    log(json.dumps(result))


def freeze():
    test_record = read(OUT / "tests.json")
    assert test_record["status"] == "passed" and test_record["source_sha256"] == sha(Path(__file__))
    from experiments import r6_transformer_audit
    audit_test = read(OUT / "audit_tests_final.json")
    assert audit_test["status"] == "passed" and audit_test["source_sha256"] == sha(Path(r6_transformer_audit.__file__))
    from experiments.verify_r5_results import verify as verify_r5
    assert verify_r5()["status"] == "passed"
    # Pin imported local implementation dependencies, including independent audit.
    files = {Path(__file__).resolve(), FEATURE_FILE, ROOT / "data/feature_manifest.json",
             ROOT / "data" / "raw" / "训练集.csv", ROOT / "active_release.json", OUT / "tests.json", OUT / "audit_tests_final.json",
             R4 / "summary.json", ROOT / "releases/ensemble4_r4/release_manifest.json"}
    for module in list(sys.modules.values()):
        path = getattr(module, "__file__", None)
        if path and Path(path).is_absolute() and Path(path).is_file() and Path(path).resolve().is_relative_to(ROOT) and ".venv" not in Path(path).parts:
            files.add(Path(path).resolve())
    for year in DEVELOPMENT + CONFIRMATION:
        files.add(R4 / f"result_{year}.json")
        for key in ("baseline", "ensemble4"):
            files.add(R4 / f"predictions_{key}_{year}.parquet")
    sources = read(ROOT / "experiments/research_r6_20260926/research_manifest.json")
    for relative, digest in sources["artifact_sha256"].items():
        assert sha(ROOT / relative) == digest
    protocol = {
        "experiment": "paired_transformer_feature_identity_repair",
        "primary_candidate": "feature_identity", "control": "shared",
        "config": CONFIG, "gates": GATES,
        "development_years": list(DEVELOPMENT), "confirmation_years": list(CONFIRMATION),
        "retrospective_previously_viewed": True,
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "training": "63 existing features, expanding history strictly before fold_cutoff; one-day label purge; all selected rows asserted is_train. Exactly 30 epochs, no epoch/seed/weight search.",
        "loss": "negative mean daily Pearson correlation against existing Float32 y_rank; only price-valid finite train labels; shuffle past training dates for SGD, never across folds",
        "normalization": "unchanged nonfinite-aware past-only scaler; unchanged apply_scaler clips +/-5 before zeroing NaN (input infinities become +/-5); identical in both arms",
        "initialization": "shared encoder/CLS/head and identical initial function. Shared weight/bias copied per feature as independent Parameters; different parameter count disclosed.",
        "postprocess": "raw replaces primary backbone; unchanged .9 EMA/.3 retention/protected current rank/top-only .25 pooled; no new model blend",
        "mechanism_gate": "feature_identity minus shared mean official score >0 AND mean raw RankIC >0 over all three development years",
        "early_futility": "After completing both arms for a development year, stop if primary minus either baseline score is strictly below -0.005. This irrevocably violates the predeclared worst-year gate; later years cannot rescue it. Only a chronological prefix may be completed.",
        "confirmation_control": "only fixed feature_identity evaluated if both development and mechanism gates pass; no runner-up",
        "checkpoint_rule": "latest completed epoch only; resume exact optimizer/RNG state; always use epoch30, never select checkpoint by validation",
        "claim_limit": "Even historical gate success does not establish new independent superiority; no automatic publication in this research run.",
        "versions": {"torch": torch.__version__, "numpy": np.__version__, "polars": pl.__version__,
                     "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None},
        "input_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(files)},
    }
    write_new(OUT / "protocol.json", protocol)
    log("Protocol frozen before any market training or candidate scoring")


def verify_protocol():
    p = read(OUT / "protocol.json")
    assert p["config"] == CONFIG and p["gates"] == GATES
    for relative, digest in p["input_sha256"].items():
        assert sha(ROOT / relative) == digest, relative
    return p


def predict_array(model, z, device):
    model.eval()
    result = np.empty(z.shape[:2], np.float32)
    with torch.no_grad():
        for start in range(0, len(z), 8):
            a = torch.from_numpy(z[start:start+8]).to(device)
            result[start:start+8] = model(a.reshape(-1, z.shape[2])).view(a.shape[:2]).cpu().numpy()
    assert np.isfinite(result).all()
    return result


def train_fold(year, keys):
    device = configure()
    features = feature_names()
    assert len(features) == 63
    dates, codes, x, y, valid, is_train = load_panel(features, year)
    before = np.asarray(dates) < fold_cutoff(year)
    outer = np.asarray([year*10000+101 <= d <= year*10000+1231 for d in dates])
    assert is_train[before | outer].all()
    first_outer = np.flatnonzero(outer)[0]
    assert np.flatnonzero(before)[-1]+1 < first_outer
    mean, std, stats = fit_scaler(x, valid, dates, fold_cutoff(year))
    z = apply_scaler(x, mean, std)
    del x; gc.collect()
    scaler_path = OUT / f"scaler_{year}.npz"
    if scaler_path.exists():
        with np.load(scaler_path) as old:
            assert np.array_equal(old["mean"], mean) and np.array_equal(old["std"], std)
    else:
        np.savez(scaler_path, mean=mean, std=std)
    training_mask = valid[before] & np.isfinite(y[before])
    train_days = np.flatnonzero(training_mask.sum(1) >= 100)
    train_z = torch.from_numpy(z[before]).to(device)
    train_y = torch.from_numpy(np.nan_to_num(y[before], nan=0.)).to(device)
    train_mask = torch.from_numpy(training_mask).to(device)
    outer_z = np.ascontiguousarray(z[outer]); del z; gc.collect()
    for key in keys:
        metadata = OUT / f"training_{key}_{year}.json"
        if metadata.exists():
            old = read(metadata)
            for relative, digest in old["artifact_sha256"].items():
                assert sha(OUT / relative) == digest
            continue
        model = build_model(key, len(features)).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=CONFIG["learning_rate"], weight_decay=CONFIG["weight_decay"])
        generator = np.random.default_rng(CONFIG["seed"])
        checkpoint = OUT / f"checkpoint_{key}_{year}.pt"
        curve, start_epoch, prior_elapsed = [], 0, 0.
        if checkpoint.exists():
            saved = torch.load(checkpoint, map_location=device, weights_only=False)
            assert saved["protocol_sha256"] == sha(OUT / "protocol.json")
            assert saved["scaler_sha256"] == sha(scaler_path)
            model.load_state_dict(saved["model"]); optimizer.load_state_dict(saved["optimizer"])
            generator.bit_generator.state = saved["shuffle_rng"]
            curve, start_epoch, prior_elapsed = saved["curve"], saved["epoch"], saved["elapsed"]
            del saved
        start = time.monotonic()
        log(f"{year} {key}: train_days={len(train_days)}, params={sum(p.numel() for p in model.parameters())}, resume_epoch={start_epoch}")
        for epoch in range(start_epoch, CONFIG["epochs"]):
            model.train(); losses = []
            order = generator.permutation(train_days)
            for left in range(0, len(order), CONFIG["batch_days"]):
                chunk = order[left:left+CONFIG["batch_days"]]
                if len(chunk) < 2:
                    continue
                index = torch.as_tensor(chunk, device=device)
                prediction = model(train_z[index].reshape(-1, len(features))).view(len(chunk), -1)
                ic, usable = daily_pearson_ic(prediction, train_y[index], train_mask[index])
                loss = -ic[usable].mean()
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"Nonfinite train loss {year} {key} {epoch}")
                optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
                losses.append(float(loss.detach()))
            curve.append({"epoch": epoch+1, "mean_train_loss": float(np.mean(losses)), "batches": len(losses)})
            elapsed = prior_elapsed + time.monotonic()-start
            torch.save({"epoch": epoch+1, "model": model.state_dict(), "optimizer": optimizer.state_dict(),
                        "shuffle_rng": generator.bit_generator.state, "curve": curve, "elapsed": elapsed,
                        "protocol_sha256": sha(OUT / "protocol.json"), "scaler_sha256": sha(scaler_path)}, checkpoint)
            log(f"{year} {key}: epoch {epoch+1}/30 loss={curve[-1]['mean_train_loss']:.6f} elapsed={elapsed:.0f}s")
        model_path = OUT / f"model_{key}_{year}.pt"
        torch.save({"state_dict": model.state_dict(), "variant": key, "features": features,
                    "config": CONFIG, "protocol_sha256": sha(OUT / "protocol.json")}, model_path)
        training_seconds = prior_elapsed + time.monotonic()-start
        inference_start = time.monotonic()
        raw = predict_array(model, outer_z, device)
        prefix = predict_array(model, outer_z[:16], device)
        assert np.array_equal(prefix, raw[:16]), "Neural raw prefix changed"
        raw[~valid[outer]] = -1e6
        raw_path = OUT / f"raw_{key}_{year}.parquet"
        pl.DataFrame({"trade_date": np.repeat(np.asarray(dates)[outer], len(codes)),
                      "ts_code": np.tile(codes, outer.sum()), "pred_raw": raw.reshape(-1)}).write_parquet(raw_path, compression="zstd")
        write_new(metadata, {"year": year, "variant": key, "training_cutoff_exclusive": fold_cutoff(year),
                            "last_training_date": int(np.asarray(dates)[before][-1]),
                            "last_label_available_date": int(dates[np.flatnonzero(before)[-1]+1]),
                            "first_validation_date": int(np.asarray(dates)[outer][0]),
                            "training_days": len(train_days), "training_rows": int(training_mask.sum()),
                            "train_state_has_only_past_rows": True, "feature_count": len(features),
                            "parameter_count": sum(p.numel() for p in model.parameters()),
                            "epochs": CONFIG["epochs"], "training_seconds": training_seconds,
                            "inference_and_output_seconds": time.monotonic()-inference_start,
                            "elapsed_seconds": prior_elapsed+time.monotonic()-start,
                            "scaler_stats": stats, "curve": curve, "raw_16day_prefix_exact": True,
                            "artifact_sha256": {p.name: sha(p) for p in (model_path, raw_path, scaler_path, checkpoint)}})
        del model, optimizer, raw; gc.collect()
        if device.type == "cuda": torch.cuda.empty_cache()
    del train_z, train_y, train_mask, outer_z; gc.collect()
    if device.type == "cuda": torch.cuda.empty_cache()


def post(frame, raw):
    panel = Panel.from_frame(frame.with_columns(pl.Series("pred_raw", raw)))
    return make_prediction(panel, frame["aux_raw"].to_numpy(), "top_only", .25)


def score_fold(year, keys):
    target = OUT / f"fold_{year}.json"
    if target.exists():
        r = read(target)
        assert r["candidate_keys"] == keys
        for relative, digest in r["artifact_sha256"].items(): assert sha(OUT / relative) == digest
        return r
    frame, _, provenance = load_year(year)
    expected = read(R4 / "summary.json")["metrics"][str(year)]
    result = {"year": year, "candidate_keys": keys, "references": {}, "candidates": {}, "provenance": provenance}
    for key in ("baseline", "ensemble4"):
        reference = pl.read_parquet(R4 / f"predictions_{key}_{year}.parquet").sort("trade_date", "ts_code")
        assert frame.select(KEYS).equals(reference.select(KEYS))
        metrics, daily = score_official(frame, reference["pred"].to_numpy())
        assert all(abs(v-expected[key][k]) < 1e-12 for k,v in metrics.items())
        result["references"][key] = metrics
        daily.write_csv(OUT / f"daily_{key}_{year}.csv")
    for key in keys:
        raw_frame = pl.read_parquet(OUT / f"raw_{key}_{year}.parquet").sort("trade_date", "ts_code")
        assert raw_frame.select(KEYS).equals(frame.select(KEYS))
        raw = raw_frame["pred_raw"].to_numpy().astype(float)
        pred = post(frame, raw)
        corrupted = frame.with_columns(pl.lit(123456.).alias("y_ret_1d"), pl.lit(False).alias("future_available"))
        assert np.array_equal(pred, post(corrupted, raw))
        count = 50 * frame["ts_code"].n_unique()
        assert np.array_equal(pred[:count], post(frame.head(count), raw[:count]))
        assert np.isfinite(pred).all() and (pred[~frame["price_valid"].to_numpy()] < -1).all()
        metrics, daily = score_official(frame, pred)
        raw_rank = make_scores(Panel.from_frame(frame), raw, 0.)
        raw_metrics, raw_daily = score_official(frame, raw_rank)
        daily.write_csv(OUT / f"daily_{key}_{year}.csv")
        raw_daily.write_csv(OUT / f"daily_raw_{key}_{year}.csv")
        frame.with_columns(pl.Series("pred_raw", raw), pl.Series("pred", pred)).write_parquet(OUT / f"predictions_{key}_{year}.parquet", compression="zstd")
        result["candidates"][key] = {"metrics": metrics, "raw_metrics": raw_metrics,
            "tests": {"label_invariance": True, "future_availability_ignored": True,
                      "postprocess_50day_prefix_exact": True, "all_finite": True, "invalid_price_low": True}}
        log(f"{year} {key} rawIC={raw_metrics['ic_mean']:.6f} score={metrics['final_score']:.9f}")
    result["artifact_sha256"] = {p.name: sha(p) for p in OUT.glob(f"*_{year}.*") if p != target}
    write_new(target, result)
    return result


def gate(folds, stage):
    thresholds = GATES[stage]
    comparisons = {}
    for key in ("baseline", "ensemble4"):
        score = [f["candidates"]["feature_identity"]["metrics"]["final_score"]-f["references"][key]["final_score"] for f in folds]
        ic = [f["candidates"]["feature_identity"]["metrics"]["ic_mean"]-f["references"][key]["ic_mean"] for f in folds]
        comparisons[key] = {"score_deltas": dict(zip([str(f["year"]) for f in folds], score)), "mean_score_delta": float(np.mean(score)), "worst_year_score_delta": min(score),
                            "mean_ic_delta": float(np.mean(ic)), "passed": bool(np.mean(score) >= thresholds["mean_score_delta_min"] and min(score) >= thresholds["worst_year_score_delta_min"] and np.mean(ic) >= thresholds["mean_ic_delta_min"])}
    return {"comparisons": comparisons, "passed": all(c["passed"] for c in comparisons.values()),
            "mean_official_score": float(np.mean([f["candidates"]["feature_identity"]["metrics"]["final_score"] for f in folds]))}


def develop():
    verify_protocol()
    if (OUT / "development.json").exists(): raise FileExistsError("Development already completed")
    folds = []
    early_stop = None
    for year in DEVELOPMENT:
        train_fold(year, list(VARIANTS))
        folds.append(score_fold(year, list(VARIANTS)))
        latest = folds[-1]
        if any(latest["candidates"]["feature_identity"]["metrics"]["final_score"] - latest["references"][ref]["final_score"] < GATES["development"]["worst_year_score_delta_min"] for ref in ("baseline", "ensemble4")):
            early_stop = "hard_worst_year_gate_failed"
            break
    aggregate = gate(folds, "development")
    score_delta = float(np.mean([f["candidates"]["feature_identity"]["metrics"]["final_score"]-f["candidates"]["shared"]["metrics"]["final_score"] for f in folds]))
    ic_delta = float(np.mean([f["candidates"]["feature_identity"]["raw_metrics"]["ic_mean"]-f["candidates"]["shared"]["raw_metrics"]["ic_mean"] for f in folds]))
    mechanism = {"mean_score_delta_vs_shared": score_delta, "mean_raw_ic_delta_vs_shared": ic_delta,
                 "partial": len(folds) != len(DEVELOPMENT), "observed_improvement": score_delta > 0 and ic_delta > 0,
                 "passed": len(folds) == len(DEVELOPMENT) and score_delta > 0 and ic_delta > 0}
    verify_protocol()
    write_new(OUT / "development.json", {"primary_candidate": "feature_identity", "protocol_sha256": sha(OUT / "protocol.json"),
              "aggregate": aggregate, "mechanism_gate": mechanism,
              "development_gate_passed": len(folds) == len(DEVELOPMENT) and aggregate["passed"] and mechanism["passed"],
              "completed_years": [f["year"] for f in folds], "early_stop_reason": early_stop,
              "partial_mechanism_is_descriptive_only": len(folds) != len(DEVELOPMENT),
              "fold_sha256": {f"fold_{f['year']}.json": sha(OUT / f"fold_{f['year']}.json") for f in folds}})


def confirm():
    verify_protocol()
    d = read(OUT / "development.json")
    assert d["protocol_sha256"] == sha(OUT / "protocol.json")
    assert d["development_gate_passed"], "Development failed; confirmation prohibited"
    assert d["completed_years"] == list(DEVELOPMENT)
    for relative, digest in d["fold_sha256"].items(): assert sha(OUT / relative) == digest
    folds = [score_fold(y, list(VARIANTS)) for y in DEVELOPMENT]
    assert gate(folds, "development") == d["aggregate"]
    from experiments.r6_transformer_audit import _frozen_development
    _frozen_development()
    audit = read(OUT / "independent_audit/development/score_audit.json")
    assert audit["status"] == "passed" and audit["stage_gate_passed"]
    assert audit["stage_record_sha256"] == sha(OUT / "development.json")
    if (OUT / "confirmation.json").exists(): raise FileExistsError("Confirmation completed")
    from experiments.audit_r5_candidate import paired_block_bootstrap
    folds = []
    for year in CONFIRMATION:
        train_fold(year, ["feature_identity"])
        folds.append(score_fold(year, ["feature_identity"]))
    aggregate = gate(folds, "confirmation")
    candidate = {y: pl.read_csv(OUT / f"daily_feature_identity_{y}.csv") for y in CONFIRMATION}
    bootstrap = {key: paired_block_bootstrap(candidate, {y: pl.read_csv(OUT / f"daily_{key}_{y}.csv") for y in CONFIRMATION}, block_days=20, draws=20000, seed=2026) for key in ("baseline", "ensemble4")}
    passed = aggregate["passed"] and all(v["bootstrap_share_positive"] >= .8 for v in bootstrap.values())
    write_new(OUT / "confirmation.json", {"primary_candidate": "feature_identity", "protocol_sha256": sha(OUT / "protocol.json"),
              "development_sha256": sha(OUT / "development.json"), "aggregate": aggregate, "bootstrap": bootstrap,
              "official_and_noise_gate_passed": passed, "no_publication": True,
              "fold_sha256": {f"fold_{y}.json": sha(OUT / f"fold_{y}.json") for y in CONFIRMATION}})


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("stage", choices=("test", "freeze", "develop", "confirm", "verify"))
    selected = args.parse_args().stage
    configure()
    {"test": tests, "freeze": freeze, "develop": develop, "confirm": confirm, "verify": verify_protocol}[selected]()
