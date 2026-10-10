"""Qualify actual recent-window winner then infer, seal, register67, QA79, main and delivery."""
from pathlib import Path
import sys,time,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
from run_protected167_complete_family_v1_20261010 import junction

def main():
    assert allowed()
    closed('RecentReturn252_after167_selected_native14_v1_20261010')
    closed('actual_shared_string_pack_full167_benchmark_v1_20261010')
    from verify_RecentReturn252Protected168_full67_preflight_v1_20261010 import main as preflight
    preflight()
    from protected168_storage_v2_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():
        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第168轮_20261010'))
        assert not logical.exists() and not physical.exists(),logical
        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical);empty(logical)
    from prepare_protected168_full_registry_sources_v1_20261010 import source_paths
    extra=[Path(__file__),A/'prepare_protected168_full_registry_sources_v1_20261010.py',A/'prepare_protected168_selected_candidate_v4_20261010.py',A/'run_RecentReturn252Protected168_full_registration_v1_20261010.py',A/'verify_RecentReturn252Protected168_full67_preflight_v1_20261010.py',A/'protected168_full_family_preflight_v1_20261010.json',A/'RecentReturn252Protected168_actual_own_bank_pointer_correction_v1_20261010.json']
    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}
    out=A/'RecentReturn252Protected168_complete_family_v1_20261010';out.mkdir(exist_ok=False)
    create(out/'frozen_before_selected_future_dispatch.json',{'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'quality_cases':67,'actual_future_X_read':False,'new_native_fits':0,'test_labels_read':False})
    for name,driver in [('RecentReturn252Protected168_selected_candidate_preparation_v1_20261010','prepare_protected168_selected_candidate_v4_20261010.py'),('RecentReturn252Protected168_selected_candidate_sealing_v1_20261010','seal_protected168_selected_candidate_v2_20261010.py'),('RecentReturn252Protected168_round168_full_registration_v1_20261010','run_RecentReturn252Protected168_full_registration_v1_20261010.py')]:
        assert allowed();row=start_service(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round168_receipt.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==67
    assert read(A/'optimization_20261003_r168/full_registration_execution.json')['status']=='passed'
    assert allowed()
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(out/'passed.json',{'status':'passed_actual67_full_candidate_graph_freeze_two_full1599600_native_replays_cold80_QA79_main_and_delivery','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'receipt':receipt,'actual_scored_records':67,'new_quality_scores_by_registration':0,'test_labels_read':False})
if __name__=='__main__':main()
