"""Prepare seven actual quantile native hooks and accurately report8192 runtime batching."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    old=A/'predict_quantile_HGB_residual_CDF_scheme_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace("'fixed_padded_inference_batch': 256","'original_serialized_state_batch_recipe': 256, 'runtime_fixed_padded_inference_batch': 8192")
    needle='                bundle = joblib.load(native)';assert text.count(needle)==1
    text=text.replace(needle,needle+"\n                assert bundle['model'].n_iter_ == 128 and bundle['model'].loss == 'quantile'\n                assert bundle['model'].quantile == info['parameters']['quantile']\n                state_metadata = ns.read(state)\n                assert state_metadata['quantile'] == info['parameters']['quantile'] and len(state_metadata['trees']) == 128")
    flag=save('predict_quantile_HGB_residual_CDF_scheme_v2_20261007.py',text)
    old_lower=A/'predict_lower_pool_after_quantile_HGB_scheme_20261007.py'
    lower=save('predict_lower_pool_after_quantile_HGB_scheme_v2_20261007.py',old_lower.read_text(encoding='utf8').replace('predict_quantile_HGB_residual_CDF_scheme_20261007',flag.stem))
    old_wrapper=A/'predict_refined_quantile_HGB_scheme_20261007.py'
    wrapper=save('predict_refined_quantile_HGB_scheme_v2_20261007.py',old_wrapper.read_text(encoding='utf8').replace('predict_quantile_HGB_residual_CDF_scheme_20261007',flag.stem).replace('predict_lower_pool_after_quantile_HGB_scheme_20261007',lower.stem))
    prototype=A/'verify_weighted_flagged_HGB_native_hook_v2_20261007.py'
    routes={
      'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007':flag.stem,
      'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007':lower.stem,
      'weighted_flagged_HGB_native_hook_preflight_v2_20261007':'quantile_HGB_native_hook7_preflight_20261007',
      'flagged_HGB_weighted_quarters340_plan_20261007':'quantile_HGB88_plan_20261007',
      'cpu_numerical_HGB_large_batch_codec_v2_20261007':'quantile_HGB_large_batch_codec_20261007',
      'passed_actual28_historical603_weighted_HGB_unique_native_independent_and_whole_day_prefix_controls':'passed_actual7_historical603_quantile_HGB_native_independent_and_whole_day_prefix_controls'}
    text=substitute(prototype.read_text(encoding='utf8'),routes)
    needle="        for name,ordered in plan['ensembles'].items():";assert text.count(needle)==1
    text=text.replace(needle,"        groups={n:[n] for n in plan['single_native_heads']};groups.update(plan['ensembles'])\n        for name,ordered in groups.items():")
    text=text.replace("'actual_native_hook_cases':28","'actual_native_hook_cases':7").replace('Run28 unique-native weighted hooks','Run7 quantile native hooks')
    text=text.replace('native_model_reload_and_controls_count_unique_not_four_repeated_slots','native1_2_4_component_controls_count_matches_declared_mean')
    text=text.replace('lower_after_weighted_parent_source_route_compiled','lower_after_quantile_parent_source_route_compiled')
    check=save('verify_quantile_HGB_native_hook7_20261007.py',text)
    create(A/'quantile_HGB_native_hook7_source_preparation_v2_20261007.json',{'status':'compiled_seven_historical_native_quantile_hook_controls_and128_actual_model_metadata_guards',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,flag,old_lower,lower,old_wrapper,wrapper,prototype,check]},
      'new_native_fits':0,'new_quality_scores':0,'full_parent15_lower_and1599600_future_not_yet_claimed':True})

if __name__=='__main__':main()
