"""Publish the actual own restart and independent CPU forward, keeping model tensors local."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    text=(A/'publish_BF16Huber010161_pretraining_controls_v1_20261010.py').read_text(encoding='utf8')
    text=text.replace('huber010','topweightedhuber010').replace('Huber010161','TopWeightedHuber010165')
    text=text.replace('from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle','from owned_idle_publication_wait_runtime_v1_20261010 import hold as suspended_idle')
    text=text.replace("    control=read(A/'current_user_runtime_control_20261010.json')","    read(A/'current_user_runtime_control_20261009.json')\n    control=read(A/'current_user_runtime_control_20261010.json')")
    needle="    paths.extend(restart.rglob('*.json'));paths.extend(small.glob('*.json'))";assert text.count(needle)==1
    text=text.replace(needle,"    paths.extend(A/name for name in ('TopWeightedHuber_independent_loss_micro_gradient_controls_v1_20261010.json','TopWeightedHuber_own_bank_controls_source_admission_v1_20261010.json','run_continuous_fast_reused_frontiers_v18_20261010.py','prepare_TopWeighted_after163_highimpact65_v1_20261010.py','run_TopWeighted_after163_high_impact65_screen_v1_20261010.py','TopWeighted_after163_high_impact65_frozen_intent_v1_20261010.json','TopWeighted_after163_highimpact65_actual_hidden_queue_v1_20261010.json','actual_optimization_fast_runtime_handoff_v14_20261010.json','high_impact_priority_temporal73_main_receipt_v10_20261010.json','github_validation_sync_main_20261005/round164_receipt.json','completed_Huber65_transient_csv_cleanup_v2_20261010/verification.json'))\n"+needle)
    text=text.replace("'own_Huber_delta':.1","'own_Huber_delta':.1,'own_top_sample_weight':5.,'own_top_training_rank_threshold':.9,'actual_closed_form_loss_gradient_micro_tail_cases':20")
    text=text.replace('保存新神经Huber排序损失公式、两项实际断点恢复及10017行独立CPU推理控制，尚未计分','保存Top加权Huber实际两项断点恢复与10017行独立CPU控制及当前最佳方案之后65项组合计划')
    target=A/'publish_BF16TopWeightedHuber010165_pretraining_controls_v1_20261010.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    row=start_service('BF16TopWeightedHuber010165_actual_pretraining_controls_main_v1_20261010',target.name,[],{str(target):sha(target),str(Path(__file__)):sha(Path(__file__))})
    create(A/'TopWeighted165_actual_pretraining_controls_main_hidden_launch_v1_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
