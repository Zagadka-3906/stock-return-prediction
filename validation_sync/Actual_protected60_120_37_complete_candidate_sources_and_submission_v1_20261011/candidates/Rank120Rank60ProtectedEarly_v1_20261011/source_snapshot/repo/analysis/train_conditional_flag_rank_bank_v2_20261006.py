"""Resume a native bank after a Unicode path loader error, preserving the first fit."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, owned
SOURCE = A / 'train_conditional_flag_rank_bank_20261006.py'
OLD = A / 'conditional_flag_rank_bank_20261006'


def main():
    service = A / 'service_owned_workflows_20261006/conditional_flag_rank_native_bank'
    assert not owned(read(service / 'native_launch.json'))
    failure = read(service / 'service_execution.json')
    assert failure['status'] == 'failed' and 'Could not open' in failure['failure']
    targets = read(OLD / 'actual_target_and_feature_alignment.json')
    assert targets['status'] == 'passed_original_float64_train_targets_exactly_match_all_official_OOF_flagged_targets'
    assert sha(OLD / 'flagged_training_targets_and_features.parquet') == targets['flagged_training_parquet_sha256']
    assert sha(OLD / 'flagged_validation_features.parquet') == targets['flagged_validation_parquet_sha256']
    preserved = [SOURCE, OLD / 'actual_target_and_feature_alignment.json', OLD / 'frozen_before_actual_training.json',
        OLD / 'failure.json', OLD / 'flagged_training_targets_and_features.parquet', OLD / 'flagged_validation_features.parquet',
        OLD / 'flag_rank_leaf7_e64/model_2020.txt', OLD / 'flag_rank_leaf7_e64/model_dump_2020.json',
        service / 'service_execution.json', service / 'native_launch.json']
    pins = {str(p): sha(p) for p in preserved}
    text = SOURCE.read_text(encoding='utf-8')
    text = text.replace("OUT = A / 'conditional_flag_rank_bank_20261006'", "OUT = A / 'conditional_flag_rank_bank_v2_20261006'")
    text = text.replace("pins = {str(p): original[str(p)] if str(p) in original else sha(p) for p in paths}",
        "pins = {**PRESERVED_PINS, **{str(p): original[str(p)] if str(p) in original else sha(p) for p in paths}}")
    left = text.index('        labels = pl.read_csv(')
    right = text.index('        x = clean_matrix(', left)
    # Reload the exact already verified training/validation data, avoiding a
    # fresh CSV parser or recomputation of the successful target alignment.
    block = """        historical = pl.read_parquet(OLD / 'flagged_training_targets_and_features.parquet')
        keyed = pl.read_parquet(OLD / 'flagged_validation_features.parquet')
        train_days = pl.scan_csv(ROOT / 'data/raw/训练集.csv').select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet', columns=['ts_code', 'trade_date', 'flag_limit_up'])
        flagged = frame.with_row_index('oof_position').filter(pl.col('flag_limit_up') == 1)
        assert keyed['oof_position'].equals(flagged['oof_position'])
        assert keyed.select('ts_code', 'trade_date').equals(flagged.select('ts_code', 'trade_date'))
        for filename in ('flagged_training_targets_and_features.parquet', 'flagged_validation_features.parquet'):
            os.link(OLD / filename, OUT / filename)
        create(OUT / 'actual_target_and_feature_alignment.json', {**PRESERVED_TARGETS,
            'actual_verified_original_targets_and_features_reloaded': True,
            'original_alignment_proof_sha256': sha(OLD / 'actual_target_and_feature_alignment.json')})
        create(OUT / 'native_path_reload_recovery.json', {'original_failure': ORIGINAL_FAILURE,
            'preserved_source_sha256': PRESERVED_PINS, 'existing_first_fit_reused': True,
            'native_weights_read_by_Python_UTF8_then_LightGBM_model_string': True,
            'original_failed_run_not_removed_or_marked_passed': True})
"""
    text = text[:left] + block + text[right:]
    before = '                booster = lgb.train(params, dataset, num_boost_round=64)'
    after = """                reused = name == 'flag_rank_leaf7_e64' and year == 2020
                if reused:
                    booster = lgb.Booster(model_str=(OLD / name / 'model_2020.txt').read_text(encoding='utf-8'))
                    assert booster.dump_model() == read(OLD / name / 'model_dump_2020.json')
                    first = booster.dump_model()['tree_info'][0]['tree_structure']
                    assert first.get('internal_count', first.get('leaf_count')) == int(training.sum())
                else:
                    booster = lgb.train(params, dataset, num_boost_round=64)"""
    assert text.count(before) == 1
    text = text.replace(before, after)
    text = text.replace('lgb.Booster(model_file=str(native_path))', "lgb.Booster(model_str=native_path.read_text(encoding='utf-8'))")
    text = text.replace("'new_native_model_fits': 1, 'future_test_features_or_labels_used': False",
        "'new_native_model_fits': 0 if reused else 1, 'original_fit_reused_after_failed_file_loader': reused, 'future_test_features_or_labels_used': False")
    text = text.replace("'actual_models': records,", "'actual_models': records, 'actual_native_fits_this_recovery': 17, 'original_native_fits_preserved_and_reused': 1,")
    assert 'model_file=str(native_path)' not in text
    namespace = {'__file__': __file__, '__name__': 'conditional_native_bank_recovery',
        'OLD': OLD, 'PRESERVED_PINS': pins, 'PRESERVED_TARGETS': targets, 'ORIGINAL_FAILURE': failure}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
