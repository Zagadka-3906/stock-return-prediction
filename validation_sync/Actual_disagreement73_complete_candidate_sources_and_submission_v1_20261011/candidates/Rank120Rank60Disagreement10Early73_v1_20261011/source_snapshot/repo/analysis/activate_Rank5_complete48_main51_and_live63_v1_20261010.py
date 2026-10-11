"""Publish prospective177 sources and observe real rank5 scoring without changing workers."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    source=A/'monitor_fast_optimization_v62_20261010.py';text=source.read_text(encoding='utf8').replace('progress_v62','progress_v63').replace('handoff_v107','handoff_v109').replace('rankings_v34','rankings_v35')
    needle="    families=['StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010'"
    extra=['actual_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010','actual_stock_rank5_embedding_after171_large29_completion_main_v65_20261010','actual_stock_rank5_embedding48_after176_normalization_queue_v2_20261010','StockRank5Embedding48_selected_native14_v2_20261010','StockRank5Embedding177_complete48_family_v2_20261010','StockRank5Embedding177_selected_candidate_preparation_v1_20261010','StockRank5Embedding177_selected_candidate_sealing_v1_20261010','StockRank5Embedding177_round177_full_registration_v1_20261010','actual_Rank5_complete48_sources_main_v51_20261010']
    assert text.count(needle)==1;text=text.replace(needle,'    jobs += '+repr(extra)+'\n'+needle)
    text=text.replace("families=['StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010'","families=['StockRank5EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010','StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010'")
    text=text.replace("('StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010',17)","('StockRank5EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010',29),('StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010',17)")
    text=text.replace("'StockTop10Embedding176_complete31_family_v2_20261010'):lines.append","'StockTop10Embedding176_complete31_family_v2_20261010','StockRank5Embedding177_complete48_family_v2_20261010'):lines.append")
    observer=save('monitor_fast_optimization_v63_20261010.py',text)
    source=A/'publish_Top10_full176_sources_actual_main_v49_20261010.py';text=source.read_text(encoding='utf8')
    start=text.index('    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    names=['prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010.py','prepare_stock_rank5_large29_and_complete48_plan_v1_20261010.py','stock_rank5_embedding177_candidate_sources_preparation_v2_20261010.json','stock_rank5_embedding177_full_registry_sources_preparation_v2_20261010.json','stock_rank5_embedding177_full_execution_sources_admission_v2_20261010.json','run_StockRank5Embedding177_complete_family_v2_20261010.py','run_StockRank5Embedding177_full_registration_v2_20261010.py','verify_StockRank5Embedding177_full48_preflight_v2_20261010.py','publish_stock_rank5_embedding_after171_large29_completion_v65_20261010.py','monitor_fast_optimization_v63_20261010.py',Path(__file__).name]
    from prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010 import NAMES,EXTRAS
    names=list(dict.fromkeys([*names,*NAMES,*EXTRAS]));assert all((A/n).is_file() for n in names)
    text=text[:start]+'    paths=[Path(__file__),*[A/n for n in '+repr(names)+']]\n'+text[end:]
    text=text.replace('StockTop10Embedding_verified_BCE_loss_and_runtime','StockRank5Embedding_complete48_sources').replace('v49_20261010','v51_20261010')
    text=text.replace("'compiled_full176_31_normalizer_selected14_candidate_freeze_registry_QA87_main_sources_actual_early171_29_scoring_running'","'compiled_rank5_e64_complete48_normalizer_selected14_candidate_freeze_two_replay_registry_QA88_main_sources_actual17_and29_scoring_pending'")
    text=text.replace("'best_actual_stock_screen_S':.4513551448431997,","'rank5_quality_improvement_not_yet_established':True,")
    text=text.replace('full173_future_candidate_submission_qualification_pending','full177_future_candidate_submission_qualification_pending')
    old="保存第176轮31项比较、独立原生检查、冻结和两次完整推理至QA87及main交付来源；提前171轮29项评分进行中，不遗漏可能优于175轮的方案"
    text=text.replace(old,'保存股票身份五日排名64轮模型的48项选优、14原生因果检查、冻结后两次完整推理、QA88及main来源；分数与未来候选待实际验证')
    publisher=save('publish_Rank5_complete48_sources_actual_main_v51_20261010.py',text)
    oldrow=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v62_20261010/native_launch.json')
    retire(oldrow,'Replace exact childless progress observer62 with63; include actual Rank5 large29 and complete177 queues; no scientific worker altered')
    for name,p in [('actual_fast_optimization_progress_v63_20261010',observer),('actual_Rank5_complete48_sources_main_v51_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'actual_observer63_started':True,'main51_source_publication_started':True,'scientific_workers_restarted':0},flush=True)
if __name__=='__main__':main()
