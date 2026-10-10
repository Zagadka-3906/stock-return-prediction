"""Follow exact replacement141 receiver3; keep failed original idle archive evidence."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'archive_KrylovGram141_completed_scoring_CSV_v1_20261008.py';text=old.read_text(encoding='utf8')
    text=text.replace('KrylovGram52_official_comparison_v2_20261008','KrylovGram52_official_comparison_v3_20261008').replace('KrylovGram52_selected_candidate_preparation_v2_20261008','KrylovGram52_selected_candidate_preparation_v3_20261008')
    text=text.replace('scoring_CSV_archive_v1_20261008.json','scoring_CSV_archive_v2_20261008.json')
    target=A/'archive_KrylovGram141_completed_scoring_CSV_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    observer=A/'monitor_actual_optimization135_to142_v12_20261008.py';pins={str(p):sha(p) for p in [Path(__file__),old,target,observer,A/'KrylovGram141_complete_hidden_launches_v3_20261008.json']}
    rows={}
    for name,p in (('KrylovGram141_completed_scoring_CSV_archivist_v2_20261008',target),('actual_optimization135_to142_live_progress_v12_20261008',observer)):
        rows[name]=start(name,p.name,[],pins)
    create(A/'KrylovGram141_corrected_archive_and_observer_hidden_launches_v2_20261008.json',{'status':'started_exact_source3_CSV_archive_and_corrected_observer12',
        'input_sha256':pins,'launches':rows,'training_workers_changed':0,'new_official_scores':0})

if __name__=='__main__':main()
