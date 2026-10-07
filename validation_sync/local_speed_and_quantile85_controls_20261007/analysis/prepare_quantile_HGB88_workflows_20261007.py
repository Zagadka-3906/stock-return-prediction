"""Compile fresh quantile scorer and frozen native candidate pipeline before admission."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    files={
      'run_flagged_HGB_small_amplitude88_official_comparison_v4_20261007.py':'run_quantile_HGB88_official_comparison_20261007.py',
      'prepare_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007.py':'prepare_quantile_HGB88_selected_candidate_20261007.py',
      'seal_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007.py':'seal_quantile_HGB88_selected_candidate_20261007.py'}
    maps={**{o[:-3]:n[:-3] for o,n in files.items()},
      'flagged_HGB_small_amplitude88_selected_release_v4_20261007':'quantile_HGB88_selected_release_20261007',
      'flagged_HGB_small_amplitude88_official_comparison_v4_20261007':'quantile_HGB88_official_comparison_20261007',
      'flagged_HGB_small_amplitude88_scores_v4_github_20261007':'quantile_HGB88_scores_github_20261007',
      'flagged_HGB_small_amplitude88_transform_preflight_20261007':'quantile_HGB88_transform_preflight_20261007',
      'flagged_HGB_small_amplitude88_pre_inference_source_freeze_v4_20261007':'quantile_HGB88_pre_inference_source_freeze_20261007',
      'flagged_HGB_small_amplitude88_plan_20261007':'quantile_HGB88_plan_20261007',
      'candidates/flagged_HGB_small_amplitude88_20261007':'candidates/quantile_HGB88_20261007',
      'cpu_conditional_residual_hgb_bank20_20261007':'quantile_HGB_native_bank20_v2_20261007',
      'cpu_conditional_residual_hgb_codec_20261007':'quantile_HGB_large_batch_codec_20261007',
      'predict_refined_flagged_CPU_HGB_scheme_20261007':'predict_refined_quantile_HGB_scheme_v2_20261007',
      'refined_flagged_HGB_native_replay_verification.json':'refined_quantile_HGB_native_replay_verification.json',
      'flagged_HGB_small_amplitude88_official_comparison_v4':'quantile_HGB88_official_comparison',
      'flagged_HGB_small_amplitude88_scores_main_publication_v4':'quantile_HGB88_scores_main_publication',
      'flagged_HGB_small_amplitude88_selected_candidate_preparation_v4':'quantile_HGB88_selected_candidate_preparation',
      'flagged_HGB_small_amplitude88_transform_preflight':'quantile_HGB_full85_transform_preflight',
      'passed_actual85_full5635800_flagged_HGB_small_amplitude_independent_oracle_and_cold80_260_975_controls':'passed_actual85_full5635800_quantile_HGB_independent_oracle_and_cold80_260_975_controls',
      'passed_actual88_flagged_HGB_small_amplitude_full_official_comparisons':'passed_actual88_quantile_HGB_full_official_comparisons',
      'passed_actual_selected_new_flagged_HGB88_candidate_inference':'passed_actual_selected_new_quantile_HGB88_candidate_inference',
      'passed_frozen_flagged_HGB88_complete_native_parent_independent_and_cold80':'passed_frozen_quantile_HGB88_complete_native_parent_independent_and_cold80',
      'passed_actual_pre_inference_source_snapshot_and_refined_flagged_HGB88_native_candidate':'passed_actual_pre_inference_source_snapshot_and_quantile_HGB88_native_candidate',
      'frozen_selected_flagged_HGB88_before_future_inference':'frozen_selected_quantile_HGB88_before_future_inference',
      '(112,114,115)':'(112,117,118)','((112,23),(114,25),(115,26))':'((112,23),(117,28),(118,29))',
      'CPU_ELASTIC44_round114_full_registration_v3':'weighted_HGB340_round117_full_registration',
      'protected_upper_pool_HGB66_round115_full_registration_v5':'HGB_quarter_numeric28_round118_full_registration',
      'actual_iterations\']==64':'actual_iterations\']==128',
      'QA27_and_main_pending':'QA30_and_main_pending','full116_qualification_pending':'full119_qualification_pending'}
    paths=[Path(__file__)]
    for old,new in files.items():
        s=substitute((A/old).read_text(encoding='utf8'),maps)
        if old.startswith('run_'):
            s=s.replace('    records=[]','    records=[];target_rank_cache={}',1)
            needle="    from official_date_index_dataframe_adapter_20261007 import installed"
            assert needle in s
            s=s.replace(needle,needle+"\n    from all_forecast_percentile_runtime_20261007 import installed as installed_percentile\n    from cached_official_spearman_runtime_20261007 import installed as installed_ic")
            needle="            with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,values)"
            assert needle in s
            s=s.replace(needle,"            with installed_percentile() as percentile_runtime, installed_ic(target_rank_cache) as ic_runtime:\n                with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,values)")
            s=s.replace("'official_date_index_runtime':dict(date_index),","'official_date_index_runtime':dict(date_index),'all_row_percentile_runtime':percentile_runtime,'scoring_only_spearman_runtime':ic_runtime,")
            needle="ROOT/'evaluate.py',ROOT/'后续选模标准.md'"
            assert needle in s
            s=s.replace(needle,"A/'all_forecast_percentile_runtime_20261007.py',A/'cached_official_spearman_runtime_20261007.py',\n        A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py',\n        A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json',"+needle)
        elif old.startswith('prepare_'):
            needle="assert info['year']==2025 and info['actual_iterations']==64"
            # The map above already updates the iteration guard.
            assert "assert info['year']==2025 and info['actual_iterations']==128" in s
            s=s.replace("assert info['year']==2025 and info['actual_iterations']==128", "assert info['year']==2025 and info['actual_iterations']==128\n        assert info['parameters']['loss']=='quantile' and info['parameters']['quantile'] in (.25,.75)")
            s=s.replace("not n.startswith('flagged_residual_hgb')", "not n.startswith(('flagged_residual_hgb','flagged_quantile_hgb'))")
        p=A/new;assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf8');paths += [A/old,p]
    create(A/'quantile_HGB88_workflow_source_preparation_20261007.json',{'status':'compiled_fresh_three88_quantile_workflows_before_full119_admission','input_sha256':{str(p):sha(p) for p in paths},'new_quality_scores':0,'new_native_fits':0,'full119_pipeline_and_actual85_admission_still_required':True})
if __name__=='__main__':main()
