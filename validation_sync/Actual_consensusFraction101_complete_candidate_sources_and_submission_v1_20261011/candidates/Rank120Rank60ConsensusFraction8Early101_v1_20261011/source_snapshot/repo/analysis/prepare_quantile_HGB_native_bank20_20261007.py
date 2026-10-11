"""Predeclare quantile20 native fits and their future88 comparisons before any fitting."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    old_plan=A/'cpu_conditional_residual_hgb_bank20_plan_20261007.json';prior=read(old_plan)
    configs={f'flagged_quantile_hgb{leaf}_q{int(q*100)}':{'loss':'quantile','quantile':q,'max_leaf_nodes':leaf} for q in (.25,.75) for leaf in (7,15)}
    plan=A/'quantile_HGB_native_bank20_plan_20261007.json';assert not plan.exists()
    create(plan,{'status':'predeclared_unfitted20_CPU_quantile_HGB_native_models',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'teacher_qualified_round':106,'configurations':configs,
      'fixed_parameters':{**prior['fixed_parameters'],'max_iter':128,'min_samples_leaf':64},
      'CPU_threads':4,'annual_native_fit_years':[2021,2022,2023,2024],'final_native_fit_year':2025,
      'prospective_native_model_fits':20,'first2020_identity':True,'feature_count':64,
      'features':'63 supplied-field-derived features plus qualified106 current forecast average_rank/N',
      'target':'mature past flagged y_rank+0.5 minus qualified106 current forecast percentile',
      'preprocessing':'finite median fill mean/std clip10 on corresponding mature past training window only',
      'early_stopping':False,'test_labels_read':False,'new_quality_scores':0,
      'difference_from_prior_squared_absolute_bank':'quantile loss .25 and .75,128 iterations,min leaf64; prior64 iterations,min leaf256',
      'later_comparison_parent_candidates':[112,117,118],'later_planned_round':119,
      'later_weights':[.0003125,.000625,.00125,.0025,.005,.0075,.01,.015,.02,.03,.04,.05],
      'later_single_heads_plus_equal_q25_equal_q75_all4_mean':7,'later_expected_official_records':88,
      'later_official_scoring_requires_complete119_source_pipeline_and85_full_controls':True,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old_plan,A/'train_cpu_conditional_residual_hgb_bank20_20261007.py',
        A/'cpu_conditional_residual_hgb_codec_20261007.py',A/'verify_cpu_conditional_residual_hgb_codec_preflight_20261007.py']},
      'all_training_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
      'global_direction_or_resource_exhaustion_not_established':True})
    routes={
      'cpu_conditional_residual_hgb_bank20_plan_20261007':'quantile_HGB_native_bank20_plan_20261007',
      'cpu_conditional_residual_hgb_bank20_admission_20261007':'quantile_HGB_native_bank20_admission_20261007',
      'cpu_conditional_residual_hgb_codec_preflight_20261007':'quantile_HGB_codec_preflight_20261007',
      'verify_cpu_conditional_residual_hgb_codec_preflight_20261007':'verify_quantile_HGB_codec_preflight_20261007',
      'cpu_conditional_residual_hgb_bank20_20261007':'quantile_HGB_native_bank20_20261007',
      'passed_actual_four_historical_CPU_HGB_codec_controls':'passed_actual_four_historical_quantile_HGB_codec_controls',
      'passed_actual20_CPU_conditional_HGB_native_independent_numpy_and_prefix_controls':'passed_actual20_CPU_quantile_HGB_native_independent_numpy_and_prefix_controls'}
    prototype=A/'verify_cpu_conditional_residual_hgb_codec_preflight_20261007.py'
    preflight=save('verify_quantile_HGB_codec_preflight_20261007.py',substitute(prototype.read_text(encoding='utf8'),routes))
    old=A/'train_cpu_conditional_residual_hgb_bank20_20261007.py';text=substitute(old.read_text(encoding='utf8'),routes)
    text=text.replace('CPU-only small histogram regressors','CPU-only .25/.75 quantile histogram regressors')
    needle="    features = read(ROOT / 'data/feature_manifest.json')['features']";assert text.count(needle)==1
    text=text.replace(needle,"    admitted=read(A/'quantile_HGB_native_bank20_admission_20261007.json')\n    assert admitted['status']=='passed_actual4_quantile_codec_fits_and20_mature_window_plan_source_admission'\n    for p,d in admitted['input_sha256'].items():assert sha(p)==d,p\n"+needle)
    trainer=save('train_quantile_HGB_native_bank20_20261007.py',text)
    create(A/'quantile_HGB_native_bank20_source_preparation_20261007.json',{'status':'compiled_unlaunched_quantile_codec4_and_mature_bank20_training_sources',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),plan,prototype,preflight,old,trainer]},'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
