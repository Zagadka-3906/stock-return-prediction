"""Full49 historical5635800-row signed-Huber CDF and147 prefix controls; no scoring."""
from pathlib import Path
import os,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/HuberIRLS64_49_parent134_historical_v1_20261008')


def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))


def main():
    folder=A/'service_owned_workflows_20261006/nonflag_HuberIRLS64_actual_bank10_v1_20261008'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    import numpy as np,polars as pl,psutil
    from threadpoolctl import threadpool_limits
    from HuberIRLS64_complete_parent_CDF_v1_20261008 import HEADS,mixture,independent_mixture,prepare,apply_prepared,transform,pandas_oracle
    pointer=read(A/'actual_nonflag_HuberIRLS64_bank10_location_v1_20261008.json');bank=Path(pointer['output'])
    proof=read(bank/'verification.json');assert proof['actual_native_fits']==10 and proof['actual_full_OOF_heads']==2
    plan_path=A/'HuberIRLS64_52_round137_plan_v1_20261008.json';plan=read(plan_path);assert plan['new_case_count']==48 and plan['total_cases']==52
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    canonical=A/'optimization_20261003_r134/full_registration_execution.json';receipt=A/'github_validation_sync_main_20261005/round134_receipt.json'
    assert read(canonical)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet';parent_path=A/'optimization_20261003_r134/selected_validation.npy'
    heads=dict(zip(HEADS,proof['configurations']))
    sources=[Path(__file__),A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',A/'CrossFamily_complete_parent_CDF_v1_20261008.py',
        plan_path,bank/'verification.json',canonical,receipt,frame_path,parent_path,
        *[bank/name/'nonflag_oof_predictions.npy' for name in heads.values()],*[bank/name/'oof_verification.json' for name in heads.values()]]
    pins={str(p):sha(p) for p in sources};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual49_full_controls.json',{'input_sha256':pins,'actual_historical_parent':134,
        'actual_quality_scores':0,'future_X_and_Y_read':False,'actual_final137_parent_not_yet_admitted':True})
    while psutil.virtual_memory().available<7*2**30:time.sleep(10)
    frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid'])
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    parent=np.load(parent_path,mmap_mode='r');dates=frame['trade_date'].to_numpy();flags=frame['flag_limit_up'].to_numpy();valid=frame['price_valid'].to_numpy()
    arrays={head:np.load(bank/name/'nonflag_oof_predictions.npy',mmap_mode='r') for head,name in heads.items()}
    for head,array in arrays.items():
        oof=read(bank/heads[head]/'oof_verification.json');assert array.shape==(len(frame),) and sha(bank/heads[head]/'nonflag_oof_predictions.npy')==oof['prediction_array_sha256']
    prepared=prepare(parent,dates);preserved=(dates<20210101)|(flags==1)|~valid;zeros=np.zeros(len(frame),dtype=np.float64)
    exact(apply_prepared(parent,zeros,dates,flags,valid,0.,prepared),parent)
    records=[{'case':'identity','full_bits_exact':True,'cold_controls':[]}];started=time.perf_counter()
    with threadpool_limits(limits=2):
        for case in plan['new_cases']:
            group=case['group'];weight=case['amplitude'];residual=mixture(arrays,group);oracle=independent_mixture(arrays,group);exact(residual,oracle)
            value=apply_prepared(parent,residual,dates,flags,valid,weight,prepared);exact(value,pandas_oracle(parent,oracle,dates,flags,valid,weight))
            exact(value[preserved],np.asarray(parent[preserved]));cold=[]
            for count in (80,260,975):
                n=count*4650;assert dates[n]!=dates[n-1]
                first=mixture({head:array[:n] for head,array in arrays.items()},group);other=independent_mixture({head:array[:n] for head,array in arrays.items()},group)
                exact(first,residual[:n]);exact(first,other);exact(transform(parent[:n],first,dates[:n],flags[:n],valid[:n],weight),value[:n])
                exact(pandas_oracle(parent[:n],other,dates[:n],flags[:n],valid[:n],weight),value[:n]);cold.append({'days':count,'rows':n,'bits_exact':True})
            item={**case,'rows':len(frame),'full_primary_independent_CDF_bits_exact':True,'all_preserved_cohorts_bits_exact':True,
                'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),'cold_controls':cold}
            create(OUT/f'case{len(records)}.json',item);records.append(item);print(f'Actual Huber historical full CDF {len(records)}/49: group{group}, amplitude{weight}',flush=True)
    for count in (80,260,975):
        n=count*4650;exact(transform(parent[:n],zeros[:n],dates[:n],flags[:n],valid[:n],0.),np.asarray(parent[:n]));records[0]['cold_controls'].append({'days':count,'rows':n,'bits_exact':True})
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual49_parent134_HuberIRLS64_full_CDF_and147_cold_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_full_cases':len(records),
        'actual_cold_cases':sum(len(item['cold_controls']) for item in records),'actual_parent_round':134,
        'parent_array_sha256':sha(parent_path),'records':records,'elapsed_seconds':time.perf_counter()-started,
        'actual_official_scores':0,'new_native_fits':0,'future_X_and_Y_read':False,'exact_current137_parent_controls_still_required_after136_qualification':True})
    create(A/'actual_HuberIRLS64_49_parent134_location_v1_20261008.json',{'status':'passed_actual49_HuberIRLS64_historical_controls_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_quality_scores':0})


if __name__=='__main__':main()
