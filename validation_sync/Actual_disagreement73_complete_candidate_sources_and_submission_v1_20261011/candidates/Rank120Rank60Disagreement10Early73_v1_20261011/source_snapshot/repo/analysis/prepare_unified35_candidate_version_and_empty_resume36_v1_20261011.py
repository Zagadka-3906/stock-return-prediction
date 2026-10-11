from pathlib import Path
import sys,importlib,re,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p
def main():
 assert allowed();old=A/'unified_completed_parent_shared_publication35_routes_v1_20261011.json';data=read(old);tasks=data['remaining_tasks'][1:];names={n:n.replace('recovery35_','recovery36_') for n,d in tasks};aliases=data['service_aliases'].copy();overrides=data['actual_source_overrides'].copy();paths=[Path(__file__),old]
 for n,d in tasks:
  f=A/'service_owned_workflows_20261006'/n;assert read(f/'service_execution.json')['status']=='failed' and not owned(read(f/'native_launch.json')),n
 for k,v in list(aliases.items()):
  if v in names:aliases[k]=names[v]
  elif v.startswith('recovery35_') and any(t in v for t in ('preparation','sealing','full_registration')):aliases[k]=v.replace('recovery35_','recovery36_')
 aliases.update(names)
 for d,filename in list(overrides.items()):
  if not d.startswith('seal_'):continue
  p=A/filename;s=p.read_text(encoding='utf8');s=s.replace("service=A/'service_owned_workflows_20261006/recovery35_","service=A/'service_owned_workflows_20261006/recovery36_");q=save(A/(Path(d).stem+'_actual_sealer_identity_recovery36.py'),s);overrides[d]=q.name;paths.extend([p,q])
 f=importlib.import_module('prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010')
 cache=A/f.EXTRAS[8];s=cache.read_text(encoding='utf8').replace('selected_feature_cache_runtime_v5','selected_feature_cache_runtime_recovery36_v1');q=save(A/(cache.stem+'_exclusive_cache_resume36.py'),s);overrides[cache.name]=q.name;paths.extend([cache,q])
 preflight=A/f.EXTRAS[7];s=preflight.read_text(encoding='utf8').replace('stock_toppair_embedding185_full_family_preflight_v3_20261010.json','stock_toppair_embedding185_full_family_preflight_actual36_20261011.json');q=save(A/(preflight.stem+'_actual36.py'),s);overrides[preflight.name]=q.name;paths.extend([preflight,q])
 family=A/f.EXTRAS[5];s=family.read_text(encoding='utf8');start=s.index('    for logical,physical in OUTPUTS.items():');end=s.index('    from prepare_StockTopPairEmbedding185_complete48_pipeline_',start)
 s=s[:start]+"    for logical,physical in OUTPUTS.items():\n        assert logical.is_junction() and logical.resolve()==physical.resolve()\n        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第185轮_20261010'))\n        empty(logical)\n"+s[end:]
 s=s.replace("out=A/'StockTopPairEmbedding185_complete_family_v1_20261010'","out=A/'StockTopPairEmbedding185_complete_family_actual_recovery36_v1_20261011'").replace("A/'stock_toppair_embedding185_full_family_preflight_v3_20261010.json'","A/'stock_toppair_embedding185_full_family_preflight_actual36_20261011.json'")
 q=save(A/(family.stem+'_verified_empty_output_resume36.py'),s);overrides[family.name]=q.name;paths.extend([family,q])
 storage=importlib.import_module('stock_toppair_embedding185_storage_v3_20261010')
 for logical,physical in storage.OUTPUTS.items():assert logical.is_junction() and logical.resolve()==physical.resolve();storage.empty(logical)
 catalog={};sourcefiles=set()
 for fn in data['source_factories']:
  m=importlib.import_module(fn)
  for name in m.NAMES+m.EXTRAS:
   p=A/name
   if p.suffix=='.py' and p.exists():sourcefiles.add(p);catalog.setdefault(re.sub(r'_v\d+_202\d{5}$','',p.stem),set()).add(p.stem)
 module_aliases={};audit=[]
 for p in sourcefiles:
  for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
   if not isinstance(node,ast.ImportFrom) or not node.module or not re.search(r'_v\d+_202\d{5}$',node.module):continue
   choices=catalog.get(re.sub(r'_v\d+_202\d{5}$','',node.module),set())
   if len(choices)==1:
    target=next(iter(choices))
    if target!=node.module:
     actual=Path(overrides.get(target+'.py',target+'.py')).stem;module_aliases[node.module]=actual;audit.append({'caller':p.name,'old_import':node.module,'actual_factory_module':target,'actual_executed_module':actual,'original_old_module_exists':(A/(node.module+'.py')).is_file()})
   elif not (A/(node.module+'.py')).exists():raise AssertionError(('Missing module without a unique actual factory version',p.name,node.module,choices))
 route=A/'route_unified_completed_parent_shared_publication35_v1_20261011.py';s=route.read_text(encoding='utf8').replace('unified_completed_parent_shared_publication35_routes_v1_20261011.json','unified_completed_parent_shared_publication36_routes_v1_20261011.json')
 needle="        if level==0 and name=='normalize_completed_stock_toppair_embedding_complete48_after184_v6_20261010':";assert needle in s;s=s.replace(needle,"        if level==0 and name in data['module_aliases']:\n            return previous_import(data['module_aliases'][name],globals,locals,fromlist,level)\n"+needle)
 newroute=save(A/'route_unified_completed_parent_shared_publication36_v1_20261011.py',s);paths.extend([route,newroute]);wrappers={}
 for d,filename in data['driver_wrappers'].items():
  p=A/filename;q=save(A/filename.replace('publication35','publication36'),p.read_text(encoding='utf8').replace('publication35','publication36'));wrappers[d]=q.name;paths.extend([p,q])
 data.update(status='compiled_unified36_actual_factory_version_imports_and_verified_empty185_resume_with_shared_publication35',service_aliases=aliases,actual_source_overrides=overrides,module_aliases=module_aliases,actual_factory_version_import_audit=audit,driver_wrappers=wrappers,remaining_tasks=[(names[n],d) for n,d in tasks],passed35_toppair_selected14_reused=True,new_fits=0,new_scores=0)
 data['input_sha256'].update({str(p):sha(p) for p in paths});proof=A/'unified_completed_parent_shared_publication36_routes_v1_20261011.json';create(proof,data)
 for n,d in tasks:
  assert allowed();p=A/wrappers[d];r=start_service(names[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(names[n]+'_activation.json'),r)
 print({'actual_unified36_remaining_workers':len(tasks),'actual_factory_version_import_controls':len(audit),'new_fits_or_scores':0},flush=True)
if __name__=='__main__':main()
