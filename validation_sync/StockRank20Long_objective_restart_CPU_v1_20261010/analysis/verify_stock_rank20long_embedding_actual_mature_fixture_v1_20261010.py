"""Real long-window mature Rank20 fixture with independent full-date ranks and peer features."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_rank20long_embedding_mature_fixture_v1_20261010')
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();import psutil
    while psutil.virtual_memory().available<11*2**30:assert allowed();time.sleep(10)
    import numpy as np,polars as pl
    import stock_rank20long_embedding_small512_BF16_native_v1_20261010 as native
    import recent504_rank20_mature_training_population_v1_20261011 as population
    import mature_population_cross120_training_matrix_v1_20261010 as matrix
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    from run import FEATURE_FILE,feature_names,to_matrix
    prep=A/'stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010.json'
    for p,d in read(prep)['input_sha256'].items():assert sha(p)==d,p
    features=feature_names();lazy=pl.scan_parquet(FEATURE_FILE);keys=['ts_code','trade_date']
    paths=[Path(__file__),prep,FEATURE_FILE,Path(native.__file__),Path(population.__file__),Path(matrix.__file__),Path(encoder.__file__),
        A/'recent504_rank20_mature_population_actual_CPU_controls_v1_20261011.json',A/'forward20_mature_training_labels_v1_20261010.py']
    pins={str(p):sha(p) for p in paths};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual_fixture.json',{'input_sha256':pins,'cutoff_exclusive':20191231,'training_calendar_window':504,'future_X_read':False,'test_labels_read':False})
    mature=population.training_frame(lazy,20191231,native.CONFIG).select(keys+['label_end_20d','y_ret_20mean','y_rank_20mean']).collect()
    assert len(mature)>49153 and mature['label_end_20d'].max()<20191231 and mature['trade_date'].n_unique()>252
    oracle=mature.select('trade_date','y_ret_20mean').to_pandas().groupby('trade_date',sort=False)['y_ret_20mean'].rank(method='average',pct=True).to_numpy()
    assert np.array_equal(oracle.view('u8'),mature['y_rank_20mean'].to_numpy().view('u8'))
    frame=mature.head(49153);vocabulary=sorted(mature['ts_code'].unique().to_list())
    encoded,alignment=matrix.matrix(lazy,frame,features)
    cohort=lazy.filter(pl.col('is_train')&pl.col('trade_date').is_in(frame['trade_date'].unique().to_list())).select(keys+features).sort('trade_date','ts_code').collect()
    raw=to_matrix(cohort,features);independent=encoder.pandas_oracle(raw,cohort['trade_date'].to_numpy(),features)
    lookup=frame.select(keys).with_row_index('_order').join(cohort.select(keys).with_row_index('_peer'),on=keys,how='left',validate='1:1').sort('_order')
    assert lookup['_peer'].null_count()==0 and lookup.select(keys).equals(frame.select(keys))
    assert np.array_equal(encoded.view('u4'),np.ascontiguousarray(independent[lookup['_peer'].to_numpy()]).view('u4'))
    x=native.architecture.attach(encoded,frame['ts_code'].to_list(),vocabulary)
    y=frame['y_rank_20mean'].to_numpy();target,bounds=native.prepare_rank_targets(y,native.CONFIG)
    centered=y-.5;lo,hi=np.quantile(centered,[.005,.995]);expected=np.minimum(np.maximum(centered,lo),hi).astype(np.float32)
    assert np.array_equal(target.view('u4'),expected.view('u4')) and bounds==[float(lo),float(hi)]
    assert native.architecture.attach(encoded[:1],['not_in_mature_population'],vocabulary)[0,-1]==0
    np.save(OUT/'past_features121.npy',x);np.save(OUT/'past_rank20_targets.npy',y);frame.select(keys+['label_end_20d']).write_parquet(OUT/'past_keys_and_label_end.parquet')
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual49153_rank20_long504_mature_origins_full_day_ranks_independent_peer_features_and_center_once',
        'input_sha256':pins,'rows':len(frame),'full_mature_rank_oracle_rows':len(mature),'full_mature_days':mature['trade_date'].n_unique(),
        'last':int(frame['trade_date'].max()),'last_label_end':int(frame['label_end_20d'].max()),'cutoff_exclusive':20191231,
        'configuration':native.CONFIG,'stock_vocabulary':vocabulary,'full_same_date_Pandas_rank_bits_exact':True,
        'independent_complete_peer_Pandas_feature121_numeric_bits_exact':True,'feature_alignment':alignment,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_stock_rank20long_embedding_mature_fixture_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_long504_fixture_rows':len(frame),'mature_days':mature['trade_date'].n_unique(),'all_peer_numeric_bits_exact':True},flush=True)
if __name__=='__main__':main()
