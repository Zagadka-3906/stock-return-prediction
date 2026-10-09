"""Install FM NumPy weights above all inherited native prediction codecs."""
def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import train_factorization_machine_bank_20261005 as native
    from linear_leaf_ensemble_future_codec_adapter_20261005 import install as install_previous
    restore_previous=install_previous()
    original=legacy.predict_arrays
    def predict_arrays(bundle,x,dates=None,valid=None):
        if bundle['kind']=='factorization_machine':return native.predict_arrays(bundle,x)
        return original(bundle,x,dates=dates,valid=valid)
    legacy.predict_arrays=predict_arrays
    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays=original
        restore_previous()
    return restore
