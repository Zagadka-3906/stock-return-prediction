"""Verify already-created sources, then finish metadata after generator3 completion."""
from pathlib import Path
import ast
import json
import sys

A=Path(__file__).resolve().parent
sys.path.insert(0,str(A))
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    proof=A/'joint_goss_membership_generator_preflight_v3_20261006/verification.json'
    assert read(proof)['status']=='passed'
    source=A/'prepare_joint_goss_round97_queue_sources_v3_20261006.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
    effective=[];replaced=0
    for node in body:
        if isinstance(node,ast.With):
            assert len(node.items)==1 and isinstance(node.body[0],ast.Expr)
            expression=node.items[0].context_expr
            assert isinstance(expression,ast.Call) and isinstance(expression.func,ast.Attribute) and expression.func.attr=='open'
            path=expression.func.value
            test=ast.Compare(left=ast.Call(func=ast.Attribute(value=path,attr='read_text',ctx=ast.Load()),
                args=[],keywords=[ast.keyword(arg='encoding',value=ast.Constant('utf-8'))]),
                ops=[ast.Eq()],comparators=[ast.Name(id='text',ctx=ast.Load())])
            effective.append(ast.Assert(test=test,msg=ast.Constant('Already-created source differs from unchanged preparation source')))
            replaced+=1
        else:effective.append(node)
    assert replaced==2
    assert not (A/'joint_goss_membership_quality_run_v3_20261006.json').exists()
    assert not (A/'joint_goss_membership_round97_previous_run_v3_20261006.json').exists()
    env={'A':A,'Path':Path,'create':create,'sha':sha}
    exec(compile(ast.fix_missing_locations(ast.Module(body=effective,type_ignores=[])),str(source),'exec'),env)
    failure=A/'joint_goss_round97_full_launcher_preflight_v3_20261006/failure.json'
    assert read(failure)['error'].startswith('FileNotFoundError:')
    out=A/'joint_goss_round97_preparation_recovery_20261006';out.mkdir()
    create(out/'verification.json',{'status':'passed_existing_queue10_and_observer34_verified_and_run3_frozen_after_generator3_pass',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),source,proof,failure,
            A/'run_dependency_queue_v10_20261006.py',A/'monitor_actual_optimization_progress_v34_20261006.py',
            A/'joint_goss_membership_quality_run_v3_20261006.json',A/'joint_goss_membership_round97_previous_run_v3_20261006.json')},
        'original_prepare_attempt_failed_before_run_metadata':True,
        'original_prepare_error':'FileNotFoundError: generator3 verification.json was not available yet',
        'two_existing_sources_byte_identical_to_unchanged_creator':True,
        'existing_sources_not_overwritten':True,'original_full_launcher3_failure_preserved':True,
        'actual_scientific_grid_or_live_workers_changed':False,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    old=A/'verify_joint_goss_round97_full_launcher_v3_20261006.py'
    text=old.read_text(encoding='utf-8')
    before='joint_goss_round97_full_launcher_preflight_v3_20261006'
    assert text.count(before)==1;text=text.replace(before,'joint_goss_round97_full_launcher_preflight_v4_20261006')
    with (A/'verify_joint_goss_round97_full_launcher_v4_20261006.py').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    print('Preparation recovered without changing old sources; full launch control4 is ready.',flush=True)

if __name__=='__main__':main()
