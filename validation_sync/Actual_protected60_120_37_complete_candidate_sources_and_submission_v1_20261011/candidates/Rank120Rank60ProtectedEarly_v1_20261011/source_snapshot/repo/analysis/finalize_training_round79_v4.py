from nystrom_ridge_release_engine_20261004 import install
install(79,globals())

def predict():
    import optimize_training_round79 as experiment
    from predict_streaming_rank_classifier_scheme_v4_20261005 import predict as infer
    assert OUT == experiment.OUT
    assert read(OUT/'causal_validation.json')['status'] == read(OUT/'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment,selected())
