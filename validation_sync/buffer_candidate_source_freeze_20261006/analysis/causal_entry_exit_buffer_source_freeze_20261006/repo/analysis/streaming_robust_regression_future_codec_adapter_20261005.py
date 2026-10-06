"""Install classification above all inherited complete future model codecs."""
def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import train_streaming_robust_regression_bank_20261005 as native
    from streaming_rank_classifier_future_codec_adapter_20261005 import install as install_previous
    restore_previous = install_previous()
    original = legacy.predict_arrays
    def predict_arrays(bundle,x,dates=None,valid=None):
        if bundle.get('kind') == 'streaming_robust_regression': return native.core.predict_arrays(bundle,x)
        return original(bundle,x,dates=dates,valid=valid)
    legacy.predict_arrays = predict_arrays
    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays = original
        restore_previous()
    return restore
