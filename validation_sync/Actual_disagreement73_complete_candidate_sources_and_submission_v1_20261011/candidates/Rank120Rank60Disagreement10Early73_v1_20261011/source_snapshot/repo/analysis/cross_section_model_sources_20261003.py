"""Route raw-input and current-day percentile-input frozen model bundles."""
from pathlib import Path
import diverse_model_sources_20261003 as previous
import train_cross_section_bank_20261003 as bank
OUT=bank.OUT
CONFIGS={**previous.CONFIGS,**bank.CONFIGS}
NEW_CONFIGS=bank.CONFIGS
YEARS=bank.YEARS
read,dump,sha,log=bank.read,bank.dump,bank.sha,bank.log


def source_dir(name):
    assert name in CONFIGS
    return bank.OUT/name if name in bank.CONFIGS else previous.source_dir(name)


def model_path(name,year):return source_dir(name)/f'model_{year}.joblib'


def train_one(name,year):
    return bank.train_one(name,year) if name in bank.CONFIGS else previous.train_one(name,year)


def load_bundle(path):
    bundle=previous.load_bundle(path);path=Path(path)
    is_cross='cross_section_bank_20261003' in path.parts or any(name in path.name for name in bank.CONFIGS)
    return dict(bundle,current_day_percentile_input=is_cross)


def predict_arrays(bundle,x,dates=None,valid=None):
    if bundle.get('current_day_percentile_input'):
        return bank.predict_arrays(bundle,x,dates=dates,valid=valid)
    return previous.predict_arrays(bundle,x)


def ranker_source(name,output):
    root=Path(__file__).resolve().parents[1]
    if name in bank.CONFIGS:return output/f'rankers/{name}.npy'
    number=15 if name in previous.NEW_CONFIGS else 14
    return root/f'analysis/optimization_20261003_r{number}/rankers/{name}.npy'


def verify():
    previous.verify();bank.verify();assert read(bank.OUT/'oof_audit.json')['status']=='passed'
