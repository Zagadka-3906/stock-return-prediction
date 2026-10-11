"""Retain real partial training log intervals without claiming completed fits."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import sys
import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path.insert(0,str(A))
OUT=A/'neural16384_epoch_progress_observation_20261005'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    original=A/'run_logs/neural16384_annual_recovery_qualified_20261005.stdout.log'
    raw=original.read_bytes()
    text=raw.decode('utf-8')
    starts=[(m.group(1),int(m.group(2))) for m in re.finditer(r'\[(\d\d:\d\d:\d\d)\] New rank16384_drop000_seed07_e32 fold(202\d): fitting',text)]
    firsts=[m.group(1) for m in re.finditer(r'\[(\d\d:\d\d:\d\d)\] MLP y_rank epoch1/32 mature-training loss=',text)]
    assert [year for _,year in starts]==[2020,2021] and len(firsts)==2
    seconds=lambda value:sum(int(v)*w for v,w in zip(value.split(':'),(3600,60,1)))
    intervals=[{'year':year,'actual_fit_start_log_at':start,'actual_epoch1_log_at':first,
        'log_start_to_first_epoch_seconds':seconds(first)-seconds(start)} for (start,year),first in zip(starts,firsts)]
    assert all(row['log_start_to_first_epoch_seconds']>0 for row in intervals)
    handoff=read(A/'recovery_qualified_workflow_handoff_20261005/verification.json')
    # Verify the real live handle by its exact launch arguments, independently of
    # any stale monitor state or a progress log that could survive process loss.
    expected_driver=str(A/'run_neural16384_full_bank_20261005.py')
    expected_run=str(A/'recovery_qualified_workflow_handoff_20261005/neural16384_annual_run.json')
    matches=[]
    for process in psutil.process_iter(['pid','name','cmdline']):
        try:
            argv=process.info['cmdline'] or []
            if process.info['name'].lower()=='python.exe' and argv[-2:]==[expected_driver,expected_run]:
                matches.append(process)
        except psutil.Error:continue
    # Venv launcher and actual interpreter share the arguments; identify the
    # owned real worker by parent/child relationship rather than numeric PID.
    workers=[p for p in matches if p.ppid() in {q.pid for q in matches}]
    assert len(workers)==1
    worker=workers[0]
    argv=worker.cmdline()
    assert argv[-2:]==[expected_driver,expected_run]
    bank=A/'neural16384_full_bank_20261005'
    info=read(bank/'rank16384_drop000_seed07_e32/info_2020.json')
    assert info['status']=='passed' and info['configuration']['epochs']==32
    assert not (bank/'rank16384_drop000_seed07_e32/info_2021.json').exists()
    model=bank/'rank16384_drop000_seed07_e32/model_2020.joblib'
    assert sha(model)==info['model_sha256']
    baseline=read(A/'linear_bank_20261003/rank_ridge_l01/info_2021.json')
    rows=[info['training_meta']['rows'],baseline['training_meta']['rows']]
    steps=[(n+32767)//32768 for n in rows]
    OUT.mkdir()
    snapshot=OUT/'original_native_log_prefix_at_observation.txt'
    with snapshot.open('xb') as stream:stream.write(raw)
    sources=[Path(__file__),snapshot,A/'train_diverse_backbones_20261003.py',
        A/'run_neural16384_full_bank_20261005.py',A/'neural16384_actual_resource_recorder_20261005.py',
        bank/'rank16384_drop000_seed07_e32/info_2020.json',A/'linear_bank_20261003/rank_ridge_l01/info_2021.json']
    create(OUT/'verification.json',{'status':'passed_actual_live_partial_epoch_progress_observation',
        'at_local':datetime.now().isoformat(timespec='seconds'),'owned_live_worker':{'pid':worker.pid,
            'creation_time':worker.create_time(),'command':argv,'cpu_seconds':sum(worker.cpu_times()[:2])},
        'actual_start_to_first_epoch_log_intervals':intervals,'actual_mature_training_rows':rows,
        'prescribed_batches_in_one_epoch':steps,'first_log_interval_ratio':intervals[1]['log_start_to_first_epoch_seconds']/intervals[0]['log_start_to_first_epoch_seconds'],
        'interval_contains_preprocessing_initialization_and_first_epoch_not_isolated_GPU_kernel_timing':True,
        'actual_full32epoch_annual_models_complete':1,'2021_full32epochs_and_artifact_not_yet_complete':True,
        'do_not_count_epoch1_as_full_fit_or_substitute_pilot_quality':True,
        'previous_rows_linear_ETA_assumption_not_yet_supported_by_second_completed_fit':True,
        'no_claim_this_proves_GPU_OOM_or_physical_resource_exhaustion':True,
        'training_not_stopped_or_restarted_or_edited':True,'test_labels_read':False,'new_quality_scores':0,
        'source_sha256':{str(path):sha(path) for path in sources}})
    print(json.dumps({'status':'passed_actual_live_partial_epoch_observation','intervals':intervals,
        'full2021fit_not_complete':True,'worker':worker.pid},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
