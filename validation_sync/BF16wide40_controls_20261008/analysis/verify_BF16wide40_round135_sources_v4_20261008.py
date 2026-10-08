"""Admit quality only after actual6 full fits, GPU oracle,37/111 transforms,3 historical hooks and24 receivers."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    for name in ('BF16_complete_parent_actual_historical_native_hook3_v1_20261008',
        'actual_BF16_independent_rank_controls_main_publication_v1_20261008',
        'nonflag_ReverseBayesFine40_round134_full_registration_v1','all_forecast_percentiles_full_scoring_benchmark',
        'cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
    import prepare_BF16wide40_round135_sources_v4_20261008 as generator
    prospective_path=A/'BF16wide40_prospective_routes_v4_20261008.json';prospective=read(prospective_path)
    assert prospective['status']=='passed_actual24_prospective135_sources_schema_graphs_baselines_status_paths_and_cross_volume_bytes'
    for p,d in prospective['input_sha256'].items():assert sha(p)==d,p
    bank=Path(read(A/'actual_BF16_micro8192_bank6_location_v2_20261008.json')['output'])
    oracle=Path(read(A/'actual_BF16_full5_independent_location_v2_20261008.json')['output'])
    transform=Path(read(A/'actual_BF16_rank_CDF_full37_location_v1_20261008.json')['output'])
    hooks=Path(read(A/'actual_BF16_native_hook3_location_v1_20261008.json')['output'])
    inputs=[bank/'verification.json',oracle/'verification.json',transform/'verification.json',hooks/'verification.json']
    b,o,t,h=map(read,inputs)
    assert b['status']=='passed_actual_six_mature_BF16_micro_annual_models' and b['actual_native_fits']==6 and len(b['actual_models'])==6
    assert o['status']=='passed_actual_full5_5635800_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes' and len(o['records'])==5
    assert t['status']=='passed_actual37_full5635800_BF16_rank_CDF_independent_and111_cold_controls' and len(t['controls'])==37
    assert t['actual_parent_round']==134 and t['actual_full_cases']==37 and t['actual_cold_cases']==111
    assert h['status']=='passed_actual3_historical_BF16_full_native_independent_CDF_and_whole_day_prefix_hooks' and len(h['records'])==3
    paths=inputs+[bank/'protocol.json',*[bank/str(y)/'info.json' for y in range(2020,2026)]]
    metadata={str(p):read(p) for p in paths}
    index_path=A/'BF16wide40_actual_controls_index_v1_20261008.json'
    create(index_path,{'status':'passed_actual6_mature_BF16_full5_GPU37_CDF111_prefix3_native_hooks',
        'input_sha256':{str(p):sha(p) for p in paths},'original_external_metadata':metadata,
        'no_large_weights_copied_into_Git':True,'new_quality_scores':0,'test_labels_read':False})
    outputs={}
    for parent in (112,133,134):
        generated=generator.generate(parent)
        outputs[str(parent)]={n:__import__('hashlib').sha256(v.encode()).hexdigest() for n,v in generated.items()}
        assert outputs[str(parent)]==prospective['generated_source_sha256'][str(parent)]
    sources=[Path(__file__),prospective_path,index_path,*[p for p in generator.source_paths() if p.is_file()],
        A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json',
        A/'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json']
    assert read(sources[-2])['status']=='passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact'
    pins={**prospective['input_sha256'],**{str(p):sha(p) for p in sources}}
    for proof in (b,o,t,h):pins.update(proof['input_sha256'])
    for p,d in pins.items():assert sha(p)==d,p
    create(A/'BF16wide40_round135_source_admission_v4_20261008.json',{
        'status':'passed_actual6_full5GPU37CDF111cold3hooks_and24_prospective135_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,
        'actual_native_fits':6,'actual_full_GPU_rows':5635800,'actual_full_transform_controls':37,'actual_cold_transform_controls':111,
        'actual_historical_native_hook_cases':3,'new_quality_scores':0,'candidate_future_inference_and_QA46_pending':True,'test_labels_read':False})
    print('Actual6/5GPU/37/111/3 and24 prospective receivers passed; first135 quality is now admitted.',flush=True)


if __name__=='__main__':main()
