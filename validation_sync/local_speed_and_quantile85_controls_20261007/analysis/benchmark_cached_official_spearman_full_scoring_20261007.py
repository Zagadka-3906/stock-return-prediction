"""Twelve uncached official evaluations of already scored vectors; compare mapped bytes and eight metrics."""
from pathlib import Path
from types import SimpleNamespace
import gc
import hashlib
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def numeric_sha(values):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()

def main():
    import numpy as np
    import polars as pl
    import psutil
    import evaluate
    import cross_round_official_score_reuse_20261003 as score_dispatch
    from score_calibrated_candidates_20261003 import score
    from exact_numpy_all_forecast_percentiles_20261007 import install
    from exact_cached_official_spearman_v2_20261007 import installed as installed_spearman
    from contextlib import nullcontext
    from refine_flagged_HGB_compatible_parent_transform_20261007 import prepare,apply_prepared
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    service=A/'service_owned_workflows_20261006/all_forecast_percentiles_full_official_scoring_benchmark'
    assert read(A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json')['actual_uncached_official_evaluation_calls']==12
    assert read(A/'exact_cached_official_spearman_v2_edge_preflight_20261007/verification.json')['status']=='passed_actual24_SciPy_statistic_pvalue_edge_and_fallback_controls'
    while psutil.virtual_memory().available<11*2**30:time.sleep(10)
    out=A/'cached_official_spearman_full_scoring_benchmark_20261007';assert not out.exists();out.mkdir()
    old_scoring=A/'optimization_20261003_r95/scoring_validation_only'
    parent_path=A/'optimization_20261003_r112/selected_validation.npy';reference_path=A/'optimization_20261003_r106/selected_validation.npy'
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    score_folder=A/'flagged_HGB_small_amplitude88_official_comparison_v4_20261007'
    cases=[('qualified112',score_folder/'case00_official.json'),('HGB7_absolute_w0025',score_folder/'case28_official.json'),('HGB15_absolute_w005',score_folder/'case41_official.json')]
    sources=[Path(__file__),A/'exact_numpy_all_forecast_percentiles_20261007.py',A/'exact_cached_official_spearman_v2_20261007.py',
        A/'exact_cached_validation_spearman_20261007.py',A/'exact_cached_official_spearman_v2_edge_preflight_20261007/verification.json',
        A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json',A/'score_calibrated_candidates_20261003.py',
        A/'connected_validation_20261002/return_mapping.py',A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',
        A/'official_validation_csv_parse_cache_20261003.py',A/'official_date_index_dataframe_adapter_20261007.py',
        ROOT/'evaluate.py',ROOT/'run.py',ROOT/'data/raw/训练集.csv',parent_path,reference_path,frame_path,
        A/'all_forecast_percentiles_benchmark_20261007/verification.json',*[old_scoring/n for n in ('测试集_X.csv','测试集_Y.csv')]]
    for label,path in cases:
        row=read(path);sources += [path,Path(row['official_score_cache']['official_metrics_source'])]
        if row['configuration']['model'] is not None:sources.append(A/'cpu_conditional_residual_hgb_bank20_20261007'/row['configuration']['model']/'flagged_oof_predictions.npy')
    pins={str(p):sha(p) for p in sources};create(out/'frozen_before_actual_full_scoring.json',{'input_sha256':pins,
        'already_scored_cases':[str(p) for label,p in cases],'expected_uncached_official_calls':12,
        'original_date_index_and_validation_CSV_parse_adapters_used_in_both_modes':True,
        'all8_metric_and_mapped_array_and_CSV_raw_bits_must_match':True,'new_distinct_model_selection_vectors':0,'new_native_fits':0,'test_labels_read':False})
    records=[];old_dispatch=score_dispatch.score;target_cache={}
    def forced_uncached(ctx,mapped):
        csv=Path(ctx.scoring)/'submission.csv'
        ctx.frame.select(['ts_code','trade_date']).with_columns(pl.Series('pred',mapped)).write_csv(csv,float_precision=17)
        metrics={k:float(v) for k,v in evaluate.evaluate(str(csv),str(ctx.scoring)).items()}
        ctx.last_uncached_evaluation={'mapped_numeric_sha256':numeric_sha(mapped),'csv_sha256':sha(csv),'official_evaluate_called_without_score_capsule_cache':True}
        ctx.last_cross_round_official_reuse={'cross_round_cache_hit':False,'benchmark_forced_uncached_official':True}
        return metrics
    score_dispatch.score=forced_uncached
    try:
        with LockedReadHashCache(pins) as scope:
            frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
            dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
            assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
            parent=np.load(parent_path,mmap_mode='r');reference=np.load(reference_path,mmap_mode='r');prepared=prepare(reference,dates,flags,valid,'all_current_raw_forecasts')
            contexts={}
            for mode in ('original','numpy'):
                folder=out/mode/'scoring_validation_only';folder.mkdir(parents=True)
                for name in ('测试集_X.csv','测试集_Y.csv'):os.link(old_scoring/name,folder/name)
                contexts[mode]=SimpleNamespace(frame=frame,dates=dates,scoring=folder)
            from official_date_index_dataframe_adapter_20261007 import installed
            for label,path in cases:
                original_case=read(path);cfg=original_case['configuration']
                if cfg['model'] is None:values=np.asarray(parent)
                else:
                    residual=np.load(A/'cpu_conditional_residual_hgb_bank20_20261007'/cfg['model']/'flagged_oof_predictions.npy',mmap_mode='r')
                    values=apply_prepared(parent,reference,flags,residual,cfg['weight'],prepared)
                assert numeric_sha(values)==original_case['prediction_numeric_bytes_sha256']
                expected_capsule=read(original_case['official_score_cache']['official_metrics_source'])
                case_records=[]
                for repetition,modes in enumerate((('original','numpy'),('numpy','original'))):
                    for mode in modes:
                        ctx=contexts[mode];gc.collect();restore=None;operator=None
                        operator,restore=install()
                        started=time.perf_counter()
                        try:
                            with installed_spearman(target_cache) if mode=='numpy' else nullcontext(None) as ic_events:
                                with installed(ctx.scoring/'submission.csv') as events:metrics=score(ctx,values)
                        finally:
                            statistics=restore() if restore else None
                        elapsed=time.perf_counter()-started
                        assert events['date_index_lookups']==1212
                        if mode=='numpy':assert ic_events['fast_calls']==1212 and ic_events['fallback_calls']==0 and ic_events['original_official_spearman_identity_restored']
                        assert metrics==original_case['metrics']==expected_capsule['metrics']
                        assert ctx.last_uncached_evaluation['csv_sha256']==expected_capsule['scope']['submission_csv_sha256']
                        item={'case':label,'mode':mode,'repetition':repetition,'elapsed_seconds':elapsed,'metrics':metrics,
                            **ctx.last_uncached_evaluation,'actual_return_mapping':ctx.last_candidate_return_mapping,'percentile_operator_statistics':statistics,'actual_scoped_spearman_statistics':ic_events,
                            'all8_original_case_metrics_exact':True,'all1212_dates_actual_fresh_official_evaluation':True}
                        create(out/f'{label}_{mode}_{repetition}.json',item);records.append(item);case_records.append(item)
                        print({'case':label,'mode':mode,'repetition':repetition,'elapsed_seconds':elapsed},flush=True)
                assert len({r['mapped_numeric_sha256'] for r in case_records})==1 and len({r['csv_sha256'] for r in case_records})==1
            scope.reverify()
    finally:score_dispatch.score=old_dispatch
    assert len(records)==12
    ratios=[]
    for label,path in cases:
        for repetition in (0,1):
            matched={r['mode']:r for r in records if r['case']==label and r['repetition']==repetition}
            ratios.append(matched['original']['elapsed_seconds']/matched['numpy']['elapsed_seconds'])
    create(out/'verification.json',{'status':'passed_actual12_uncached_full_official_calls_cached_SciPy_Spearman_all_mapped_bits_CSV_bytes_eight_metrics_and_two_orders',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_uncached_official_evaluation_calls':12,
        'all_full_rows_days_stocks':[5635800,1212,4650],'median_full_mapping_and_official_score_phase_speedup':float(np.median(ratios)),
        'date_index_and_parse_cache_math_unchanged_in_both_modes':True,'same_verified_fast_percentile_operator_used_in_both_modes':True,'only_official_SciPy_Spearman_runtime_differs':True,
        'fixed_training_validation_label_ranks_cached_only_within_scoring':True,'target_rank_cache_vectors':len(target_cache),
        'new_distinct_model_selection_vectors':0,'new_native_fits':0,'test_labels_read':False,'whole_goal_speedup_not_claimed':True})
    print({'status':'passed','uncached_full_evaluations':12,'phase_speedup':float(np.median(ratios))},flush=True)

if __name__=='__main__':main()
