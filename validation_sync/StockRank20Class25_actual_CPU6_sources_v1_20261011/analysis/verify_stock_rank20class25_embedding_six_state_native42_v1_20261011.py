"""42 real TRAIN saved-state cases,42 cold replays and7 strict prefit refusals."""
from pathlib import Path
from types import SimpleNamespace
import sys,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_rank20class25_embedding_six_state_native42_v1_20261011')
for k in ('TMP','TEMP','TMPDIR','TORCH_HOME','TORCHINDUCTOR_CACHE_DIR','TRITON_CACHE_DIR','CUDA_CACHE_PATH'):os.environ[k]=str(OUT/'tmp'/k)
os.environ['CUDA_CACHE_DISABLE']='1'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('StockRank20Class25EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
    import numpy as np,polars as pl
    import stock_rank20class25_embedding_after_complete_qualified_parent_native_stage_v1_20261011 as stage
    import stock_rank20class25_embedding_small512_BF16_native_v1_20261011 as native
    from run import FEATURE_FILE,feature_names,to_matrix
    bank=Path(read(A/'actual_stock_rank20class25_embedding_small512_bank6_location_v1_20261011.json')['output'])
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r169/selected_validation.npy'
    features=feature_names();keys=['ts_code','trade_date']
    pins={str(p):sha(p) for p in [Path(__file__),Path(stage.__file__),Path(native.__file__),A/'stock_identity_embedding_network_v1_20261010.py',A/'stock_rank20class25_embedding_saved_tensor_decoder_v1_20261011.py',A/'stock_rank20class25_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json',framepath,parentpath,bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('model.joblib','info.json')]]}
    assert not (OUT/'frozen_before_native42.json').exists();OUT.mkdir(parents=True,exist_ok=True)
    create(OUT/'frozen_before_native42.json',{'input_sha256':pins,'actual_reference_parent_round':169,'actual_quality_parent172_pending':True,'same_stock_grid':'4650 canonical rows/day','expected_native':42,'expected_cold':42,'expected_prefit_rejections':7,'test_labels_read':False})
    frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy();parent=np.load(parentpath,mmap_mode='r');records=[];refusals=[]
    for year in range(2020,2026):
        assert allowed()
        sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];idx=np.flatnonzero(np.isin(dates,days));panel=frame[idx]
        xf=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+features).sort('trade_date','ts_code').collect();assert xf.select(keys).equals(panel.select(keys))
        x=to_matrix(xf,features);info=read(bank/str(year)/'info.json')
        component={'name':'rank_MLP512_StockRank20Class25Embedding16_Cross120Recent252Rank20Class25Mean_seed09_e64','path':str(bank/str(year)/'model.joblib'),'sha256':info['model_sha256'],'training_info':info,'configuration':native.CONFIG}
        for calendar in ((year,) if year<2025 else (2025,2026)):
            testdates=panel['trade_date'].to_numpy().copy()
            if year==2025:testdates=np.asarray([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)
            for codec in ('CDF','valid_pool_protection_v1','official_Top_protection_v2'):
                for sign in (1.,-1.):
                    assert allowed()
                    spec={'recipe':'stock_rank20class25_embedding16_cross120_rank20mean_recent252_small512_BF16_e64','codec':codec,'stage_kind':'stock_rank20class25_embedding_rank20mean_direct','role':'nonflag_valid','weight':.016,'protect_fraction':None if codec=='CDF' else .15,'sign':sign,'original_complete_parent_round':169,'first2020_active':True,'position':'after_complete_qualified_parent','decay':None}
                    ctx=SimpleNamespace(frame=panel.with_columns(pl.Series('trade_date',testdates)),dates=testdates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),_BF16_raw_features=x,_BF16_feature_names=features,_whole_graph={stage.GRAPH_KEY:spec})
                    value,report=stage.after_parent(SimpleNamespace(sha=sha),ctx,np.asarray(parent[idx]),spec,component)
                    cold=SimpleNamespace(**vars(ctx));cold.frame=ctx.frame.head(4650)
                    for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(ctx,field)[:4650])
                    prefix,coldreport=stage.after_parent(SimpleNamespace(sha=sha),cold,np.asarray(parent[idx])[:4650],spec,component)
                    assert np.array_equal(prefix.view('u8'),value[:4650].view('u8'))
                    row={'year':year,'calendar':calendar,'codec':codec,'sign':sign,'full':report,'cold':coldreport,'native_independent_and_cold_bits_exact':True};create(OUT/f'native{len(records):02d}.json',row);records.append(row)
                    print(f'Actual stock embedding saved stage {len(records)}/42; model{year} calendar{calendar}',flush=True)
            bad=SimpleNamespace(**vars(ctx));bad.dates=np.full(len(ctx.dates),info['training_meta']['cutoff_exclusive'])
            try:stage.after_parent(SimpleNamespace(sha=sha),bad,np.asarray(parent[idx]),spec,component)
            except AssertionError:refusals.append({'year':year,'calendar':calendar,'prefit_rejected':True})
            else:raise AssertionError('stock_embedding_prefit_accepted')
    assert len(records)==42 and len(refusals)==7
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual_six_stock_embedding_saved_states42_native42_cold7_prefit_refusals','input_sha256':pins,'records':records,'prefit_rejections':refusals,'actual_saved_states':6,'actual_native_cases':42,'actual_cold_cases':42,'test_labels_read':False,'actual_complete172_selected_stage_and_full_future_replays_pending':True,'new_quality_scores':0})
    create(A/'actual_stock_rank20class25_embedding_six_state_native42_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
