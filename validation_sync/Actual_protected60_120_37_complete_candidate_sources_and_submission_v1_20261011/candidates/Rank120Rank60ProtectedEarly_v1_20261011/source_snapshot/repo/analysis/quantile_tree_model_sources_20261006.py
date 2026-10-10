"""Route full quantile models and preserve every ancestor family."""
import classifier_consensus_model_sources_20261005 as previous
import train_quantile_tree_bank_20261006 as native
CONFIGS={**previous.CONFIGS,**native.CONFIGS}
NEW_CONFIGS=native.CONFIGS
YEARS=native.YEARS
read,dump,sha,log=native.read,native.dump,native.sha,native.log
def source_dir(name):
    assert name in CONFIGS
    return native.OUT/name if name in NEW_CONFIGS else previous.source_dir(name)
def model_path(name,year):return source_dir(name)/f"model_{year}.joblib"
def load_bundle(path):return native.engine.load_bundle(path)
def predict_arrays(bundle,x,dates=None,valid=None):
    if bundle.get("kind")=="lightgbm_quantile_tree":return native.predict_arrays(bundle,x)
    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)
