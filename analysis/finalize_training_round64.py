"""Select complete agreement-gated output by the unchanged official score."""
from nystrom_ridge_release_engine_20261004 import install
install(64, globals())


def predict():
    assert read(OUT / 'causal_validation.json')['status'] == read(OUT / 'calibrated_csv_official.json')['status'] == 'passed'
    from predict_agreement_scheme_20261005 import predict as infer
    infer(selected())
