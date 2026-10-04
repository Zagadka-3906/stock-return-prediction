"""Interpret sampled peaks by the workload actually running, retaining original records."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def stages(path):
    data=path.read_bytes();events=[]
    for line in data.decode('utf-8-sig').splitlines():
        if not line.startswith('{'):continue
        try:record=json.loads(line)
        except json.JSONDecodeError:continue
        if 'stage' in record and 'updated_at_local' in record:events.append(record)
    return events,{'path':str(path.resolve()),'captured_prefix_bytes':len(data),'captured_prefix_sha256':hashlib.sha256(data).hexdigest()}


def main():
    out=ROOT/'analysis/nonlinear_ridge_resource_scope_audit_20261004.json';assert not out.exists()
    registry=read(ROOT/'analysis/resumed_rounds_fourier_20261004.json')
    paths={r['round']:Path(r['stdout']) for r in registry}
    e25,p25=stages(paths[25]);e26,p26=stages(paths[26])
    selection=next(e for e in e25 if e['stage']=='finalize_training_round25.select')
    summaries={name:read(ROOT/f'analysis/{name}_ridge_resource_observations_20261004/summary.json') for name in ('additive','fourier')}
    f=summaries['fourier'];start=f['progress_points'][0]['at_local'];finish=f['finished_at_local']
    assert start>selection['updated_at_local']
    assert not any(e['stage']=='independent' and e['updated_at_local']<=finish for e in e26)
    source=ROOT/'analysis/run_training_round25_pipeline.py';text=source.read_text(encoding='utf-8')
    assert text.index("shutdown('optimize_training_round25')")<text.index('for stage in (release.select')
    evidence=[]
    for name,summary in summaries.items():
        assert summary['status']=='passed'
        folder=ROOT/f'analysis/{name}_ridge_resource_observations_20261004'
        for file,key in (('protocol.json','protocol_sha256'),('samples.jsonl','samples_sha256')):
            assert hashlib.sha256((folder/file).read_bytes()).hexdigest()==summary[key]
        evidence.append({'family':name,'samples':summary['samples'],
            'minimum_available_ram_GiB_sampled':summary['minimum_available_ram_bytes_sampled']/2**30,
            'maximum_tracked_python_rss_sum_GiB_sampled':summary['maximum_tracked_python_rss_sum_bytes_sampled']/2**30,
            'maximum_gpu_memory_miB_sampled':summary['maximum_gpu_memory_mib_sampled'],
            'summary_sha256':hashlib.sha256((folder/'summary.json').read_bytes()).hexdigest()})
    payload={'status':'passed','verified_at_local':datetime.now().isoformat(timespec='seconds'),
        'families':evidence,'fourier_sampling_period':{'start':start,'finish':finish},
        'fourier_phase_had_no_four_worker_official_scoring_overlap':True,
        'basis_for_workload_interpretation':'R25 shuts down its pool before select; Fourier sampling starts after select. R26 remained in build until after sampling ended. R25 serial official calibration/evaluation and causal checking did overlap.',
        'fourier_sampler_legacy_counter_field':'completed_additive_annual_fits means Fourier annual artifacts in this sampler; its bank path is fourier_ridge_bank_20261004.',
        'raw_sampler_four_worker_scope_wording_not_used_as_capacity_evidence':True,
        'resource_efficiency_comparison_not_controlled_for_workload':True,
        'chosen8GiB_fit_reserve_not_a_physical_resource_boundary':True,
        'global_resource_exhaustion_established':False,'test_labels_read':False,
        'event_log_snapshots':[p25,p26],
        'source_sha256':{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),source)}}
    out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','families':evidence,'fourier_four_worker_capacity_claim_rejected':True},ensure_ascii=False))


if __name__=='__main__':main()
