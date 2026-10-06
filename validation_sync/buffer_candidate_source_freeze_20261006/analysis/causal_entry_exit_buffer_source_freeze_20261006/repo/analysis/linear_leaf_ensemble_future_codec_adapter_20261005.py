"""Install composite codec above linear-leaf and Nyström native codecs."""
def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import build_linear_leaf_ensemble_bank_20261005 as native
    from linear_leaf_future_codec_adapter_20261005 import install as install_previous
    restore_previous=install_previous()
    original=legacy.predict_arrays
    def predict_arrays(bundle,x,dates=None,valid=None):
        if bundle['kind']=='linear_leaf_ensemble':return native.predict_arrays(bundle,x)
        return original(bundle,x,dates=dates,valid=valid)
    legacy.predict_arrays=predict_arrays
    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays=original
        restore_previous()
    return restore
