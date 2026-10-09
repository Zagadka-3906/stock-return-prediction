"""Route learned past-OOF meta models and every earlier frozen backbone."""
import regularization_model_sources_20261003 as previous
import train_oof_stacking_bank_20261004 as bank
import causal_model_loading_20261004 as loading
loading.install(bank.members)
OUT=bank.OUT
CONFIGS={**previous.CONFIGS,**bank.CONFIGS}
NEW_CONFIGS=bank.CONFIGS
YEARS=bank.YEARS
read,dump,sha,log=bank.read,bank.dump,bank.sha,bank.log


def source_dir(name):
    assert name in CONFIGS
    return bank.OUT/name if name in bank.CONFIGS else previous.source_dir(name)


def model_path(name,year):return source_dir(name)/f'model_{year}.joblib'
def train_one(name,year):return bank.train_one(name,year) if name in bank.CONFIGS else previous.train_one(name,year)
def load_bundle(path):return bank.load_bundle(path) if 'oof_' in str(path) else loading.load_bundle(path)
def predict_arrays(bundle,x,dates=None,valid=None):
    if bundle['kind']=='past_oof_ridge':return bank.predict_arrays(bundle,x,dates=dates,valid=valid)
    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)


def ranker_source(name,output):
    if name in bank.CONFIGS:return output/f'rankers/{name}.npy'
    return previous.ranker_source(name,output)


def verify():
    previous.verify();bank.verify();assert read(bank.OUT/'oof_audit.json')['status']=='passed'
    for path,digest in read(bank.OUT/'input_routing_recovery_protocol.json')['input_sha256'].items():assert sha(path)==digest,path
