"""Test all15 quarter-step convex residual blends and three fixed amplitudes."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
SOURCE = A / 'run_conditional_flag_residual_official_comparison_20261006.py'
OUT = A / 'residual_simplex47_official_comparison_20261006'
BANK = A / 'conditional_residual128_256_bank40_20261006'


def main():
    service = A / 'service_owned_workflows_20261006/conditional_residual128_256_native_bank40'
    while owned(read(service / 'native_launch.json')):
        time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    release = A / 'longer_residual74_release_20261006'
    selected = read(release / 'selection.json')
    names = ['flag_residual_leaf7_e256', 'flag_residual_leaf15_e256', 'flag_residual_leaf31_e256']
    assert selected['native_component_names'] == names
    assert selected['chosen_postprocessor'] == {'model': 'equal_mean_three_feature_residuals_e256', 'weight': .75}
    assert all(Path(selected['selected_component_bank_paths'][name]).resolve() == BANK.resolve() for name in names)
    triples = [(a, b, 4-a-b) for a in range(5) for b in range(5-a)]
    assert len(triples) == 15 and len(set(triples)) == 15
    integer_weights = {f'simplex4_{a}_{b}_{c}_e256': [a, b, c] for a, b, c in triples}
    ensembles = {key: [name for name, repeats in zip(names, weights) for _ in range(repeats)]
        for key, weights in integer_weights.items()}
    assert all(len(components) == 4 for components in ensembles.values())
    evidence = [SOURCE, Path(__file__), release / 'selection.json', release / 'selected_validation.npy',
        release / 'calibrated_csv_official.json', release / 'source_package_verification.json',
        A / 'conditional_flag_residual_extrapolation_transform_20261006.py',
        A / 'conditional_residual128_256_comparison74_20261006/verification.json',
        A / 'train_conditional_residual128_256_bank40_20261006.py']
    text = SOURCE.read_text(encoding='utf-8')
    before = "    ensembles = {'equal_mean_three_feature_residuals': supplied_feature_models,\n        'equal_mean_all_four_residuals': original_models}\n    heads = [*original_models, *ensembles]\n    cases = [{'model': None, 'weight': 0.}]"
    assert text.count(before) == 1
    text = text.replace(before,
        "    ensembles = dict(SIMPLEX_ENSEMBLES)\n"
        "    heads = list(ensembles)\n"
        "    assert len(heads) == 15\n"
        "    ensembles[SELECTED_CONFIGURATION['model']] = SIMPLEX_NATIVE_NAMES\n"
        "    cases = [{'model': None, 'weight': 0.}, dict(SELECTED_CONFIGURATION)]")
    patches = {
        "OUT = A / 'conditional_flag_residual_official_comparison_20261006'": "OUT = A / 'residual_simplex47_official_comparison_20261006'",
        "BANK = A / 'conditional_flag_residual_bank_20261006'": "BANK = A / 'conditional_residual128_256_bank40_20261006'",
        'service_owned_workflows_20261006/conditional_flag_residual_native_bank': 'service_owned_workflows_20261006/conditional_residual128_256_native_bank40',
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec': 'passed_actual40_matched128_256_conditional_residual_native_models_and_independent_codec',
        "bank['actual_native_fits'] == 20": "bank['actual_native_fits'] == 40",
        'from conditional_flag_residual_transform_20261006 import transform': 'from conditional_flag_residual_extrapolation_transform_20261006 import transform',
        '(.01, .025, .05, .1, .25, .5, .75, 1.)': '(.75, 1., 1.25)',
        'assert len(cases) == 49': 'assert len(cases) == 47',
        "sources = [Path(__file__), A / 'conditional_flag_residual_transform_20261006.py',":
            "sources = [*SIMPLEX_EVIDENCE, Path(__file__), A / 'conditional_flag_residual_extrapolation_transform_20261006.py',",
        "'native_bank_fits': 20": "'native_bank_fits': 40, 'actual_new_native_fits': 0",
        "'all49_final_past_return_mapped_CSVs_original_official_scored'": "'all47_final_past_return_mapped_CSVs_original_official_scored'",
        'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons':
            'passed_actual47_convex_simplex_residual_ensemble_full_official_comparisons',
        "'existing_native_bank_fits': 20": "'existing_native_bank_fits': 40",
        "'new_quality_score_records': 49": "'new_quality_score_records': 47",
    }
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    before = "'new_native_fits_by_this_comparison': 0, 'test_labels_read': False})"
    assert text.count(before) == 1
    text = text.replace(before,
        "'new_native_fits_by_this_comparison': 0, 'test_labels_read': False,\n"
        "        'ordered_unique_native_components': SIMPLEX_NATIVE_NAMES,\n"
        "        'ensemble_integer_weights': SIMPLEX_INTEGER_WEIGHTS,\n"
        "        'ensemble_arithmetic': 'Repeat each component in fixed leaf7/15/31 order; ordered float64 sum of four entries divided by4',\n"
        "        'all15_nonnegative_integer_triples_sum4_and_fixed_amplitudes': [.75, 1., 1.25]})")
    before = '            metrics = score(ctx, values)'
    assert text.count(before) == 1
    text = text.replace(before,
        "            if index == 1:\n"
        "                assert case == SELECTED_CONFIGURATION\n"
        "                assert np.array_equal(values.view(np.uint64), np.load(SELECTED_RELEASE / 'selected_validation.npy', mmap_mode='r').view(np.uint64))\n"
        + before + "\n            if index == 1:\n"
        "                assert metrics == read(SELECTED_RELEASE / 'calibrated_csv_official.json')['metrics']")
    before = "'ensembles': ensembles, 'test_labels_read': False,"
    assert text.count(before) == 1
    text = text.replace(before, before +
        "\n        'ordered_unique_native_components': SIMPLEX_NATIVE_NAMES, 'ensemble_integer_weights': SIMPLEX_INTEGER_WEIGHTS,")
    compile(text, str(SOURCE), 'exec')
    namespace = {'__file__': __file__, '__name__': 'actual_convex_simplex_residual_comparison47',
        'SIMPLEX_EVIDENCE': evidence, 'SIMPLEX_ENSEMBLES': ensembles, 'SIMPLEX_NATIVE_NAMES': names,
        'SIMPLEX_INTEGER_WEIGHTS': integer_weights, 'SELECTED_CONFIGURATION': selected['chosen_postprocessor'],
        'SELECTED_RELEASE': release}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    try:
        namespace['main']()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_simplex47_official_comparison',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise


if __name__ == '__main__':
    main()
