"""Give repaired final receiver independent Git transport and registration directories."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    source=A/'run_ConeRidgeAlpha100_round144_full_registration_v3_20261008.py';text=source.read_text(encoding='utf8')
    changes={'run_ConeRidgeAlpha100_round144_full_registration_v1_file_IO_20261008':'run_ConeRidgeAlpha100_round144_full_registration_v4_file_IO_20261008',
             'ConeRidgeAlpha100_round144_actual_registration_v1_20261008':'ConeRidgeAlpha100_round144_actual_registration_v4_20261008'}
    for before,after in changes.items():assert text.count(before)==1;text=text.replace(before,after)
    target=A/'run_ConeRidgeAlpha100_round144_full_registration_v4_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    previous=A/'service_owned_workflows_20261006/ConeRidgeAlpha100_round144_full_registration_v3_20261008/service_execution.json'
    assert read(previous)['status']=='failed'
    pins={str(p):sha(p) for p in (Path(__file__),source,target,previous)}
    create(A/'ConeRidgeAlpha144_registration_isolation_v4_20261008.json',{
        'status':'frozen_fresh4_Git_and_registration_directories_without_scientific_source_changes',
        'input_sha256':pins,'changes':changes,'six_existing_module_routed_scientific_receivers3_untouched':True,
        'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    name='ConeRidgeAlpha100_round144_full_registration_v4_20261008';row=start(name,target.name,[],pins)
    index=A/'ConeRidgeAlpha144_complete_dependency_plan_v3_20261008.json';jobs=read(index)['jobs']
    services={}
    for old,driver,args in jobs:
        if old=='ConeRidgeAlpha100_round144_full_registration_v3_20261008':services[name]=row
        else:services[old]=read(A/'service_owned_workflows_20261006'/old/'native_launch.json')
    create(A/'ConeRidgeAlpha144_complete_hidden_launches_v4_20261008.json',{
        'status':'started_six_exact_scientific_receivers3_and_isolated_registration4',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'launches':services,'input_sha256':pins,
        'expected_scored_cases':100,'QA_version':55,'actual_quality_scores_by_dispatch':0,
        'existing_actual_current_parent97_controls_service_version':2,
        'historical_native_calendar_completed_and_current_scoring_candidate_main_remaining':True})
    print('Full144 registration4 isolated; scientific six3 and original fitter stay unchanged.',flush=True)
if __name__=='__main__':main()
