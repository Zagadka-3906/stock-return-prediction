"""Extend the immutable earlier observer with actual137 services and completed Huber historical/causal evidence."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    source=A/'monitor_neural135_and_CrossFamily136_v3_20261008.py';text=source.read_text(encoding='utf8')
    needle="        state['actual_HuberIRLS64_progress']=huber";assert text.count(needle)==1
    inserted="""        if (bank/'verification.json').exists():huber.pop('actual_stage',None)
        huber['actual_historical_full_CDF_cases']=49
        huber['actual_historical_cold_CDF_cases']=147
        huber['actual_historical_native_hooks']=18
        huber['actual_historical_cold_native_hooks']=18
        huber['actual_own_maturity_windows']=5
        huber['actual_later_training_label_poison_controls']=10
        for phase,folder in (('historical','HuberIRLS64_historical_controls_main_v2_20261008'),('causal','HuberIRLS64_causal_handoff_main_v3_20261008')):
            receipt=A/folder/'receipt.json'
            if receipt.exists():huber[phase+'_main_receipt']=read(receipt)
        current137=read(A/'Huber137_complete_hidden_launches_v1_20261008.json')['launches']
        services137={}
        for name,row in current137.items():
            live=owned(row);folder=A/'service_owned_workflows_20261006'/name
            item={'live':live,'owned_worker_pid':row['owned_worker_pid'],'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
            if live:
                try:item['RSS_GiB']=round(psutil.Process(row['owned_worker_pid']).memory_info().rss/2**30,3)
                except psutil.Error:pass
            elif (folder/'service_execution.json').exists():item['terminal']=read(folder/'service_execution.json')
            services137[name]=item
        pilot137=A/'Huber52_official_comparison_v1_20261008/verification.json';quality137={'completed_records':0,'expected_records':52}
        if pilot137.exists():
            proof137=read(pilot137);quality137.update(completed_records=len(proof137['records']),best_score=proof137['best']['connected_final_score'],actual_parent=proof137['actual_comparison_parent_round'])
        elif (pilot137.parent/'actual_stage.json').exists():quality137.update(read(pilot137.parent/'actual_stage.json'))
        state['actual137_quality']=quality137;state['actual137_services']=services137
        receipt137=A/'Huber137_receiver_preflight_main_v1_20261008/receipt.json'
        state['Huber137_receiver_preflight_main_receipt']=read(receipt137) if receipt137.exists() else None
        state['actual137_waits_complete136_then_exact_current_parent']=True
"""
    text=text.replace(needle,inserted+needle)
    needle="            f\"第136轮实际官方比较：{quality.get('completed_records',quality.get('actual_completed_cases',0))}/94。\",'',"
    assert text.count(needle)==1
    text=text.replace(needle,needle+"\n            f\"第137轮实际官方比较：{quality137.get('completed_records',quality137.get('actual_completed_cases',0))}/52。\",'',")
    needle="            f\"Huber鲁棒残差：真实20万行检查已通过；完整年度模型{huber['actual_completed_annual_models']}/10。尚无官方比较分。\",'',"
    assert text.count(needle)==1
    text=text.replace(needle,"            f\"Huber鲁棒残差：完整年度模型{huber['actual_completed_annual_models']}/10；49完整CDF/147冷前缀、18原生接入/18冷接入、5独立成熟窗口/10标签扰动检查已通过。\",'',\n            '第137轮24项预检、588项完整父图保留和9基准/6同分排序检查通过；八步骤队列先等待完整136，再固定父方案、52项评分、冻结、候选、QA48和完整榜main。','',")
    text=text.replace('progress_v3_20261008','progress_v4_20261008')
    target=A/'monitor_neural135_and_CrossFamily136_v4_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    pins={str(path):sha(path) for path in (Path(__file__),source,target)}
    row=start('actual_optimization135136137_live_progress_v4_20261008',target.name,[],pins)
    create(A/'actual_optimization135136137_progress_hidden_launch_v4_20261008.json',{
        'status':'started_actual_neural_and135136137_complete_workflow_progress','identity':row,'input_sha256':pins})


if __name__=='__main__':main()
