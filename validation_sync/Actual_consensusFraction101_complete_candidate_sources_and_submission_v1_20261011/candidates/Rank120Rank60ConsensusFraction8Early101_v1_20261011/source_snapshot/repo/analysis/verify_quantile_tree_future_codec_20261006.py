"""Independently test copied inference and restored ancestor codec bindings."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_tree_codec_preflight_20261006'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import numpy as np
    import polars as pl
    import quantile_tree_candidate_20261006 as core
    import quantile_tree_future_codec_20261006 as codec
    import fourier_tuning_model_sources_20261004 as legacy
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    initial = A / 'quantile_tree_preflight_20261006/verification.json'
    proof = json.loads(initial.read_text(encoding='utf-8'))
    assert proof['status'] == 'passed_actual_quantile_native_maturity_reload_and_cold80_controls'
    assert not OUT.exists()
    OUT.mkdir()
    bindings = {**proof['source_sha256'], **{str(p.resolve()): sha(p)
        for p in (Path(__file__), Path(codec.__file__), initial,
            A / 'classifier_consensus_future_codec_adapter_20261005.py')}}
    create(OUT / 'frozen_before_controls.json', {'input_sha256': bindings,
        'actual_native_control_fits_planned': 4, 'actual_annual_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False})
    native = core.matched.engine
    checks = []
    try:
        with LockedReadHashCache(bindings) as cache:
            lazy = pl.scan_parquet(native.FEATURE_FILE)
            features, cutoff = native.feature_names(), native.fold_cutoff(2020)
            dates = (lazy.filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == 2020))
                .select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_list())
            frame = (lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= dates[0])
                & (pl.col('trade_date') <= dates[79])).select(native.KEYS + features)
                .sort('trade_date', 'ts_code').collect())
            assert len(frame) == 372000
            x = native.to_matrix(frame, features)
            expected = {row['model']: row for row in proof['checks']}
            for name, cfg in core.CONFIGS.items():
                past = native.training_frame(lazy, cutoff, cfg).select(features + [cfg['target']]).head(4096).collect()
                bundle = core.fit_arrays(native.to_matrix(past, features), past[cfg['target']].to_numpy(),
                                         dict(cfg, num_boost_round=48))
                direct = codec.predict_arrays(bundle, x)
                assert native.array_hash(direct) == expected[name]['cold80_raw_array_sha256']
                assert np.array_equal(direct, core.predict_arrays(bundle, x))
                assert np.array_equal(direct[:80 * 4650], codec.predict_arrays(bundle, x[:80 * 4650]))
                assert np.array_equal(direct[:37 * 4650], codec.predict_arrays(bundle, x[:37 * 4650]))
                original = legacy.predict_arrays
                restore = codec.install()
                try:
                    assert np.array_equal(direct, legacy.predict_arrays(bundle, x))
                finally:
                    restore()
                assert legacy.predict_arrays is original
                # The copied inference module has no project/training imports: execute
                # its actual source with a candidate-local __file__ and native bundle.
                namespace = {'__name__': 'copied_quantile_codec', '__file__': str(OUT / 'candidate/quantile_tree_future_codec_20261006.py')}
                exec(compile(Path(codec.__file__).read_text(encoding='utf-8'), namespace['__file__'], 'exec'), namespace)
                assert np.array_equal(direct, namespace['predict_arrays'](bundle, x))
                checks.append({'model': name, 'actual_control_fit_rows': 4096,
                    'actual_control_fit_iterations': 48, 'actual_cold80_rows': len(x),
                    'original_verified_cold80_array_sha256': expected[name]['cold80_raw_array_sha256'],
                    'independent_direct_codec_bit_identical': True,
                    'copied_candidate_local_codec_without_training_imports_bit_identical': True,
                    'actual_installed_ancestor_codec_route_bit_identical_and_all_bindings_restored': True,
                    'actual37_day_cold_prefix_bit_identical': True,
                    'actual_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
                print(json.dumps({'model': name, 'status': 'passed_actual_independent_copied_codec'}), flush=True)
            cache.reverify()
        create(OUT / 'verification.json', {'status': 'passed',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'checks': checks,
            'source_sha256': bindings, 'actual_native_control_fits': 4,
            'actual_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'complete_five_year_official_quality_and_full_future_scheme_still_pending': True})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_copied_quantile_codec_controls',
            'error': f'{type(error).__name__}: {error}'})
        raise


if __name__ == '__main__':
    main()
