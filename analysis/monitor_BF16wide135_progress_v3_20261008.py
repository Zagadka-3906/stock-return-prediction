"""Lightweight live progress for the full neural and135 workflows; scientific workers remain untouched."""
from pathlib import Path
from datetime import datetime
import json,re,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write


def update():
    now=datetime.now().isoformat(timespec='seconds')
    launches=read(A/'BF16wide135_complete_hidden_launches_v3_20261008.json')['launches']
    names=['actual_neural_BF16_micro8192_bank6_v2_20261008','BF16_independent_full5_GPU_controls_v2_20261008',
        'BF16_rank_CDF_actual_full37_controls_v1_20261008','BF16_complete_parent_actual_historical_native_hook3_v1_20261008',
        'actual_BF16wide135_receiver_preflight_main_publication_v1_20261008',*launches]
    services={}
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');live=owned(row)
        result={'live':live,'owned_worker_pid':row['owned_worker_pid'],'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
        if live:
            try:result['RSS_GiB']=round(psutil.Process(row['owned_worker_pid']).memory_info().rss/2**30,3)
            except psutil.Error:pass
        elif (folder/'service_execution.json').exists():result['terminal']=read(folder/'service_execution.json')
        services[name]=result
    qualified=[]
    for number in range(128,146):
        folder=A/f'optimization_20261003_r{number}';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        if not receipt.exists() or not (folder/'full_registration_execution.json').exists():continue
        if read(folder/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified':
            info=read(receipt);qualified.append({'round':number,'official_score':info['official_score'],'connected_records':info['connected_records'],'main_commit':info['commit']})
    best=min(qualified,key=lambda r:(-r['official_score'],r['round']));latest=max(qualified,key=lambda r:r['round'])
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    annual=[]
    for year in range(2020,2026):
        path=bank/str(year)/'info.json'
        if path.exists():
            info=read(path);annual.append({'year':year,'status':info['status'],'model_sha256':info['model_sha256'],
                'training_rows':info['training_meta']['rows'],'full_annual_reload_bits_exact':info.get('actual_full_annual_reload_prediction_bits_exact'),
                'cold80_bits_exact':info.get('actual_cold80_prefix_bits_exact')})
    stage=read(bank/'actual_stage.json') if (bank/'actual_stage.json').exists() else None
    log=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/stdout.log'
    with log.open('rb') as stream:
        stream.seek(max(0,log.stat().st_size-32768));tail=stream.read().decode('utf8',errors='replace')
    starts=list(re.finditer(r'Actual new BF16 annual (\d+):',tail));epoch=None
    if starts:
        year=int(starts[-1].group(1));tail=tail[starts[-1].end():]
        completed=re.findall(r'BF16 micro8192 epoch (\d+)/(\d+) loss=([\d.eE+-]+) fit_seconds=([\d.]+)',tail)
        saved=re.findall(r'durable_epoch=(\d+) checkpoint_seconds=([\d.]+)',tail)
        if completed:
            n,total,loss,elapsed=completed[-1]
            epoch={'year':year,'completed_epoch':int(n),'total_epochs':int(total),'saved_epoch':int(saved[-1][0]) if saved else None,
                'fit_seconds':float(elapsed),'training_loss':float(loss),'training_loss_is_not_validation_score':True}
    pilot=A/'BF16wide40_official_comparison_v1_20261008/verification.json'
    quality={'completed_records':0,'expected_records':40}
    if pilot.exists():
        proof=read(pilot);quality={'completed_records':len(proof['records']),'expected_records':40,'best_score':proof['best']['connected_final_score'],
            'full135_qualified':any(r['round']==135 for r in qualified)}
    else:
        progress=pilot.parent/'actual_stage.json'
        if progress.exists():quality.update(read(progress))
    deadline=read(A/'actual_user_submission_deadline_and_priority_20261008.json')['deadline_local']
    state={'status':'active_actual_owned_training_and_complete135_ordered_workflows','at_local':now,'deadline_local':deadline,
        'best_fully_qualified':best,'latest_fully_qualified':latest,'annual_models_complete':annual,'expected_annual_models':6,
        'actual_training_stage':stage,'latest_actual_epoch':epoch,'actual135_quality':quality,'actual_services':services,
        'available_RAM_GiB':round(psutil.virtual_memory().available/2**30,3),'D_free_GiB':round(psutil.disk_usage('D:/').free/2**30,3),
        'E_free_GiB':round(psutil.disk_usage('E:/').free/2**30,3),'selected_new_scheme_future_inference_required_if_it_wins':True,
        'global_boundary_or_goal_completion_not_claimed':True,'test_labels_read':False}
    write(A/'actual_BF16wide135_progress_v3_20261008.json',state)
    lines=['# 当前优化进度','',f'更新时间：{now}；截止时间：{deadline}。','',
        f"完整合格最佳：第{best['round']}轮，官方连续验证S={best['official_score']:.12f}；完整榜{latest['connected_records']:,}条。",'',
        f'新宽网络：已完成{len(annual)}/6个年度；已完成年度：'+','.join(str(r['year']) for r in annual)+'。','',
        '当前训练：'+json.dumps(stage,ensure_ascii=False),'', '当前周期：'+json.dumps(epoch,ensure_ascii=False),'',
        '第135轮评分：'+json.dumps(quality,ensure_ascii=False),'',
        '后续顺序：六年度训练 → 五年度独立GPU推理 → 37项CDF/111冷前缀 → 三组历史原生检查 → 40项官方评分 → 选中方案冻结与推理 → 完整榜QA46 → GitHub main。','',
        '实际服务：']
    for name,value in services.items():lines.append(f"- {name}：{'运行或等待依赖' if value['live'] else value.get('terminal',{}).get('status','无终态记录')}，PID {value['owned_worker_pid']}，窗口句柄{value['actual_native_console_handle']}。")
    lines += ['',f"可用空间：D盘{state['D_free_GiB']:.2f} GiB；E盘{state['E_free_GiB']:.2f} GiB。",'',
        '尚未证明全局优化穷尽；训练损失不能替代验证分数。']
    target=A/'actual_BF16wide135_progress_v3_20261008.md';temporary=target.with_suffix('.md.part')
    temporary.write_text('\n'.join(lines)+'\n',encoding='utf8',newline='\n');temporary.replace(target)


def main():
    while True:update();time.sleep(10)


if __name__=='__main__':main()
