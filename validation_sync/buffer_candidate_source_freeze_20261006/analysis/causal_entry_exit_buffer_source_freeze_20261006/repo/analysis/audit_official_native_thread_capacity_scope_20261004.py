"""Independently reconcile scorer thread controls, observed resources and proof scope."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'analysis/official_native_thread_capacity_qa_20261004'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    proof_path=QA/'verification.json';proof=read(proof_path)
    protocol_path=QA/'diagnostic_frozen_before_scoring.json';protocol=read(protocol_path)
    assert sha(protocol_path)==proof['diagnostic_freeze_sha256']
    for p,digest in protocol['input_sha256'].items():assert sha(Path(p))==digest,p
    expected=read(ROOT/'analysis/optimization_20261003_r30/calibrated_csv_official.json')['metrics']
    controls=proof['execution_controls'];blocks=[];completed_jobs=0
    originals={name:ROOT/'analysis/optimization_20261003_r30'/p for name,p in
        (('submission.csv','calibrated_validation.csv'),('测试集_X.csv','scoring_validation_only/测试集_X.csv'),('测试集_Y.csv','scoring_validation_only/测试集_Y.csv'))}
    for block in controls:
        i=block['block'];threads=block['native_threads'];assert threads==protocol['thread_order'][i]
        assert read(QA/f'block{i:02d}_result.json')==block
        if block['status']=='not_launched_for_current_memory_budget':
            assert block['available_bytes_at_launch']<block['required_bytes_at_launch'];continue
        samples_path=QA/f'block{i:02d}_samples.jsonl'
        assert sha(samples_path)==block['resource_samples_sha256']
        samples=[json.loads(line) for line in samples_path.read_text(encoding='utf-8').splitlines()]
        assert len(samples)==block['samples']
        assert min(s['available_bytes'] for s in samples)==block['minimum_available_bytes_sampled']
        assert max(s['own_worker_rss_sum_bytes'] for s in samples)==block['maximum_own_worker_rss_sum_bytes_sampled']
        hist=dict(Counter(str(len(s['background'].get('actual_official_worker_pids',[]))) for s in samples))
        assert hist==block['actual_background_official_worker_count_samples']
        jobs=block['jobs_details'];assert len(jobs)==block['jobs_completed']
        assert block['all_completed_jobs_eight_metrics_bit_identical']==all(j['metrics']==expected for j in jobs)
        for job in jobs:
            assert all(value==str(threads) for value in job['native_thread_environment'].values())
            for pool in job['loaded_native_threadpools']:
                if pool['user_api']=='blas':assert pool['num_threads']==threads,pool
            for name,original in originals.items():
                a=(QA/f'block{i:02d}'/f"job{job['job']}"/name).stat();b=original.stat()
                assert (a.st_dev,a.st_ino,a.st_size)==(b.st_dev,b.st_ino,b.st_size)
        if block['status']=='passed':
            assert len(jobs)==protocol['same_jobs_per_block']
            assert block['records_per_minute_completed_control_only']==len(jobs)*60/block['total_seconds_including_spawn_and_shutdown']
        else:assert block['records_per_minute_completed_control_only'] is None
        completed_jobs+=len(jobs)
        blocks.append({'block':i,'native_threads':threads,'status':block['status'],
            'records_per_minute_in_observed_background':block['records_per_minute_completed_control_only'],
            'minimum_available_GiB':block['minimum_available_bytes_sampled']/2**30,
            'actual_background_official_worker_count_samples':hist})
    assert completed_jobs==proof['completed_control_jobs']
    paired=[]
    for threads in sorted(set(protocol['thread_order'])):
        arm=[b for b in controls if b['native_threads']==threads and b['status']=='passed']
        if len(arm)!=2:continue
        seconds=sum(b['total_seconds_including_spawn_and_shutdown'] for b in arm);jobs=sum(b['jobs_completed'] for b in arm)
        rates=[b['records_per_minute_completed_control_only'] for b in arm]
        paired.append({'native_threads':threads,'completed_control_jobs':jobs,
            'combined_records_per_minute_in_observed_background':jobs*60/seconds,
            'individual_measurement_rates':rates,'same_thread_repeat_relative_spread':max(rates)/min(rates)-1})
    target=ROOT/'analysis/official_native_thread_capacity_scope_audit_20261004.json'
    output={'status':'passed','at_local':datetime.now().isoformat(timespec='seconds'),
        'control_proof_status':proof['status'],'completed_control_jobs':completed_jobs,
        'blocks':blocks,'balanced_repeated_thread_measurements':paired,
        'actual_native_thread_environments_andloaded_BLAS_pools_checked':True,
        'all_job_inputs_are_hardlinks_to_the_original_verified_training_CSVs':True,
        'memory_is_available_physical_bytes_not_sum_RSS':True,
        'repeated_order_does_not_remove_uncontrolled_background_confounding':True,
        'no_quality_ranking_or_production_configuration_changed':True,
        'no_hardware_maximum_inferred':True,'new_quality_scores':0,'test_labels_read':False,
        'input_sha256':{str(p.resolve()):sha(p) for p in (Path(__file__),proof_path,protocol_path)}}
    with target.open('x',encoding='utf-8') as stream:json.dump(output,stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':output['status'],'control_proof_status':proof['status'],
        'completed_control_jobs':completed_jobs,'paired_measurements':paired},ensure_ascii=False))

if __name__=='__main__':main()
