"""Real full-period signed/cohort rank mixtures after fixed148; no test labels or future X."""
from pathlib import Path
import sys,os,time,gc,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/BF16Seed10_155_full73_training_v2_20261009')
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(OUT/'tmp'/key)
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    assert read(f/'service_execution.json')['status']=='passed',name

def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))

def main():
    closed('BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009')
    import numpy as np,polars as pl,psutil
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    p=A/'BF16Seed10_80_round155_proposal_v1_20261009.json';plan=read(p)
    assert plan['fixed_scientific_stage_base_round']==148 and plan['expected_full_cases']==73
    assert read(A/'optimization_20261003_r148/full_registration_execution.json')['status']=='passed'
    loc=A/'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009.json';folder=Path(read(loc)['output'])
    proof=folder/'verification.json';assert sha(proof)==read(loc)['verification_sha256']
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    parent_path=A/'optimization_20261003_r148/selected_validation.npy';raw_path=folder/'combined_raw.parquet'
    syn=A/'BF16Seed10_80_synthetic73_cold219_v1_20261009.json'
    assert (read(syn)['actual_cases'],read(syn)['actual_cold_cases'])==(73,219)
    pins={**read(proof)['input_sha256'],**{str(x):sha(x) for x in (Path(__file__),p,loc,proof,frame_path,parent_path,raw_path,syn,Path(codec.__file__),A/'BF16_complete_parent_rank_CDF_v1_20261008.py')}}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_full73_training_controls.json',{'input_sha256':pins,'plan':plan,'official_scores':0,'future_X_read':False})
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    keys=['ts_code','trade_date'];frame=pl.read_parquet(frame_path,columns=keys+['flag_limit_up','price_valid']);rawframe=pl.read_parquet(raw_path)
    assert frame.select(keys).equals(rawframe.select(keys))
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    parent=np.load(parent_path,mmap_mode='r');raw=rawframe['pred_raw'].to_numpy()
    dates=frame['trade_date'].to_numpy();flags=frame['flag_limit_up'].to_numpy();valid=frame['price_valid'].to_numpy()
    records=[];last_sign=None;prepared=None
    for i,c in enumerate(plan['new_cases']):
        started=time.monotonic()
        if last_sign!=c['sign']:
            prepared=codec.prepare(parent,raw,dates,flags,valid,c['sign']);last_sign=c['sign']
        out=codec.apply_prepared(parent,flags,valid,c['role'],c['weight'],prepared)
        independent=codec.pandas_oracle(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign']);exact(out,independent)
        mask=codec.selected(flags,valid,c['role']);exact(out[~mask],np.asarray(parent)[~mask])
        if not c['weight']:exact(out,np.asarray(parent))
        cold=[]
        for days in (80,260,975):
            n=days*4650
            prefix=codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign'])
            oracle=codec.pandas_oracle(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign'])
            exact(prefix,out[:n]);exact(oracle,out[:n]);cold.append({'days':days,'rows':n,'native_and_independent_bits_exact':True})
        record={'case':i,'configuration':c,'rows':len(out),'controls':cold,'full_independent_Pandas_bits_exact':True,
          'invalid_and_declared_unselected_parent_bits_exact':True,'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(out)).cast('B')).hexdigest(),
          'first2020_changed_rows':int(np.count_nonzero(out[dates<20210101]!=parent[dates<20210101])),
          'elapsed_seconds':time.monotonic()-started}
        create(OUT/f'case{i:02d}.json',record);records.append(record)
        del out,independent,prefix,oracle;gc.collect()
        print(f'Actual seed10_155 full training {i+1}/73; signed Pandas and three prefixes bit exact',flush=True)
    for f,d in pins.items():assert sha(f)==d,f
    create(OUT/'verification.json',{'status':'passed_actual73_full5635800_seed10_155_signed_rank_mix_and219_cold_prefixes',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_parent_round':148,'controls':records,
      'rows_days_stocks':[5635800,1212,4650],'actual_full_cases':73,'actual_cold_cases':219,'new_quality_scores':0,
      'new_native_fits':0,'first2020_active':True,'test_labels_read':False,'actual_future_X_read':False})
    create(A/'actual_BF16Seed10_155_full73_training_location_v1_20261009.json',{'status':'passed_actual_seed10_155_training73_cold219_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
