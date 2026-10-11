"""Start exact completed scratch-CSV archival and the actual eight-pipeline observer."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'archive_KrylovGram141_completed_scoring_CSV_v1_20261008.py';text=old.read_text(encoding='utf8')
    text=text.replace('KrylovGram','ConeRidge').replace('ConeRidge141','ConeRidge142').replace('第141轮','第142轮')
    text=text.replace('completed141','completed142').replace('Completed141','Completed142').replace('generated141','generated142')
    text=text.replace('ConeRidge52_official_comparison_v2_20261008','ConeRidge52_official_comparison_v1_20261008').replace('ConeRidge52_selected_candidate_preparation_v2_20261008','ConeRidge52_selected_candidate_preparation_v1_20261008')
    target=A/'archive_ConeRidge142_completed_scoring_CSV_v1_20261008.py'
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    observer=A/'monitor_actual_optimization135_to142_v11_20261008.py'
    pins={str(p):sha(p) for p in [Path(__file__),old,target,observer,A/'ConeRidge142_complete_hidden_launches_v1_20261008.json',A/'ConeRidge52_prospective_routes_v1_20261008.json']}
    rows={}
    for name,p in (('ConeRidge142_completed_scoring_CSV_archivist_v1_20261008',target),('actual_optimization135_to142_live_progress_v11_20261008',observer)):
        rows[name]=start(name,p.name,[],pins);assert owned(rows[name])
    create(A/'ConeRidge142_archive_and_observer_hidden_launches_v1_20261008.json',{'status':'started_exact_completed142_CSV_archivist_and_observer11',
        'input_sha256':pins,'launches':rows,'new_quality_scores':0,'test_labels_read':False})
    print('Independent142 exact completed-CSV archivist and observer11 started consolelessly.',flush=True)

if __name__=='__main__':main()
