"""Predeclare119 and fresh128-iteration quantile helpers after measured20-model equivalence."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    f=A/'service_owned_workflows_20261006/quantile_HGB_large_batch20_benchmark'
    assert not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='passed'
    measured_path=A/'quantile_HGB_large_batch20_benchmark_20261007/verification.json';measured=read(measured_path)
    assert measured['actual_existing_native_models_tested']==20 and measured['actual_model_repeat_count']==40
    assert measured['native_phase_speedup']>1. and measured['independent_decoder_phase_speedup']>1.
    bank_plan_path=A/'quantile_HGB_native_bank20_plan_20261007.json';bank_plan=read(bank_plan_path)
    heads=list(bank_plan['configurations']);assert len(heads)==4
    ensembles={'equal_mean_q25':[h for h in heads if h.endswith('_q25')],
      'equal_mean_q75':[h for h in heads if h.endswith('_q75')],'equal_mean_all_four':heads}
    assert [len(ns) for ns in ensembles.values()]==[2,2,4]
    plan=A/'quantile_HGB88_plan_20261007.json';assert not plan.exists()
    create(plan,{'status':'predeclared_unscored_quantile_HGB88_complete_parent_refinements',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'planned_round':119,'planned_wave':402,'preceding_round':118,
      'qualified_anchor_rounds':[112,117,118],'single_native_heads':heads,'ensembles':ensembles,
      'weights':bank_plan['later_weights'],'existing_native_bank':'quantile_HGB_native_bank20_v2_20261007',
      'existing_native_fits':20,'expected_native_iterations':128,'new_native_fits_by_comparison':0,
      'universe':'all_current_raw_forecasts','expected_scored_records':88,'nonanchor_records':85,
      'feature_teacher_qualified_round':106,'aggregation':'ordered float64 zero-plus-heads divided by component count; no repeated head slots',
      'explicit_ablation':'remove_flagged_HGB: retain complete nonflag parent and original106 flag predictions',
      'actual_comparison_parent_choice':'highest complete qualified112_117_118 original official S; exact tie earliest',
      'actual_scheme_base_choice':'highest compatible106 core complete qualified112_117_118 original official S; exact tie earliest',
      'incompatible_qualified_anchors_remain_candidates':True,
      'full85_independentCDF_and255_cold_controls_original88_official_metrics_required':True,
      'freeze_before_complete1599600_native_independent_two_replays_cold80_CSV_fullQA30_and_main':True,
      'exact_anchor_reuse_all_validation_bits8_metrics_graph_all_sealed_bytes_and_original_freeze_required':True,
      'all_training_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
      'global_resource_or_direction_exhaustion_not_established':True,'test_labels_read':False,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),bank_plan_path,measured_path,
        A/'quantile_HGB_native_bank20_v2_20261007/verification.json',A/'refine_flagged_HGB_compatible_parent_transform_20261007.py']}})
    source=A/'predict_conditional_CPU_HGB_residual_CDF_scheme_20261007.py';text=source.read_text(encoding='utf8')
    text=text.replace('from cpu_conditional_residual_hgb_codec_20261007 import predict_native, predict_decoded','from quantile_HGB_large_batch_codec_20261007 import predict_native, predict_decoded')
    text=text.replace("info['actual_iterations'] == 64","info['actual_iterations'] == 128")
    needle="                assert info['year'] == 2025 and info['actual_iterations'] == 128";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n                assert info['parameters']['loss'] == 'quantile' and info['parameters']['quantile'] in (.25, .75)")
    text=text.replace('CPU_HGB_residual_CDF_native_replay_verification.json','quantile_HGB_residual_CDF_native_replay_verification.json')
    flag=save('predict_quantile_HGB_residual_CDF_scheme_20261007.py',text)
    source_lower=A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007.py';text=source_lower.read_text(encoding='utf8')
    text=text.replace('predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',flag.name)
    lower=save('predict_lower_pool_after_quantile_HGB_scheme_20261007.py',text)
    source_wrapper=A/'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007.py';text=source_wrapper.read_text(encoding='utf8')
    text=text.replace('predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007',flag.stem).replace('predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007',lower.stem)
    text=text.replace('weighted_refined_flagged_HGB_native_replay_verification.json','refined_quantile_HGB_native_replay_verification.json')
    text=text.replace('passed_actual_weighted_full_refined_graph_saved_native_independent_two_replays_and_cold80','passed_actual_quantile_full_refined_graph_saved_native_independent_two_replays_and_cold80')
    wrapper=save('predict_refined_quantile_HGB_scheme_20261007.py',text)
    create(A/'quantile_HGB88_native_source_preparation_20261007.json',{'status':'compiled_fresh_quantile128_unique1_to4_complete_native_helpers_before_future_inference',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),plan,flag,lower,wrapper,source,source_lower,source_wrapper,
        A/'quantile_HGB_large_batch_codec_20261007.py',measured_path]},'new_native_fits':0,'new_quality_scores':0,
      'actual_complete1599600_future_candidate_not_yet_claimed':True})

if __name__=='__main__':main()
