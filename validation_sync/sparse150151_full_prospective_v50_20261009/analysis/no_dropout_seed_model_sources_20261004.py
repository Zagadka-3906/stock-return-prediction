"""Route all old signals and the new native/virtual no-dropout configurations."""
import additive_basis_model_sources_20261004 as previous
import train_no_dropout_seed_bank_20261004 as native
import train_no_dropout_seed_ensembles_20261004 as virtual
CONFIGS = {**previous.CONFIGS, **native.CONFIGS, **virtual.CONFIGS}
NEW_CONFIGS = {**native.CONFIGS, **virtual.CONFIGS}
YEARS = native.YEARS
read, dump, sha, log = native.read, native.dump, native.sha, native.log


def source_dir(name):
    assert name in CONFIGS
    if name in native.CONFIGS:
        return native.OUT / name
    if name in virtual.CONFIGS:
        return virtual.OUT / name
    return previous.source_dir(name)


def model_path(name, year):
    return source_dir(name) / f'model_{year}.joblib'


def train_one(name, year):
    if name in native.CONFIGS:
        return native.train_one(name, year)
    if name in virtual.CONFIGS:
        return virtual.train_one(name, year)
    return previous.train_one(name, year)


def load_bundle(path):
    return previous.load_bundle(path)


def predict_arrays(bundle, x, dates=None, valid=None):
    return previous.predict_arrays(bundle, x, dates=dates, valid=valid)


def ranker_source(name, output):
    return output / f'rankers/{name}.npy' if name in NEW_CONFIGS else previous.ranker_source(name, output)


def verify():
    previous.verify()
    native.verify()
    virtual.verify()
    assert read(native.OUT / 'oof_audit.json')['status'] == read(virtual.OUT / 'oof_audit.json')['status'] == 'passed'
