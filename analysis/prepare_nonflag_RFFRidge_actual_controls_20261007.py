"""Declare complete-output comparison axes and launch actual native/CDF controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    stage=A/'nonflag_residual_RFFRidge_native_stage_20261007.py'
    hooks=A/'run_nonflag_residual_RFFRidge_hook3_after_bank_20261007.py'
    transforms=A/'verify_nonflag_residual_RFFRidge37_transform_20261007.py'
    original=[A/'nonflag_residual_Ridge_native_stage_20261007.py',A/'run_nonflag_residual_Ridge_hook3_after_bank_20261007.py',A/'verify_nonflag_residual_Ridge37_transform_20261007.py']
    mapping={'nonflag_residual_Ridge':'nonflag_residual_RFFRidge','nonflag_CPU_Ridge':'nonflag_CPU_RFFRidge',
        'nonflag_Ridge40':'nonflag_RFFRidge40','nonflag_Ridge':'nonflag_RFFRidge',
        'nonflag_cpu_ridge_':'nonflag_cpu_rffridge_','independent_linear_state':'independent_random_fourier_linear_state'}
    for old,new in zip(original,[stage,hooks,transforms]):
        assert not new.exists();source=old.read_text(encoding='utf8')
        for before,after in mapping.items():source=source.replace(before,after)
        source=source.replace("nonflag_residual_RFFRidge_native_bank10'","nonflag_residual_RFFRidge_native_bank10_v2'")
        source=source.replace('round121_candidate_QA32','round122_candidate_QA33')
        if new==stage:
            needle="            assert native['model'].get_params()['solver']=='cholesky'\n            assert native['model'].alpha==info['parameters']['alpha'] and state['features']==info['features']"
            assert source.count(needle)==1
            source=source.replace(needle,"""            projection=native['model'].named_steps['rbf'];linear=native['model'].named_steps['ridge']
            assert linear.solver=='cholesky' and linear.alpha==info['parameters']['alpha']
            assert projection.gamma==info['parameters']['gamma'] and projection.n_components==info['parameters']['n_components']
            assert projection.random_state==info['parameters']['random_state'] and state['features']==info['features']""")
        compile(source,str(new),'exec');new.write_text(source,encoding='utf8',newline='\n')
    plan=read(A/'nonflag_Ridge40_plan_20261007.json')
    import json
    text=json.dumps(plan,ensure_ascii=False)
    for before,after in mapping.items():text=text.replace(before,after)
    plan=json.loads(text);heads=list(read(A/'nonflag_residual_RFFRidge10_plan_20261007.json')['configurations'])
    plan.update(status='frozen_RFFRidge40_before_full_controls_and_official_scores',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        round=122,wave=405,qualified_anchor_rounds=[112,120,121],after_round=121,
        single_native_heads=heads,ensembles={'nonflag_residual_rffridge_equal_mean_two':heads},
        selection='highest_full_connected_official_score_after_actual122_source_admission',
        full_future_candidate_native_replays_and_QA33_required=True,
        parent_nonflag_HGB_or_Ridge_replaced_by_RFFRidge_complete_flag_graph_retained=True,
        input_sha256={str(p):sha(p) for p in [Path(__file__),stage,hooks,transforms,A/'nonflag_residual_RFFRidge10_plan_20261007.json']})
    plan.pop('full_future_candidate_native_replays_and_QA32_required',None)
    plan.pop('parent_nonflag_HGB_replaced_by_Ridge_complete_flag_graph_retained',None)
    plan['existing_native_bank']='nonflag_residual_RFFRidge_bank10_20261007'
    create(A/'nonflag_RFFRidge40_plan_20261007.json',plan)
    paths=[Path(__file__),*original,stage,hooks,transforms,A/'run_nonflag_RFFRidge_actual_controls_20261007.py',A/'nonflag_RFFRidge40_plan_20261007.json']
    pins={str(p):sha(p) for p in paths}
    create(A/'nonflag_RFFRidge_actual_controls_source_preparation_20261007.json',{'status':'compiled_RFFRidge_native3_and_full37_controls_before_execution','input_sha256':pins,'actual_official_scores':0})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_RFFRidge_actual_hook3_and_full37_controls','run_nonflag_RFFRidge_actual_controls_20261007.py',[],pins)
    create(A/'nonflag_RFFRidge_actual_controls_hidden_launch_20261007.json',row)
    print({'status':'started_actual_controls_after_native_bank','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
