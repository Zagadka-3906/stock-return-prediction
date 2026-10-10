"""Freeze additive dispatch and exercise actual ownership without public mutations."""
from pathlib import Path
from copy import deepcopy
import ast
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=A/'joint_goss_round97_queue_preparation_20261006'

def main():
    assert not OUT.exists();OUT.mkdir()
    proof=A/'joint_goss_round97_full_launcher_preflight_v4_20261006/verification.json'
    assert read(proof)['status']=='passed_actual_joint97_nested_bridges_full_QA_and_preserved93_through96_main_export_routes'
    old_path=A/'service_owned_dependency_queue_v4_20261006/queue_plan_v7.json'
    old=read(old_path)
    sources=[Path(__file__),old_path,proof,A/'joint_goss_round97_preparation_recovery_20261006/verification.json',
        A/'handoff_joint_goss_round97_full_execution_20261006.py',A/'run_dependency_queue_v10_20261006.py',
        A/'monitor_actual_optimization_progress_v34_20261006.py',A/'watch_validations_main_v7_20261006.py',
        A/'joint_goss_membership_quality_run_v3_20261006.json',
        A/'joint_goss_membership_round97_previous_run_v3_20261006.json']
    pins={**read(sources[-2])['input_sha256'],**{str(p):sha(p) for p in sources}}
    for p,digest in pins.items():assert sha(p)==digest,p
    plan=deepcopy(old)
    job={'name':'round97','round':97,'previous_run':str(sources[-1]),
        'gate':{'parent':95,'closed_jobs':['round95'],'quality_slot':True,
            'markers':[{'path':str(proof),'statuses':[read(proof)['status']]},
                       {'path':str(A/'joint_goss_membership_generator_preflight_v3_20261006/verification.json'),'statuses':['passed']}]},
        'scratch':str(ROOT/'tmp/joint_goss_round97_20261006')}
    insertion=next(i for i,j in enumerate(plan['deferred_jobs']) if j['name']=='round96')+1
    plan['deferred_jobs'].insert(insertion,job)
    assert [j for j in plan['deferred_jobs'] if j['name']!='round97']==old['deferred_jobs']
    assert len({j['round'] for j in old['deferred_jobs'] if 'round' in j})==25
    assert len({j['round'] for j in plan['deferred_jobs'] if 'round' in j})==26
    plan.update(status='prospective_additive_joint97_before_actual_handoff',input_sha256={**old['input_sha256'],**pins},
        prior_queue_plan=str(old_path),additional_required_rounds=[95,96,97],
        activation_handoff_commit_marker=str(A/'joint_goss_round97_actual_handoff_20261006/handoff_commit.json'),
        original_scientific_grids_and_all25_routes_and67_through96_retained=True,
        joint97_expected_full_records=151,additional_unqualified_records_not_in_complete_board=True)
    plan['exact_rank_cached_rounds']=sorted(set(old['exact_rank_cached_rounds'])|{97})
    create(OUT/'prospective_queue_plan_v10.json',plan)
    text=(A/'run_dependency_queue_v10_20261006.py').read_text(encoding='utf-8')
    tree=ast.parse(text)
    target=next(node for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute)
        and node.func.attr=='update' and any(k.arg=='original_script' for k in node.keywords))
    expression=next(k.value for k in target.keywords if k.arg=='original_script')
    routes={}
    for n in (84,85,86,95,96,97):
        routes[n]=Path(eval(compile(ast.Expression(expression),str(A/'run_dependency_queue_v10_20261006.py'),'eval'),
            {'A':A,'job':{'round':n},'plan':plan})).name
    assert routes[97]=='run_joint_goss_quality_with_exact_rank_cache_v3_20261006.py'
    assert routes[95]==routes[96]=='run_goss_reference_quality_with_exact_rank_cache_20261006.py'
    assert all(routes[n]=='run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py' for n in (84,85,86))
    import monitor_actual_optimization_progress_v34_20261006 as monitor
    queue=read(A/'service_owned_workflows_20261006/dependency_queue_v7/native_launch.json')
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    assert owned(queue) and owned(state['activated_jobs']['round95'])
    value=read(A/'ongoing_optimization_state.json');private=deepcopy(value)
    private['pending_required_rounds']=sorted(set(private['pending_required_rounds'])|{97})
    stub=deepcopy(state);stub['activated_jobs']['round97']=deepcopy(stub['activated_jobs']['round95'])
    private_state={}
    # Only the private fixture uses an actual95 handle under a97 key.
    monitor.augment_ready_goss_ownership(private,private_state,queue,stub)
    assert private['current_recovered_worker_ownership']['round97']['owned_live_now']
    bad=deepcopy(stub);bad['activated_jobs']['round97']['owned_worker_creation_time']+=1
    other=deepcopy(value);other['pending_required_rounds']=private['pending_required_rounds']
    monitor.augment_ready_goss_ownership(other,{},queue,bad)
    assert not other['current_recovered_worker_ownership']['round97']['owned_live_now']
    for p,digest in pins.items():assert sha(p)==digest,p
    create(OUT/'verification.json',{'status':'passed_all_original25_routes_preserved_and_additive151_record_dispatch_and_owner_controls',
        'input_sha256':pins,'original_routes':25,'new_total_routes':26,'additional_records':151,
        'actual_dispatch_expression_routes':routes,'actual95_handle_accepted_only_in_private97_fixture':True,
        'private_mismatched_creation_time_rejected':True,'public_ownership_fixtures_written':False,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False,
        'actual_handoff_and151_quality_records_still_required':True})
    print('passed_original25_routes_and_additive151_record_dispatch_and_private_owner_controls',flush=True)

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_joint97_queue_preparation','error':f'{type(exc).__name__}: {exc}'})
        raise
