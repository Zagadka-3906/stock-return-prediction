"""Fit L1/Huber residual heads with matched L2 features, targets, windows and128 trees."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
SOURCE = A / 'train_conditional_flag_residual_bank_20261006.py'
REFERENCE = A / 'conditional_residual128_256_bank40_20261006'
OUT = A / 'robust_conditional_residual_bank20_20261006'


def main():
    # Finish the selected longer-tree scheme's real full/cold inference first.
    service = A / 'service_owned_workflows_20261006/longer_residual74_candidate_sealing'
    identity = read(service / 'native_launch.json')
    while owned(identity): time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    assert read(REFERENCE / 'verification.json')['actual_native_fits'] == 40
    reference_names = ['flag_residual_rank_only_leaf7_e128', 'flag_residual_leaf7_e128']
    evidence = [SOURCE, REFERENCE / 'verification.json',
        A / 'longer_residual74_release_20261006/source_package_verification.json',
        *[REFERENCE / name / f'info_{year}.json' for name in reference_names for year in range(2021, 2026)],
        *[REFERENCE / name / f'model_{year}.txt' for name in reference_names for year in range(2021, 2026)]]
    text = SOURCE.read_text(encoding='utf-8')
    patches = {
        "OUT = A / 'conditional_flag_residual_bank_20261006'": "OUT = A / 'robust_conditional_residual_bank20_20261006'",
        "paths = [Path(__file__),": "paths = [*MATCHED_REFERENCE_EVIDENCE, Path(__file__),",
        "'maximum_boosting_rounds': 64": "'maximum_boosting_rounds': 128",
        "**{k: v for k, v in cfg.items() if k != 'rank_only'}":
            "**{k: v for k, v in cfg.items() if k not in ('rank_only', 'reference128_name')}",
        'booster = lgb.train(params, dataset, num_boost_round=64)': 'booster = lgb.train(params, dataset, num_boost_round=128)',
        "assert 1 <= item['actual_tree_count'] <= 64": "assert 1 <= item['actual_tree_count'] <= 128",
        'passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec':
            'passed_actual20_matched_L1_Huber_conditional_residual_native_models_and_independent_codec',
    }
    for before in sorted(patches, key=len, reverse=True):
        assert before in text, before
        text = text.replace(before, patches[before])
    before = "        'no_validation_early_stopping_or_model_selection': True,"
    assert text.count(before) == 1
    text = text.replace(before, before +
        "\n        'matched_changes_only': 'L2 objective becomes regression_l1 or huber with alpha0.9; same128 rounds and all other native parameters',\n"
        "        'robust_loss_alpha_not_selected_from_validation': 0.9,\n"
        "        'new_native_fit_grid': 'L1/Huber x rank-only/full63pluspercentile leaf7 x four annual and one final windows',")
    before = '                primary = booster.predict(test, num_threads=2)'
    assert text.count(before) == 1
    text = text.replace(before,
        "                ref_path = MATCHED_REFERENCE / cfg['reference128_name'] / f'info_{year}.json'\n"
        "                reference = read(ref_path)\n"
        "                assert reference['features'] == model_features\n"
        "                assert reference['training_rows'] == int(training.sum())\n"
        "                assert reference['training_residual_numeric_sha256'] == numeric_sha(residual)\n"
        "                assert (reference['last_training_label_date'], reference['last_training_label_end'], reference['exclusive_cutoff']) == (last, end, cutoff)\n"
        "                assert {k: v for k, v in params.items() if k not in ('objective', 'alpha')} == {k: v for k, v in reference['parameters'].items() if k not in ('objective', 'alpha')}\n"
        "                assert params['objective'] in ('regression_l1', 'huber')\n"
        "                assert ('alpha' not in params) if params['objective'] == 'regression_l1' else params['alpha'] == .9\n"
        "                reference_native = lgb.Booster(model_str=Path(reference['native_model_path']).read_text(encoding='utf-8'))\n"
        "                reference_values = reference_native.predict(test, num_threads=2)\n"
        "                create(folder / f'matched_L2_reference_{year}_verification.json', {\n"
        "                    'status': 'passed_actual_matched128_L2_features_targets_windows_and_other_native_parameters',\n"
        "                    'new_name': name, 'reference_name': cfg['reference128_name'], 'year': year,\n"
        "                    'reference_info_sha256': sha(ref_path), 'control_rows': len(test),\n"
        "                    'reference_native_prediction_numeric_sha256': numeric_sha(reference_values),\n"
        "                    'new_loss': params['objective'], 'fixed_alpha': params.get('alpha'),\n"
        "                    'new_prediction_equality_not_required_for_changed_loss': True, 'test_labels_read': False})\n"
        "                del reference_native, reference_values\n" + before)
    namespace = {'__file__': __file__, '__name__': 'actual_robust_conditional_residual_bank20',
        'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE': REFERENCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    base = namespace['CONFIGS']
    configs = {}
    for loss, objective in [('l1', 'regression_l1'), ('huber', 'huber')]:
        for rank_only in (True, False):
            reference64 = 'flag_residual_' + ('rank_only_' if rank_only else '') + 'leaf7_e64'
            name = f'robust_residual_{loss}_' + ('rank_only_' if rank_only else '') + 'leaf7_e128'
            configs[name] = {**base[reference64], 'objective': objective,
                'reference128_name': reference64.removesuffix('_e64') + '_e128',
                **({'alpha': .9} if loss == 'huber' else {})}
    assert len(configs) == 4
    namespace['CONFIGS'] = configs
    try:
        namespace['main']()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {
                'status': 'failed_preserved_actual_L1_Huber_conditional_residual_bank20',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False,
            })
        raise


if __name__ == '__main__': main()
