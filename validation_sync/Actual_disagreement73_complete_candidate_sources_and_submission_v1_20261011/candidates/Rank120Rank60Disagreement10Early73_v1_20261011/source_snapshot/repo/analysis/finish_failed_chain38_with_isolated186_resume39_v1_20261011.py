from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'run_StockRank20Seed10Embedding186_registered_QA_main_resume38_v1_20261011.py'
 f=A/'service_owned_workflows_20261006/actual186_registered_QA_main_resume38_v1_20261011';assert read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json'))
 s=old.read_text(encoding='utf8').replace('resume38','resume39').replace('frozen_external_capsule_publication_guard_v3.json','frozen_external_capsule_publication_guard_resume39_v3.json').replace('late_snapshot_encoder_import.json','late_snapshot_encoder_import_resume39.json')
 p=A/'run_StockRank20Seed10Embedding186_registered_QA_main_resume39_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
 proof38=A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json';d=read(proof38)
 tasks=[('actual186_registered_QA_main_resume39_v1_20261011',p.name),*d['tasks'][1:]];wrappers={}
 route=A/'route_canonical_publication_resume186_isolated39_v1_20261011.py'
 for name,driver in tasks:
  q=A/(Path(driver).stem+'_isolated186_resume39_wrapper.py');text="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_canonical_publication_resume186_isolated39_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n";ast.parse(text);assert not q.exists();q.write_text(text,encoding='utf8');wrappers[driver]=q
 proof=A/'canonical_publication_resume186_isolated39_admission_v1_20261011.json'
 create(proof,{'status':'resume39_isolated_exclusive_logs_after_pre_main_guard_FileExists_failure','input_sha256':{str(q):sha(q) for q in [Path(__file__),old,p,proof38,route,*wrappers.values()]},'preserved_failure':read(f/'service_execution.json'),'tasks':tasks,'actual186_resume38_alias':'actual186_registered_QA_main_resume39_v1_20261011','new_fits_or_scores':0,'existing186_registration_not_rerun':True})
 count=0
 for name,driver in tasks:
  folder=A/'service_owned_workflows_20261006'/name
  if folder.exists():
   assert (folder/'native_launch.json').exists() and owned(read(folder/'native_launch.json')),name;continue
  assert allowed();q=wrappers[driver];r=start_service(name,q.name,[],{str(q):sha(q),str(proof):sha(proof)});create(A/(name+'_activation.json'),r);count+=1
 print({'actual38_chain_and186_resume39_started':count,'no_refit_or_rescore':True},flush=True)
if __name__=='__main__':main()
