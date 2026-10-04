"""Audit observed matched-width OOF resources without inferring earlier peaks."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/nystrom_ridge_resource_scope_audit_20261004.json'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if OUT.exists():
        for p,d in read(OUT)['input_sha256'].items():assert sha(Path(p))==d,p
        print('Frozen neural width OOF resource scope verified');return
    bank=ROOT/'analysis/nystrom_ridge_bank_20261004'
    obs=ROOT/'analysis/nystrom_ridge_resource_observations_recovery_20261005'
    summary=read(obs/'summary.json');assert summary['status']=='passed'
    assert sha(obs/'samples.jsonl')==summary['samples_sha256']
    assert sha(obs/'protocol.json')==summary['protocol_sha256']
    rows=[json.loads(line) for line in (obs/'samples.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(rows)==summary['samples']
    assert min(r['available_ram_bytes'] for r in rows)==summary['minimum_available_ram_bytes_sampled']
    assert max(r['tracked_python_rss_sum_bytes'] for r in rows)==summary['maximum_tracked_python_rss_sum_bytes_sampled']
    assert read(bank/'oof_audit.json')['status']=='passed'
    execution=read(bank/'training_execution_scope.json');assert execution['status']=='passed' and execution['all_sha_bindings_restored']
    infos=sorted(bank.glob('*/info_202[0-4].json'));assert len(infos)==20
    assert len({(read(p)['model'],read(p)['year']) for p in infos})==20
    gpu=[r['gpu_last_sample'] for r in rows if r.get('gpu_last_sample',{}).get('query_status')=='passed']
    assert gpu and max(r['memory_used_mib'] for r in gpu)==summary['maximum_all_gpu_memory_used_mib_sampled']
    assert rows[0]['actual_completed_annual_fits']==0 and rows[-1]['actual_completed_annual_fits']==20
    workers=dict(Counter(str(r['actual_spawned_official_workers']) for r in rows))
    sources=[Path(__file__),ROOT/'analysis/audit_nystrom_ridge_resource_scope_20261004.py',ROOT/'analysis/nystrom_restart_source_audit_20261005.json',obs/'recovery_binding.json',bank/'protocol.json',bank/'oof_audit.json',bank/'training_execution_scope.json',obs/'protocol.json',obs/'summary.json',obs/'samples.jsonl',*infos]
    payload={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_completed_annual_fits':20,'five_year_native_configurations':4,'samples':len(rows),
        'sampling_started_after_completed_annual_fits':0,'prior_peaks_not_inferred':True,'sampler_window_includes_serialized_pretraining_wait':True,
        'samples_after_training_protocol_before_execution_scope':sum(r['training_bank_protocol_present'] and not r['training_execution_scope_present'] for r in rows),
        'minimum_available_ram_GiB_sampled':summary['minimum_available_ram_bytes_sampled']/2**30,
        'maximum_tracked_python_rss_GiB_sampled':summary['maximum_tracked_python_rss_sum_bytes_sampled']/2**30,
        'actual_spawned_official_worker_count_samples':workers,
        'official_worker_counts_observed_from_actual_process_trees':True,
        'maximum_all_gpu_memory_used_mib_sampled':max(r['memory_used_mib'] for r in gpu),
        'observed_gpu_total_mib_values':sorted({r['memory_total_mib'] for r in gpu}),
        'gpu_memory_includes_background_GPU_work':True,
        'actual_fit_information':[{k:read(p)[k] for k in ('model','year','fit_seconds','elapsed_seconds')} for p in infos],
        'sum_RSS_may_include_shared_pages_more_than_once':True,
        'chosen14GiB_reserve_is_start_scheduling_rule_not_guaranteed_free_peak_memory':True,
        'future_fulltraining_andinference_peak_not_in_this_sampler_window':True,
        'future_resource_evidence_tracked_separately':'analysis/nystrom_ridge_future_models_qa_20261004/resource_summary.json',
        'physical_resource_boundary_established':False,'global_resource_exhaustion_established':False,
        'finite_landmark_grid_does_not_exhaust_kernel_model_space':True,'test_data_read':False,
        'input_sha256':{str(p.resolve()):sha(p) for p in sources}}
    with OUT.open('x',encoding='utf-8') as f:json.dump(payload,f,ensure_ascii=False,indent=2)
    print(json.dumps({k:payload[k] for k in ('status','samples','actual_completed_annual_fits','minimum_available_ram_GiB_sampled','maximum_all_gpu_memory_used_mib_sampled','actual_spawned_official_worker_count_samples')}))

if __name__=='__main__':main()
