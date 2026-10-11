"""Admit94 quality comparisons only after actual30 heads, exact current91/273 controls,15 hooks and24 receiver routes."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    closed('CrossFamily15_native_historical_hooks_v2_20261008')
    closed('multiyear_residual_native_calendar_v1_20261008')
    closed('multiyear136137_recovery_main_publication_v1_20261008')
    cp=Path(read(A/'actual_multiyear_residual_calendar_location_v1_20261008.json')['output'])/'verification.json'
    assert read(cp)['actual_calendar_cases']==33 and read(cp)['actual_whole_day_controls']==66
    for name in ('CrossFamily91_current_parent_controls_v1_20261008','CrossFamily_preliminary_controls_main_publication_v1_20261008',
        'BF16wide40_round135_full_registration_v4_20261008','all_forecast_percentiles_full_scoring_benchmark',
        'cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
    import prepare_CrossFamily94_round136_sources_v3_20261008 as generator
    prospective_path=A/'CrossFamily94_prospective_routes_v3_20261008.json';prospective=read(prospective_path)
    assert prospective['status']=='passed_actual24_prospective136_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes'
    for path,digest in prospective['input_sha256'].items():assert sha(path)==digest,path
    inputs=[Path(read(A/pointer)['output'])/'verification.json' for pointer in ('actual_CrossFamily_bank30_synthetic_location_v1_20261008.json',
        'actual_CrossFamily91_current_parent_location_v1_20261008.json','actual_CrossFamily15_native_hooks_location_v2_20261008.json')]
    bank,current,hooks=map(read,inputs)
    assert bank['actual_model_count']==30 and bank['actual_full_OOF_heads']==6 and bank['synthetic_case_count']==90
    assert current['status']=='passed_actual91_current_parent_CrossFamily_CDF_and273_cold_controls' and current['actual_full_cases']==91 and current['actual_cold_cases']==273
    assert current['final136_exact_current_parent_controls_fulfilled'] and current['actual_comparison_parent_round'] in (134,135)
    assert hooks['actual_hooks']==hooks['actual_cold_hooks']==15
    plan=read(A/'CrossFamily94_round136_plan_v1_20261008.json')
    metadata_paths=list(inputs)
    for row in plan['heads'].values():
        metadata_paths.append(Path(row['folder'])/'oof_verification.json')
        for path in row['infos'].values():
            path=Path(path);info=read(path);metadata_paths.extend([path,Path(info['independent_'+row['state_kind']+'_state_path'])])
    index_path=A/'CrossFamily94_actual_controls_index_v2_20261008.json'
    create(index_path,{'status':'passed_actual30_heads91_current_CDF273cold15_historical_native_hooks',
        'input_sha256':{str(path):sha(path) for path in dict.fromkeys(metadata_paths)},
        'original_external_metadata':{str(path):read(path) for path in dict.fromkeys(metadata_paths)},
        'actual_comparison_parent_round':current['actual_comparison_parent_round'],'no_large_weights_copied_into_Git':True,'new_quality_scores':0,'test_labels_read':False})
    outputs={}
    for parent in (112,134,135):
        outputs[str(parent)]={name:hashlib.sha256(text.encode()).hexdigest() for name,text in generator.generate(parent).items()}
        assert outputs[str(parent)]==prospective['generated_source_sha256'][str(parent)]
    runtime=A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json'
    assert read(runtime)['status']=='passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact'
    sources=[Path(__file__),cp,prospective_path,index_path,*[path for path in generator.source_paths() if path.is_file()],runtime]
    pins={**prospective['input_sha256'],**{str(path):sha(path) for path in sources}}
    for proof in (bank,current,hooks):
        for path,digest in proof['input_sha256'].items():
            assert path not in pins or pins[path]==digest,path
            pins[path]=digest
    for path,digest in pins.items():assert sha(path)==digest,path
    create(A/'CrossFamily94_round136_source_admission_v3_20261008.json',{
        'status':'passed_actual30_heads91_current_CDF273cold15hooks_and24_prospective136_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'generated_source_sha256':outputs,'actual_existing_native_model_audits':30,'actual_full_OOF_heads':6,
        'actual_full_transform_controls':91,'actual_cold_transform_controls':273,'actual_historical_native_hooks':15,
        'actual_comparison_parent_round':current['actual_comparison_parent_round'],'new_quality_scores':0,'candidate_future_inference_and_QA47_pending':True,'test_labels_read':False})
    print('Actual30-head audit, exact current91/273 controls,15 native hooks and24 receivers passed;136 first quality admitted.',flush=True)


if __name__=='__main__':main()
