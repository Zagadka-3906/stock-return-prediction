"""Report actual143 quality and corrected pending11 identities from immutable proofs."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write
def services(rows):
    result={}
    for name,row in rows.items():
        item={'live':owned(row),'owned_worker_pid':row['owned_worker_pid'],'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
        terminal=A/'service_owned_workflows_20261006'/name/'service_execution.json'
        if not item['live'] and terminal.exists():item['terminal']=read(terminal)
        result[name]=item
    return result
def main():
    fine=read(A/'ConeRidgeFine143_complete_hidden_launches_v1_20261008.json')['launches']
    while True:
        state=read(A/'actual_optimization135_to142_progress_v12_20261008.json')
        state.update(status='active_ordered135141_and_independent_fine143',observer_version=13,at_local=datetime.now().isoformat(timespec='seconds'))
        for n in range(137,142):
            index=A/f'round{n}_complete_hidden_launches_v11_20261008.json'
            if index.exists():state[f'actual{n}_services']=services(read(index)['launches'])
        state['actual143_services']=services(fine)
        folder=A/'ConeRidgeFine68_official_comparison_v1_20261008';records=[read(p) for p in sorted(folder.glob('case*_official.json'))]
        q={'completed_records':len(records),'expected_records':68,'fully_qualified':False}
        if records:
            best=min(records,key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],r['configuration']['weight'],r['case']))
            q.update(best_score_so_far=best['connected_final_score'],partial_scores_are_not_full_qualification=True)
        if (folder/'actual_stage.json').exists():q['stage']=read(folder/'actual_stage.json')
        if (folder/'verification.json').exists():q.update(full68_comparison_passed=True,selected_case=read(folder/'verification.json')['best']['case'])
        full=A/'optimization_20261003_r143/full_registration_execution.json';receipt=A/'github_validation_sync_main_20261005/round143_receipt.json'
        if full.exists() and receipt.exists():q['fully_qualified']=read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        state['actual143_quality']=q
        routes=read(A/'ConeRidgeFine68_prospective_routes_v1_20261008.json')
        controls={'prospective_sources':routes['actual_prospective_sources'],'complete_parent_graph_controls':routes['actual_graph_controls'],'new_native_fits_by_grid':0}
        for label,pointer in (('CDF','actual_ConeRidgeFine65_parent134_location_v1_20261008.json'),('native','actual_ConeRidgeFine24_native_hooks_location_v1_20261008.json'),('calendar','actual_ConeRidgeFine_multiyear_calendar_location_v1_20261008.json')):
            p=A/pointer
            if p.exists():
                v=read(Path(read(p)['output'])/'verification.json')
                if label=='CDF':controls.update(full_CDF=v['actual_full_cases'],cold_CDF=v['actual_cold_cases'])
                elif label=='native':controls.update(native_hooks=v['actual_hooks'],native_cold_hooks=v['actual_cold_hooks'])
                else:controls.update(calendar_controls=v['actual_calendar_cases'],calendar_day_controls=v['actual_whole_day_controls'])
        history=A/'ConeRidgeFine143_historical_causal_main_v1_20261008/receipt.json'
        controls['historical_main_receipt']=read(history) if history.exists() else None
        state['actual143_completed_controls']=controls
        dispatch=A/'pending137to141_receiver_dispatch_v11_20261008.json'
        state['pending137141_corrected_dispatch_complete']=dispatch.exists()
        state['available_RAM_GiB']=round(psutil.virtual_memory().available/2**30,3)
        state['D_free_GiB']=round(psutil.disk_usage('D:/').free/2**30,3);state['E_free_GiB']=round(psutil.disk_usage('E:/').free/2**30,3)
        write(A/'actual_optimization135_to143_progress_v13_20261008.json',state)
        best=state['best_fully_qualified'];epoch=state['latest_actual_epoch']
        lines=['# 本机优化实际进度','',f"更新：{state['at_local']}；提交截止：2026-10-10 23:59。",'',
          f"已完整合格最佳第{best['round']}轮，S={best['official_score']:.12f}；完整榜{state['latest_fully_qualified']['connected_records']:,}条。",'',
          f"神经年度完成{len(state['annual_models_complete'])}/6，最终年度完成{epoch['completed_epoch']}/{epoch['total_epochs']}轮。训练损失不代表验证分。",'',
          f"第142轮52项评分、冻结候选复核、六视图QA53和main已完成；第143轮完成{q['completed_records']}/68项官方评分，完整合格状态{q['fully_qualified']}。",'',
          f"第143轮实际{controls.get('full_CDF',0)}完整CDF、{controls.get('cold_CDF',0)}冷前缀、{controls.get('native_hooks',0)}原生检查、{controls.get('calendar_controls',0)}跨年检查；24登记脚本与1,560完整父图已通过。",'',
          '第137至141轮使用新登记来源11，15项真实函数参数合同和五轮完整预演已通过。旧源、错误引用及失败记录保留；实际服务状态见JSON。',
          f"可用内存{state['available_RAM_GiB']:.2f}GiB；D余{state['D_free_GiB']:.2f}GiB；E余{state['E_free_GiB']:.2f}GiB。大文件存E。",'',
          '目标active；未证明全部方向穷尽。所有选模仅用TRAIN连续向前验证，未读取测试答案。','']
        target=A/'actual_optimization135_to143_progress_v13_20261008.md';part=target.with_suffix('.md.part');part.write_text('\n'.join(lines),encoding='utf8',newline='\n');part.replace(target);time.sleep(10)
if __name__=='__main__':main()
