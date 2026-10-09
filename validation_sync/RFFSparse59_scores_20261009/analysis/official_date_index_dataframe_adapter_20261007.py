"""Invoke unchanged official code; replace repeated date masks with exact row positions."""
from contextlib import contextmanager
from pathlib import Path
import numpy as np


class DatePositions:
    def __init__(self, owner, positions):
        self.owner = owner
        self.positions = positions


class DateColumn:
    def __init__(self, frame):
        self.frame = frame

    def __getattr__(self, name):
        return getattr(self.frame.value['trade_date'], name)

    def __eq__(self, key):
        if not np.isscalar(key) or bool(np.isnan(key)):
            return self.frame.value['trade_date'] == key
        if self.frame.positions is None:
            self.frame.positions = self.frame.value.groupby('trade_date', sort=False).indices
        positions = self.frame.positions.get(key, np.empty(0, dtype=np.intp))
        self.frame.events['date_index_lookups'] += 1
        return DatePositions(self.frame, positions)


class IndexedFrame:
    def __init__(self, value, events):
        self.value, self.events, self.positions = value, events, None

    def __len__(self):
        return len(self.value)

    def __getattr__(self, name):
        return getattr(self.value, name)

    def merge(self, other, *args, **kwargs):
        if isinstance(other, IndexedFrame):
            other = other.value
        return IndexedFrame(self.value.merge(other, *args, **kwargs), self.events)

    def __getitem__(self, key):
        if isinstance(key, DatePositions):
            assert key.owner is self
            # Return ordinary pandas frames. Every original sorting/filtering rule remains active.
            return self.value.iloc[key.positions]
        if isinstance(key, str) and key == 'trade_date':
            return DateColumn(self)
        return self.value[key]


@contextmanager
def installed(submission_path):
    import evaluate
    original = evaluate.pd
    events = {'date_index_lookups': 0, 'official_source_math_changed': False}
    target = Path(submission_path).resolve()

    class PandasProxy:
        def __getattr__(self, name):
            return getattr(original, name)

        def read_csv(self, path, *args, **kwargs):
            value = original.read_csv(path, *args, **kwargs)
            if isinstance(path, (str, Path)) and Path(path).resolve() == target:
                return IndexedFrame(value, events)
            return value

    evaluate.pd = PandasProxy()
    try:
        yield events
    finally:
        evaluate.pd = original
