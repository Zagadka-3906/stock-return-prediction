"""Freeze and infer the actual complete GOSS round76."""
from nystrom_ridge_release_engine_20261004 import install
install(76, globals())

def predict():
    import optimize_training_round76 as experiment
    from predict_gradient_sampling_scheme_20261005 import predict as infer
    assert OUT == experiment.OUT
    assert read(OUT / 'causal_validation.json')['status'] == read(OUT / 'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment, selected())
