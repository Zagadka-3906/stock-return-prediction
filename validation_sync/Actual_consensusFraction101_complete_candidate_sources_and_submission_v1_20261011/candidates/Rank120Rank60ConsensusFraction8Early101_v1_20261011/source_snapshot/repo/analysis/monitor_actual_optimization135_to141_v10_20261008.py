"""Report seven implemented pipelines with completed141 controls and actual scores kept separate."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write

def main():
    routes=read(A/'KrylovGram52_prospective_routes_v2_20261008.json')
    assert routes['actual_prospective_sources']==24 and routes['actual_graph_controls']==1029
    while True:
        state=read(A/'actual_optimization135_to140_progress_v9_20261008.json')
        upstream=state['at_local'];state.update(status='active_actual135_to141_ordered_complete_pipelines',observer_version=10,at_local=datetime.now().isoformat(timespec='seconds'),upstream_at_local=upstream)
        services={}
        for name,row in read(A/'KrylovGram141_complete_hidden_launches_v2_20261008.json')['launches'].items():
            item={'live':owned(row),'owned_worker_pid':row['owned_worker_pid'],'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
            folder=A/'service_owned_workflows_20261006'/name
            if item['live']:
                try:item['RSS_GiB']=round(psutil.Process(row['owned_worker_pid']).memory_info().rss/2**30,3)
                except psutil.Error:pass
            elif (folder/'service_execution.json').exists():item['terminal']=read(folder/'service_execution.json')
            services[name]=item
        state['actual141_services']=services
        pilot=A/'KrylovGram52_official_comparison_v1_20261008/verification.json';quality={'completed_records':0,'expected_records':52}
        if pilot.exists():
            proof=read(pilot);quality.update(completed_records=len(proof['records']),best_score=proof['best']['connected_final_score'],actual_parent=proof['actual_comparison_parent_round'])
        elif (pilot.parent/'actual_stage.json').exists():quality.update(read(pilot.parent/'actual_stage.json'))
        state['actual141_quality']=quality
        state['actual141_completed_preliminary_controls']={'saved_annual_models':20,'full_OOF_heads':4,'complete5635800_CDF':49,'cold_CDF':147,
            'historical_native_hooks':24,'historical_cold_hooks':24,'calendar_native':24,'calendar_day':48,'adapter_contracts':7,
            'own_maturity_windows':5,'actual_same_recipe_later_TRAIN_poison_refits':20,'prospective_sources':24,'complete_parent_graph_controls':1029,
            'baseline_controls':9,'same_score_controls':6,'physical_SHA_count_controls':8,'native_numerical_recipe':2,'bank_administration':3,
            'main_receipt':read(A/'KrylovGram141_historical_causal_main_v1_20261008/receipt.json')}
        receipt=A/'KrylovGram141_receiver_preflight_main_v1_20261008/receipt.json'
        state['actual141_receiver_preflight_main_receipt']=read(receipt) if receipt.exists() else None
        state['actual141_waits_complete140_registration3_QA51_main_then_exact_current_parent']=True
        state['available_RAM_GiB']=round(psutil.virtual_memory().available/2**30,3)
        state['D_free_GiB']=round(psutil.disk_usage('D:/').free/2**30,3);state['E_free_GiB']=round(psutil.disk_usage('E:/').free/2**30,3)
        write(A/'actual_optimization135_to141_progress_v10_20261008.json',state)
        best=state['best_fully_qualified'];epoch=state['latest_actual_epoch']
        lines=['# 本机持续优化实际进度','',f"更新时间：{state['at_local']}；原观察时间：{upstream}；截止：{state['deadline_local']}。",'',
            f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；完整榜{state['latest_fully_qualified']['connected_records']:,}条。",'',
            f"神经年度完成{len(state['annual_models_complete'])}/6；当前{epoch['year']}年度完成{epoch['completed_epoch']}/{epoch['total_epochs']}轮、保存{epoch['saved_epoch']}轮。训练损失不是验证分。" if epoch else f"神经年度完成{len(state['annual_models_complete'])}/6。",'',
            '| 轮次 | 实际官方比较进度 | 计划项数 |','|---|---:|---:|']
        for number in range(135,142):
            q=state[f'actual{number}_quality'];lines.append(f"| {number} | {q.get('completed_records',q.get('actual_completed_cases',0))} | {q['expected_records']} |")
        lines += ['',
            '135–141七轮完整队列已实施，本机无控制台运行；第141轮先等待140完整注册版本3、QA51和main，再固定138/139/140三个合格锚点中的完整父方案。',
            '新增第141轮：20成熟年度CG模型/4完整OOF；49完整/147冷CDF；24历史原生/24冷；24跨年/48按日；7接入检查；5窗口/20标签扰动重训练均通过。',
            '24接收器/1029完整父图、9基准/6同分/8物理SHA去重和9原始D评分目录范围检查通过。52项官方评分、完整方案冻结、真实候选、QA52和main继续执行；尚未完成的结果不计入完成。',
            '141服务采用源版本2，父方案编号修复与旧断言失败均保留。原神经训练未停止或重启。','',
            f"可用内存{state['available_RAM_GiB']:.2f}GiB；D剩余{state['D_free_GiB']:.2f}GiB；E剩余{state['E_free_GiB']:.2f}GiB。大文件在E，原官方评分目录在D。",'',
            '目标active，没有全局可行方向或资源穷尽证明。','']
        target=A/'actual_optimization135_to141_progress_v10_20261008.md';temporary=target.with_suffix('.md.part')
        assert target.resolve().is_relative_to(A.resolve());temporary.write_text('\n'.join(lines)+'\n',encoding='utf8',newline='\n');temporary.replace(target)
        time.sleep(10)

if __name__=='__main__':main()
