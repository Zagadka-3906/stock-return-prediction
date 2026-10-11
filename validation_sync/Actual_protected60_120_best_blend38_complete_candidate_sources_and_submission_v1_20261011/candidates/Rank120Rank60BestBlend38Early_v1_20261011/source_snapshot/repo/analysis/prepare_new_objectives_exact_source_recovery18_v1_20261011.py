from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'new_objectives_exact_source_recovery17_routes_v1_20261011.json';data=read(old)
 assert not Path('E:/赛题五_本机临时/StockRank10Rank20_after175_higher_allocation49_screen_v1_20261011').exists()
 original='run_rank10_rank20_after175_higher_allocation49_screen_v1_20261011.py';p=A/data['source_overrides'][original];q=A/p.name.replace('recovery17_v2','recovery18_v3');assert not q.exists()
 s=p.read_text(encoding='utf8');needle='rank10_rank20_mixed_horizon49_predeclared_plan_v1_20261011.json';assert s.count(needle)==1
 s=s.replace(needle,'rank10_rank20_higher_allocation49_predeclared_sources_admission_v1_20261011.json');compile(s,str(q),'exec');q.write_text(s,encoding='utf8',newline='\n');data['source_overrides'][original]=q.name
 route=A/'route_new_objectives_exact_source_recovery17_v1_20261011.py';newroute=A/route.name.replace('recovery17','recovery18');assert not newroute.exists();s=route.read_text(encoding='utf8').replace('recovery17','recovery18');compile(s,str(newroute),'exec');newroute.write_text(s,encoding='utf8',newline='\n')
 wrappers={};paths=[Path(__file__),old,p,q,route,newroute,A/'rank10_rank20_higher_allocation49_predeclared_sources_admission_v1_20261011.json']
 for driver,name in data['driver_wrappers'].items():
  oldp=A/name;newp=A/name.replace('recovery17','recovery18');assert not newp.exists();s=oldp.read_text(encoding='utf8').replace('recovery17','recovery18');compile(s,str(newp),'exec');newp.write_text(s,encoding='utf8',newline='\n');wrappers[driver]=newp.name;paths.extend([oldp,newp])
 data['driver_wrappers']=wrappers;data['service_aliases']={n:v.replace('recovery17_','recovery18_') for n,v in data['service_aliases'].items()}
 data['input_sha256'].update({str(p):sha(p) for p in paths});data.update(status='compiled_actual49_real_rank10_horizon_and_existing_predeclared_admission_source_before_scoring',prior_failed17_preserved=True,new_fits=0,new_scores=0)
 proof=A/'new_objectives_exact_source_recovery18_routes_v1_20261011.json';create(proof,data)
 for name,driver in data['remaining_tasks']:
  assert allowed();p=A/wrappers[driver];r=start_service(data['service_aliases'][name],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(data['service_aliases'][name]+'_activation.json'),r)
 print({'recovery18_actual_new_workers':len(data['remaining_tasks']),'old_failures_preserved':True,'new_scores':0},flush=True)
if __name__=='__main__':main()
