"""Run all120 new signed cross-family cases and identity on historical134; independently verify full and cold bits."""
from pathlib import Path
import os,sys,json,time,hashlib,gc
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/CrossFamilyFine121_parent134_historical_v1_20261008')
def main():
    import numpy as np,polars as pl,psutil
    from threadpoolctl import threadpool_limits
    import CrossFamilyFine_complete_parent_CDF_v1_20261008 as codec
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    def exact(a,b):
        assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
        assert np.array_equal(a.view('u8'),b.view('u8'))
    plan_path=A/'CrossFamilyFine125_round145_proposal_v1_20261008.json';plan=read(plan_path)
    assert len(plan['new_cases'])==120 and plan['scientific_stage_base_round']==134 and set(plan['heads'])=={'ridge_l001','ridge_l025','rff_g00625','rff_g0125'}
    native_audit=Path(read(A/'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json')['output'])/'verification.json';audit=read(native_audit)
    assert audit['actual_model_count']==30 and audit['actual_full_OOF_heads']==6
    selected=[r for r in audit['actual_native_replay_records'] if r['head'] in plan['heads']]
    assert len(selected)==20 and {r['year'] for r in selected}=={2021,2022,2023,2024,2025}
    assert all(r['full_saved_reloaded_independent_bits_exact'] for r in selected)
    parent_path=A/'optimization_20261003_r134/selected_validation.npy';frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    full=A/'optimization_20261003_r134/full_registration_execution.json';receipt=A/'github_validation_sync_main_20261005/round134_receipt.json'
    assert read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
    sources=[Path(__file__),Path(codec.__file__),plan_path,native_audit,parent_path,frame_path,full,receipt,*[Path(r['oof']) for r in plan['heads'].values()]]
    pins={str(p):sha(p) for p in sources};assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_actual_full_controls.json',{'input_sha256':pins,'actual_stage_base_round':134,'proposed_quality_cases':125,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False,'all145_scoring_candidate_and_registry_receivers_still_required':True})
    # Ties, sentinel cohorts, signed directions, and shorter same-day calendars must preserve the exact operator.
    rng=np.random.default_rng(20261008);dates0=np.repeat(np.array([20201230,20210104,20210105,20210106]),37)
    base0=np.round(rng.normal(size=len(dates0)),1);flags0=(rng.random(len(base0))<.2).astype(int);valid0=rng.random(len(base0))>.2;base0[~valid0]=-1e6
    raw0={h:rng.normal(size=len(base0)) for h in plan['heads']};synthetic=[]
    for case in plan['new_cases']:
        residual=codec.mixture(raw0,case['group'],case['share']);independent=codec.independent_mixture(raw0,case['group'],case['share']);exact(residual,independent)
        value=codec.transform(base0,residual,dates0,flags0,valid0,case['amplitude']);exact(value,codec.pandas_oracle(base0,independent,dates0,flags0,valid0,case['amplitude']))
        preserved=(dates0<20210101)|(flags0==1)|~valid0;exact(value[preserved],base0[preserved])
        for days in (1,2,3):
            n=days*37;exact(codec.transform(base0[:n],residual[:n],dates0[:n],flags0[:n],valid0[:n],case['amplitude']),value[:n])
        synthetic.append({**case,'native_and_independent_bits_exact':True,'cold_day_prefixes':[1,2,3]})
    create(OUT/'synthetic120_controls.json',{'status':'passed120_signed_tied_and_preserved_cohort_synthetic_cases_and360_cold_controls','records':synthetic})
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    records=[];started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid'])
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        assert dates.min()>=20200101 and dates.max()<20250101
        base=np.load(parent_path,mmap_mode='r');assert base.dtype==np.float64 and base.shape==(5635800,)
        arrays={h:np.load(r['oof'],mmap_mode='r') for h,r in plan['heads'].items()};prepared=codec.prepare(base,dates)
        preserved=(dates<20210101)|(flags==1)|~valid;last_share=None;residual=independent=None
        for index,case in enumerate([*plan['new_cases'],{'group':None,'share':None,'amplitude':0.}]):
            if case['amplitude']==0.:
                residual=independent=np.zeros(len(base),dtype=np.float64)
            elif case['share']!=last_share:
                residual=codec.mixture(arrays,4,case['share']);independent=codec.independent_mixture(arrays,4,case['share']);exact(residual,independent);last_share=case['share']
            value=codec.apply_prepared(base,residual,dates,flags,valid,case['amplitude'],prepared)
            exact(value,codec.pandas_oracle(base,independent,dates,flags,valid,case['amplitude']));exact(value[preserved],np.asarray(base)[preserved])
            cold=[]
            for count in (80,260,975):
                n=count*4650;assert dates[n]!=dates[n-1]
                if case['amplitude']:
                    r=codec.mixture({h:x[:n] for h,x in arrays.items()},4,case['share']);other=codec.independent_mixture({h:x[:n] for h,x in arrays.items()},4,case['share']);exact(r,other);exact(r,residual[:n])
                else:r=other=np.zeros(n,dtype=np.float64)
                exact(codec.transform(base[:n],r,dates[:n],flags[:n],valid[:n],case['amplitude']),value[:n])
                exact(codec.pandas_oracle(base[:n],other,dates[:n],flags[:n],valid[:n],case['amplitude']),value[:n])
                cold.append({'days':count,'rows':n,'native_and_independent_arithmetic_and_CDF_bits_exact':True})
            item={**case,'rows':len(base),'primary_full_independent_bits_exact':True,'preserved2020_limit_up_invalid_bits_exact':True,
                'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),'cold_controls':cold}
            create(OUT/f'case{index:03d}.json',item);records.append(item);del value;gc.collect()
            print(json.dumps({'actual_full_controls':len(records),'expected':121,'configuration':case}),flush=True)
        scope.reverify()
    assert len(records)==121 and sum(len(r['cold_controls']) for r in records)==363
    create(OUT/'verification.json',{'status':'passed_actual120_new_signed_full_CDF360_cold_controls_and_identity_on_exact134_parent',
        'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'records':records,'actual_stage_base_round':134,
        'actual_nonzero_full_cases':120,'actual_nonzero_cold_cases':360,'actual_full_cases_including_identity':121,'actual_cold_cases_including_identity':363,
        'actual_synthetic_cases':120,'actual_synthetic_cold_cases':360,'actual_existing_native_model_records_revalidated':20,
        'elapsed_seconds':time.perf_counter()-started,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False,
        'all125_quality_and145_freeze_inference_complete_board_main_still_required':True,'finite_grid_not_global_exhaustion':True})
    create(A/'actual_CrossFamilyFine121_parent134_location_v1_20261008.json',{'status':'passed_actual_signed_fine_full_historical_controls_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})
if __name__=='__main__':main()
