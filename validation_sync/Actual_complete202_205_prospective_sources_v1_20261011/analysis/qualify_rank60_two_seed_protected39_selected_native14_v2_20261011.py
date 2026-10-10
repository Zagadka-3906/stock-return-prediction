"""Qualify the actual88 winner with both signs, six paired states, cold replays and prefit refusals."""
from pathlib import Path
from types import SimpleNamespace
import sys,os,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/rank60_two_seed_protected39_selected_native14_v1_20261011')
for k in ('TMP','TEMP','TMPDIR','TORCH_HOME','TORCHINDUCTOR_CACHE_DIR','TRITON_CACHE_DIR','CUDA_CACHE_PATH'):os.environ[k]=str(OUT/'tmp'/k)
os.environ['CUDA_CACHE_DISABLE']='1'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from normalize_completed_rank60_two_seed_protected39_after204_v2_20261011 import best_key

def main():
    assert allowed();closed('actual_rank60_two_seed_protected39_after204_normalization_v1_20261011')
    pointer=A/'actual_rank60_two_seed_protected_complete39_after204_location_v1_20261011.json'
    original=Path(read(pointer)['output'])/'pilot39.json';pilot=read(original)
    assert len(pilot['records'])==39 and (pilot['actual_nonidentity_full_controls'],pilot['actual_nonidentity_prefix_controls'])==(36,108)
    best=min(pilot['records'],key=best_key);assert best==pilot['best'];cfg=best['configuration']
    pins={**pilot['input_sha256'],str(original):sha(original),str(pointer):sha(pointer),str(Path(__file__)):sha(__file__)}
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot39.json',{**pilot,'input_sha256':pins,'normalization_source':str(original)})
    if cfg['model'] is None:
        assert read(A/f"optimization_20261003_r{cfg['anchor_round']}/full_registration_execution.json")['status']=='passed'
        create(OUT/'verification.json',{'status':'passed_selected_fully_qualified_anchor39_no_new_native_stage_claimed',
            'best':best,'input_sha256':pins,'actual_native_cases':0,'actual_cold_cases':0,'new_native_fits':0,'new_quality_scores':0,
            'actual_future_X_read':False,'test_labels_read':False,'full205_registration_pending':True})
    else:
        closed('StockRank60EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
        import psutil,time
        while psutil.virtual_memory().available<12*2**30:assert allowed();time.sleep(15)
        import numpy as np,polars as pl
        from run import FEATURE_FILE,feature_names,to_matrix
        stage=importlib.import_module(best['native_stage_module'])
        assert cfg['anchor_round']==183 and len(best['native_bank_components'])==2
        banks=[Path(m['bank']) for m in best['native_bank_components']]
        framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r183/selected_validation.npy'
        features=feature_names();keys=['ts_code','trade_date']
        sources=[Path(stage.__file__),FEATURE_FILE,framepath,parentpath,*[A/(m+'.py') for m in stage.BACKENDS[stage.RECIPE]],
            A/'rank20_two_seed_raw_signal_v1_20261010.py',A/'rank60_two_seed_after183_protected37_predeclared_sources_admission_v1_20261011.json',
            A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'protected_upper_tail_rank_permutation_v1_20261010.py',
            A/'protected_official_top_rank_permutation_v2_20261010.py',A/'daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json',
            *[b/str(y)/n for b in banks for y in range(2020,2026) for n in ('info.json','model.joblib')]]
        pins.update({str(p):sha(p) for p in sources})
        create(OUT/'selected_native14_frozen_before_saved_replays.json',{'best':best,'input_sha256':pins,'expected_native':14,'expected_cold':14,
            'expected_prefit_refusals':7,'physical_saved_states':12,'actual_future_X_read':False,'test_labels_read':False})
        frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy();parent=np.load(parentpath,mmap_mode='r')
        records=[];refusals=[]
        for year in range(2020,2026):
            assert allowed()
            sourceyear=min(year,2024);days=np.unique(dates[dates//10000==sourceyear])[:3];idx=np.flatnonzero(np.isin(dates,days));panel=frame[idx]
            xf=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+features).sort('trade_date','ts_code').collect()
            assert xf.select(keys).equals(panel.select(keys)) and len(panel)==13950
            x=to_matrix(xf,features);members=[]
            for i,bank in enumerate(banks):
                info=read(bank/str(year)/'info.json')
                members.append({'name':best['native_bank_components'][i]['name'],'path':str(bank/str(year)/'model.joblib'),
                    'sha256':info['model_sha256'],'training_info':info,'configuration':info['configuration']})
            component={'horizon_components':members}
            for calendar in ((year,) if year<2025 else (2025,2026)):
                testdates=panel['trade_date'].to_numpy().copy()
                if year==2025:testdates=np.asarray([calendar*10000+102,calendar*10000+105,calendar*10000+106]).repeat(4650)
                for sign in (-1.,1.):
                    assert allowed()
                    spec={**cfg,'sign':sign,'recipe':stage.RECIPE,'original_complete_parent_round':183,'first2020_active':True,'position':'after_complete_qualified_parent'}
                    ctx=SimpleNamespace(frame=panel.with_columns(pl.Series('trade_date',testdates)),dates=testdates,
                        flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                        _BF16_raw_features=x,_BF16_feature_names=features,_whole_graph={stage.GRAPH_KEY:spec})
                    value,full=stage.after_parent(SimpleNamespace(sha=sha),ctx,np.asarray(parent[idx]),spec,component)
                    cold=SimpleNamespace(**vars(ctx));cold.frame=ctx.frame.head(4650)
                    for field in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,field,getattr(ctx,field)[:4650])
                    prefix,coldreport=stage.after_parent(SimpleNamespace(sha=sha),cold,np.asarray(parent[idx])[:4650],spec,component)
                    assert np.array_equal(prefix.view('u8'),value[:4650].view('u8'))
                    row={'year':year,'calendar':calendar,'configuration':spec,'full':full,'cold':coldreport,'native_independent_and_cold_bits_exact':True}
                    create(OUT/f'native{len(records):02d}.json',row);records.append(row)
                    print(f'Actual selected two-seed native {len(records)}/14; model{year} calendar{calendar}',flush=True)
                bad=SimpleNamespace(**vars(ctx));bad.dates=np.full(len(ctx.dates),members[0]['training_info']['training_meta']['cutoff_exclusive'])
                try:stage.after_parent(SimpleNamespace(sha=sha),bad,np.asarray(parent[idx]),spec,component)
                except AssertionError:refusals.append({'year':year,'calendar':calendar,'prefit_rejected':True})
                else:raise AssertionError('two-seed prefit accepted')
        assert len(records)==14 and len(refusals)==7
        for p,d in pins.items():assert sha(p)==d,p
        create(OUT/'verification.json',{'status':'passed_selected_rank60_two_seed_protected39_six_pairs14_native14_cold7_prefit_refusals',
            'input_sha256':pins,'best':best,'records':records,'prefit_rejections':refusals,'actual_saved_states':12,
            'actual_native_cases':14,'actual_cold_cases':14,'new_quality_scores':0,'new_native_fits':0,
            'actual_future_X_read':False,'test_labels_read':False,'full205_candidate_and_registration_pending':True})
    create(A/'actual_rank60_two_seed_protected39_selected_native14_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
