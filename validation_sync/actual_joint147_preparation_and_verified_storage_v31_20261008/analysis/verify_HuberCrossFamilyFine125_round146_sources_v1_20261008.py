"""Admit125 official comparisons only after full/cold native controls,32 prospective receivers and all anchors qualify."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
def main():
    for name in ('HuberCrossFamilyFine146_complete_prospective_controls_v1_20261008','HuberCrossFamilyFine30_actual_native_historical_controls_v1_20261008',
        'HuberCrossFamilyFine121_actual_full_historical_controls_v1_20261008','HuberCrossFamilyFine30_multiyear_calendar_controls_v1_20261008','CrossFamilyFine125_round145_full_registration_v2_20261008',
        'actual_fine146_historical_controls_main_publication_v30_20261008','all_forecast_percentiles_full_scoring_benchmark',
        'cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
    import prepare_HuberCrossFamilyFine125_round146_sources_v1_20261008 as generator
    prospective=A/'HuberCrossFamilyFine125_prospective_routes_v1_20261008.json';p=read(prospective)
    assert p['status']=='passed_actual32_prospective146_sources_fixed_stage_graphs_baselines_status_paths_model_counts_signed_ties_and_cross_volume_bytes'
    for path,digest in p['input_sha256'].items():assert sha(path)==digest,path
    pointers=('actual_HuberCrossFamilyFine_bank15_location_v1_20261008.json','actual_HuberCrossFamilyFine121_parent136_location_v1_20261008.json','actual_HuberCrossFamilyFine30_native_hooks_location_v1_20261008.json')
    inputs=[Path(read(A/n)['output'])/'verification.json' for n in pointers];bank,current,hooks=map(read,inputs)
    assert bank['actual_model_count']==15 and bank['actual_full_OOF_heads']==3
    plan_path=A/'HuberCrossFamilyFine125_round146_plan_v2_20261008.json';plan=read(plan_path)
    relevant=[r for r in bank['actual_native_replay_records'] if r['head'] in plan['heads']]
    assert len(relevant)==15 and len(plan['heads'])==3
    assert current['actual_stage_base_round']==136 and current['actual_full_cases_including_identity']==121 and current['actual_cold_cases_including_identity']==363
    assert current['actual_nonzero_full_cases']==120 and current['actual_nonzero_cold_cases']==360
    assert hooks['actual_hooks']==hooks['actual_cold_hooks']==30
    calendar=Path(read(A/'actual_HuberCrossFamilyFine_multiyear_calendar_location_v1_20261008.json')['output'])/'verification.json';c=read(calendar)
    assert c['actual_calendar_cases']==30 and c['actual_whole_day_controls']==60
    metadata=[*inputs,calendar]
    for r in plan['heads'].values():
        metadata.append(Path(r['folder'])/'oof_verification.json')
        for path in r['infos'].values():
            info=read(path);metadata.extend([Path(path),Path(info['independent_'+r['state_kind']+'_state_path'])])
    for n in plan['anchor_rounds']:
        f=A/f'optimization_20261003_r{n}';candidate=ROOT/f'candidates/optimization_20261003_r{n}';receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json'
        assert read(f/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        metadata.extend([f/'full_registration_execution.json',f/'calibrated_csv_official.json',receipt,candidate/'verification.json',candidate/'manifest.json'])
    index=A/'HuberCrossFamilyFine125_actual_controls_index_v1_20261008.json'
    create(index,{'status':'passed_actual15_heads121_fixed_base_CDF363cold30_historical_native_hooks','input_sha256':{str(f):sha(f) for f in dict.fromkeys(metadata)},
        'original_external_metadata':{str(f):read(f) for f in dict.fromkeys(metadata) if not f.is_relative_to(ROOT)},
        'existing_bank15_actual15_relevant_native_records':relevant,'fixed_scientific_stage_base_round':136,'no_large_weights_copied_into_Git':True,'new_quality_scores':0,'test_labels_read':False})
    outputs={str(n):{name:hashlib.sha256(text.encode()).hexdigest() for name,text in generator.generate(n).items()} for n in plan['anchor_rounds']}
    assert outputs==p['generated_source_sha256']
    inputs=[Path(__file__),Path(generator.__file__),prospective,plan_path,index,*metadata,A/'HuberCrossFamilyFine146_complete_receiver_preparation_v1_20261008.json',A/'HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.json']
    pins={**p['input_sha256'],**{str(f):sha(f) for f in dict.fromkeys(inputs)}}
    create(A/'HuberCrossFamilyFine125_round146_source_admission_v1_20261008.json',{'status':'passed_actual15_heads121_fixed_base_CDF363cold30hooks_and32_prospective146_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,'fixed_scientific_stage_base_round':136,
        'actual_relevant_saved_native_heads':15,'actual_full_OOF_heads':3,'actual_new_native_fits':0,'prospective_sources':32,
        'quality_scoring_admitted_cases':125,'new_quality_scores_by_admission':0,'test_labels_read':False})
    print('All15 native states,121/363 full/cold controls,30/30 native hooks and32 sources admitted for125 official comparisons.',flush=True)
if __name__=='__main__':main()
