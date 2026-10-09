"""Native no-dropout seed routing, with original selected control reused."""
import regularization_model_sources_20261003 as previous
import train_no_dropout_seed_bank_20261004 as bank
CONFIGS = {**previous.CONFIGS, **bank.CONFIGS}
NEW_CONFIGS = bank.CONFIGS
YEARS = bank.YEARS
read, dump, sha, log = bank.read, bank.dump, bank.sha, bank.log


def source_dir(name):
    assert name in CONFIGS
    return bank.OUT / name if name in bank.CONFIGS else previous.source_dir(name)


def model_path(name, year):
    return source_dir(name) / f'model_{year}.joblib'


def train_one(name, year):
    return bank.train_one(name, year) if name in bank.CONFIGS else previous.train_one(name, year)


def load_bundle(path):
    return previous.load_bundle(path)


def predict_arrays(bundle, x, dates=None, valid=None):
    return previous.predict_arrays(bundle, x, dates=dates, valid=valid)


def verify():
    previous.verify()
    bank.verify()
    assert read(bank.OUT / 'oof_audit.json')['status'] == 'passed'
