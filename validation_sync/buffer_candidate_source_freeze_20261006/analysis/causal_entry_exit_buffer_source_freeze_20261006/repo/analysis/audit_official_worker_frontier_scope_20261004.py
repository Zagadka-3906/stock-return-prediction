"""Inspect every completed orguarded scorer control without assigning partial throughput."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/official_worker_frontier_scope_audit_20261004.json'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if OUT.exists():
        for path,digest in read(OUT)['input_sha256'].items():assert sha(Path(path))==digest,path
        print('Frozen official worker frontier scope verified');return
    execution=ROOT/'analysis/official_worker_frontier_execution_20261004/verification.json'
    top=read(execution);assert top['status']=='passed'
    sources=[Path(__file__),execution,ROOT/'analysis/optimization_20261003_r30/calibrated_csv_official.json']
    expected=read(sources[-1])['metrics'];records=[];jobs_total=0
    for block in top['actual_control_blocks']:
        proof_path=Path(block['source']);assert sha(proof_path)==block['verification_sha256']
        proof=read(proof_path);assert proof['status']=='passed' and proof['new_quality_scores']==0
        protocol=proof_path.parent/'diagnostic_frozen_before_scoring.json'
        assert sha(protocol)==proof['diagnostic_freeze_sha256']
        frozen=read(protocol);assert frozen['same_jobs_per_count']==16 and frozen['native_threads_per_worker']==8
        assert frozen['worker_counts']==([8,10,12,16] if block['block']=='forward' else [16,12,10,8])
        for path,digest in frozen['input_sha256'].items():assert sha(Path(path))==digest,path
        sources.extend([proof_path,protocol]);completed=[]
        for control in proof['execution_controls']:
            count=control['workers'];result=proof_path.parent/f'workers{count}_result.json'
            assert read(result)==control;sources.append(result)
            if control['status']=='not_launched_for_current_memory_budget':
                assert control['available_bytes_at_launch']<control['required_bytes_at_launch']
                assert control.get('records_per_minute_completed_control_only') is None
                records.append({'block':block['block'],'workers':count,'status':control['status'],
                    'actually_completed_jobs':0,'throughput_rank_available':False,'physical_exhaustion_proved':False})
                continue
            assert control['status'] in ('passed','stopped_at_declared_control_boundary')
            sample=proof_path.parent/f'workers{count}_samples.jsonl';assert sha(sample)==control['resource_samples_sha256']
            rows=[json.loads(line) for line in sample.read_text(encoding='utf-8').splitlines()]
            assert len(rows)==control['samples'] and rows
            assert min(r['available_bytes'] for r in rows)==control['minimum_available_bytes_sampled']
            assert max(r['own_worker_rss_sum_bytes'] for r in rows)==control['maximum_own_worker_rss_sum_bytes_sampled']
            histogram=dict(Counter(str(len(r['background'].get('actual_official_worker_pids',[]))) for r in rows))
            assert histogram==control['actual_background_official_worker_count_samples']
            jobs=control['jobs_details'];assert len(jobs)==control['jobs_completed']<=16
            assert len({job['job'] for job in jobs})==len(jobs) and all(0<=job['job']<16 for job in jobs)
            assert all(job['metrics']==expected for job in jobs);jobs_total+=len(jobs)
            if control['status']=='passed':
                assert len(jobs)==16 and control['stop_reason'] is None
                assert control['records_per_minute_completed_control_only']==16*60/control['total_seconds_including_spawn_and_shutdown']
                completed.append(count)
            else:
                assert control['records_per_minute_completed_control_only'] is None
                assert control['stop_reason'] in ('sampled_memory_floor','declared_wall_time_budget')
                assert any(r['available_bytes']<2*2**30 for r in rows) if control['stop_reason']=='sampled_memory_floor' else any(r['elapsed_seconds']>240 for r in rows)
            sources.append(sample)
            records.append({'block':block['block'],'workers':count,'status':control['status'],
                'actually_completed_jobs':len(jobs),'all_actual_eight_metrics_bit_identical':True,
                'throughput_rank_available':control['status']=='passed',
                'observed_records_per_minute_completed_control_only':control['records_per_minute_completed_control_only'],
                'minimum_available_host_GiB_sampled':control['minimum_available_bytes_sampled']/2**30,
                'maximum_own_worker_sum_RSS_GiB_sampled':control['maximum_own_worker_rss_sum_bytes_sampled']/2**30,
                'actual_background_official_worker_count_samples':histogram,'stop_reason':control['stop_reason'],
                'physical_exhaustion_proved':False})
        assert completed==proof['completed_counts']
    for path,digest in top['input_sha256'].items():assert sha(Path(path))==digest,path
    payload={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_completed_official_control_jobs':jobs_total,'actual_controls':records,
        'all_actual_completed_job_metrics_match_the_same_frozen_training_CSV':True,
        'never_ranked_guarded_orunattempted_counts_by_throughput':True,
        'forward_reverse_order_andbackground_not_a_randomized_isolated_benchmark':True,
        'sum_RSS_includes_shared_pages_more_than_once':True,
        'full_model_forecast_construction_andfitting_not_in_this_capacity_measurement':True,
        'guards_andtimeouts_are_execution_policies_not_hardware_maxima':True,
        'physical_global_resource_exhaustion_not_proved':True,'new_quality_scores':0,'test_labels_read':False,
        'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}}
    with OUT.open('x',encoding='utf-8') as stream:json.dump(payload,stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'passed','actual_completed_jobs':jobs_total,'actual_controls':len(records)}),flush=True)

if __name__=='__main__':main()
