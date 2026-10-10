"""Keep exact rank caching and add proven date-index execution in owned official workers."""
import atexit
from pathlib import Path
from official_date_index_dataframe_adapter_20261007 import installed
import exact_rank_cache_official_worker_adapter_20261006 as rank

original = rank.original
MAXIMUM_BYTES = rank.MAXIMUM_BYTES


_CONFIGURE_BINDINGS=[]

def _install_score(context):
    if context.__dict__.get('_owned_actual_date_index_score_installed',False):
        return
    original_score=context.score
    def score(pred):
        with installed(Path(context.scoring)/'submission.csv') as events:
            metrics=original_score(pred)
        context.last_actual_date_index_execution=dict(events)
        assert events['date_index_lookups']>=0
        return metrics
    context.score=score
    context._owned_actual_date_index_score_installed=True

def install_context(context):
    cls=type(context)
    if not cls.__dict__.get('_owned_actual_date_index_configure_installed',False):
        original_configure=cls.configure
        def configure(instance,*args,**kwargs):
            result=original_configure(instance,*args,**kwargs)
            _install_score(instance)
            return result
        cls.configure=configure
        cls._owned_actual_date_index_configure_installed=True
        _CONFIGURE_BINDINGS.append((cls,original_configure,configure))
    _install_score(context)

def restore_context_classes():
    for cls,original_configure,configure in reversed(_CONFIGURE_BINDINGS):
        assert cls.configure is configure
        cls.configure=original_configure
        delattr(cls,'_owned_actual_date_index_configure_installed')
    _CONFIGURE_BINDINGS.clear()


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
        restore_context_classes()

    return restore
