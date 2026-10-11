"""Execute the scorer's exact unique-model expression for anchors, identity and physical neural reuse."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    source=A/'run_BF16reverse40_official_comparison_v1_20261008.py';tree=ast.parse(source.read_text(encoding='utf8'))
    item=next(node.value for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in node.targets) and isinstance(node.value,ast.Dict))
    expression=next(v for k,v in zip(item.keys,item.values) if isinstance(k,ast.Constant) and k.value=='expected_unique_native_models')
    code=compile(ast.Expression(body=expression),str(source),'eval');records=[]
    for reused in (False,True):
        models={'a':{'sha256':'A'},'b':{'sha256':'N' if reused else 'B'}}
        for model,weight in ((None,0.),('identity',0.),('negative_new_neural',.0025),('negative_new_neural',1.)):
            value=eval(code,{'cfg':{'anchor_round':137,'model':model,'weight':weight},'parent_models':{137:models},'neural_sha':'N'})
            expected=2 if reused or model is None or weight==0. else 3;assert value==expected
            records.append({'neural_physically_in_parent':reused,'model':model,'weight':weight,'actual_expression_count':value})
    selected=A/'prepare_BF16reverse40_selected_candidate_v1_20261008.py';selected_text=selected.read_text(encoding='utf8')
    assert "component['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()}" in selected_text
    create(A/'BF16reverse138_model_count_contract_v1_20261008.json',{'status':'passed_actual8_anchor_identity_new_and_reused_neural_unique_SHA_union_count_expressions',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,selected]},'records':records,
        'alias_names_do_not_add_physical_models_to_selection':True,'new_official_scores':0,'new_fits':0,'test_labels_read':False})
    print('Actual8 model count contracts passed, including zero extra physical models for an existing positive neural head.',flush=True)


if __name__=='__main__':main()
