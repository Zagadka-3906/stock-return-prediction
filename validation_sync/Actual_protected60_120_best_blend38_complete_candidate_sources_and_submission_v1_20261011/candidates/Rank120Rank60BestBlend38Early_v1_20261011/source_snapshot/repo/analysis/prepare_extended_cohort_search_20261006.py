"""Prepare a wider training-only binning, shrinkage and blending comparison."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import sha, create


def main():
    source = A / 'cohort_rank_calibration_20261006.py'
    text = source.read_text(encoding='utf-8')
    old = 'assert bins in (32, 128) and pseudocount in (0., 200.)'
    new = 'assert bins in (8, 16, 32, 64, 128, 256) and pseudocount in (0., 50., 200., 1000.)'
    assert text.count(old) == 1
    extended = text.replace(old, new)
    assert extended.replace(new, old) == text
    destination = A / 'cohort_rank_calibration_v2_20261006.py'
    compile(extended, str(destination), 'exec')
    with destination.open('x', encoding='utf-8') as stream:
        stream.write(extended)
    create(A / 'extended_cohort_search_preparation_20261006.json', {
        'status': 'prepared_unscored_extended_cohort_bin_shrink_blend_search',
        'input_sha256': {str(source): sha(source), str(destination): sha(destination), str(Path(__file__)): sha(__file__)},
        'entire_math_source_exact_except_admitted_bin_and_pseudocount_values': True,
        'new_cases': 64, 'comparison_anchors': 2, 'expected_actual_scored_records': 66,
        'new_grid': {'bins': [8, 16, 64, 256], 'pseudocount': [0., 50., 200., 1000.], 'weight': [.25, .5, .75, 1.]},
        'anchors': [{'weight': 0., 'bins': None, 'pseudocount': None}, {'weight': 1., 'bins': 32, 'pseudocount': 0.}],
        'mature_original_fold_cutoffs_and_all_full_controls_required': True,
        'new_quality_scores': 0, 'new_native_base_model_fits': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
