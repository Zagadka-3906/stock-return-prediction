"""Actual mature historical CPU codec controls; these are not selection fits or scores."""
from pathlib import Path
import sys
import warnings
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    import numpy as np
    import polars as pl
    import joblib
    from sklearn.ensemble import HistGradientBoostingRegressor
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    from cpu_conditional_residual_hgb_codec_20261007 import fit_preprocessing, prepare, export, predict_native, predict_decoded
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out = A / 'quantile_HGB_codec_preflight_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), A / 'cpu_conditional_residual_hgb_codec_20261007.py',
        A / 'quantile_HGB_native_bank20_plan_20261007.json', ROOT / 'data/features.parquet',
        ROOT / 'data/feature_manifest.json', ROOT / 'run.py']
    pins = {str(p): sha(p) for p in sources}
    create(out / 'frozen_before_actual_controls.json', {'input_sha256': pins,
        'diagnostic_only_no_official_selection_scores': True, 'test_labels_read': False})
    with LockedReadHashCache(pins) as scope, threadpool_limits(limits=4):
        features = read(ROOT / 'data/feature_manifest.json')['features']
        frame = pl.scan_parquet(ROOT / 'data/features.parquet').filter(
            pl.col('is_train') & (pl.col('flag_limit_up') == 1) &
            (pl.col('trade_date') < fold_cutoff(2021)) & pl.col('y_rank').is_finite()
        ).sort(['trade_date', 'ts_code']).select(*features, 'trade_date', 'y_rank').head(601).collect()
        assert len(frame) == 601 and frame['trade_date'].max() < fold_cutoff(2021)
        x = np.column_stack([frame.select(features).to_numpy(), np.zeros(len(frame))]).astype(np.float64)
        y = frame['y_rank'].to_numpy().astype(np.float64)
        preprocessing = fit_preprocessing(x[:512])
        plan = read(A / 'quantile_HGB_native_bank20_plan_20261007.json')
        records = []
        for name, cfg in plan['configurations'].items():
            params = {**plan['fixed_parameters'], **cfg, 'max_iter': 3, 'min_samples_leaf': 16}
            with warnings.catch_warnings(record=True) as captured:
                warnings.simplefilter('always')
                model = HistGradientBoostingRegressor(**params).fit(prepare(x[:512], preprocessing), y[:512])
            bundle = {'model': model, 'preprocessing': preprocessing}
            native = out / (name + '.joblib')
            joblib.dump(bundle, native)
            state_path = out / (name + '.json')
            create(state_path, export(model, preprocessing, [*features, 'zero_diagnostic_extra_feature']))
            actual = predict_native(bundle, x)
            saved = joblib.load(native)
            replay = predict_native(saved, x)
            decoded = predict_decoded(read(state_path), x)
            assert np.array_equal(actual.view('u8'), replay.view('u8'))
            assert np.array_equal(actual.view('u8'), decoded.view('u8'))
            for count in (0, 1, 79, 256, 511, 601):
                assert np.array_equal(actual[:count].view('u8'), predict_native(saved, x[:count]).view('u8'))
                assert np.array_equal(actual[:count].view('u8'), predict_decoded(read(state_path), x[:count]).view('u8'))
            records.append({'name': name, 'actual_iterations': model.n_iter_, 'actual_training_rows': 512,
                'actual_full_prediction_rows': 601, 'prefix_row_counts': [0, 1, 79, 256, 511, 601],
                'saved_native_reload_independent_decoder_and_prefix_bits_exact': True,
                'native_sha256': sha(native), 'independent_state_sha256': sha(state_path),
                'warnings': [str(w.message) for w in captured]})
        scope.reverify()
        create(out / 'verification.json', {'status': 'passed_actual_four_historical_quantile_HGB_codec_controls',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'actual_diagnostic_fits': 4, 'actual_selection_model_fits': 0, 'actual_official_scores': 0,
            'records': records, 'no_CUDA_or_torch_used': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
