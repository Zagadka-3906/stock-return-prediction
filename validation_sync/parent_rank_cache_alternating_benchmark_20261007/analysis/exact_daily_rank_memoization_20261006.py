"""Bounded memoization of the unchanged daily rank function, keyed by all inputs."""
from collections import OrderedDict
from functools import wraps
import hashlib
import sys
import threading
import time
import types
import numpy as np


class DailyRankCache:
    def __init__(self, original, maximum_bytes=512 * 1024**2):
        self.original = original
        self.maximum_bytes = int(maximum_bytes)
        assert self.maximum_bytes > 0
        self.entries = OrderedDict()
        self.bytes = 0
        self.lock = threading.RLock()
        self.hits = self.misses = self.evictions = self.uncacheable = 0
        self.hash_seconds = self.original_seconds = 0.0

    def __call__(self, values, valid, dates):
        started = time.perf_counter()
        digest = hashlib.sha256()
        for array in (values, valid, dates):
            array = np.asarray(array)
            if array.dtype.hasobject:
                self.uncacheable += 1
                return self.original(values, valid, dates)
            contiguous = np.ascontiguousarray(array)
            digest.update(str((array.shape, array.dtype.str)).encode('ascii'))
            digest.update(memoryview(contiguous.view(np.uint8)).cast('B'))
        key = digest.digest()
        self.hash_seconds += time.perf_counter() - started
        with self.lock:
            if key in self.entries:
                self.hits += 1
                result = self.entries.pop(key)
                self.entries[key] = result
                # Preserve the original function's independent mutable return value.
                return result.copy()
            self.misses += 1
        started = time.perf_counter()
        result = self.original(values, valid, dates)
        self.original_seconds += time.perf_counter() - started
        if result.nbytes <= self.maximum_bytes:
            stored = result.copy()
            stored.flags.writeable = False
            with self.lock:
                if key not in self.entries:
                    while self.entries and self.bytes + stored.nbytes > self.maximum_bytes:
                        _, removed = self.entries.popitem(last=False)
                        self.bytes -= removed.nbytes
                        self.evictions += 1
                    self.entries[key] = stored
                    self.bytes += stored.nbytes
                assert self.bytes <= self.maximum_bytes
        return result

    def statistics(self):
        return {'hits': self.hits, 'misses': self.misses, 'evictions': self.evictions,
            'uncacheable_object_input_calls': self.uncacheable, 'retained_bytes': self.bytes,
            'maximum_bytes': self.maximum_bytes, 'hash_seconds': self.hash_seconds,
            'original_function_seconds': self.original_seconds,
            'full_values_valid_mask_dates_dtype_and_shape_hashed': True,
            'cached_returns_copied_to_preserve_mutability': True}


def install(maximum_bytes=512 * 1024**2):
    import optimize_wave15 as ranks
    original = ranks.daily_ranks
    cache = DailyRankCache(original, maximum_bytes)

    @wraps(original)
    def cached(values, valid, dates):
        return cache(values, valid, dates)

    bindings = []
    for module in tuple(sys.modules.values()):
        if isinstance(module, types.ModuleType):
            for name, value in tuple(vars(module).items()):
                if value is original:
                    setattr(module, name, cached)
                    bindings.append((module, name))
    assert (ranks, 'daily_ranks') in bindings

    def restore():
        for module, name in reversed(bindings):
            assert getattr(module, name) is cached
            setattr(module, name, original)
        return cache.statistics()

    return cache, restore
