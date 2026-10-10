"""Preserve monitor2 and expose the new CPU bank with the latest complete-board count."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    source=A/'monitor_neural135_and_CrossFamily136_v2_20261008.py';text=source.read_text(encoding='utf8')
    needle="        write(A/'actual_neural135_CrossFamily136_progress_v2_20261008.json',state)"
    assert text.count(needle)==1
    inserted="""        bank=Path('E:/赛题五_本机临时/nonflag_HuberIRLS64_bank10_v1_20261008')
        infos=list(bank.glob('*/info_*.json')) if bank.exists() else []
        huber={'actual_completed_annual_models':len(infos),'expected_annual_models':10,'actual_official_scores':0}
        if (bank/'actual_stage.json').exists():huber['actual_stage']=read(bank/'actual_stage.json')
        if (bank/'verification.json').exists():
            proof=read(bank/'verification.json');huber.update(status=proof['status'],actual_full_OOF_heads=proof['actual_full_OOF_heads'])
        for phase in ('probe','bank'):
            receipt=A/'nonflag_HuberIRLS64_controls_main_v1_20261008'/phase/'receipt.json'
            if receipt.exists():huber[phase+'_main_receipt']=read(receipt)
        state['actual_HuberIRLS64_progress']=huber
"""
    text=text.replace(needle,inserted+needle)
    text=text.replace("best['connected_records']","state['latest_fully_qualified']['connected_records']")
    needle="            '模型、预测和官方指标只在相应实际证据通过后登记。没有宣布全局优化方向或资源已穷尽。','',"
    assert text.count(needle)==1
    text=text.replace(needle,"            f\"Huber鲁棒残差：真实20万行检查已通过；完整年度模型{huber['actual_completed_annual_models']}/10。尚无官方比较分。\",'',\n"+needle)
    text=text.replace('progress_v2_20261008','progress_v3_20261008')
    target=A/'monitor_neural135_and_CrossFamily136_v3_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in (Path(__file__),source,target)}
    row=start('actual_neural135_CrossFamily136_Huber_live_progress_v3_20261008',target.name,[],pins)
    create(A/'actual_neural135_CrossFamily136_Huber_progress_hidden_launch_v3_20261008.json',{
        'status':'started_actual_three_family_progress_monitor_without_altering_old_monitors','identity':row,'input_sha256':pins})


if __name__=='__main__':main()
