"""Freeze the latest graph, calibrate mature past OOF, then infer copied models."""
from nystrom_ridge_release_engine_20261004 import install
install(63, globals())


def predict():
    assert read(OUT / 'causal_validation.json')['status'] == read(OUT / 'calibrated_csv_official.json')['status'] == 'passed'
    from predict_latest_joint_scheme_20261005 import predict as infer
    infer(selected())
