"""Publish actual GPU restart and independent CPU evidence, without annual score claims."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    service=A/'service_owned_workflows_20261006/actual_stock_top10_embedding_small512_restart_v1_20261010'
    assert read(service/'service_execution.json')['status']=='passed' and not owned(read(service/'native_launch.json'))
    folder=Path(read(A/'actual_stock_top10_embedding_small512_restart_location_v1_20261010.json')['output'])
    assert read(folder/'verification.json')['status']=='passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    small=A/'service_owned_workflows_20261006/StockTop10EmbeddingSmall512_independent_small_CPU_v1_20261009'
    assert read(small/'service_execution.json')['status']=='passed'
    template=A/'publish_fast_Top10_schedule_and_large29_actual_main_v44_20261010.py';text=template.read_text(encoding='utf8');tree=ast.parse(text)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    paths=[Path(p) for p in ast.literal_eval(node.value)]
    paths += [Path(__file__),template,A/'verify_Top10_six_parent_hooks_and_live57_v1_20261010.py',A/'stock_top10_actual_six_parent_callback_CPU_controls_v1_20261010.json',A/'monitor_fast_optimization_v57_20261010.py',A/'actual_fast_optimization_progress_v57_activation_20261010.json',A/'actual_stock_top10_embedding_small512_restart_location_v1_20261010.json',*folder.rglob('*.json')]
    paths += [service/name for name in ('native_launch.json','service_execution.json','job_definition.json')]
    paths += [small/name for name in ('native_launch.json','service_execution.json','job_definition.json')]
    assert all(p.exists() for p in paths)
    lines=text.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths='+repr([str(p) for p in paths])+'\n'];text=''.join(lines)
    for key in ('StockTop10Embedding_verified_BCE_loss_and_runtime_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v'):
        text=text.replace(key+'43_20261010',key+'45_20261010')
    text=text.replace('passed_schedule3_independent_Top10_GPU_routes_started_predeclared29_large_CDF_allocation_actual28_TRAIN_codec_controls_full_classifier_scores_pending','passed_actual_Top10_GPU_small32_and_wide2_restart_independent_CPU_and_six_exact_parent_callbacks_annual_fit_and_official_scores_pending')
    text=text.replace('提前启动独立Top10分类训练，保留内存保护和检查点；预声明29项大权重融合并完成28项真实TRAIN编解码控制，保存D盘历史报告无损迁移记录','保存Top10分类实际GPU重启参数逐位一致性、独立小样本推理和六个完整父方案回调控制；六年度训练进行中，未声明新官方分数')
    driver=A/'publish_Top10_actual_restart_and_six_hooks_actual_main_v45_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_Top10_actual_restart_and_six_hooks_main_v45_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_Top10_actual_restart_and_six_hooks_main_activation_v45_20261010.json',row);print({'actual_main45_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
