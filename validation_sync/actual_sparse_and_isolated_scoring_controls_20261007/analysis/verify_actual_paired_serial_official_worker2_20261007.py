"""Measure four uncached full official calls at the available RAM budget on two already-scored vectors."""
from pathlib import Path
from types import SimpleNamespace
import os,sys,time,hashlib,threading,gc
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create

def numeric_sha(x):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(x)).cast('B')).hexdigest()

def main():
    import numpy as np,polars as pl,psutil,evaluate
    import cross_round_official_score_reuse_20261003 as dispatcher
    from score_calibrated_candidates_20261003 import score
    from nonflag_residual_HGB_CDF_transform_20261007 import prepare,apply_prepared
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as installed_percentile
    from cached_official_spearman_runtime_20261007 import installed as installed_ic
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    while psutil.virtual_memory().available<8.5*2**30:time.sleep(10)
    slot=int(sys.argv[1]);assert slot in (0,1)
    out=A/f'actual_paired_serial_uncached_scoring_controls_20261007/worker{slot}';assert not out.exists();out.mkdir()
    cases=[A/'nonflag_RFF12876_official_comparison_v1_20261007/case01_official.json',
           A/'nonflag_RFF12876_official_comparison_v1_20261007/case05_official.json']
    original_scoring=A/'optimization_20261003_r95/scoring_validation_only'
    parent_path=A/'optimization_20261003_r121/selected_validation.npy'
    reference_path=A/'optimization_20261003_r106/selected_validation.npy'
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    bank=A/'nonflag_residual_RFF128_bank10_20261007';residual_path=bank/'nonflag_residual_rff128_g003125/nonflag_oof_predictions.npy'
    paths=[Path(__file__),*cases,parent_path,reference_path,residual_path,frame_path,ROOT/'evaluate.py',ROOT/'run.py',
           ROOT/'后续选模标准.md',ROOT/'data/raw/训练集.csv',A/'score_calibrated_candidates_20261003.py',
           A/'nonflag_residual_HGB_CDF_transform_20261007.py',A/'official_validation_csv_parse_cache_20261003.py',
           A/'official_date_index_dataframe_adapter_20261007.py',A/'all_forecast_percentile_runtime_20261007.py',
           A/'cached_official_spearman_runtime_20261007.py',A/'connected_validation_20261002/return_mapping.py',
           *[original_scoring/n for n in ('测试集_X.csv','测试集_Y.csv')],
           *[Path(read(p)['official_score_cache']['official_metrics_source']) for p in cases]]
    pins={str(p):sha(p) for p in paths}
    create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'actual_uncached_calls_expected':2,
        'already_scored_vectors':2,'actual_start_RAM_GiB':psutil.virtual_memory().available/2**30,
        'original_scoring_formula_mapping_and_prediction_bits_unchanged':True,'new_distinct_quality_scores':0,'test_labels_read':False})
    records=[];cache={};original_dispatch=dispatcher.score
    def fresh(ctx,mapped):
        csv=ctx.scoring/'submission.csv'
        ctx.frame.select(['ts_code','trade_date']).with_columns(pl.Series('pred',mapped)).write_csv(csv,float_precision=17)
        metrics={k:float(v) for k,v in evaluate.evaluate(str(csv),str(ctx.scoring)).items()}
        ctx.actual_uncached={'mapped_numeric_sha256':numeric_sha(mapped),'csv_sha256':sha(csv)}
        ctx.last_cross_round_official_reuse={'cross_round_cache_hit':False,'forced_uncached_control':True}
        return metrics
    dispatcher.score=fresh
    try:
        with LockedReadHashCache(pins) as scope:
            frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
            dates,flags,valid=[frame[c].to_numpy() for c in ('trade_date','flag_limit_up','price_valid')]
            assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
            parent=np.load(parent_path,mmap_mode='r');reference=np.load(reference_path,mmap_mode='r')
            residual=np.load(residual_path,mmap_mode='r');prepared=prepare(reference,dates,flags,valid,'all_current_raw_forecasts')
            folder=out/'scoring_validation_only';folder.mkdir()
            for name in ('测试集_X.csv','测试集_Y.csv'):os.link(original_scoring/name,folder/name)
            ctx=SimpleNamespace(frame=frame,dates=dates,scoring=folder)
            for repeat,order in enumerate(((slot,),(slot,))):
                for index in order:
                    row=read(cases[index]);cfg=row['configuration']
                    values=np.asarray(parent) if cfg['model'] is None else apply_prepared(parent,reference,flags,residual*cfg['residual_sign'],cfg['weight'],prepared)
                    assert numeric_sha(values)==row['prediction_numeric_bytes_sha256']
                    expected=read(row['official_score_cache']['official_metrics_source'])
                    event=threading.Event();samples=[];process=psutil.Process()
                    def sample():
                        while not event.is_set():
                            samples.append((time.perf_counter(),psutil.virtual_memory().available/2**30,process.memory_info().rss/2**30))
                            event.wait(.2)
                    worker=threading.Thread(target=sample,daemon=True);worker.start();start=time.perf_counter()
                    try:
                        with installed_percentile(),installed_ic(cache),installed(ctx.scoring/'submission.csv'):
                            metrics=score(ctx,values)
                    finally:event.set();worker.join()
                    assert metrics==row['metrics']==expected['metrics']
                    assert ctx.actual_uncached['csv_sha256']==expected['scope']['submission_csv_sha256']
                    item={'index':index,'repetition':repeat,'elapsed_seconds':time.perf_counter()-start,
                        'metrics':metrics,**ctx.actual_uncached,'input_prediction_numeric_sha256':numeric_sha(values),
                        'minimum_sampled_available_RAM_GiB':min(r[1] for r in samples),
                        'peak_sampled_own_RSS_GiB':max(r[2] for r in samples),
                        'sampling_period_seconds':.2,'sampled_RSS_is_not_system_peak_commit':True,
                        'all8_historical_metrics_and_full_CSV_bytes_exact':True,'new_distinct_quality_scores':0,'test_labels_read':False}
                    create(out/f'case{index}_repeat{repeat}.json',item);records.append(item)
                    print({'index':index,'repetition':repeat,'elapsed_seconds':item['elapsed_seconds'],
                           'minimum_RAM_GiB':item['minimum_sampled_available_RAM_GiB']},flush=True)
                    del values;gc.collect()
            scope.reverify()
    finally:dispatcher.score=original_dispatch
    assert len(records)==2
    create(out/'verification.json',{'status':'passed_actual2_uncached_full_official_calls_in_isolated_process_all8_CSV_and_input_bits_exact',
        'input_sha256':pins,'actual_uncached_official_calls':2,'records':records,
        'minimum_sampled_available_RAM_GiB':min(r['minimum_sampled_available_RAM_GiB'] for r in records),
        'peak_sampled_own_RSS_GiB':max(r['peak_sampled_own_RSS_GiB'] for r in records),
        'new_distinct_quality_scores':0,'new_native_fits':0,'all_future_model_memory_phases_not_qualified_by_this_control':True,
        'user_applications_stopped':0,'original_GPU_or_queue_stopped':False,'test_labels_read':False,'worker_pid':psutil.Process().pid,'worker_slot':slot,'all_shared_cache_donor_reads_bypassed':True})
if __name__=='__main__':main()
