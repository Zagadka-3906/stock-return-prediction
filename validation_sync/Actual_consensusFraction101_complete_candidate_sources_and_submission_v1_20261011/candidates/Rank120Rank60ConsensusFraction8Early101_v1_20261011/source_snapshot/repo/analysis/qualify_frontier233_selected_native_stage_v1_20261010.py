"""Qualify the actual completed233 winner without reading future X or fitting new models."""
from pathlib import Path
from types import SimpleNamespace
import sys,time,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/frontier233_selected_native_stage_v1_20261010')

def main():
    assert allowed();closed('actual_frontier233_after169_and170_normalization_queue_v1_20261010')
    import numpy as np,polars as pl
    import frontier233_after_complete_parent_native_stage_v1_20261010 as stage
    from cross120_after_complete169_native_stage_v2_20261010 import BACKENDS
    from run import FEATURE_FILE,feature_names,to_matrix
    original=Path(read(A/'actual_frontier233_after169_and170_location_v1_20261010.json')['output'])/'pilot233.json';pilot=read(original)
    assert len(pilot['records'])==233
    best=min(pilot['records'],key=lambda row:(-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case']))
    assert best==pilot['best'];cfg=best['configuration'];pins={**pilot['input_sha256'],str(original):sha(original)}
    for p in [Path(__file__),Path(stage.__file__),A/'predict_frontier233_complete_parent_scheme_v1_20261010.py',A/'frontier233_parent_only_native_adapter_actual18_real_TRAIN_CPU_controls_v1_20261010.json',A/'frontier233_dual2020_actual9_TRAIN_native_and_cold_controls_v1_20261010.json',A/'frontier233_actual169_and170_parent_hook_CPU_controls_v1_20261010.json']:pins[str(p)]=sha(p)
    if cfg['stage_kind']=='dual120_rank_consensus':
        # Any new GPU bank must finish before selected-stage GPU work begins.
        closed('actual_cross120_recent252_return_own_controls_and_training_queue_v2_20261010')
    OUT.mkdir(exist_ok=False);create(OUT/'pilot233.json',{**pilot,'input_sha256':pins,'normalization_source':str(original)})
    if cfg['stage_kind']=='anchor':
        create(OUT/'verification.json',{'status':'passed_selected233_fully_qualified_anchor_no_new_native_stage_claimed','best':best,'input_sha256':pins,'new_native_fits':0,'test_labels_read':False})
        create(A/'actual_frontier233_selected_native_stage_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')});return
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/f'optimization_20261003_r{cfg["anchor_round"]}/selected_validation.npy'
    frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']);parent=np.load(parentpath,mmap_mode='r');dates=frame['trade_date'].to_numpy();features=feature_names()
    for p in [framepath,parentpath,FEATURE_FILE]:pins[str(p)]=sha(p)
    create(OUT/'selected_stage_frozen_before_actual_saved_replays.json',{'best':best,'input_sha256':pins,'historical_contexts':5,'calendar_contexts':2,'full_contexts':7,'full_and_cold_controls':14,'actual_future_X_read':False})
    probes=[];prefit=[]
    for year in range(2020,2026):
        assert allowed();sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];indices=np.flatnonzero(np.isin(dates,days));panel=frame[indices]
        source=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(['ts_code','trade_date',*features]).sort('trade_date','ts_code').collect()
        assert source.select(['ts_code','trade_date']).equals(panel.select(['ts_code','trade_date'])) and len(panel)==13950
        components=[]
        if cfg['stage_kind']=='dual120_rank_consensus':
            for leaf in best['native_bank_components']:
                bank=Path(leaf['bank']);info=read(bank/str(year)/'info.json');native=importlib.import_module(BACKENDS[leaf['recipe']][0])
                components.append({'name':leaf['name'],'recipe':leaf['recipe'],'path':str(bank/str(year)/'model.joblib'),'sha256':info['model_sha256'],'training_info':info,'configuration':native.CONFIG})
        for calendar in ((year,) if year<2025 else (2025,2026)):
            current=panel
            if year==2025:current=panel.with_columns(pl.Series('trade_date',np.array([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)))
            # Dual has signed diagnostics; a budget is tested with two independent prefix lengths.
            variants=[('sign',sign) for sign in (1.,-1.)] if components else [('prefix',n) for n in (4650,9300)]
            for variation,setting in variants:
                spec={**cfg,'position':'after_complete_qualified_parent'}
                if variation=='sign':spec['sign']=setting
                ctx=SimpleNamespace(frame=current,dates=current['trade_date'].to_numpy(),flags=current['flag_limit_up'].to_numpy(),valid=current['price_valid'].to_numpy(),
                    _BF16_feature_names=features,_BF16_raw_features=to_matrix(source,features),_whole_graph={stage.GRAPH_KEY:spec})
                value,full=stage.after_parent(SimpleNamespace(sha=sha),ctx,np.asarray(parent[indices],dtype=np.float64),spec,components)
                n=4650 if variation=='sign' else setting;cold=SimpleNamespace(**vars(ctx));cold.frame=current.head(n)
                for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(ctx,field)[:n])
                prefix,report=stage.after_parent(SimpleNamespace(sha=sha),cold,np.asarray(parent[indices][:n],dtype=np.float64),spec,components)
                assert np.array_equal(value[:n].view('u8'),prefix.view('u8'))
                row={'model_year':year if components else None,'historical_source_year':sourceyear,'calendar_year':calendar,'variation':variation,'setting':setting,'full':full,'cold':report,'cold_prefix_bits_exact':True,'actual_future_X_read':False}
                create(OUT/f'native{len(probes):02d}.json',row);probes.append(row)
            if components:
                cutoff=min(component['training_info']['training_meta']['cutoff_exclusive'] for component in components)
                bad=SimpleNamespace(**vars(ctx));bad.dates=np.array([cutoff,cutoff+1,cutoff+2]).repeat(4650);bad.frame=current.with_columns(pl.Series('trade_date',bad.dates))
                try:stage.after_parent(SimpleNamespace(sha=sha),bad,np.asarray(parent[indices],dtype=np.float64),spec,components)
                except AssertionError:prefit.append({'model_year':year,'calendar_year':calendar,'prefit_rejected_before_inference':True})
                else:raise AssertionError('Pre-fit dual model calendar accepted')
    assert len(probes)==14 and len(prefit)==(7 if cfg['stage_kind']=='dual120_rank_consensus' else 0)
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_selected233_stage14_native_or_pure_postprocessor_and14_cold_contexts','input_sha256':pins,'best':best,'records':probes,'prefit_rejections':prefit,
        'actual_added_stage_saved_states':12 if cfg['stage_kind']=='dual120_rank_consensus' else 0,'actual_historical_cases':10,'actual_calendar_cases':4,'actual_cold_cases':14,
        'postprocessing_only_parent_model_prefit_guards_remain_in_complete_parent_pipeline':not bool(prefit),'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    create(A/'actual_frontier233_selected_native_stage_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
