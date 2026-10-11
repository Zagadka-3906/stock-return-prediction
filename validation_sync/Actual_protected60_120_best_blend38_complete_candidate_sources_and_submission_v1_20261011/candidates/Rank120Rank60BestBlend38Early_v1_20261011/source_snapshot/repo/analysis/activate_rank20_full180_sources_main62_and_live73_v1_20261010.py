"""Publish new48/QA91 routes and observe the existing actual training and inference workers."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();text=(A/'monitor_fast_optimization_v72_20261010.py').read_text(encoding='utf8').replace('progress_v72','progress_v73').replace('handoff_v123','handoff_v124').replace('rankings_v44','rankings_v45')
    jobs=['actual_stock_rank20_embedding_full5_native42_and_early17_queue_v1_20261010','StockRank20EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_rank20_embedding_six_state_native42_v1_20261010','actual_stock_rank20_embedding_after173_fast17_screen_v1_20261010','actual_stock_rank20_embedding_after173_large_allocation29_screen_v1_20261010','actual_stock_rank20_embedding_after173_completion_main_v77_20261010','actual_stock_rank20_embedding_six_state_native42_completion_main_v78_20261010','actual_stock_rank20_embedding_after173_large29_completion_main_v79_20261010','actual_stock_rank20_embedding48_after179_normalization_queue_v5_20261010','StockRank20Embedding48_selected_native14_v5_20261010','StockRank20Embedding180_complete48_family_v6_20261010','actual_rank20_full180_sources_main_v62_20261010']
    families=['StockRank20EmbeddingSmall512_after173_high_impact17_screen_v1_20261010','StockRank20EmbeddingSmall512_after173_large_allocation29_screen_v1_20261010']
    text=text.replace('    while True:\n','    jobs += '+repr(jobs)+'\n    families += '+repr(families)+'\n    while True:\n')
    text=text.replace('        lines += [f"内存可用',"        lines.append(f\"20日排名完整48项/QA91资格服务：{services['StockRank20Embedding180_complete48_family_v6_20261010']['status']}；尚未完成的年度训练和评分以真实回执为准。\")\n        lines += [f\"内存可用")
    observer=save('monitor_fast_optimization_v73_20261010.py',text)
    import prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010 as full
    proof=A/'stock_rank20_embedding180_full_execution_sources_admission_v1_20261010.json'
    paths=[Path(__file__),observer,*full.source_paths(),proof,A/'prepare_stock_rank20_embedding_full5_native42_and_screen46_v1_20261010.py',A/'prepare_stock_rank20_embedding_full5_native42_screen46_v1_20261010.py',A/'publish_stock_rank20_embedding_after173_completion_v77_20261010.py',A/'publish_stock_rank20_embedding_six_state_native42_completion_v78_20261010.py',A/'publish_stock_rank20_embedding_after173_large29_completion_v79_20261010.py',A/'stock_rank20_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json',A/'stock_rank20_embedding_own64_native_sources_preparation_v1_20261010.json',A/'stock_rank20_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json']
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    source=A/'publish_StockRank20_actual49153_CPU7_own64_sources_main_v61_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('StockRank20_real49153_CPU7_own64_sources_v61','StockRank20_full180_complete48_sources_v62').replace('StockRank20_real49153_CPU7_own64_sources_main_v61','StockRank20_full180_complete48_sources_main_v62').replace('StockRank20_real49153_CPU7_own64_sources_main_receipt_v61','StockRank20_full180_complete48_sources_main_receipt_v62')
    text=text.replace('passed_actual49153_rank20_identity_cross120_mature_fixture_and_all_mature_day_Pandas_rank_bits_and7_scalar_poison_cases_own64_GPU_training_pending','compiled_rank20_complete48_selected14_source_freeze_two_full_future_replays_QA91_and_main_routes_actual11_parent_callbacks_CPU_annual_training_pending')
    text=text.replace('保存股票身份与120维特征二十日截面排名目标的实际49153成熟样本、全成熟日Pandas排名位级检查和7项标量因果检查；年度GPU训练等待174候选封装','保存二十日截面排名模型180轮完整48项比较、11个完整父方案回调、冻结推理与完整榜QA91源码；年度训练及质量评分按实际完成回执判定')
    publisher=save('publish_StockRank20_full180_complete48_sources_main_v62_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v72_20261010/native_launch.json'),'Replace childless observer72 with73 including exact future full180 and rank20 TRAIN46 jobs')
    for name,p in [('actual_fast_optimization_progress_v73_20261010',observer),('actual_rank20_full180_sources_main_v62_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'full18048_sources_main62_started':True,'live73_started':True,'no_future_or_training_completion_claimed':True},flush=True)
if __name__=='__main__':main()
