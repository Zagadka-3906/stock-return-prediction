"""Verify actual owned waiters before extending the versioned quality registry."""
from pathlib import Path
from datetime import datetime
import json
import psutil
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def create(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)

def main():
    jobs=[]
    for label in ('training','observer','future','complete_scheme','evidence_audits'):
        job=read(ROOT/f'analysis/nystrom_ridge_{label}_run_20261004.json')
        proc=psutil.Process(job['pid']);assert job['script'] in proc.cmdline(),label
        assert Path(job['stderr']).stat().st_size==0,label
        jobs.append({'pid':job['pid'],'script':job['script']})
    entries=read(ROOT/'analysis/nystrom_ridge_waiter_entries_20261004.json')
    assert [v['round'] for v in entries]==[61,62]
    for entry in entries:
        proc=psutil.Process(entry['pid']);assert entry['script'] in proc.cmdline()
        assert str(entry['round']) in proc.cmdline() and Path(entry['stderr']).stat().st_size==0
        state=read(ROOT/f"analysis/ongoing_optimization_r{entry['round']}_state.json")
        assert state['stage']=='waiting_for_actual_previous_round_andlocked_execution_checks'
    global_state=ROOT/'analysis/ongoing_optimization_state.json'
    previous=read(global_state)['active_run_registry'];old=read(ROOT/previous)
    assert not any(v['round'] in (61,62) for v in old)
    registry='analysis/resumed_rounds_nystrom_locked_20261004.json'
    create(ROOT/registry,old+entries)
    for path in (global_state,ROOT/'analysis/resume_optimization_20261004.json'):
        value=read(path);assert value['active_run_registry']==previous
        value.update(active_run_registry=registry,last_queued_round=62,
            nystrom_ridge_queue_evidence='analysis/nystrom_ridge_waiter_entries_20261004.json')
        path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    create(ROOT/'analysis/nystrom_ridge_queue_adoption_20261004.json',{
        'status':'passed_actual_owned_process_andidle_stage_verification',
        'at_local':datetime.now().isoformat(timespec='seconds'),'new_rounds':[61,62],
        'original_registry_preserved':previous,'effective_registry':registry,
        'all_original_entries_unchanged':True,'owned_model_gate_jobs':jobs,
        'actual_annual_fits_completed':0,'new_quality_scores':0,'test_labels_read':False,
        'scope':'Actual live queue adoption only; all annual/future/complete-output quality checks remain required.'})
    print('Seven actual owned gate processes verified; versioned quality registry extended through R62',flush=True)

if __name__=='__main__':main()
