"""Normalize missing layer fields only during inherited constructor warm-up."""
from copy import deepcopy
from pathlib import Path
import importlib
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
TARGETS=tuple(range(29,49))


def normalize(configuration,fields):
    missing=[key for key in fields if key not in configuration]
    if not missing:return configuration
    result=deepcopy(configuration)
    for key in missing:
        if key.endswith('_augmentation'):
            result[key]={role:{'model':'none','weight':0.} for role in ('membership','top','rest')}
        elif key.endswith('_limit_delta'):result[key]=0.
        elif key=='standalone':result[key]=None
        elif key=='standalone_replacement':result[key]=False
        else:raise AssertionError(('Unexpected missing ancestor field',key))
    return result


def install_context(module):
    if getattr(module,'_late_constructor_recovery_installed',False):return module.Context
    original=module.Context
    class RecoveredContext(original):
        def __init__(self,*args,**kwargs):
            self._late_constructor_warming=True;self._late_normalized_field_events=[]
            try:super().__init__(*args,**kwargs)
            finally:self._late_constructor_warming=False
        def configure(self,cfg):
            if getattr(self,'_late_constructor_warming',False):
                missing=[key for key in module.FIELDS if key not in cfg]
                if missing:self._late_normalized_field_events.append(missing)
                cfg=normalize(cfg,module.FIELDS)
            return super().configure(cfg)
    module.Context=RecoveredContext;module._late_constructor_recovery_installed=True
    return RecoveredContext


def install_pool_routes():
    import parallel_candidate_scoring_four_20261004 as pool
    if getattr(pool,'_late_context_routes_installed',False):return
    original_evaluate=pool.evaluate_many;original_shutdown=pool.shutdown
    routes={f'optimize_training_round{number}':f'optimize_training_round{number}_context_recovery_20261004' for number in TARGETS}
    def evaluate_many(module_name,*args,**kwargs):
        return original_evaluate(routes.get(module_name,module_name),*args,**kwargs)
    def shutdown(module_name=None):return original_shutdown(routes.get(module_name,module_name))
    pool.evaluate_many=evaluate_many;pool.shutdown=shutdown;pool._late_context_routes_installed=True


def verify_binding(module):
    path=module.OUT/'context_initialization_recovery_protocol.json'
    value=module.read(path)
    for source,digest in value['input_sha256'].items():assert module.sha(source)==digest,source
    return value


def bind_execution(module,number):
    proof=ROOT/'analysis/late_context_initialization_recovery_20261004/verification.json'
    assert module.read(proof)['status']=='passed'
    module.OUT.mkdir(exist_ok=True)
    path=module.OUT/'context_initialization_recovery_protocol.json'
    sources=[Path(__file__),proof,ROOT/'analysis/run_late_context_recovered_pipeline_20261004.py',
             ROOT/f'analysis/optimize_training_round{number}_context_recovery_20261004.py',
             ROOT/f'analysis/optimize_training_round{number}.py',ROOT/f'analysis/run_training_round{number}_pipeline.py',
             ROOT/'analysis/parallel_candidate_scoring_four_20261004.py']
    for source,digest in module.read(proof)['input_sha256'].items():assert module.sha(source)==digest,source
    if not path.exists():
        module.dump(path,{'status':'frozen_before_recovered_execution','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'round':number,'actual_worker_factory':f'optimize_training_round{number}_context_recovery_20261004',
            'scope':'Constructor-only typed zero defaults for layer fields absent from older ancestor warm-up configurations. Final complete configurations, prediction formulas, arms andofficial scoring unchanged.',
            'original_protocol_preserved_if_already_frozen':True,'test_labels_read':False,
            'input_sha256':{str(source.resolve()):module.sha(source) for source in sources}},immutable=True)
    verify_binding(module)
    original_verify=module.verify;original_dump=module.dump
    def verify():
        original=original_verify();verify_binding(module);return original
    def dump(path_to_write,payload,*args,**kwargs):
        target=Path(path_to_write)
        if target==module.OUT/'protocol.json':
            payload={**payload,'input_sha256':{**payload['input_sha256'],str(path.resolve()):module.sha(path)},
                     'context_initialization_recovery':str(path.resolve())}
        elif target==module.OUT/'selection.json':
            payload={**payload,'frozen_sha256':{**payload['frozen_sha256'],path.relative_to(ROOT).as_posix():module.sha(path)},
                     'context_initialization_recovery':str(path.resolve())}
        return original_dump(path_to_write,payload,*args,**kwargs)
    module.verify=verify;module.dump=dump


def install(number,bind=False):
    assert number in TARGETS
    module=importlib.import_module(f'optimize_training_round{number}')
    install_context(module);install_pool_routes()
    if bind:bind_execution(module,number)
    return module
