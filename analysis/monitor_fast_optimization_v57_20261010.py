"""Actual job states, current qualified delivery, concise high-impact progress."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,ast,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from scheduled_user_pause_20261007 import write
def inventories():
    tree=ast.parse((A/'monitor_fast_optimization_v44_20261010.py').read_text(encoding='utf8'))
    lists={}
    for node in ast.walk(tree):
        if isinstance(node,ast.For) and isinstance(node.target,ast.Name) and node.target.id in ('name','family') and isinstance(node.iter,ast.List):lists[node.target.id]=ast.literal_eval(node.iter)
    return lists['name'],lists['family']
def main():
    import psutil
    jobs,families=inventories()
    jobs=['actual_stock_embedding_after170_fast17_screen_v2_20261010','actual_stock_embedding_after170_completion_main_v53_20261010','actual_stock_embedding_six_state_native42_completion_main_v50_20261010','actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_v34_20261010','actual_stock_embedding_six_state_native42_v2_20261010','actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010','actual_stock_embedding_own_training_queue_v4_20261010','actual_stock_embedding_small512_restart_v1_20261010','StockEmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_embedding_small512_bank6_v1_20261010','StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_embedding_after172_high_impact17_screen_v2_20261010','actual_stock_embedding_after172_completion_main_v52_20261010','actual_stock_embedding_actual_CPU_preparation_main_v32_20261010',*jobs]
    jobs=['StockEmbedding173_complete36_family_v3_20261010', 'actual_stock_embedding36_after172_normalization_queue_v1_20261010', 'StockEmbedding36_selected_native14_v1_20261010', 'actual_stock_rank_embedding_own_training_queue_v2_20261010', 'actual_stock_rank_embedding_small512_restart_v1_20261010', 'StockRankEmbeddingSmall512_independent_small_CPU_v1_20261009', 'actual_stock_rank_embedding_small512_bank6_v1_20261010', 'StockRankEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009', 'actual_stock_rank_embedding_native42_and_fast17_queue_v1_20261010', 'actual_stock_rank_embedding_six_state_native42_v1_20261010', 'actual_stock_rank_embedding_after170_fast17_screen_v1_20261010']+jobs
    jobs += ['actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010','actual_stock_dual_embedding_after173_completion_main_v57_20261010','actual_stock_rank_embedding_native42_completion_main_v54_20261010','actual_stock_rank_embedding_after170_completion_main_v57_20261010']
    jobs += ['actual_stock_rank_dual44_after173_normalization_v2_20261010','actual_stock_dual_embedding_actual36_native_v1_20261010','Frontier133172_complete36_family_v2_20261010']
    jobs += ['StockRankDual44_selected_native14_v1_20261010','actual_stock_dual_embedding_actual36_and_selected44_main_v39_20261010']
    jobs += ['StockRankDual174_complete44_family_v2_20261010','StockRankDual174_actual_rank_branch_TRAIN_reconstruction_v1_20261010','actual_StockRankDual174_full_pipeline_preparation_main_v40_20261010']
    jobs += ['actual_stock_top10_embedding_own_training_queue_v3_20261010', 'actual_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010', 'actual_stock_top10_embedding_small512_restart_v1_20261010', 'actual_stock_top10_embedding_small512_bank6_v1_20261010', 'StockTop10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009', 'actual_stock_top10_embedding_six_state_native42_v1_20261010', 'actual_stock_top10_embedding_after174_fast17_screen_v1_20261010', 'actual_stock_top10_embedding_native42_completion_main_v58_20261010', 'actual_stock_top10_embedding_after174_completion_main_v59_20261010', 'StockRankDual174_actual_dual_TRAIN_branch_v1_20261010']
    jobs += ['actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after174_large_allocation29_completion_main_v60_20261010']
    families=['StockTop10EmbeddingSmall512_after174_large_allocation29_screen_v1_20261010','StockTop10EmbeddingSmall512_after174_high_impact17_screen_v1_20261010','StockDualEmbedding_after173_high_impact25_screen_v1_20261010','StockRankEmbeddingSmall512_after170_high_impact17_screen_v1_20261010','StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010','StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010',*families]
    while True:
        now=datetime.now(timezone(timedelta(hours=8)));control=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
        services={}
        for name in dict.fromkeys(jobs):
            folder=A/'service_owned_workflows_20261006'/name;launch=folder/'native_launch.json';execution=folder/'service_execution.json'
            if execution.exists():services[name]=read(execution)
            elif launch.exists():
                row=read(launch);services[name]={'status':'running' if owned(row) else 'exited_without_verified_completion','worker_pid':row.get('owned_worker_pid')}
            else:services[name]={'status':'not_started'}
        state={'at_local':now.isoformat(),'deadline_local':control['stop_at_local'],'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),'services':services,'resources':{'RAM_available_GiB':psutil.virtual_memory().available/2**30,'D_free_GiB':shutil.disk_usage('D:/').free/2**30,'E_free_GiB':shutil.disk_usage('E:/').free/2**30},'stock_embedding_own_training':read(A/'stock_embedding_small512_own_training_queue_v1_20261010/state.json')}
        state['stock_embedding_completed_models']=[y for y in range(2020,2026) if Path(f'E:/赛题五_本机临时/stock_embedding_small512_BF16_bank6_v1_20261010/{y}/info.json').exists()]
        summaries={};rows=[]
        for family in dict.fromkeys(families):
            folder=Path('E:/赛题五_本机临时')/family
            if (folder/'best_so_far.json').exists():summaries[family]=read(folder/'best_so_far.json')
            for p in folder.glob('case*_official.json'):
                r=read(p);rows.append({'family':family,'case':r['case'],'S':r['connected_final_score'],'gain':r['score_gain_over_qualified_parent'],'configuration':r['configuration'],'source':str(p),'submission_qualified':False})
        top_bank=Path('E:/赛题五_本机临时/stock_top10_embedding_small512_BF16_bank6_v1_20261010')
        state['top10_classifier']={'completed_annual_models':[y for y in range(2020,2026) if (top_bank/str(y)/'info.json').exists()], 'bank_stage':read(top_bank/'actual_stage.json') if (top_bank/'actual_stage.json').exists() else None,'checkpoint_files':[{'year':y,'bytes':p.stat().st_size,'mtime':p.stat().st_mtime} for y in range(2020,2026) if (p:=top_bank/str(y)/'checkpoint.joblib').exists()], 'stage_status_is_legacy_text_not_evidence_of_waiting':True,'live_actual_worker':services.get('actual_stock_top10_embedding_small512_bank6_v1_20261010')}
        state['screen_progress']=summaries;state['supplementary_actual_scored_records']=len(rows)
        rows.sort(key=lambda r:(-r['S'],r['family'],r['case']))
        write(A/'high_impact_additional_validation_rankings_v29_20261010.json',{'at_local':now.isoformat(),'records':rows,'scores_from_actual_training_only_official_capsules':True,'full_board_authoritative_directory':str(A/'all_model_ranking_qa')})
        write(A/'optimization_live_progress_v57_20261010.json',state);write(A/'actual_optimization_fast_runtime_handoff_v97_20261010.json',state)
        best=state['best_fully_qualified'];lines=[f"更新时间：{now.isoformat()}",f"截止：{control['stop_at_local']}",f"已完全验证最佳：第{best['selected_round']}轮，S={best['official_score']:.12f}",f"GPU新股票嵌入模型：{len(state['stock_embedding_completed_models'])}/6；{state['stock_embedding_own_training']['status']}"]
        for family,total in [('Dual120Consensus_after169_high_impact193_screen_v1_20261010',193),('Cross120RecentReturn252_after169_high_impact81_screen_v1_20261010',81),('Cross120Smoothed_after170_high_impact49_screen_v1_20261010',49),('StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010',17),('StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',17),('StockRankEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',17),('StockDualEmbedding_after173_high_impact25_screen_v1_20261010',25),('StockTop10EmbeddingSmall512_after174_high_impact17_screen_v1_20261010',17)]:
            s=summaries.get(family,{});lines.append(f"{family}：{s.get('completed_cases',0)}/{total}，TRAIN候选S={s.get('best',{}).get('connected_final_score')}；完整提交资格以已验证交付指针为准。")
        lines.append(f"Top10分类：已完成年度模型{len(state['top10_classifier']['completed_annual_models'])}/6；实际训练服务{state['top10_classifier']['live_actual_worker']}。大权重29项官方评分尚待前置验证，未记为完成。")
        for name in ('Frontier233171_complete233_family_v2_20261010','Frontier133172_complete133_family_v2_20261010','StockEmbedding173_complete36_family_v3_20261010','actual_stock_rank_embedding_own_training_queue_v2_20261010','StockRankDual174_complete44_family_v2_20261010'):lines.append(f"{name}：{services[name]['status']}")
        lines += [f"内存可用{state['resources']['RAM_available_GiB']:.2f}GiB；D可用{state['resources']['D_free_GiB']:.2f}GiB；E可用{state['resources']['E_free_GiB']:.2f}GiB。","所有尚未完成的评分和候选均未记为完成；新模型和缓存保存在E盘。"]
        p=A/'optimization_live_progress_v57_20261010.md';tmp=p.with_suffix('.tmp');tmp.write_text('\n\n'.join(lines)+'\n',encoding='utf8');tmp.replace(p)
        stable=A/'optimization_live_progress_current_20261010.md';stabletmp=stable.with_suffix('.tmp');stabletmp.write_text(p.read_text(encoding='utf8'),encoding='utf8');stabletmp.replace(stable)
        if now>=datetime.fromisoformat(control['stop_at_local']) or control['status']!='optimization_active_after_explicit_manual_resume':return
        time.sleep(20)
if __name__=='__main__':main()
