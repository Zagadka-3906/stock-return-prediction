"""Track the full145 pipeline and preflight/main phases without confusing live waiting workers with completed scores."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'monitor_actual_chronological_optimization_progress_v25_20261008.py';s=old.read_text(encoding='utf8')
    s=s.replace("141:('KrylovGram52',52,18)}","141:('KrylovGram52',52,18),145:('CrossFamilyFine125',125,1)}")
    needle="        if (folder/'verification.json').exists():";assert s.count(needle)==1
    s=s.replace(needle,"        if number==145:\n            row['full_registration']=status('CrossFamilyFine125_round145_full_registration_v2_20261008')\n"+needle)
    s=s.replace('optimization_live_progress_v25_20261008','optimization_live_progress_v28_20261008')
    s=s.replace("'quality_scoring_not_admitted_or_started':True", "'quality_source_admission':status('CrossFamilyFine125_round145_source_admission_v1_20261008'),'quality_scoring':status('CrossFamilyFine125_official_comparison_v1_20261008')")
    s=s.replace("'source_receivers_and_prospective_controls_still_required':True", "'complete_prospective_controls':status('CrossFamilyFine145_complete_prospective_controls_v1_20261008'),'chronological_dispatch':status('CrossFamilyFine145_complete_chronological_dispatch_v1_20261008'),'prospective_main_publication':status('actual145_complete_prospective_main_publication_v27_20261008')")
    s=s.replace('125项官方评分尚未准入或开始。','125项官方评分准入{state[\'fine145_frontier\'][\'quality_source_admission\'][\'status\']}，评分任务{state[\'fine145_frontier\'][\'quality_scoring\'][\'status\']}。')
    target=A/'monitor_actual_chronological_optimization_progress_v28_20261008.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [Path(__file__),old,target]};row=start('actual_chronological_optimization_progress_observer_v28_20261008',target.name,[],pins)
    create(A/'latest_actual_optimization_progress_pointer_v28_20261008.json',{'status':'active_full145_pipeline_observer_with_score_count_and_qualification_distinct','observer':row,'progress':str(A/'optimization_live_progress_v28_20261008.json'),'input_sha256':pins})
    print(json.dumps({'observer_worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
