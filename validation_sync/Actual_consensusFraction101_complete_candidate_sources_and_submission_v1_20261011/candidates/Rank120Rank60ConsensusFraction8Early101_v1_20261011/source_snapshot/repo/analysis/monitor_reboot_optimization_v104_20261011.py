"""Observe exact post-reboot identities, original terminal failures and actual scores."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,os,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write
def status(name):
    f=A/'service_owned_workflows_20261006'/name
    if not (f/'native_launch.json').exists():return {'status':'not_dispatched'}
    launch=read(f/'native_launch.json');terminal=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None
    live=owned(launch)
    return {'status':'running' if live else terminal['status'] if terminal else 'interrupted_without_completion','live_exact_identity':live,'worker_pid':launch['owned_worker_pid'],'terminal':terminal}
def main():
    routes=read(A/'verified4650_recovery_routes_v14_20261011.json')
    while True:
        c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');now=datetime.now(timezone(timedelta(hours=8)))
        names=list(dict.fromkeys([*[n for n,d in routes['remaining_tasks']],*routes['service_aliases'].values(),'main_publisher_reboot_v12_20261011','actual_user_stop1100_reboot_guard_v2_20261011','actual_reboot_routes_protected37_capsules_main_v1_20261011','actual_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011','actual_mixed_horizon49_and_registered13_sources_main_v1_20261011','actual_rank5_rank20_after175_near_pure49_screen_v1_20261011','actual_rank20_short_long_after175_mixed_window49_screen_v1_20261011','recovery14_actual_rank5_rank20_mixed_selected_native14_v1_20261011','actual_additional_cached_mixed_ensembles_stages_main_v1_20261011','recovery14_actual_three_cached_mixed149_after188_normalization_v1_20261011','recovery14_actual_three_cached_mixed149_selected_native14_v1_20261011','actual_three_cached_mixed149_sources_main_v1_20261011','recovery14_MixedObjectiveWindow189_complete149_family_v3_20261011','actual_MixedObjectiveWindow189_sources_main_v2_20261011','recovery14_actual_three_cached_mixed149_after188_normalization_v1_20261011','actual_three_cached_mixed149_wait_bridge_sources_main_v1_20261011','actual_MixedObjectiveWindow189_sources_main_v3_20261011','actual_rank5_rank20_after175_near_protected37_screen_v1_20261011','recovery14_actual_rank5_rank20_near_protected_selected_native14_v1_20261011','actual_near_protected37_stages_main_v1_20261011','actual_shared_immutable_snapshot_actual181_payload_controls_v2_20261011','actual_shared_immutable_ranking_loader_benchmark_sources_main_v1_20261011','recovery14_actual_near_protected39_after189_normalization_v1_20261011','recovery14_actual_near_protected39_selected_native14_v1_20261011','recovery14_MixedProtected190_complete39_family_v1_20261011','actual_MixedProtected190_sources_main_v1_20261011','actual_closed_profiles_byte_preserving_NTFS_compression_v1_20261011','actual_rank5_rank20_after175_near_refined25_screen_v1_20261011','actual_near_refined25_stages_main_v1_20261011','recovery14_actual_near_refined27_after190_normalization_v1_20261011','recovery14_actual_near_refined27_selected_native14_v1_20261011','recovery14_MixedRefined191_complete27_family_v1_20261011','actual_MixedRefined191_sources_main_v1_20261011']))
        services={n:status(n) for n in names};rounds={}
        for n in range(175,192):
            receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json';execution=A/f'optimization_20261003_r{n}/full_registration_execution.json'
            rounds[n]={'full_registration':read(execution) if execution.exists() else None,'main_receipt':read(receipt) if receipt.exists() else None}
        scores={}
        for name in ['StockRank20LongEmbeddingSmall512_after175_high_impact17_screen_v1_20261010','StockRank20LongEmbeddingSmall512_after175_large_allocation29_screen_v1_20261010','StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011']:
            p=Path('E:/赛题五_本机临时')/name/'verification.json';d=read(p);scores[name]={'completed':len(d['records']),'best_S':d['best']['connected_final_score'],'submission_qualified':False}
        mixed=Path('E:/赛题五_本机临时/StockRank5Rank20_after175_mixed_horizon49_screen_v2_20261011')
        saved=list(mixed.glob('case*_official.json'))
        scores['Rank5_Rank20_mixed_horizon49']={'completed':len(saved),'expected':49,'best_S':max((read(p)['connected_final_score'] for p in saved),default=None),'submission_qualified':False}
        for display,folder in [('Rank5_Rank20_near_pure49','Rank5Rank20_after175_near_pure49_screen_v1_20261011'),('Rank20_short_long_window49','Rank20ShortLong_after175_mixed_window49_screen_v1_20261011')]:
            path=Path('E:/赛题五_本机临时')/folder;completed=list(path.glob('case*_official.json'))
            scores[display]={'completed':len(completed),'expected':49,'best_S':max((read(p)['connected_final_score'] for p in completed),default=None),'submission_qualified':False}
        protected=Path('E:/赛题五_本机临时/Rank5Rank20_after175_near_protected37_screen_v1_20261011');actual=list(protected.glob('case*_official.json'))
        scores['Rank5_Rank20_near_protected37']={'completed':len(actual),'expected':37,'best_S':max((read(p)['connected_final_score'] for p in actual),default=None),'submission_qualified':False}
        refined=Path('E:/赛题五_本机临时/Rank5Rank20_after175_near_refined25_screen_v1_20261011');actual_refined=list(refined.glob('case*_official.json'))
        scores['Rank5_Rank20_near_refined25']={'completed':len(actual_refined),'expected':25,'best_S':max((read(p)['connected_final_score'] for p in actual_refined),default=None),'submission_qualified':False}
        delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')
        state={'status':'observing_actual_post_reboot_continuations','at_local':now.isoformat(),'observer_pid':os.getpid(),'actual_observer_version':104,'services':services,'rounds':rounds,'completed_screens':scores,'latest_verified_submission':delivery,'stop_at_local':c['stop_at_local'],'global_goal_exhaustion_proven':False,'root_index_sha256':hashlib.sha256((ROOT/'.git/index').read_bytes()).hexdigest()}
        write(A/'optimization_live_progress_v104_20261011.json',state);write(A/'actual_optimization_fast_runtime_handoff_v184_20261011.json',state)
        lines=[f"更新时间：{now.isoformat()}","11:00按用户截止要求停工；当前继续优化。","147项缓存融合及37项保护排序已完成官方评分；25项负向CDF邻近权重验证已启动。完整189/190/191流程已建立，第183轮已由新版本通过实际4650只股票的14原生/14冷启动/7拒绝检查，后续任务已切换恢复14入口；原失败记录保留。实际选模、候选推理和main状态以下列回执为准；尚未完成的父方案不记为已完成。"]
        for n,row in rounds.items():
            e=row['full_registration'];r=row['main_receipt'];lines.append(f"第{n}轮：完整登记{e['status'] if e else '待完成'}；main{r['commit'] if r and r.get('status')=='pushed_and_remote_head_verified' else '待完成'}。")
        for name,row in scores.items():lines.append(f"{name}：已评分{row['completed']}项，TRAIN最高S={row['best_S']}；完整交付资格单独核实。")
        for n,d in routes['remaining_tasks']:
            if services[n]['status']=='failed':lines.append(f"失败待修复：{n}；{services[n]['terminal'].get('failure')}")
        for name in ['optimization_live_progress_v104_20261011.md','optimization_live_progress_current_20261010.md']:
            path=A/name;tmp=path.with_suffix('.tmp');tmp.write_text('\n\n'.join(lines)+'\n',encoding='utf8');tmp.replace(path)
        if now>=datetime.fromisoformat(c['stop_at_local']) or c['status']!='optimization_active_after_explicit_manual_resume':return
        time.sleep(20)
if __name__=='__main__':main()
