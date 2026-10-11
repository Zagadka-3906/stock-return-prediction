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
    routes=read(A/'reboot_complete_candidate_routes_v11_20261011.json')
    while True:
        c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');now=datetime.now(timezone(timedelta(hours=8)))
        names=list(dict.fromkeys([*[n for n,d in routes['remaining_tasks']],*routes['service_aliases'].values(),'main_publisher_reboot_v12_20261011','actual_user_stop1100_reboot_guard_v2_20261011','actual_reboot_routes_protected37_capsules_main_v1_20261011']))
        services={n:status(n) for n in names};rounds={}
        for n in range(175,189):
            receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json';execution=A/f'optimization_20261003_r{n}/full_registration_execution.json'
            rounds[n]={'full_registration':read(execution) if execution.exists() else None,'main_receipt':read(receipt) if receipt.exists() else None}
        scores={}
        for name in ['StockRank20LongEmbeddingSmall512_after175_high_impact17_screen_v1_20261010','StockRank20LongEmbeddingSmall512_after175_large_allocation29_screen_v1_20261010','StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011']:
            p=Path('E:/赛题五_本机临时')/name/'verification.json';d=read(p);scores[name]={'completed':len(d['records']),'best_S':d['best']['connected_final_score'],'submission_qualified':False}
        delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')
        state={'status':'observing_actual_post_reboot_continuations','at_local':now.isoformat(),'observer_pid':os.getpid(),'actual_observer_version':94,'services':services,'rounds':rounds,'completed_screens':scores,'latest_verified_submission':delivery,'stop_at_local':c['stop_at_local'],'global_goal_exhaustion_proven':False,'root_index_sha256':hashlib.sha256((ROOT/'.git/index').read_bytes()).hexdigest()}
        write(A/'optimization_live_progress_v94_20261011.json',state);write(A/'actual_optimization_fast_runtime_handoff_v165_20261011.json',state)
        lines=[f"更新时间：{now.isoformat()}","本机01:24重启；新身份从已落盘模型、评分和第180轮已完成候选继续。原失败及中断记录保留。","11:00截止，已建立新停工守护，未重启旧守护。"]
        for n,row in rounds.items():
            e=row['full_registration'];r=row['main_receipt'];lines.append(f"第{n}轮：完整登记{e['status'] if e else '待完成'}；main{r['commit'] if r and r.get('status')=='pushed_and_remote_head_verified' else '待完成'}。")
        for name,row in scores.items():lines.append(f"{name}：已评分{row['completed']}项，TRAIN最高S={row['best_S']}；完整交付资格单独核实。")
        for n,d in routes['remaining_tasks']:
            if services[n]['status']=='failed':lines.append(f"失败待修复：{n}；{services[n]['terminal'].get('failure')}")
        for name in ['optimization_live_progress_v94_20261011.md','optimization_live_progress_current_20261010.md']:
            path=A/name;tmp=path.with_suffix('.tmp');tmp.write_text('\n\n'.join(lines)+'\n',encoding='utf8');tmp.replace(path)
        if now>=datetime.fromisoformat(c['stop_at_local']) or c['status']!='optimization_active_after_explicit_manual_resume':return
        time.sleep(20)
if __name__=='__main__':main()
