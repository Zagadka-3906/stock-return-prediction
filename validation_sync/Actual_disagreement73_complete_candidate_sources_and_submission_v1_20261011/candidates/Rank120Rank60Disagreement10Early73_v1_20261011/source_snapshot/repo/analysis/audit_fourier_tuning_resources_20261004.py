"""Bound the measured Fourier tuning workload without inferring exhaustion."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/fourier_tuning_resource_scope_audit_20261004.json'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        for path,digest in read(OUT)['input_sha256'].items():assert sha(Path(path))==digest,path
        print('Frozen Fourier tuning resource scope verified');return
    folder=ROOT/'analysis/fourier_tuning_resource_observations_20261004'
    summary=read(folder/'summary.json');assert summary['status']=='passed'
    assert summary['samples_sha256']==sha(folder/'samples.jsonl')
    assert summary['protocol_sha256']==sha(folder/'protocol.json')
    samples=[json.loads(line) for line in (folder/'samples.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(samples)==summary['samples']
    assert min(value['available_ram_bytes'] for value in samples)==summary['minimum_available_ram_bytes_sampled']
    assert max(value['tracked_python_rss_sum_bytes'] for value in samples)==summary['maximum_tracked_python_rss_sum_bytes_sampled']
    stages=Counter(f"r{stage['round']}:{stage['stage']}" for value in samples for stage in value['live_official_pipeline_stages'])
    assert dict(stages)==summary['pipeline_stage_sample_counts']
    bank=ROOT/'analysis/fourier_tuning_bank_20261004'
    audit=read(bank/'oof_audit.json');assert audit['status']=='passed'
    infos=sorted(bank.glob('*/info_202[0-4].json'));assert len(infos)==50
    future=ROOT/'analysis/fourier_tuning_future_pipelines_qa_20261004/verification.json'
    assert read(future)['status']=='passed'
    sources=[Path(__file__),folder/'protocol.json',folder/'samples.jsonl',folder/'summary.json',
             bank/'protocol.json',bank/'oof_audit.json',future,*infos]
    value={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
           'sample_count':len(samples),'window_first':samples[0]['at_local'],'window_last':samples[-1]['at_local'],
           'completed_actual_annual_fits':50,'configured_native_schemes':10,
           'basis_columns':[191,319,575],'minimum_available_ram_GiB_sampled':summary['minimum_available_ram_bytes_sampled']/2**30,
           'maximum_tracked_python_rss_GiB_sampled':summary['maximum_tracked_python_rss_sum_bytes_sampled']/2**30,
           'maximum_gpu_memory_mib_sampled':summary['maximum_gpu_memory_mib_sampled'],
           'pipeline_stage_sample_counts':dict(stages),
           'scope':'Complete50 annual fitting andOOF checking window with actual changingR26/R27 pipeline stages. The later575-column full2025 fit andfuture implementation checks occur after this window.',
           'official_worker_count_not_inferred_from_stage_name':True,
           'different_pipeline_stages_are_not_matched_workload_benchmarks':True,
           'gpu_observations_are_process_shared_not_a_ridge_gpu_memory_estimate':True,
           'chosen8GiB_reserve_checks_only_before_each_fit':True,
           'chosen_reserve_not_a_model_peak_requirement_or_physical_boundary':True,
           'physical_resource_exhaustion_established':False,'global_resource_exhaustion_established':False,
           'future_implementation_checks_passed_but_future_resource_peak_not_measured_here':True,
           'test_labels_read':False,'input_sha256':{str(path.resolve()):sha(path) for path in sources}}
    OUT.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value[key] for key in ('status','sample_count','completed_actual_annual_fits','minimum_available_ram_GiB_sampled','global_resource_exhaustion_established')}))


if __name__=='__main__':main()
