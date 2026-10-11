"""Sync real weighted-BCE expression/gradient and corrected v2 GPU routes."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    proof=A/'stock_top10_actual_CUDA_weight_loss_CPU_and_runtime_admission_v2_20261010.json'
    assert read(proof)['status'].startswith('passed')
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    source=A/'publish_stock_top10_sources_and_actual_dual24_main_v41_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows',begin)
    files=[Path(__file__),proof,A/'admit_top10_exact_CUDA_loss_device_and_runtime_v2_20261010.py',A/'stock_top10_embedding_own_sources_admission_v2_20261010.json',A/'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v2_20261010.json']
    files += list(A.glob('*stock_top10*20261010.py'))+list(A.glob('actual_stock_top10*activation*.json'))
    text=text[:begin]+'    paths=[Path(__file__),'+','.join('Path('+repr(str(p))+')' for p in dict.fromkeys(files))+']\n'+text[end:]
    text=text.replace('StockTop10Embedding_sources_and_actual_dual24_v41','StockTop10Embedding_verified_BCE_loss_and_runtime_v42').replace('StockTop10Embedding_sources_and_actual_dual24_main_v41','StockTop10Embedding_verified_BCE_loss_and_runtime_main_v42').replace('StockTop10Embedding_sources_and_actual_dual24_main_receipt_v41','StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v42')
    text=text.replace('passed_actual24_dual_candidate_TRAIN_branches_and_exact_source_name_bindings_new_Top10_BCE_Pos9_actual49153_4909_positive_binary_label_CPU_conversion_six_fits_native42_and17_scores_queued_after174_seal','passed_actual_Top10_weighted_BCE_source_expression_CUDA_weight_binding_CPU_value_and_gradient_original_mature49153_targets_fresh_v2_GPU_routes_queued_after174_seal_no_training_completion_claimed')
    text=text.replace('保存174双模型候选24项真实TRAIN分支独立逐位核对、精确源文件兼容引用，以及新Top10概率分类模型真实49153行目标转换与预声明训练评分队列；GPU训练和17项评分尚待完成','保存Top10概率分类新损失真实源表达式的CPU数值、解析梯度及CUDA正类权重绑定验证，实际v2训练和独立推理来源；保持原17项对照，GPU训练尚待174候选密封')
    pub=A/'publish_stock_top10_verified_loss_and_runtime_main_v42_20261010.py';assert not pub.exists();compile(text,str(pub),'exec');pub.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_stock_top10_verified_loss_and_runtime_main_v42_20261010',pub.name,[],{str(pub):sha(pub)});create(A/'actual_stock_top10_verified_loss_and_runtime_main_activation_v42_20261010.json',row)
    source=A/'monitor_fast_optimization_v54_20261010.py';text=source.read_text(encoding='utf8').replace('actual_stock_top10_embedding_own_training_queue_v1_20261010','actual_stock_top10_embedding_own_training_queue_v2_20261010').replace('actual_stock_top10_embedding_native42_and_after174_fast17_queue_v1_20261010','actual_stock_top10_embedding_native42_and_after174_fast17_queue_v2_20261010')
    text=text.replace('optimization_live_progress_v54','optimization_live_progress_v55').replace('actual_optimization_fast_runtime_handoff_v91','actual_optimization_fast_runtime_handoff_v93').replace('high_impact_additional_validation_rankings_v26','high_impact_additional_validation_rankings_v27')
    monitor=A/'monitor_fast_optimization_v55_20261010.py';assert not monitor.exists();compile(text,str(monitor),'exec');monitor.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_fast_optimization_progress_v55_20261010',monitor.name,[],{str(monitor):sha(monitor)});create(A/'actual_fast_optimization_progress_activation_v55_20261010.json',row)
    while not (A/'optimization_live_progress_v55_20261010.json').exists():assert owned(row);time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v54_20261010/native_launch.json'),'Observer55 tracks actual v2 classifier queues after original pre-dispatch controller retirement; scientific jobs unchanged.')
    create(A/'actual_optimization_fast_runtime_handoff_v92_20261010.json',{'status':'active_full171_registry_and_ranking_after_actual_inference_and_seal_PAS_Top10_loss_CPU_PAS_v2_GPU_queued','deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],'previous_handoff':str(A/'actual_optimization_fast_runtime_handoff_v90_20261010.json'),'actual_progress_observer':55,'actual171_full_registration_worker':38072,'actual171_selected_inference_and_seal_PAS':True,'Top10_actual_training_queue':'actual_stock_top10_embedding_own_training_queue_v2_20261010','Top10_actual_native42_and_score17_queue':'actual_stock_top10_embedding_native42_and_after174_fast17_queue_v2_20261010','Top10_actual_native_module':'stock_top10_embedding_small512_BF16_native_v2_20261010.py','Top10_GPU_phases_wait_actual174_seal':True,'Top10_actual_BCE_expression_and_gradient_CPU_PAS':True,'Top10_new_fits_or_scores':0,'Top10_completed_validation_main_publishers':[58,59],'D_last_seen_free_MB':32.8,'E_last_seen_free_GiB':78.3,'results_json_and_html_actual_targets_on_E_verified':True,'disk_inspection_active_shell_session':1766,'global_optimization_boundary_not_proven':True,'test_labels_read':False})
    print({'verified_loss_and_runtime_main':42,'actual_observer':55},flush=True)
if __name__=='__main__':main()
