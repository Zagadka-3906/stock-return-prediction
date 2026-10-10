"""Extend owned progress reporting and publish newly admitted rank experiment sources."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    jobs=['StockEmbedding173_complete36_family_v3_20261010','actual_stock_embedding36_after172_normalization_queue_v1_20261010','StockEmbedding36_selected_native14_v1_20261010','actual_stock_rank_embedding_own_training_queue_v2_20261010','actual_stock_rank_embedding_small512_restart_v1_20261010','StockRankEmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_rank_embedding_small512_bank6_v1_20261010','StockRankEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_rank_embedding_native42_and_fast17_queue_v1_20261010','actual_stock_rank_embedding_six_state_native42_v1_20261010','actual_stock_rank_embedding_after170_fast17_screen_v1_20261010']
    source=A/'monitor_fast_optimization_v48_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace("    families=['StockEmbeddingSmall512",'    jobs='+repr(jobs)+'+jobs\n'+'    families=[\'StockRankEmbeddingSmall512_after170_high_impact17_screen_v1_20261010\',\'StockEmbeddingSmall512')
    text=text.replace('optimization_live_progress_v48','optimization_live_progress_v49').replace('high_impact_additional_validation_rankings_v20','high_impact_additional_validation_rankings_v21').replace('actual_optimization_fast_runtime_handoff_v79','actual_optimization_fast_runtime_handoff_v81')
    text=text.replace("for name in ('Frontier233171_complete233_family_v2_20261010','Frontier133172_complete133_family_v2_20261010'):","for name in ('Frontier233171_complete233_family_v2_20261010','Frontier133172_complete133_family_v2_20261010','StockEmbedding173_complete36_family_v3_20261010','actual_stock_rank_embedding_own_training_queue_v2_20261010'):")
    text=text.replace("('StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',17)","('StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',17),('StockRankEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',17)")
    p=A/'monitor_fast_optimization_v49_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_fast_optimization_progress_v49_20261010',p.name,[],{str(p):sha(p)})
    create(A/'actual_fast_optimization_progress_activation_v49_20261010.json',row)
    while not (A/'optimization_live_progress_v49_20261010.json').exists():
        assert owned(row);time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v48_20261010/native_launch.json'),'Successor49 records actual stock173 and centered-rank GPU/scoring queues; no scientific worker changed.')
    prototype=A/'publish_StockEmbedding173_actual_complete_pipeline_preparation_v35_20261010.py';text=prototype.read_text(encoding='utf8')
    begin=text.index('    from prepare_stock_embedding173_full_registry_sources');end=text.index('    import publish_classifier_consensus_workflows',begin)
    files=[p,A/'prepare_stock_rank_embedding_own_sources_v1_20261010.py',A/'activate_stock_rank_embedding_checkpoint_yield_training_v2_20261010.py',A/'stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json',A/'stock_rank_embedding_actual_priority173_runtime_admission_v2_20261010.json',A/'stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json',A/'actual_stock_rank_embedding_own_training_queue_activation_v2_20261010.json',A/'actual_stock_rank_embedding_native42_and_fast17_queue_activation_v1_20261010.json',A/'actual_stock_rank_embedding_small512_restart_location_v1_20261010.json']
    files.extend(A.glob('*stock_rank*20261010.py'))
    files.append(Path(read(A/'actual_stock_rank_embedding_small512_restart_location_v1_20261010.json')['output'])/'verification.json')
    inventory='    paths=[Path(__file__),'+','.join('Path('+repr(str(f))+')' for f in dict.fromkeys(files))+']\n'
    text=text[:begin]+inventory+text[end:]
    text=text.replace('StockEmbedding173_actual_complete_pipeline_preparation_v35','StockRankEmbedding_actual_restart_and_predeclared17_v36').replace('StockEmbedding173_actual_complete_pipeline_preparation_main_v35','StockRankEmbedding_actual_restart_and_predeclared17_main_v36')
    text=text.replace('passed_actual4_TRAIN_candidate_transform_cases_and_full5635800_winner_reconstruction_266_local_import_routes_complete36_selected14_and_full173_QA84_main_queued','passed_actual_centered_rank_restart_controls_and_predeclared17_TRAIN_screen_six_fits_full5_native42_pending')
    text=text.replace('保存股票嵌入提分方案真实5635800行训练预测逐位重建、266条本地模块路由检查，以及36比较到完整173冻结推理QA84主分支发布流程','保存股票排名目标嵌入模型真实断点恢复验证、训练来源与17项训练集评分对照；六年度训练和完整独立推理验证持续执行')
    pub=A/'publish_stock_rank_embedding_actual_sources_main_v36_20261010.py';assert not pub.exists();compile(text,str(pub),'exec');pub.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_stock_rank_embedding_actual_sources_main_v36_20261010',pub.name,[],{str(pub):sha(pub)})
    create(A/'actual_stock_rank_embedding_actual_sources_main_activation_v36_20261010.json',row)
    print({'actual_observer':49,'rank_GPU_restart_and_sources_main_publication':'started'},flush=True)
if __name__=='__main__':main()
