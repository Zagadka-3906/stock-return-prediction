"""Publish completed early six-state controls as their own validation batch."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    service=A/'service_owned_workflows_20261006/actual_stock_top10_embedding_early171_six_state_native42_v3_20261010'
    assert read(service/'service_execution.json')['status']=='passed' and not owned(read(service/'native_launch.json'))
    pointer=A/'actual_stock_top10_embedding_early171_six_state_native42_location_v3_20261010.json';folder=Path(read(pointer)['output']);proof=read(folder/'verification.json')
    assert (proof['actual_saved_states'],proof['actual_native_cases'],proof['actual_cold_cases'],len(proof['prefit_rejections']))==(6,42,42,7)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    template=A/'publish_early171_large29_and_followup31_actual_main_v47_20261010.py';text=template.read_text(encoding='utf8');tree=ast.parse(text);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='paths'for t in n.targets))
    paths=[Path(p)for p in ast.literal_eval(node.value)]+[Path(__file__),template,pointer,*folder.glob('*.json'),*[service/n for n in ('native_launch.json','service_execution.json','job_definition.json')]]
    assert all(p.exists()for p in paths)
    lines=text.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths='+repr([str(p)for p in paths])+'\n'];text=''.join(lines)
    for key in ('StockTop10Embedding_verified_BCE_loss_and_runtime_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v'):text=text.replace(key+'47_20261010',key+'48_20261010')
    text=text.replace('actual_early171_independent42_and_29_TRAIN_score_queues_complete175_unchanged_followup31_predeclared_no_early_score_completion_claimed','passed_actual_Top10_six_saved_states42_native42_cold7_prefit_controls_early171_TRAIN29_official_scoring_running')
    text=text.replace('提前在已合格171轮运行独立六状态检查和29项分类大权重官方评分；保留175完整流程并预声明31项后续比较，早期分数和176交付尚未完成','保存Top10分类实际六状态42项原生、42项冷启动和7项拟合前拒绝检查；提前171轮29项官方评分进行中，不声明提分或完整176交付')
    driver=A/'publish_Top10_early171_actual42_actual_main_v48_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_Top10_early171_actual42_controls_main_v48_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_Top10_early171_actual42_controls_main_activation_v48_20261010.json',row);print({'completed_native_cases':42,'completed_cold_cases':42,'completed_prefit_refusals':7,'actual_main48_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
