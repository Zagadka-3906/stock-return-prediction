"""Real TRAIN feature probes of three mixtures, two codecs, two signs and three calendars."""
from pathlib import Path
from types import SimpleNamespace
import sys,os,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_dual_embedding_actual36_native_and_cold_v1_20261010')
for key in ('TMP','TEMP','TMPDIR','TORCH_HOME','TORCHINDUCTOR_CACHE_DIR','TRITON_CACHE_DIR','CUDA_CACHE_PATH'):os.environ[key]=str(OUT/'tmp'/key)
os.environ['CUDA_CACHE_DISABLE']='1'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def yield_priority():
    assert allowed()
    if Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():closed('StockEmbedding173_selected_candidate_sealing_v1_20261010')
def main():
    assert allowed();closed('actual_stock_rank_embedding_six_state_native42_v1_20261010');closed('actual_stock_embedding_six_state_native42_v2_20261010')
    yield_priority()
    import numpy as np,polars as pl
    import stock_dual_embedding_after_complete_parent_native_stage_v1_20261010 as stage
    from run import FEATURE_FILE,feature_names,to_matrix
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r169/selected_validation.npy'
    banks=[Path('E:/赛题五_本机临时/stock_embedding_small512_BF16_bank6_v1_20261010'),Path('E:/赛题五_本机临时/stock_rank_embedding_small512_BF16_bank6_v1_20261010')]
    recipes=(stage.RETURN_RECIPE,stage.RANK_RECIPE)
    paths=[Path(__file__),Path(stage.__file__),A/'stock_dual_embedding_five_parent_hooks_CPU_controls_v1_20261010.json',FEATURE_FILE,framepath,parentpath,A/'dual_target_daily_rank_consensus_v1_20261010.py',A/'stock_identity_embedding_network_v1_20261010.py']
    for bank,recipe in zip(banks,recipes):
        assert read(bank/'verification.json')['actual_native_fits']==6
        paths += [bank/'verification.json',*[bank/str(y)/n for y in (2020,2025) for n in ('info.json','model.joblib')]]
        paths += [A/(m+'.py') for m in stage.BACKENDS[recipe]]
    pins={str(p):sha(p) for p in paths}
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'frozen_before36.json').exists()
    create(OUT/'frozen_before36.json',{'input_sha256':pins,'expected_native':36,'expected_cold':36,'expected_prefit_refusals':3,'actual_reference_parent_round':169,'quality_parent173_pending':True,'actual_future_X_read':False})
    features=feature_names();keys=['ts_code','trade_date'];frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy();parent=np.load(parentpath,mmap_mode='r');records=[];refusals=[]
    for year in (2020,2025):
        sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];idx=np.flatnonzero(np.isin(dates,days));panel=frame[idx]
        xf=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+features).sort('trade_date','ts_code').collect();assert xf.select(keys).equals(panel.select(keys))
        x=to_matrix(xf,features);components=[]
        for bank,recipe in zip(banks,recipes):
            native=importlib.import_module(stage.BACKENDS[recipe][0]);info=read(bank/str(year)/'info.json')
            components.append({'name':bank.name,'path':str(bank/str(year)/'model.joblib'),'sha256':info['model_sha256'],'training_info':info,'configuration':native.CONFIG})
        for calendar in ((2020,) if year==2020 else (2025,2026)):
            testdates=panel['trade_date'].to_numpy().copy()
            if year==2025:testdates=np.array([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)
            for mixture in (.25,.5,.75):
                for codec in stage.CODECS:
                    for sign in (1.,-1.):
                        yield_priority()
                        spec={'stage_kind':'stock_return_rank_embedding_consensus','anchor_round':169,'position':'after_complete_qualified_parent','first2020_active':True,'mean_weight':mixture,'codec':codec,'weight':.016,'protect_fraction':.15,'sign':sign}
                        ctx=SimpleNamespace(frame=panel.with_columns(pl.Series('trade_date',testdates)),dates=testdates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),_BF16_raw_features=x,_BF16_feature_names=features,_whole_graph={stage.GRAPH_KEY:spec})
                        value,report=stage.after_parent(SimpleNamespace(sha=sha),ctx,np.asarray(parent[idx]),spec,components)
                        cold=SimpleNamespace(**vars(ctx));cold.frame=ctx.frame.head(4650)
                        for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(ctx,field)[:4650])
                        prefix,coldreport=stage.after_parent(SimpleNamespace(sha=sha),cold,np.asarray(parent[idx])[:4650],spec,components)
                        assert np.array_equal(value[:4650].view('u8'),prefix.view('u8'))
                        row={'model_year':year,'calendar_year':calendar,'spec':spec,'full':report,'cold':coldreport,'cold_bits_exact':True};create(OUT/f'native{len(records):02d}.json',row);records.append(row)
                        print(f'Actual complementary embedding {len(records)}/36 native+cold',flush=True)
            bad=SimpleNamespace(**vars(ctx));bad.dates=np.full(len(ctx.dates),components[0]['training_info']['training_meta']['cutoff_exclusive'])
            try:stage.after_parent(SimpleNamespace(sha=sha),bad,np.asarray(parent[idx]),spec,components)
            except AssertionError:refusals.append({'year':year,'calendar':calendar,'prefit_refused':True})
            else:raise AssertionError('Dual prefit accepted')
    assert len(records)==36 and len(refusals)==3
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual_two_year_four_saved_states_three_calendars36_native36_cold3_prefit_refusals','records':records,'prefit_rejections':refusals,'input_sha256':pins,'actual_native_cases':36,'actual_cold_cases':36,'actual_saved_states':4,'does_not_claim_all12_saved_state_selected_stage_verification':True,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_stock_dual_embedding_actual36_native_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
