"""Actual full73 independent CDF oracles and219 whole-day cold prefixes, no quality scoring."""
from pathlib import Path
import sys,time,os,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    import numpy as np,pandas as pd,polars as pl,psutil
    from nonflag_residual_HGB_CDF_transform_20261007 import prepare,apply_prepared,transform
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    f=A/'service_owned_workflows_20261006/nonflag_residual_RFF128Low_native_bank10_v2'
    while owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed'
    while psutil.virtual_memory().available<9*2**30:time.sleep(10)
    bank=A/'nonflag_residual_RFF128Low_bank10_20261007';proof=read(bank/'verification.json')
    assert proof['status']=='passed_actual10_nonflag_residual_RFF128Low_mature_native_reload_independent_and_prefix_controls' and proof['actual_native_fits']==10
    out=A/'nonflag_residual_RFF128Low73_transform_preflight_20261007';assert not out.exists();out.mkdir()
    plan_path=A/'nonflag_RFF128Low76_plan_20261007.json';plan=read(plan_path)
    reference_path=A/'optimization_20261003_r106/selected_validation.npy';parent_path=A/'optimization_20261003_r112/selected_validation.npy'
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    paths=[Path(__file__),A/'nonflag_residual_HGB_CDF_transform_20261007.py',plan_path,bank/'verification.json',reference_path,parent_path,frame_path,
      *[bank/n/'nonflag_oof_predictions.npy' for n in plan['single_native_heads']]]
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in paths}}
    create(out/'frozen_before_actual_full_controls.json',{'input_sha256':pins,'expected_full_cases':73,'expected_cold_controls':219,'new_quality_scores':0,'test_labels_read':False})
    controls=[]
    with LockedReadHashCache(pins) as scope:
        frame=pl.read_parquet(frame_path,columns=['trade_date','ts_code','flag_limit_up','price_valid'])
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        reference=np.load(reference_path,mmap_mode='r');parent=np.load(parent_path,mmap_mode='r')
        head={n:np.load(bank/n/'nonflag_oof_predictions.npy',mmap_mode='r') for n in plan['single_native_heads']}
        ensemble=np.zeros(len(parent),dtype=np.float64)
        for n in plan['single_native_heads']:ensemble+=head[n]
        ensemble/=2.;head['equal_mean_two']=ensemble;head['remove_nonflag_RFF128Low']=np.zeros(len(parent),dtype=np.float64)
        prepared=prepare(reference,dates,flags,valid,'all_current_raw_forecasts')
        oracle=[];days,starts=np.unique(dates,return_index=True);ends=np.r_[starts[1:],len(dates)]
        for day,left,right in zip(days,starts,ends):
            if day<20210101:continue
            positions=np.flatnonzero(flags[left:right]!=1)+left
            percentile=pd.Series(reference[left:right]).rank(method='average',pct=True).to_numpy()[positions-left]
            ordered=np.sort(np.asarray(reference[left:right]),kind='mergesort');knots=np.arange(1,right-left+1,dtype=np.float64)/(right-left)
            oracle.append((int(day),positions,percentile,knots,ordered))
        cases=[(n,w,s) for n in [*plan['single_native_heads'],'equal_mean_two'] for s in (-1,1) for w in plan['weights']]+[('remove_nonflag_RFF128Low',0.,1)];assert len(cases)==73
        for n,w,sign in cases:
            actual=apply_prepared(parent,reference,flags,head[n]*sign,w,prepared);independent=np.asarray(parent).copy()
            for day,positions,pct,knots,ordered in oracle:
                if w==0.:independent[positions]=reference[positions]
                else:independent[positions]=np.interp(np.minimum(np.maximum(pct+w*(head[n][positions]*sign),knots[0]),knots[-1]),knots,ordered)
            assert np.array_equal(actual.view('u8'),independent.view('u8'))
            assert np.array_equal(actual[flags==1].view('u8'),parent[flags==1].view('u8'))
            assert np.array_equal(actual[dates<20210101].view('u8'),parent[dates<20210101].view('u8'))
            for count in (80,260,975):
                size=int(ends[count-1]);cold=transform(parent[:size],reference[:size],dates[:size],flags[:size],valid[:size],head[n][:size]*sign,w,'all_current_raw_forecasts')
                assert np.array_equal(cold.view('u8'),actual[:size].view('u8'))
            controls.append({'head':n,'weight':w,'residual_sign':sign,'full5635800_independent_Pandas_CDF_bits_exact':True,'flagged_and2020_parent_bits_preserved':True,
              'cold80_260_975_bits_exact':True,'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(actual)).cast('B')).hexdigest()})
        scope.reverify()
    create(out/'verification.json',{'status':'passed_actual73_full5635800_nonflag_residual_RFF128Low_independent_CDF_and219_cold_controls',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'controls':controls,'actual_full_cases':73,'actual_cold_cases':219,
      'qualified_parent112_reference106_only_future118_119_not_used_by_this_preflight':True,'new_native_fits':0,'new_quality_scores':0,
      'official40_comparisons_and_round126_candidate_QA37_not_claimed':True,'test_labels_read':False})
    print({'status':'passed','full_cases':73,'cold_controls':219},flush=True)
if __name__=='__main__':main()
