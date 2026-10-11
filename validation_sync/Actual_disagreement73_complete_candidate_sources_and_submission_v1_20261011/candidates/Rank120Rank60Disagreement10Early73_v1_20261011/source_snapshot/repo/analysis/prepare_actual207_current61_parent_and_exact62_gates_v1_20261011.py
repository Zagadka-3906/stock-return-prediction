"""Correct207 future service names and bind the restored206 parent; no science rerun."""
from pathlib import Path
import sys,ast,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_Rank120Rank60BestBlend207_complete40_pipeline_v1_20261011 as factory
PROOF='actual207_current61_parent_exact62_gates_admission_v1_20261011.json'

def main():
 assert allowed()
 prior=A/'actual189_missing_service_evidence_and_failed_chain61_admission_v1_20261011.json';data=read(prior)
 oldnames=['actual_rank120_rank60_bestblend40_after206_normalization_v1_20261011','actual_rank120_rank60_bestblend40_selected_native14_v1_20261011','Rank120Rank60BestBlend203_complete40_family_v1_20261011']
 newnames=['recovery62_actual_rank120_rank60_bestblend40_after206_normalization_v1_20261011','recovery62_actual_rank120_rank60_bestblend40_selected_native14_v1_20261011','recovery62_Rank120Rank60BestBlend207_complete40_family_v1_20261011']
 old=[];paths=[Path(__file__),prior,A/factory.PROOF,*factory.source_paths()]
 for index,name in enumerate(oldnames):
  folder=A/'service_owned_workflows_20261006'/name;identity=read(folder/'native_launch.json')
  if index==0:
   assert read(folder/'service_execution.json')['status']=='failed' and not owned(identity);paths.append(folder/'service_execution.json');dump=None
  else:
   assert owned(identity) and not (folder/'service_execution.json').exists()
   dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(identity['owned_worker_pid'])],capture_output=True,text=True,encoding='utf-8',check=True).stdout
   assert '(idle)' in dump and 'closed (' in dump and not psutil.Process(identity['owned_worker_pid']).children(recursive=True)
  old.append({'name':name,'identity':identity,'actual_idle_stack':dump})
 assert not Path('E:/赛题五_本机临时/rank120_rank60_bestblend_complete40_after206_v1_20261011').exists()
 assert not Path('E:/赛题五_本机临时/rank120_rank60_bestblend51_selected_native14_v1_20261011').exists()
 aliases=dict(data['service_alias_updates']);aliases.update(zip(oldnames,newnames))
 aliases['actual_rank120_rank60_bestblend51_after206_normalization_v1_20261011']=newnames[0]
 aliases['actual_rank120_rank60_bestblend51_selected_native14_v1_20261011']=newnames[1]
 aliases['Rank120Rank60BestBlend207_complete40_family_v1_20261011']=newnames[2]
 route=A/'route_actual207_current61_parent_exact62_gates_v1_20261011.py'
 text=(A/'route_actual189_evidence_failed_descendants61_v1_20261011.py').read_text(encoding='utf-8')
 text=text.replace("PROOF=A/'"+prior.name+"'","PROOF=A/'"+PROOF+"'")
 needle="'actual_future202_206_current60_raw59_admission_v1_20261011.json']:";assert text.count(needle)==1
 text=text.replace(needle,"'actual_future202_206_current60_raw59_admission_v1_20261011.json','"+prior.name+"']:")
 ast.parse(text);assert not route.exists();route.write_text(text,encoding='utf-8',newline='\n');paths.append(route)
 wrappers=dict(data['driver_wrappers'])
 for name in dict.fromkeys([*factory.NAMES,*[n for n in factory.EXTRAS if n.endswith('.py')]]):
  p=A/(Path(name).stem+'_exact62_future207_wrapper.py')
  text="from route_actual207_current61_parent_exact62_gates_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(name)+")\n";ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf-8',newline='\n');paths.append(p);wrappers[name]=p.name
 sourcefactories=list(dict.fromkeys([*data['source_factories'],factory.FACTORY]))
 tasks=list(zip(newnames,[factory.EXTRAS[0],factory.EXTRAS[1],factory.EXTRAS[5]]))
 create(A/PROOF,{'status':'actual207_current61_parent_and_exact40_service_gates_original51_named_modules_preserved_no_prior207_science','input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'service_alias_updates':aliases,'driver_wrappers':wrappers,'source_factories':sourcefactories,'tasks':tasks,'publication_module_corrections':data['publication_module_corrections'],'actual_family_folder_controls':data['actual_family_folder_controls'],'original_terminal_or_actual_idle_services':old,'expected_records':40,'expected_full_controls':37,'expected_prefix_controls':111,'expected_board':18412,'expected_QA':118,'scientific_workers_restarted':0,'new_fits_or_scores':0,'test_labels_read':False})
 for row in old[1:]:
  identity=row['identity'];assert owned(identity);p=psutil.Process(identity['owned_worker_pid']);assert not p.children(recursive=True);p.terminate()
 for name,driver in tasks:
  assert allowed();p=A/wrappers[driver];identity=start_service(name,p.name,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),identity)
 print({'207_actual_dependency_names_recovered':3,'actual_207_new_scores_or_inference_claimed':False,'scientific_workers_restarted':0},flush=True)

if __name__=='__main__':main()
