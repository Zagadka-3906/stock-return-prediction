"""Fit matched128/256-tree residuals and verify the real original64-tree prefix."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
SOURCE = A / 'train_conditional_flag_residual_bank_20261006.py'
REFERENCE = A / 'conditional_flag_residual_bank_20261006'
OUT = A / 'conditional_residual128_256_bank40_20261006'


def main():
    # Finish the currently selected scheme's real native replay before admitting
    # another bank. The original wide fit and queued scientific grids continue.
    service = A / 'service_owned_workflows_20261006/residual_extrapolation43_candidate_sealing'
    identity = read(service / 'native_launch.json')
    while owned(identity): time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    assert read(REFERENCE / 'verification.json')['actual_native_fits'] == 20
    evidence = [SOURCE, REFERENCE / 'verification.json',
        *REFERENCE.glob('*/info_*.json'), *REFERENCE.glob('*/model_*.txt'),
        *REFERENCE.glob('*/model_dump_*.json'),
        A / 'residual_extrapolation43_release_20261006/source_package_verification.json']
    text = SOURCE.read_text(encoding='utf-8')
    patches = {
        "OUT = A / 'conditional_flag_residual_bank_20261006'": "OUT = A / 'conditional_residual128_256_bank40_20261006'",
        "paths = [Path(__file__),": "paths = [*MATCHED_REFERENCE_EVIDENCE, Path(__file__),",
        "'expected_actual_native_fits': 20": "'expected_actual_native_fits': 40",
        "'maximum_boosting_rounds': 64,": "'maximum_boosting_rounds': 256, 'boosting_rounds_per_model': {n: c['boosting_rounds'] for n, c in CONFIGS.items()},",
        "**{k: v for k, v in cfg.items() if k != 'rank_only'}":
            "**{k: v for k, v in cfg.items() if k not in ('rank_only', 'boosting_rounds', 'reference64_name')}",
        'booster = lgb.train(params, dataset, num_boost_round=64)':
            "booster = lgb.train(params, dataset, num_boost_round=cfg['boosting_rounds'])",
        "'actual_tree_count': booster.num_trees(), 'maximum_boosting_rounds': 64":
            "'actual_tree_count': booster.num_trees(), 'maximum_boosting_rounds': cfg['boosting_rounds']",
        "assert 1 <= item['actual_tree_count'] <= 64": "assert 64 <= item['actual_tree_count'] <= cfg['boosting_rounds']",
        'assert len(records) == 20': 'assert len(records) == 40',
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec':
            'passed_actual40_matched128_256_conditional_residual_native_models_and_independent_codec',
        "'actual_native_fits': 20": "'actual_native_fits': 40"}
    # Replace the per-model maximum first; the protocol maximum is a different
    # statement and must not overwrite each model's declared128/256 setting.
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    before = '                primary = booster.predict(test, num_threads=2)'
    assert text.count(before) == 1
    text = text.replace(before,
        "                reference_info = read(MATCHED_REFERENCE / cfg['reference64_name'] / f'info_{year}.json')\n"
        "                assert reference_info['features'] == model_features\n"
        "                assert reference_info['training_rows'] == int(training.sum())\n"
        "                assert reference_info['training_residual_numeric_sha256'] == numeric_sha(residual)\n"
        "                assert reference_info['parameters'] == params\n"
        "                reference64 = lgb.Booster(model_str=Path(reference_info['native_model_path']).read_text(encoding='utf-8'))\n"
        "                assert reference64.num_trees() == 64\n"
        "                original_values = reference64.predict(test, num_threads=2)\n"
        "                matched_prefix = booster.predict(test, num_iteration=64, num_threads=2)\n"
        "                assert np.array_equal(original_values.view(np.uint64), matched_prefix.view(np.uint64))\n"
        "                assert read(dump_path)['tree_info'][:64] == read(reference_info['independent_tree_dump_path'])['tree_info']\n"
        "                create(folder / f'original64_prefix_{year}_verification.json', {\n"
        "                    'status': 'passed_actual_matched_original64_tree_prefix_full_native_predictions',\n"
        "                    'original_name': cfg['reference64_name'], 'extended_name': name, 'year': year,\n"
        "                    'original_info_sha256': sha(MATCHED_REFERENCE / cfg['reference64_name'] / f'info_{year}.json'),\n"
        "                    'rows': len(test), 'original_and_extended_prefix_numeric_sha256': numeric_sha(original_values),\n"
        "                    'all_first64_tree_structures_and_values_exact': True,\n"
        "                    'training_features_targets_and_parameters_exact': True, 'test_labels_read': False})\n"
        "                del reference64, original_values, matched_prefix\n" + before)
    namespace = {'__file__': __file__, '__name__': 'actual_matched_longer_conditional_residual_bank40',
        'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE': REFERENCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    base = namespace['CONFIGS']
    configs = {}
    for name, cfg in base.items():
        for rounds in (128, 256):
            extended_name = name.removesuffix('_e64') + f'_e{rounds}'
            configs[extended_name] = {**cfg, 'boosting_rounds': rounds, 'reference64_name': name}
    assert len(configs) == 8
    namespace['CONFIGS'] = configs
    try:
        namespace['main']()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_matched128_256_residual_bank40',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise


if __name__ == '__main__': main()
