"""Real two-seed TRAIN stages: six paired annual states, native84/cold84 and seven prefit refusals."""
from pathlib import Path
from types import SimpleNamespace
import sys,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/rank20_two_seed_six_pair_states_native84_v1_20261010')
for k in ('TMP','TEMP','TMPDIR','TORCH_HOME','TORCHINDUCTOR_CACHE_DIR','TRITON_CACHE_DIR','CUDA_CACHE_PATH'):os.environ[k]=str(OUT/'tmp'/k)
os.environ['CUDA_CACHE_DISABLE']='1'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010')
    import numpy as np,polars as pl
    import rank20_two_seed_after_qualified_parent_native_stage_v1_20261010 as stage
    from run import FEATURE_FILE,feature_names,to_matrix
    banks=[Path(f'E:/赛题五_本机临时/{name}_small512_BF16_bank6_v1_20261010') for name in ('stock_rank20_embedding','stock_rank20seed10_embedding')]
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r175/selected_validation.npy'
    features=feature_names();keys=['ts_code','trade_date']
    sources=[Path(__file__),Path(stage.__file__),A/'rank20_two_seed_raw_signal_v1_20261010.py',A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json',framepath,parentpath,
        *[A/(m+'.py') for m in stage.BACKENDS[stage.RECIPE]],
        *[bank/'verification.json' for bank in banks],
        *[bank/str(y)/n for bank in banks for y in range(2020,2026) for n in ('model.joblib','info.json')]]
    pins={str(p):sha(p) for p in sources}
    assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_native84.json',{'input_sha256':pins,'actual_reference_parent_round':175,'expected_native':84,'expected_cold':84,'expected_prefit_refusals':7,'physical_saved_states':12,'test_labels_read':False})
    frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy();parent=np.load(parentpath,mmap_mode='r');records=[];refusals=[]
    for year in range(2020,2026):
        assert allowed()
        sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];idx=np.flatnonzero(np.isin(dates,days));panel=frame[idx]
        xf=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+features).sort('trade_date','ts_code').collect();assert xf.select(keys).equals(panel.select(keys))
        x=to_matrix(xf,features);members=[]
        for i,bank in enumerate(banks):
            info=read(bank/str(year)/'info.json')
            members.append({'name':f'Rank20_ID16_Cross120_seed{(20261009,20261010)[i]}_e64','path':str(bank/str(year)/'model.joblib'),'sha256':info['model_sha256'],'training_info':info,'configuration':info['configuration']})
        component={'seed_components':members}
        for calendar in ((year,) if year<2025 else (2025,2026)):
            testdates=panel['trade_date'].to_numpy().copy()
            if year==2025:testdates=np.asarray([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)
            for blend in (.25,.5,.75):
                for role in ('nonflag_valid','all_valid'):
                    for sign in (-1.,1.):
                        assert allowed()
                        spec={'recipe':stage.RECIPE,'codec':'CDF','stage_kind':'rank20_two_seed_raw_average','role':role,'weight':.0003125,'protect_fraction':None,'sign':sign,'original_complete_parent_round':175,'first2020_active':True,'position':'after_complete_qualified_parent','decay':None,'second_seed_weight':blend}
                        ctx=SimpleNamespace(frame=panel.with_columns(pl.Series('trade_date',testdates)),dates=testdates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),_BF16_raw_features=x,_BF16_feature_names=features,_whole_graph={stage.GRAPH_KEY:spec})
                        value,report=stage.after_parent(SimpleNamespace(sha=sha),ctx,np.asarray(parent[idx]),spec,component)
                        cold=SimpleNamespace(**vars(ctx));cold.frame=ctx.frame.head(4650)
                        for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(ctx,field)[:4650])
                        prefix,coldreport=stage.after_parent(SimpleNamespace(sha=sha),cold,np.asarray(parent[idx])[:4650],spec,component)
                        assert np.array_equal(prefix.view('u8'),value[:4650].view('u8'))
                        row={'year':year,'calendar':calendar,'configuration':spec,'full':report,'cold':coldreport,'native_independent_and_cold_bits_exact':True};create(OUT/f'native{len(records):02d}.json',row);records.append(row)
                        print(f'Actual two-seed native stage {len(records)}/84; model{year} calendar{calendar}',flush=True)
            bad=SimpleNamespace(**vars(ctx));bad.dates=np.full(len(ctx.dates),members[0]['training_info']['training_meta']['cutoff_exclusive'])
            try:stage.after_parent(SimpleNamespace(sha=sha),bad,np.asarray(parent[idx]),spec,component)
            except AssertionError:refusals.append({'year':year,'calendar':calendar,'prefit_rejected':True})
            else:raise AssertionError('two-seed prefit accepted')
    assert len(records)==84 and len(refusals)==7
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual12_physical_models_six_pairs_native84_cold84_and7_prefit_refusals','input_sha256':pins,'records':records,'prefit_rejections':refusals,'actual_saved_states':12,'actual_native_cases':84,'actual_cold_cases':84,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    create(A/'actual_rank20_two_seed_native84_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
