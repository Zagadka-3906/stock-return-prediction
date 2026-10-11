"""Compare matched longer residual trees with both actual100 and qualified102 anchors."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
SOURCE = A / 'run_conditional_flag_residual_official_comparison_20261006.py'
OUT = A / 'conditional_residual128_256_comparison74_20261006'
REFERENCE = A / 'conditional_flag_residual_bank_20261006'


def main():
    service = A / 'service_owned_workflows_20261006/conditional_residual128_256_native_bank40'
    identity = read(service / 'native_launch.json')
    while owned(identity): time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    reference_names = ['flag_residual_leaf7_e64', 'flag_residual_leaf15_e64', 'flag_residual_leaf31_e64']
    evidence = [SOURCE, A / 'conditional_flag_residual_extrapolation_transform_20261006.py',
        A / 'optimization_20261003_r102/selected_validation.npy',
        A / 'optimization_20261003_r102/calibrated_csv_official.json',
        *[REFERENCE / n / 'flagged_oof_predictions.npy' for n in reference_names],
        A / 'github_validation_sync_main_20261005/round102_receipt.json']
    text = SOURCE.read_text(encoding='utf-8')
    before = "    ensembles = {'equal_mean_three_feature_residuals': supplied_feature_models,\n        'equal_mean_all_four_residuals': original_models}\n    heads = [*original_models, *ensembles]\n    cases = [{'model': None, 'weight': 0.}]"
    assert text.count(before) == 1
    text = text.replace(before,
        "    ensembles = {}\n"
        "    for rounds in (128, 256):\n"
        "        ensembles[f'equal_mean_three_feature_residuals_e{rounds}'] = [n for n in supplied_feature_models if bank['configurations'][n]['boosting_rounds'] == rounds]\n"
        "        ensembles[f'equal_mean_all_four_residuals_e{rounds}'] = [n for n in original_models if bank['configurations'][n]['boosting_rounds'] == rounds]\n"
        "    heads = [*original_models, *ensembles]\n"
        "    assert len(heads) == 12\n"
        "    ensembles['qualified102_original_e64'] = MATCHED_REFERENCE_NAMES\n"
        "    cases = [{'model': None, 'weight': 0.}, {'model': 'qualified102_original_e64', 'weight': 1.}]")
    patches = {
        "OUT = A / 'conditional_flag_residual_official_comparison_20261006'": "OUT = A / 'conditional_residual128_256_comparison74_20261006'",
        "BANK = A / 'conditional_flag_residual_bank_20261006'": "BANK = A / 'conditional_residual128_256_bank40_20261006'",
        'service_owned_workflows_20261006/conditional_flag_residual_native_bank':
            'service_owned_workflows_20261006/conditional_residual128_256_native_bank40',
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec':
            'passed_actual40_matched128_256_conditional_residual_native_models_and_independent_codec',
        "bank['actual_native_fits'] == 20": "bank['actual_native_fits'] == 40",
        'from conditional_flag_residual_transform_20261006 import transform':
            'from conditional_flag_residual_extrapolation_transform_20261006 import transform',
        '(.01, .025, .05, .1, .25, .5, .75, 1.)': '(.5, .75, 1., 1.25, 1.5, 2.)',
        'assert len(cases) == 49': 'assert len(cases) == 74',
        "sources = [Path(__file__), A / 'conditional_flag_residual_transform_20261006.py',":
            "sources = [*MATCHED_REFERENCE_EVIDENCE, Path(__file__), A / 'conditional_flag_residual_extrapolation_transform_20261006.py',",
        "'native_bank_fits': 20": "'native_bank_fits': 40, 'original64_models_reused_not_new_fits': 3",
        "'all49_final_past_return_mapped_CSVs_original_official_scored'": "'all74_final_past_return_mapped_CSVs_original_official_scored'",
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':
            'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons',
        "'existing_native_bank_fits': 20": "'existing_native_bank_fits': 40",
        "'new_quality_score_records': 49": "'new_quality_score_records': 74"}
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    before = '        for name, components in ensembles.items():'
    assert text.count(before) == 1
    text = text.replace(before,
        "        head_paths.update({n: MATCHED_REFERENCE / n / 'flagged_oof_predictions.npy' for n in MATCHED_REFERENCE_NAMES})\n" + before)
    before = '            metrics = score(ctx, values)'
    assert text.count(before) == 1
    text = text.replace(before,
        "            if index == 1:\n"
        "                assert case == {'model': 'qualified102_original_e64', 'weight': 1.}\n"
        "                assert np.array_equal(values.view(np.uint64), np.load(A / 'optimization_20261003_r102/selected_validation.npy', mmap_mode='r').view(np.uint64))\n" + before +
        "\n            if index == 1:\n"
        "                assert metrics == read(A / 'optimization_20261003_r102/calibrated_csv_official.json')['metrics']")
    namespace = {'__file__': __file__, '__name__': 'actual_matched_longer_residual_comparison74',
        'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE_NAMES': reference_names,
        'MATCHED_REFERENCE': REFERENCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    try:
        namespace['main']()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_matched128_256_residual_comparison74',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise


if __name__ == '__main__': main()
