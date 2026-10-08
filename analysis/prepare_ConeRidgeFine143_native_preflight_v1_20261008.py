"""Prepare calendar controls and execute five adapter contracts without future X or labels."""
from pathlib import Path
from types import SimpleNamespace
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import numpy as np
    import predict_ConeRidge64_complete_parent_scheme_v1_20261008 as wrapper
    plan=A/'ConeRidgeFine68_round143_plan_v1_20261008.json'
    assert read(plan)['expected_scored_cases']==68
    sources=[Path(__file__),plan,Path(wrapper.__file__)];records=[]
    for backend,(filename,module,has_teacher) in wrapper.BACKENDS.items():
        original=A/filename;text=wrapper.prepared_backend(original.read_text(encoding='utf8'),backend)
        compile(text,str(original),'exec');sources.append(original)
        # Execute the adapter's actual inserted function against an isolated pure sentinel.
        import ast
        tree=ast.parse(text)
        inserted=[node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name=='after_parent']
        assert len(inserted)==1
        teacher=np.array([-.2,0.,.4],dtype=np.float64);parent=np.array([4.,5.,6.],dtype=np.float64)
        ctx=SimpleNamespace();events=[]
        def complete(*args):
            assert args[1] is ctx;events.append('complete_parent');return parent+2.,{'original_parent_report':True}
        complete=wrapper.teacher_capture(complete) if has_teacher else complete
        if not has_teacher:
            capture=wrapper.teacher_capture(lambda *args:(parent,{}))
            capture(None,ctx,teacher,parent,{},[])
        def appended(context,value,passed_teacher):
            assert context is ctx and np.array_equal(value,parent+2.)
            assert context._ConeRidge64_teacher106 is teacher
            assert passed_teacher is teacher if has_teacher else passed_teacher is None
            events.append('new_stage');return value+3.
        namespace={'COMPLETE_PARENT_AFTER':complete,'HUBER_CROSS_AFTER_COMPLETE_PARENT':appended}
        exec(compile(ast.fix_missing_locations(ast.Module(body=inserted,type_ignores=[])),str(original),'exec'),namespace)
        args=(None,ctx,teacher,parent,{},[]) if has_teacher else (None,ctx,parent,{}, {})
        result,report=namespace['after_parent'](*args)
        assert events==['complete_parent','new_stage'] and np.array_equal(result,parent+5.) and report=={'original_parent_report':True}
        records.append({'backend':backend,'actual_inserted_adapter_executed':True,'teacher106_identity_preserved':True,
            'complete_parent_before_new_stage':True,'full_inference_not_claimed':True})
    stages=[('nonflag_CPU_ReverseBayes64_residual_CDF','ReverseBayes'),('BF16_complete_parent_rank_CDF','BF16'),
        ('nonflag_CPU_CrossFamily_complete_parent_CDF','CrossFamily'),('nonflag_CPU_HuberIRLS64_complete_parent_CDF','Huber'),
        ('BF16_reverse_complete_parent_rank_CDF','ReverseBF16'),('nonflag_CPU_HuberCrossFamily_complete_parent_CDF','HuberCrossFamily'),('nonflag_CPU_SpectralGram64_complete_parent_CDF','SpectralGram64'),('nonflag_CPU_KrylovGram64_complete_parent_CDF','KrylovGram64')]
    graph={}
    for key,expected in stages:
        graph[key]={'prospective_only':True};assert wrapper.backend_for(graph)==expected
    assert len(records)==8
    create(A/'ConeRidgeFine143_native_receiver_preflight_v1_20261008.json',{
        'status':'passed_eight_actual_inserted_adapter_contracts_before_quality',
        'input_sha256':{str(p):sha(p) for p in sources},'adapter_controls':records,'backend_priority_cases':8,
        'new_fits':0,'new_official_scores':0,'new_actual_future_inference_claimed':False,'test_labels_read':False})
    print('Eight actual complete-parent adapter contracts passed; no actual future features read.',flush=True)

if __name__=='__main__':main()
