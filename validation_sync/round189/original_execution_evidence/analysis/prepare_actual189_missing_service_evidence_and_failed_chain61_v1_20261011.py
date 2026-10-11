"""Resume existing verified189 candidate sealing; recover only terminal failed descendants."""
from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
PROOF='actual189_missing_service_evidence_and_failed_chain61_admission_v1_20261011.json'

def save(path,text):
    ast.parse(text);assert not path.exists();path.write_text(text,encoding='utf-8',newline='\n');return path

def main():
    assert allowed()
    prior=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'
    future=A/'actual_future202_206_current60_raw59_admission_v1_20261011.json'
    data=read(prior);newer=read(future)
    ready=read(A/'MixedObjectiveWindow189_selected_release_v1_20261010/inference_ready.json')
    candidate=Path(ready['source_candidate']);assert ready['new_inference_claimed'] and not (candidate/'manifest.json').exists()
    actualprep='recovery58_MixedObjectiveWindow189_selected_candidate_preparation_v1_20261010'
    prepdir=A/'service_owned_workflows_20261006'/actualprep
    assert read(prepdir/'service_execution.json')['status']=='passed' and not owned(read(prepdir/'native_launch.json'))
    oldsealer=A/'seal_MixedObjectiveWindow189_selected_candidate_v3_20261011_actual_preparation_identity38.py'
    text=oldsealer.read_text(encoding='utf-8')
    assert "recovery38_MixedObjectiveWindow189_selected_candidate_preparation_v1_20261010" in text
    text=text.replace('recovery38_MixedObjectiveWindow189_selected_candidate_preparation_v1_20261010',actualprep)
    needle="target=candidate/'source_snapshot/repo'/relative;target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);assert sha(target)==info['sha256']"
    assert text.count(needle)==1
    text=text.replace(needle,"target=candidate/'source_snapshot/repo'/relative;target.parent.mkdir(parents=True,exist_ok=True)\n        if target.exists():assert sha(target)==sha(source)==info['sha256']\n        else:os.link(source,target)\n        assert sha(target)==info['sha256']")
    needle='    for source in evidence:';assert text.count(needle)==1
    text=text.replace(needle,"    evidence += [Path(__file__),A/'"+PROOF+"']\n"+needle)
    sealer=save(A/'seal_MixedObjectiveWindow189_actual_completed_evidence_resume61_v1_20261011.py',text)
    sealname='actual189_completed_inference_missing_evidence_sealing_resume61_v1_20261011'
    resume=save(A/'resume_actual189_complete_family_after_verified_inference61_v1_20261011.py','''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('''+repr(sealname)+''')
 ready=read(A/'MixedObjectiveWindow189_selected_release_v1_20261010/selected_candidate_ready_for_registration.json');assert ready['sealed_candidate_complete']
 driver='run_MixedObjectiveWindow189_full_registration_v3_20261011.py';name='MixedObjectiveWindow189_round189_full_registration_v1_20261010'
 from prepare_MixedObjectiveWindow189_complete149_pipeline_v3_20261011 import source_paths
 pins={str(p):sha(p) for p in source_paths()};assert allowed();start_service(name,driver,[],pins);closed(name)
 receipt=read(A/'github_validation_sync_main_20261005/round189_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==149
 assert read(A/'optimization_20261003_r189/full_registration_execution.json')['status']=='passed'
 from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
 assert allowed();update()
 create(A/'actual189_verified_family_resume61_complete_v1_20261011.json',{'status':'passed_actual149_full_candidate_QA100_main_and_delivery_no_inference_rerun','receipt':receipt,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
if __name__=='__main__':main()
''')
    oldroute=A/'route_future202_206_current60_raw59_v1_20261011.py'
    text=oldroute.read_text(encoding='utf-8').replace("PROOF=A/'actual_future202_206_current60_raw59_admission_v1_20261011.json'","PROOF=A/'"+PROOF+"'")
    needle="'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json']:";assert text.count(needle)==1
    text=text.replace(needle,"'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json','actual_future202_206_current60_raw59_admission_v1_20261011.json']:")
    needle="  source=A/data['actual_source_overrides'].get(name,name)";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n  if name=='run_MixedObjectiveWindow189_complete_family_v3_20261011.py':return raw(str(A/'"+resume.name+"'),run_name='__main__')")
    # Future sealers must bind physical evidence to the same actual service as their closure.
    needle="  if name.startswith('seal_') or '_full_registration_' in name:return raw(str(source),run_name='__main__')";assert text.count(needle)==1
    text=text.replace(needle,"""  if name.startswith('seal_'):
   import re
   text=source.read_text(encoding='utf8')
   def service_binding(match):
    logical=match.group(1);seen=set()
    while logical in data['service_aliases'] and data['service_aliases'][logical]!=logical:
     assert logical not in seen;seen.add(logical);logical=data['service_aliases'][logical]
    return "service=A/'service_owned_workflows_20261006/"+logical+"'"
   text=re.sub(r"service=A/'service_owned_workflows_20261006/([^']+)'",service_binding,text)
   namespace={'__name__':'__main__','__file__':str(source)};exec(compile(text,str(source),'exec'),namespace);return namespace
  if '_full_registration_' in name:return raw(str(source),run_name='__main__')""")
    route=save(A/'route_actual189_evidence_failed_descendants61_v1_20261011.py',text)
    tasks=[];failures=[];aliases=dict(newer['service_alias_updates']);paths=[Path(__file__),prior,future,oldroute,route,oldsealer,sealer,resume,prepdir/'native_launch.json',prepdir/'service_execution.json']
    for name,driver in [*data['tasks'][:-15],*newer['tasks']]:
        folder=A/'service_owned_workflows_20261006'/name
        terminal=folder/'service_execution.json'
        if not terminal.exists() or read(terminal)['status']!='failed':continue
        assert not owned(read(folder/'native_launch.json'))
        new=name.replace('recovery58_','recovery61_',1).replace('recovery60_','recovery61_',1)
        assert new!=name;aliases[name]=new;tasks.append((new,driver));paths.append(terminal);failures.append({'name':name,'terminal':read(terminal)})
    assert tasks and tasks[0][1]=='run_MixedObjectiveWindow189_complete_family_v3_20261011.py'
    aliases['recovery58_MixedObjectiveWindow189_selected_candidate_sealing_v1_20261010']=sealname
    aliases['MixedObjectiveWindow189_round189_full_registration_v1_20261010']='recovery61_MixedObjectiveWindow189_round189_full_registration_v1_20261010'
    drivers=dict(data['driver_wrappers']);wrappers={}
    for driver in drivers:
        p=save(A/(Path(driver).stem+'_actual_evidence61_wrapper.py'),"from route_actual189_evidence_failed_descendants61_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n")
        wrappers[driver]=p.name;paths.append(p)
    create(A/PROOF,{'status':'actual189_completed36_model_inference_sealer_missing_old_service_path_resume_existing_source_links_exact_all_terminal_descendants_recover','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':data['source_factories'],'tasks':tasks,'publication_module_corrections':data['publication_module_corrections'],'actual_family_folder_controls':data['actual_family_folder_controls'],'original_failed_gates':failures,'science_workers_restarted':0,'new_fits_or_scores':0,'test_labels_read':False})
    assert allowed();r=start_service(sealname,sealer.name,[],{str(sealer):sha(sealer),str(A/PROOF):sha(A/PROOF)});create(A/(sealname+'_activation.json'),r)
    for name,driver in tasks:
        assert allowed();p=A/wrappers[driver];r=start_service(name,p.name,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),r)
    print({'189_sealing_resumed_from_completed_inference':True,'terminal_descendants_recovered':len(tasks),'scientific_workers_restarted':0},flush=True)

if __name__=='__main__':main()
