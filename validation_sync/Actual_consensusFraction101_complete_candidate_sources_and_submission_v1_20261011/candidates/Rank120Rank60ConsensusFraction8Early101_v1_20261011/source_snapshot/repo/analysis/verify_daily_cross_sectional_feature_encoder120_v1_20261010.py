"""Independent scalar and Pandas groups, row permutation, full-day causal prefixes and real TRAIN."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import numpy as np,polars as pl
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    from run import FEATURE_FILE,feature_names,to_matrix
    features=feature_names();expanded,indices=encoder.names(features);assert len(expanded)==120
    rng=np.random.default_rng(20261010);records=[]
    exact=lambda x,y:np.array_equal(np.asarray(x,dtype=np.float32).view('u4'),np.asarray(y,dtype=np.float32).view('u4'))
    for count in (0,1,2,7,31,63,127):
        raw=rng.integers(-3,4,size=(count,63)).astype(np.float32);dates=(np.arange(count)//7+1).astype('i4')
        if count:
            raw[::5,2]=np.nan;raw[::7,4]=np.inf;raw[::11,6]=-np.inf;raw[:,9]=np.nan;raw[:,12]=2.
        actual=encoder.encode(raw,dates,features);oracle=encoder.pandas_oracle(raw,dates,features)
        assert exact(actual,oracle) and exact(actual[:,:63],raw)
        # Independent scalar finite-only peer rank for every augmented channel.
        for row in range(count):
            for column,index in enumerate(indices):
                value=raw[row,index];values=[float(raw[j,index]) for j in range(count) if dates[j]==dates[row] and np.isfinite(raw[j,index])]
                target=.5 if not np.isfinite(value) else (sum(v<float(value) for v in values)+(sum(v==float(value) for v in values)+1)/2.)/len(values)
                assert actual[row,63+column].view('u4')==np.float32(target).view('u4')
        permutation=rng.permutation(count)
        assert exact(encoder.encode(raw[permutation],dates[permutation],features),actual[permutation])
        prefixes=0
        for day in np.unique(dates):
            end=int(np.flatnonzero(dates==day)[-1])+1
            assert exact(encoder.encode(raw[:end],dates[:end],features),actual[:end]);prefixes+=1
        if count:
            future=rng.normal(size=(14,63)).astype('f4')*1e6;future[0]=np.inf
            joined=np.vstack([raw,future]);future_dates=np.r_[dates,np.repeat(int(dates.max())+1,14)].astype('i4')
            assert exact(encoder.encode(joined,future_dates,features)[:count],actual)
        records.append({'rows':count,'scalar_all_augmented_channels_exact':True,'Pandas_bits_exact':True,'raw63_bits_unchanged':True,'row_permutation_exact':True,'whole_date_prefix_cases':prefixes,'appended_future_poison_does_not_change_past':True})
    out=Path('E:/赛题五_本机临时/daily_feature_encoder120_actual_TRAIN_controls_v1_20261010');out.mkdir(exist_ok=False)
    lazy=pl.scan_parquet(FEATURE_FILE)
    days=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<20191231)).select('trade_date').unique().sort('trade_date').tail(3).collect()['trade_date'].to_list()
    frame=lazy.filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(['ts_code','trade_date',*features]).sort('trade_date','ts_code').collect()
    assert len(frame)==13950 and not frame.select(['ts_code','trade_date']).is_duplicated().any()
    raw=to_matrix(frame,features);dates=frame['trade_date'].to_numpy();started=time.perf_counter();actual=encoder.encode(raw,dates,features);native_seconds=time.perf_counter()-started
    oracle=encoder.pandas_oracle(raw,dates,features);assert exact(actual,oracle) and exact(actual[:,:63],raw) and np.isfinite(actual[:,63:]).all()
    assert exact(encoder.encode(raw[:4650],dates[:4650],features),actual[:4650])
    np.save(out/'raw63.npy',raw,allow_pickle=False);np.save(out/'encoded120.npy',actual,allow_pickle=False)
    create(out/'verification.json',{'status':'passed_real3_TRAIN_days13950_rows120_features_Pandas_exact_and_cold1_date_prefix','rows':13950,'days':days,'raw_names':features,'encoded_names':expanded,
        'native_encode_seconds':native_seconds,'within_day_all4650_forecasts_encoded_before_any_target_or_price_valid_filter':True,'future_X_read':False,'test_labels_read':False,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(encoder.__file__),FEATURE_FILE,out/'raw63.npy',out/'encoded120.npy']},'new_native_fits':0,'new_quality_scores':0})
    proof=A/'daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json'
    create(proof,{'status':'passed7_scalar_and_Pandas_tied_peer_ranks_missing_infinities_permutation_causal_full_date_prefixes_and_real13950_TRAIN_rows',
        'records':records,'real_TRAIN_control':str(out/'verification.json'),'real_TRAIN_verification_sha256':sha(out/'verification.json'),
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(encoder.__file__),out/'verification.json']},
        'encoding':{'raw_channels':63,'new_daily_peer_channels':57,'total':120,'missing_peer_percentile':.5,'cohort':'all supplied forecasts on the same date, before filtering training targets'},
        'horizon_or_rolling_features_not_recomputed':True,'feature_encoder_has_no_trainable_parameters_or_labels':True,'future_X_read':False,'test_labels_read':False,'new_native_fits':0,'new_quality_scores':0,'model_training_and_official_validation_pending':True})
    print({'synthetic_scalar_and_Pandas_cases':7,'actual_TRAIN_rows':13950,'features':120,'actual_native_3_day_seconds':native_seconds,'GPU_training_not_started':True},flush=True)
if __name__=='__main__':main()
