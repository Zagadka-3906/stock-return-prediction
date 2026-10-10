"""Publish verified scheduling improvements and predeclared TRAIN tests to main."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    original=A/'publish_stock_top10_verified_loss_and_runtime_main_v42_20261010.py'
    text=original.read_text(encoding='utf8')
    tree=ast.parse(text);mainnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    assignment=next(n for n in mainnode.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    names=['accelerate_independent_Top10_training_schedule_v3_20261010.py','verify_stock_top10_embedding_small512_restart_memory_guard_v3_20261010.py','train_stock_top10_embedding_small512_BF16_bank6_memory_guard_v3_20261010.py','run_stock_top10_embedding_own_training_queue_v3_20261010.py','run_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010.py','stock_top10_independent_training_schedule_admission_v3_20261010.json','actual_stock_top10_independent_training_acceleration_v3_20261010.json','prepare_Top10_large_allocation29_and_fast_runtime_v1_20261010.py','run_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010.py','predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010.py','stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json','publish_stock_top10_embedding_after174_large_allocation29_completion_v60_20261010.py','actual_stock_top10_large_allocation29_activation_v1_20261010.json','monitor_fast_optimization_v56_20261010.py','actual_fast_optimization_progress_v56_activation_20261010.json','actual_D_historical_reports_lossless_E_relocation_verification_v1_20261010.json']
    paths=[Path(__file__),original,*[A/n for n in names]]
    for n in ('actual_stock_top10_embedding_own_training_queue_v3_20261010','actual_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010','actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after174_large_allocation29_completion_main_v60_20261010'):
        paths.extend(A/'service_owned_workflows_20261006'/n/f for f in ('native_launch.json','job_definition.json'))
    paths.extend(Path('E:/赛题五_本机临时/D盘历史报告无损迁移_v1_20261010')/n for n in ('manifest.json','historical_reports_batch_v2.json'))
    assert all(p.exists() for p in paths)
    lines=text.splitlines(keepends=True)
    lines[assignment.lineno-1:assignment.end_lineno]=['    paths='+repr([str(p) for p in paths])+'\n','    paths=[Path(p) for p in paths]\n']
    text=''.join(lines).replace('v42_20261010','v43_20261010')
    text=text.replace('passed_actual_Top10_weighted_BCE_source_expression_CUDA_weight_binding_CPU_value_and_gradient_original_mature49153_targets_fresh_v2_GPU_routes_queued_after174_seal_no_training_completion_claimed','passed_schedule3_independent_Top10_GPU_routes_started_predeclared29_large_CDF_allocation_actual28_TRAIN_codec_controls_full_classifier_scores_pending')
    text=text.replace('保存Top10概率分类新损失真实源表达式的CPU数值、解析梯度及CUDA正类权重绑定验证，实际v2训练和独立推理来源；保持原17项对照，GPU训练尚待174候选密封','提前启动独立Top10分类训练，保留内存保护和检查点；预声明29项大权重融合并完成28项真实TRAIN编解码控制，保存D盘历史报告无损迁移记录')
    driver=A/'publish_fast_Top10_schedule_and_large29_actual_main_v43_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_fast_Top10_schedule_and_large29_main_v43_20261010',driver.name,[],{str(driver):sha(driver),str(Path(__file__)):sha(__file__)})
    create(A/'actual_fast_Top10_schedule_and_large29_main_activation_v43_20261010.json',row)
    print({'actual_source_publication_worker':row['owned_worker_pid'],'branch':'main'},flush=True)
if __name__=='__main__':main()
