"""Actual isolated predictor callbacks and unchanged Windows storage API checks."""
from pathlib import Path
import sys,ast,copy,ctypes
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import predict_rank120_rank60_consensusWeight_complete_qualified183_scheme85_v1_20261011 as predictor
 original=A/'stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
 parents=[*[r['parent'] for r in read(original)['records']],'predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py']
 records=[]
 for name in parents:
  path=A/name;tree=ast.parse(predictor.prepared_parent(path.read_text(encoding='utf8')))
  nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
  context=object();ns=object();spec=object();component=object();components=[component];calls=[];events=[]
  def before(a,b,c,d,e):
   assert a is ns and b is context and c==11 and d is spec and (e is component or e is components)
   events.append('complete_parent_first');return 22,{}
  def after(a,b):
   assert a is context and b==22 and len(calls)==1;events.append('disagreement_stage_last');return 33
  scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=before,RANK120_RANK60_PROTECTED_AFTER_WHOLE_QUALIFIED_PARENT=after)
  exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(path)+'::actual_disagreement_CPU_callback','exec'),scope)
  assert scope[nodes[0].name](context,11)==33 and events==['complete_parent_first','disagreement_stage_last']
  records.append({'parent':name,'sha256':sha(path),'actual_callback_order':events,'CPU_stub_only':True})
 assert len(records)==12
 storage=A/'rank120_rank60_consensusWeight8_early85_storage_v1_20261011.py'
 tree=ast.parse(storage.read_text(encoding='utf8'))
 attributes=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,ast.Attribute) and n.attr=='GetFileAttributesW']
 assert attributes==['ctypes.windll.kernel32.GetFileAttributesW']
 actual=ctypes.windll.kernel32.GetFileAttributesW(str(A));assert actual!=0xFFFFFFFF
 stage=A/'rank120_rank60_consensusWeight_after_qualified183_native_stage85_v1_20261011.py'
 import rank120_rank60_consensusWeight_after_qualified183_native_stage85_v1_20261011 as module
 assert module.GRAPH_KEY=='rank120_rank60_consensusWeight_after_complete_qualified_parent85_v1_20261011'
 assert module.RECIPE=='stock_rank120_rank60_consensusWeight_label_horizon_ID16_cross120_recent252_e64'
 create(A/'actual_consensusWeight85_callback12_storage_and_recipe_CPU_controls_v1_20261011.json',{'status':'passed_actual_callback12_storage_Win32_API_and_recipe_controls','records':records,'actual_kernel32_GetFileAttributesW_result':actual,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(predictor.__file__),storage,stage,original]},'native_replay_not_yet_claimed':True,'future_X_read':False,'test_labels_read':False})
 print({'actual_CPU_callbacks':12,'actual_storage_API_passed':True,'native_candidate_not_yet_claimed':True},flush=True)
if __name__=='__main__':main()
