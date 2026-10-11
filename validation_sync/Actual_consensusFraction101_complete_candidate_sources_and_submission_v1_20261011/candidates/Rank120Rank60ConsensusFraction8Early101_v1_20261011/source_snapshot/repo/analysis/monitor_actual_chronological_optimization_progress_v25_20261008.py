"""Compact actual score/qualification monitor for the recovered chronological pipeline."""
from pathlib import Path
import argparse,json,os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
COMPARISONS={136:('CrossFamily94',94,5),137:('Huber52',52,14),138:('BF16reverse40',40,14),139:('HuberCrossFamily112',112,18),140:('SpectralGram52',52,18),141:('KrylovGram52',52,18)}
def status(name):
    folder=A/'service_owned_workflows_20261006'/name
    if (folder/'service_execution.json').exists():return read(folder/'service_execution.json')
    if (folder/'native_launch.json').exists():
        launch=read(folder/'native_launch.json');return {'status':'running' if owned(launch) else 'ownership_not_yet_reconciled','worker':launch['owned_worker_pid']}
    return {'status':'not_started'}
def write(path,data):
    path=Path(path);temporary=path.with_name(path.name+f'.{os.getpid()}.tmp');temporary.write_text(data,encoding='utf8');os.replace(temporary,path)
def snapshot():
    import psutil
    qualified=[]
    for directory in A.glob('optimization_20261003_r*'):
        suffix=directory.name.removeprefix('optimization_20261003_r')
        if not suffix.isdecimal():continue
        number=int(suffix);full=directory/'full_registration_execution.json';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        if not all(p.is_file() for p in (full,receipt,directory/'calibrated_csv_official.json',candidate/'verification.json')):continue
        if read(full)['status']!='passed' or read(receipt)['status']!='pushed_and_remote_head_verified' or read(candidate/'verification.json')['status']!='passed':continue
        metrics=read(directory/'calibrated_csv_official.json')['metrics'];models=read(candidate/'verification.json')['models']
        qualified.append({'round':number,'score':metrics['final_score'],'unique_models':len({row['sha256'] for row in models.values()}),'main_commit':read(receipt)['commit']})
    assert qualified
    best=min(qualified,key=lambda row:(-row['score'],row['unique_models'],row['round']))
    pipeline={}
    for number,(prefix,count,version) in COMPARISONS.items():
        folder=A/f'{prefix}_official_comparison_v1_20261008'
        row={'expected_cases':count,'quality':status(f'{prefix}_official_comparison_v{version}_20261008'),
            'controls_main':status(f'{prefix}_controls_main_publication_v{version}_20261008'),
            'scores_main':status(f'{prefix}_scores_main_publication_v{version}_20261008'),
            'selected_candidate':status(f'{prefix}_selected_candidate_preparation_v{version}_20261008'),
            'candidate_sealing':status(f'{prefix}_selected_candidate_sealing_v{version}_20261008'),
            'full_registration':status(f'{prefix}_round{number}_full_registration_v{6 if number==136 else version}_20261008')}
        if number==138:
            row.update(scores_main=status('exact138_connected_API_publication_reconciliation_v2_20261008'),selected_candidate=status('BF16reverse40_selected_candidate_preparation_v17_20261008'),candidate_sealing=status('BF16reverse40_selected_candidate_sealing_v17_20261008'),full_registration=status('BF16reverse40_round138_full_registration_v17_20261008'))
        if (folder/'verification.json').exists():
            proof=read(folder/'verification.json');row.update(completed_cases=len(proof['records']),scoring_winner={'case':proof['best']['case'],'score':proof['best']['connected_final_score'],'configuration':proof['best']['configuration']},scoring_winner_is_not_a_full_qualification=True)
        elif (folder/'actual_stage.json').exists():
            progress=read(folder/'actual_stage.json');row['actual_scoring_stage']=progress;row['completed_cases']=progress.get('actual_completed_cases',0)
        else:row['completed_cases']=0
        pipeline[str(number)]=row
    state={'status':'actual_chronological_optimization_active','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'deadline_local':'2026-10-10T23:59:00+08:00','best_fully_qualified':best,'pipeline':pipeline,
        'fresh18_three_round_full_prospective_controls':status('pending139to141_complete_prospective_controls_v18_20261008'),
        'fresh18_chronological_dispatch':status('pending139to141_chronological_dispatch_v18_20261008'),
        'available_memory_GiB':psutil.virtual_memory().available/2**30,
        'free_storage_GiB':{d:psutil.disk_usage(d+':/').free/2**30 for d in ('D','E')},
        'optimization_exhaustion_proven':False,'new_official_scores_by_observer':0,'test_labels_read':False}
    fine=Path('E:/赛题五_本机临时/CrossFamilyFine121_parent134_historical_v1_20261008')
    state['fine145_frontier']={'native30_controls':status('CrossFamilyFine30_actual_native_historical_controls_v1_20261008'),'full121_controls':status('CrossFamilyFine121_actual_full_historical_controls_v1_20261008'),'actual_full_control_records':len(list(fine.glob('case*.json'))),'expected_full_control_records_including_identity':121,'synthetic120_controls_completed':(fine/'synthetic120_controls.json').is_file(),'quality_case_count_planned':125,'quality_scoring_not_admitted_or_started':True,'new_official_scores':0,'new_native_fits':0,'source_receivers_and_prospective_controls_still_required':True}
    state['actual138_fine145_controls_main_publication']=status('actual138_fine145_historical_controls_main_publication_v25_20261008')
    write(A/'optimization_live_progress_v25_20261008.json',json.dumps(state,ensure_ascii=False,indent=2)+'\n')
    text=f"# 赛题五实际优化进度\n\n更新时间：{state['at_local']}。截止：10月10日23:59。\n\n完全通过评分、候选检查、完整榜和 main 同步的最佳为第{best['round']}轮，S={best['score']:.12f}，{best['unique_models']}个物理模型。\n\n"
    text+='\n'.join(f"- 第{n}轮：官方评分{r['completed_cases']}/{r['expected_cases']}，评分任务{r['quality']['status']}，候选准备{r['selected_candidate']['status']}，完整验证{r['full_registration']['status']}。" for n,r in pipeline.items())
    text+=f"\n\n可用内存{state['available_memory_GiB']:.2f} GiB；D/E可用{state['free_storage_GiB']['D']:.2f}/{state['free_storage_GiB']['E']:.2f} GiB。试验最高分需完成全部候选检查才可采用。未证明可行优化方向或计算资源穷尽。\n"
    text+=f"\n细权重第145轮：原生30项控制{state['fine145_frontier']['native30_controls']['status']}，完整控制{state['fine145_frontier']['actual_full_control_records']}/121，125项官方评分尚未准入或开始。\n"
    write(A/'optimization_live_progress_v25_20261008.md',text)
    return state
def main(once):
    while True:
        state=snapshot()
        if once:print(json.dumps({'at_local':state['at_local'],'best':state['best_fully_qualified'],'pipeline':{n:{'completed':r['completed_cases'],'quality':r['quality']['status'],'full':r['full_registration']['status']} for n,r in state['pipeline'].items()}},ensure_ascii=False),flush=True);return
        time.sleep(45)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--once',action='store_true');main(parser.parse_args().once)
