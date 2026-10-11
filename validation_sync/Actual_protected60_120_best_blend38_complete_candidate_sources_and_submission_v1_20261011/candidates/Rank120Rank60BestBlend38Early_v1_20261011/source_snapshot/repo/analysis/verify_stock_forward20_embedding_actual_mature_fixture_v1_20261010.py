"""Real49153 mean20 mature rows, full-peer rank oracle, independent sampled label arithmetic."""
from pathlib import Path
import sys,time,hashlib,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_forward20_embedding_mature_fixture_v1_20261010')
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();import psutil
    while psutil.virtual_memory().available<11*2**30:assert allowed();time.sleep(10)
    import numpy as np,polars as pl
    import stock_forward20_embedding_small512_BF16_native_v1_20261010 as native
    import recent252_forward20_mature_training_population_v1_20261010 as population
    import stock_identity_embedding_network_v1_20261010 as architecture
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    from run import FEATURE_FILE,feature_names,to_matrix
    admission=A/'stock_forward20_embedding_own64_native_sources_preparation_v1_20261010.json'
    for p,d in read(admission)['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),admission,Path(native.__file__),Path(population.__file__),Path(architecture.__file__),Path(encoder.__file__),FEATURE_FILE];pins={str(p):sha(p) for p in paths}
    OUT.mkdir(exist_ok=False);create(OUT/'frozen_before_actual_mature_fixture.json',{'input_sha256':pins,'cutoff_exclusive':20191231,'actual_future_X_read':False,'test_labels_read':False})
    lazy=pl.scan_parquet(FEATURE_FILE);keys=['ts_code','trade_date'];names=feature_names();cutoff=20191231
    mature=population.training_frame(lazy,cutoff,native.CONFIG)
    vocabulary=sorted(mature.select('ts_code').unique().collect()['ts_code'].to_list());assert 0<len(vocabulary)<=4650
    frame=mature.select(keys+['y_ret_20mean','label_end_20d']).limit(49153).collect();assert len(frame)==49153
    days=frame['trade_date'].unique().sort().to_list()
    peers=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)&pl.col('trade_date').is_in(days)).select(keys+names).sort('trade_date','ts_code').collect()
    dates=peers['trade_date'].to_numpy();assert np.all(np.unique(dates,return_counts=True)[1]==4650)
    raw=np.ascontiguousarray(to_matrix(peers,names),dtype=np.float32);numeric=encoder.encode(raw,dates,names);oracle=encoder.pandas_oracle(raw,dates,names)
    assert np.array_equal(numeric.view('u4'),oracle.view('u4')) and np.array_equal(numeric[:,:63].view('u4'),raw.view('u4'))
    numbered=peers.select(keys).with_row_index('_raw_peer_row')
    aligned=frame.join(numbered,on=keys,how='left',validate='1:1').sort('trade_date','ts_code');assert aligned.select(keys).equals(frame.select(keys)) and not aligned['_raw_peer_row'].null_count()
    selected=numeric[aligned['_raw_peer_row'].to_numpy()];x=architecture.attach(selected,frame['ts_code'].to_list(),vocabulary)
    mapping={c:i+1 for i,c in enumerate(vocabulary)};expected=np.asarray([mapping[c] for c in frame['ts_code']],dtype=np.float32)
    assert x.shape==(49153,121) and np.array_equal(x[:,:120].view('u4'),selected.view('u4')) and np.array_equal(x[:,120],expected)
    y=frame['y_ret_20mean'].to_numpy();assert np.isfinite(y).all() and int(frame['label_end_20d'].max())<cutoff
    target,bounds=native.prepare_return_targets(y,native.CONFIG);lo,hi=np.quantile(y,[.005,.995]);expected=(np.minimum(np.maximum(y,lo),hi)*20.).astype(np.float32)
    assert np.array_equal(target.view('u4'),expected.view('u4')) and bounds==[float(lo),float(hi)]
    # Independently check256 real stock/origin spans against provided TRAIN one-day labels.
    sample=frame[np.linspace(0,len(frame)-1,256,dtype=np.int64)];calendar=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    left=int(np.searchsorted(calendar,int(sample['trade_date'].min())));right=int(np.searchsorted(calendar,int(sample['trade_date'].max())))+21;span=calendar[left:right].tolist()
    past=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)&pl.col('ts_code').is_in(sample['ts_code'].unique().to_list())&pl.col('trade_date').is_in(span)).select(keys+['y_ret_1d']).sort('ts_code','trade_date').collect()
    groups={key[0]:part for key,part in past.partition_by('ts_code',as_dict=True).items()};controls=[]
    for row in sample.iter_rows(named=True):
        part=groups[row['ts_code']];ds=part['trade_date'].to_numpy();i=int(np.searchsorted(ds,row['trade_date']));values=part['y_ret_1d'].to_numpy()[i:i+20]
        assert len(values)==20 and np.isfinite(values).all() and int(ds[i+20])==row['label_end_20d']<cutoff
        assert int(np.searchsorted(calendar,ds[i+20])-np.searchsorted(calendar,ds[i]))==20
        actual=float(np.mean(values,dtype=np.float64));assert np.isclose(actual,row['y_ret_20mean'],rtol=1e-12,atol=1e-14)
        controls.append({'ts_code':row['ts_code'],'trade_date':row['trade_date'],'label_end':row['label_end_20d'],'independent_TRAIN_mean20':actual,'production_target':row['y_ret_20mean']})
    unknown=architecture.attach(selected[:1],['not_in_mature_vocabulary'],vocabulary);assert unknown[0,-1]==0
    np.save(OUT/'past_features121.npy',x);np.save(OUT/'past_forward20_targets.npy',y);frame.select(keys+['label_end_20d']).write_parquet(OUT/'past_keys_and_label_end.parquet')
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual49153_forward20_mature_returns_full_peer_Pandas_numeric120_bits_stock_IDs_and256_independent_TRAIN_label_spans','input_sha256':pins,'rows':49153,'full_raw_peer_rows':len(peers),'last':int(frame['trade_date'].max()),'last_label_end':int(frame['label_end_20d'].max()),'cutoff_exclusive':cutoff,'configuration':native.CONFIG,'stock_vocabulary':vocabulary,'numeric120_full_peer_native_Pandas_bits_exact_before_mature_row_filter':True,'stock_IDs_independent_dictionary_exact':True,'unknown_stock_zero':True,'forward20_return_winsor_scaled20_bits_exact':True,'independent_sampled_label_controls':controls,'feature121_sha256':sha(OUT/'past_features121.npy'),'raw_forward20_target_sha256':sha(OUT/'past_forward20_targets.npy'),'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    create(A/'actual_stock_forward20_embedding_mature_fixture_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')});print({'actual_forward20_mature_fixture_passed':True,'rows':49153,'independent_label_spans':256},flush=True)
if __name__=='__main__':main()
