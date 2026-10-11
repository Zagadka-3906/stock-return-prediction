"""Align49153 real five-day mature labels and peer features to own mature stock vocabulary."""
from pathlib import Path
import sys,os,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_rank5_embedding_mature_fixture_v1_20261010')
for k in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):os.environ[k]=str(OUT/'tmp'/k)
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();import psutil
    while psutil.virtual_memory().available<11*2**30:assert allowed();time.sleep(10)
    import numpy as np,polars as pl
    import stock_rank5_embedding_small512_BF16_native_v1_20261010 as native
    import recent252_rank5_mature_training_population_v1_20261010 as population
    import stock_identity_embedding_network_v1_20261010 as architecture
    from run import FEATURE_FILE,feature_names
    proof=read(A/'stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json')
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    old=Path(read(A/'actual_Cross120Recent252Rank5Huber050_past_fixture_location_v2_20261010.json')['output']);oldproof=read(old/'verification.json')
    assert oldproof['last_label_end']<20191231 and oldproof['rows']==49153
    prior=A/'cross120_rank5_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json'
    for p,d in read(prior)['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),Path(native.__file__),Path(population.__file__),Path(architecture.__file__),prior,FEATURE_FILE,old/'verification.json',old/'past_features.npy',old/'past_return_targets.npy']
    pins={str(p):sha(p)for p in paths};OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_actual_mature_fixture.json',{'input_sha256':pins,'cutoff_exclusive':20191231,'test_labels_read':False})
    lazy=pl.scan_parquet(FEATURE_FILE);raw_names=feature_names();keys=['ts_code','trade_date']
    mature=population.training_frame(lazy,20191231,native.CONFIG)
    vocabulary=sorted(mature.select('ts_code').unique().collect()['ts_code'].to_list());assert len(vocabulary)<=4650
    frame=mature.select(keys+['y_rank_5mean','label_end_5d']).limit(49153).collect()
    y=frame['y_rank_5mean'].to_numpy();x120=np.load(old/'past_features.npy')
    assert np.array_equal(y.view('u8'),np.load(old/'past_return_targets.npy').view('u8')) and x120.shape==(49153,120)
    x121=architecture.attach(x120,frame['ts_code'].to_list(),vocabulary)
    mapping={code:i+1 for i,code in enumerate(vocabulary)};expected=np.array([mapping[str(c)]for c in frame['ts_code']],dtype=np.float32)
    assert np.array_equal(x121[:,:120].view('u4'),x120.view('u4')) and np.array_equal(x121[:,-1],expected)
    assert int(frame['label_end_5d'].max())==oldproof['last_label_end']<20191231
    target,bounds=native.prepare_rank_targets(y,native.CONFIG);centered=y-.5;lo,hi=np.quantile(centered,[.005,.995]);oracle=np.minimum(np.maximum(centered,lo),hi).astype(np.float32)
    assert np.array_equal(target.view('u4'),oracle.view('u4')) and bounds==[float(lo),float(hi)]
    refusal=[]
    for bad in (np.array([0.,1.]),np.array([-.01,.5]),np.array([.5,1.01]),np.array([np.nan,.5])):
        try:native.prepare_rank_targets(bad,native.CONFIG)
        except AssertionError:refusal.append(True)
        else:raise AssertionError('Invalid raw rank5 target accepted')
    unknown=architecture.attach(x120[:1],['not_in_mature_vocabulary'],vocabulary);assert unknown[0,-1]==0
    np.save(OUT/'past_features121.npy',x121);np.save(OUT/'past_rank5_targets.npy',y)
    frame.select(keys+['label_end_5d']).write_parquet(OUT/'past_keys_and_label_end.parquet')
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual49153_rank5_mature_targets_raw120_bits_stock_vocab_IDS_and_exact_once_centering_CPU','input_sha256':pins,'rows':49153,'last':int(frame['trade_date'].max()),'last_label_end':int(frame['label_end_5d'].max()),'cutoff_exclusive':20191231,'configuration':native.CONFIG,'stock_vocabulary':vocabulary,'numeric120_bits_match_prior_independent_peer_Pandas_fixture':True,'stock_IDs_match_independent_dictionary':True,'unknown_stock_zero':True,'rank5_centered_once_and_winsorized_bits_exact':True,'invalid_raw_target_refusals':len(refusal),'feature121_sha256':sha(OUT/'past_features121.npy'),'raw_rank5_target_sha256':sha(OUT/'past_rank5_targets.npy'),'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_stock_rank5_embedding_mature_fixture_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_mature_rank5_rows':49153,'new_embedding_input_features':121,'target_centered_once':True},flush=True)
if __name__=='__main__':main()
