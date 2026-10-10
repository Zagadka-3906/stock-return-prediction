"""Train-only high-impact screening after fully qualified157; never a submission qualification."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from types import SimpleNamespace
import sys,os,time,gc,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
OUT=Path('E:/赛题五_本机临时/high_impact_cumulative_screen_v2_20261010')
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(OUT/'tmp'/key)
from run_dependency_queue_v3_20261006 import read,sha,create
import json

def write(path,value):
    temporary=path.with_name(path.name+f'.{os.getpid()}.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    os.replace(temporary,path)

def allowed():
    c=read(A/'current_user_runtime_control_20261010.json')
    read(A/'current_user_runtime_control_20261009.json')
    return c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])

def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))

def main():
    assert allowed()
    import numpy as np,polars as pl,psutil
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as percentiles
    from cached_official_spearman_runtime_20261007 import installed as spearman
    plan_path=A/'high_impact_cumulative_screen_plan_v2_20261010.json';plan=read(plan_path)
    for p,d in plan['input_sha256'].items():assert sha(p)==d,p
    assert plan['parent_round']==157 and len(plan['cases'])==97
    OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_any_controls_or_scores.json',{'plan':plan,'plan_sha256':sha(plan_path),'at_local':datetime.now().isoformat(),'submission_qualified':False})
    scoring=A/'high_impact_cumulative_screen_D_scoring_v2_20261010/scoring_validation_only'
    scoring.mkdir(parents=True,exist_ok=False)
    source=A/'optimization_20261003_r95/scoring_validation_only'
    for name in ('测试集_X.csv','测试集_Y.csv'):os.link(source/name,scoring/name)
    while psutil.virtual_memory().available<11.5*2**30:
        if not allowed():return
        write(OUT/'actual_stage.json',{'status':'waiting_actual_memory_before_training_only_screen','available_GiB':psutil.virtual_memory().available/2**30,'new_scores':0})
        time.sleep(15)
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    parent=np.load(A/'optimization_20261003_r157/selected_validation.npy',mmap_mode='r')
    baseline=read(A/'optimization_20261003_r157/calibrated_csv_official.json')['metrics']
    ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);rank_cache={};records=[]
    last_recipe=None;last_sign=None;prepared=None;raw=None
    for i,c in enumerate(plan['cases']):
        if not allowed():return
        if c['recipe'] is None:
            value=np.asarray(parent);controls=[]
        else:
            if c['recipe']!=last_recipe:
                prepared=None;raw=None;gc.collect()
                location=read(A/plan['bank_locations'][c['recipe']]);folder=Path(location['output'])
                assert sha(folder/'verification.json')==location['verification_sha256']
                rf=pl.read_parquet(folder/'combined_raw.parquet')
                assert frame.select(['ts_code','trade_date']).equals(rf.select(['ts_code','trade_date']))
                raw=rf['pred_raw'].to_numpy();last_recipe=c['recipe'];last_sign=None
            if c['sign']!=last_sign:
                prepared=codec.prepare(parent,raw,dates,flags,valid,c['sign']);last_sign=c['sign']
            value=codec.apply_prepared(parent,flags,valid,c['role'],c['weight'],prepared)
            oracle=codec.pandas_oracle(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign']);exact(value,oracle)
            mask=codec.selected(flags,valid,c['role']);exact(value[~mask],np.asarray(parent)[~mask])
            controls=[]
            for days in (80,260,975):
                n=days*4650
                prefix=codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign'])
                independent=codec.pandas_oracle(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign'])
                exact(value[:n],prefix);exact(value[:n],independent)
                controls.append({'days':days,'rows':n,'native_and_independent_bits_exact':True})
            del oracle,prefix,independent,mask;gc.collect()
        control={'case':i,'configuration':c,'rows':len(value),'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),
                 'full_independent_Pandas_exact':c['recipe'] is not None,'prefix_controls':controls,'complete_parent157_preserved_before_stage':True,'future_X_read':False}
        create(OUT/f'case{i:03d}_controls.json',control)
        write(OUT/'actual_stage.json',{'status':'actual_high_impact_train_only_official_scoring','at_local':datetime.now().isoformat(),'case':i,'completed_cases':len(records),'expected_cases':97,'configuration':c})
        assert allowed()
        with percentiles() as pct,spearman(rank_cache) as ic:
            with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,value)
        if c['recipe'] is None:assert metrics==baseline
        capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
        row={'case':i,'configuration':c,'metrics':metrics,'connected_final_score':metrics['final_score'],'score_gain_over_qualified_parent':metrics['final_score']-baseline['final_score'],
             'control_sha256':sha(OUT/f'case{i:03d}_controls.json'),'prediction_numeric_sha256':control['numeric_sha256'],'official_metric_capsule_sha256':sha(capsule),
             'official_score_cache':ctx.last_official_score_cache,'actual_return_mapping':ctx.last_candidate_return_mapping,
             'full_independent_and_three_cold_prefixes_passed':c['recipe'] is not None,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,
             'selection_bias_uncorrected':True,'new_scheme_native_replay_freeze_and_full_registration_required_before_adoption':True}
        create(OUT/f'case{i:03d}_official.json',row);records.append(row)
        best=max(records,key=lambda r:r['connected_final_score'])
        write(OUT/'best_so_far.json',{'completed_cases':len(records),'expected_cases':97,'best':best,'submission_qualified':False})
        print({'case':i,'configuration':c,'S':metrics['final_score'],'gain':row['score_gain_over_qualified_parent']},flush=True)
        del value;gc.collect()
    for p,d in plan['input_sha256'].items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed97_train_only_high_impact_cumulative_comparisons','at_local':datetime.now().isoformat(),'input_sha256':plan['input_sha256'],
           'records':records,'best':max(records,key=lambda r:r['connected_final_score']),'new_quality_score_records':97,'actual_nonidentity_full_controls':96,
           'actual_nonidentity_prefix_controls':288,'parent_round':157,'submission_qualified':False,'test_labels_read':False,'future_X_read':False,
           'global_feasible_direction_exhaustion_not_proven':True})
    create(A/'actual_high_impact_cumulative_screen_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
