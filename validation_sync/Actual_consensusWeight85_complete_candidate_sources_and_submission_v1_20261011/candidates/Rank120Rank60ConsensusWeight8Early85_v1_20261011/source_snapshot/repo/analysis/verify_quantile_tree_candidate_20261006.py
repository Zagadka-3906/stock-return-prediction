"""Actual mature-data native controls, explicitly excluded from quality scores."""
from pathlib import Path
import gc
import hashlib
import importlib.metadata
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_tree_preflight_20261006'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import lightgbm as lgb
    import numpy as np
    import polars as pl
    import psutil
    import quantile_tree_candidate_20261006 as core
    from verify_linear_leaf_bank_20261005 import manual_native_prediction
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from hidden_windows_child_creation_20261006 import install
    native = core.matched.engine
    assert not OUT.exists()
    OUT.mkdir()
    paths = [Path(__file__), Path(core.__file__), Path(core.matched.__file__),
        native.SOURCE if hasattr(native, 'SOURCE') else A / 'train_diverse_backbones_20261003.py',
        A / 'verify_linear_leaf_bank_20261005.py', core.matched.STORAGE,
        A / 'optimize_training_round12.py', A / 'locked_read_hash_cache_20261004.py',
        A / 'hidden_windows_child_creation_20261006.py',
        A / 'quantile_tree_candidate_plan_20261006.json',
        native.FEATURE_FILE, native.MANIFEST, ROOT / 'run.py', ROOT / 'src/features.py',
        ROOT / '后续选模标准.md']
    bindings = {str(p.resolve()): sha(p) for p in dict.fromkeys(paths)}
    create(OUT / 'frozen_before_actual_controls.json', {
        'status': 'frozen_before_actual_mature_quantile_native_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': bindings,
        'production_configurations': core.CONFIGS, 'control_rows': 4096,
        'control_boosting_iterations': 48, 'actual_annual_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False})
    restore = install()
    started = time.monotonic()
    checks, pilot_predictions = [], {}
    before_ram = psutil.virtual_memory().available
    try:
        with LockedReadHashCache(bindings) as cache:
            features = native.feature_names()
            assert len(features) == 63
            cutoff = native.fold_cutoff(2020)
            lazy = pl.scan_parquet(native.FEATURE_FILE)
            dates = (lazy.filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == 2020))
                .select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_list())
            cold80 = (lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= dates[0])
                & (pl.col('trade_date') <= dates[79])).select(native.KEYS + features + ['price_valid'])
                .sort('trade_date', 'ts_code').collect())
            assert len(cold80) == 80 * 4650 and cold80['trade_date'].n_unique() == 80
            assert cold80['ts_code'].n_unique() == 4650 and int(cold80['trade_date'].min()) >= cutoff
            cold_x = native.to_matrix(cold80, features)
            prefix_rows = int((cold80['trade_date'] <= dates[36]).sum())
            for name, cfg in core.CONFIGS.items():
                columns = native.KEYS + features + ['y_rank', 'y_ret_1d', 'is_train', 'price_valid']
                past = native.training_frame(lazy, cutoff, cfg).select(columns).head(4096).collect()
                future = lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= cutoff)).select(columns).head(1024).collect()
                sample = pl.concat([past, future])
                poisoned = sample.with_columns([pl.when(pl.col('trade_date') >= cutoff)
                    .then(pl.lit(12345., dtype=sample.schema[target])).otherwise(pl.col(target))
                    .alias(target) for target in ('y_rank', 'y_ret_1d')])
                clean = native.training_frame(sample.lazy(), cutoff, cfg).collect()
                changed = native.training_frame(poisoned.lazy(), cutoff, cfg).collect()
                assert clean.equals(changed) and len(clean) == 4096
                assert int(clean['trade_date'].max()) < cutoff
                x, y = native.to_matrix(clean, features), clean[cfg['target']].to_numpy()
                pilot = dict(cfg, num_boost_round=48)
                fit_started = time.monotonic()
                a = core.fit_arrays(x, y, pilot)
                b = core.fit_arrays(native.to_matrix(changed, features), changed[cfg['target']].to_numpy(), pilot)
                assert a['model_string'] == b['model_string'] and a['target_bounds'] == b['target_bounds']
                assert np.array_equal(a['mean'], b['mean']) and np.array_equal(a['scale'], b['scale'])
                model = OUT / f'{name}.joblib'
                native.save_bundle(model, a)
                values = core.predict_arrays(a, cold_x)
                assert np.isfinite(values).all()
                assert np.array_equal(values, core.predict_arrays(native.load_bundle(model), cold_x))
                assert np.array_equal(values[:prefix_rows], core.predict_arrays(native.load_bundle(model), cold_x[:prefix_rows]))
                changed_x = cold_x.copy()
                changed_x[prefix_rows:] = 12345.
                assert np.array_equal(values[:prefix_rows], core.predict_arrays(a, changed_x)[:prefix_rows])
                probe = x[:131].copy()
                probe[::5, 2] = np.nan
                probe[::7, 5] = np.inf
                probe[::11, 8] = a['mean'][8]
                z = core.matched.standardize(probe, a['mean'], a['scale'], pilot)
                assert np.isnan(z[::5, 2]).all() and np.isnan(z[::7, 5]).all()
                assert np.isfinite(z[::11, 8]).all()
                booster = lgb.Booster(model_str=a['model_string'])
                manual = manual_native_prediction(booster, z)
                actual = core.predict_arrays(a, probe)
                error = float(np.max(np.abs(manual - actual)))
                assert np.isfinite(actual).all() and error < 1e-10
                pilot_predictions[name] = core.predict_arrays(a, x)
                check = {'model': name, 'target': cfg['target'], 'native_objective': 'quantile',
                    'alpha': cfg['alpha'], 'actual_training_rows': len(clean),
                    'actual_trees_each_of_two_control_fits': 48,
                    'cutoff_exclusive': cutoff, 'last_training_date': int(clean['trade_date'].max()),
                    'training_matrix_sha256': native.array_hash(x),
                    'training_target_sha256': native.array_hash(y),
                    'training_key_sha256': native.array_hash(clean.select(native.KEYS).hash_rows(seed=2026).to_numpy()),
                    'future_label_poison_retraining_and_preprocessing_bit_identical': True,
                    'actual_cold80_training_validation_rows': len(cold80),
                    'actual_cold80_days': 80, 'actual_codes': 4650,
                    'actual_cold80_native_reload_bit_identical': True,
                    'actual37_day_cold_prefix_and_later_feature_poison_bit_identical': True,
                    'independent_dumped_leaf_sum_max_abs_error': error,
                    'NaN_inf_missing_and_finite_zero_controls_passed': True,
                    'native_model_sha256': sha(model), 'cold80_raw_array_sha256': native.array_hash(values),
                    'elapsed_seconds': time.monotonic() - fit_started,
                    'actual_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
                checks.append(check)
                print(json.dumps({'status': 'passed_actual_quantile_native_controls', 'model': name,
                    'cold80_rows': len(cold80), 'annual_fits': 0, 'quality_scores': 0}), flush=True)
                del a, b, values, changed_x, booster, x, y, past, future, sample, poisoned, clean, changed
                gc.collect()
            return_names = [name for name in core.CONFIGS if name.startswith('return_')]
            assert all(not np.array_equal(pilot_predictions[a], pilot_predictions[b])
                for i, a in enumerate(return_names) for b in return_names[i+1:])
            cache.reverify()
        create(OUT / 'verification.json', {'status': 'passed_actual_quantile_native_maturity_reload_and_cold80_controls',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source_sha256': bindings,
            'checks': checks, 'actual_native_control_fits': 8, 'actual_annual_fits': 0,
            'planned_full_annual_fits': 20, 'planned_full_final_fits': 4,
            'full_five_year_official_scoring_and_complete_scheme_causality_and_future_still_pending': True,
            'actual_controls_do_not_establish_full_data_resource_feasibility': True,
            'physical_resource_boundary_established': False, 'selection_bias_uncorrected': True,
            'versions': {name: importlib.metadata.version(name)
                for name in ('lightgbm', 'numpy', 'polars', 'joblib')},
            'host_available_bytes_before': before_ram,
            'host_available_bytes_after': psutil.virtual_memory().available,
            'elapsed_seconds': time.monotonic() - started,
            'new_quality_scores': 0, 'test_labels_read': False})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_quantile_native_controls',
            'error': f'{type(error).__name__}: {error}', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S')})
        raise
    finally:
        create(OUT / 'actual_hidden_child_creations.json', {'events': restore()})


if __name__ == '__main__':
    main()
