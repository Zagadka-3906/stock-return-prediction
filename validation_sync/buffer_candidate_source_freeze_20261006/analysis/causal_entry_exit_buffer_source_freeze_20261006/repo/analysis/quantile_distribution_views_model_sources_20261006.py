"""Add self-contained fixed distribution views, retaining every earlier route."""
import quantile_tree_model_sources_20261006 as previous
import build_quantile_distribution_views_bank_20261006 as native

CONFIGS = {**previous.CONFIGS, **native.CONFIGS}
NEW_CONFIGS = native.CONFIGS
YEARS = native.YEARS
read, dump, sha, log = native.read, native.dump, native.sha, native.log


def source_dir(name):
    assert name in CONFIGS
    return native.OUT / name if name in NEW_CONFIGS else previous.source_dir(name)


def model_path(name, year):
    return source_dir(name) / f'model_{year}.joblib'


def load_bundle(path):
    return native.engine.load_bundle(path)


def predict_arrays(bundle, x, dates=None, valid=None):
    if bundle.get('kind') == 'quantile_distribution_view':
        return native.predict_arrays(bundle, x)
    return previous.predict_arrays(bundle, x, dates=dates, valid=valid)
