"""Run the new CPU kernel bank after actual scientific and capacity controls finish."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    scientific=ROOT/'results/optimization_20261003_r60.json'
    gates=[ROOT/'analysis/optimization_20261003_r60/provenance_scope_execution.json',
        ROOT/'analysis/neural_width_frontier_scope_audit_20261004.json',
        ROOT/'analysis/official_worker_frontier_scope_audit_20261004.json',
        ROOT/'analysis/nystrom_ridge_preflight_20261004/verification.json',
        ROOT/'analysis/nystrom_ridge_search_generator_preflight_20261004/verification.json',
        ROOT/'analysis/nystrom_ridge_frozen_provenance_preflight_20261004/verification.json']
    observer=ROOT/'analysis/nystrom_ridge_resource_observations_recovery_20261005/protocol.json'
    plan=ROOT/'analysis/nystrom_ridge_complete_output_search_plan_20261004.json'
    while True:
        try:values=[read(p) for p in [scientific,*gates,observer,plan]]
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        assert values[0]['status']=='complete'
        assert all(v['status']=='passed' for v in values[1:1+len(gates)])
        assert values[-2]['status']=='sampling_started';break
    import train_nystrom_ridge_bank_20261004 as bank
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    from locked_read_hash_cache_20261004 import fresh_sha
    correction=read(ROOT/'analysis/nystrom_ridge_complete_scheme_source_correction_audit_20261004.json')
    assert correction['status']=='passed_pre_execution_source_correction_audit'
    assert fresh_sha(Path(correction['effective_source']))==correction['effective_source_sha256']
    assert fresh_sha(Path(correction['original_source_preserved']))==correction['original_source_sha256']
    sources=[Path(__file__),ROOT/'analysis/run_nystrom_ridge_training_20261004.py',ROOT/'analysis/nystrom_restart_source_audit_20261005.json',ROOT/'analysis/nystrom_ridge_resource_observations_recovery_20261005/recovery_binding.json',ROOT/'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT/'analysis/locked_read_hash_cache_20261004.py',scientific,*gates,observer,plan,
        ROOT/'analysis/observe_nystrom_restart_resources_20261005.py',
        ROOT/'analysis/nystrom_ridge_complete_scheme_source_correction_audit_20261004.json',
        ROOT/'analysis/nystrom_ridge_training_run_20261005.json']
    metadata={'script':str(Path(__file__).resolve()),'driver_source_sha256':fresh_sha(Path(__file__)),
        'delegate':'train_nystrom_ridge_bank_20261004.all_oof',
        'all_declared_kernel_training_configurations_unchanged':True,
        'actual_scientific_andGPU_andCPU_capacity_scope_audits_required':True,
        'landmarks_preprocessing_andtargets_fitted_onmature_past_rows_only':True}
    scope=FrozenProvenanceExecutionScope(bank,sources,metadata,ROOT/'analysis').install();failure=None
    try:bank.all_oof()
    except BaseException as error:failure=f'{type(error).__name__}: {error}';raise
    finally:
        report=scope.close(failed=failure is not None);bank.OUT.mkdir(exist_ok=True)
        with (bank.OUT/'training_execution_scope.json').open('x',encoding='utf-8') as stream:
            json.dump({'status':'passed' if failure is None else 'failed','failure':failure,
                'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),**report,
                'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)

if __name__=='__main__':main()
