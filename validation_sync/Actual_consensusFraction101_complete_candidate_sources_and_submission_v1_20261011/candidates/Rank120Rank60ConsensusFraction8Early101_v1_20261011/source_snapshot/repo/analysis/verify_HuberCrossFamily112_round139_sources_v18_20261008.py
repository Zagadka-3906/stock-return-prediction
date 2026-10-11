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
    for name in ('HuberCrossFamily18_native_historical_hooks_v1_20261008','HuberCrossFamily_multiyear_native_calendar_v1_20261008',
        'HuberCrossFamily139_preliminary_historical_main_publication_v1_20261008','BF16reverse40_round138_full_registration_v17_20261008',
        'HuberCrossFamily109_current_parent_controls_v18_20261008','all_forecast_percentiles_full_scoring_benchmark',
        'cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
    import prepare_HuberCrossFamily112_round139_sources_v18_20261008 as generator
    prospective_path=A/'HuberCrossFamily112_prospective_routes_v18_20261008.json';prospective=read(prospective_path)
    assert prospective['status']=='passed_actual24_prospective139_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes'
    for path,digest in prospective['input_sha256'].items():assert sha(path)==digest,path
    plan_path=A/'HuberCrossFamily112_round139_plan_v1_20261008.json';plan=read(plan_path)
    assert len(plan['heads'])==5 and len(plan['window_controls'])==5 and plan['reused_existing_own_mature_annual_models']==25
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    metadata=[plan_path];proofs={}
    for label,pointer in (('historical','actual_HuberCrossFamily109_parent134_location_v1_20261008.json'),
        ('current','actual_HuberCrossFamily109_current_parent_location_v18_20261008.json'),
        ('hooks','actual_HuberCrossFamily18_native_hooks_location_v1_20261008.json'),
        ('calendar','actual_HuberCrossFamily_multiyear_calendar_location_v1_20261008.json')):
        path=Path(read(A/pointer)['output'])/'verification.json';metadata += [A/pointer,path];proofs[label]=read(path)
    current=proofs['current'];assert current['actual_full_cases']==109 and current['actual_cold_cases']==327
    assert current['final139_exact_current_parent_controls_fulfilled'] and current['actual_comparison_parent_round'] in (136,137,138)
    assert proofs['hooks']['actual_hooks']==proofs['hooks']['actual_cold_hooks']==18
    assert proofs['calendar']['actual_calendar_cases']==18 and proofs['calendar']['actual_whole_day_controls']==36
    for row in plan['heads'].values():
        metadata.append(Path(row['folder'])/'oof_verification.json')
        for path in row['infos'].values():
            path=Path(path);info=read(path);metadata += [path,Path(info['independent_'+row['state_kind']+'_state_path'])]
    metadata=list(dict.fromkeys(metadata));index_path=A/'HuberCrossFamily112_actual_controls_index_v18_20261008.json'
    create(index_path,{'status':'passed_actual25_heads109_current_CDF327cold18_historical_native_hooks',
        'input_sha256':{str(path):sha(path) for path in metadata},'original_external_metadata':{str(path):read(path) for path in metadata},
        'actual_comparison_parent_round':current['actual_comparison_parent_round'],'no_large_weights_copied_into_Git':True,
        'new_quality_scores':0,'test_labels_read':False})
    outputs={str(parent):{name:hashlib.sha256(text.encode()).hexdigest() for name,text in generator.generate(parent).items()} for parent in (136,137,138)}
    assert outputs==prospective['generated_source_sha256']
    runtime=A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json'
    assert read(runtime)['status']=='passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact'
    pins={**prospective['input_sha256'],**plan['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),plan_path,index_path,prospective_path,runtime,*[p for p in generator.source_paths() if p.is_file()]]}}
    for proof in proofs.values():
        for path,digest in proof['input_sha256'].items():
            assert path not in pins or pins[path]==digest,path
            pins[path]=digest
    for path,digest in pins.items():assert sha(path)==digest,path
    create(A/'HuberCrossFamily112_round139_source_admission_v18_20261008.json',{
        'status':'passed_actual25_heads109_current_CDF327cold18hooks_and24_prospective139_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,
        'actual_existing_native_model_audits':25,'actual_full_OOF_heads':5,'actual_full_transform_controls':109,
        'actual_cold_transform_controls':327,'actual_historical_native_hooks':18,'actual_calendar_cases':18,
        'actual_comparison_parent_round':current['actual_comparison_parent_round'],'new_quality_scores':0,
        'candidate_future_inference_and_QA50_pending':True,'test_labels_read':False})
    print('139 first quality admitted after actual25,109/327,18 hooks and24 receiver checks.',flush=True)


if __name__=='__main__':main()
