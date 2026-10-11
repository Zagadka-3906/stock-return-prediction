"""Establish the clean bar a sequence model must clear.

The released 2022 Rank IC of 0.118468 is measured *after* EMA smoothing, the Top
persistence bonus, protected-block rank restoration and the 25% pooled blend. A
new model family should first be compared against the raw LightGBM backbone with
none of that post-processing, otherwise the comparison conflates model quality
with a post-processing stack tuned on the same years.

Read-only: loads the frozen fold caches and calls the unmodified evaluator.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from run import ROOT
from experiments.bonus_extension import (AUXILIARY, BASE_BONUS, BLEND_WEIGHT, FOLD,
                                         blend_top_only, file_hash, load_auxiliary,
                                         load_panel, release_scores)
from experiments.official_seed_development import official_score

OUT = ROOT / "experiments" / "sequence_model_eval"
YEARS = (2022, 2023, 2024)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "reference_bars.json"
    if path.exists():
        raise SystemExit("Reference bars already recorded; preserving them")
    started = time.monotonic()
    released = release_scores()
    years = {}
    for year in YEARS:
        panel = load_panel(year)
        auxiliary = load_auxiliary(year, panel)
        backbone_raw = panel.frame["pred_raw"].to_numpy().astype(np.float64)
        blended = blend_top_only(panel, auxiliary, BASE_BONUS, BLEND_WEIGHT)

        raw = official_score(panel, backbone_raw, year)[0]
        aux = official_score(panel, np.asarray(auxiliary, dtype=np.float64), year)[0]
        full = official_score(panel, blended, year)[0]
        years[str(year)] = {
            "backbone_raw_no_postprocess": {k: float(v) for k, v in raw.items()},
            "pooled_auxiliary_raw_no_postprocess": {k: float(v) for k, v in aux.items()},
            "released_full_pipeline": {k: float(v) for k, v in full.items()},
            "released_pipeline_matches_authority":
                abs(full["final_score"] - released[year]) <= 1e-12,
        }
        print(f"{year}  backbone raw IC={raw['ic_mean']:.6f} score={raw['final_score']:.6f} | "
              f"auxiliary raw IC={aux['ic_mean']:.6f} | "
              f"released IC={full['ic_mean']:.6f} score={full['final_score']:.6f}", flush=True)
        if not years[str(year)]["released_pipeline_matches_authority"]:
            raise AssertionError(f"{year}: released pipeline does not reproduce the authority score")
        del panel, auxiliary, blended

    output = {
        "generated_at_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": time.monotonic() - started,
        "purpose": "Separate the raw model bar from the post-processed released bar so a new "
                   "model family is compared against the right baseline.",
        "scorer": "Unmodified evaluate.py via official_score: float17 CSV round trip, original "
                  "Float64 labels, pandas default descending tie order.",
        "years": years,
        "gate_for_sequence_model": {
            "primary_bar": "backbone_raw_no_postprocess ic_mean per year",
            "secondary_bar": "released_full_pipeline ic_mean per year",
            "note": "A sequence model is first judged on raw IC against the raw backbone. Only a "
                    "model that clears the raw bar is worth putting through the released "
                    "post-processing stack, and only then can a composite score be compared.",
        },
        "source_and_input_sha256": {
            str(Path(__file__).relative_to(ROOT)).replace("\\", "/"): file_hash(Path(__file__)),
            "experiments/bonus_extension.py": file_hash(ROOT / "experiments/bonus_extension.py"),
            "evaluate.py": file_hash(ROOT / "evaluate.py"),
            **{FOLD.format(year=y): file_hash(ROOT / FOLD.format(year=y)) for y in YEARS},
            **{AUXILIARY.format(year=y): file_hash(ROOT / AUXILIARY.format(year=y)) for y in YEARS},
        },
    }
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {path}", flush=True)


if __name__ == "__main__":
    main()
