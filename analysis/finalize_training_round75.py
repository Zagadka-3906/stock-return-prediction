"""Freeze and infer the actual complete GOSS round75."""
from nystrom_ridge_release_engine_20261004 import install
install(75, globals())

def predict():
    import optimize_training_round75 as experiment
    from predict_gradient_sampling_scheme_20261005 import predict as infer
    assert OUT == experiment.OUT
    assert read(OUT / 'causal_validation.json')['status'] == read(OUT / 'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment, selected())
