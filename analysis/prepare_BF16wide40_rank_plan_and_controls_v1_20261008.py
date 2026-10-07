"""Freeze all3 role masks and12 weights before looking at any new neural quality score."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    native = A/'neural_BF16_micro8192_native_v1_20261008.py'
    synthetic = A/'BF16_rank_CDF_synthetic_preflight_v1_20261008/verification.json'
    assert read(synthetic)['status']=='passed_actual18_synthetic_BF16_rank_CDF_roles_and36_day_prefixes'
    plan = A/'BF16wide40_round135_plan_v1_20261008.json'
    create(plan, {'status':'frozen_future40_complete_parent_BF16_rank_CDF_comparisons_before_any_new_quality_score',
        'round':135,'model_name':'rank_MLP16384_BF16_micro8192_32epochs',
        'native_recipe':'own_mature_BF16_micro8192_weighted_accum_v1_20261008',
        'actual_annual_bank':'E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008',
        'qualified_anchor_rounds':[112,133,134],
        'roles':['all_valid','nonflag_valid','flag_valid'],
        'weights':[.0025,.005,.01,.025,.05,.075,.1,.2,.35,.5,.75,1.],
        'expected_scored_records':40,'expected_transform_controls':37,'expected_cold_controls':111,
        'rank_universe':'all_current_raw_forecasts','first2020_active':True,
        'new_stage_position':'after_complete_qualified_parent_all_flag_nonflag_and_historical_branches',
        'transform':'inverseCDF_parent((1-weight)*parent_day_average_rank_over_N+weight*neural_day_average_rank_over_N)',
        'invalid_and_declared_unselected_parent_raw_values_preserved':True,
        'zero_weight_is_exact_whole_parent_identity':True,
        'additional_model_fits_by_this_comparison':0,
        'whole_native_independent_replay_and_candidate_sources_required_before_scoring':True,
        'select_by_actual_official_continuous_S_all8_metrics_no_extra_quality_gates':True,
        'selection_bias_uncorrected':True,'test_labels_read':False,'global_exhaustion_claimed':False})
    paths = [Path(__file__),native,synthetic,plan,
        A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
        A/'verify_BF16_rank_CDF_full37_v1_20261008.py',
        A/'verify_BF16_rank_CDF_synthetic_v1_20261008.py',
        A/'neural_BF16_independent_forward_v1_20261008.py',
        A/'verify_BF16_full5_independent_GPU_v2_20261008.py']
    pins = {str(p):sha(p) for p in paths}
    row = start('BF16_rank_CDF_actual_full37_controls_v1_20261008','verify_BF16_rank_CDF_full37_v1_20261008.py',[],pins)
    create(A/'actual_BF16wide40_rank_plan_and_full37_hidden_launch_v1_20261008.json', {
        'status':'frozen_actual40_grid_and_started_dependency_gated_full37_and111_controls',
        'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False,
        'full135_source_admission_selected_future_inference_and_QA_and_main_pending':True})
    print('40-case BF16 rank mixing grid frozen; actual37/111 controls await complete6 fits and134.',flush=True)


if __name__ == '__main__':main()
