"""Evidence-based remaining directions; this is a manual-resume plan, never an autostart request."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    sources=[Path(__file__),A/'actual_single_host_resource_boundary_after_resume_20261007.json',A/'actual_new_streamed_RFF_and_empirical_Bayes_scientific_identity_20261007.json',
      A/'nonflag_RidgeFine52_official_comparison_v1_20261007/verification.json',A/'github_validation_sync_main_20261005/round128_receipt.json',
      A/'nonflag_RFF128StreamMid76_plan_20261007.json',A/'nonflag_EmpiricalBayes40_plan_20261007.json',A/'nonflag_RidgeMicro40_plan_20261007.json']
    actual=read(sources[2]);assert actual['status']=='recorded_actual20_new_mature_native_fits_and_explicit_solver_identities'
    receipt=read(sources[4]);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['official_score']==.45111336969856725
    current=[{'round':number,'family':family,'actual_closed':(A/f'optimization_20261003_r{number}/full_registration_execution.json').exists(),
      'completed_case_records':len(list((A/f'{family}_official_comparison_v1_20261007').glob('case*_official.json')))}
      for number,family in [(129,'nonflag_RFF128StreamMid76'),(130,'nonflag_EmpiricalBayes40'),(131,'nonflag_RidgeMicro40')]]
    create(A/'remaining_feasible_optimization_frontier_manual_resume_20261007.json',{
      'status':'proposals_supported_by_existing_native_banks_and_actual_resource_snapshot_not_exhaustion_claim','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'current_actual_queued_or_running_rounds':current,'fully_qualified_best_at_record':{'round':128,'official_score':receipt['official_score'],'receipt':str(sources[4])},
      'directions':[
        {'method':'negative_direction_empirical_Bayes_scalar_diagonal_and_equal_mean',
          'coverage_gap':'current_empirical_Bayes40_plan_has_only_positive_residual_direction',
          'existing_native_bank':'nonflag_residual_EmpiricalBayes64_bank10_20261007','additional_native_fits_needed':0,
          'required_before_scoring':['fresh_signed_native_and_independent_stage','native3_sign_controls','full37_CDF_and111_cold_controls','actual_qualified_parent_source_admission'],
          'proposed_official_cases':40,'not_frozen_not_scored_not_dispatched':True},
        {'method':'cross_family_Ridge_RFF128_and_empirical_Bayes_residual_ensembles',
          'coverage_gap':'current_new_plans_have_within_family_equal_means_but_no_cross_family_blends',
          'existing_native_banks':['nonflag_residual_Ridge_bank10_20261007','nonflag_residual_RFF128StreamMid_bank10_20261007','nonflag_residual_EmpiricalBayes64_bank10_20261007'],
          'additional_native_fits_needed':0,'proposed_component_shares':[.25,.5,.75],
          'requirements':['immutable_component_order_and_explicit_codec_per_component','own_year_mature_labels_only','independent_native_and_JSON_decoder','full5635800_CDF_and_cold_controls','complete_frozen_selected1599600_two_replays_and_QA_and_main'],
          'not_frozen_not_scored_not_dispatched':True},
        {'method':'sparse_L1_or_ElasticNet64_mature_residual_models',
          'coverage_gap':'new_current_linear_families_are_fixed_L2_or_learned_Gaussian_shrinkage',
          'existing_feature_and_target_caches_reusable_only_after_exact_window_and_label_hash_checks':True,
          'additional_native_fits_needed':10,'bounded_fit_recipe_and_independent_codec_not_yet_admitted':True,
          'not_frozen_not_scored_not_dispatched':True},
        {'method':'GPU_epoch_checkpoint_validation_and_more_memory_bounded_neural_recipes',
          'coverage_gap':'actual_CPU32_checkpoint_equivalence_is_passed_but_actual_GPU_equivalence_is_not_verified',
          'actual_original_saved_years':[2020,2021],'current_original_year2022_unsaved_work_will_not_survive_poweroff':True,
          'requirements':['user_manual_resume','sufficient_actual_free_GPU_memory','fresh_process_original_vs_epoch_restart_equivalence','new_recipe_scientific_freeze_if_batch_or_precision_changes'],
          'do_not_silently_reuse_old_annual_weights_for_changed_training_recipe':True,'not_frozen_not_scored_not_dispatched':True}],
      'global_optimization_boundary_proven':False,'resource_boundary_is_specific_to_observed_original_large_GPU_recipe':True,
      'no_performance_guarantee_for_unexecuted_directions':True,'continue_only_after_actual_user_message':True,
      'automatic_morning_restart_enabled':False,'fixed_tonight_stop_at_local':'2026-10-07T23:55:00+08:00',
      'new_quality_scores':0,'test_labels_read':False,'input_sha256':{str(p):sha(p) for p in sources}})

if __name__=='__main__':main()
