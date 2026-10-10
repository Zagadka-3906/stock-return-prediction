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
    routes=read(A/'complete180_registered_continuation_routes_v13_20261011.json')
    while True:
        c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');now=datetime.now(timezone(timedelta(hours=8)))
        names=list(dict.fromkeys([*[n for n,d in routes['remaining_tasks']],*routes['service_aliases'].values(),'main_publisher_reboot_v12_20261011','actual_user_stop1100_reboot_guard_v2_20261011','actual_reboot_routes_protected37_capsules_main_v1_20261011','actual_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011','actual_mixed_horizon49_and_registered13_sources_main_v1_20261011','actual_rank5_rank20_after175_near_pure49_screen_v1_20261011','actual_rank20_short_long_after175_mixed_window49_screen_v1_20261011','actual_rank5_rank20_mixed_selected_native14_v1_20261011','actual_additional_cached_mixed_ensembles_stages_main_v1_20261011','actual_three_cached_mixed149_after188_normalization_v1_20261011','actual_three_cached_mixed149_selected_native14_v1_20261011','actual_three_cached_mixed149_sources_main_v1_20261011','MixedObjectiveWindow189_complete149_family_v3_20261011','actual_MixedObjectiveWindow189_sources_main_v2_20261011','actual_three_cached_mixed149_after186_normalization_v1_20261011','actual_three_cached_mixed149_wait_bridge_sources_main_v1_20261011','actual_MixedObjectiveWindow189_sources_main_v3_20261011','actual_rank5_rank20_after175_near_protected37_screen_v1_20261011','actual_rank5_rank20_near_protected_selected_native14_v1_20261011','actual_near_protected37_stages_main_v1_20261011','actual_shared_immutable_snapshot_actual181_payload_controls_v2_20261011','actual_shared_immutable_ranking_loader_benchmark_sources_main_v1_20261011','actual_near_protected39_after189_normalization_v1_20261011','actual_near_protected39_selected_native14_v1_20261011','MixedProtected190_complete39_family_v1_20261011','actual_MixedProtected190_sources_main_v1_20261011','actual_closed_profiles_byte_preserving_NTFS_compression_v1_20261011']))
        services={n:status(n) for n in names};rounds={}
        for n in range(175,191):
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
        delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')
        state={'status':'observing_actual_post_reboot_continuations','at_local':now.isoformat(),'observer_pid':os.getpid(),'actual_observer_version':101,'services':services,'rounds':rounds,'completed_screens':scores,'latest_verified_submission':delivery,'stop_at_local':c['stop_at_local'],'global_goal_exhaustion_proven':False,'root_index_sha256':hashlib.sha256((ROOT/'.git/index').read_bytes()).hexdigest()}
        write(A/'optimization_live_progress_v101_20261011.json',state);write(A/'actual_optimization_fast_runtime_handoff_v180_20261011.json',state)
        lines=[f"更新时间：{now.isoformat()}","本机01:24重启；新身份从已落盘模型、评分和第180轮已完成候选继续。原失败及中断记录保留。","11:00截止，已建立新停工守护，未重启旧守护。","147项缓存融合均已完成；追加37项大权重保护排序（两目标独立成熟，未新增训练），完整190工厂已建立并等待39项统一选模；保护排序37项与已完成175/189锚点共39项，第190轮QA101和17726项主榜资格等待实际回执；第189轮已接入经实际main六文件字节一致与双动态加载检查的低内存完整榜读取，实际候选及QA100仍待完成；149原生验证旧after186依赖已建立兼容入口，核实真正after188任务后才放行；三组缓存融合149项统一选模和原生14项流程已建立；完整189候选工厂已建立、正在等待实际149选模，QA100与17687项主榜资格以真实回执为准。"]
        for n,row in rounds.items():
            e=row['full_registration'];r=row['main_receipt'];lines.append(f"第{n}轮：完整登记{e['status'] if e else '待完成'}；main{r['commit'] if r and r.get('status')=='pushed_and_remote_head_verified' else '待完成'}。")
        for name,row in scores.items():lines.append(f"{name}：已评分{row['completed']}项，TRAIN最高S={row['best_S']}；完整交付资格单独核实。")
        for n,d in routes['remaining_tasks']:
            if services[n]['status']=='failed':lines.append(f"失败待修复：{n}；{services[n]['terminal'].get('failure')}")
        for name in ['optimization_live_progress_v101_20261011.md','optimization_live_progress_current_20261010.md']:
            path=A/name;tmp=path.with_suffix('.tmp');tmp.write_text('\n\n'.join(lines)+'\n',encoding='utf8');tmp.replace(path)
        if now>=datetime.fromisoformat(c['stop_at_local']) or c['status']!='optimization_active_after_explicit_manual_resume':return
        time.sleep(20)
if __name__=='__main__':main()
