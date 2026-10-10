"""Real mature mean10 ranks and independently encoded full peers before selecting training rows."""
from pathlib import Path
import sys,os,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_rank60_embedding_mature_fixture_v1_20261011')
for k in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):os.environ[k]=str(OUT/'tmp'/k)
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import psutil
    while psutil.virtual_memory().available<11*2**30:assert allowed();time.sleep(10)
    import numpy as np,polars as pl
    import stock_rank60_embedding_small512_BF16_native_v1_20261011 as native
    import recent252_rank60_mature_training_population_v2_20261011 as population
    import forward60_mature_training_labels_v2_20261011 as labels
    import mature_population_cross120_training_matrix_v1_20261010 as matrix
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    import stock_identity_embedding_network_v1_20261010 as architecture
    from run import FEATURE_FILE,feature_names,to_matrix
    admission=A/'stock_rank60_embedding_own64_native_sources_preparation_v1_20261011.json'
    for p,d in read(admission)['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),admission,FEATURE_FILE,Path(native.__file__),Path(population.__file__),Path(labels.__file__),
           Path(matrix.__file__),Path(encoder.__file__),Path(architecture.__file__),
           A/'recent252_rank60_mature_population_actual_CPU_controls_v2_20261011.json']
    pins={str(p):sha(p) for p in paths};OUT.mkdir(exist_ok=False)
    cutoff=20191231
    create(OUT/'frozen_before_actual_mature_fixture.json',{'input_sha256':pins,'cutoff_exclusive':cutoff,'test_labels_read':False})
    lazy=pl.scan_parquet(FEATURE_FILE);features=feature_names();keys=['ts_code','trade_date']
    mature=population.training_frame(lazy,cutoff,native.CONFIG)
    vocabulary=sorted(mature.select('ts_code').unique().collect()['ts_code'].to_list());assert 0<len(vocabulary)<=4650
    frame=mature.select(keys+['y_rank_60mean','label_end_60d']).limit(49153).collect()
    assert len(frame)==49153 and frame['label_end_60d'].max()<cutoff
    y=frame['y_rank_60mean'].to_numpy();x120,alignment=matrix.matrix(lazy,frame,features)
    assert alignment['encoder_before_label_and_price_valid_filter']
    dates=frame['trade_date'].unique().to_list()
    cohort=lazy.filter(pl.col('is_train')&pl.col('trade_date').is_in(dates)).select(keys+features).sort('trade_date','ts_code').collect()
    raw=to_matrix(cohort,features)
    oracle=encoder.pandas_oracle(raw,cohort['trade_date'].to_numpy(),features)
    lookup=frame.select(keys).with_row_index('_order').join(cohort.select(keys).with_row_index('_peer'),on=keys,how='left',validate='1:1').sort('_order')
    assert lookup['_peer'].null_count()==0 and lookup.select(keys).equals(frame.select(keys))
    expected120=oracle[lookup['_peer'].to_numpy()]
    assert np.array_equal(x120.view('u4'),expected120.view('u4'))
    # Future label poisoning must leave all actual mature training keys and targets unchanged.
    poisoned=lazy.with_columns(pl.when(pl.col('trade_date')>=cutoff).then(float('inf')).otherwise(pl.col('y_ret_1d')).alias('y_ret_1d'))
    replay=population.training_frame(poisoned,cutoff,native.CONFIG).select(keys+['y_rank_60mean','label_end_60d']).limit(49153).collect()
    assert replay.equals(frame)
    x121=architecture.attach(x120,frame['ts_code'].to_list(),vocabulary)
    dictionary={code:i+1 for i,code in enumerate(vocabulary)}
    expectedIDs=np.array([dictionary[str(code)] for code in frame['ts_code']],dtype=np.float32)
    assert np.array_equal(x121[:,:120].view('u4'),x120.view('u4')) and np.array_equal(x121[:,-1],expectedIDs)
    target,bounds=native.prepare_rank_targets(y,native.CONFIG);center=y-.5;lo,hi=np.quantile(center,[.005,.995])
    assert np.array_equal(target.view('u4'),np.clip(center,lo,hi).astype(np.float32).view('u4')) and bounds==[float(lo),float(hi)]
    refusals=[]
    for bad in (np.array([0.,1.]),np.array([-.01,.5]),np.array([.5,1.01]),np.array([np.nan,.5])):
        try:native.prepare_rank_targets(bad,native.CONFIG)
        except AssertionError:refusals.append(True)
        else:raise AssertionError('Invalid raw mean10 rank accepted')
    assert architecture.attach(x120[:1],['not_in_mature_vocabulary'],vocabulary)[0,-1]==0
    np.save(OUT/'past_features121.npy',x121);np.save(OUT/'past_rank60_targets.npy',y)
    frame.select(keys+['label_end_60d']).write_parquet(OUT/'past_keys_and_label_end.parquet')
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual49153_rank60_mature_targets_full_peer_Pandas120_stock_IDS_and_exact_once_centering_CPU',
           'input_sha256':pins,'rows':len(frame),'last':int(frame['trade_date'].max()),'last_label_end':int(frame['label_end_60d'].max()),
           'cutoff_exclusive':cutoff,'configuration':native.CONFIG,'stock_vocabulary':vocabulary,'alignment':alignment,
           'numeric120_full_supplied_peer_Pandas_bits_exact':True,'stock_IDs_independent_dictionary_exact':True,'unknown_stock_zero':True,
           'actual_future_label_poisoning_same_keys_and_targets':True,'rank60_centered_once_and_winsorized_bits_exact':True,
           'invalid_raw_target_refusals':len(refusals),'feature121_sha256':sha(OUT/'past_features121.npy'),
           'raw_rank60_target_sha256':sha(OUT/'past_rank60_targets.npy'),'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_stock_rank60_embedding_mature_fixture_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_mature_rank60_rows':49153,'full_peer_Pandas120_exact':True,'new_fits':0},flush=True)

if __name__=='__main__':main()
