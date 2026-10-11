"""Sequentially infer, seal, and register the selected real protected76 candidate."""
from pathlib import Path
import sys,time,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_Return_protected_pilot67_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service

def junction(logical,physical):
    quote=lambda value:"'"+str(value).replace("'","''")+"'"
    command='New-Item -ItemType Junction -Path '+quote(logical)+' -Target '+quote(physical)+' | Out-Null'
    subprocess.run(['powershell','-NoProfile','-NonInteractive','-Command',command],check=True,creationflags=subprocess.CREATE_NO_WINDOW,stdin=subprocess.DEVNULL)

def main():
    assert allowed();closed('ReusedNN166Quality19_round166_full_registration_v1_20261009')
    driver=A/'prepare_Return_protected_pilot67_and_selected_native14_v1_20261010.py'
    row=start_service('ReturnProtected167_selected_native14_v1_20261010',driver.name,[],{str(driver):sha(driver),str(A/'protected_Return_after163_native_stage_v3_20261010.py'):sha(A/'protected_Return_after163_native_stage_v3_20261010.py')})
    closed('ReturnProtected167_selected_native14_v1_20261010')
    from protected167_storage_v2_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():
        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第167轮_20261010'))
        assert not logical.exists() and not physical.exists(),logical
        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True)
        junction(logical,physical)
        empty(logical)
    from prepare_protected167_full_registry_sources_v1_20261010 import source_paths
    pins={str(p):sha(p) for p in source_paths()}
    native_folder=Path(read(A/'actual_protected_Return_selected_native14_location_v1_20261010.json')['output'])
    pins.update({str(p):sha(p) for p in [native_folder/'verification.json',native_folder/'pilot67.json']})
    out=A/'protected167_complete_family_v1_20261010';out.mkdir(exist_ok=False)
    create(out/'frozen_before_selected_future_dispatch.json',{'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'quality_cases':67,'actual_future_X_read':False,'new_native_fits':0,'test_labels_read':False})
    for name,driver in [('ReturnProtected167_selected_candidate_preparation_v1_20261010','prepare_protected167_selected_candidate_v2_20261010.py'),('ReturnProtected167_selected_candidate_sealing_v1_20261010','seal_protected167_selected_candidate_v2_20261010.py'),('ReturnProtected167_round167_full_registration_v1_20261010','run_protected167_full_registration_v1_20261010.py')]:
        assert allowed()
        row=start_service(name,driver,[],pins);create(out/(name+'_launch.json'),row);closed(name)
    assert read(A/'optimization_20261003_r167/full_registration_execution.json')['status']=='passed'
    # Administrative predecessor compatibility only; the actual contract remains76.
    actual=A/'service_owned_workflows_20261006/ReturnProtected167_round167_full_registration_v1_20261010'
    alias=A/'service_owned_workflows_20261006/ReusedNN167Quality19_round167_full_registration_v1_20261009'
    assert not alias.exists() and read(actual/'service_execution.json')['status']=='passed'
    junction(alias,actual)
    assert alias.resolve()==actual.resolve()
    create(out/'passed.json',{'status':'passed_actual67_candidate_full_graph_freeze_native_inference_cold80_QA78_and_main','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_full_service':str(actual),'legacy19_name_is_only_a_dispatch_compatibility_alias':str(alias),'actual_scored_records':67,'new_quality_scores_by_registration':0,'test_labels_read':False})

if __name__=='__main__':main()
