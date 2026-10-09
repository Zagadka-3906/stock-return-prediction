"""Verify full historical equal-weight ensemble arithmetic from two independent saved-state replays."""
from pathlib import Path
import sys,time,os,gc
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/BF16TwoSeed154_equal_mean_full5_v1_20261009')
def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    assert read(f/'service_execution.json')['status']=='passed',name
def main():
    closed('BF16Medium153_independent_full5_GPU_controls_v1_20261009')
    closed('BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009')
    import numpy as np,polars as pl,pandas as pd,psutil
    pointers=[A/'actual_BF16Medium153_full5_independent_location_v1_20261009.json',A/'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009.json']
    folders=[Path(read(p)['output']) for p in pointers];proofs=[read(f/'verification.json') for f in folders]
    for p,f,proof in zip(pointers,folders,proofs):
        assert sha(f/'verification.json')==read(p)['verification_sha256']
        assert proof['rows_days_stocks']==[5635800,1212,4650] and len(proof['records'])==5
        assert all(r['full_original_native_reload_and_independent_bits_exact'] for r in proof['records'])
    proposal=A/'BF16TwoSeed79_round154_proposal_v1_20261009.json';plan=read(proposal)
    assert plan['seed_values']==[20261009,20261010] and plan['actual_scheme_base_round']==148 and len(plan['scientific_cases'])==73
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet';raw_paths=[f/'combined_raw.parquet' for f in folders]
    inputs=[Path(__file__),proposal,frame_path,*pointers,*raw_paths,*(f/'verification.json' for f in folders)]
    pins={**proofs[0]['input_sha256'],**proofs[1]['input_sha256'],**{str(p):sha(p) for p in inputs}}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_equal_mean_controls.json',{'input_sha256':pins,'arithmetic':plan['raw_ensemble_arithmetic'],'quality_scores':0,'test_labels_read':False})
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    keys=['ts_code','trade_date'];frame=pl.read_parquet(frame_path,columns=keys+['price_valid'])
    raws=[pl.read_parquet(p) for p in raw_paths]
    assert all(r.select(keys).equals(frame.select(keys)) for r in raws)
    left,right=[r['pred_raw'].to_numpy() for r in raws];valid=frame['price_valid'].to_numpy()
    assert left.dtype==right.dtype==np.float64 and np.isfinite(left).all() and np.isfinite(right).all()
    assert np.all(left[~valid]==-1e6) and np.all(right[~valid]==-1e6)
    mean=(left+right)*.5;oracle=((pd.Series(left)+pd.Series(right))/2.).to_numpy()
    assert np.array_equal(mean.view('u8'),oracle.view('u8')) and np.all(mean[~valid]==-1e6)
    records=[];dates=frame['trade_date'].to_numpy()
    for year in range(2020,2025):
        mask=dates//10000==year;n=int(mask.sum());unique=int(np.unique(dates[mask]).size)
        a,b=left[mask],right[mask];expected=mean[mask]
        cold=[]
        for days in (80,160):
            count=min(days,unique)*4650;observed=(a[:count]+b[:count])*.5
            assert np.array_equal(observed.view('u8'),expected[:count].view('u8'))
            cold.append({'days':days,'rows':count,'equal_mean_bits_exact':True})
        record={'year':year,'rows':n,'days':unique,'full_independent_Pandas_equal_mean_bits_exact':True,'cold_controls':cold}
        create(OUT/f'year{year}_verification.json',record);records.append(record)
    frame.select(keys).with_columns(pl.Series('pred_raw',mean)).write_parquet(OUT/'combined_raw.parquet')
    for f,d in pins.items():assert sha(f)==d,f
    create(OUT/'verification.json',{'status':'passed_actual_two_independent_seeds5635800_equal_mean_and10_annual_prefixes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'rows_days_stocks':[5635800,1212,4650],
        'actual_complete_annual_models_across_seeds':12,'actual_cold_controls':10,'raw_sha256':sha(OUT/'combined_raw.parquet'),
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    create(A/'actual_BF16TwoSeed154_equal_mean_full5_location_v1_20261009.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
