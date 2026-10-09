"""Admit78 schemes only after six own fits, full73/219, native42,40 routes and actual152 duplicate audit."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    assert read(f/'service_execution.json')['status']=='passed',name

def main():
    for n in ('BF16Seed10_155_complete_prospective_controls_v1_20261009','BF16Seed10_155_actual_full73_training_v2_20261009',
      'BF16Seed10_155_actual_native42_calendar_v1_20261009','BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009',
      'actual_BF16_medium2048_seed10_e64_bank6_v1_20261009','BF16TwoSeed79_round154_full_registration_v1_20261009',
      'BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009'):closed(n)
    import prepare_BF16Seed10_80_round155_sources_v1_20261009 as g
    prospective=A/'BF16Seed10_80_prospective_routes_v1_20261009.json';p=read(prospective)
    assert p['prospective_sources']==56 and len(p['graph_controls'])==2100
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    pointers=[A/n for n in ('actual_BF16Seed10_155_full73_training_location_v1_20261009.json',
      'actual_BF16Seed10_155_native42_calendar_location_v1_20261009.json','actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009.json',
      'actual_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.json')]
    proofs=[]
    for ptr in pointers:
        path=Path(read(ptr)['output'])/'verification.json';assert sha(path)==read(ptr)['verification_sha256'];proofs.append(path)
    full,native,independent,duplicate=map(read,proofs)
    assert (full['actual_parent_round'],full['actual_full_cases'],full['actual_cold_cases'])==(148,73,219)
    assert (native['actual_saved_states'],native['actual_historical_cases'],native['actual_calendar_cases'],native['actual_cold_cases'])==(6,30,12,42)
    assert len(native['prefit_rejections'])==7
    assert independent['rows_days_stocks']==[5635800,1212,4650] and len(independent['records'])==5
    assert duplicate['actual_current_cases']==73 and duplicate['known_zero_control_count']==1
    planpath=A/'BF16Seed10_80_round155_plan_v1_20261009.json';plan=read(planpath)
    bank=Path(plan['actual_annual_bank']);bankproof=bank/'verification.json'
    assert read(bankproof)['actual_native_fits']==6 and len(read(bankproof)['actual_models'])==6
    metadata=[*pointers,*proofs,planpath,bankproof,bank/'protocol.json'];states=[]
    for y in range(2020,2026):
        folder=bank/str(y);info=read(folder/'info.json');m=info['training_meta']
        assert info['year']==y and info['configuration']==plan['configuration']
        assert sha(folder/'model.joblib')==info['model_sha256']
        assert m['last']<m['cutoff_exclusive']<y*10000+101 and m['last_label_end']<=m['cutoff_exclusive']
        assert m['actual_future_training_label_poisoning_population_exact']
        if y<2025:
            assert sha(folder/'raw.parquet')==info['prediction_sha256']
            assert info['actual_full_annual_reload_prediction_bits_exact'] and info['actual_cold80_prefix_bits_exact']
        else:assert info['full_mature_final_fit_no_actual_future_features_read']
        metadata.extend([folder/'info.json',folder/'frozen_training_inputs.json'])
        states.append({'model_year':y,'model_sha256':info['model_sha256'],'own_mature_training_rows':m['rows'],'cutoff_exclusive':m['cutoff_exclusive']})
    for y in plan['qualified_anchor_rounds']:
        folder=A/f'optimization_20261003_r{y}';candidate=ROOT/f'candidates/optimization_20261003_r{y}';receipt=A/f'github_validation_sync_main_20261005/round{y}_receipt.json'
        assert read(folder/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        metadata.extend([folder/'full_registration_execution.json',folder/'calibrated_csv_official.json',receipt,candidate/'verification.json',candidate/'manifest.json'])
    pins={}
    for proof in (full,native,independent,duplicate,read(bankproof)):
        for f,d in proof['input_sha256'].items():
            assert sha(f)==d,f
            if f in pins:assert pins[f]==d
            pins[f]=d
    pins.update({str(f):sha(f) for f in dict.fromkeys(metadata)})
    index=A/'BF16Seed10_80_actual_controls_index_v1_20261009.json'
    create(index,{'status':'passed_actual6_seed10_155_states42_native73_full219_cold_controls','input_sha256':pins,
      'original_external_metadata':{str(f):read(f) for f in dict.fromkeys(metadata) if not f.is_relative_to(ROOT) and f.suffix=='.json'},
      'actual6_saved_states':states,'fixed_scientific_stage_base_round':148,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})
    outputs={str(y):{name:hashlib.sha256(s.encode()).hexdigest() for name,s in g.generate(y).items()} for y in plan['qualified_anchor_rounds']}
    assert outputs==p['generated_source_sha256']
    inputs=[Path(__file__),Path(g.__file__),prospective,index,A/'BF16Seed10_155_D_scoring_scope_v1_20261009.json',
      A/'BF16Seed10_155_actual_receiver_bindings_v1_20261009.json',A/'BF16Seed10_155_complete_native_predictor_preparation_v1_20261009.json',
      A/'BF16Seed10_155_complete_pipeline_preparation_v1_20261009.json']
    pins={**p['input_sha256'],**pins,**{str(f):sha(f) for f in inputs}}
    create(A/'BF16Seed10_80_round155_source_admission_v1_20261009.json',{
      'status':'passed_actual6_medium_states42_native73_full219_cold56_prospective_routes_and_actual_duplicate_audit',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,
      'fixed_scientific_stage_base_round':148,'actual_saved_states':6,'actual_full_OOF_heads':1,'prospective_sources':56,
      'complete56_routes_and_graph_controls_passed':True,'prior_complete_forecast_duplicate_audit_passed':True,
      'quality_scoring_admitted_cases':80,'new_quality_scores_by_admission':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'quality_cases_admitted':80,'actual_six_states':6,'full_training_cases':73,'prefixes':219,'prospective_sources':56},flush=True)

if __name__=='__main__':main()
