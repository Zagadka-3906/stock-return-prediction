"""Preserve frozen current-day input preprocessing when using a generic loader."""
from pathlib import Path
import linear_model_sources_20261003 as generic
import train_cross_section_bank_20261003 as cross_section
_installed={}


def annotate(bundle,path):
    path=Path(path)
    is_cross=('cross_section_bank_20261003' in path.parts or
              any(name in path.parts or name in path.name for name in cross_section.CONFIGS))
    if is_cross:
        assert bundle['kind']=='mlp'
        return dict(bundle,current_day_percentile_input=True)
    return bundle


def load_bundle(path):return annotate(generic.load_bundle(path),path)


def install(namespace):
    key=namespace.__name__
    if key not in _installed:
        original=namespace.load_bundle
        def wrapped(path):return annotate(original(path),path)
        _installed[key]=wrapped;namespace.load_bundle=wrapped
    else:assert namespace.load_bundle is _installed[key]

