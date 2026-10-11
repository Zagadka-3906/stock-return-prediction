"""Independent pointwise order/projection with self-contained native bundles."""


def from_heads(cfg, heads):
    import numpy as np
    ordered = np.sort(np.asarray(heads, dtype=np.float64), axis=0)
    assert ordered.ndim == 2 and len(ordered) == 3 and np.isfinite(ordered).all()
    lower, middle, upper = ordered
    if cfg['operation'] == 'midpoint':
        return (lower + upper) * .5
    if cfg['operation'] == 'negative_width':
        return -(upper - lower)
    if cfg['operation'] == 'reflected_upper':
        return -upper
    assert cfg['operation'] == 'median_minus_width'
    return middle - cfg['width_penalty'] * (upper - lower)


def predict_arrays(bundle, x):
    from quantile_tree_future_codec_20261006 import predict_arrays as native
    assert bundle['kind'] == 'quantile_distribution_view'
    assert [item['name'] for item in bundle['members']] == [
        'return_lgb_quantile_a010_r300', 'return_lgb_quantile_a050_r300', 'return_lgb_quantile_a090_r300']
    return from_heads(bundle['config'], [native(item['bundle'], x) for item in bundle['members']])


def install():
    import fourier_tuning_model_sources_20261004 as legacy
    from quantile_tree_future_codec_20261006 import install as previous
    restore_previous = previous()
    original = legacy.predict_arrays

    def route(bundle, x, dates=None, valid=None):
        if bundle.get('kind') == 'quantile_distribution_view':
            return predict_arrays(bundle, x)
        return original(bundle, x, dates=dates, valid=valid)

    legacy.predict_arrays = route

    def restore():
        assert legacy.predict_arrays is route
        legacy.predict_arrays = original
        restore_previous()

    return restore
