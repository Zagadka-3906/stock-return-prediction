"""Freeze the MLP same-protocol training-period validation BEFORE any score exists.

Why this round exists: the 2026-09-29 unified-postprocess control showed the ten already-trained
neural nets had only ever been judged on their RAW output, and that with the released postprocess
stack MLP-h128 reaches 0.398590 on the reconstructed test slice, above every tree arm there. That
number is on the evaluation set and therefore inadmissible for selection. The only fair row for the
neural family in a model comparison is a 2020-2024 same-protocol validation, which does not exist:
every saved checkpoint is full-history-through-2024 and no fold weights were ever persisted. This
round trains the folds.

It is DESCRIPTIVE, not an adoption gate. All five years have been viewed repeatedly; a positive here
is selection-relevant evidence and, per the standing rule, cannot be acted on without a blind period.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "mlp_training_validation_20260929"

ARMS = ["mlp_h64", "mlp_h128"]
RECIPE = {"architecture": "mlp", "window": 1, "epochs": 27, "optimizer": "Adam",
          "learning_rate": 1e-3, "weight_decay": 1e-6, "torch_seed": 2026,
          "epoch_source": "the fixed historical best_epoch+1 of the saved fulltrain checkpoints "
                          "(early/neural_training_scope_audit.json records epochs=27 for both)"}
COMPARATORS = ["slow_only8", "peer67_slow8", "peer67_slow16", "base63_8", "top2"]
YEARS = [2020, 2021, 2022, 2023, 2024]

PINNED = [
    "experiments/sequence_training.py",
    "experiments/sequence_model.py",
    "analysis/all_models_test_20260929/early/train_neural.py",
    "analysis/all_models_test_20260929/early/neural_control_protocol.json",
    "experiments/final_sweep.py",
    "experiments/final_sweep_extra.py",
    "experiments/wave14_seed_average.py",
    "experiments/wave21_peer_lags.py",
    "experiments/revalidate_fold_local.py",
    "evaluate.py",
    "run.py",
    "src/scoring.py",
]

RULES = {
    "fold_boundary": "identical to the tree arms: w21.fold(year)['cutoff'] (run.py fold_cutoff), the "
                     "last training signal date before 1 Jan of the validation year, excluded "
                     "because its label matures at the next close",
    "postprocess": "w14.stacked(bundle, raw): the PER-FOLD pooled auxiliary raw carried in the fold "
                   "bundle plus the frozen stack alpha=0.9, bonus=0.3, restore_lower, "
                   "top_current_weight=1.0, auxiliary top_only 0.25. The frozen full-history "
                   "auxiliary (releases/pooled_rms25/auxiliary_raw.parquet) is PROHIBITED here: it "
                   "was trained through 2024-12-31 and would leak into 2020-2024.",
    "scorer": "revalidate_fold_local.score_official -> unmodified evaluate.py",
    "interpretation": "descriptive only; NOT an adoption gate; no arm is promoted or rejected here",
    "reporting": "per-year composite, five-year equal-weight mean, worst year, and paired 20-day "
                 "moving-block bootstrap CI95 of each MLP arm against slow_only8 and against "
                 "peer67_slow8 on the daily official terms",
    "prohibited": [
        "tuning epochs, hidden size, window, optimizer or seed on these years",
        "using the frozen full-history pooled auxiliary",
        "reading any 2025-2026 return label or score",
        "relaxing any rule after seeing a score",
        "writing outside analysis/mlp_training_validation_20260929/",
    ],
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "protocol.json"
    if target.exists():
        raise SystemExit("protocol.json already exists; never re-freeze in place")
    for relative in PINNED:
        if not (ROOT / relative).exists():
            raise SystemExit(f"pinned source missing: {relative}")
    payload = {
        "experiment": "mlp_same_protocol_training_period_validation",
        "status": "frozen_before_any_score",
        "frozen_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "role": RULES["interpretation"],
        "arms": ARMS, "recipe": RECIPE, "comparators": COMPARATORS, "years": YEARS,
        "rules": RULES,
        "pinned_sha256": {r: sha(ROOT / r) for r in PINNED},
        "environment": {"python": sys.version.split()[0]},
    }
    try:
        import torch
        payload["environment"]["torch"] = torch.__version__
    except Exception as exc:  # pragma: no cover - environment fact only
        payload["environment"]["torch"] = f"unavailable: {exc}"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"frozen {target}")
    print(f"protocol sha256 {sha(target)}")


if __name__ == "__main__":
    freeze()
