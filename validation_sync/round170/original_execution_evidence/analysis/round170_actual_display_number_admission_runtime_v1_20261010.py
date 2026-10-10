"""Bind the actual round170 display while retaining its original empty E-junction checks."""
from contextlib import contextmanager
from pathlib import Path

def admit(path,number,create=True):
    import cross120170_storage_v1_20261010 as storage
    assert number==170
    assert Path(path)==storage.ROOT/'analysis/lossless_ranking_display_v2_20261006/round170'
    storage.empty(path)

@contextmanager
def installed():
    import cross120170_storage_v1_20261010 as storage
    original=storage.ensure_display;storage.ensure_display=admit
    try:yield
    finally:
        assert storage.ensure_display is admit
        storage.ensure_display=original
