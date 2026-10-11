"""Dispatch Nyström bundles through their frozen native predictor."""


def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import train_nystrom_ridge_bank_20261004 as native
    original = legacy.predict_arrays

    def predict_arrays(bundle, x, dates=None, valid=None):
        if bundle['kind'] == 'ridge_nystrom':
            return native.predict_arrays(bundle, x)
        return original(bundle, x, dates=dates, valid=valid)

    legacy.predict_arrays = predict_arrays

    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays = original

    return restore
