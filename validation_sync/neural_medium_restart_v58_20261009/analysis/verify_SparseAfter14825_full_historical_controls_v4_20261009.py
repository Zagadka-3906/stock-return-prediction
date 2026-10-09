"""Verify all55 frozen mixtures on the entire training OOF panel with independent Pandas and165 day-prefix controls."""
from pathlib import Path
import gc
import hashlib
import os
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for option in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[option]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/SparseAfter14825_parent148_historical_v1_20261009')


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'service_execution.json').exists():time.sleep(10)
    while owned(read(folder/'native_launch.json')):time.sleep(1)
    assert read(folder/'service_execution.json')['status']=='passed',name


def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
    assert np.array_equal(a.view('u8'),b.view('u8'))


def main():
    closed('SparseAfter14860_native_historical_calendar_controls_v2_20261009')
    closed('AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009')
    import numpy as np
    import polars as pl
    import psutil
    from threadpoolctl import threadpool_limits
    import SparseAfter148_complete_parent_CDF_v1_20261009 as codec
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    proposal=A/'SparseAfter14829_round152_proposal_v1_20261009.json';plan=read(proposal)
    pointer=A/'actual_SparseAfter14860_native_calendar_location_v1_20261009.json'
    native_path=Path(read(pointer)['output'])/'verification.json'
    assert sha(native_path)==read(pointer)['verification_sha256']
    native=read(native_path)
    assert native['actual_historical_cases']==48 and native['actual_calendar_cases']==12
    assert native['actual_cold_cases']==60 and native['actual_prefit_final_model_date_rejections']==12
    assert len(plan['new_cases'])==25 and plan['fixed_scientific_stage_base_round']==148
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet'
    parent=A/'optimization_20261003_r148'
    receipt=A/'github_validation_sync_main_20261005/round148_receipt.json'
    assert read(parent/'full_registration_execution.json')['status']=='passed'
    assert read(receipt)['status']=='pushed_and_remote_head_verified'
    sources=[Path(__file__),Path(codec.__file__),A/'HuberCrossFamily_complete_parent_CDF_v1_20261008.py',
        proposal,pointer,native_path,framepath,parent/'selected_validation.npy',parent/'full_registration_execution.json',receipt,
        *[Path(row['oof']) for row in plan['heads'].values()]]
    pins={**native['input_sha256'],**{str(path):sha(path) for path in sources}}
    OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_actual25_full_controls.json',{
        'input_sha256':pins,'actual_stage_base_round':148,'cases':plan['new_cases'],
        'expected_full_cases':25,'expected_cold_cases':75,'resource_start_threshold_GiB':12,
        'native_thread_limit':2,'all_current_parent_forecasts_include_flag1_and_invalid_CDF_knots':True,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False})
    while psutil.virtual_memory().available<12*2**30:time.sleep(10)
    records=[];started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid'])
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        dates,flags,valid=[frame[name].to_numpy() for name in ('trade_date','flag_limit_up','price_valid')]
        assert dates.max()<20250101
        base=np.load(parent/'selected_validation.npy',mmap_mode='r')
        raw={head:np.load(row['oof'],mmap_mode='r') for head,row in plan['heads'].items()}
        assert base.dtype==np.float64 and base.shape==(5635800,)
        assert all(x.dtype==np.float64 and x.shape==base.shape for x in raw.values())
        residuals={(g,s):codec.mixture(raw,g,s) for g in range(6) for s in (.5,)}
        for (group,share),value in residuals.items():exact(value,codec.independent_mixture(raw,group,share))
        prepared=codec.prepare(base,dates)
        preserved=(dates<20210101)|(flags==1)|~valid
        for index,case in enumerate(plan['new_cases']):
            residual=residuals[(case['group'],case['share'])]
            value=codec.apply_prepared(base,residual,dates,flags,valid,case['amplitude'],prepared)
            exact(value,codec.pandas_oracle(base,residual,dates,flags,valid,case['amplitude']))
            exact(value[preserved],np.asarray(base)[preserved])
            cold=[]
            for days in (80,260,975):
                n=days*4650;assert dates[n-1]!=dates[n]
                cold_raw={h:x[:n] for h,x in raw.items()}
                cold_residual=codec.mixture(cold_raw,case['group'],case['share'])
                exact(value[:n],codec.transform(base[:n],cold_residual,dates[:n],flags[:n],valid[:n],case['amplitude']))
                exact(value[:n],codec.pandas_oracle(base[:n],codec.independent_mixture(cold_raw,case['group'],case['share']),dates[:n],flags[:n],valid[:n],case['amplitude']))
                cold.append({'days':days,'rows':n,'native_independent_mixture_and_Pandas_bits_exact':True})
            if case['amplitude']==0.:exact(value,np.asarray(base))
            heads=list(dict.fromkeys(h for group,sign in codec.GROUPS[case['group']] for h in group)) if case['amplitude'] else []
            row={'case':index,'configuration':case,'rows':len(value),'full_independent_Pandas_bits_exact':True,
                'preserved2020_flag1_invalid_bits_exact':True,'cold_controls':cold,'ordered_native_heads':heads,
                'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),
                'qualified_anchor_numeric_identity_round':148 if case['amplitude']==0. else None}
            create(OUT/f'case{index:03d}.json',row);records.append(row)
            del value;gc.collect()
            print({'actual_full_controls':len(records),'expected':25,'case':index},flush=True)
        scope.reverify()
    assert len(records)==25 and sum(len(row['cold_controls']) for row in records)==75
    create(OUT/'verification.json',{'status':'passed_actual25_SparseAfter148_full_training_CDF_and75_cold_controls_with_exact148_identity',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,
        'actual_stage_base_round':148,'actual_full_cases_including_identity':25,'actual_cold_cases_including_identity':75,
        'existing10_saved_states_reused_not_new_fits':True,'elapsed_seconds':time.perf_counter()-started,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False,
        'all29_quality_receivers_duplicate_audit_freeze_inference_full_board_and_main_still_required':True})
    create(A/'actual_SparseAfter14825_parent148_location_v1_20261009.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})


if __name__=='__main__':main()
