"""Standalone GOSS inference using only a saved bundle and raw feature matrix."""
import numpy as np
import lightgbm as lgb


def predict(bundle, matrix):
    assert bundle['kind'] == 'lightgbm_gradient_sampling'
    cfg = bundle['config']
    assert cfg['data_sample_strategy'] == 'goss'
    mean = np.asarray(bundle['mean'], dtype=np.float64)
    scale = np.asarray(bundle['scale'], dtype=np.float64)
    assert matrix.shape[1] == len(mean) == len(scale) == 63
    booster = lgb.Booster(model_str=bundle['model_string'])
    assert booster.current_iteration() == cfg['num_boost_round'] == 300
    output = np.empty(len(matrix), dtype=np.float64)
    # An independently chosen block size also checks that row boundaries do not
    # alter the original elementwise preprocessing or native tree predictions.
    for offset in range(0, len(matrix), 8192):
        values = np.array(matrix[offset:offset + 8192], dtype=np.float64, copy=True)
        values[~np.isfinite(values)] = np.nan
        values = np.clip((values - mean) / scale, -cfg['clip_z'], cfg['clip_z']).astype(np.float32)
        output[offset:offset + len(values)] = booster.predict(values, num_threads=1)
    return output
