"""Actual saved-tensor native stage controls on historical3-day panels; never actual future data."""
from pathlib import Path
from types import SimpleNamespace
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/BF16_complete_parent_native_hook3_v1_20261008')


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    # Full-oracle and native-hook GPU work is deliberately serial.
    closed('BF16_independent_full5_GPU_controls_v2_20261008')
    closed('BF16_rank_CDF_actual_full37_controls_v1_20261008')
    import numpy as np
    import polars as pl
    from run import FEATURE_FILE,feature_names,to_matrix
    from BF16_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY
    import neural_BF16_micro8192_native_v1_20261008 as native
    from BF16_complete_parent_rank_CDF_v1_20261008 import ROLES
    control=Path(read(A/'actual_BF16_rank_CDF_full37_location_v1_20261008.json')['output'])
    proof=read(control/'verification.json');assert proof['status']=='passed_actual37_full5635800_BF16_rank_CDF_independent_and111_cold_controls'
    parent=proof['actual_parent_round']
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    keys=['ts_code','trade_date'];features=feature_names()
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    parent_path=A/f'optimization_20261003_r{parent}/selected_validation.npy'
    paths=[Path(__file__),A/'BF16_complete_parent_native_stage_v1_20261008.py',
           A/'neural_BF16_independent_forward_v1_20261008.py',Path(native.__file__),
           A/'BF16_complete_parent_rank_CDF_v1_20261008.py',FEATURE_FILE,frame_path,parent_path,
           control/'verification.json',bank/'verification.json',
           *[bank/str(year)/name for year in (2020,2022,2024) for name in ('model.joblib','info.json')]]
    pins={str(p):sha(p) for p in paths}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_actual3_historical_native_hooks.json',{'input_sha256':pins,
        'years':[2020,2022,2024],'days_each':3,'roles':list(ROLES),'cold_day_prefix':1,
        'actual_future_features_and_labels_read':False,'new_quality_scores':0})
    frame=pl.read_parquet(frame_path,columns=keys+['flag_limit_up','price_valid'])
    all_dates=frame['trade_date'].to_numpy();all_raw=np.load(parent_path,mmap_mode='r')
    records=[]
    for year,role,weight in zip((2020,2022,2024),ROLES,(.005,.05,.2)):
        days=np.unique(all_dates[all_dates//10000==year])[:3]
        chosen=np.flatnonzero(np.isin(all_dates,days));panel=frame[chosen]
        test=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train') & pl.col('trade_date').is_in(days)).select(keys+features).sort('trade_date','ts_code').collect()
        assert test.select(keys).equals(panel.select(keys)) and len(panel)==3*4650
        info=read(bank/str(year)/'info.json')
        component={'name':'rank_MLP16384_BF16_micro8192_32epochs','path':str(bank/str(year)/'model.joblib'),
                   'sha256':info['model_sha256'],'training_info':info,'configuration':native.CONFIG}
        spec={'model':component['name'],'role':role,'weight':weight,'rank_universe':'all_current_raw_forecasts',
              'first2020_active':True,'position':'after_complete_qualified_parent'}
        context=SimpleNamespace(dates=panel['trade_date'].to_numpy(),flags=panel['flag_limit_up'].to_numpy(),
            valid=panel['price_valid'].to_numpy(),_BF16_feature_names=features,
            _BF16_raw_features=to_matrix(test,features),_whole_graph={GRAPH_KEY:spec})
        source_raw=np.asarray(all_raw[chosen],dtype=np.float64)
        value,full=after_parent(SimpleNamespace(sha=sha),context,source_raw,spec,component)
        cold_context=SimpleNamespace(**vars(context))
        for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold_context,field,getattr(context,field)[:4650])
        prefix,cold=after_parent(SimpleNamespace(sha=sha),cold_context,source_raw[:4650],spec,component)
        assert np.array_equal(prefix.view('u8'),value[:4650].view('u8'))
        record={'year':year,'role':role,'weight':weight,'full':full,'cold':cold,'whole_day_prefix_bits_exact':True}
        create(OUT/f'year{year}.json',record);records.append(record)
        print(f'Actual wide BF16 native hook {year}:3 days, saved/reloaded/independent/CDF and1-day prefix exact',flush=True)
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual3_historical_BF16_full_native_independent_CDF_and_whole_day_prefix_hooks',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_BF16_native_hook3_location_v1_20261008.json',{'status':'actual3_BF16_historical_native_hooks_passed_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})


if __name__=='__main__':main()
