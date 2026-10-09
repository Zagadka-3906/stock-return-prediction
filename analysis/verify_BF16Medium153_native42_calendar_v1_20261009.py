"""Replay all six saved states in native and independent code; calendar probes use training X."""
from pathlib import Path
from types import SimpleNamespace
import sys,os,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/BF16Medium153_native42_calendar_v1_20261009')
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR','CUDA_CACHE_PATH'):os.environ[key]=str(OUT/'tmp'/key)
os.environ['CUDA_CACHE_DISABLE']='1'
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    service=A/'service_owned_workflows_20261006/BF16Medium153_independent_full5_GPU_controls_v1_20261009'
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
    assert read(service/'service_execution.json')['status']=='passed'
    import numpy as np,polars as pl
    from run import FEATURE_FILE,feature_names,to_matrix
    import neural_BF16_medium2048_seed09_e64_native_v1_20261009 as native
    import BF16Medium153_complete_parent_native_stage_v1_20261009 as stage
    from BF16Medium153_complete_parent_rank_CDF_v1_20261009 import ROLES
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed09_e64_bank6_v1_20261009')
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r148/selected_validation.npy'
    features=feature_names();keys=['ts_code','trade_date']
    paths=[Path(__file__),Path(stage.__file__),Path(native.__file__),A/'neural_BF16_medium2048_seed09_independent_forward_v1_20261009.py',
      A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
      FEATURE_FILE,framepath,parentpath,bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('info.json','model.joblib')]]
    pins={str(p):sha(p) for p in paths};assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_actual_native42.json',{'input_sha256':pins,'states':list(range(2020,2026)),
      'historical_cases':30,'calendar_remapped_training_cases':12,'cold_cases':42,'actual_future_X_read':False})
    frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy();parent=np.load(parentpath,mmap_mode='r')
    records=[];prefit=[]
    for year in range(2020,2026):
        sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];idx=np.flatnonzero(np.isin(dates,days));panel=frame[idx]
        xframe=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+features).sort('trade_date','ts_code').collect()
        assert xframe.select(keys).equals(panel.select(keys)) and len(panel)==13950
        info=read(bank/str(year)/'info.json');component={'name':'rank_MLP2048_BF16_seed09_e64','path':str(bank/str(year)/'model.joblib'),
          'sha256':info['model_sha256'],'training_info':info,'configuration':native.CONFIG}
        sourceparent=np.asarray(parent[idx],dtype=np.float64);x=to_matrix(xframe,features)
        for calendar in ((year,) if year<2025 else (2025,2026)):
            testdates=panel['trade_date'].to_numpy().copy()
            if year==2025:testdates=np.array([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)
            for sign in (1.,-1.):
                for role,weight in zip(ROLES,(.004,.064,.25)):
                    spec={'model':component['name'],'role':role,'weight':weight,'sign':sign,'rank_universe':'all_current_raw_forecasts','first2020_active':True,'position':'after_complete_qualified_parent'}
                    context=SimpleNamespace(dates=testdates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                      _BF16_feature_names=features,_BF16_raw_features=x,_whole_graph={stage.GRAPH_KEY:spec})
                    out,full=stage.after_parent(SimpleNamespace(sha=sha),context,sourceparent,spec,component)
                    cold=SimpleNamespace(**vars(context))
                    for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(context,field)[:4650])
                    prefix,report=stage.after_parent(SimpleNamespace(sha=sha),cold,sourceparent[:4650],spec,component)
                    assert np.array_equal(prefix.view('u8'),out[:4650].view('u8'))
                    row={'model_year':year,'calendar_year':calendar,'historical_source_year':sourceyear,'actual_future_X_read':False,
                      'sign':sign,'role':role,'full':full,'cold':report,'whole_day_prefix_bits_exact':True}
                    create(OUT/f'case{len(records):02d}.json',row);records.append(row)
                    print(f'Actual medium153 native {len(records)}/42, state{year}, calendar{calendar}, {role}, sign{sign:g}',flush=True)
            bad=SimpleNamespace(**vars(context));bad.dates=np.full(len(sourceparent),info['training_meta']['cutoff_exclusive'])
            try:stage.after_parent(SimpleNamespace(sha=sha),bad,sourceparent,spec,component)
            except AssertionError:prefit.append({'model_year':year,'calendar_year':calendar,'prefit_rejected_before_inference':True})
            else:raise AssertionError('pre-fit calendar accepted')
    assert len(records)==42 and len(prefit)==7
    for f,d in pins.items():assert sha(f)==d,f
    create(OUT/'verification.json',{'status':'passed_actual_six_medium_states42_native_reload_independent_calendar_and42_cold_controls',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'prefit_rejections':prefit,
      'actual_saved_states':6,'actual_historical_cases':30,'actual_calendar_cases':12,'actual_cold_cases':42,
      'actual_future_X_read':False,'test_labels_read':False,'new_native_fits':0,'new_quality_scores':0})
    create(A/'actual_BF16Medium153_native42_calendar_location_v1_20261009.json',{'status':'passed_actual_medium153_six_state_native42_cold42_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
