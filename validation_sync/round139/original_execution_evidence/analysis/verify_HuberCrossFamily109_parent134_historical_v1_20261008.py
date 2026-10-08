"""Full historical CDF controls on parent134; no claim of future round136 admission."""
from pathlib import Path
import os,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/HuberCrossFamily109_parent134_historical_v1_20261008')


def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
    assert np.array_equal(a.view('u8'),b.view('u8'))


def numeric_sha(x):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(x)).cast('B')).hexdigest()


def main():
    folder=A/'service_owned_workflows_20261006/CrossFamily30_native_and90_synthetic_controls_v1_20261008'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    import numpy as np,polars as pl,psutil
    from threadpoolctl import threadpool_limits
    from HuberCrossFamily_complete_parent_CDF_v1_20261008 import prepare,apply_prepared,transform,pandas_oracle,mixture,independent_mixture
    location=read(A/'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json');audit=Path(location['output'])/'verification.json'
    proof=read(audit);assert proof['actual_model_count']==30 and proof['actual_full_OOF_heads']==6
    plan_path=A/'HuberCrossFamily112_round139_plan_v1_20261008.json';plan=read(plan_path)
    canonical=A/'optimization_20261003_r134/full_registration_execution.json';assert read(canonical)['status']=='passed'
    receipt=A/'github_validation_sync_main_20261005/round134_receipt.json';assert read(receipt)['status']=='pushed_and_remote_head_verified'
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet';parent_path=A/'optimization_20261003_r134/selected_validation.npy'
    sources=[Path(__file__),A/'HuberCrossFamily_complete_parent_CDF_v1_20261008.py',plan_path,audit,canonical,receipt,frame_path,parent_path,
             *[Path(row['oof']) for row in plan['heads'].values()]]
    pins={str(p):sha(p) for p in sources}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_actual109_full_historical_controls.json',{'input_sha256':pins,'parent_round':134,'actual_quality_scores':0,'actual_future_X_and_labels_read':False,'final139_parent_not_yet_admitted':True})
    while psutil.virtual_memory().available<7*2**30:time.sleep(10)
    frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid'])
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    parent=np.load(parent_path,mmap_mode='r');assert parent.dtype==np.float64 and parent.shape==(len(frame),)
    dates=frame['trade_date'].to_numpy();flags=frame['flag_limit_up'].to_numpy();valid=frame['price_valid'].to_numpy();days=np.unique(dates)
    arrays={head:np.load(row['oof'],mmap_mode='r') for head,row in plan['heads'].items()}
    prepared=prepare(parent,dates);preserved=(dates<20210101)|(flags==1)|~valid
    residual0=np.zeros(len(parent),dtype=np.float64);exact(apply_prepared(parent,residual0,dates,flags,valid,0.,prepared),parent)
    records=[{'case':'exact_zero_amplitude_identity','full_bits_exact':True,'cold_controls':[]}];started=time.perf_counter()
    with threadpool_limits(limits=2):
        for group in range(6):
            for share in (.25,.5,.75):
                residual=mixture(arrays,group,share);oracle_residual=independent_mixture(arrays,group,share);exact(residual,oracle_residual)
                for amplitude in (.0025,.005,.01,.025,.05,.1):
                    value=apply_prepared(parent,residual,dates,flags,valid,amplitude,prepared)
                    exact(value,pandas_oracle(parent,oracle_residual,dates,flags,valid,amplitude));exact(value[preserved],np.asarray(parent[preserved]))
                    cold=[]
                    for count in (80,260,975):
                        n=count*4650;assert dates[n-1]==days[count-1] and dates[n]!=dates[n-1]
                        cold_residual=mixture({h:array[:n] for h,array in arrays.items()},group,share)
                        independent_cold=independent_mixture({h:array[:n] for h,array in arrays.items()},group,share);exact(cold_residual,residual[:n]);exact(cold_residual,independent_cold)
                        exact(transform(parent[:n],cold_residual,dates[:n],flags[:n],valid[:n],amplitude),value[:n])
                        exact(pandas_oracle(parent[:n],independent_cold,dates[:n],flags[:n],valid[:n],amplitude),value[:n])
                        cold.append({'days':count,'rows':n,'native_arithmetic_and_independent_CDF_bits_exact':True})
                    item={'group':group,'share':share,'amplitude':amplitude,'rows':len(parent),'full_primary_independent_bits_exact':True,
                          'preserved2020_flag1_invalid_bits_exact':True,'numeric_sha256':numeric_sha(value),'cold_controls':cold}
                    create(OUT/f'case{len(records)}.json',item);records.append(item)
                    print(f'Actual historical full CDF {len(records)}/109, group{group}, share{share}, amplitude{amplitude}',flush=True)
    for count in (80,260,975):
        n=count*4650;exact(transform(parent[:n],residual0[:n],dates[:n],flags[:n],valid[:n],0.),np.asarray(parent[:n]))
        records[0]['cold_controls'].append({'days':count,'rows':n,'exact_identity':True})
    assert len(records)==109 and sum(len(r['cold_controls']) for r in records)==327
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual109_parent134_Huber_crossfamily_CDF_and327_cold_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_parent_round':134,'parent_array_sha256':sha(parent_path),
        'actual_full_cases':109,'actual_cold_cases':327,'records':records,'elapsed_seconds':time.perf_counter()-started,
        'new_native_fits':0,'actual_official_scores':0,'actual_future_X_and_labels_read':False,
        'final139_current_parent_controls_still_required_after138_is_qualified':True,'finite_grid_not_global_exhaustion':True})
    create(A/'actual_HuberCrossFamily109_parent134_location_v1_20261008.json',{'status':'passed_actual109_parent134_Huber_crossfamily_controls_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_quality_scores':0})


if __name__=='__main__':main()
