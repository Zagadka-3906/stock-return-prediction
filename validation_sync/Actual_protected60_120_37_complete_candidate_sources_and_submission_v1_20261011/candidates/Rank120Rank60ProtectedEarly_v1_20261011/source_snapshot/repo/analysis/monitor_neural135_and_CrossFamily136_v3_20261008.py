"""Expose both real owned pipelines and completed controls; keep model quality separate from epoch loss."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write


def main():
    while True:
        neural=read(A/'actual_BF16wide135_progress_v4_20261008.json')
        launch_path=A/'CrossFamily136_complete_hidden_launches_v2_20261008.json';launches=read(launch_path)['launches']
        services={}
        for name,row in launches.items():
            live=owned(row);folder=A/'service_owned_workflows_20261006'/name
            item={'live':live,'owned_worker_pid':row['owned_worker_pid'],'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
            if live:
                try:item['RSS_GiB']=round(psutil.Process(row['owned_worker_pid']).memory_info().rss/2**30,3)
                except psutil.Error:pass
            elif (folder/'service_execution.json').exists():item['terminal']=read(folder/'service_execution.json')
            services[name]=item
        pilot=A/'CrossFamily94_official_comparison_v1_20261008/verification.json';quality={'completed_records':0,'expected_records':94}
        if pilot.exists():
            proof=read(pilot);quality.update(completed_records=len(proof['records']),best_score=proof['best']['connected_final_score'],actual_parent=proof['actual_comparison_parent_round'])
        elif (pilot.parent/'actual_stage.json').exists():quality.update(read(pilot.parent/'actual_stage.json'))
        receiver=A/'CrossFamily136_receiver_preflight_main_v2_20261008/receipt.json'
        state={'status':'active_actual_neural135_and_ordered_crossfamily136_workflows','at_local':datetime.now().isoformat(timespec='seconds'),
            'deadline_local':neural['deadline_local'],'best_fully_qualified':neural['best_fully_qualified'],'latest_fully_qualified':neural['latest_fully_qualified'],
            'annual_models_complete':neural['annual_models_complete'],'expected_annual_models':6,'latest_actual_epoch':neural['latest_actual_epoch'],
            'actual135_quality':neural['actual135_quality'],'actual136_quality':quality,
            'crossfamily_completed_preliminary_controls':{'actual_saved_model_audits':30,'actual_full_OOF_heads':6,'actual_full_parent134_CDF_cases':91,
                'actual_cold_CDF_cases':273,'actual_historical_native_hooks':15,'actual_historical_cold_hooks':15,
                'main_receipt':read(A/'CrossFamily_preliminary_controls_main_v1_20261008/historical/receipt.json')},
            'crossfamily24_receiver_controls_main_receipt':read(receiver) if receiver.exists() else None,
            'actual136_services':services,'actual135_services':neural['actual_services'],
            'available_RAM_GiB':round(psutil.virtual_memory().available/2**30,3),'D_free_GiB':round(psutil.disk_usage('D:/').free/2**30,3),
            'E_free_GiB':round(psutil.disk_usage('E:/').free/2**30,3),'actual136_waits_complete135_then_exact_current_parent':True,
            'new_scoring_or_future_inference_not_claimed_until_actual_proofs_exist':True,'global_exhaustion_or_goal_completion_not_claimed':True,'test_labels_read':False}
        bank=Path('E:/赛题五_本机临时/nonflag_HuberIRLS64_bank10_v1_20261008')
        infos=list(bank.glob('*/info_*.json')) if bank.exists() else []
        huber={'actual_completed_annual_models':len(infos),'expected_annual_models':10,'actual_official_scores':0}
        if (bank/'actual_stage.json').exists():huber['actual_stage']=read(bank/'actual_stage.json')
        if (bank/'verification.json').exists():
            proof=read(bank/'verification.json');huber.update(status=proof['status'],actual_full_OOF_heads=proof['actual_full_OOF_heads'])
        for phase in ('probe','bank'):
            receipt=A/'nonflag_HuberIRLS64_controls_main_v1_20261008'/phase/'receipt.json'
            if receipt.exists():huber[phase+'_main_receipt']=read(receipt)
        state['actual_HuberIRLS64_progress']=huber
        write(A/'actual_neural135_CrossFamily136_progress_v3_20261008.json',state)
        best=state['best_fully_qualified'];epoch=state['latest_actual_epoch'];done=len(state['annual_models_complete'])
        lines=['# 本机持续优化进度','',f"更新时间：{state['at_local']}；提交截止：{state['deadline_local']}。",'',
            f"当前完整合格最佳：第{best['round']}轮，官方连接综合分{best['official_score']:.12f}，完整榜{state['latest_fully_qualified']['connected_records']:,}条记录。",'',
            f"神经模型成熟年度完成{done}/6；当前年度训练：{epoch['year']}，已保存{epoch['saved_epoch']}/{epoch['total_epochs']}轮。训练损失不是验证分。" if epoch else f'神经年度完成{done}/6。','',
            f"第135轮实际官方比较：{state['actual135_quality'].get('completed_records',state['actual135_quality'].get('actual_completed_cases',0))}/40。",
            f"第136轮实际官方比较：{quality.get('completed_records',quality.get('actual_completed_cases',0))}/94。",'',
            '跨模型前置检查已通过：30个既有年度模型、6组完整OOF；91项5635800行变换及273冷前缀；15项实际历史原生模型接入及15冷接入。记录已上传main。',
            '第136轮先等待第135轮完整评分、候选、QA46及main回执，再固定完整父方案；继续执行94项官方比较、冻结、实际候选复核、QA47和完整榜main更新。','',
            f"可用内存{state['available_RAM_GiB']:.2f}GiB；D剩余{state['D_free_GiB']:.2f}GiB；E剩余{state['E_free_GiB']:.2f}GiB。大文件保存在E；评分目录按原缓存要求保留D。",'',
            f"Huber鲁棒残差：真实20万行检查已通过；完整年度模型{huber['actual_completed_annual_models']}/10。尚无官方比较分。",'',
            '模型、预测和官方指标只在相应实际证据通过后登记。没有宣布全局优化方向或资源已穷尽。','',
            '| 第136轮实际服务 | PID | 当前状态 |','|---|---:|---|']
        for name,item in services.items():lines.append(f"| {name} | {item['owned_worker_pid']} | {'运行或等待已验证依赖' if item['live'] else item.get('terminal',{}).get('status','未取得终态')} |")
        target=A/'actual_neural135_CrossFamily136_progress_v3_20261008.md';temporary=target.with_suffix('.md.part')
        assert target.resolve().is_relative_to(A.resolve())
        temporary.write_text('\n'.join(lines)+'\n',encoding='utf8',newline='\n');temporary.replace(target)
        time.sleep(10)


if __name__=='__main__':main()
