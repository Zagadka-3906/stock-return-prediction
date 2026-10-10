"""Full raw-bit and cold controls for85 branch refinements on an actually qualified parent112."""
from pathlib import Path
import hashlib
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    import psutil
    from refine_flagged_HGB_compatible_parent_transform_20261007 import prepare,apply_prepared,transform,compatible
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    assert read(A/'quantile_HGB_native_hook7_preflight_20261007/verification.json')['status']=='passed_actual7_historical603_quantile_HGB_native_independent_and_whole_day_prefix_controls'
    out=A/'quantile_HGB88_transform_preflight_20261007';assert not out.exists();out.mkdir()
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    plan_path=A/'quantile_HGB88_plan_20261007.json';plan=read(plan_path)
    reference_path=A/'optimization_20261003_r106/selected_validation.npy';parent_path=A/'optimization_20261003_r112/selected_validation.npy'
    bank=A/plan['existing_native_bank'];proof=read(bank/'verification.json')
    assert proof['actual_native_fits']==len(proof['actual_models'])==20
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    sources=[Path(__file__),plan_path,A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',
        A/'direct_flag_centered_rank_CDF_transform_20261007.py',A/'conditional_residual_mlp_CDF_transform_20261007.py',
        reference_path,parent_path,frame_path,bank/'verification.json',*[bank/n/'flagged_oof_predictions.npy' for n in plan['single_native_heads']]]
    pins={**plan['input_sha256'],**{str(p):sha(p) for p in sources}}
    for model in proof['actual_models']:
        for path_key,sha_key in (('native_model_path','native_model_sha256'),('independent_hist_tree_state_path','independent_hist_tree_state_sha256')):
            pins[model[path_key]]=model[sha_key]
    create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'labels_read':False})
    with LockedReadHashCache(pins) as scope:
        assert compatible(read(ROOT/'candidates/optimization_20261003_r112/verification.json')['whole_scheme_graph'],
            read(ROOT/'candidates/simplex_residual47_20261006/verification.json')['whole_scheme_graph'])
        frame=pl.read_parquet(frame_path,columns=['trade_date','ts_code','flag_limit_up','price_valid'])
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        reference=np.load(reference_path,mmap_mode='r');parent=np.load(parent_path,mmap_mode='r')
        head={n:np.load(bank/n/'flagged_oof_predictions.npy',mmap_mode='r') for n in plan['single_native_heads']}
        for name,names in plan['ensembles'].items():
            values=np.zeros(len(reference),dtype=np.float64)
            for n in names:values+=head[n]
            values/=len(names);head[name]=values
        head['remove_flagged_HGB']=np.zeros(len(reference),dtype=np.float64)
        prepared=prepare(reference,dates,flags,valid,plan['universe'])
        oracle=[];days,starts=np.unique(dates,return_index=True);ends=np.r_[starts[1:],len(dates)]
        for day,left,right in zip(days,starts,ends):
            positions=np.flatnonzero(flags[left:right]==1)+left
            pct=pd.Series(reference[left:right]).rank(method='average',pct=True).to_numpy()[positions-left]
            ordered=np.sort(np.asarray(reference[left:right]),kind='mergesort');knots=np.arange(1,len(ordered)+1,dtype=np.float64)/len(ordered)
            oracle.append((day,positions,pct,ordered,knots))
        cases=[(name,weight) for name in [*plan['single_native_heads'],*plan['ensembles']] for weight in plan['weights']]+[('remove_flagged_HGB',0.)]
        assert len(cases)==85
        controls=[]
        nonflag=flags!=1;year2020=dates<20210101
        for name,weight in cases:
            values=apply_prepared(parent,reference,flags,head[name],weight,prepared)
            independent=np.asarray(parent).copy();independent[flags==1]=reference[flags==1]
            if weight>0.:
                for day,positions,pct,ordered,knots in oracle:
                    if day<20210101:assert np.all(head[name][positions]==0.);continue
                    q=pct+weight*head[name][positions]
                    independent[positions]=np.interp(np.minimum(np.maximum(q,knots[0]),knots[-1]),knots,ordered)
            assert np.array_equal(values.view('u8'),independent.view('u8'))
            assert np.array_equal(values[nonflag].view('u8'),parent[nonflag].view('u8'))
            assert np.array_equal(values[year2020].view('u8'),parent[year2020].view('u8'))
            for count in (80,260,975):
                n=int(ends[count-1]);cold=transform(parent[:n],reference[:n],dates[:n],flags[:n],valid[:n],head[name][:n],weight,plan['universe'])
                assert np.array_equal(cold.view('u8'),values[:n].view('u8'))
            controls.append({'head':name,'weight':weight,'full5635800_independent_Pandas_CDF_bits_exact':True,
                'cold80_260_975_bits_exact':True,'all_nonflag_and2020_complete_parent_bits_unchanged':True,
                'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
        scope.reverify()
    create(out/'verification.json',{'status':'passed_actual85_full5635800_quantile_HGB_independent_oracle_and_cold80_260_975_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'controls':controls,
        'actual_qualified_parent112_nonflag_and2020_preserved_bits_exact':True,
        'parent117_118_graphs_not_used_by_reference112_preflight':True,'current_parent112_full_graph_compatibility':True,
        'no_labels_or_future_features_read':True,'new_native_fits':0,'new_quality_scores':0,
        'actual_future_inference_or_full119_QA30_not_claimed':True,'test_labels_read':False})
    print({'status':'passed','full5635800_cases':85,'cold_prefix_cases':255,'new_quality_scores':0},flush=True)


if __name__=='__main__':main()
