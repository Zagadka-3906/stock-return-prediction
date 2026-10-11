"""Compare L1/Huber heads and equal means against actual100 and the qualified74 winner."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
SOURCE = A / 'run_conditional_flag_residual_official_comparison_20261006.py'
OUT = A / 'robust_conditional_residual_comparison50_20261006'


def main():
    service = A / 'service_owned_workflows_20261006/robust_conditional_residual_native_bank20'
    identity = read(service / 'native_launch.json')
    while owned(identity): time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    release = A / 'longer_residual74_release_20261006'
    selected = read(release / 'selection.json')
    cfg = selected['chosen_postprocessor']
    reference_names = selected['native_component_names']
    reference_banks = {n: Path(selected['selected_component_bank_paths'][n]) for n in reference_names}
    pilot74 = A / 'conditional_residual128_256_comparison74_20261006'
    evidence = [SOURCE, A / 'conditional_flag_residual_extrapolation_transform_20261006.py',
        release / 'selection.json', release / 'selected_validation.npy',
        release / 'calibrated_csv_official.json', release / 'source_package_verification.json',
        pilot74 / 'verification.json',
        *[reference_banks[n] / n / 'flagged_oof_predictions.npy' for n in reference_names]]
    text = SOURCE.read_text(encoding='utf-8')
    before = "    ensembles = {'equal_mean_three_feature_residuals': supplied_feature_models,\n        'equal_mean_all_four_residuals': original_models}\n    heads = [*original_models, *ensembles]\n    cases = [{'model': None, 'weight': 0.}]"
    assert text.count(before) == 1
    text = text.replace(before,
        "    ensembles = {f'equal_mean_{loss}_residuals': [n for n in original_models if bank['configurations'][n]['objective'] == objective]\n"
        "        for loss, objective in [('l1', 'regression_l1'), ('huber', 'huber')]}\n"
        "    assert all(len(v) == 2 for v in ensembles.values())\n"
        "    heads = [*original_models, *ensembles]\n"
        "    assert len(heads) == 6\n"
        "    ensembles[MATCHED_SELECTED_CONFIGURATION['model']] = MATCHED_REFERENCE_NAMES\n"
        "    cases = [{'model': None, 'weight': 0.}, dict(MATCHED_SELECTED_CONFIGURATION)]")
    patches = {
        "OUT = A / 'conditional_flag_residual_official_comparison_20261006'": "OUT = A / 'robust_conditional_residual_comparison50_20261006'",
        "BANK = A / 'conditional_flag_residual_bank_20261006'": "BANK = A / 'robust_conditional_residual_bank20_20261006'",
        'service_owned_workflows_20261006/conditional_flag_residual_native_bank': 'service_owned_workflows_20261006/robust_conditional_residual_native_bank20',
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec': 'passed_actual20_matched_L1_Huber_conditional_residual_native_models_and_independent_codec',
        'from conditional_flag_residual_transform_20261006 import transform': 'from conditional_flag_residual_extrapolation_transform_20261006 import transform',
        '(.01, .025, .05, .1, .25, .5, .75, 1.)': '(.1, .25, .5, .75, 1., 1.25, 1.5, 2.)',
        'assert len(cases) == 49': 'assert len(cases) == 50',
        "sources = [Path(__file__), A / 'conditional_flag_residual_transform_20261006.py',": "sources = [*MATCHED_REFERENCE_EVIDENCE, Path(__file__), A / 'conditional_flag_residual_extrapolation_transform_20261006.py',",
        "'all49_final_past_return_mapped_CSVs_original_official_scored'": "'all50_final_past_return_mapped_CSVs_original_official_scored'",
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons': 'passed_actual50_matched_L1_Huber_residual_and_ensemble_full_official_comparisons',
        "'new_quality_score_records': 49": "'new_quality_score_records': 50",
    }
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    before = '        for name, components in ensembles.items():'
    assert text.count(before) == 1
    text = text.replace(before,
        "        head_paths.update({n: MATCHED_REFERENCE_BANKS[n] / n / 'flagged_oof_predictions.npy' for n in MATCHED_REFERENCE_NAMES})\n" + before)
    before = '            metrics = score(ctx, values)'
    assert text.count(before) == 1
    text = text.replace(before,
        "            if index == 1:\n"
        "                assert case == MATCHED_SELECTED_CONFIGURATION\n"
        "                assert np.array_equal(values.view(np.uint64), np.load(MATCHED_RELEASE / 'selected_validation.npy', mmap_mode='r').view(np.uint64))\n" + before +
        "\n            if index == 1:\n"
        "                assert metrics == read(MATCHED_RELEASE / 'calibrated_csv_official.json')['metrics']")
    namespace = {'__file__': __file__, '__name__': 'actual_matched_L1_Huber_residual_comparison50',
        'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE_NAMES': reference_names,
        'MATCHED_REFERENCE_BANKS': reference_banks, 'MATCHED_SELECTED_CONFIGURATION': cfg, 'MATCHED_RELEASE': release}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    try:
        namespace['main']()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_matched_L1_Huber_residual_comparison50',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise


if __name__ == '__main__': main()
