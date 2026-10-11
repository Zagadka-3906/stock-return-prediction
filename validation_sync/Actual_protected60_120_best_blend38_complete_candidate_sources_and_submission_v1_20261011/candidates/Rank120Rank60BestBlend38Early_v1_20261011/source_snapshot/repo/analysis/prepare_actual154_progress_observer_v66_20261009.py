"""Version the observer with the actual successful154 admission and dispatcher."""
from pathlib import Path
import sys, ast
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def main():
    source=A/'monitor_actual_chronological_optimization_progress_v65_20261009.py'
    text=source.read_text(encoding='utf8').replace('v65_20261009','v66_20261009')
    pairs={
        'BF16TwoSeed154_complete_chronological_dispatch_v4_20261009':'BF16TwoSeed154_complete_chronological_dispatch_v5_20261009',
        'BF16TwoSeed79_round154_source_admission_v1_20261009':'BF16TwoSeed79_round154_source_admission_v2_20261009',
        "state['current_turn_evidence_main']=status('actual153_complete_and_dropout156_controls_main_publication_v77_20261009')":"state['current_turn_evidence_main']=status('actual154_corrected_receivers_and_cache_cleanup_main_publication_v79_20261009')\n    state['previous153_156_evidence_main']=status('actual153_complete_and_dropout156_controls_main_publication_v77_20261009')\n    state['historical_browser_cleanup']=read(A/'historical_inactive_browser_cache_cleanup_v78_20261009.json')"
    }
    for old,new in pairs.items():
        assert text.count(old)==1,(old,text.count(old));text=text.replace(old,new)
    ast.parse(text)
    target=A/'monitor_actual_chronological_optimization_progress_v66_20261009.py'
    with target.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    start_source=A/'start_actual_recovered_progress_v65_20261009.py'
    start_text=start_source.read_text(encoding='utf8').replace('v65_20261009','v66_20261009').replace('observer_v64_20261009','observer_v65_20261009')
    ast.parse(start_text);starter=A/'start_actual_recovered_progress_v66_20261009.py'
    with starter.open('x',encoding='utf8',newline='\n') as f:f.write(start_text)
    create(A/'actual154_progress_observer_bindings_v66_20261009.json',{'status':'actual154_successful_admission2_dispatch5_bound','input_sha256':{str(p):sha(p) for p in (Path(__file__),source,start_source,target,starter)},'scientific_jobs_changed':0,'new_scores_claimed':0})
if __name__=='__main__':main()
