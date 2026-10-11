"""Evaluate prespecified candidates in two isolated processes; preserve commit order."""
from __future__ import annotations
import atexit
import importlib
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORKERS=2
_POOLS={}
_CONTEXT=None
_MODULE=None
_SLOT=None


def _initialize(module_name,out,slots):
    global _CONTEXT,_MODULE,_SLOT
    _SLOT=slots.get(timeout=60)
    _MODULE=importlib.import_module(module_name)
    _CONTEXT=_MODULE.Context()
    source=Path(_CONTEXT.scoring)
    folder=Path(out)/'parallel_official_workers'/f'worker_{_SLOT}'/'scoring_validation_only'
    folder.mkdir(parents=True,exist_ok=True)
    for name in ('测试集_X.csv','测试集_Y.csv'):
        target=folder/name
        if target.exists():
            assert os.path.samefile(source/name,target),(source/name,target)
        else:os.link(source/name,target)
    _CONTEXT.scoring=folder


def _evaluate(job):
    key,cfg=job
    # Each process owns its prediction CSV and scorer globals. Bound signal-cache RAM.
    for name in ('_diverse_cache','_final_cache','_regime_cache','_raw_cache','_linear_cache','_regularization_cache'):
        value=getattr(_CONTEXT,name,None)
        if isinstance(value,dict):value.clear()
    row=_MODULE.evaluate(_CONTEXT,cfg)
    row['parallel_execution']={'worker_slot':_SLOT,'worker_pid':os.getpid(),
                               'private_scoring_directory':str(_CONTEXT.scoring),
                               'same_declared_configuration':True}
    return key,row


def evaluate_many(module_name,jobs,out):
    """Yield in declared order; stage-dependent callers decide subsequent batches."""
    jobs=list(jobs)
    if not jobs:return
    out=Path(out).resolve()
    assert out.is_relative_to(ROOT/'analysis')
    identity=(module_name,str(out))
    if identity not in _POOLS:
        for slot in range(WORKERS):
            (out/'parallel_official_workers'/f'worker_{slot}'/'identical_official_scores').mkdir(parents=True,exist_ok=True)
        spawn=multiprocessing.get_context('spawn');slots=spawn.Queue()
        for slot in range(WORKERS):slots.put(slot)
        executor=ProcessPoolExecutor(max_workers=WORKERS,mp_context=spawn,initializer=_initialize,
                                     initargs=(module_name,str(out),slots))
        _POOLS[identity]=(executor,slots)
    executor,_=_POOLS[identity]
    yield from executor.map(_evaluate,jobs,chunksize=1)


def shutdown(module_name=None):
    for identity,(executor,slots) in list(_POOLS.items()):
        if module_name is None or identity[0]==module_name:
            executor.shutdown(wait=True,cancel_futures=False)
            slots.close();slots.join_thread();del _POOLS[identity]


atexit.register(shutdown)
