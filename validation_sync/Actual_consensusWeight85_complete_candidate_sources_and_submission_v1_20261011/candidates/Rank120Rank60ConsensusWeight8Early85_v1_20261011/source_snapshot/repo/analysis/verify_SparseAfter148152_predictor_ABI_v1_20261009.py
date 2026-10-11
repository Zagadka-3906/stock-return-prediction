"""Prepare the new parent adapter without performing any future-feature inference."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
 import predict_SparseAfter148_complete_parent_scheme_v1_20261009 as module
 import predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008 as parent
 p=A/module.PARENT_FILENAME;before=p.read_text(encoding='utf8');after=module.prepared_parent148(before)
 compile(after,str(p),'exec')
 left,right=ast.parse(before),ast.parse(after)
 functions=lambda t:{n.name:n for n in ast.walk(t) if isinstance(n,ast.FunctionDef)}
 f0,f1=functions(left),functions(right);assert set(f0)==set(f1)
 for name in f0:
  if name in ('cross_stage','predict'):continue
  assert ast.dump(f0[name],include_attributes=False)==ast.dump(f1[name],include_attributes=False),name
 returns=[n for n in ast.walk(f1['cross_stage']) if isinstance(n,ast.Return)]
 assert len(returns)==1 and isinstance(returns[0].value,ast.Call)
 assert ast.unparse(returns[0].value)=='SPARSE_AFTER_COMPLETE148(context, value, teacher)'
 rows=[];sources=[Path(__file__),Path(module.__file__),p,A/'SparseAfter148_complete_parent_native_stage_v1_20261009.py']
 for backend,(filename,_,_) in parent.BACKENDS.items():
  source=A/filename;compile(parent.prepared_backend(source.read_text(encoding='utf8'),backend),str(source),'exec')
  rows.append({'backend':backend,'source':str(source),'sha256':sha(source),'original148_adapter_compiles':True});sources.append(source)
 create(A/'SparseAfter148152_complete_native_predictor_preparation_v1_20261009.json',{
  'status':'passed_sparse_after_entire148_adapter_only_final_stage_hook_and5_original_parent_ABI_controls',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
  'original148_predictor_definition_source_unchanged':True,'original5_parent_backends_preserved':rows,
  'new_stage_runs_after_actual148_JointCrossHuber_before_return_mapping':True,
  'source_teacher_is_original148_captured106_forecast':True,
  'actual_candidate_inference_not_performed':True,'actual_future_X_read':False,'new_native_fits':0,'new_official_scores':0,'test_labels_read':False})
 print({'parent':148,'original_ABI_controls':5,'actual_future_inference':0},flush=True)
if __name__=='__main__':main()
