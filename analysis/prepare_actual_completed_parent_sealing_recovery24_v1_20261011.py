from pathlib import Path
import sys,subprocess,psutil,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p
def main():
 assert allowed();old=A/'completed_score_parent_chain_recovery21_routes_v1_20261011.json';data=read(old);tasks=data['remaining_tasks'];names={n:n.replace('recovery21_','recovery24_') for n,d in tasks};aliases=data['service_aliases'].copy();aliases.update(names)
 for k,v in list(aliases.items()):
  if v in names:aliases[k]=names[v]
 # Reuse the already passed184 anchor preparation; all other future children get fresh identities.
 passedprep='recovery15_StockPairRankEmbedding184_selected_candidate_preparation_v1_20261010'
 for k,v in list(aliases.items()):
  if ('184' in k or '185' in k or '186' in k or '187' in k or '188' in k or '189' in k or '190' in k or '191' in k) and ('preparation' in k or 'sealing' in k or 'full_registration' in k) and v!=passedprep:aliases[k]='recovery24_'+v.split('_',1)[1] if v.startswith(('recovery15_','recovery16_','recovery19_','recovery21_')) else 'recovery24_'+v
 route=A/'route_completed_score_parent_chain_recovery21_v1_20261011.py';newroute=save(A/route.name.replace('recovery21','recovery24'),route.read_text(encoding='utf8').replace('recovery21','recovery24'));paths=[Path(__file__),old,route,newroute];overrides=data['actual_source_overrides'].copy()
 for factory in data['source_factories']:
  if not any(str(n) in factory for n in range(184,192)):continue
  m=importlib.import_module(factory)
  for filename in m.EXTRAS:
   if not filename.startswith('seal_') or not filename.endswith('.py'):continue
   p=A/filename;s=p.read_text(encoding='utf8');needle="    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)\n    assert read(service/'service_execution.json')['status']=='passed'"
   if needle in s:
    s=s.replace(needle,"    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed\n    closed(service.name)");q=save(A/(p.stem+'_actual_terminal_recovery24.py'),s);overrides[filename]=q.name;paths.extend([p,q])
 original='run_StockPairRankEmbedding184_complete_family_v9_20261010.py';p=A/original;s=p.read_text(encoding='utf8')
 s=s.replace('    preflight()\n',"    proof=read(A/'stock_pairrank_embedding184_full_family_preflight_v3_20261010.json')\n    for path,d in proof['input_sha256'].items():assert sha(path)==d,path\n")
 needle="        assert not logical.exists() and not physical.exists(),logical\n        physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical);empty(logical)";assert s.count(needle)==1
 s=s.replace(needle,"        import os\n        assert physical.is_dir() and logical.is_dir() and os.path.samefile(logical,physical),logical")
 s=s.replace("out=A/'StockPairRankEmbedding184_complete_family_v1_20261010'","out=A/'StockPairRankEmbedding184_complete_family_recovery24_v1_20261011'")
 q=save(A/'run_StockPairRankEmbedding184_completed_anchor_preparation_resume_recovery24_v1_20261011.py',s);overrides[original]=q.name;paths.extend([p,q]);wrappers={}
 for d,name in data['driver_wrappers'].items():
  oldp=A/name;newp=save(A/name.replace('recovery21','recovery24'),oldp.read_text(encoding='utf8').replace('recovery21','recovery24'));wrappers[d]=newp.name;paths.extend([oldp,newp])
 audit=[]
 for n in [*[n for n,d in tasks],'recovery15_StockPairRankEmbedding184_selected_candidate_sealing_v1_20261010']:
  f=A/'service_owned_workflows_20261006'/n;row=read(f/'native_launch.json');stack=None
  if owned(row):
   p=psutil.Process(row['owned_worker_pid']);assert not p.children(),n;stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout
   assert 'closed (' in stack or ('seal_StockPairRankEmbedding184_selected_candidate_v5_20261010.py:13' in stack),n
   retire(row,'Resolve exact idle legacy canonical sealer barrier to real aliased completed preparation, preserve184 existing anchor preparation and all scientific caches')
  else:assert not (f/'service_execution.json').exists() or read(f/'service_execution.json')['status']=='failed',n
  audit.append({'identity':row,'actual_idle_stack':stack})
 data.update(status='compiled_actual_alias_aware_terminal_sealers_and184_completed_anchor_resume',service_aliases=aliases,driver_wrappers=wrappers,actual_source_overrides=overrides,remaining_tasks=[(names[n],d) for n,d in tasks],preserved_prior_idle21_helpers=audit,new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'completed_score_parent_chain_recovery24_routes_v1_20261011.json';create(proof,data)
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(names[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(names[n]+'_activation.json'),r)
 print({'actual_recovery24_parent_chain_workers':len(tasks),'completed184_anchor_preparation_reused':True,'new_fits':0,'new_scores':0},flush=True)
if __name__=='__main__':main()
