"""Execute the entire148 native route, then the frozen sparse stage before return mapping."""
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy
import os

PARENT_FILENAME='predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008.py'
def prepared_parent148(text):
 needle='        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value'
 assert text.count(needle)==1
 return text.replace(needle,'        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return SPARSE_AFTER_COMPLETE148(context,value,teacher)')

def predict(ns,record,candidate,parent_curve_source,mapping_path):
 from SparseAfter148_complete_parent_native_stage_v1_20261009 import after_parent,GRAPH_KEY
 graph=record['winner'][ns.GRAPH_FIELD]
 assert 'nonflag_CPU_joint_Cross_Huber_adaptive_complete_parent_CDF' in graph
 spec=deepcopy(graph[GRAPH_KEY]);assert spec['original_complete_parent_round']==148
 components=deepcopy(spec['ordered_native_components'])
 candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
 for component in components:
  assert component['state_kind']=='SparseGram64_linear'
  for src,dst,digest,suffix in (
   ('source_path','path','sha256','.joblib'),
   ('independent_state_source_path','independent_state_path','independent_state_sha256','.json')):
   source=Path(component[src]);target=candidate/(component['name']+suffix)
   assert ns.sha(source)==component[digest]
   if not target.exists():
    if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
    else:
     import shutil
     with source.open('rb') as reader,target.open('xb') as writer:shutil.copyfileobj(reader,writer,1024**2)
   assert ns.sha(target)==component[digest];component[dst]=str(target)
 calls=[]
 def sparse_stage(context,parent,teacher):
  value,report=after_parent(ns,context,teacher,parent,spec,components)
  calls.append(report);return value
 final=candidate/'verification.json';intermediate=candidate/'complete148_route_before_SparseAfter148_report.json'
 read,dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
 proxy.read=lambda path:read(intermediate if Path(path).resolve()==final.resolve() else path)
 def routed_dump(path,value,*args,**kwargs):return dump(intermediate if Path(path).resolve()==final.resolve() else path,value,*args,**kwargs)
 proxy.dump=routed_dump
 source=ns.ROOT/'analysis'/PARENT_FILENAME
 namespace={'__file__':str(source),'__name__':'actual_complete148_then_sparse',
  'SPARSE_AFTER_COMPLETE148':sparse_stage}
 exec(compile(prepared_parent148(source.read_text(encoding='utf8')),str(source),'exec'),namespace)
 result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
 full=[r for r in calls if r['rows']==1599600];cold=[r for r in calls if r['rows']==80*4650]
 assert len(full)>=2 and len(cold)>=1
 assert all(r['native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact'] for r in calls)
 before=len(result['models']);new=[];reused=[]
 for component in components:
  previous=[k for k,v in result['models'].items() if v['sha256']==component['sha256']]
  assert len(previous)<=1
  if previous:
   reused.append({'head':component['head'],'existing_model_key':previous[0],'sha256':component['sha256']});continue
  key='SparseAfter148_'+component['head'];assert key not in result['models'];result['models'][key]=component
  storage.append({'key':key,'source':component['source_path'],'target':component['path'],'sha256':component['sha256'],
   'samefile':os.path.samefile(component['source_path'],component['path'])})
  for field,report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
   control=deepcopy(next(c for c in report['controls'] if c['head']==component['head']));control['name']=key;result[field].append(control)
  new.append(component['head'])
 assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==before+len(new)
 assert len({v['sha256'] for v in result['models'].values()})==len(result['models'])
 result.update(actual_entire148_then_sparse_native_independent_replays=True,SparseAfter148_stage_calls=calls,
  SparseAfter148_new_physical_heads=new,SparseAfter148_reused_physical_heads=reused,
  complete148_all_original_branches_and_JointCrossHuber_parameters_preserved=True)
 dump(final,result,immutable=True)
 dump(candidate/'SparseAfter148_complete_parent_native_replay_verification.json',{
  'status':'passed_actual_complete148_and_sparse_two_full_native_independent_replays_and_cold80',
  'calls':calls,'actual_saved_model_count':len(result['models']),'actual_native_model_storage':storage,
  'new_physical_heads':new,'reused_physical_heads':reused,'new_native_fits':0,'test_labels_read':False},immutable=True)
 return result,storage
