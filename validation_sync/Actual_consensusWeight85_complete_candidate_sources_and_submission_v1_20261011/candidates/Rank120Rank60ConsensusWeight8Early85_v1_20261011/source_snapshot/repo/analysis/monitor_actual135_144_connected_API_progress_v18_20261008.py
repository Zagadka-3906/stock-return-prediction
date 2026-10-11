"""Report actual native/QAs/main proofs; never promote a pilot score to a qualified candidate."""
from pathlib import Path
import sys,json,time,os,argparse
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
def status(name):
    folder=A/'service_owned_workflows_20261006'/name
    if (folder/'service_execution.json').exists():return read(folder/'service_execution.json')
    if (folder/'native_launch.json').exists():
        row=read(folder/'native_launch.json');return {'status':'running' if owned(row) else 'ownership_not_yet_reconciled','pid':row['owned_worker_pid']}
    return {'status':'not_started'}
def snapshot():
    import psutil
    services=['exact135_144_connected_API_publication_reconciliation_v3_20261008','BF16wide40_selected_candidate_preparation_v6_20261008','BF16wide40_selected_candidate_sealing_v6_20261008','BF16wide40_round135_full_registration_v7_20261008','ConeRidgeAlpha100_selected_candidate_preparation_v9_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v9_20261008','ConeRidgeAlpha100_round144_full_registration_v11_20261008']
    stages={n:status(n) for n in services};scores={}
    for number,path in [(135,A/'BF16wide40_official_comparison_v1_20261008/verification.json'),(144,A/'ConeRidgeAlpha100_official_comparison_v5_20261008/verification.json')]:
        proof=read(path);scores[str(number)]={'records':len(proof['records']),'case':proof['best']['case'],'score':proof['best']['connected_final_score'],'configuration':proof['best']['configuration']}
    qualified=143
    for number in (135,144):
        proof=A/f'optimization_20261003_r{number}/full_registration_execution.json';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        if proof.exists() and receipt.exists() and read(proof)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified':
            if read(ROOT/f'candidates/optimization_20261003_r{number}/selection.json')['winner']['metrics']['final_score']>read(ROOT/f'candidates/optimization_20261003_r{qualified}/selection.json')['winner']['metrics']['final_score']:qualified=number
    requests={str(n):read(A/f'round{n}_connected_API_main_request_v1_20261008.json') if (A/f'round{n}_connected_API_main_request_v1_20261008.json').exists() else {'status':'full_native_or_QA_not_yet_ready_for_publication'} for n in (135,144)}
    state={'status':'actual_connected_API_recovery_and_candidate_QA_in_progress','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00','official_scores':scores,'best_fully_qualified_round':qualified,'best_fully_qualified_score':read(ROOT/f'candidates/optimization_20261003_r{qualified}/selection.json')['winner']['metrics']['final_score'],'stages':stages,'publication_requests':requests,'available_memory_GiB':psutil.virtual_memory().available/2**30,'free_storage_GiB':{p:psutil.disk_usage(p+':/').free/2**30 for p in ('D','E')},'score_publication_actual_main_commit':read(A/'exact135_144_connected_API_reconciliation_v3_20261008.json')['commit'],'new_quality_scores_by_recovery':0,'pilot144_not_promoted_until_full_native_sealing_QA_and_main_receipt':True,'pending136_to141_need_fresh135_gate_repair':True,'optimization_exhaustion_proven':False,'test_labels_read':False}
    path=A/'actual_optimization135_144_connected_API_progress_v18_20261008.json';temp=path.with_name(path.name+f'.{os.getpid()}.tmp');temp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(temp,path)
    text=f"# 赛题五真实进度\n\n更新时间：{state['at_local']}。截止：10月10日23:59。\n\n第135轮40项、第144轮100项官方评分已完成，140项评分已同步 main。\n\n已完成全部验证的最佳：第{qualified}轮，S={state['best_fully_qualified_score']:.12f}。第144轮试验最高 S={scores['144']['score']:.12f}，完整候选检查尚未完成时不能采用。\n\n"
    text+='\n'.join(f"- {n}：{v['status']}" for n,v in stages.items())+'\n\n'+f"可用内存：{state['available_memory_GiB']:.2f} GiB。D/E 可用空间：{state['free_storage_GiB']['D']:.2f}/{state['free_storage_GiB']['E']:.2f} GiB。大文件存 E；不读取实际测试标签；未证明优化穷尽。\n"
    path=A/'actual_optimization135_144_connected_API_progress_v18_20261008.md';temp=path.with_name(path.name+f'.{os.getpid()}.tmp');temp.write_text(text,encoding='utf8');os.replace(temp,path)
    return state
def main(once):
    while True:
        state=snapshot()
        if once:print(json.dumps({'at_local':state['at_local'],'qualified_round':state['best_fully_qualified_round'],'stages':state['stages'],'available_memory_GiB':state['available_memory_GiB']},ensure_ascii=False),flush=True);return
        time.sleep(45)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--once',action='store_true');main(p.parse_args().once)
