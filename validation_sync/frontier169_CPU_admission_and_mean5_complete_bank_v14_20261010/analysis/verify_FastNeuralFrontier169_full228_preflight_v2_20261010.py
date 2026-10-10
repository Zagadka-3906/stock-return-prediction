"""Admit all228 measured capsules, two real bases, four own banks and complete QA80 routes."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments

def main():
    assert allowed()
    import prepare_frontier169_full_registry_sources_v2_20261010 as routes
    for name in ['frontier169_candidate_sources_preparation_v2_20261010.json','frontier169_candidate_sources_preparation_v3_20261010.json',
                 'frontier169_full_registry_source_preparation_v2_20261010.json','fast_neural_frontier169_actual_parent_callback_CPU_controls_v2_20261010.json']:
        for p,d in read(A/name)['input_sha256'].items():assert sha(p)==d,p
    sources=list(dict.fromkeys([*routes.source_paths(),Path(__file__),A/'prepare_frontier169_full_registry_sources_v2_20261010.py']))
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    opt=literal_assignments(A/'optimize_training_round169.py')
    assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(169,168,(452,))
    register=(A/routes.NAMES[0]).read_text(encoding='utf8')
    for token in ["'expected_scored_records': 228","'explicit_parent_round': 168","'waves': [452]","r{cfg['anchor_round']}/verification.json", "'original_complete_parent_round':cfg['anchor_round']"]:assert token in register,token
    publisher=(A/routes.NAMES[1]).read_text(encoding='utf8')
    for token in ['collect(169, 80, 228)',"namespace['snapshot'](169)","'scored_records': 228","'actual_full_QA_version': 80"]:assert token in publisher,token
    prep=(A/'prepare_frontier169_selected_candidate_v5_20261010.py').read_text(encoding='utf8')
    for token in ['parent_number in (167,168)',
                  'actual_BF16RecentReturn252Huber050169_full5_independent_location_v1_20261009.json',
                  'actual_BF16Recent252Forward20Huber050170_full5_independent_location_v1_20261009.json',
                  'actual_BF16Recent252Forward5Huber050171_full5_independent_location_v1_20261009.json',
                  'actual_BF16Recent252Rank5Huber050172_full5_independent_location_v1_20261009.json',
                  'exact_E_guard(scoring', 'predict_fast_neural_frontier169_complete_scheme_v2_20261010']:
        assert token in prep,token
    nativefolder=Path(read(A/'actual_fast_neural_frontier228_selected_native14_location_v1_20261010.json')['output'])
    pilot=read(nativefolder/'pilot228.json');controls=read(nativefolder/'verification.json')
    assert len(pilot['records'])==228 and pilot['expected_scored_records']==228 and pilot['actual_comparison_parent_round']==168
    assert pilot['actual_scheme_base_round']==pilot['best']['configuration']['anchor_round'] in (167,168)
    assert pilot['best']['configuration']['model'] is not None
    assert (controls['actual_saved_states'],controls['actual_historical_cases'],controls['actual_calendar_cases'],controls['actual_cold_cases'])==(6,10,4,14)
    assert len(controls['prefit_rejections'])==7 and controls['best']==pilot['best']
    assert pilot['best']==min(pilot['records'],key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    assert pilot['best']['connected_final_score']>read(A/'optimization_20261003_r168/calibrated_csv_official.json')['metrics']['final_score']
    for record in pilot['records']:
        cfg=record['configuration'];capsule=Path(record['official_score_cache']['official_metrics_source'])
        assert sha(capsule)==record['official_metric_capsule_sha256'] and read(capsule)['metrics']==record['metrics']
        assert cfg['anchor_round'] in (167,168)
        if 'original_screen_case' in record and record['original_screen_case']==0:
            assert cfg['anchor_round']==168 and cfg['model'] is None
        if cfg['model'] is not None:
            assert record['whole_complete_parent_branches_preserved_before_new_stage'] and record['actual_cold80_260_975_bits_exact']
    for p,d in pilot['input_sha256'].items():assert sha(p)==d,p
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'frontier169_full_family_preflight_v2_20261010.json',{'status':'passed228_actual_capsules_per_record167_168_graph_bases4_own_recipe_routes_selected14_QA80_and_E_only_scoring_before_future_dispatch',
        'input_sha256':{str(p):sha(p) for p in [*sources,nativefolder/'pilot228.json',nativefolder/'verification.json']},
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'full_selected_future_inference_pending':True})
    print({'admitted_records':228,'QA_version':80,'selected_base':pilot['actual_scheme_base_round'],'selected_native_and_cold_cases':14,'future_inference_not_started':True},flush=True)
if __name__=='__main__':main()
