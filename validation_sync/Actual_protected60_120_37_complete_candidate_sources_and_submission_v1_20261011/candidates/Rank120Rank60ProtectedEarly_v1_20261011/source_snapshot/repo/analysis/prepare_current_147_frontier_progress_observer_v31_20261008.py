"""Bind only actual recovery8, finite benchmark2, fine146 dispatch4 and new147 evidence to current monitor."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
 old=A/'monitor_actual_chronological_optimization_progress_v30_20261008.py';s=old.read_text(encoding='utf8').replace('_v30_20261008','_v31_20261008')
 # Keep the actual historical main publication service at30; its output is not an observer version.
 s=s.replace('actual_fine146_historical_controls_main_publication_v31_20261008','actual_fine146_historical_controls_main_publication_v30_20261008')
 s=s.replace('actual_full_board_deferred_serialization_benchmark_v1_20261008','actual_full_board_deferred_serialization_benchmark_v2_20261008')
 s=s.replace('HuberCrossFamilyFine146_complete_chronological_dispatch_v3_20261008','HuberCrossFamilyFine146_complete_chronological_dispatch_v4_20261008')
 s=s.replace('Git_publisher_refreshed_current_main_and_E_relocation_v7_20261008','Git_publisher_private_stat_refresh_verified_E_relocation_v8_20261008')
 needle="    write(A/'optimization_live_progress_v31_20261008.json'";assert s.count(needle)==1
 extra="""    joint=Path('E:/赛题五_本机临时/JointCrossHuber181_parent134_historical_v1_20261008')
    state['joint147_frontier']={'expected_quality_cases':185,'complete_quality_receivers_not_yet_prepared':True,
        'synthetic181':status('JointCrossHuber181_actual_synthetic_controls_v1_20261008'),
        'native80':status('JointCrossHuber80_native_historical_calendar_controls_v2_20261008'),
        'full181':status('JointCrossHuber181_actual_full_historical_controls_v1_20261008'),
        'actual_full_control_records':len(list(joint.glob('case*.json'))),'actual147_official_scores':0,
        'existing35_evidence_is_rehash_not_new_native_replay':True,'actual_future_inference':0}
    state['isolated_serialization_benchmark']['memory_wait_budget_seconds']=300
    state['isolated_serialization_benchmark']['original24GiB_start_threshold_preserved']=True
"""
 s=s.replace(needle,extra+needle)
 needle="    write(A/'optimization_live_progress_v31_20261008.md',text)";assert s.count(needle)==1
 s=s.replace(needle,"    text+=f\"\\n第147轮联合两阶段与顺序：185项比较提案，合成181项/543截断{state['joint147_frontier']['synthetic181']['status']}；真实原生80项{state['joint147_frontier']['native80']['status']}，完整训练控制{state['joint147_frontier']['actual_full_control_records']}/181。尚未官方评分。\\n\"\n"+needle)
 target=A/'monitor_actual_chronological_optimization_progress_v31_20261008.py';compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p) for p in [Path(__file__),old,target]};r=start('actual_chronological_optimization_progress_observer_v31_20261008',target.name,[],pins)
 create(A/'actual_joint147_progress_observer_hidden_launch_v31_20261008.json',{'launch':r,'input_sha256':pins})
 create(A/'latest_actual_optimization_progress_pointer_v31_20261008.json',{'json':str(A/'optimization_live_progress_v31_20261008.json'),'markdown':str(A/'optimization_live_progress_v31_20261008.md'),'observer_worker':r['owned_worker_pid']})
 print(json.dumps({'worker':r['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
