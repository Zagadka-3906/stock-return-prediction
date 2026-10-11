"""Actual2020 saved-state probes for the new single-leaf direct and causal-smoothed stage."""
from pathlib import Path
from types import SimpleNamespace
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
    assert allowed();closed('actual_cross120_recent252_return_own_controls_and_training_queue_v2_20261010')
    # These probes occupy the idle gap before the long193 screen can release selected233 GPU work.
    scoreout=Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010')
    assert not (scoreout/'verification.json').exists(),'Do not overlap the selected233 GPU window'
    import numpy as np,polars as pl
    import frontier133_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    from normalize_completed_frontier133_after171_v1_20261010 import RECIPES
    from run import FEATURE_FILE,feature_names,to_matrix
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']).head(13950)
    dates=frame['trade_date'].to_numpy();features=feature_names();source=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(np.unique(dates))).select(['ts_code','trade_date',*features]).sort('trade_date','ts_code').collect()
    assert source.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date'])) and len(frame)==13950
    x=to_matrix(source,features);parents={n:np.load(A/f'optimization_20261003_r{n}/selected_validation.npy',mmap_mode='r')[:13950] for n in (169,170)}
    paths=[Path(__file__),Path(stage.__file__),A/'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py',A/'frontier133_actual_three_nested_parent_hooks_CPU_controls_v1_20261010.json',framepath,FEATURE_FILE,*[A/f'optimization_20261003_r{n}/selected_validation.npy' for n in (169,170)]]
    rows=[];prefit=[]
    for recipe,(name,bankname) in RECIPES.items():
        bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2020/info.json');native=importlib.import_module(stage.BACKENDS[recipe][0]);component={'name':name,'recipe':recipe,'path':str(bank/'2020/model.joblib'),'sha256':info['model_sha256'],'training_info':info,'configuration':native.CONFIG}
        paths += [bank/'2020/model.joblib',bank/'2020/info.json']
        smoothing=recipe!='cross120recent252returnhuber050';base=170 if smoothing else 169
        for decay in ((.25,.5,.75) if smoothing else (None,)):
            for codec in stage.CODECS:
                for sign in (1.,-1.):
                    assert allowed();assert not (scoreout/'verification.json').exists(),'Selected233 GPU interval has opened'
                    spec={'stage_kind':'cross120_causal_smoothing' if smoothing else 'cross120_return1d_direct','recipe':recipe,'model':name,'codec':codec,'weight':.016,'protect_fraction':.15 if codec!='CDF' else None,'role':'nonflag_valid','sign':sign,'decay':decay,'original_complete_parent_round':base,'position':'after_complete_qualified_parent','first2020_active':True}
                    ctx=SimpleNamespace(frame=frame,dates=dates,flags=frame['flag_limit_up'].to_numpy(),valid=frame['price_valid'].to_numpy(),_BF16_feature_names=features,_BF16_raw_features=x,_whole_graph={stage.GRAPH_KEY:spec})
                    value,full=stage.after_parent(SimpleNamespace(sha=sha),ctx,np.asarray(parents[base],dtype=np.float64),spec,component);cold_reports=[]
                    for n in (4650,9300):
                        cold=SimpleNamespace(**vars(ctx));cold.frame=frame.head(n)
                        for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(ctx,field)[:n])
                        prefix,report=stage.after_parent(SimpleNamespace(sha=sha),cold,np.asarray(parents[base][:n],dtype=np.float64),spec,component);assert np.array_equal(prefix.view('u8'),value[:n].view('u8'));cold_reports.append(report)
                    rows.append({'configuration':spec,'actual_model_year':2020,'actual_TRAIN_rows':13950,'full':full,'cold':cold_reports,'cold4650_and9300_bits_exact':True})
        bad=SimpleNamespace(**vars(ctx));bad.dates=np.full(len(dates),info['training_meta']['cutoff_exclusive']);bad.frame=frame.with_columns(pl.Series('trade_date',bad.dates))
        original=stage.feature_matrix;called=[]
        def must_not_encode(*args):called.append(True);raise RuntimeError('Pre-fit guard failed before feature encoding')
        stage.feature_matrix=must_not_encode
        try:
            try:stage.after_parent(SimpleNamespace(sha=sha),bad,np.asarray(parents[base],dtype=np.float64),spec,component)
            except AssertionError:assert not called;prefit.append({'recipe':recipe,'prefit_rejected_before_feature_encoding':True})
            else:raise AssertionError('Pre-fit model accepted')
        finally:stage.feature_matrix=original
    assert len(rows)==42 and len(prefit)==3
    create(A/'frontier133_actual42_TRAIN_native_and84_cold_controls_v1_20261010.json',{'status':'passed_actual2020_three_own120_saved_states42_native_independent_stage_and84_cold_controls','input_sha256':{str(p):sha(p) for p in paths},'records':rows,'prefit_rejections':prefit,'actual_saved_model_states':3,'all_six_annual_selected_stage_qualification_still_required':True,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'actual_native_probes':42,'actual_cold_probes':84,'actual_saved_2020_states':3,'future_X_read':False},flush=True)

if __name__=='__main__':main()
