"""Normalize both completed protected screens and actual anchors, then qualify the selected saved stage."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime,timezone,timedelta
import sys,time,hashlib,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_rank20_embedding85_selected_native14_v2_20261011')
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def allowed():
    c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    return c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])

def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while allowed():
        if (f/'service_execution.json').is_file() and (f/'native_launch.json').is_file() and not owned(read(f/'native_launch.json')):
            assert read(f/'service_execution.json')['status']=='passed',name;return
        time.sleep(10)
    raise RuntimeError('User stop reached before selected tail native qualification')

def main():
    assert allowed()
    closed('actual_stock_rank20_embedding85_after182_normalization_queue_v5_20261010')
    closed('actual_stock_rank20_embedding_six_state_native42_v1_20261010')
    import numpy as np,polars as pl
    import stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    from normalize_completed_stock_rank20_embedding_complete85_after182_v5_20261010 import RECIPES as recipes
    from run import FEATURE_FILE,feature_names,to_matrix
    original=Path(read(A/'actual_stock_rank20_embedding_complete85_after182_location_v1_20261010.json')['output'])/'pilot85.json'
    pilot=read(original);assert len(pilot['records'])==85
    records=pilot['records'];best=min(records,key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    assert best==pilot['best'];pins={**pilot['input_sha256'],str(original):sha(original)}
    for source in [Path(__file__),Path(stage.__file__),A/'predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py',A/'stock_rank20_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261010.json']:
        pins[str(source)]=sha(source)
    OUT.mkdir(exist_ok=False)
    normalized={**pilot,'status':'passed_normalized48_actual_TRAIN_official_records_selected_stage_and_full_inference_pending','input_sha256':pins,'normalization_source':str(original),'new_quality_scores_by_normalization':0}
    create(OUT/'pilot85.json',normalized)
    cfg=best['configuration']
    if cfg['model'] is None:
        create(OUT/'verification.json',{'status':'passed_selected_fully_qualified_anchor85_no_new_native_stage_claimed','best':best,'input_sha256':pins,'new_native_fits':0,'test_labels_read':False})
        create(A/'actual_stock_rank20_embedding85_selected_native14_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')});return
    bank=Path('E:/赛题五_本机临时')/recipes[cfg['recipe']][1];native=importlib.import_module(stage.BACKENDS[cfg['recipe']][0])
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/f'optimization_20261003_r{cfg["anchor_round"]}/selected_validation.npy'
    features=feature_names();keys=['ts_code','trade_date']
    decoder=importlib.import_module(stage.BACKENDS[cfg['recipe']][1])
    for p in [FEATURE_FILE,framepath,parentpath,Path(native.__file__),Path(decoder.__file__),
              A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py',A/'daily_cross_sectional_feature_encoder120_v1_20261010.py',A/'daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json',
              bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('info.json','model.joblib')]]:pins[str(p)]=sha(p)
    create(OUT/'selected_native14_frozen_before_saved_replays.json',{'best':best,'input_sha256':pins,'states':list(range(2020,2026)),
        'historical_cases':10,'calendar_training_X_cases':4,'cold_cases':14,'actual_future_X_read':False})
    frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy();parent=np.load(parentpath,mmap_mode='r')
    probes=[];prefit=[]
    for year in range(2020,2026):
        assert allowed()
        sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];idx=np.flatnonzero(np.isin(dates,days));panel=frame[idx]
        xf=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+features).sort('trade_date','ts_code').collect()
        assert xf.select(keys).equals(panel.select(keys)) and len(panel)==13950
        info=read(bank/str(year)/'info.json');component={'name':cfg['model'],'path':str(bank/str(year)/'model.joblib'),
            'sha256':info['model_sha256'],'training_info':info,'configuration':native.CONFIG}
        sourceparent=np.asarray(parent[idx],dtype=np.float64);x=to_matrix(xf,features)
        for calendar in ((year,) if year<2025 else (2025,2026)):
            testdates=panel['trade_date'].to_numpy().copy()
            if year==2025:testdates=np.array([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)
            for sign in (1.,-1.):
                spec={**cfg,'sign':sign,'original_complete_parent_round':cfg['anchor_round'],'first2020_active':True,'position':'after_complete_qualified_parent'}
                ctx=SimpleNamespace(frame=panel.with_columns(pl.Series('trade_date',testdates)),dates=testdates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                    _BF16_feature_names=features,_BF16_raw_features=x,_whole_graph={stage.GRAPH_KEY:spec})
                value,full=stage.after_parent(SimpleNamespace(sha=sha),ctx,sourceparent,spec,component)
                cold=SimpleNamespace(**vars(ctx));cold.frame=ctx.frame.head(4650)
                for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(ctx,field)[:4650])
                prefix,report=stage.after_parent(SimpleNamespace(sha=sha),cold,sourceparent[:4650],spec,component)
                assert np.array_equal(prefix.view('u8'),value[:4650].view('u8'))
                row={'model_year':year,'calendar_year':calendar,'historical_source_year':sourceyear,'sign':sign,'full':full,'cold':report,
                    'whole_day_prefix_bits_exact':True,'actual_future_X_read':False};create(OUT/f'native{len(probes):02d}.json',row);probes.append(row)
                print(f'Actual selected protected-tail native {len(probes)}/14, model{year}, calendar{calendar}',flush=True)
            bad=SimpleNamespace(**vars(ctx));bad.dates=np.full(len(sourceparent),info['training_meta']['cutoff_exclusive'])
            try:stage.after_parent(SimpleNamespace(sha=sha),bad,sourceparent,spec,component)
            except AssertionError:prefit.append({'model_year':year,'calendar_year':calendar,'prefit_rejected_before_inference':True})
            else:raise AssertionError('pre-fit selected tail calendar accepted')
    assert len(probes)==14 and len(prefit)==7
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_selected_protected_tail_six_states14_native_and14_cold_and7_prefit_rejections',
        'at_local':datetime.now().isoformat(),'input_sha256':pins,'best':best,'records':probes,'prefit_rejections':prefit,
        'actual_saved_states':6,'actual_historical_cases':10,'actual_calendar_cases':4,'actual_cold_cases':14,
        'actual_future_X_read':False,'test_labels_read':False,'new_native_fits':0,'new_quality_scores':0})
    create(A/'actual_stock_rank20_embedding85_selected_native14_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
