"""Publish actual20 independent loss controls, admitted new training and current complete163 handoff."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    names=['prepare_topweighted_Huber_training_frontier_v1_20261010.py','neural_BF16_medium2048_topweightedhuber010_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_topweightedhuber010_seed09_independent_forward_v1_20261009.py','train_neural_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009.py','neural_BF16_medium2048_topweightedhuber010_seed09_e64_frontier_v1_20261010.json','verify_topweighted_Huber_loss_micro_gradients_v1_20261010.py','TopWeightedHuber_independent_loss_micro_gradient_controls_v1_20261010.json','prepare_topweighted_Huber_own_bank_controls_v1_20261010.py','TopWeightedHuber_own_bank_controls_source_admission_v1_20261010.json','run_continuous_fast_reused_frontiers_v18_20261010.py','handoff_topweighted_training_priority_controller_v18_20261010.py','prepare_progress_observer18_topweighted_training_v1_20261010.py','monitor_fast_optimization_v18_20261010.py','save_high_impact_runtime_handoff_v13_20261010.py','actual_optimization_fast_runtime_handoff_v13_20261010.json','cleanup_discarded_quantization_budget_scoring_csv_v1_20261010.py','github_validation_sync_main_20261005/round163_receipt.json','optimization_20261003_r163/full_registration_execution.json','high_impact_priority_preparation_main_receipt_v10_20261010.json']
    proof=read(A/'TopWeightedHuber_own_bank_controls_source_admission_v1_20261010.json')
    for p,d in proof['input_sha256'].items():
        path=Path(p);assert sha(path)==d
        if path.is_relative_to(ROOT):names.append(path.relative_to(A).as_posix())
    text=(A/'publish_priority_Huber163_temporal73_v10_20261010.py').read_text(encoding='utf8')
    needle="    if phase in ('scores'";assert text.count(needle)==1
    before="    sources.extend(A/name for name in "+repr(list(dict.fromkeys(names)))+")\n"
    before+="    for tag in ('topweighted_training_priority_handoff_v18_20261010','TopWeighted_training_observer_handoff_v18_20261010','discarded_quantization_budget_csv_cleanup_v1_20261010'):\n        sources.extend((A/tag).glob('*.json'))\n"
    text=text.replace(needle,before+needle)
    text=text.replace('main_v10_20261010','main_v11_20261010').replace("phase+'_v10_20261010'","phase+'_v11_20261010'").replace('main_receipt_v10_20261010','main_receipt_v11_20261010')
    text=text.replace("'high_impact_priority_preparation_main_receipt_v11_20261010.json'","'high_impact_priority_preparation_main_receipt_v10_20261010.json'")
    text=text.replace('优先验证实测更高分Huber163并扩展73项因果神经信号平滑','发布新TopWeightedHuber20项独立损失梯度控制与完整163候选及新训练安排')
    driver=A/'publish_topweighted_controls_and_handoff_v11_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_topweighted_controls_handoff_preparation_main_v11_20261010',driver.name,['preparation'],{str(driver):sha(driver),str(Path(__file__)):sha(Path(__file__))})
    create(A/'TopWeighted_controls_handoff_main_actual_launch_v11_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
