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
    jobs=['actual_stock_embedding_after170_fast17_screen_v1_20261010','actual_stock_embedding_after170_fast17_completion_main_v51_20261010','actual_stock_embedding_six_state_native42_completion_main_v50_20261010','actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_v34_20261010','actual_stock_embedding_six_state_native42_v2_20261010','actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010','actual_stock_embedding_own_training_queue_v4_20261010','actual_stock_embedding_small512_restart_v1_20261010','StockEmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_embedding_small512_bank6_v1_20261010','StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_embedding_after172_high_impact17_screen_v1_20261010','actual_stock_embedding17_completion_main_v49_20261010','actual_stock_embedding_actual_CPU_preparation_main_v32_20261010',*jobs]
    families=['StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010','StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010',*families]
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
        state['screen_progress']=summaries;state['supplementary_actual_scored_records']=len(rows)
        rows.sort(key=lambda r:(-r['S'],r['family'],r['case']))
        write(A/'high_impact_additional_validation_rankings_v18_20261010.json',{'at_local':now.isoformat(),'records':rows,'scores_from_actual_training_only_official_capsules':True,'full_board_authoritative_directory':str(A/'all_model_ranking_qa')})
        write(A/'optimization_live_progress_v47_20261010.json',state);write(A/'actual_optimization_fast_runtime_handoff_v77_20261010.json',state)
        best=state['best_fully_qualified'];lines=[f"更新时间：{now.isoformat()}",f"截止：{control['stop_at_local']}",f"已完全验证最佳：第{best['selected_round']}轮，S={best['official_score']:.12f}",f"GPU新股票嵌入模型：{len(state['stock_embedding_completed_models'])}/6；{state['stock_embedding_own_training']['status']}"]
        for family,total in [('Dual120Consensus_after169_high_impact193_screen_v1_20261010',193),('Cross120RecentReturn252_after169_high_impact81_screen_v1_20261010',81),('Cross120Smoothed_after170_high_impact49_screen_v1_20261010',49),('StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010',17),('StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',17)]:
            s=summaries.get(family,{});lines.append(f"{family}：{s.get('completed_cases',0)}/{total}，TRAIN候选S={s.get('best',{}).get('connected_final_score')}；完整提交资格以已验证交付指针为准。")
        for name in ('Frontier233171_complete233_family_v2_20261010','Frontier133172_complete133_family_v2_20261010'):lines.append(f"{name}：{services[name]['status']}")
        lines += [f"内存可用{state['resources']['RAM_available_GiB']:.2f}GiB；D可用{state['resources']['D_free_GiB']:.2f}GiB；E可用{state['resources']['E_free_GiB']:.2f}GiB。","所有尚未完成的评分和候选均未记为完成；新模型和缓存保存在E盘。"]
        p=A/'optimization_live_progress_v47_20261010.md';tmp=p.with_suffix('.tmp');tmp.write_text('\n\n'.join(lines)+'\n',encoding='utf8');tmp.replace(p)
        if now>=datetime.fromisoformat(control['stop_at_local']) or control['status']!='optimization_active_after_explicit_manual_resume':return
        time.sleep(20)
if __name__=='__main__':main()
