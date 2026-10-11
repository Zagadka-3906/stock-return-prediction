"""Expose real fine145 control progress separately from official scores and fully qualified candidates."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'monitor_actual_chronological_optimization_progress_v24_20261008.py';s=old.read_text(encoding='utf8')
    s=s.replace('optimization_live_progress_v24_20261008','optimization_live_progress_v25_20261008')
    needle="    write(A/'optimization_live_progress_v25_20261008.json'";assert s.count(needle)==1
    s=s.replace(needle,"    fine=Path('E:/赛题五_本机临时/CrossFamilyFine121_parent134_historical_v1_20261008')\n    state['fine145_frontier']={'native30_controls':status('CrossFamilyFine30_actual_native_historical_controls_v1_20261008'),'full121_controls':status('CrossFamilyFine121_actual_full_historical_controls_v1_20261008'),'actual_full_control_records':len(list(fine.glob('case*.json'))),'expected_full_control_records_including_identity':121,'synthetic120_controls_completed':(fine/'synthetic120_controls.json').is_file(),'quality_case_count_planned':125,'quality_scoring_not_admitted_or_started':True,'new_official_scores':0,'new_native_fits':0,'source_receivers_and_prospective_controls_still_required':True}\n    state['actual138_fine145_controls_main_publication']=status('actual138_fine145_historical_controls_main_publication_v25_20261008')\n"+needle)
    needle="    write(A/'optimization_live_progress_v25_20261008.md'";assert s.count(needle)==1
    s=s.replace(needle,"    text+=f\"\\n细权重第145轮：原生30项控制{state['fine145_frontier']['native30_controls']['status']}，完整控制{state['fine145_frontier']['actual_full_control_records']}/121，125项官方评分尚未准入或开始。\\n\"\n"+needle)
    target=A/'monitor_actual_chronological_optimization_progress_v25_20261008.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [Path(__file__),old,target]};row=start('actual_chronological_optimization_progress_observer_v25_20261008',target.name,[],pins)
    create(A/'latest_actual_optimization_progress_pointer_v25_20261008.json',{'status':'active_actual25_observer_separating_controls_scores_and_full_qualification','observer':row,'progress':str(A/'optimization_live_progress_v25_20261008.json'),'deadline_local':'2026-10-10T23:59:00+08:00','input_sha256':pins})
    print(json.dumps({'observer_worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
