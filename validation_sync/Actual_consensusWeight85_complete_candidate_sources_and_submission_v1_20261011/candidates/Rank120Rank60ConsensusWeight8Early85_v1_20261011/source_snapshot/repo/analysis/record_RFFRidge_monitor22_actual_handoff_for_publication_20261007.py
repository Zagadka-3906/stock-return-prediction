"""Preserve exact monitor code and actual handoff evidence in the next family publication."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    folder=A/'service_owned_workflows_20261006/local_only_monitor_v22_exact_idle_handoff'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='passed'
    out=A/'local_only_monitor_v22_actual_handoff_20261007'
    proof=read(out/'verification.json');assert proof['scientific_workers_stopped']==0
    sources=[Path(__file__),A/'prepare_local_only_monitor_v22_20261007.py',
        A/'monitor_local_only_runtime_v22_20261007.py',A/'handoff_local_only_monitor_v22_20261007.py']
    evidence=[*out.glob('*.json'),A/'local_only_monitor_v22_source_preparation_20261007.json',folder/'service_execution.json',folder/'native_launch.json']
    create(A/'nonflag_residual_RFFRidge_monitor22_handoff_20261007.json',{
        'status':'recorded_actual_passed_monitor22_handoff_and_exact_source_for_main_publication',
        'source_snapshots':{str(p):{'sha256':sha(p),'utf8_text':p.read_text(encoding='utf8')} for p in sources},
        'actual_evidence':{str(p):{'sha256':sha(p),'value':read(p)} for p in evidence},
        'scientific_workers_stopped_or_restarted':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
