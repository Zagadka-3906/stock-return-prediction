"""Reuse all actual67/native14 results and verified empty E outputs after a helper name collision."""
from pathlib import Path
from datetime import datetime
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_Return_protected_pilot67_and_selected_native14_v1_20261010 import allowed,closed
OUT=A/'Return167_actual_native14_recovery_v3_20261010'
def main():
    assert allowed();OUT.mkdir(exist_ok=False)
    old=A/'service_owned_workflows_20261006/ReturnProtected167_complete67_family_admitted_v2_20261010'
    assert not owned(read(old/'native_launch.json')) and read(old/'service_execution.json')['failure']=="TypeError: 'str' object is not callable"
    native=A/'service_owned_workflows_20261006/ReturnProtected167_selected_native14_v1_20261010'
    assert not owned(read(native/'native_launch.json')) and read(native/'service_execution.json')['status']=='passed'
    folder=Path(read(A/'actual_protected_Return_selected_native14_location_v1_20261010.json')['output'])
    proof=read(folder/'verification.json');assert proof['actual_saved_states']==6 and proof['actual_cold_cases']==14 and len(proof['prefit_rejections'])==7
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    from protected167_storage_v2_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():
        assert logical.resolve()==physical.resolve() and physical.resolve().is_relative_to(Path('E:/赛题五_本机临时/第167轮_20261010').resolve())
        empty(logical)
    assert not (A/'service_owned_workflows_20261006/ReturnProtected167_selected_candidate_preparation_v1_20261010').exists()
    import prepare_protected167_full_registry_sources_v1_20261010 as routes
    original_source_paths=routes.source_paths
    extras=[Path(__file__),A/'run_Return167_full_registration_admitted_v3_20261010.py',A/'prepare_protected167_selected_candidate_v3_20261010.py',A/'predict_protected_Return_after163_complete_scheme_v4_20261010.py',A/'protected167_full_family_preflight_v1_20261010.json',A/'Return167_actual_parent163_source_and_callback_controls_v2_20261010.json']
    routes.source_paths=lambda original_source_paths=original_source_paths:list(dict.fromkeys([*original_source_paths(),*extras]))
    # Actual callable route inspection avoids the original loop-variable capture.
    sources=routes.source_paths();assert all(p.is_file() for p in sources)
    pins={str(p):sha(p) for p in [*sources,folder/'verification.json',folder/'pilot67.json']}
    create(OUT/'frozen_before_reused_native14_future_dispatch.json',{'input_sha256':pins,'at_local':datetime.now().isoformat(),'preserved_failure':read(old/'service_execution.json'),'actual_native14_reused':True,'all5_existing_output_junctions_exact_and_empty':True,'new_model_training_or_scores_or_native14_by_recovery':0})
    for name,driver in [('ReturnProtected167_selected_candidate_preparation_v1_20261010','prepare_protected167_selected_candidate_v3_20261010.py'),('ReturnProtected167_selected_candidate_sealing_v1_20261010','seal_protected167_selected_candidate_v2_20261010.py'),('ReturnProtected167_round167_full_registration_v1_20261010','run_Return167_full_registration_admitted_v3_20261010.py')]:
        assert allowed();row=start_service(name,driver,[],pins);create(OUT/(name+'_launch.json'),row);closed(name)
    assert read(A/'optimization_20261003_r167/full_registration_execution.json')['status']=='passed'
    create(OUT/'verification.json',{'status':'passed_actual67_selected_native14_reuse_full_candidate_QA78_and_main','new_quality_scores_by_recovery':0,'test_labels_read':False})
if __name__=='__main__':main()
