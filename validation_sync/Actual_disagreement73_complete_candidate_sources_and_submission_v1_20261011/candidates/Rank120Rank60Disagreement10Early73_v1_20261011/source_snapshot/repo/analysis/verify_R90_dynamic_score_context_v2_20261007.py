"""Two full actual schemes: original scoring versus Windows-owned reset-safe score hooks."""
from pathlib import Path
import sys
import gc
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    import numpy as np
    import psutil
    import optimize_training_round90_v3 as module
    import parallel_candidate_scoring_one_20261005 as scoring
    import classifier_consensus_recovery_official_speed_adapter_v2_20261007 as speed
    from hidden_windows_child_creation_20261006 import install as hidden
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'R90_dynamic_score_context_v2_preflight_20261007';assert not out.exists();out.mkdir()
    prior=A/'service_owned_workflows_20261006/classifier_consensus_R90_root_resolution_recovery'
    assert not owned(read(prior/'native_launch.json')) and read(prior/'service_execution.json')['status']=='failed'
    while psutil.virtual_memory().available<10*2**30:time.sleep(15)
    proto=A/'optimization_20261003_r90/protocol.json'
    sources=[Path(__file__),A/'classifier_consensus_recovery_official_speed_adapter_v2_20261007.py',A/'classifier_consensus_recovery_official_speed_adapter_20261007.py',A/'official_date_index_dataframe_adapter_20261007.py',A/'optimization_20261003_r90/component_audit.json',proto,ROOT/'后续选模标准.md']
    pins={**read(proto)['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
    create(out/'frozen_before_actual_control.json',{'input_sha256':pins,'actual_rows':5635800,'actual_days':1212,'schemes':['baseline89','first_standalone90'],'old_context_reset_error_reproduced_from_failed_actual_scope':True,'new_fits':0,'new_selection_scores':0,'test_labels_read':False})
    original_args=sys.argv;restore_hidden=hidden();restore_speed=None
    try:
        with LockedReadHashCache(pins) as held:
            configs=[module.baseline(),module.standalone_cfg(module.MODELS[0])]
            ctx=module.Context(scoring=out/'original_reference_scores')
            references=[]
            for cfg in configs:
                references.append(module.evaluate(ctx,cfg))
            del ctx;gc.collect()
            restore_speed=speed.install()
            rows=list(scoring.evaluate_many(module.__name__,[(str(i),cfg) for i,cfg in enumerate(configs)],out/'actual_windows_worker'))
            assert len(rows)==2
            controls=[]
            for index,(key,row) in enumerate(rows):
                reference=references[index]
                assert key==str(index)
                assert set(row['metrics'])==set(reference['metrics']) and len(row['metrics'])==8
                for name,value in reference['metrics'].items():
                    assert np.asarray(value,dtype=np.float64).view('u8')==np.asarray(row['metrics'][name],dtype=np.float64).view('u8'),name
                events=row['actual_original_official_date_index_execution']
                assert events['date_index_lookups'] in (0,1212)
                assert row['exact_daily_rank_execution']['installed_in_actual_scoring_worker']
                controls.append({'scheme':index,'all8_original_metric_uint64_bits_exact':True,'actual_date_index':events,'actual_reset_safe_hook_present_after_native_worker_configuration':True,'original':reference,'actual':row})
            scoring.shutdown(module.__name__);restore_speed();restore_speed=None
            held.reverify();create(out/'verification.json',{'status':'passed_actual_two_full5635800_scheme_original8_metric_bits_and_Windows_reset_safe_score_hooks','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'controls':controls,'actual_original_reference_scheme_evaluations':2,'actual_windows_scheme_evaluations':2,'new_fits':0,'new_selection_score_records':0,'full138_recovery_not_claimed':True,'test_labels_read':False})
    finally:
        scoring.shutdown(module.__name__)
        if restore_speed is not None:restore_speed()
        sys.argv=original_args;create(out/'actual_hidden_diagnostic_children.json',{'events':restore_hidden()})
if __name__=='__main__':main()
