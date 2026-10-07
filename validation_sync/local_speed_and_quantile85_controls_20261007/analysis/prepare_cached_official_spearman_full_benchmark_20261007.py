"""Prepare isolated scoring-only twelve-call equivalence and throughput benchmark."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,create,sha
def replace(text,old,new):
    assert old in text,old
    return text.replace(old,new)
def main():
    edge=A/'exact_cached_official_spearman_v2_edge_preflight_20261007/verification.json'
    assert read(edge)['status']=='passed_actual24_SciPy_statistic_pvalue_edge_and_fallback_controls'
    source=A/'benchmark_all_forecast_percentiles_full_scoring_20261007.py'
    s=source.read_text(encoding='utf8')
    s=replace(s,"from exact_numpy_all_forecast_percentiles_20261007 import install", "from exact_numpy_all_forecast_percentiles_20261007 import install\n    from exact_cached_official_spearman_v2_20261007 import installed as installed_spearman\n    from contextlib import nullcontext")
    s=replace(s,"service_owned_workflows_20261006/all_forecast_percentiles_full_benchmark", "service_owned_workflows_20261006/all_forecast_percentiles_full_official_scoring_benchmark")
    # Require the already-completed full percentile equivalence, independently of service naming.
    s=replace(s,"    while owned(read(service/'native_launch.json')):time.sleep(10)\n    assert read(service/'service_execution.json')['status']=='passed'", "    assert read(A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json')['actual_uncached_official_evaluation_calls']==12\n    assert read(A/'exact_cached_official_spearman_v2_edge_preflight_20261007/verification.json')['status']=='passed_actual24_SciPy_statistic_pvalue_edge_and_fallback_controls'")
    s=replace(s,"out=A/'all_forecast_percentiles_full_scoring_benchmark_20261007'", "out=A/'cached_official_spearman_full_scoring_benchmark_20261007'")
    s=replace(s,"A/'exact_numpy_all_forecast_percentiles_20261007.py',A/'score_calibrated_candidates_20261003.py',", "A/'exact_numpy_all_forecast_percentiles_20261007.py',A/'exact_cached_official_spearman_v2_20261007.py',\n        A/'exact_cached_validation_spearman_20261007.py',A/'exact_cached_official_spearman_v2_edge_preflight_20261007/verification.json',\n        A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json',A/'score_calibrated_candidates_20261003.py',")
    s=replace(s,"records=[];old_dispatch=score_dispatch.score", "records=[];old_dispatch=score_dispatch.score;target_cache={}")
    s=replace(s,"if mode=='numpy':operator,restore=install()", "operator,restore=install()")
    s=replace(s,"with installed(ctx.scoring/'submission.csv') as events:metrics=score(ctx,values)", "with installed_spearman(target_cache) if mode=='numpy' else nullcontext(None) as ic_events:\n                                with installed(ctx.scoring/'submission.csv') as events:metrics=score(ctx,values)")
    s=replace(s,"assert events['date_index_lookups']==1212", "assert events['date_index_lookups']==1212\n                        if mode=='numpy':assert ic_events['fast_calls']==1212 and ic_events['fallback_calls']==0 and ic_events['original_official_spearman_identity_restored']")
    s=replace(s,"'percentile_operator_statistics':statistics,", "'percentile_operator_statistics':statistics,'actual_scoped_spearman_statistics':ic_events,")
    s=replace(s,"passed_actual12_uncached_full_official_calls_all_mapped_bits_CSV_bytes_eight_metrics_and_two_orders", "passed_actual12_uncached_full_official_calls_cached_SciPy_Spearman_all_mapped_bits_CSV_bytes_eight_metrics_and_two_orders")
    s=replace(s,"'only_return_mapping_all_row_percentile_operator_differs':True,", "'same_verified_fast_percentile_operator_used_in_both_modes':True,'only_official_SciPy_Spearman_runtime_differs':True,\n        'fixed_training_validation_label_ranks_cached_only_within_scoring':True,'target_rank_cache_vectors':len(target_cache),")
    target=A/'benchmark_cached_official_spearman_full_scoring_20261007.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8')
    pins={str(p):sha(p) for p in [Path(__file__),source,target,edge,A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py']}
    create(A/'cached_official_spearman_full_benchmark_source_preparation_20261007.json',{'status':'compiled_scoring_only_full12_actual_benchmark_not_yet_run','input_sha256':pins})
if __name__=='__main__':main()
