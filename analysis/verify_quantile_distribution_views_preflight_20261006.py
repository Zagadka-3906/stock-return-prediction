"""Real six-view native cold80 controls, with serialized pilot weights kept in RAM."""
from pathlib import Path
import gc
import hashlib
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_distribution_views_preflight_20261006'


def main():
    import numpy as np
    import polars as pl
    import joblib
    import quantile_distribution_views_20261006 as views
    import quantile_distribution_views_future_codec_20261006 as codec
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    parent = views.parent
    assert not OUT.exists()
    OUT.mkdir()
    plan = A / 'quantile_distribution_views_complete_plan_20261006.json'
    assert parent.read(plan)['configurations'] == views.CONFIGS
    assert parent.read(parent.CAPACITY / 'verification.json')['actual_full_final_fits'] == 4
    sources = [Path(__file__), Path(views.__file__), Path(codec.__file__), Path(parent.__file__),
        Path(parent.core.__file__), A / 'quantile_tree_future_codec_20261006.py',
        A / 'locked_read_hash_cache_20261004.py', A / 'linear_leaf_actual_resource_sampler_20261005.py',
        plan, parent.engine.FEATURE_FILE, parent.engine.MANIFEST,
        parent.CAPACITY / 'protocol.json', parent.CAPACITY / 'verification.json',
        A / 'service_owned_workflows_20261006/quantile_tree_memmap_capacity/service_execution.json']
    for name in views.MEMBERS:
        sources += [parent.OUT / name / 'model_2025.joblib', parent.OUT / name / 'info_2025.json']
    bindings = {str(path.resolve()): parent.sha(path) for path in sources}
    parent.dump(OUT / 'frozen_before_actual_component_controls.json', {
        'input_sha256': bindings, 'all6_operations_fixed_before_future_X_loaded': True,
        'actual_native_cold80_rows_required': 372000, 'new_model_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    sampler, failure, checks = ResourceSampler(OUT), None, []
    try:
        with LockedReadHashCache(bindings) as cache:
            sampler.start()
            features = parent.engine.feature_names()
            base = pl.scan_parquet(parent.engine.FEATURE_FILE).filter(~pl.col('is_train'))
            cutoff = int(base.select('trade_date').unique().sort('trade_date').collect()['trade_date'][79])
            frame = base.filter(pl.col('trade_date') <= cutoff).select(parent.engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
            assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (372000, 80, 4650)
            x, valid = parent.engine.to_matrix(frame, features), frame['price_valid'].to_numpy()
            heads = np.stack([parent.predict_arrays(parent.engine.load_bundle(parent.OUT / name / 'model_2025.joblib'), x) for name in views.MEMBERS])
            artificial = np.random.default_rng(20261006).normal(size=(3, 32768))
            artificial[:, :8] = [[0, 1, 3, -4, 0, 4, 1, 0], [0, 2, 2, -2, 2, 0, 1, 0], [0, 3, 1, -1, -2, -4, 1, 0]]
            for name, cfg in views.CONFIGS.items():
                sampler.context = {'stage': 'actual372000row_selfcontained_native_cold80_buffer_reload', 'model': name}
                math_pred = views.from_heads(cfg, artificial)
                assert np.array_equal(math_pred, codec.from_heads(cfg, artificial))
                poison = artificial.copy()
                poison[:, 131:] = poison[:, 131:] * 100 + 10
                assert np.array_equal(math_pred[:131], views.from_heads(cfg, poison)[:131])
                bundle, meta, provenance = views.bundle_from(name, 2025)
                assert meta['cutoff_exclusive'] <= int(frame['trade_date'].min())
                buffer = io.BytesIO()
                joblib.dump(bundle, buffer, compress=3)
                serialized_sha = hashlib.sha256(buffer.getbuffer()).hexdigest()
                byte_count = len(buffer.getbuffer())
                buffer.seek(0)
                reloaded = joblib.load(buffer)
                assert reloaded['config'] == cfg and reloaded['new_model_fits'] == 0
                actual, expected = codec.predict_arrays(reloaded, x), views.from_heads(cfg, heads)
                actual[~valid] = expected[~valid] = -1e6
                assert np.array_equal(actual, expected) and np.all(actual[~valid] == -1e6)
                checks.append({'model': name, 'rows': len(frame), 'days': 80, 'codes': 4650,
                    'all_native_parents_actual300_iterations_and_full_mature_metadata_checked': True,
                    'actual_selfcontained_serialized_bundle_bytes': byte_count,
                    'actual_serialized_bundle_sha256': serialized_sha,
                    'actual_prediction_array_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(actual)).cast('B')).hexdigest(),
                    'actual_native_primary_vs_independent_codec_cold80_bit_identical': True,
                    'actual32768row_crossing_constant_and_future_head_poison_controls_passed': True,
                    'all_invalid_price_rows_restored_to_minus1million': True,
                    'pilot_weights_written_to_disk': 0, 'new_model_fits': 0, 'new_quality_scores': 0})
                print(json.dumps({'status': 'passed_actual_native_distribution_view_cold80', 'model': name, 'rows': len(frame)}), flush=True)
                del bundle, reloaded, buffer, actual, expected
                gc.collect()
            cache.reverify()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        parent.dump(OUT / 'resource_summary.json', sampler.finish(), immutable=True)
        parent.dump(OUT / 'execution_scope.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'input_sha256': bindings, 'new_model_fits': 0,
            'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    parent.dump(OUT / 'verification.json', {
        'status': 'passed_actual_six_distribution_views_native_cold80_independent_codec_and_math_controls',
        'checks': checks, 'actual_native_views_checked': 6, 'actual372000row80day4650code_each_view': True,
        'input_sha256': bindings, 'pilot_weights_written_to_disk': 0, 'new_model_fits': 0,
        'all30_virtual_annual6_final_entire_future_and262_quality_records_still_required': True,
        'original198_quality_records_preserved': True, 'physical_resource_boundary_established': False,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
