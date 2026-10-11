"""Preserve early-score lineage and predeclare comparison with fully qualified175."""
from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    plan=A/'stock_top10_embedding_followup31_after175_selection_plan_v1_20261010.json'
    create(plan,{'status':'predeclared_compare_early171_large29_with_complete175_no_score_adaptive_case_addition','expected_records':31,'fully_qualified_anchors':[171,175],'families':[{'name':'StockTop10EmbeddingSmall512_after171_large_allocation29','base_round':171,'records':29,'stage_kind':'stock_top10_embedding_BCE_classifier_direct','actual_service':'actual_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010','main_receipt':'stock_top10_embedding29_after171_completion_main_receipt_v61_20261010.json'}],'expected_full_controls':28,'expected_prefix_controls':84,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','must_not_drop_early171_winner_if_better_than175':True,'actual_comparison_parent_round':175,'new_quality_scores_by_normalization':0,'future_X_read_for_selection':False,'test_labels_read':False,'full176_pipeline_sources_pending':True})
    template=A/'publish_Top10_actual_own6_full5_and_full175_sources_main_v46_20261010.py';text=template.read_text(encoding='utf8');tree=ast.parse(text);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='paths'for t in n.targets))
    paths=[Path(p)for p in ast.literal_eval(node.value)]
    names=['prepare_Top10_after171_early_large29_v1_20261010.py','stock_top10_after171_early_large29_predeclared_admission_v1_20261010.json','admit_Top10_early171_independent42_and_receipt62_v2_20261010.py','admit_Top10_early171_independent42_and_receipt62_v3_20261010.py','admit_Top10_early171_independent42_and_receipt62_v4_20261010.py','recover_Top10_early42_whole_line_schedule_removal_v4_20261010.py','verify_stock_top10_embedding_early171_six_state_native42_v3_20261010.py','run_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010.py','publish_stock_top10_embedding_after171_large_allocation29_completion_v62_20261010.py','stock_top10_early171_independent42_route_admission_v2_20261010.json','monitor_fast_optimization_v60_20261010.py','actual_fast_optimization_progress_v60_activation_20261010.json','actual_stock_top10_embedding_early171_six_state_native42_v3_20261010_activation.json','actual_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010_activation.json','actual_stock_top10_embedding_after171_large_allocation29_completion_main_v62_20261010_activation.json']
    paths += [Path(__file__),template,plan,*[A/n for n in names]];assert all(p.exists()for p in paths)
    lines=text.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths='+repr([str(p)for p in paths])+'\n'];text=''.join(lines)
    for key in ('StockTop10Embedding_verified_BCE_loss_and_runtime_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v'):text=text.replace(key+'46_20261010',key+'47_20261010')
    text=text.replace('passed_actual_Top10_BCE_six_own_mature_annual_fits_full5635800_independent_replay_controls_and_complete47_full175_sources_official_classifier_scores_pending','actual_early171_independent42_and_29_TRAIN_score_queues_complete175_unchanged_followup31_predeclared_no_early_score_completion_claimed')
    text=text.replace('保存Top10分类实际六年度独立训练、五年度5635800行独立解码和冷启动，以及47项选模至完整175轮交付来源；官方分类评分尚未完成','提前在已合格171轮运行独立六状态检查和29项分类大权重官方评分；保留175完整流程并预声明31项后续比较，早期分数和176交付尚未完成')
    driver=A/'publish_early171_large29_and_followup31_actual_main_v47_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_early171_large29_and_followup31_sources_main_v47_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_early171_large29_and_followup31_sources_main_activation_v47_20261010.json',row);print({'actual_main47_worker':row['owned_worker_pid'],'followup31_predeclared':True,'actual_176_pipeline_pending':True},flush=True)
if __name__=='__main__':main()
