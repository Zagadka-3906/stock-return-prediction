"""Start exact141 completed-CSV archival and the seven-pipeline progress observer10."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    source=A/'archive_SpectralGram140_completed_scoring_CSV_v1_20261008.py'
    text=source.read_text(encoding='utf8').replace('SpectralGram140','KrylovGram141').replace('SpectralGram52','KrylovGram52').replace('第140轮','第141轮').replace('completed140','completed141').replace('Completed140','Completed141').replace('generated140','generated141')
    target=A/'archive_KrylovGram141_completed_scoring_CSV_v1_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    files=[Path(__file__),source,target,A/'monitor_actual_optimization135_to141_v10_20261008.py',
        A/'KrylovGram141_complete_hidden_launches_v2_20261008.json',A/'KrylovGram52_prospective_routes_v2_20261008.json']
    pins={str(p):sha(p) for p in files}
    row=start('KrylovGram141_completed_scoring_CSV_archivist_v1_20261008',target.name,[],pins)
    create(A/'actual_KrylovGram141_completed_CSV_archivist_hidden_launch_v1_20261008.json',row);assert owned(row)
    row=start('actual_optimization135_to141_live_progress_v10_20261008','monitor_actual_optimization135_to141_v10_20261008.py',[],pins)
    create(A/'actual_optimization135_to141_progress_hidden_launch_v10_20261008.json',row);assert owned(row)
    create(A/'KrylovGram141_archive_and_observer_preparation_v1_20261008.json',{'status':'passed_exact_completed141_CSV_archivist_and_actual_observer10_started',
        'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    print('Exact141 completed-CSV archivist and seven-pipeline observer10 started consolelessly.',flush=True)

if __name__=='__main__':main()
