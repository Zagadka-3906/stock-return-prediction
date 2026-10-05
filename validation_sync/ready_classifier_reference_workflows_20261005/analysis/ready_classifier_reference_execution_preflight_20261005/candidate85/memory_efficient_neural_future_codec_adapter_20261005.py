"""Route the memory-layout MLPs above the complete GOSS/inherited codec."""
def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import train_memory_efficient_neural_bank_20261005 as native
    from gradient_sampling_future_codec_adapter_20261005 import install as install_previous
    restore_previous = install_previous()
    original = legacy.predict_arrays
    def predict_arrays(bundle,x,dates=None,valid=None):
        if bundle.get('kind')=='mlp' and bundle.get('config',{}).get('memory_mode') in ('accumulate','checkpoint','combined'):
            return native.engine.predict_arrays(bundle,x)
        return original(bundle,x,dates=dates,valid=valid)
    legacy.predict_arrays = predict_arrays
    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays = original
        restore_previous()
    return restore
