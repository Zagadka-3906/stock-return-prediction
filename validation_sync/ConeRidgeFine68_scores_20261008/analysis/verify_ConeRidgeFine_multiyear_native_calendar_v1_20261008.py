"""Use final2025 saved models on date-remapped training X only; not future qualification."""
from pathlib import Path
from types import SimpleNamespace
import os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/ConeRidgeFine_multiyear_native_calendar_v1_20261008')


def main():
    import numpy as np,polars as pl
    from run import FEATURE_FILE,feature_names
    import ConeRidge64_complete_parent_native_stage_v1_20261008 as cross
    from ConeRidge64_complete_parent_CDF_v1_20261008 import GROUPS
    plan=read(A/'ConeRidgeFine68_round143_plan_v1_20261008.json')
    feature_names_=feature_names();frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    teacher_path=A/'optimization_20261003_r106/selected_validation.npy';parent_path=A/'optimization_20261003_r134/selected_validation.npy'
    authoritative=ROOT/'candidates/optimization_20261003_r134/submission.csv'
    authoritative_proof=ROOT/'candidates/optimization_20261003_r134/verification.json'
    assert read(authoritative_proof)['status']=='passed'
    sources=[Path(__file__),FEATURE_FILE,frame_path,teacher_path,parent_path,authoritative,authoritative_proof,
        A/'ConeRidgeFine68_round143_plan_v1_20261008.json',
        A/'ConeRidge64_complete_parent_native_stage_v1_20261008.py',A/'ConeRidge64_complete_parent_CDF_v1_20261008.py']
    all_components={'CrossFamily':{}}
    for head,row in plan['heads'].items():
        info_path=Path(row['infos']['2025']);info=read(info_path);kind=row['state_kind']
        item={'head':head,'name':info['name'],'state_kind':row['native_stage_state_kind'],
            'path':info['native_model_path'],'sha256':info['native_model_sha256'],
            'independent_state_path':info['independent_'+kind+'_state_path'],
            'independent_state_sha256':info['independent_'+kind+'_state_sha256'],'training_info':info}
        all_components['CrossFamily'][head]=item;sources += [info_path,Path(item['path']),Path(item['independent_state_path'])]
    pins={str(p):sha(p) for p in dict.fromkeys(sources)};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_calendar_controls.json',{'input_sha256':pins,'new_fits':0,'new_quality_scores':0,
        'actual_future_feature_X_and_Y_read':False,'already_qualified_R134_only_trade_date_column_read':True})
    # Read only the already-qualified output's dates for schema evidence; no forecasts or future X/Y.
    calendar=pl.scan_csv(authoritative).select(pl.col('trade_date').min().alias('first'),pl.col('trade_date').max().alias('last'),
        pl.col('trade_date').n_unique().alias('days'),(pl.col('trade_date')//10000).unique().sort().implode().alias('years')).collect().to_dicts()[0]
    assert calendar=={'first':20250102,'last':20260608,'days':344,'years':[2025,2026]}
    keys=['ts_code','trade_date'];frame=pl.read_parquet(frame_path,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy()
    days=np.unique(dates[dates//10000==2024])[:3];positions=np.flatnonzero(np.isin(dates,days));panel=frame[positions]
    test=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+feature_names_).sort('trade_date','ts_code').collect()
    assert test.select(keys).equals(panel.select(keys)) and len(panel)==13950 and not {'y_rank','y_ret_1d'}&set(test.columns)
    teacher=np.asarray(np.load(teacher_path,mmap_mode='r')[positions],dtype=np.float64)
    parent=np.asarray(np.load(parent_path,mmap_mode='r')[positions],dtype=np.float64)
    raw=test.select(feature_names_).to_numpy().astype(np.float64)
    calendar_sets={'single2025':(20251229,20251230,20251231),'boundary2025_2026':(20251229,20251230,20260102),'single2026':(20260102,20260105,20260106)}
    records=[];namespace=SimpleNamespace(read=read,sha=sha)
    for family,module in (('CrossFamily',cross),):
        for group in range(8):
            spec={'group':group,'amplitude':.025,'universe':'all_current_raw_forecasts','position':'after_complete_qualified_parent',
                'teacher_feature':'qualified106_current_forecast_average_rank_over_N'}
            if family=='CrossFamily':spec['share']=.5;needed=list(dict.fromkeys(h for heads,sign in GROUPS[group] for h in heads))
            else:needed=required_heads(group)
            components=[all_components[family][head] for head in needed];reference=None
            for label,mapped in calendar_sets.items():
                ctx=SimpleNamespace(dates=np.repeat(np.array(mapped,dtype=dates.dtype),4650),flags=panel['flag_limit_up'].to_numpy(),
                    valid=panel['price_valid'].to_numpy(),_nonflag_raw_features=raw,_nonflag_raw_feature_names=feature_names_,_whole_graph={module.GRAPH_KEY:spec})
                value,report=module.after_parent(namespace,ctx,teacher,parent,spec,components)
                assert report['year']==2025 and report['saved_fit_year_fixed_for_all_prediction_dates']
                if reference is None:reference=value
                module.exact(value,reference)
                cold_ctx=SimpleNamespace(**vars(ctx))
                for field in ('dates','flags','valid','_nonflag_raw_features'):setattr(cold_ctx,field,getattr(ctx,field)[:4650])
                cold,cold_report=module.after_parent(namespace,cold_ctx,teacher[:4650],parent[:4650],spec,components);module.exact(cold,value[:4650])
                # A second day from2026 is admissible without labels or a replacement model.
                day_ctx=SimpleNamespace(**vars(ctx))
                for field in ('dates','flags','valid','_nonflag_raw_features'):setattr(day_ctx,field,getattr(ctx,field)[9300:])
                day,day_report=module.after_parent(namespace,day_ctx,teacher[9300:],parent[9300:],spec,components);module.exact(day,value[9300:])
                item={'family':family,'group':group,'calendar':label,'full':report,'first_day':cold_report,'last_day':day_report,
                    'date_remapping_forecast_bits_exact':True,'same_saved2025_models_no_refit':True}
                create(OUT/f'control{len(records)+1}.json',item);records.append(item)
            print(f'Actual calendar native controls: {family} group{group}, fixed2025 model across2026.',flush=True)
    # Reject model-year inconsistency and cutoff leakage instead of silently changing the model.
    from copy import deepcopy
    rejected=[]
    for family,module in (('CrossFamily',cross),):
        spec={'group':0,'amplitude':.025,'universe':'all_current_raw_forecasts','position':'after_complete_qualified_parent',
            'teacher_feature':'qualified106_current_forecast_average_rank_over_N'}
        if family=='CrossFamily':spec['share']=.5;needed=list(dict.fromkeys(h for heads,sign in GROUPS[0] for h in heads))
        else:needed=required_heads(0)
        components=[deepcopy(all_components[family][head]) for head in needed]
        ctx=SimpleNamespace(dates=np.full(4650,20241231,dtype=dates.dtype),flags=panel['flag_limit_up'].to_numpy()[:4650],
            valid=panel['price_valid'].to_numpy()[:4650],_nonflag_raw_features=raw[:4650],_nonflag_raw_feature_names=feature_names_,_whole_graph={module.GRAPH_KEY:spec})
        try:module.after_parent(namespace,ctx,teacher[:4650],parent[:4650],spec,components)
        except AssertionError:rejected.append({'family':family,'pre_fit_calendar_rejected':True})
        else:raise AssertionError('Future2025 fit was incorrectly admitted into2024.')
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual24_ConeRidge_saved2025_calendar_controls_and48_day_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'authoritative_frozen_output_calendar':calendar,
        'records':records,'actual_calendar_cases':24,'actual_whole_day_controls':64,'rejected_pre_fit_cases':rejected,
        'new_fits':0,'new_official_scores':0,'actual_future_feature_X_and_Y_read':False,
        'historical_X_date_remapping_is_not_actual_future_candidate_qualification':True})
    create(A/'actual_ConeRidgeFine_multiyear_calendar_location_v1_20261008.json',{'status':'passed_actual24_ConeRidgeFine_multiyear_calendar_controls_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_quality_scores':0})


if __name__=='__main__':main()
