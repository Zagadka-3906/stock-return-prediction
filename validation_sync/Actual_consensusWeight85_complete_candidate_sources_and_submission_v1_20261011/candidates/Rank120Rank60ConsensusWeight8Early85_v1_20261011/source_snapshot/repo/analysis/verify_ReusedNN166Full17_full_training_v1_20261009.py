"""Full training-only composition controls: existing seed09 after the complete152 graph."""
from pathlib import Path
import sys,os,time,gc,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/ReusedNN166Full17_full_training_v1_20261009')
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
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
    closed('BF16Seed10_80_round155_full_registration_v1_20261009')
    closed('actual_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009')
    import numpy as np,polars as pl,psutil
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    planpath=A/'ReusedNN166Full17_train_only_proposal_v1_20261009.json';plan=read(planpath)
    assert plan['fixed_scientific_stage_base_round']==152 and len(plan['new_cases'])==17
    for p,d in plan['input_sha256'].items():assert sha(p)==d,p
    assert read(A/'optimization_20261003_r152/full_registration_execution.json')['status']=='passed'
    loc=A/'actual_BF16ReturnHuber050166_full5_independent_location_v1_20261009.json';folder=Path(read(loc)['output'])
    proof=folder/'verification.json';assert sha(proof)==read(loc)['verification_sha256']
    native_pointer=A/'actual_BF16ReturnHuber050166_native42_calendar_location_v1_20261009.json'
    native_proof=Path(read(native_pointer)['output'])/'verification.json';assert sha(native_proof)==read(native_pointer)['verification_sha256']
    assert read(native_proof)['actual_saved_states']==6 and len(read(native_proof)['records'])==42
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet'
    parentpath=A/'optimization_20261003_r152/selected_validation.npy';rawpath=folder/'combined_raw.parquet'
    pins={**read(proof)['input_sha256'],**{str(p):sha(p) for p in (Path(__file__),planpath,loc,proof,native_pointer,native_proof,framepath,parentpath,rawpath,Path(codec.__file__),A/'BF16_complete_parent_rank_CDF_v1_20261008.py')}}
    OUT.mkdir(parents=True,exist_ok=False)
    create(OUT/'frozen_before_actual_full17_controls.json',{'input_sha256':pins,'plan':plan,'new_native_fits':0,'new_quality_scores':0,'future_X_read':False})
    while psutil.virtual_memory().available<11.5*2**30:time.sleep(15)
    keys=['ts_code','trade_date'];frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);rawframe=pl.read_parquet(rawpath)
    assert frame.select(keys).equals(rawframe.select(keys))
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    parent=np.load(parentpath,mmap_mode='r');raw=rawframe['pred_raw'].to_numpy()
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    records=[];lastsign=None;prepared=None
    for i,c in enumerate(plan['new_cases']):
        started=time.monotonic()
        if lastsign!=c['sign']:prepared=codec.prepare(parent,raw,dates,flags,valid,c['sign']);lastsign=c['sign']
        value=codec.apply_prepared(parent,flags,valid,c['role'],c['weight'],prepared)
        oracle=codec.pandas_oracle(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign']);exact(value,oracle)
        mask=codec.selected(flags,valid,c['role']);exact(value[~mask],np.asarray(parent)[~mask])
        if not c['weight']:exact(value,np.asarray(parent))
        cold=[]
        for days in (80,260,975):
            n=days*4650
            prefix=codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign'])
            oracle_prefix=codec.pandas_oracle(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign'])
            exact(value[:n],prefix);exact(value[:n],oracle_prefix);cold.append({'days':days,'rows':n,'native_and_independent_CDF_bits_exact':True})
        record={'case':i,'configuration':c,'rows':len(value),'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),
            'full_independent_Pandas_bits_exact':True,'unselected_nonflag_and_invalid_forecast_bits_preserved':True,'cold_controls':cold,
            'existing_six_seed09_native_states_and_prior42_calendar_controls_reused_not_new_native_replays':True,
            'actual_complete152_source_preserved':True,'elapsed_seconds':time.monotonic()-started}
        create(OUT/f'case{i:02d}.json',record);records.append(record)
        print({'actual_full17_completed':len(records),'expected':17},flush=True)
        del value,oracle,prefix,oracle_prefix;gc.collect()
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual17_complete152_flag_only_neural_compositions_and51_cold_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_parent_round':152,'controls':records,
        'actual_full_cases':17,'actual_cold_cases':51,'rows_days_stocks':[5635800,1212,4650],
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False,'actual_future_X_read':False,
        'new_candidate_native_end_to_end_replays_and_full_registration_not_yet_done':True})
    create(A/'actual_ReusedNN166Full17_full_training_location_v1_20261009.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
