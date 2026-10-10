"""Real49153 mean20 mature origins: independent full-date rank, peer features and identity IDs."""
from pathlib import Path
import sys,time,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_rank20_embedding_mature_fixture_v1_20261010')
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();import psutil
    while psutil.virtual_memory().available<11*2**30:assert allowed();time.sleep(10)
    import numpy as np,polars as pl,pandas as pd
    import stock_rank20_embedding_small512_BF16_native_v1_20261010 as native
    import recent252_rank20_mature_training_population_v1_20261010 as population
    import stock_identity_embedding_network_v1_20261010 as architecture
    from run import FEATURE_FILE
    prep=A/'stock_rank20_embedding_own64_native_sources_preparation_v1_20261010.json'
    for p,d in read(prep)['input_sha256'].items():assert sha(p)==d,p
    pointer=A/'actual_stock_forward20_embedding_mature_fixture_location_v1_20261010.json';prior=Path(read(pointer)['output']);oldproof=read(prior/'verification.json')
    assert oldproof['rows']==49153 and oldproof['last_label_end']<20191231
    pins={str(p):sha(p) for p in [Path(__file__),prep,pointer,prior/'verification.json',prior/'past_features121.npy',prior/'past_keys_and_label_end.parquet',FEATURE_FILE,Path(native.__file__),Path(population.__file__),Path(architecture.__file__),A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json']}
    OUT.mkdir(exist_ok=False);create(OUT/'frozen_before_actual_fixture.json',{'input_sha256':pins,'cutoff_exclusive':20191231,'future_X_read':False,'test_labels_read':False})
    mature=population.training_frame(pl.scan_parquet(FEATURE_FILE),20191231,native.CONFIG).select('ts_code','trade_date','label_end_20d','y_ret_20mean','y_rank_20mean').collect()
    assert len(mature)>49153 and mature['label_end_20d'].max()<20191231
    oracle=mature.select('trade_date','y_ret_20mean').to_pandas().groupby('trade_date',sort=False)['y_ret_20mean'].rank(method='average',pct=True).to_numpy()
    assert np.array_equal(oracle.view('u8'),mature['y_rank_20mean'].to_numpy().view('u8'))
    frame=mature.head(49153);keys=['ts_code','trade_date'];prior_keys=pl.read_parquet(prior/'past_keys_and_label_end.parquet')
    assert frame.select(keys+['label_end_20d']).equals(prior_keys)
    vocabulary=sorted(mature['ts_code'].unique().to_list());xprior=np.load(prior/'past_features121.npy');x121=architecture.attach(xprior[:,:120],frame['ts_code'].to_list(),vocabulary)
    assert np.array_equal(x121.view('u4'),xprior.view('u4'))
    y=frame['y_rank_20mean'].to_numpy();target,bounds=native.prepare_rank_targets(y,native.CONFIG)
    centered=y-.5;lo,hi=np.quantile(centered,[.005,.995]);expected=np.minimum(np.maximum(centered,lo),hi).astype(np.float32)
    assert np.array_equal(target.view('u4'),expected.view('u4')) and bounds==[float(lo),float(hi)]
    refusals=[]
    for bad in (np.array([0.,1.]),np.array([-.01,.5]),np.array([.5,1.01]),np.array([np.nan,.5])):
        try:native.prepare_rank_targets(bad,native.CONFIG)
        except AssertionError:refusals.append(True)
        else:raise AssertionError('Invalid raw rank20 target accepted')
    assert architecture.attach(x121[:1,:120],['not_in_mature_vocabulary'],vocabulary)[0,-1]==0
    np.save(OUT/'past_features121.npy',x121);np.save(OUT/'past_rank20_targets.npy',y);frame.select(keys+['label_end_20d']).write_parquet(OUT/'past_keys_and_label_end.parquet')
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual49153_rank20_mature_origins_all_mature_date_Pandas_rank_peer120_identity_and_center_once_bits','input_sha256':pins,'rows':49153,'full_mature_rank_oracle_rows':len(mature),'last':int(frame['trade_date'].max()),'last_label_end':int(frame['label_end_20d'].max()),'cutoff_exclusive':20191231,'configuration':native.CONFIG,'stock_vocabulary':vocabulary,'all_mature_day_Pandas_raw_rank_bits_exact':True,'feature121_bits_match_prior_actual_independent_Pandas_peer_and_ID_fixture':True,'rank_target_centered_once_and_winsorized_bits_exact':True,'invalid_raw_target_refusals':len(refusals),'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_rank20_mature_fixture_rows':49153,'full_mature_rank_oracle_rows':len(mature),'new_fits':0},flush=True)
if __name__=='__main__':main()
