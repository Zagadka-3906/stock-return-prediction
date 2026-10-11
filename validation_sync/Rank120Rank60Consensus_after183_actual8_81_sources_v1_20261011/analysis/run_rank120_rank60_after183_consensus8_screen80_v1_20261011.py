"""Screen a genuinely new loss bank cumulatively, including tail-preserving interactions."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import sys,os,time,hashlib,gc,json
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
OUT=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensus8_screen80_v1_20261011')
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def write(path,value):
    t=path.with_name(path.name+f'.{os.getpid()}.tmp');t.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(t,path)

def cases():
    return [{'kind': 'anchor183', 'role': None, 'weight': 0.0, 'sign': 1.0, 'protect_fraction': None, 'disagreement_penalty': None}, {'kind': 'valid_pool_protection_v1', 'role': 'nonflag_valid', 'weight': 0.032, 'sign': 1.0, 'protect_fraction': 0.2, 'disagreement_penalty': 0.5}, {'kind': 'valid_pool_protection_v1', 'role': 'nonflag_valid', 'weight': 0.032, 'sign': 1.0, 'protect_fraction': 0.2, 'disagreement_penalty': 0.75}, {'kind': 'valid_pool_protection_v1', 'role': 'nonflag_valid', 'weight': 0.064, 'sign': 1.0, 'protect_fraction': 0.2, 'disagreement_penalty': 0.75}, {'kind': 'valid_pool_protection_v1', 'role': 'nonflag_valid', 'weight': 0.032, 'sign': 1.0, 'protect_fraction': 0.2, 'disagreement_penalty': 1.0}, {'kind': 'valid_pool_protection_v1', 'role': 'nonflag_valid', 'weight': 0.064, 'sign': 1.0, 'protect_fraction': 0.2, 'disagreement_penalty': 1.0}, {'kind': 'valid_pool_protection_v1', 'role': 'nonflag_valid', 'weight': 0.032, 'sign': 1.0, 'protect_fraction': 0.2, 'disagreement_penalty': 2.0}, {'kind': 'valid_pool_protection_v1', 'role': 'nonflag_valid', 'weight': 0.064, 'sign': 1.0, 'protect_fraction': 0.2, 'disagreement_penalty': 2.0}]



def main():
    assert allowed()
    closed('actual_rank120_rank60_after183_disagreement_CDFfine8_screen77_v1_20261011')
    closed('actual_completed_disagreement10_pointer_namespace_bridge72_v1_20261011')
    closed('actual_fraction38_completed_namespace_bridge_v1_20261011')
    closed('actual_rank120_rank60_after183_protected37_screen_v2_20261011')
    closed('actual_stock_rank120_embedding_after183_direct_allocation33_v1_20261011')
    closed('actual_stock_rank120_embedding_six_state_native42_v1_20261011')
    closed('actual_stock_rank60_embedding_six_state_native42_v1_20261011')
    closed('actual_stock_rank120_embedding_small512_bank6_v1_20261011')
    closed('StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
    release=read(A/'github_validation_sync_main_20261005/round183_receipt.json')
    assert release['status']=='pushed_and_remote_head_verified' and release['scored_records']==85
    import numpy as np,polars as pl,psutil
    import immutable_prepared_rank_panel_cache_v1_20261010 as panel_cache
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as cdf
    import protected_upper_tail_rank_permutation_v1_20261010 as valid_tail
    import protected_official_top_rank_permutation_v2_20261010 as top_tail
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as percentiles
    from cached_official_spearman_runtime_20261007 import installed as spearman
    bank=Path('E:/赛题五_本机临时/stock_rank120_embedding_small512_BF16_bank6_v1_20261011')
    fullpointer=A/'actual_StockRank120EmbeddingSmall512_full5_independent_location_v1_20261011.json';nativepointer=fullpointer
    full=Path(read(fullpointer)['output']);native=Path(read(nativepointer)['output'])
    assert read(bank/'verification.json')['actual_native_fits']==6
    assert read(full/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
    assert read(native/'verification.json')['actual_complete_bank_fits']==6
    assert len(read(native/'verification.json')['records'])==5
    actual_native_pointer=A/'actual_stock_rank120_embedding_six_state_native42_location_v1_20261011.json'
    actual_native_folder=Path(read(actual_native_pointer)['output']);actual_native_proof=read(actual_native_folder/'verification.json')
    assert actual_native_proof['actual_saved_states']==6 and actual_native_proof['actual_native_cases']==42 and actual_native_proof['actual_cold_cases']==42
    import rank120_rank60_consensus_raw_signal80_v1_20261011 as mixing
    oldpointer=A/'actual_StockRank60EmbeddingSmall512_full5_independent_location_v1_20261011.json'
    oldfull=Path(read(oldpointer)['output'])
    oldbank=Path('E:/赛题五_本机临时/stock_rank60_embedding_small512_BF16_bank6_v1_20261011')
    assert read(oldfull/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
    assert read(oldbank/'verification.json')['actual_native_fits']==6
    oldnativepointer=A/'actual_stock_rank60_embedding_six_state_native42_location_v1_20261011.json'
    oldnative=Path(read(oldnativepointer)['output']);oldnativeproof=read(oldnative/'verification.json')
    assert oldnativeproof['actual_saved_states']==6 and oldnativeproof['actual_native_cases']==42 and oldnativeproof['actual_cold_cases']==42
    paths=[actual_native_pointer,actual_native_folder/'verification.json',Path(__file__),A/'exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010.py',A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json',A/'exact_E_TRAIN_validation_actual_anchor169_all8_compatibility_v1_20261010.json',A/'后续选模标准.md' if (A/'后续选模标准.md').exists() else ROOT/'后续选模标准.md',fullpointer,nativepointer,
        bank/'verification.json',full/'verification.json',native/'verification.json',full/'combined_raw.parquet',
        A/'optimization_20261003_r183/selected_validation.npy',A/'optimization_20261003_r183/calibrated_csv_official.json',A/'connected_validation_20261002/combined_fold_frame.parquet',
        Path(cdf.__file__),Path(valid_tail.__file__),Path(top_tail.__file__),A/'protected_upper_tail_rank_permutation_controls_v1_20261010.json',A/'protected_official_top_rank_permutation_controls_v2_20261010.json']
    paths.extend([Path(panel_cache.__file__),A/'immutable_prepared_rank_panel_cache_actual_full_TRAIN_benchmark_v1_20261010.json'])
    paths += [oldpointer,oldfull/'verification.json',oldfull/'combined_raw.parquet',oldbank/'verification.json',
        oldnativepointer,oldnative/'verification.json',Path(mixing.__file__),A/'actual_consensus8_pointwise_CPU_controls80_v1_20261011.json',
        A/'rank120_rank60_after183_protected37_predeclared_sources_admission_v1_20261011.json']
    for year in range(2020,2026):
        left=read(oldbank/str(year)/'info.json');right=read(bank/str(year)/'info.json')
        assert left['configuration']['seed']==right['configuration']['seed']==20261009
        assert left['configuration']['label_horizon_trading_days']==60
        assert right['configuration']['label_horizon_trading_days']==120
        assert left['configuration']['target']=='y_rank_60mean' and right['configuration']['target']=='y_rank_120mean'
        assert left['configuration']['training_calendar_window']==right['configuration']['training_calendar_window']==252
        assert left['model_sha256']!=right['model_sha256']
        # Each horizon is independently matured. Their training matrices/populations are intentionally different.
        paths += [oldbank/str(year)/'info.json',bank/str(year)/'info.json']
    paths += [A/'rank120_rank60_best_blend_fraction38_predeclared_sources_admission_v1_20261011.json',Path('E:/赛题五_本机临时/StockRank120Rank60_after183_protected37_screen_v1_20261011/verification.json'),A/'actual_fraction38_completed_only_terminal_namespace_collision_bridge_v1_20261011.json']
    paths += [A/'rank120_rank60_consensus8_predeclared_sources80_v1_20261011.json']
    pins={str(p):sha(p) for p in paths};plan=cases()
    OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_any_new_controls_or_scores.json',{'status':'frozen8_consensus80_own_stock_embedding_return1d_after183_hypotheses_after_own6_full5_independent_qualification_selected_six_state_stage_pending','at_local':datetime.now().isoformat(),'input_sha256':pins,'cases':plan,'parent_round':183,'both_actual_mature_horizon_banks_training_complete':True,'future_X_read':False,'test_labels_read':False,'new_native_fits_by_screen':0})
    scoring=OUT/'scoring_validation_only';scoring.mkdir(parents=True,exist_ok=False)
    for name in ('测试集_X.csv','测试集_Y.csv'):
        import shutil
        label_source=A/'optimization_20261003_r95/scoring_validation_only'/name
        shutil.copyfile(label_source,scoring/name)
        assert sha(label_source)==sha(scoring/name)
    scratch=OUT/'tmp';scratch.mkdir()
    for key in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    import tempfile;tempfile.tempdir=str(scratch)
    from exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010 import installed as exact_E_TRAIN_guard
    with exact_E_TRAIN_guard(scoring,OUT/'actual_E_TRAIN_cache_guard_binding_v2_20261010.json'):
        while psutil.virtual_memory().available<11.5*2**30:assert allowed();time.sleep(15)
        frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        rf=pl.read_parquet(full/'combined_raw.parquet');assert rf.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
        rf09=pl.read_parquet(oldfull/'combined_raw.parquet');assert rf09.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        parent=np.load(A/'optimization_20261003_r183/selected_validation.npy',mmap_mode='r');raw=rf['pred_raw'].to_numpy()
        baseline=read(A/'optimization_20261003_r183/calibrated_csv_official.json')['metrics'];ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring)
        ranks={};records=[];prepared={}
        raw120=raw;raw09=rf09['pred_raw'].to_numpy();active_blend=None
        panel=None
        exact=lambda x,y:np.array_equal(np.asarray(x,dtype=np.float64).view('u8'),np.asarray(y,dtype=np.float64).view('u8'))
        def transformed(c,n=None,oracle=False):
            n=len(parent) if n is None else n
            if c['kind']=='anchor183':return np.asarray(parent[:n])
            if not oracle:return panel.transform(c,n)
            codec=cdf if c['kind']=='CDF' else valid_tail if c['kind']=='valid_pool_protection_v1' else top_tail
            args=(c['role'],c['weight'],c['sign']) if c['kind']=='CDF' else (c['weight'],c['protect_fraction'],c['sign'])
            fn=codec.pandas_oracle if oracle else codec.transform
            return fn(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args)
        for i,c in enumerate(plan):
            assert allowed()
            if i and c['disagreement_penalty']!=active_blend:
                active_blend=c['disagreement_penalty'];raw=mixing.combine(raw09,raw120,active_blend)
                scalar=mixing.scalar_oracle(raw09,raw120,active_blend);assert exact(raw,scalar);del scalar
                for days in (80,260,975):
                    n=days*4650;assert exact(raw[:n],mixing.combine(raw09[:n],raw120[:n],active_blend))
                    assert exact(raw[:n],mixing.scalar_oracle(raw09[:n],raw120[:n],active_blend))
                create(OUT/f'blend{active_blend}_controls.json',{'disagreement_penalty':active_blend,'rows':len(raw),'actual_full_scalar_bits_exact':True,'prefix_days':[80,260,975],'future_X_read':False})
                del panel;gc.collect();panel=panel_cache.Panel(parent,raw,dates,flags,valid)
            value=transformed(c)
            checks=[]
            if i:
                oracle=transformed(c,oracle=True);assert exact(value,oracle);del oracle
                if c['kind']=='CDF':assert exact(value[~cdf.selected(flags,valid,c['role'])],parent[~cdf.selected(flags,valid,c['role'])])
                else:(valid_tail if c['kind']=='valid_pool_protection_v1' else top_tail).assert_invariants(parent,value,dates,flags,valid,c['protect_fraction'])
                for days in (80,260,975):
                    n=days*4650;prefix=transformed(c,n);oracle=transformed(c,n,True)
                    assert exact(value[:n],prefix) and exact(value[:n],oracle);checks.append({'days':days,'rows':n,'native_and_independent_bits_exact':True});del prefix,oracle
            numeric=hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()
            create(OUT/f'case{i:03d}_controls.json',{'case':i,'configuration':c,'numeric_sha256':numeric,'full_independent_Pandas_exact':bool(i),'prefix_controls':checks,'rows':len(value),'complete_parent183_preserved_before_stage':True,'future_X_read':False})
            write(OUT/'actual_stage.json',{'status':'actual_disagreement_rank120_rank60_10_TRAIN_only_official_scoring','case':i,'completed_cases':len(records),'expected_cases':8,'at_local':datetime.now().isoformat()})
            assert allowed()
            with percentiles(),spearman(ranks),installed(scoring/'submission.csv'):metrics=score(ctx,value)
            if not i:assert metrics==baseline
            if i==1:
                reference=read(Path('E:/赛题五_本机临时/StockRank120Rank60_after183_disagreement10_screen_v1_20261011/verification.json'))['best']
                assert metrics==reference['metrics'] and numeric==reference['prediction_numeric_sha256']
            capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
            row={'case':i,'configuration':c,'recipe':'stock_rank120_rank60_disagreement_label_horizon_ID16_cross120_recent252_e64','metrics':metrics,'connected_final_score':metrics['final_score'],'score_gain_over_qualified_parent':metrics['final_score']-baseline['final_score'],'control_sha256':sha(OUT/f'case{i:03d}_controls.json'),'prediction_numeric_sha256':numeric,'official_metric_capsule_sha256':sha(capsule),'official_score_cache':ctx.last_official_score_cache,'actual_return_mapping':ctx.last_candidate_return_mapping,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'selection_bias_uncorrected':True}
            create(OUT/f'case{i:03d}_official.json',row);records.append(row)
            write(OUT/'best_so_far.json',{'completed_cases':len(records),'expected_cases':8,'best':max(records,key=lambda r:r['connected_final_score']),'submission_qualified':False})
            print({'case':i,'configuration':c,'S':metrics['final_score'],'gain':row['score_gain_over_qualified_parent']},flush=True);del value;gc.collect()
        for p,d in pins.items():assert sha(p)==d,p
        create(OUT/'verification.json',{'status':'passed8_consensus80_rank120_rank60_TRAIN_only_protected_both_signs_official_comparisons','at_local':datetime.now().isoformat(),'input_sha256':pins,'records':records,'best':max(records,key=lambda r:r['connected_final_score']),'new_quality_score_records':8,'actual_nonidentity_full_controls':7,'actual_nonidentity_prefix_controls':21,'submission_qualified':False,'future_X_read':False,'test_labels_read':False,'global_feasible_direction_exhaustion_not_proven':True})
        create(A/'actual_StockRank120Rank60_after183_consensus8_screen80_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
