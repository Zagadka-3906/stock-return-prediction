"""Standalone native quantile inference; embedded bundle data is sufficient."""
def predict_arrays(bundle, x):
    import lightgbm as lgb
    import numpy as np
    assert bundle['kind'] == 'lightgbm_quantile_tree'
    cfg = bundle['config']
    booster = lgb.Booster(model_str=bundle['model_string'])
    parts = []
    for offset in range(0, len(x), cfg['chunk_rows']):
        block = np.asarray(x[offset:offset + cfg['chunk_rows']], dtype=np.float64)
        block = np.where(np.isfinite(block), block, np.nan)
        z = np.clip((block - bundle['mean']) / bundle['scale'], -cfg['clip_z'], cfg['clip_z']).astype(np.float32)
        parts.append(booster.predict(z, num_threads=1))
    return np.concatenate(parts) if parts else np.empty(0, dtype=np.float64)


def install():
    import fourier_tuning_model_sources_20261004 as legacy
    from classifier_consensus_future_codec_adapter_20261005 import install as previous
    restore_previous = previous()
    original = legacy.predict_arrays

    def route(bundle, x, dates=None, valid=None):
        if bundle.get('kind') == 'lightgbm_quantile_tree':
            return predict_arrays(bundle, x)
        return original(bundle, x, dates=dates, valid=valid)

    legacy.predict_arrays = route

    def restore():
        assert legacy.predict_arrays is route
        legacy.predict_arrays = original
        restore_previous()

    return restore
