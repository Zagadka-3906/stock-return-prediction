"""Extend the attained residual boundary using the unchanged full official controls."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
SOURCE = A / 'run_conditional_flag_residual_official_comparison_20261006.py'
OUT = A / 'conditional_residual_extrapolation43_official_20261006'


def main():
    registration = A / 'service_owned_workflows_20261006/conditional_residual_round102_full_registration'
    identity = read(registration / 'native_launch.json')
    while owned(identity):
        time.sleep(30)
    assert read(registration / 'service_execution.json')['status'] == 'passed'
    receipt = A / 'github_validation_sync_main_20261005/round102_receipt.json'
    assert read(receipt)['actual_full_QA_version'] == 13
    assert read(receipt)['scored_records'] == 49 and read(receipt)['full_immutable_ranking_and_all_original_QA_preserved']
    parent = A / 'optimization_20261003_r102'
    assert read(parent / 'provenance_scope_execution.json')['status'] == 'passed'
    original_transform = (A / 'conditional_flag_residual_transform_20261006.py').read_text(encoding='utf-8')
    extended_transform = (A / 'conditional_flag_residual_extrapolation_transform_20261006.py').read_text(encoding='utf-8')
    original_body = original_transform[original_transform.index('import numpy'):]
    extended_body = extended_transform[extended_transform.index('import numpy'):]
    assert original_body.replace('<= 1.', '<= 8.') == extended_body
    evidence = [SOURCE, A / 'conditional_flag_residual_extrapolation_transform_20261006.py',
        A / 'conditional_flag_residual_transform_20261006.py', receipt,
        parent / 'selected_validation.npy', parent / 'selection.json',
        parent / 'calibrated_csv_official.json', parent / 'provenance_scope_execution.json']
    pins = {str(p): sha(p) for p in evidence}
    text = SOURCE.read_text(encoding='utf-8')
    before = "cases = [{'model': None, 'weight': 0.}]"
    assert text.count(before) == 1
    patches = {
        "conditional_flag_residual_official_comparison_20261006'": "conditional_residual_extrapolation43_official_20261006'",
        'from conditional_flag_residual_transform_20261006 import transform':
            'from conditional_flag_residual_extrapolation_transform_20261006 import transform',
        before: "cases = [{'model': 'equal_mean_three_feature_residuals', 'weight': 1.}]",
        '(.01, .025, .05, .1, .25, .5, .75, 1.)': '(1.25, 1.5, 2., 3., 4., 6., 8.)',
        'assert len(cases) == 49': 'assert len(cases) == 43',
        "baseline = read(parent / 'calibrated_csv_official.json')['metrics']":
            "baseline = read(A / 'optimization_20261003_r102/calibrated_csv_official.json')['metrics']",
        "sources = [Path(__file__), A / 'conditional_flag_residual_transform_20261006.py',":
            "sources = [*EXTRAPOLATION_EVIDENCE, Path(__file__), A / 'conditional_flag_residual_extrapolation_transform_20261006.py',",
        "'explicit_parent_round': 100": "'explicit_parent_round': 102, 'residual_calculation_parent_round': 100",
        "'all49_final_past_return_mapped_CSVs_original_official_scored'": "'all43_final_past_return_mapped_CSVs_original_official_scored'",
        "assert np.array_equal(values.view(np.uint64), np.asarray(raw).view(np.uint64))":
            "assert np.array_equal(values.view(np.uint64), np.load(A / 'optimization_20261003_r102/selected_validation.npy', mmap_mode='r').view(np.uint64))",
        'score_gain_over_parent100': 'score_gain_over_parent102',
        'gain_over_parent100': 'gain_over_parent102',
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':
            'passed_actual43_conditional_residual_extrapolation_full_official_comparisons',
        "'new_quality_score_records': 49": "'new_quality_score_records': 43"}
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    namespace = {'__file__': __file__, '__name__': 'actual_residual_extrapolation43_full_comparison',
                 'EXTRAPOLATION_EVIDENCE': evidence}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    for path, digest in pins.items():
        assert sha(path) == digest, path
    try:
        namespace['main']()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_residual_extrapolation43_full_comparison',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise


if __name__ == '__main__':
    main()
