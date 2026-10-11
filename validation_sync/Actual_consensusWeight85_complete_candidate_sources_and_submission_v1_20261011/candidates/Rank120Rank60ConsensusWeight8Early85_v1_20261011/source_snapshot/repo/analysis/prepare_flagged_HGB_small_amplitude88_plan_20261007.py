"""Declare an uncovered small-amplitude grid using existing20 native models, without scoring."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    from refine_flagged_HGB_compatible_parent_transform_20261007 import compatible
    operator=A/'refine_flagged_HGB_compatible_parent_transform_20261007.py'
    reference=read(ROOT/'candidates/simplex_residual47_20261006/verification.json')['whole_scheme_graph']
    parent=read(ROOT/'candidates/optimization_20261003_r112/verification.json')['whole_scheme_graph']
    assert compatible(parent,reference)
    wrong=dict(parent);wrong['undeclared_extra_stage']={'weight':.5};assert not compatible(wrong,reference)
    old=read(A/'cpu_conditional_residual_hgb_bank20_plan_20261007.json');names=list(old['configurations'])
    ensembles={'equal_mean_squared':names[:2],'equal_mean_absolute':names[2:],'equal_mean_all_four':names}
    weights=[.00125,.0025,.005,.0075,.01,.0125,.015,.02,.025,.03,.035,.04]
    assert len(weights)==len(set(weights))==12
    plan=A/'flagged_HGB_small_amplitude88_plan_20261007.json';assert not plan.exists()
    create(plan,{'status':'predeclared_unscored_flagged_HGB_small_amplitude_and_ablation_grid',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'planned_round':116,'planned_wave':399,'preceding_round':115,
        'qualified_anchor_rounds':[112,114,115],'actual_comparison_parent_choice':'highest official S among complete qualified112_114_115; exact tie earliest',
        'actual_scheme_base_choice':'highest official S among112_114_115 whose graph is exactly106 core plus optional flagged_HGB and lower_pool_HGB; exact tie earliest',
        'structural_compatibility_not_an_extra_performance_elimination_gate':True,
        'all_qualified_anchors_remain_candidates_even_if_incompatible_with_this_specific_branch_refinement':True,
        'fixed_reference_training_teacher_round':106,'reference_core_exact_except_rebased_file_paths':True,
        'current112_reference_core_compatibility_checked':True,'unknown_extra_graph_stage_rejected':True,
        'single_native_heads':names,'ensembles':ensembles,'weights':weights,'universe':'all_current_raw_forecasts',
        'nonanchor_records':85,'expected_scored_records':88,'explicit_ablation':'remove_flagged_HGB: overwrite flagged values with unmodified106 reference; retain complete parent nonflag values',
        'existing_native_bank':'cpu_conditional_residual_hgb_bank20_20261007','existing_native_fits':20,'new_native_fits':0,
        'first2020_flag_branch_identity':True,'training_feature_teacher_remains_exact_qualified106':True,
        'graph_refinement':'replace existing conditional_flag_CPU_HGB_residual_CDF native heads/weight or remove for zero; preserve optional lower_pool_HGB after it',
        'nonflag_complete_parent_output_bits_unchanged':True,'pool_and_transform_use_current_forecasts_flags_price_valid_only':True,
        'validation_controls':'full5635800 independentPandas percentile/CDF, cold80_260_975, parent original branch reproduction, all8 original official scores',
        'selection':'highest complete original official mapped2020_2024 score; no extra Top worst_year or significance gate',
        'new_scheme_freeze_full1599600_native_independent_two_replays_cold80_CSV_and_full_QA27_main_required':True,
        'exact_existing_candidate_reuse_requires_all_validation_bits8_metrics_graph_parameters_sealed_source_bytes_original_freeze_and0new_inference':True,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),operator,A/'conditional_residual_mlp_CDF_transform_20261007.py',
            A/'cpu_conditional_residual_hgb_bank20_plan_20261007.json',A/'cpu_conditional_residual_hgb_bank20_20261007/verification.json',
            ROOT/'candidates/optimization_20261003_r112/verification.json',ROOT/'candidates/simplex_residual47_20261006/verification.json']},
        'selection_bias_uncorrected':True,'test_labels_read':False,'new_quality_scores':0,
        'global_feasible_direction_or_resource_exhaustion_claimed':False})
    print({'declared_records':88,'new_native_fits':0,'new_quality_scores':0},flush=True)


if __name__=='__main__':main()
