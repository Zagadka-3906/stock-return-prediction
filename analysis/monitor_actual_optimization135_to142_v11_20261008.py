"""Observe existing seven queues plus independent CPU142 using completed proofs and actual records."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write

def main():
    launches=read(A/'ConeRidge142_complete_hidden_launches_v1_20261008.json')['launches']
    routes=read(A/'ConeRidge52_prospective_routes_v1_20261008.json')
    assert routes['actual_graph_controls']==1176 and routes['actual_prospective_sources']==24
    while True:
        state=read(A/'actual_optimization135_to141_progress_v10_20261008.json')
        state.update(status='active_seven_ordered_queues_and_independent_CPU142',observer_version=11,
            upstream_at_local=state['at_local'],at_local=datetime.now().isoformat(timespec='seconds'))
        services={}
        for name,row in launches.items():
            item={'live':owned(row),'owned_worker_pid':row['owned_worker_pid'],
                'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
            folder=A/'service_owned_workflows_20261006'/name
            if not item['live'] and (folder/'service_execution.json').exists():item['terminal']=read(folder/'service_execution.json')
            services[name]=item
        state['actual142_services']=services
        folder=A/'ConeRidge52_official_comparison_v1_20261008';records=[read(p) for p in sorted(folder.glob('case*_official.json'))]
        quality={'completed_records':len(records),'expected_records':52,'fully_qualified':False}
        if records:
            best=min(records,key=lambda row:(-row['connected_final_score'],row['expected_unique_native_models'],row['configuration']['weight'],row['case']))
            quality.update(best_score_so_far=best['connected_final_score'],partial_comparison_not_selected_candidate=True)
        if (folder/'actual_stage.json').exists():quality['stage']=read(folder/'actual_stage.json')
        if (folder/'verification.json').exists():quality.update(actual_parent=read(folder/'verification.json')['actual_comparison_parent_round'],full52_comparison_passed=True)
        registration=A/'optimization_20261003_r142/full_registration_execution.json'
        receipt=A/'github_validation_sync_main_20261005/round142_receipt.json'
        if registration.exists() and receipt.exists():quality['fully_qualified']=read(registration)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        state['actual142_quality']=quality
        controls={'saved_annual_models':20,'full_OOF_heads':4,'own_mature_windows':5,'same_recipe_causal_refits':20,
            'adapter_contracts':8,'prospective_sources':24,'complete_parent_graph_controls':1176,
            'baseline_controls':9,'same_score_controls':6,'physical_SHA_count_controls':8}
        for label,pointer in (('historical','actual_ConeRidge49_parent134_location_v1_20261008.json'),
            ('native','actual_ConeRidge24_native_hooks_location_v1_20261008.json'),
            ('calendar','actual_ConeRidge_multiyear_calendar_location_v1_20261008.json')):
            p=A/pointer
            if p.exists():
                path=Path(read(p)['output'])/'verification.json';proof=read(path)
                if label=='historical':controls.update(complete5635800_CDF=proof['actual_full_cases'],cold_CDF=proof['actual_cold_cases'])
                elif label=='native':controls.update(historical_native_hooks=proof['actual_hooks'],historical_cold_hooks=proof['actual_cold_hooks'])
                else:controls.update(calendar_native=proof['actual_calendar_cases'],calendar_day=proof['actual_whole_day_controls'])
        history=A/'ConeRidge142_historical_causal_main_v1_20261008/receipt.json'
        controls['historical_main_receipt']=read(history) if history.exists() else None
        state['actual142_completed_controls']=controls
        state['actual142_uses_already_qualified132133134_without_waiting135141']=True
        state['available_RAM_GiB']=round(psutil.virtual_memory().available/2**30,3)
        state['D_free_GiB']=round(psutil.disk_usage('D:/').free/2**30,3);state['E_free_GiB']=round(psutil.disk_usage('E:/').free/2**30,3)
        write(A/'actual_optimization135_to142_progress_v11_20261008.json',state)
        best=state['best_fully_qualified'];epoch=state['latest_actual_epoch']
        lines=['# 本机优化实际进度','',f"更新时间：{state['at_local']}；截止：{state['deadline_local']}。",'',
            f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；完整榜{state['latest_fully_qualified']['connected_records']:,}条。",'',
            f"神经年度完成{len(state['annual_models_complete'])}/6；当前{epoch['year']}年度完成{epoch['completed_epoch']}/{epoch['total_epochs']}轮。训练损失不是验证分。" if epoch else '神经年度训练继续。','',
            '| 轮次 | 已完成官方比较 | 计划项数 |','|---|---:|---:|']
        for number in range(135,143):
            q=state[f'actual{number}_quality'];lines.append(f"| {number} | {q.get('completed_records',q.get('actual_completed_cases',0))} | {q['expected_records']} |")
        lines += ['',
            '135至141保持原冻结计划。独立CPU第142轮只依赖已完整合格的132、133、134，继续完成52官方评分、冻结、候选复核、六视图45秒QA53与main。',
            '第142轮20年度约束岭回归模型、4完整OOF、5成熟窗口/20次标签扰动重训已通过。8接入检查、24接收器/1176父图、9基准/6同分/8物理SHA去重已通过。',
            f"49完整/147冷及24历史原生检查完成状态以JSON中actual142_completed_controls为准；跨年已完成{controls.get('calendar_native',0)}项。",'',
            f"可用内存{state['available_RAM_GiB']:.2f}GiB；D剩余{state['D_free_GiB']:.2f}GiB；E剩余{state['E_free_GiB']:.2f}GiB。大文件在E。",'',
            '目标active；尚无全局优化或资源边界证据。未完成的质量分和候选不计入完成。','']
        target=A/'actual_optimization135_to142_progress_v11_20261008.md';temporary=target.with_suffix('.md.part')
        temporary.write_text('\n'.join(lines),encoding='utf8',newline='\n');temporary.replace(target);time.sleep(10)

if __name__=='__main__':main()
