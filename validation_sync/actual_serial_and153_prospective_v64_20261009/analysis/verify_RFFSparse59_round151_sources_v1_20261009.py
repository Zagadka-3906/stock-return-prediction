"""Admit59 official cases after32 generated routes,55/165 controls,72 native checks and actual149 duplicate audit."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    for name in ('RFFSparse151_complete_prospective_controls_v1_20261009','RFFSparse72_native_historical_calendar_controls_v1_20261009',
                 'RFFSparse55_full_historical_controls_v1_20261009','HuberSparse59_round150_full_registration_v1_20261008',
                 'RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009',
                 'all_forecast_percentiles_full_scoring_benchmark','cached_official_spearman_full12_benchmark','exact_native_JSON_archive_runtime_full_preflight'):closed(name)
    import prepare_RFFSparse59_round151_sources_v1_20261009 as generator
    prospective=A/'RFFSparse59_prospective_routes_v1_20261009.json';p=read(prospective)
    assert p['status']=='passed_actual32_prospective151_sources_fixed_stage_graphs_baselines_status_paths_model_counts_signed_ties_and_cross_volume_bytes'
    for path,digest in p['input_sha256'].items():assert sha(path)==digest,path
    pointers=[A/n for n in ('actual_RFFSparse55_parent134_location_v1_20261009.json','actual_RFFSparse72_native_calendar_location_v1_20261009.json','actual_RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009.json')]
    proofs=[]
    for pointer in pointers:
        descriptor=read(pointer);full=Path(descriptor['output'])/'verification.json';assert sha(full)==descriptor['verification_sha256'];proofs.append(full)
    current,hooks,duplicate=map(read,proofs)
    assert current['actual_stage_base_round']==134 and current['actual_full_cases_including_identity']==55 and current['actual_cold_cases_including_identity']==165
    assert hooks['actual_historical_cases']==54 and hooks['actual_calendar_cases']==18 and hooks['actual_cold_cases']==72 and hooks['actual_existing_annual_states']==20
    assert duplicate['actual_current_cases']==55 and duplicate['known_zero_control_count']==1
    duplicate_raw=A/'RFFSparse151_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json';assert not duplicate_raw.exists();duplicate_raw.write_bytes(proofs[2].read_bytes());assert sha(duplicate_raw)==sha(proofs[2])
    plan_path=A/'RFFSparse59_round151_plan_v1_20261009.json';plan=read(plan_path)
    metadata=[*pointers,*proofs,duplicate_raw,A/'RFFSparse59_synthetic55_and_state20_metadata_v1_20261009.json']
    native=[]
    for head,row in plan['heads'].items():
        metadata.extend([Path(row['folder'])/'oof_verification.json',Path(row['oof'])])
        for year,path in row['infos'].items():
            info=read(path);state=Path(info['independent_'+row['state_kind']+'_state_path']);assert sha(state)==info['independent_'+row['state_kind']+'_state_sha256']
            metadata.extend([Path(path),state]);native.append({'head':head,'year':int(year),'native_model_sha256':info['native_model_sha256'],'independent_state_sha256':sha(state)})
    assert len(native)==20
    for n in plan['anchor_rounds']:
        f=A/f'optimization_20261003_r{n}';candidate=ROOT/f'candidates/optimization_20261003_r{n}';receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json'
        assert read(f/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        metadata.extend([f/'full_registration_execution.json',f/'calibrated_csv_official.json',receipt,candidate/'verification.json',candidate/'manifest.json'])
    pins={**current['input_sha256'],**hooks['input_sha256'],**duplicate['input_sha256']}
    for path,digest in pins.items():assert sha(path)==digest,path
    pins.update({str(f):sha(f) for f in dict.fromkeys(metadata)})
    annual_path=A/'sparse150151_all20_annual_native_coverage_v1_20261009.json';annual=read(annual_path)
    coverage=next(r for r in annual['records'] if r['round']==151)
    assert coverage['actual_head_year_states']==20 and coverage['actual_native_cases']==coverage['actual_cold_cases']==90
    for path,digest in annual['input_sha256'].items():assert sha(path)==digest,path
    supplemental_pointer=A/'actual_RFFSparse18_year2023_native_supplement_location_v1_20261009.json'
    supplemental=Path(read(supplemental_pointer)['output'])/'verification.json'
    assert sha(supplemental)==read(supplemental_pointer)['verification_sha256']
    metadata.extend([annual_path,supplemental_pointer,supplemental]);pins.update(annual['input_sha256']);pins.update({str(p):sha(p) for p in (annual_path,supplemental_pointer,supplemental)})
    index=A/'RFFSparse59_actual_controls_index_v1_20261009.json'
    create(index,{'status':'passed_actual20_states55_fixed_base_CDF165cold72_native_calendar_controls','input_sha256':pins,
                  'original_external_metadata':{str(f):read(f) for f in dict.fromkeys(metadata) if not f.is_relative_to(ROOT) and f.suffix=='.json'},
                  'actual20_saved_states':native,'actual90_native_and_cold_stage_cases':True,'all20_own_annual_native_states_replayed':True,'fixed_scientific_stage_base_round':134,'no_large_weights_copied_into_Git':True,'new_quality_scores':0,'test_labels_read':False})
    outputs={str(n):{name:hashlib.sha256(text.encode()).hexdigest() for name,text in generator.generate(n).items()} for n in plan['anchor_rounds']}
    assert outputs==p['generated_source_sha256']
    inputs=[Path(__file__),Path(generator.__file__),prospective,plan_path,index,A/'RFFSparse151_receiver_label_refinement_v3_20261009.json',A/'RFFSparse151_D_scoring_scope_v1_20261009.json']
    pins={**p['input_sha256'],**pins,**{str(f):sha(f) for f in inputs}}
    create(A/'RFFSparse59_round151_source_admission_v1_20261009.json',{'status':'passed_actual20_states55_CDF165cold72_native_and32_prospective151_sources_and_actual_duplicate_audit',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,'fixed_scientific_stage_base_round':134,
        'actual_relevant_saved_native_heads':20,'actual_full_OOF_heads':4,'actual_new_native_fits':0,'prospective_sources':32,
        'complete32_routes_and_graph_controls_passed':True,'all20_own_annual_native_states_replayed':True,'prior_complete_forecast_duplicate_audit_passed':True,
        'quality_scoring_admitted_cases':59,'new_quality_scores_by_admission':0,'test_labels_read':False})
    print('20 states,55/165 full/cold controls,72 native checks and32 sources admitted for59 comparisons.',flush=True)
if __name__=='__main__':main()
