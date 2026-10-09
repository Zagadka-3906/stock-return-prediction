"""Install exact bounded rank execution inside the actual Windows scoring initializer."""
import atexit
from pathlib import Path
import parallel_candidate_scoring_one_20261005 as original
from exact_daily_rank_memoization_20261006 import install as install_cache

ROOT = Path(__file__).resolve().parents[1]
MAXIMUM_BYTES = 1024 * 1024**2
_INITIALIZE = original._initialize
_EVALUATE = original._evaluate
_CACHE = None


def initialize(module_name, output, slots):
    global _CACHE
    _INITIALIZE(module_name, output, slots)
    assert _CACHE is None
    _CACHE, restore = install_cache(maximum_bytes=MAXIMUM_BYTES)
    atexit.register(restore)


def evaluate(job):
    assert _CACHE is not None
    before = _CACHE.statistics()
    key, row = _EVALUATE(job)
    row['exact_daily_rank_execution'] = {
        'bounded_original_function_memoization': True, 'maximum_bytes': MAXIMUM_BYTES,
        'installed_in_actual_scoring_worker': True, 'before': before, 'after': _CACHE.statistics(),
        'same_values_mask_dates_dtype_shape_required': True,
        'scientific_configuration_and_official_evaluator_unchanged': True,
        'adapter_source': str(Path(__file__).resolve())}
    return key, row


def install():
    assert not original._POOLS, 'Install before creating any scoring executor.'
    assert original._initialize is _INITIALIZE and original._evaluate is _EVALUATE
    original._initialize, original._evaluate = initialize, evaluate

    def restore():
        assert not original._POOLS, 'Shut down all scoring pools before restoring the adapter.'
        assert original._initialize is initialize and original._evaluate is evaluate
        original._initialize, original._evaluate = _INITIALIZE, _EVALUATE

    return restore
