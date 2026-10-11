"""Preserve observer failure and support actual GOSS duration schemas without inventing timings."""
from pathlib import Path
import hashlib
import json

A=Path(__file__).resolve().parent


def main():
    old=A/'refresh_gradient_sampling_cost_evidence_20261005.py'
    source=old.read_text(encoding='utf-8')
    assert source.count("info['elapsed_seconds']")==2
    source=source.replace("info['elapsed_seconds']","info.get('elapsed_seconds')")
    source=source.replace("'fit_seconds': info['fit_seconds'],", "'fit_seconds': info['fit_seconds'], 'total_elapsed_seconds_recorded': 'elapsed_seconds' in info,")
    source=source.replace('Extend the actual fit ledger with six matched constant/linear leaf configurations.', 'Observe six complete GOSS configurations; missing total elapsed timing stays unknown.')
    new=A/'refresh_gradient_sampling_cost_evidence_v2_20261006.py'
    compile(source,str(new),'exec')
    with new.open('x',encoding='utf-8',newline='\n') as stream:stream.write(source)
    monitor=(A/'monitor_actual_optimization_progress_v29_20261006.py').read_text(encoding='utf-8')
    monitor=monitor.replace('actual_observer_version=29','actual_observer_version=30').replace("'actual_observer_version': 29","'actual_observer_version': 30")
    hook='''
def with_actual_GOSS_cost_schema(function):
    def call():
        import refresh_gradient_sampling_cost_evidence_20261005 as legacy
        import refresh_gradient_sampling_cost_evidence_v2_20261006 as actual
        from atomic_optimization_observer_writes_20261005 import operational_writes
        old = legacy.main
        legacy.main = actual.main
        try:
            with operational_writes('refresh_gradient_sampling_cost_evidence_v2_20261006'):
                return function()
        finally:
            legacy.main = old
    return call


update = with_actual_GOSS_cost_schema(update)

'''
    assert monitor.count('def main():')==1
    monitor=monitor.replace('def main():',hook+'def main():')
    path=A/'monitor_actual_optimization_progress_v30_20261006.py'
    compile(monitor,str(path),'exec')
    with path.open('x',encoding='utf-8',newline='\n') as stream:stream.write(monitor)
    failure=A/'service_owned_workflows_20261006/progress_monitor_v28/service_execution.json'
    metadata={'status':'prepared_versioned_GOSS_cost_schema_recovery','original_failed_service':json.loads(failure.read_text(encoding='utf-8-sig')),'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (old,new,path,failure)},'missing_total_elapsed_duration_is_null_not_fabricated_fit_duration':True,'scientific_info_and_models_not_modified':True,'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False}
    with (A/'GOSS_cost_schema_observer30_recovery_20261006.json').open('x',encoding='utf-8') as stream:json.dump(metadata,stream,ensure_ascii=False,indent=2)
    print('prepared_actual_GOSS_duration_schema_recovery_without_modifying_frozen_models',flush=True)


if __name__=='__main__':main()
