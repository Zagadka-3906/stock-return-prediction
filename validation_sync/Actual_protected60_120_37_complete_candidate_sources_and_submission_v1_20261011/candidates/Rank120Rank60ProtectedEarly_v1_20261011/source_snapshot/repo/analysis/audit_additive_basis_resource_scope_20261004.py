"""Verify actual60-fit resource evidence without claiming an unmeasured limit."""
from pathlib import Path
from collections import Counter
import json
import hashlib
import time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/additive_basis_resource_scope_audit_20261004.json'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        for path,digest in read(OUT)['input_sha256'].items():assert sha(Path(path))==digest,path
        print('Frozen additive basis resource scope verified');return
    bank=ROOT/'analysis/additive_basis_bank_20261004'
    observations=ROOT/'analysis/additive_basis_resource_observations_20261004'
    summary=read(observations/'summary.json');assert summary['status']=='passed'
    assert sha(observations/'samples.jsonl')==summary['samples_sha256']
    assert sha(observations/'protocol.json')==summary['protocol_sha256']
    samples=[json.loads(line) for line in (observations/'samples.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(samples)==summary['samples']
    assert min(s['available_ram_bytes'] for s in samples)==summary['minimum_available_ram_bytes_sampled']
    assert max(s['tracked_python_rss_sum_bytes'] for s in samples)==summary['maximum_tracked_python_rss_sum_bytes_sampled']
    assert read(bank/'oof_audit.json')['status']=='passed'
    infos=sorted(bank.glob('*/info_202[0-4].json'));assert len(infos)==60
    assert len({(read(p)['model'],read(p)['year']) for p in infos})==60
    workers=Counter(str(s['actual_spawned_official_workers']) for s in samples)
    sources=[Path(__file__),bank/'protocol.json',bank/'oof_audit.json',observations/'protocol.json',
        observations/'samples.jsonl',observations/'summary.json',
        ROOT/'analysis/late_context_lazy_queue_replacement_20261004.json',*infos]
    payload={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_completed_annual_fits':60,'five_year_native_configurations':12,'basis_columns':[252,378],
        'samples':len(samples),'minimum_available_ram_GiB_sampled':summary['minimum_available_ram_bytes_sampled']/2**30,
        'maximum_tracked_python_rss_GiB_sampled':summary['maximum_tracked_python_rss_sum_bytes_sampled']/2**30,
        'actual_spawned_official_worker_count_samples':dict(workers),
        'official_worker_counts_observed_from_actual_process_trees':True,
        'actual_fit_information':[{key:read(p)[key] for key in ('model','year','fit_seconds','elapsed_seconds')} for p in infos],
        'sum_RSS_may_include_shared_pages_more_than_once':True,
        'not_a_matched_throughput_or_maximum_worker_benchmark':True,
        'chosen8GiB_reserve_is_start_scheduling_rule_not_guaranteed_free_peak_memory':True,
        'future_fulltraining_andinference_peak_not_in_this_sampler_window':True,
        'future_resource_evidence_tracked_separately':'analysis/additive_basis_future_models_qa_20261004/resource_summary.json',
        'physical_resource_boundary_established':False,'global_resource_exhaustion_established':False,
        'finite_layout_grid_does_not_exhaust_additive_model_space':True,'test_data_read':False,
        'input_sha256':{str(p.resolve()):sha(p) for p in sources}}
    with OUT.open('x',encoding='utf-8') as f:json.dump(payload,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'passed','actual_fits':60,'samples':len(samples),
        'minimum_available_ram_GiB_sampled':payload['minimum_available_ram_GiB_sampled'],
        'actual_worker_histogram':dict(workers),'physical_boundary_established':False}))


if __name__=='__main__':main()
