"""Record verified live handoff and correct inherited round164 prose without changing science."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    controls={name:read(A/name) for name in ['current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json']}
    now=datetime.now(timezone(timedelta(hours=8)));assert all(c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local']) for c in controls.values())
    state=read(A/'optimization_live_progress_v19_20261010.json')
    launches={name:read(A/'service_owned_workflows_20261006'/name/'native_launch.json') for name in ['continuous_fast_reused_frontiers_v19_20261010','actual_fast_optimization_progress_v19_20261010','actual_user_stop1100_wait_manual_continue_v1_20261011','main_publisher_v11_20261010']}
    assert all(owned(v) for v in launches.values())
    frontier=read(A/'ReusedNN164_prepared_frontier_v1_20261010.json');receipt=read(A/'github_validation_sync_main_20261005/round164_receipt.json')
    assert [frontier[k] for k in ['recipe','role','count','QA','grid']]==['huber010','all_valid',19,75,10]
    assert receipt['scored_records']==19 and read(A/'optimization_20261003_r164/full_registration_execution.json')['status']=='passed'
    correction=A/'round164_actual_scope_prose_correction_v1_20261010.json'
    create(correction,{'status':'verified_actual_contract_corrects_inherited_prose_only','round':164,'actual_recipe':'huber010','actual_role':'all_valid','actual_quality_records':19,'actual_anchors':[152,163],'actual_QA':75,'actual_grid':10,'actual_main_commit':receipt['commit'],'inherited_template_prose_may_say_seed09_flag_valid_22_five_anchors':True,'official_scores_and_scientific_proofs_unchanged':True,'input_sha256':{str(A/n):sha(A/n) for n in ['ReusedNN164_prepared_frontier_v1_20261010.json','github_validation_sync_main_20261005/round164_receipt.json','optimization_20261003_r164/full_registration_execution.json']}})
    handoff=A/'actual_optimization_fast_runtime_handoff_v15_20261010.json'
    create(handoff,{'status':'active_verified_new_signal_priority_until_actual_deadline','at_local':now.isoformat(),'controls':controls,'launches':launches,'best_fully_qualified':state['best_fully_qualified'],'actual_new_TopWeighted_training':state['actual_new_TopWeighted_training'],'new_return_training':state['actual_new_ReturnHuber_training'],'TopWeighted_after163_screen':state['TopWeighted_after163_screen'],'CPU20_return_main_receipt':read(A/'ReturnHuber050_actual_CPU20_fixture_main_receipt_v1_20261010.json'),'priority':'complete Top165 and stronger-parent65, qualify any actual winner first, otherwise own return restart/six fits/full5/native42 then166','scientific_workers_stopped_or_restarted_by_handoff':0,'new_scores_claimed_by_handoff':0,'resource_or_direction_exhaustion_proven':False,'disk_free_GiB':state['disk_free_GiB']})
    s=(A/'publish_ReturnHuber050_actual_CPU20_fixture_controls_v1_20261010.py').read_text(encoding='utf8')
    names=['record_and_publish_new_signal_priority_v15_20261010.py','actual_optimization_fast_runtime_handoff_v15_20261010.json','round164_actual_scope_prose_correction_v1_20261010.json','prepare_new_return_priority_controller_v19_20261010.py','run_continuous_fast_reused_frontiers_v19_20261010.py','handoff_new_return_priority_controller_v19_20261010.py','new_return_priority_handoff_v19_20261010/verification.json','new_return_priority_handoff_v19_20261010/frozen_before_handoff.json','prepare_progress_observer19_new_return_v1_20261010.py','monitor_fast_optimization_v19_20261010.py','actual_fast_optimization_progress_v19_handoff_v1_20261010.json','prepare_TopWeighted65_completion_main_v12_20261010.py','publish_TopWeighted_after163_65_completion_v12_20261010.py','TopWeighted_after163_65_completion_main_hidden_launch_v12_20261010.json','completed164_temporal73_transient_csv_cleanup_v1_20261010/verification.json']
    needle='    import publish_classifier_consensus_workflows_20261006 as h';assert s.count(needle)==1
    s=s.replace(needle,'    paths.extend(A/name for name in '+repr(names)+')\n'+needle)
    s=s.replace('ReturnHuber050_actual_CPU20_fixture_controls_v1_20261010','new_signal_priority_handoff_v15_20261010').replace('ReturnHuber050_actual_CPU20_fixture_main_v1_20261010','new_signal_priority_handoff_main_v15_20261010').replace('ReturnHuber050_actual_CPU20_fixture_main_receipt_v1_20261010.json','new_signal_priority_handoff_main_receipt_v15_20261010.json')
    s=s.replace('保存直接收益率宽网络20项实际CPU目标损失梯度检查及成熟训练样本证明，GPU验证待执行','优先新训练目标并保留科学进程：Top加权与直接收益率宽网络，修正164轮继承说明文字')
    target=A/'publish_new_signal_priority_handoff_v15_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    row=start_service('actual_new_signal_priority_handoff_main_v15_20261010',target.name,[],{str(target):sha(target),str(Path(__file__)):sha(Path(__file__))})
    create(A/'new_signal_priority_handoff_main_launch_v15_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
