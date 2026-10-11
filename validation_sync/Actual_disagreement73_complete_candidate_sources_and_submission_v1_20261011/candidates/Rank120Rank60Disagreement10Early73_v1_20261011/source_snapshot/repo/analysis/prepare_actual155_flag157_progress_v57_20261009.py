"""Bind a real current157 frontier and explicit stop to observer69 without changing science."""
from pathlib import Path
import sys,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def write(name,text):
    ast.parse(text);p=A/name
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p
def main():
    original=A/'monitor_actual_chronological_optimization_progress_v68_20261009.py';s=original.read_text(encoding='utf8').replace('v68_20261009','v69_20261009')
    assert s.count("156:('BF16Drop05_81',81,1)")==1;s=s.replace("156:('BF16Drop05_81',81,1)","156:('BF16Drop05_81',81,1),157:('BF16FlagAfter15222',22,1)")
    marker="        folder=A/f'{prefix}_official_comparison_v1_{date}'";assert s.count(marker)==1
    s=s.replace(marker,marker+"\n        if number==157:folder=Path('E:/赛题五_本机临时/BF16FlagAfter15222_official_comparison_v1_20261009')")
    s=s.replace('actual155_progress_and_main81_reconciliation_main_publication_v83_20261009','actual155_flag157_and_stop_schedule_main_publication_v85_20261009')
    marker="    write(A/'optimization_live_progress_v69_20261009.json',json.dumps(state,ensure_ascii=False,indent=2)+'\\n')";assert s.count(marker)==1
    extra="""    flag_full=Path('E:/赛题五_本机临时/BF16FlagAfter15217_full_training_v1_20261009')
    state['flag_after152_157_frontier']={'potential_round':157,'fixed_stage_base':152,'only_flag_valid_rows_may_change':True,
        'new_native_fits':0,'actual_synthetic_cases':17,'actual_synthetic_prefixes':51,
        'full17':status('BF16FlagAfter15217_actual_full_training_controls_v1_20261009'),
        'actual_full_control_records':len(list(flag_full.glob('case*.json'))),'expected_full_controls':17,
        'expected_cold_controls':51,'official22':pipeline['157']['quality'],'official_scores':pipeline['157']['completed_cases'],
        'expected_official_scores':22,'official_scoring_waits_actual156_full':True,
        'full_candidate_freeze_native_replays_and_registration_not_prepared_yet':True,'actual_future_X_read':False,'test_labels_read':False}
    state['explicit_today_stop']=read(A/'current_user_runtime_control_20261009.json')
    state['today_stop_guard']=status('actual_user_stop2355_wait_manual_continue_v1_20261009')
"""
    s=s.replace(marker,extra+marker)
    marker="    write(A/'optimization_live_progress_v69_20261009.md',text)";assert s.count(marker)==1
    s=s.replace(marker,"    text+=f\"\\n第157轮新方向：在完整152后仅调整涨停且行情有效股票，复用seed09；17合成/51前缀已通过，真实完整控制{state['flag_after152_157_frontier']['actual_full_control_records']}/17。22项官方评分排在156完整通过之后；候选原生回放、封存、完整榜仍须完成。\\n\"\n    text+='\\n用户明确安排今晚2026-10-09 23:55停工，23:53收拢派发；停工后等待用户实际发送“继续”。当前目标不提前暂停。\\n'\n"+marker)
    observer=write('monitor_actual_chronological_optimization_progress_v69_20261009.py',s)
    starter_source=A/'start_actual_recovered_progress_v68_20261009.py';s=starter_source.read_text(encoding='utf8').replace('v68_20261009','v69_20261009').replace('observer_v67_20261009','observer_v68_20261009')
    starter=write('start_actual_recovered_progress_v69_20261009.py',s)
    create(A/'actual155_flag157_progress_preparation_v57_20261009.json',{'status':'prepared_actual155_and157_frontier_and_explicit_stop_observer69','input_sha256':{str(p):sha(p) for p in (Path(__file__),original,observer,starter_source,starter)},'new_quality_scores':0})
if __name__=='__main__':main()
