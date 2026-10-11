"""Lazy versioned handoff to original R53/R54 stages with declared SHA scope."""
from pathlib import Path
import argparse
import importlib
import json
import runpy
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def gates(number):
    return [ROOT/f'results/optimization_20261003_r{number-1}.json',
        ROOT/'analysis/no_dropout_seed_bank_20261004/oof_audit.json',
        ROOT/'analysis/no_dropout_ensemble_bank_20261004/oof_audit.json',
        ROOT/'analysis/no_dropout_seed_future_models_qa_20261004/verification.json',
        ROOT/'analysis/no_dropout_seed_search_generator_preflight_20261004/verification.json',
        ROOT/'analysis/no_dropout_seed_complete_scheme_preflight_20261004/verification.json',
        ROOT/'analysis/locked_no_dropout_complete_scheme_preflight_20261004/verification.json',
        ROOT/'analysis/no_dropout_frozen_provenance_execution_preflight_20261004/verification.json']

def main(number,probe=False):
    assert number in (53,54)
    if probe:
        import psutil
        print(json.dumps({'round':number,'lazy_imports_only':not any(n in sys.modules for n in ('numpy','polars','torch','pandas')),
            'python_rss_bytes':psutil.Process().memory_info().rss,'gates':[str(p) for p in gates(number)]}),flush=True)
        return
    state_path=ROOT/f'analysis/ongoing_optimization_r{number}_state.json'
    while not all(p.exists() for p in gates(number)):
        state_path.write_text(json.dumps({'round':number,'stage':'waiting_for_actual_previous_round_andlocked_execution_checks',
            'status':'running','updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'pending':[str(p) for p in gates(number) if not p.exists()],
            'continuous_optimization_authorized':True,'test_labels_read':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        time.sleep(10)
    for p in gates(number):
        value=read(p);assert value['status'] in ('passed','complete'),p
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    from locked_read_hash_cache_20261004 import fresh_sha
    module=importlib.import_module(f'optimize_training_round{number}')
    importlib.import_module(f'finalize_training_round{number}')
    sources=[Path(__file__),ROOT/'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT/'analysis/locked_read_hash_cache_20261004.py',ROOT/f'analysis/run_training_round{number}_pipeline.py',
        ROOT/'analysis/run_no_dropout_seed_round_pipeline_20261004.py',*gates(number)[-2:]]
    metadata={'script':str(Path(__file__).resolve()),'round':number,'delegate':f'analysis/run_training_round{number}_pipeline.py',
        'driver_source_sha256':fresh_sha(Path(__file__)),'original_stage_order_andalgorithms_unchanged':True}
    scope=FrozenProvenanceExecutionScope(module,sources,metadata,ROOT/'analysis').install();failure=None
    try:runpy.run_path(str(ROOT/f'analysis/run_training_round{number}_pipeline.py'),run_name='__main__')
    except BaseException as error:failure=f'{type(error).__name__}: {error}';raise
    finally:
        report=scope.close(failed=failure is not None)
        destination=module.OUT/'provenance_scope_execution.json'
        destination.parent.mkdir(parents=True,exist_ok=True)
        with destination.open('x',encoding='utf-8') as stream:
            json.dump({'status':'passed' if failure is None else 'failed','failure':failure,
                'updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),**report,
                'new_model_fits':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('number',type=int,choices=(53,54));parser.add_argument('--probe',action='store_true')
    arguments=parser.parse_args();main(arguments.number,arguments.probe)
