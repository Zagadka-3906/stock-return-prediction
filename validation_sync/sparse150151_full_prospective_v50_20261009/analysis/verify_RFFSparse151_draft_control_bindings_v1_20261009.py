"""Bind actual151 full controls to its54 nonzero drafts and identity; do not claim32-route quality admission."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    proposal_path=A/'RFFSparse59_round151_proposal_v1_20261009.json';plan_path=A/'RFFSparse59_round151_plan_v1_20261009.json'
    prep_path=A/'RFFSparse151_core_receiver_draft_preparation_v2_20261009.json';pointer_path=A/'actual_RFFSparse55_parent134_location_v1_20261009.json'
    proposal,plan,prep,pointer=map(read,(proposal_path,plan_path,prep_path,pointer_path));control_path=Path(pointer['output'])/'verification.json'
    assert sha(control_path)==pointer['verification_sha256'];controls=read(control_path)
    assert proposal['new_cases'][1:]==plan['new_cases'] and len(plan['new_cases'])==54 and len(controls['records'])==55
    assert plan['anchor_rounds']==[147,148,149,150] and plan['round']==151 and plan['QA_version']==62 and plan['wave']==434 and plan['expected_scored_cases']==59
    assert plan['heads']==proposal['heads'] and plan['groups']==proposal['groups'] and plan['original_proposal_sha256']==sha(proposal_path)
    for p,digest in prep['input_sha256'].items():assert sha(p)==digest,p
    grid=[]
    for official_case,cfg in [(i+4,c) for i,c in enumerate(plan['new_cases'])]+[(58,proposal['new_cases'][0])]:
        records=[r for r in controls['records'] if r['configuration']==cfg];assert len(records)==1;r=records[0]
        assert r['rows']==5635800 and r['full_independent_Pandas_bits_exact'] and r['preserved2020_flag1_invalid_bits_exact']
        assert [c['days'] for c in r['cold_controls']]==[80,260,975] and all(c['native_independent_mixture_and_Pandas_bits_exact'] for c in r['cold_controls'])
        grid.append({'official_case':official_case,'control_case':r['case'],'configuration':cfg,'expected_numeric_sha256':r['numeric_sha256']})
    import RFFSparse_complete_parent_CDF_v3_20261009 as codec
    import RFFSparse151_storage_v2_20261009 as storage
    counts=sorted({len({h for names,sign in codec.GROUPS[c['group']] for h in names}) for c in plan['new_cases']});assert counts==[3,4]
    files=[A/n for n in ('RFFSparse151_storage_v2_20261009.py','verify_RFFSparse151_D_scoring_scope_v2_20261009.py','run_RFFSparse59_official_comparison_v2_20261009.py',
        'prepare_RFFSparse59_selected_candidate_v2_20261009.py','seal_RFFSparse59_selected_candidate_v2_20261009.py','run_RFFSparse59_round151_full_registration_v2_20261009.py')]
    for p in files:ast.parse(p.read_text(encoding='utf8'))
    for logical in storage.OUTPUTS:storage.empty(logical)
    assert len(prep['outputs'])==6
    scorer=(files[2]).read_text(encoding='utf8');candidate=(files[3]).read_text(encoding='utf8')
    assert "numeric==measured['numeric_sha256']==duplicate_rows[control_case]['numeric_sha256']" in scorer
    assert 'from run_RFFSparse59_official_comparison_v2_20261009 import best_key' in candidate
    assert "kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']" in candidate
    assert 'independent_'+plan['heads']['rff_g00625']['state_kind']+'_state_path'=='independent_random_fourier_linear_state_path'
    create(A/'RFFSparse151_draft_control_bindings_v1_20261009.json',{'status':'passed55_control_bindings_six_draft_parse_empty_E_outputs_and_actual_mixed_native_storage_kind_not_full_quality_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),proposal_path,plan_path,prep_path,pointer_path,control_path,*files]},
        'control_to_official_mapping':grid,'native_component_counts':counts,'actual_control_bindings':55,'compiled_drafts':6,'verified_empty_E_outputs':6,
        'numeric_SHA_and_duplicate_metric_guards_present_in_scorer_draft':True,'candidate_best_key_import_is_actual_current_scorer':True,
        'required_next':['normalize_inherited_full150_status_labels_and_canonical_date_paths_before_source_admission',
            'prepare_canonical_eight_sources_and_all32_prospective_routes440_graphs','prepare_phase_publishers_and_actual_prior_complete_forecast_duplicate_audit',
            'complete_actual150_full_qualification_before151_quality_admission','execute59_official_scores_selected_source_freeze_native_independent_CSV_cold80_full_QA62_main'],
        'quality_source_admitted':False,'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0,'test_labels_read':False})
    print({'actual_control_bindings':55,'parsed_drafts':6,'verified_empty_E_outputs':6,'quality_admitted':False},flush=True)
if __name__=='__main__':main()
