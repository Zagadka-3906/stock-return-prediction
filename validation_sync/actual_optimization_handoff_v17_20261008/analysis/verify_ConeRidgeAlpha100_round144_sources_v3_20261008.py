"""Admit139 after completed native checks, exact current-parent controls and24 source routes."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    assert_already_qualified_parents()
    for name in ('ConeRidgeAlpha48_native_historical_hooks_v1_20261008','ConeRidgeAlpha_multiyear_native_calendar_v1_20261008',
        'ConeRidgeAlpha8_completed_controls_main_publication_v1_20261008','ConeRidgeAlpha40_causal_refit_v2_20261008',
        'ConeRidgeAlpha97_current_parent_controls_v2_20261008','all_forecast_percentiles_full_scoring_benchmark',
        'cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
    import prepare_ConeRidgeAlpha100_round144_sources_v3_20261008 as generator
    prospective_path=A/'ConeRidgeAlpha100_prospective_routes_v3_20261008.json';prospective=read(prospective_path)
    assert prospective['status']=='passed_actual24_prospective144_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes'
    for path,digest in prospective['input_sha256'].items():assert sha(path)==digest,path
    plan_path=A/'ConeRidgeAlpha100_round144_plan_v1_20261008.json';plan=read(plan_path)
    assert len(plan['heads'])==8 and plan['actual_existing_own_mature_annual_models']==40
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    metadata=[plan_path];proofs={}
    for label,pointer in (('historical','actual_ConeRidgeAlpha97_parent134_location_v1_20261008.json'),
        ('current','actual_ConeRidgeAlpha97_current_parent_location_v1_20261008.json'),
        ('hooks','actual_ConeRidgeAlpha48_native_hooks_location_v1_20261008.json'),
        ('calendar','actual_ConeRidgeAlpha_multiyear_calendar_location_v1_20261008.json'),('causal','actual_ConeRidgeAlpha40_causal_refit_location_v2_20261008.json')):
        path=Path(read(A/pointer)['output'])/'verification.json';metadata += [A/pointer,path];proofs[label]=read(path)
    current=proofs['current'];assert current['actual_full_cases']==97 and current['actual_cold_cases']==291
    assert current['final144_exact_current_parent_controls_fulfilled'] and current['actual_comparison_parent_round'] in (132,134,143)
    assert proofs['hooks']['actual_hooks']==proofs['hooks']['actual_cold_hooks']==48
    assert proofs['calendar']['actual_calendar_cases']==48 and proofs['calendar']['actual_whole_day_controls']==96
    assert proofs['causal']['actual_causal_same_configuration_refit_controls']==40 and proofs['causal']['actual_maturity_windows']==5
    for row in plan['heads'].values():
        metadata.append(Path(row['folder'])/'oof_verification.json')
        for path in row['infos'].values():
            path=Path(path);info=read(path);metadata += [path,Path(info['independent_'+row['state_kind']+'_state_path'])]
    metadata=list(dict.fromkeys(metadata));index_path=A/'ConeRidgeAlpha100_actual_controls_index_v1_20261008.json'
    create(index_path,{'status':'passed_actual40_heads97_current_CDF291cold48_historical_native_hooks',
        'input_sha256':{str(path):sha(path) for path in metadata},'original_external_metadata':{str(path):read(path) for path in metadata},
        'actual_comparison_parent_round':current['actual_comparison_parent_round'],'no_large_weights_copied_into_Git':True,
        'new_quality_scores':0,'test_labels_read':False})
    outputs={str(parent):{name:hashlib.sha256(text.encode()).hexdigest() for name,text in generator.generate(parent).items()} for parent in (132,134,143)}
    assert outputs==prospective['generated_source_sha256']
    runtime=A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json'
    assert read(runtime)['status']=='passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact'
    pins={**prospective['input_sha256'],**plan['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),plan_path,index_path,prospective_path,runtime,*[p for p in generator.source_paths() if p.is_file()]]}}
    for proof in proofs.values():
        for path,digest in proof['input_sha256'].items():
            assert path not in pins or pins[path]==digest,path
            pins[path]=digest
    for path,digest in pins.items():assert sha(path)==digest,path
    create(A/'ConeRidgeAlpha100_round144_source_admission_v3_20261008.json',{
        'status':'passed_actual40_heads97_current_CDF291cold48hooks_and24_prospective144_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,
        'actual_existing_native_model_audits':40,'actual_full_OOF_heads':8,'actual_full_transform_controls':97,
        'actual_cold_transform_controls':291,'actual_historical_native_hooks':48,'actual_calendar_cases':48,
        'actual_comparison_parent_round':current['actual_comparison_parent_round'],'new_quality_scores':0,
        'candidate_future_inference_and_QA55_pending':True,'test_labels_read':False})
    print('140 first quality admitted after actual20,49/147,24 hooks and24 receiver checks.',flush=True)



def assert_already_qualified_parents():
    for number in (132,134,143):
        assert read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status']=='passed'
        assert read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')['status']=='pushed_and_remote_head_verified'

if __name__=='__main__':main()
