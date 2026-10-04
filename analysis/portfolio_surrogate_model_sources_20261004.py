"""Route frozen old models andthe four mature portfolio-loss fine-tuning extensions."""
import neural_width_model_sources_20261004 as previous
import train_portfolio_surrogate_bank_20261004 as native
CONFIGS={**previous.CONFIGS,**native.CONFIGS}
NEW_CONFIGS=native.CONFIGS
YEARS=native.YEARS
read,dump,sha,log=native.read,native.dump,native.sha,native.log

def source_dir(name):
    assert name in CONFIGS
    return native.OUT/name if name in NEW_CONFIGS else previous.source_dir(name)

def model_path(name,year):return source_dir(name)/f'model_{year}.joblib'
def train_one(name,year):return native.train_one(name,year) if name in NEW_CONFIGS else previous.train_one(name,year)
def load_bundle(path):return previous.load_bundle(path)
def predict_arrays(bundle,x,dates=None,valid=None):return previous.predict_arrays(bundle,x,dates=dates,valid=valid)
def ranker_source(name,output):return output/f'rankers/{name}.npy' if name in NEW_CONFIGS else previous.ranker_source(name,output)
def verify():
    previous.verify();native.verify()
    assert read(native.OUT/'oof_audit.json')['status']=='passed'
