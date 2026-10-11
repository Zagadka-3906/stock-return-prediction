"""Show the admitted14 native controls and corrected quality2; publish before actual quality."""
from pathlib import Path
import sys,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def write(name,text):
    ast.parse(text);p=A/name
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p
def main():
    source=A/'monitor_actual_chronological_optimization_progress_v69_20261009.py';s=source.read_text(encoding='utf8').replace('v69_20261009','v70_20261009')
    old="157:('BF16FlagAfter15222',22,1)";assert s.count(old)==1;s=s.replace(old,"157:('BF16FlagAfter15222',22,2)")
    s=s.replace('actual155_flag157_and_stop_schedule_main_publication_v85_20261009','flag157_native_admission_main_publication_v87_20261009')
    marker="    state['explicit_today_stop']=read(A/'current_user_runtime_control_20261009.json')";assert s.count(marker)==1
    extra="""    state['flag_after152_157_frontier'].update(
        native14=status('BF16FlagAfter152157_actual_native14_calendar_v1_20261009'),
        expected_native14_controls=14,expected_native14_cold_controls=14,expected_prefit_rejections=7,
        only_final_complete152_stage_changed_ABI_proof=str(A/'BF16FlagAfter152157_complete_native_predictor_preparation_v58_20261009.json'))
    state['drop05_156_frontier']['actual_training_stage']=read(bank156/'actual_stage.json') if (bank156/'actual_stage.json').exists() else None
    state['previous155_flag157_stop_main']=status('actual155_flag157_and_stop_schedule_main_publication_v85_20261009')
"""
    s=s.replace(marker,extra+marker)
    marker="    write(A/'optimization_live_progress_v70_20261009.md',text)";assert s.count(marker)==1
    s=s.replace(marker,"    text+=f\"\\n第157轮原生阶段已完成接口检查：保留完整152及其全部早期分支，仅在最后152阶段之后插入神经修正；14原生/14冷与7训练前日期拒绝已排队，评分入口v2必须等待这些实测检查。状态：{state['flag_after152_157_frontier']['native14']['status']}。\\n\"\n"+marker)
    observer=write('monitor_actual_chronological_optimization_progress_v70_20261009.py',s)
    start_source=A/'start_actual_recovered_progress_v69_20261009.py';s=start_source.read_text(encoding='utf8').replace('v69_20261009','v70_20261009').replace('observer_v68_20261009','observer_v69_20261009')
    starter=write('start_actual_recovered_progress_v70_20261009.py',s)
    pub_source=A/'publish_actual155_and_flag157_stop_schedule_main_v85_20261009.py';s=pub_source.read_text(encoding='utf8').replace('v85_20261009','v87_20261009')
    old="create(A/'actual155_flag157_and_stop_schedule_main_v85_receipt_20261009.json',value)";assert s.count(old)==1
    s=s.replace(old,"create(A/'flag157_native_admission_main_v87_receipt_20261009.json',value)")
    marker="    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)";assert s.count(marker)==1
    extra="""    sources.extend([A/'prepare_flag157_native_progress_and_main_v61_20261009.py',A/'actual155_flag157_and_stop_schedule_main_v85_receipt_20261009.json'])
    for pattern in ('*progress*v70_20261009.py','*progress*v70_20261009.json','*progress*v70_20261009.md'):
        sources.extend(p for p in A.glob(pattern) if p.is_file())
"""
    s=s.replace(marker,extra+marker)
    s=s.replace('同步155完整80评分与QA66及157新152涨停修正方向17检查和23点55停工实测','同步157完整152新神经阶段接口与原生14准入及22评分v2和隐藏控制交接')
    pub=write('publish_flag157_native_admission_main_v87_20261009.py',s)
    create(A/'flag157_native_progress_and_main_preparation_v61_20261009.json',{'status':'prepared_actual157_native14_gate_quality2_observer70_and_main87_unique_receipt',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),source,observer,start_source,starter,pub_source,pub)},'new_quality_scores':0})
if __name__=='__main__':main()
