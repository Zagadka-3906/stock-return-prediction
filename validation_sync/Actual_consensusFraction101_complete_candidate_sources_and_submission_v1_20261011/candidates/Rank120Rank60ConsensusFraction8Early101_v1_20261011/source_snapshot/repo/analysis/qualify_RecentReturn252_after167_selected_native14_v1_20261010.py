"""Normalize both completed protected screens and actual anchors, then qualify the selected saved stage."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime,timezone,timedelta
import sys,time,hashlib,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/protected_RecentReturn252_selected_native14_v1_20261010')
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
    # The existing sequential controller must hold future162 GPU dispatch until this service closes.
    for name in ('actual_RecentReturn252_after167_high_impact65_screen_v1_20261010','actual_RecentReturn252_after167_65_completion_main_v19_20261010'):closed(name)
    closed('actual_recent252_return_own_controls_and_training_queue_v2_20261010')
    import numpy as np,polars as pl
    import protected_RecentReturn252_after167_native_stage_v1_20261010 as stage
    from run import FEATURE_FILE,feature_names,to_matrix
    recipes={'recent252returnhuber050':('rank_MLP2048_BF16_RecentReturn252Huber050_seed09_e64','neural_BF16_medium2048_recent252returnhuber050_seed09_e64_bank6_v1_20261009')}
    records=[];pins={};models={n:read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json')['models'] for n in (166,167)}
    for n in (166,167):
        f=A/f'optimization_20261003_r{n}';assert read(f/'full_registration_execution.json')['status']=='passed'
        pred=np.load(f/'selected_validation.npy',mmap_mode='r');metrics=read(f/'calibrated_csv_official.json')['metrics']
        sel=read(f/'selection.json')['winner'];cache=sel['official_score_cache'];capsule=Path(cache['official_metrics_source']);assert read(capsule)['metrics']==metrics
        cfg={'anchor_round':n,'model':None,'recipe':None,'codec':None,'role':None,'weight':0.,'sign':1.,'protect_fraction':None,'universe':None}
        records.append({'case':len(records),'configuration':cfg,'metrics':metrics,'connected_final_score':metrics['final_score'],
            'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(pred)).cast('B')).hexdigest(),
            'expected_unique_native_models':len({m['sha256'] for m in models[n].values()}),'official_score_cache':cache,
            'official_metric_capsule_sha256':sha(capsule),'qualified_anchor_all8_metrics_exact':True,'ordered_native_components':[],
            'actual_return_mapping':sel.get('causal_return_mapping',{}),'test_labels_read':False})
        for p in (capsule,f/'selection.json',f/'selected_validation.npy',f/'full_registration_execution.json',A/f'github_validation_sync_main_20261005/round{n}_receipt.json'):pins[str(p)]=sha(p)
    for family in ('RecentReturn252_after167_high_impact65_screen_v1_20261010',):
        folder=Path('E:/赛题五_本机临时')/family;proof=read(folder/'verification.json')
        assert len(proof['records'])==65 and proof['actual_nonidentity_full_controls']==64 and proof['actual_nonidentity_prefix_controls']==192
        pins.update(proof['input_sha256']);pins[str(folder/'verification.json')]=sha(folder/'verification.json')
        for source in proof['records']:
            cfg=dict(source['configuration']);cfg.update(recipe=None if source['case']==0 else 'recent252returnhuber050',codec=None if source['case']==0 else source['configuration']['kind'],anchor_round=167,universe='all_current_raw_forecasts')
            if cfg['recipe'] is None:
                cfg.update(model=None,role=None,codec=None,universe=None);physical=len({m['sha256'] for m in models[167].values()})
            else:
                model,bankname=recipes[cfg['recipe']];cfg['model']=model
                info=read(Path('E:/赛题五_本机临时')/bankname/'2025/info.json')
                physical=len({m['sha256'] for m in models[167].values()}|{info['model_sha256']})
            path=folder/f"case{source['case']:03d}_official.json";control=folder/f"case{source['case']:03d}_controls.json"
            assert sha(control)==source['control_sha256'];capsule=Path(source['official_score_cache']['official_metrics_source']);assert sha(capsule)==source['official_metric_capsule_sha256']
            assert read(capsule)['metrics']==source['metrics']
            records.append({**source,'case':len(records),'configuration':cfg,'original_screen_record':str(path),
                'original_screen_case':source['case'],'prediction_numeric_bytes_sha256':source['prediction_numeric_sha256'],
                'expected_unique_native_models':physical,'qualified_anchor_all8_metrics_exact':cfg['model'] is None,
                'ordered_native_components':[] if cfg['model'] is None else [cfg['model']],
                'whole_complete_parent_branches_preserved_before_new_stage':cfg['model'] is not None,
                'invalid_and_declared_unselected_raw_bits_preserved':cfg['model'] is not None,
                'actual_cold80_260_975_bits_exact':cfg['model'] is not None,'first2020_active':cfg['model'] is not None})
            for p in (path,control,capsule):pins[str(p)]=sha(p)
    assert len(records)==67
    best=min(records,key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    model_sources=[Path(__file__),Path(stage.__file__),A/'RecentReturn252_after167_selected_native14_source_admission_v1_20261010.json',
        A/'predict_protected_RecentReturn252_after167_complete_scheme_v1_20261010.py',A/'protected_upper_tail_rank_permutation_v1_20261010.py',A/'protected_official_top_rank_permutation_v2_20261010.py']
    pins.update({str(p):sha(p) for p in model_sources})
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot67.json',{'status':'passed_normalized67_actual_complete_training_only_official_records','at_local':datetime.now().isoformat(),
        'records':records,'best':best,'input_sha256':pins,'actual_scheme_base_round':167,'actual_comparison_parent_round':167,
        'new_quality_scores_by_normalization':0,'expected_scored_records':67,'selected_native14_and_future_inference_pending':True,'test_labels_read':False})
    cfg=best['configuration']
    if cfg['model'] is None:
        create(OUT/'verification.json',{'status':'passed_selected_fully_qualified_anchor67_no_new_native_stage_claimed','best':best,'input_sha256':pins,'new_native_fits':0,'test_labels_read':False})
        create(A/'actual_protected_RecentReturn252_selected_native14_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')});return
    bank=Path('E:/赛题五_本机临时')/recipes[cfg['recipe']][1];native=importlib.import_module(stage.BACKENDS[cfg['recipe']][0])
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r167/selected_validation.npy'
    features=feature_names();keys=['ts_code','trade_date']
    decoder=importlib.import_module(stage.BACKENDS[cfg['recipe']][1])
    for p in [FEATURE_FILE,framepath,parentpath,Path(native.__file__),Path(decoder.__file__),
              A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
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
                spec={**cfg,'sign':sign,'original_complete_parent_round':167,'first2020_active':True,'position':'after_complete_qualified_parent'}
                ctx=SimpleNamespace(dates=testdates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                    _BF16_feature_names=features,_BF16_raw_features=x,_whole_graph={stage.GRAPH_KEY:spec})
                value,full=stage.after_parent(SimpleNamespace(sha=sha),ctx,sourceparent,spec,component)
                cold=SimpleNamespace(**vars(ctx))
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
    create(A/'actual_protected_RecentReturn252_selected_native14_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
