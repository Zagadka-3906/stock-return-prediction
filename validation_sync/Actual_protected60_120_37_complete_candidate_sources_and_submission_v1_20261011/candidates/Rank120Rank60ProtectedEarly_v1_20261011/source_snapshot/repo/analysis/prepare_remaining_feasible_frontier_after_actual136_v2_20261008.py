"""Record an evidence-supported finer cross-family proposal; do not claim its controls or quality have run."""
from pathlib import Path
import json,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    score_path=A/'CrossFamily94_official_comparison_v1_20261008/verification.json'
    proof=read(score_path);winner=proof['best'];old_plan=A/'CrossFamily94_round136_plan_v1_20261008.json'
    plan=read(old_plan);assert len(proof['records'])==94 and winner['case']==81
    assert winner['configuration']['group']==4 and winner['configuration']['share']==.5 and winner['configuration']['weight']==.0025
    assert .0025==min(c['amplitude'] for c in plan['new_cases'] if c['amplitude']>0)
    shares=[.25,.375,.5,.625,.75]
    amplitudes=[.00025,.0005,.00075,.001,.00125,.0015,.00175,.002,.00225,.00275,.003,.00325]
    cases=[{'group':4,'share':share,'amplitude':direction*amplitude} for share in shares for direction in (1,-1) for amplitude in amplitudes]
    assert len(cases)==120 and len({(c['group'],c['share'],c['amplitude']) for c in cases})==120
    previous={(c['group'],c['share'],c['amplitude']) for c in plan['new_cases']}
    assert not previous.intersection((c['group'],c['share'],c['amplitude']) for c in cases)
    proposal=A/'CrossFamilyFine125_round145_proposal_v1_20261008.json'
    create(proposal,{'status':'prepared_bounded_proposal_not_admitted_not_scored_not_dispatched',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':145,
        'evidence':{'actual136_cases':94,'actual136_winner_score':winner['connected_final_score'],
            'best_existing_fully_qualified_round144_score':read(A/'optimization_20261003_r144/calibrated_csv_official.json')['metrics']['final_score'],
            'winner_at_smallest_positive_original_amplitude':True,'selected_components':winner['ordered_native_components']},
        'new_cases':cases,'new_case_count':120,'anchor_rounds':[134,136,141,144],
        'zero_amplitude_identity_count':1,'expected_scored_cases':125,
        'scientific_stage_base_round':134,'operation':'retune_the_existing_cross_family_stage_over_exact_complete134_parent',
        'final_selection_compares_all125_cases_including_all_qualified_anchor_schemes':True,
        'heads':{name:plan['heads'][name] for name in winner['ordered_native_components']},
        'new_native_fits_needed':0,'required_before_quality':['all_anchor_full_QA_and_actual_main_receipts',
            'freeze_complete_145_registry_scoring_candidate_and_QA_receivers',
            'new_actual120_full_OOF_transform_and360_cold_prefix_controls',
            'actual_native_independent_mixture_controls_for_all_five_shares',
            'original_official_scoring_runtime_and_TRAIN_mature_return_mapping_gates',
            'complete_prospective_generated_receiver_preflights'],
        'required_after_selection':['source_parameters_and_return_mapping_freeze_before_future_X',
            'two_complete1599600_native_independent_replays_reload_and_cold80',
            'causal_window_audit','all_original_six_ranking_views_QA','complete_main_publication'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),score_path,old_plan,A/'CrossFamily94_actual_controls_index_v4_20261008.json']},
        'new_official_scores':0,'new_candidate_inference':0,'actual_test_labels_read':False,
        'source_receivers_and_native_controls_not_yet_prepared':True,'finite_grid_does_not_prove_exhaustion':True})
    create(A/'remaining_feasible_optimization_frontier_v2_20261008.json',{
        'status':'further_feasible_direction_supported_by_actual_new_score_and_existing_native_bank',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00',
        'actual13694_official_scoring_completed':True,'actual136_future_replays_and_sealing_completed':True,
        'actual136_full_ranking_QA_and_main_still_require_actual_terminal_proof':True,
        'pending137_to141_cases':308,'pending_five_round120_receiver_sources_preflight_passed':True,
        'next_uncovered_direction':str(proposal),'proposal_sha256':sha(proposal),
        'no_additional_training_needed_for_next125_case_proposal':True,
        'global_search_boundary_proven':False,'global_compute_boundary_proven':False,
        'resource_limits_are_specific_observations_not_an_exhaustion_claim':True,
        'new_official_scores_by_frontier_record':0,'test_labels_read':False})
    print('Evidence-backed125-case proposal prepared; no new quality or inference claimed.',flush=True)
if __name__=='__main__':main()
