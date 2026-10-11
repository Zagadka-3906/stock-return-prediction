"""Replay twelve annual states in42 two-seed historical/calendar stages and42 cold prefixes."""
from pathlib import Path
from types import SimpleNamespace
import sys,os,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/BF16TwoSeed154_native42_calendar_v1_20261009')
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR','CUDA_CACHE_PATH'):os.environ[key]=str(OUT/'tmp'/key)
os.environ['CUDA_CACHE_DISABLE']='1'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    gate=A/'service_owned_workflows_20261006/BF16TwoSeed154_equal_mean_full5_controls_v1_20261009'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(15)
    assert read(gate/'service_execution.json')['status']=='passed'
    import numpy as np,polars as pl,psutil
    from run import FEATURE_FILE,feature_names,to_matrix
    import BF16TwoSeed154_complete_parent_native_stage_v1_20261009 as stage
    from BF16Medium153_complete_parent_rank_CDF_v1_20261009 import ROLES
    banks=[Path(read(A/f'actual_BF16_medium2048_seed{seed}_e64_bank6_location_v1_20261009.json')['output']) for seed in ('09','10')]
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r148/selected_validation.npy'
    paths=[Path(__file__),Path(stage.__file__),A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
        FEATURE_FILE,framepath,parentpath,A/'BF16TwoSeed79_round154_proposal_v1_20261009.json']
    for seed,bank in zip(('09','10'),banks):
        paths.extend([A/f'neural_BF16_medium2048_seed{seed}_e64_native_v1_20261009.py',A/f'neural_BF16_medium2048_seed{seed}_independent_forward_v1_20261009.py',bank/'verification.json'])
        paths.extend(bank/str(y)/name for y in range(2020,2026) for name in ('info.json','model.joblib'))
        assert read(bank/'verification.json')['actual_native_fits']==6
    pins={str(p):sha(p) for p in paths};assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_actual_native42.json',{'input_sha256':pins,'states':list(range(2020,2026)),
        'actual_saved_states_expected':12,'historical_cases':30,'calendar_remapped_training_cases':12,'cold_cases':42,'actual_future_X_read':False})
    frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy();parent=np.load(parentpath,mmap_mode='r')
    features=feature_names();records=[];prefit=[]
    for year in range(2020,2026):
        while psutil.virtual_memory().available<9*2**30:time.sleep(15)
        sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];idx=np.flatnonzero(np.isin(dates,days));panel=frame[idx]
        xframe=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(['ts_code','trade_date',*features]).sort('trade_date','ts_code').collect()
        assert xframe.select(['ts_code','trade_date']).equals(panel.select(['ts_code','trade_date'])) and len(panel)==13950
        components=[]
        for bank,name in zip(banks,stage.NAMES):
            info=read(bank/str(year)/'info.json');components.append({'name':name,'path':str(bank/str(year)/'model.joblib'),
                'sha256':info['model_sha256'],'training_info':info,'configuration':info['configuration']})
        sourceparent=np.asarray(parent[idx],dtype=np.float64);x=to_matrix(xframe,features)
        for calendar in ((year,) if year<2025 else (2025,2026)):
            testdates=panel['trade_date'].to_numpy().copy()
            if year==2025:testdates=np.array([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)
            for sign in (1.,-1.):
                for role,weight in zip(ROLES,(.004,.064,.25)):
                    spec={'model':'fixed_equal_seed09_seed10_mean','role':role,'weight':weight,'sign':sign,'rank_universe':'all_current_raw_forecasts',
                        'first2020_active':True,'position':'after_complete_qualified_parent','seed_weights':[.5,.5],'seed_values':[20261009,20261010]}
                    context=SimpleNamespace(dates=testdates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                        _BF16_feature_names=features,_BF16_raw_features=x,_whole_graph={stage.GRAPH_KEY:spec})
                    out,full=stage.after_parent(SimpleNamespace(sha=sha),context,sourceparent,spec,components)
                    cold=SimpleNamespace(**vars(context))
                    for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(context,field)[:4650])
                    prefix,report=stage.after_parent(SimpleNamespace(sha=sha),cold,sourceparent[:4650],spec,components)
                    assert np.array_equal(prefix.view('u8'),out[:4650].view('u8')) and len(full['controls'])==len(report['controls'])==2
                    row={'model_year':year,'calendar_year':calendar,'historical_source_year':sourceyear,'actual_future_X_read':False,
                        'sign':sign,'role':role,'full':full,'cold':report,'whole_day_prefix_bits_exact':True}
                    create(OUT/f'case{len(records):02d}.json',row);records.append(row)
                    print(f'Actual two-seed154 native {len(records)}/42, pair{year}, calendar{calendar}, {role}, sign{sign:g}',flush=True)
            bad=SimpleNamespace(**vars(context));bad.dates=np.full(len(sourceparent),components[0]['training_info']['training_meta']['cutoff_exclusive'])
            try:stage.after_parent(SimpleNamespace(sha=sha),bad,sourceparent,spec,components)
            except AssertionError:prefit.append({'model_year':year,'calendar_year':calendar,'prefit_rejected_before_either_network':True})
            else:raise AssertionError('pre-fit calendar accepted')
    assert len(records)==42 and len(prefit)==7
    for f,d in pins.items():assert sha(f)==d,f
    create(OUT/'verification.json',{'status':'passed_actual_twelve_states42_two_seed_native_reload_independent_calendar_and42_cold_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'prefit_rejections':prefit,
        'actual_saved_states':12,'actual_historical_cases':30,'actual_calendar_cases':12,'actual_cold_cases':42,
        'actual_individual_native_model_replays':84,'actual_individual_cold_model_replays':84,
        'actual_future_X_read':False,'test_labels_read':False,'new_native_fits':0,'new_quality_scores':0})
    create(A/'actual_BF16TwoSeed154_native42_calendar_location_v1_20261009.json',{'status':'passed_actual_two_seed154_twelve_state_native42_cold42_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
