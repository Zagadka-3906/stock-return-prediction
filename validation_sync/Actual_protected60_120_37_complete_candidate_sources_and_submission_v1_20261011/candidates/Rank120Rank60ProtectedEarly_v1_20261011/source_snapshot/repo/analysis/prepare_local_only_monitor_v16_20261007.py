"""Route119 qualification and live counts to corrected realv3 services."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    old=A/'monitor_local_only_runtime_v15_20261007.py';s=old.read_text(encoding='utf8')
    services=['quantile_HGB88_round119_source_admission','quantile_HGB88_full85_controls_main_publication','quantile_HGB88_official_comparison','quantile_HGB88_scores_main_publication',
      'quantile_HGB88_selected_candidate_preparation','quantile_HGB88_selected_candidate_sealing','quantile_HGB88_round119_full_registration']
    s=substitute(s,{**{n:n+'_v3' for n in services},'local_only_v15':'local_only_v16',
      'single_host_optimization_live_status_v15_20261007':'single_host_optimization_live_status_v16_20261007'})
    target=A/'monitor_local_only_runtime_v16_20261007.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8')
    old_h=A/'handoff_local_only_monitor_v15_20261007.py';h=old_h.read_text(encoding='utf8')
    h=substitute(h,{'local_only_monitor_v15_actual_handoff_20261007':'local_only_monitor_v16_actual_handoff_20261007',
      'local_only_progress_monitor_v14':'local_only_progress_monitor_v15','local_only_progress_monitor_v15':'local_only_progress_monitor_v16',
      'monitor_local_only_runtime_v14_20261007.py':'monitor_local_only_runtime_v15_20261007.py','monitor_local_only_runtime_v15_20261007.py':'monitor_local_only_runtime_v16_20261007.py',
      'local_only_v15':'local_only_v16','administrative_supersession_local_v15_20261007':'administrative_supersession_local_v16_20261007',
      'passed_actual_idle_observer14_complete118_119_and_nonflag_training_routes_and_R90_gate':'passed_actual_idle_observer15_correct119v3_qualification_and_all_existing_science_preserved'})
    target_h=A/'handoff_local_only_monitor_v16_20261007.py';assert not target_h.exists();compile(h,str(target_h),'exec');target_h.write_text(h,encoding='utf8')
    create(A/'local_only_monitor_v16_source_preparation_20261007.json',{'status':'compiled_correct119v3_qualification_and_prospective_scores_observation','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,old_h,target_h]},'scientific_workers_stopped':0})
if __name__=='__main__':main()
