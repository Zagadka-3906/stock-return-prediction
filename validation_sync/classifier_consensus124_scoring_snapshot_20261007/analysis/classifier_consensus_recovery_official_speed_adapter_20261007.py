"""Keep exact rank caching and add proven date-index execution in owned official workers."""
import atexit
from pathlib import Path
from official_date_index_dataframe_adapter_20261007 import installed
import exact_rank_cache_official_worker_adapter_20261006 as rank

original = rank.original
MAXIMUM_BYTES = rank.MAXIMUM_BYTES


def install_context(context):
    original = context.score

    def score(pred):
        with installed(Path(context.scoring) / 'submission.csv') as events:
            metrics = original(pred)
        context.last_actual_date_index_execution = dict(events)
        assert events['date_index_lookups'] >= 0
        return metrics

    context.score = score


def initialize(module_name, output, slots):
    rank.initialize(module_name, output, slots)
    install_context(rank.original._CONTEXT)


def evaluate(job):
    key, row = rank.evaluate(job)
    row['actual_original_official_date_index_execution'] = dict(rank.original._CONTEXT.last_actual_date_index_execution)
    return key, row


def install():
    restore_rank = rank.install()
    assert rank.original._initialize is rank.initialize
    rank.original._initialize, rank.original._evaluate = initialize, evaluate

    def restore():
        assert not rank.original._POOLS
        assert rank.original._initialize is initialize and rank.original._evaluate is evaluate
        rank.original._initialize, rank.original._evaluate = rank.initialize, rank.evaluate
        restore_rank()

    return restore
