"""Start exact-output140 archival and a truthful six-pipeline progress observer."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'archive_HuberCrossFamily139_completed_scoring_CSV_v1_20261008.py'
    text=old.read_text(encoding='utf8').replace('HuberCrossFamily139','SpectralGram140').replace('HuberCrossFamily112','SpectralGram52').replace('第139轮','第140轮').replace('completed139','completed140').replace('Completed139','Completed140')
    for stem in ('SpectralGram52_official_comparison','SpectralGram52_selected_candidate_preparation'):
        text=text.replace(stem+'_v1_20261008',stem+'_v2_20261008')
    text=text.replace('archived_only_closed_generated136_scoring_CSVs','archived_only_closed_generated140_scoring_CSVs')
    target=A/'archive_SpectralGram140_completed_scoring_CSV_v1_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    files=[Path(__file__),old,target,A/'monitor_actual_optimization135_to140_v8_20261008.py',A/'SpectralGram140_complete_hidden_launches_v4_20261008.json',A/'SpectralGram52_prospective_routes_v2_20261008.json']
    pins={str(p):sha(p) for p in files}
    archive=start('SpectralGram140_completed_scoring_CSV_archivist_v1_20261008',target.name,[],pins)
    create(A/'actual_SpectralGram140_completed_CSV_archivist_hidden_launch_v1_20261008.json',archive)
    observer=start('actual_optimization135_to140_live_progress_v8_20261008','monitor_actual_optimization135_to140_v8_20261008.py',[],pins)
    create(A/'actual_optimization135_to140_progress_hidden_launch_v8_20261008.json',observer)
    assert owned(archive) and owned(observer)
    create(A/'SpectralGram140_archive_and_observer_preparation_v1_20261008.json',{'status':'passed_consoleless_exact140_archivist_and_six_pipeline_observer8_started',
        'input_sha256':pins,'archivist':archive,'observer':observer,'new_quality_scores':0,'test_labels_read':False})
    print('Exact140 completed-CSV archivist and six-pipeline observer8 started consolelessly.',flush=True)

if __name__=='__main__':main()
