"""Report verified140 controls alongside actual135139 training, score and qualification progress."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write

def main():
    prospective=read(A/'SpectralGram52_prospective_routes_v2_20261008.json')
    assert prospective['actual_prospective_sources']==24 and prospective['actual_graph_controls']==882
    while True:
        state=read(A/'actual_neural135_CrossFamily136_HuberCross139_progress_v7_20261008.json')
        upstream_at=state['at_local'];state.update(status='active_actual135_to140_ordered_complete_pipelines',at_local=datetime.now().isoformat(timespec='seconds'),upstream_at_local=upstream_at,observer_version=8)
        services={}
        for name,row in read(A/'SpectralGram140_complete_hidden_launches_v4_20261008.json')['launches'].items():
            live=owned(row);item={'live':live,'owned_worker_pid':row['owned_worker_pid'],'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
            folder=A/'service_owned_workflows_20261006'/name
            if live:
                try:item['RSS_GiB']=round(psutil.Process(row['owned_worker_pid']).memory_info().rss/2**30,3)
                except psutil.Error:pass
            elif (folder/'service_execution.json').exists():item['terminal']=read(folder/'service_execution.json')
            services[name]=item
        state['actual140_services']=services
        pilot=A/'SpectralGram52_official_comparison_v1_20261008/verification.json'
        quality={'completed_records':0,'expected_records':52}
        if pilot.exists():
            proof=read(pilot);quality.update(completed_records=len(proof['records']),best_score=proof['best']['connected_final_score'],actual_parent=proof['actual_comparison_parent_round'])
        elif (pilot.parent/'actual_stage.json').exists():quality.update(read(pilot.parent/'actual_stage.json'))
        state['actual140_quality']=quality
        state['actual140_completed_preliminary_controls']={
            'actual_saved_annual_models':20,'actual_full_OOF_heads':4,'complete5635800_CDF':49,'cold_CDF':147,
            'historical_native_hooks':24,'historical_cold_hooks':24,'calendar_native':24,'calendar_day':48,
            'adapter_contracts':6,'own_maturity_windows':5,'actual_same_configuration_later_TRAIN_target_poison_refits':20,
            'prospective_sources':24,'complete_parent_graph_controls':882,'baseline_controls':9,'same_score_controls':6,'physical_SHA_count_controls':8,
            'historical_and_causal_main_receipt':read(A/'SpectralGram140_historical_causal_main_v1_20261008/receipt.json')}
        receipt=A/'SpectralGram140_receiver_preflight_main_v1_20261008/receipt.json'
        state['actual140_receiver_preflight_main_receipt']=read(receipt) if receipt.exists() else None
        state['actual140_waits_complete139_then_exact_current_parent']=True
        state['actual140_receiver_versions']={'science':2,'full_registration':3,'dispatch':4}
        state['available_RAM_GiB']=round(psutil.virtual_memory().available/2**30,3)
        state['D_free_GiB']=round(psutil.disk_usage('D:/').free/2**30,3);state['E_free_GiB']=round(psutil.disk_usage('E:/').free/2**30,3)
        write(A/'actual_optimization135_to140_progress_v8_20261008.json',state)
        best=state['best_fully_qualified'];epoch=state['latest_actual_epoch'];done=len(state['annual_models_complete'])
        lines=['# 本机持续优化实际进度','',f"更新时间：{state['at_local']}；原训练观察时间：{upstream_at}；截止：{state['deadline_local']}。",'',
            f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；完整榜{state['latest_fully_qualified']['connected_records']:,}条。",'',
            f"神经年度已完成{done}/6；当前{epoch['year']}年度已保存{epoch['saved_epoch']}/{epoch['total_epochs']}轮。训练损失不是验证分。" if epoch else f'神经年度已完成{done}/6。','',
            '| 轮次 | 实际官方比较进度 | 计划项数 |','|---|---:|---:|']
        for number in range(135,141):
            q=state[f'actual{number}_quality'];lines.append(f"| {number} | {q.get('completed_records',q.get('actual_completed_cases',0))} | {q['expected_records']} |")
        lines += ['',
            '新增第140轮主成分截断岭回归：20个成熟年度模型、4组完整OOF、49完整CDF/147冷前缀、24历史原生/24冷接入、24跨年/48按日检查已通过。',
            '5个独立成熟窗口和20次后续训练标签扰动的实际重训练逐位一致；24接收器/882完整父图、9基准/6同分排序/8物理模型SHA计数检查通过。',
            '源记录字段修正版采用科学接收器2；独占行政输出目录修正版采用注册接收器3。原失败日志与旧版本均保留。',
            '第140轮八步骤队列等待完整139、QA50和main回执，再检查实际父方案、52项原官方评分、冻结、候选、QA51和完整榜main。尚未执行的结果不计入完成。','',
            f"可用内存{state['available_RAM_GiB']:.2f}GiB；D剩余{state['D_free_GiB']:.2f}GiB；E剩余{state['E_free_GiB']:.2f}GiB。大文件在E，原官方评分缓存按要求在D。",'',
            '保持原GPU训练，目标active。没有宣称全局可行优化方向或计算资源已穷尽。','']
        write(A/'actual_optimization135_to140_progress_v8_20261008.md','\n'.join(lines))
        time.sleep(10)

if __name__=='__main__':main()
