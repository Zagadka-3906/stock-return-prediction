"""Correct inherited version1 administrative paths before any annual fit; keep numerical recipe2."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    failed=A/'service_owned_workflows_20261006/nonflag_KrylovGram64_bank20_v2_20261008'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    assert read(failed/'service_execution.json')['failure'].startswith('FileNotFoundError:')
    assert not Path('E:/赛题五_本机临时/nonflag_KrylovGram64_bank20_v1_20261008').exists()
    source=A/'train_nonflag_KrylovGram64_bank20_v2_20261008.py';target=A/'train_nonflag_KrylovGram64_bank20_v3_20261008.py'
    mapping={'nonflag_KrylovGram64_bank20_v1_20261008':'nonflag_KrylovGram64_bank20_v3_20261008',
        'nonflag_KrylovGram64_bank20_plan_v1_20261008':'nonflag_KrylovGram64_bank20_plan_v3_20261008',
        'nonflag_KrylovGram64_bank20_location_v1_20261008':'nonflag_KrylovGram64_bank20_location_v3_20261008'}
    text=source.read_text(encoding='utf8');updated=text
    for before,after in mapping.items():assert before in updated;updated=updated.replace(before,after)
    tree=ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node,ast.Constant) and isinstance(node.value,str):
            for before,after in mapping.items():node.value=node.value.replace(before,after)
    assert ast.dump(tree)==ast.dump(ast.parse(updated))
    assert not target.exists();compile(updated,str(target),'exec');target.write_text(updated,encoding='utf8',newline='\n')
    previous=A/'nonflag_KrylovGram64_bank20_plan_v2_20261008.json';plan=read(previous)
    files=[Path(__file__),source,target,previous,failed/'native_launch.json',failed/'job_definition.json',failed/'service_execution.json',failed/'stderr.log']
    recovery=A/'KrylovGram64_bank20_admin_path_preparation_v3_20261008.json'
    create(recovery,{'status':'passed_constant_only_bank_admin_path_correction_before_actual_training',
        'input_sha256':{str(p):sha(p) for p in files},'constant_mapping':mapping,'AST_math_and_control_flow_unchanged':True,
        'native_numerical_recipe_version':2,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    plan.update(status='frozen_before_actual20_own_mature_reorthogonalizedCG_recipe2_bank3',
        input_sha256={**plan['input_sha256'],**{str(p):sha(p) for p in [*files,recovery]}},
        native_numerical_recipe_version=2,bank_administrative_version=3)
    plan_path=A/'nonflag_KrylovGram64_bank20_plan_v3_20261008.json';create(plan_path,plan)
    row=start('nonflag_KrylovGram64_bank20_v3_20261008',target.name,[],{**plan['input_sha256'],str(plan_path):sha(plan_path)})
    create(A/'actual_nonflag_KrylovGram64_bank20_hidden_launch_v3_20261008.json',row)
    print('Twenty native2 own-mature fits dispatched in fresh bank3 administrative paths.',flush=True)

if __name__=='__main__':main()
