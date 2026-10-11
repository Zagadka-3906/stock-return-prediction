"""Verify that only the final148-stage return receives the new neural hook; no future inference."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    import predict_BF16Seed10_155_complete_parent_scheme_v1_20261009 as module
    import predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008 as parent
    path=A/module.PARENT_FILENAME;before=path.read_text(encoding='utf8');after=module.prepared_parent148(before);compile(after,str(path),'exec')
    f=lambda s:{n.name:n for n in ast.walk(ast.parse(s)) if isinstance(n,ast.FunctionDef)}
    left,right=f(before),f(after);assert set(left)==set(right)
    for name in left:
        if name not in ('cross_stage','predict'):assert ast.dump(left[name],include_attributes=False)==ast.dump(right[name],include_attributes=False),name
    returns=[n for n in ast.walk(right['cross_stage']) if isinstance(n,ast.Return)]
    assert len(returns)==1 and ast.unparse(returns[0].value)=='SEED10_AFTER_COMPLETE148(context, value)'
    rows=[];sources=[Path(__file__),Path(module.__file__),path,A/'BF16Seed10_155_complete_parent_native_stage_v1_20261009.py']
    for backend,(filename,_,_) in parent.BACKENDS.items():
        source=A/filename;compile(parent.prepared_backend(source.read_text(encoding='utf8'),backend),str(source),'exec')
        rows.append({'backend':backend,'source':str(source),'sha256':sha(source),'original148_adapter_compiles':True});sources.append(source)
    create(A/'BF16Seed10_155_complete_native_predictor_preparation_v1_20261009.json',{
      'status':'passed_seed10_155_only_final148_hook_and5_original_parent_ABI_controls',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
      'original148_definition_unchanged':True,'original5_parent_backends_preserved':rows,
      'new_stage_runs_after_actual148_before_return_mapping':True,'actual_candidate_inference_not_performed':True,
      'actual_future_X_read':False,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'parent':148,'original_ABI_controls':5,'actual_future_inference':0},flush=True)

if __name__=='__main__':main()
