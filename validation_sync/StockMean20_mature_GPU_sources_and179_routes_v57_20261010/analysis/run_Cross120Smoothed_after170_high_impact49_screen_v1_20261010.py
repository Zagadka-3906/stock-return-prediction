"""Test persistence of the two own120 forecasts after qualified170, without new fits."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import sys,os,time,gc,hashlib,json
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
OUT=Path('E:/赛题五_本机临时/Cross120Smoothed_after170_high_impact49_screen_v1_20261010')
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
POINTERS={'cross120recent252forward5huber050':'actual_BF16Cross120Recent252Forward5Huber050173_full5_independent_location_v1_20261009.json','cross120recent252rank5huber050':'actual_BF16Cross120Recent252Rank5Huber050174_full5_independent_location_v1_20261009.json'}

def cases():
    rows=[{'kind':'anchor170','recipe':None,'decay':None,'role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for recipe in POINTERS:
        for decay in (.25,.5,.75):
            for sign in (1.,-1.):
                for weight in (.004,.016):rows.append({'kind':'CDF','recipe':recipe,'decay':decay,'role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':None})
            for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
                for weight in (.016,.064):rows.append({'kind':kind,'recipe':recipe,'decay':decay,'role':'nonflag_valid','weight':weight,'sign':1.,'protect_fraction':.15})
    assert len(rows)==49;return rows

def write(path,value):
    temporary=path.with_name(path.name+f'.{os.getpid()}.tmp');temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(temporary,path)

def main():
    assert allowed();closed('Cross120170_complete132_family_v5_20261010')
    # Keep the main193 search ahead of this additional no-fit hypothesis family.
    closed('actual_Dual120Consensus_after169_high_impact193_screen_v3_20261010')
    import numpy as np,polars as pl,psutil
    import causal_neural_rank_smoothing_v1_20261010 as smoothing
    import immutable_prepared_rank_panel_cache_v1_20261010 as cache
    from cross120_after_complete169_native_stage_v2_20261010 import CODECS
    import importlib
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as percentiles
    from cached_official_spearman_runtime_20261007 import installed as spearman
    planpath=A/'cross120_smoothed49_predeclared_training_only_selection_plan_v1_20261010.json';plan=read(planpath)
    assert plan['cases']==cases() and plan['parent_round']==170
    for p,d in plan['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),planpath,Path(smoothing.__file__),Path(cache.__file__),A/'optimization_20261003_r170/selected_validation.npy',A/'optimization_20261003_r170/calibrated_csv_official.json',A/'optimization_20261003_r170/full_registration_execution.json',A/'connected_validation_20261002/combined_fold_frame.parquet']
    locations={recipe:Path(read(A/pointer)['output']) for recipe,pointer in POINTERS.items()}
    for recipe,folder in locations.items():
        assert read(folder/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
        paths += [A/POINTERS[recipe],folder/'verification.json',folder/'combined_raw.parquet']
    pins={**plan['input_sha256'],**{str(p):sha(p) for p in paths}}
    OUT.mkdir(exist_ok=False);create(OUT/'frozen_before_any_new_controls_or_scores.json',{'status':'frozen49_own120_neural_persistence_hypotheses_after_complete170','input_sha256':pins,'cases':cases(),'parent_round':170,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    scoring=OUT/'scoring_validation_only';scoring.mkdir()
    import shutil,tempfile
    for name in ('测试集_X.csv','测试集_Y.csv'):
        source=A/'optimization_20261003_r95/scoring_validation_only'/name;shutil.copyfile(source,scoring/name);assert sha(source)==sha(scoring/name)
    scratch=OUT/'tmp';scratch.mkdir()
    for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    tempfile.tempdir=str(scratch)
    from exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010 import installed as guard
    while psutil.virtual_memory().available<11.5*2**30:assert allowed();time.sleep(15)
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    grid=frame['ts_code'].to_numpy().reshape(1212,4650);assert np.all(grid==grid[0]) and np.array_equal(grid[0],np.asarray(sorted(grid[0]))) and len(set(grid[0]))==4650
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')];parent=np.load(A/'optimization_20261003_r170/selected_validation.npy',mmap_mode='r');baseline=read(A/'optimization_20261003_r170/calibrated_csv_official.json')['metrics']
    ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);records=[];ranks={};active={'recipe':None,'decay':None,'panel':None,'raw':None}
    exact=lambda a,b:np.array_equal(np.asarray(a,dtype=np.float64).view('u8'),np.asarray(b,dtype=np.float64).view('u8'))
    def transformed(c,n=None,oracle=False):
        n=len(parent) if n is None else n
        if c['recipe'] is None:return np.asarray(parent[:n])
        if active['recipe']!=c['recipe']:
            active['panel']=None;active['raw']=None;gc.collect();rf=pl.read_parquet(locations[c['recipe']]/'combined_raw.parquet');assert rf.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']));active['raw']=rf['pred_raw'].to_numpy();active['recipe']=c['recipe'];active['decay']=None
        if oracle:
            signal=smoothing.smooth(active['raw'][:n],dates[:n],valid[:n],c['decay'],oracle=True);codec=importlib.import_module(CODECS[c['kind']]);args=(c['role'],c['weight'],c['sign']) if c['kind']=='CDF' else (c['weight'],c['protect_fraction'],c['sign'])
            return codec.pandas_oracle(parent[:n],signal,dates[:n],flags[:n],valid[:n],*args)
        if active['decay']!=c['decay']:
            active['panel']=None;gc.collect();signal=smoothing.smooth(active['raw'],dates,valid,c['decay']);assert exact(signal,smoothing.smooth(active['raw'],dates,valid,c['decay'],oracle=True));active['panel']=cache.Panel(parent,signal,dates,flags,valid);active['decay']=c['decay']
        if n==len(parent):return active['panel'].transform(c)
        # Prefix smooth is computed from the prefix only, including its own initial state.
        signal=smoothing.smooth(active['raw'][:n],dates[:n],valid[:n],c['decay']);return cache.Panel(parent[:n],signal,dates[:n],flags[:n],valid[:n]).transform(c)
    with guard(scoring,OUT/'actual_E_TRAIN_cache_guard_binding_v2_20261010.json'):
        for i,c in enumerate(cases()):
            assert allowed();value=transformed(c);checks=[]
            if i:
                assert exact(value,transformed(c,oracle=True))
                codec=importlib.import_module(CODECS[c['kind']])
                if c['kind']=='CDF':assert exact(value[~codec.selected(flags,valid,c['role'])],parent[~codec.selected(flags,valid,c['role'])])
                else:codec.assert_invariants(parent,value,dates,flags,valid,c['protect_fraction'])
                for days in (80,260,975):
                    n=days*4650;assert exact(value[:n],transformed(c,n)) and exact(value[:n],transformed(c,n,True));checks.append({'days':days,'native_and_independent_Pandas_prefix_bits_exact':True})
            numeric=hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()
            create(OUT/f'case{i:03d}_controls.json',{'case':i,'configuration':c,'numeric_sha256':numeric,'rows':len(value),'full_independent_Pandas_exact':bool(i),'prefix_controls':checks,'stock_identity_grid_verified':True,'state_not_reset_at_annual_boundaries':True,'future_X_read':False})
            write(OUT/'actual_stage.json',{'case':i,'completed_cases':len(records),'expected_cases':49,'at_local':datetime.now().isoformat()})
            assert allowed()
            with percentiles(),spearman(ranks),installed(scoring/'submission.csv'):metrics=score(ctx,value)
            if not i:assert metrics==baseline
            capsule=Path(ctx.last_official_score_cache['official_metrics_source']);row={'case':i,'configuration':c,'metrics':metrics,'connected_final_score':metrics['final_score'],'score_gain_over_qualified_parent':metrics['final_score']-baseline['final_score'],'control_sha256':sha(OUT/f'case{i:03d}_controls.json'),'prediction_numeric_sha256':numeric,'official_metric_capsule_sha256':sha(capsule),'official_score_cache':ctx.last_official_score_cache,'actual_return_mapping':ctx.last_candidate_return_mapping,'new_native_fits':0,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'selection_bias_uncorrected':True}
            create(OUT/f'case{i:03d}_official.json',row);records.append(row);write(OUT/'best_so_far.json',{'completed_cases':len(records),'expected_cases':49,'best':max(records,key=lambda r:r['connected_final_score']),'submission_qualified':False});print({'case':i,'S':metrics['final_score'],'configuration':c},flush=True);del value;gc.collect()
        for p,d in pins.items():assert sha(p)==d,p
        create(OUT/'verification.json',{'status':'passed49_own120_forecast_persistence_after_complete170_TRAIN_only_official_comparisons','input_sha256':pins,'records':records,'best':max(records,key=lambda r:r['connected_final_score']),'new_quality_score_records':49,'actual_nonidentity_full_controls':48,'actual_nonidentity_prefix_controls':144,'new_native_fits':0,'submission_qualified':False,'future_X_read':False,'test_labels_read':False})
        create(A/'actual_Cross120Smoothed_after170_high_impact49_screen_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
