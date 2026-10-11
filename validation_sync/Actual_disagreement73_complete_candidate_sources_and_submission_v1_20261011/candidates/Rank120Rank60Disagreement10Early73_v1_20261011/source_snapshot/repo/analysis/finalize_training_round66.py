"""Freeze, calibrate and infer the expanded kernel standalone winner."""
from nystrom_ridge_release_engine_20261004 import install
install(66, globals())


def predict():
    import optimize_training_round66 as experiment
    from predict_nystrom_tuning_scheme_20261005 import predict as infer
    assert read(OUT / 'causal_validation.json')['status'] == read(OUT / 'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment, selected())
