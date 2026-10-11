"""Audit30 existing native heads and their full OOFs; test90 new CDF cases without scoring."""
from pathlib import Path
import os,sys,time,gc,hashlib
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'; sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/CrossFamily_bank30_synthetic_v1_20261008')


def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
    assert np.array_equal(a.view('u8'),b.view('u8'))


def numeric_sha(x):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(x)).cast('B')).hexdigest()


def main():
    import numpy as np,polars as pl,psutil,joblib
    from threadpoolctl import threadpool_limits
    from nonflag_residual_Ridge_codec_20261007 import predict_native as lin_native,predict_decoded as lin_decoded
    from nonflag_residual_RFF128_codec_20261007 import predict_native as rff_native,predict_decoded as rff_decoded
    from nonflag_RFF128_streamed_gram_fitter_20261007 import prepared_sha
    from CrossFamily_complete_parent_CDF_v1_20261008 import HEADS,mixture,independent_mixture,transform,pandas_oracle
    plan_path=A/'CrossFamily94_round136_plan_v1_20261008.json';plan=read(plan_path)
    assert plan['new_case_count']==90 and plan['new_quality_scores']==0 and set(plan['heads'])==set(HEADS)
    assert not OUT.exists();OUT.mkdir(parents=True)
    pins={**plan['input_sha256'],str(plan_path):sha(plan_path),str(Path(__file__)):sha(__file__)}
    create(OUT/'frozen_before_actual_bank_replay.json',{'input_sha256':pins,'plan_sha256':sha(plan_path),'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    started=time.perf_counter()
    for index,(path,digest) in enumerate(pins.items(),1):
        assert sha(path)==digest,path
        if index%10==0:print(f'Actual immutable input SHA audit {index}/{len(pins)}',flush=True)
    while psutil.virtual_memory().available<7*2**30:time.sleep(10)
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid']).with_row_index('oof_position')
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    keys=frame.filter(pl.col('flag_limit_up')!=1)
    positions=keys['oof_position'].to_numpy();kd=keys['trade_date'].to_numpy()
    dates=frame['trade_date'].to_numpy();flags=frame['flag_limit_up'].to_numpy();valid=frame['price_valid'].to_numpy()
    alignment=read(A/'nonflag_residual_HGB_bank10_20261007/actual_teacher_target_and_key_alignment.json')
    raw=np.load(alignment['feature_cache'],mmap_mode='r');assert raw.shape==(len(keys),64)
    assert sha(alignment['feature_cache'])==alignment['feature_cache_sha256']
    assert numeric_sha(raw[:,63])==alignment['teacher_feature_numeric_sha256']
    teacher=np.load(A/'optimization_20261003_r106/selected_validation.npy',mmap_mode='r')
    teacher_pct=pl.DataFrame({'date':dates,'teacher':np.asarray(teacher)}).with_columns((pl.col('teacher').rank(method='average').over('date')/pl.len().over('date')).alias('pct'))['pct'].to_numpy()
    exact(raw[:,63],teacher_pct[positions]);del teacher_pct
    labels=keys.select('ts_code','trade_date').join(pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('trade_date')>=20200101)).select('ts_code','trade_date','y_rank').collect(),on=['ts_code','trade_date'],how='left',validate='1:1',maintain_order='left')
    y=labels['y_rank'].to_numpy().astype(float)+.5-raw[:,63]
    assert numeric_sha(y)==alignment['target_numeric_sha256'];del labels;gc.collect()
    eligible=np.isfinite(y)&keys['price_valid'].to_numpy()
    arrays={head:np.load(row['oof'],mmap_mode='r') for head,row in plan['heads'].items()}
    for head,array in arrays.items():
        assert array.shape==(5635800,) and array.dtype==np.float64 and np.isfinite(array).all()
        exact(np.asarray(array[(flags==1)|(dates<20210101)]),np.zeros(np.count_nonzero((flags==1)|(dates<20210101)),dtype=np.float64))
    all_days=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    records=[];window_checks=[];oof_days=np.unique(dates)
    metadata_keys=('year','features','training_rows','last_training_label_date','last_training_label_end','exclusive_cutoff','training_matrix_numeric_sha256','training_target_numeric_sha256')
    with threadpool_limits(limits=2):
        for year in range(2021,2026):
            infos={h:read(row['infos'][str(year)]) for h,row in plan['heads'].items()}
            first=infos[HEADS[0]]
            for h,info in infos.items():
                assert {k:info[k] for k in metadata_keys}=={k:first[k] for k in metadata_keys},(year,h)
            train=(kd<first['exclusive_cutoff'])&eligible;idx=np.flatnonzero(train)
            last=int(kd[idx].max());end=int(all_days[np.searchsorted(all_days,last)+1])
            assert len(idx)==first['training_rows'] and last==first['last_training_label_date'] and end==first['last_training_label_end'] and end<=first['exclusive_cutoff']
            window=np.load(Path(alignment['feature_cache']).parent/f'mature_training_features64_{year}.npy',mmap_mode='r')
            assert window.shape==(len(idx),64)
            for left in range(0,len(idx),8192):exact(np.asarray(window[left:left+8192]),np.asarray(raw[idx[left:left+8192]]))
            preprocessing=None
            for head in HEADS:
                info=infos[head];bundle=joblib.load(info['native_model_path'])
                if preprocessing is None:preprocessing=bundle['preprocessing']
                assert bundle['preprocessing']==preprocessing and bundle['features']==info['features']
            assert prepared_sha(window,preprocessing)==first['training_matrix_numeric_sha256']
            assert numeric_sha(y[train])==first['training_target_numeric_sha256']
            window_checks.append({'year':year,'training_rows':len(idx),'last_label_date':last,'last_label_end':end,'cutoff':first['exclusive_cutoff'],'all6_heads_same_own_mature_preprocessing_feature_and_target_hashes':True,'every_cached_training_row_rechecked':True})
            selection=kd//10000==year;year_positions=positions[selection]
            test=np.asarray(raw[selection]) if year<2025 else np.asarray(window[:1000]).copy()
            for head in HEADS:
                info=infos[head];kind=plan['heads'][head]['state_kind']
                native,decoded=(rff_native,rff_decoded) if kind=='random_fourier_linear' else (lin_native,lin_decoded)
                bundle=joblib.load(info['native_model_path']);reloaded=joblib.load(info['native_model_path'])
                state=read(info['independent_'+kind+'_state_path'])
                assert state['features']==bundle['features'] and state['preprocessing']==bundle['preprocessing']
                if head.startswith('ridge_'):assert bundle['model'].alpha==info['parameters']['alpha'] and bundle['model'].solver=='cholesky'
                elif head.startswith('rff_'):
                    projection=bundle['model'].named_steps['rbf'];linear=bundle['model'].named_steps['ridge']
                    assert projection.gamma==info['parameters']['gamma'] and projection.n_components==128 and projection.random_state==20261007 and linear.alpha==info['parameters']['alpha']
                else:assert bundle['model'].get_params()['solver']=='empirical_bayes_centered_Gram64' and bundle['model'].alpha==info['parameters']['alpha']
                actual=np.empty(len(test),dtype=np.float64)
                for left in range(0,len(test),65536):
                    block=test[left:left+65536];value=native(bundle,block)
                    exact(value,native(reloaded,block));exact(value,decoded(state,block));actual[left:left+len(block)]=value
                if year<2025:exact(actual,np.asarray(arrays[head][year_positions]))
                cold=[]
                for count in ((80,260,975) if year<2025 else (1,79,999)):
                    n=int(np.count_nonzero(kd[selection]<=oof_days[count-1])) if year<2025 else count
                    for left in range(0,n,65536):
                        right=min(n,left+65536);exact(native(reloaded,test[left:right]),actual[left:right]);exact(decoded(state,test[left:right]),actual[left:right])
                    cold.append({'combined_days_or_training_sample_rows':count,'actual_rows':n,'bits_exact':True,'empty_year_prefix':n==0})
                record={'head':head,'year':year,'actual_rows':len(test),'full_saved_reloaded_independent_bits_exact':True,'saved_full_annual_OOF_bits_exact':year<2025,'actual2025_future_X_read':False,'cold_controls':cold}
                create(OUT/f'{head}_{year}.json',record);records.append(record)
                print(f'Actual30-head audit {len(records)}/30: {head} {year}, {len(test)} rows exact',flush=True)
                del bundle,reloaded,state,actual;gc.collect()
            window._mmap.close();del window,test,idx;gc.collect()
    # Independent synthetic arithmetic/CDF probes include ties, invalidsentinels and preserved cohorts.
    rng=np.random.default_rng(20261008);syn_dates=np.repeat(np.array([20201230,20210104,20210105,20210106]),37)
    parent=np.round(rng.normal(size=len(syn_dates)),1);syn_flags=(rng.random(len(parent))<.2).astype(int);syn_valid=rng.random(len(parent))>.2
    parent[~syn_valid]=-1e6
    syn_raw={h:rng.normal(size=len(parent)) for h in HEADS}
    synthetic=[]
    for case in plan['new_cases']:
        residual=mixture(syn_raw,case['group'],case['share']);oracle_residual=independent_mixture(syn_raw,case['group'],case['share']);exact(residual,oracle_residual)
        value=transform(parent,residual,syn_dates,syn_flags,syn_valid,case['amplitude'])
        exact(value,pandas_oracle(parent,oracle_residual,syn_dates,syn_flags,syn_valid,case['amplitude']))
        preserved=(syn_dates<20210101)|(syn_flags==1)|~syn_valid;exact(value[preserved],parent[preserved])
        for days in (1,2,3):
            n=days*37;exact(transform(parent[:n],residual[:n],syn_dates[:n],syn_flags[:n],syn_valid[:n],case['amplitude']),value[:n])
        synthetic.append({**case,'independent_arithmetic_and_CDF_bits_exact':True,'actual_cold_day_prefixes':[1,2,3]})
    exact(transform(parent,np.zeros(len(parent)),syn_dates,syn_flags,syn_valid,0.),parent)
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual30_existing_native_heads_full_OOF_and90_synthetic_crossfamily_CDF_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'annual_window_checks':window_checks,'actual_native_replay_records':records,
        'actual_model_count':30,'actual_full_OOF_heads':6,'synthetic_cases':synthetic,'synthetic_case_count':90,'actual_synthetic_cold_controls':270,
        'actual_current_parent_full_CDF_controls_still_required':True,'new_native_fits':0,'actual_quality_scores':0,'elapsed_seconds':time.perf_counter()-started,
        'actual_future_X_and_labels_read':False,'finite_grid_not_global_exhaustion':True})
    create(A/'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json',{'status':'passed_actual_existing30_native_heads_and90_synthetic_controls_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_quality_scores':0})


if __name__=='__main__':main()
