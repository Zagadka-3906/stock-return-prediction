"""Publish a truthful live monitor for verified API138 and fresh prospective139–141."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    old=A/'monitor_actual_chronological_optimization_progress_v23_20261008.py';s=old.read_text(encoding='utf8')
    s=s.replace("139:('HuberCrossFamily112',112,14),140:('SpectralGram52',52,14),141:('KrylovGram52',52,14)","139:('HuberCrossFamily112',112,18),140:('SpectralGram52',52,18),141:('KrylovGram52',52,18)")
    needle="        if (folder/'verification.json').exists():";assert s.count(needle)==1
    s=s.replace(needle,"        if number==138:\n            row.update(scores_main=status('exact138_connected_API_publication_reconciliation_v2_20261008'),selected_candidate=status('BF16reverse40_selected_candidate_preparation_v17_20261008'),candidate_sealing=status('BF16reverse40_selected_candidate_sealing_v17_20261008'),full_registration=status('BF16reverse40_round138_full_registration_v17_20261008'))\n"+needle)
    s=s.replace('fresh14_full_prospective_controls_actual15','fresh18_three_round_full_prospective_controls').replace('pending137to141_complete_prospective_controls_actual_D1_v15_20261008','pending139to141_complete_prospective_controls_v18_20261008')
    s=s.replace('fresh14_dispatch_actual16','fresh18_chronological_dispatch').replace('pending137to141_dispatch_verified_fresh14_after_actual15_controls_v16_20261008','pending139to141_chronological_dispatch_v18_20261008')
    s=s.replace('optimization_live_progress_v23_20261008','optimization_live_progress_v24_20261008')
    target=A/'monitor_actual_chronological_optimization_progress_v24_20261008.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [Path(__file__),old,target]};row=start('actual_chronological_optimization_progress_observer_v24_20261008',target.name,[],pins)
    create(A/'latest_actual_optimization_progress_pointer_v24_20261008.json',{'status':'active_verified_actual24_observer','observer':row,'progress':str(A/'optimization_live_progress_v24_20261008.json'),'deadline_local':'2026-10-10T23:59:00+08:00','input_sha256':pins})
    print(json.dumps({'observer_worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
