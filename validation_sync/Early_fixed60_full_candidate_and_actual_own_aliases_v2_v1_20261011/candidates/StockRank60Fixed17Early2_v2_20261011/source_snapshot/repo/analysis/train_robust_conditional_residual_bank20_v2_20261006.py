"""Resume the codec-rejected bank using its real first fit and19 new unchanged fits."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, owned
SOURCE = A / 'train_robust_conditional_residual_bank20_20261006.py'
OLD = A / 'robust_conditional_residual_bank20_20261006'


def main():
    service = A / 'service_owned_workflows_20261006/robust_conditional_residual_native_bank20'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'failed'
    assert "model['objective'].split()[0] == 'regression'" in (service / 'stderr.log').read_text(encoding='utf-8')
    assert not list(OLD.glob('*/info_*.json'))
    assert len(list(OLD.glob('*/model_*.txt'))) == 1
    first = OLD / 'robust_residual_l1_rank_only_leaf7_e128'
    dump = read(first / 'model_dump_2021.json')
    assert dump['objective'] == 'regression_l1' and len(dump['tree_info']) == 128
    evidence = [SOURCE, Path(__file__), A / 'conditional_identity_regression_tree_codec_20261006.py',
        OLD / 'frozen_before_actual_training.json', OLD / 'actual_training_admission.json',
        OLD / 'failure.json', first / 'model_2021.txt', first / 'model_dump_2021.json',
        first / 'matched_L2_reference_2021_verification.json',
        A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json']
    for name in ('robust_conditional_residual_native_bank20', 'robust_conditional_residual_comparison50',
                 'robust_conditional_residual_bank20_evidence_publication', 'robust_conditional_residual_scores50_evidence_publication'):
        folder = A / 'service_owned_workflows_20261006' / name
        assert not owned(read(folder / 'native_launch.json'))
        assert read(folder / 'service_execution.json')['status'] == 'failed'
        evidence.extend([*folder.glob('*.json'), *folder.glob('*.log')])
    text = SOURCE.read_text(encoding='utf-8')
    text = text.replace('robust_conditional_residual_bank20_20261006', 'robust_conditional_residual_bank20_v2_20261006')
    before = '    evidence = [SOURCE, REFERENCE'
    assert text.count(before) == 1
    text = text.replace(before, '    evidence = [*RECOVERY_EVIDENCE, SOURCE, REFERENCE')
    before = "    namespace = {'__file__': __file__, '__name__': 'actual_robust_conditional_residual_bank20',"
    assert text.count(before) == 1
    insertion = '''    before = 'from conditional_flag_rank_codec_20261006 import clean_matrix, predict_dump'
    assert text.count(before) == 1
    text = text.replace(before, 'from conditional_identity_regression_tree_codec_20261006 import clean_matrix, predict_dump')
    before = '                booster = lgb.train(params, dataset, num_boost_round=128)'
    assert text.count(before) == 1
    text = text.replace(before,
        "                reused = name == 'robust_residual_l1_rank_only_leaf7_e128' and year == 2021\\n"
        "                if reused:\\n"
        "                    booster = lgb.Booster(model_str=(RECOVERY_ORIGINAL_BANK / name / 'model_2021.txt').read_text(encoding='utf-8'))\\n"
        "                    assert booster.dump_model() == read(RECOVERY_ORIGINAL_BANK / name / 'model_dump_2021.json')\\n"
        "                    first = booster.dump_model()['tree_info'][0]['tree_structure']\\n"
        "                    assert first.get('internal_count', first.get('leaf_count')) == int(training.sum())\\n"
        "                else:\\n"
        "                    booster = lgb.train(params, dataset, num_boost_round=128)")
    before = "                with native_path.open('x', encoding='utf-8') as stream:\\n                    stream.write(booster.model_to_string())\\n                dump_path = folder / f'model_dump_{year}.json'\\n                create(dump_path, booster.dump_model())"
    assert text.count(before) == 1
    text = text.replace(before,
        "                dump_path = folder / f'model_dump_{year}.json'\\n"
        "                if reused:\\n"
        "                    os.link(RECOVERY_ORIGINAL_BANK / name / 'model_2021.txt', native_path)\\n"
        "                    os.link(RECOVERY_ORIGINAL_BANK / name / 'model_dump_2021.json', dump_path)\\n"
        "                else:\\n"
        "                    with native_path.open('x', encoding='utf-8') as stream:\\n"
        "                        stream.write(booster.model_to_string())\\n"
        "                    create(dump_path, booster.dump_model())")
    before = "'future_test_features_or_labels_used': False}"
    assert text.count(before) == 1
    text = text.replace(before, "'actual_new_native_fits_this_item': 0 if reused else 1, 'original_fit_reused_after_codec_guard_failure': reused, " + before)
    before = "'actual_models': records, 'diagnostic_parent_curve_pair_refits': 5,"
    assert text.count(before) == 1
    text = text.replace(before, "'actual_models': records, 'actual_new_native_fits_this_recovery': 19, 'original_native_fits_preserved_and_reused': 1, 'diagnostic_parent_curve_pair_refits': 5,")
    before = "        'no_validation_early_stopping_or_model_selection': True,"
    assert text.count(before) == 1
    text = text.replace(before, before + "\\n        'original_failed_run_preserved_and_first_native_fit_reused': True,\\n        'codec_change_only_identity_objective_whitelist_tree_sum_body_unchanged': True,")
'''
    text = text.replace(before, insertion + before)
    before = "'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE': REFERENCE}"
    assert text.count(before) == 1
    text = text.replace(before, "'MATCHED_REFERENCE_EVIDENCE': evidence, 'MATCHED_REFERENCE': REFERENCE, 'RECOVERY_ORIGINAL_BANK': RECOVERY_ORIGINAL_BANK}")
    before = "    assert len(configs) == 4"
    assert text.count(before) == 1
    text = text.replace(before, before + "\n    assert configs == read(RECOVERY_ORIGINAL_BANK / 'frozen_before_actual_training.json')['configurations']")
    namespace = {'__file__': __file__, '__name__': 'robust_residual_codec_guard_recovery_v2',
        'RECOVERY_EVIDENCE': evidence, 'RECOVERY_ORIGINAL_BANK': OLD}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__': main()
