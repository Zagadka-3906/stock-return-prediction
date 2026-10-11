"""Qualify actual recent-window winner then infer, seal, register132, QA81, main and delivery."""
from pathlib import Path
import sys,time,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
from run_protected167_complete_family_v1_20261010 import junction

def main():
    assert allowed()
    closed('Cross120170_selected_native14_v3_20261010')
    closed('actual_shared_string_pack_full167_benchmark_v1_20261010')
    from verify_Cross120170_full132_preflight_v4_20261010 import main as preflight
    preflight()
    from cross120170_storage_v1_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():
        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第170轮_20261010'))
        assert not logical.exists() and not physical.exists(),logical
        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical);empty(logical)
    from prepare_cross120170_full_registry_sources_v1_20261010 import source_paths
    extra=[Path(__file__),A/'prepare_cross120170_full_registry_sources_v1_20261010.py',A/'prepare_cross120170_selected_candidate_v4_20261010.py',A/'run_Cross120170_full_registration_v4_20261010.py',A/'verify_Cross120170_full132_preflight_v4_20261010.py',A/'cross120170_full_family_preflight_v4_20261010.json',A/'cross120170_candidate_actual132_and_own_source_routes_preflight_v2_20261010.json']
    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}
    out=A/'Cross120170_complete_family_v1_20261010';out.mkdir(exist_ok=False)
    create(out/'frozen_before_selected_future_dispatch.json',{'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'quality_cases':132,'actual_future_X_read':False,'new_native_fits':0,'test_labels_read':False})
    for name,driver in [('Cross120170_selected_candidate_preparation_v1_20261010','prepare_cross120170_selected_candidate_v4_20261010.py'),('Cross120170_selected_candidate_sealing_v1_20261010','seal_cross120170_selected_candidate_v1_20261010.py'),('Cross120170_round170_full_registration_v1_20261010','run_Cross120170_full_registration_v4_20261010.py')]:
        assert allowed();row=start_service(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round170_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==132
    assert read(A/'optimization_20261003_r170/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(out/'passed.json',{'status':'passed_actual132_complete_selected_native_candidate_or_exact_qualified_anchor_QA81_main_and_delivery','actual_new_selected_inference':read(A/'Cross120170_selected_release_v1_20261010/selected_candidate_ready_for_registration.json')['new_inference_claimed'],'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'receipt':receipt,'actual_scored_records':132,'new_quality_scores_by_registration':0,'test_labels_read':False})
if __name__=='__main__':main()
