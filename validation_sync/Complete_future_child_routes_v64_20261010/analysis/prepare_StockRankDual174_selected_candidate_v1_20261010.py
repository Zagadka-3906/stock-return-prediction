"""Freeze a complete mature neural/parent scheme before selected future X; reuse exact anchors honestly."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import hashlib,os,shutil,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=A/'StockRankDual174_selected_release_v1_20261010'
CANDIDATE=ROOT/'candidates/StockRankDual174_v1_20261010'
GRAPH_FIELD='conditional_flag_residual_scheme_graph'
GRAPH_KEY='stock_rank_dual44_after_complete_parent_v1_20261010'
CODECS={'CDF':'BF16Medium153_complete_parent_rank_CDF_v1_20261009','valid_pool_protection_v1':'protected_upper_tail_rank_permutation_v1_20261010','official_Top_protection_v2':'protected_official_top_rank_permutation_v2_20261010'}


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name


def rebase_graph(node):
    if isinstance(node,dict):
        if 'source_path' in node and 'path' in node:
            node['path']=str(CANDIDATE/Path(node['path']).name)
            for key in ('independent_dump_path','independent_state_path'):
                if key in node:node[key]=str(CANDIDATE/Path(node[key]).name)
        for value in node.values():rebase_graph(value)
    elif isinstance(node,list):
        for value in node:rebase_graph(value)


def main():
    from qualify_stock_rank_dual44_selected_native14_v1_20261010 import allowed
    assert allowed()
    closed('StockRankDual44_selected_native14_v1_20261010')
    import numpy as np
    import pandas as pd
    import polars as pl
    import psutil
    from run import fold_cutoff
    from stock_rank_dual174_storage_v1_20261010 import empty,installed_transfer
    import importlib
    import stock_rank_dual44_selected_native_stage_v1_20261010 as native_stage
    from score_calibrated_candidates_20261003 import score
    from return_mapping import daily_percentile,fit_mapping
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    from qualify_stock_rank_dual44_selected_native14_v1_20261010 import OUT as native_out
    empty(OUT);empty(CANDIDATE)
    while psutil.virtual_memory().available<9*2**30:time.sleep(15)
    pilot_path=native_out/'pilot44.json';pilot=read(pilot_path)
    assert pilot['status']=='passed_normalized44_actual_TRAIN_official_records_selected_stage_and_full_inference_pending'
    assert len(pilot['records'])==44
    def best_key(r):return (-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case'])
    best=min(pilot['records'],key=best_key)
    assert best==pilot['best'];cfg=best['configuration']
    comparison_parent=pilot['actual_comparison_parent_round']
    parent_number=cfg['anchor_round']
    assert parent_number in (170,173)
    parent_candidate=ROOT/f'candidates/optimization_20261003_r{parent_number}'
    parent_release=A/f'optimization_20261003_r{parent_number}'
    parent_record=read(parent_candidate/'selection.json');parent_prediction=read(parent_candidate/'verification.json')
    parent_manifest=read(parent_candidate/'manifest.json')
    assert read(parent_release/'full_registration_execution.json')['status']=='passed'
    import optimize_training_round95_v3 as native_parent
    from resolve_sealed_scientific_protocol_v2_20261007 import resolve
    scientific_protocol,protocol_pins,protocol_proof=resolve(parent_candidate,parent_release,parent_prediction['whole_scheme_graph'],native_parent)
    create(OUT/'scientific_protocol_resolution_before_future_features.json',protocol_proof)
    sources=[Path(__file__),A/'stock_rank_dual174_storage_v1_20261010.py',A/'predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py',A/'stock_rank_dual44_selected_native_stage_v1_20261010.py',A/'seal_stock_rank_dual174_selected_candidate_v1_20261010.py',A/'stock_rank_dual174_candidate_sources_preparation_v1_20261010.json',native_out/'verification.json',pilot_path,parent_candidate/'manifest.json',parent_candidate/'source_package_verification.json',parent_release/'full_registration_execution.json']
    pins={**protocol_pins,**pilot['input_sha256'],**{str(p):sha(p) for p in sources}}
    pins[str(A/'resolve_sealed_scientific_protocol_v2_20261007.py')]=sha(A/'resolve_sealed_scientific_protocol_v2_20261007.py')
    for relative,info in parent_manifest['files'].items():
        path=parent_candidate/relative;assert sha(path)==info['sha256'];pins[str(path)]=info['sha256']
    create(OUT/'selected_case_before_future_features.json',{'status':'selected_by_all44_actual_official_scores',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'best':best,
        'explicit_parent_round':comparison_parent,'actual_scheme_base_round':parent_number,
        'future_features_for_new_selected_scheme_not_yet_read':True,'new_native_fits':0,'test_labels_read':False})
    raw_path=parent_release/'selected_validation.npy'
    if cfg['model'] is None or cfg['weight']==0.:
        raw=np.load(raw_path,mmap_mode='r')
        assert hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest()==best['prediction_numeric_bytes_sha256']
        assert best['metrics']==parent_record['winner']['metrics']
        assert parent_prediction['status']=='passed' and parent_prediction['whole_scheme_graph']==parent_record['winner'][GRAPH_FIELD]
        for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert parent_prediction[key]
        assert sha(parent_candidate/'submission.csv')==parent_prediction['csv_sha256']
        create(OUT/'inference_ready.json',{'status':'passed_exact_selected_anchor44_candidate_reuse',
            'source_candidate':str(parent_candidate),'source_release':str(parent_release),'selected_configuration':cfg,'best':best,
            'manifest_sha256':sha(parent_candidate/'manifest.json'),'actual_saved_native_models':len(parent_prediction['models']),
            'actual_rehashed_candidate_files':len(parent_manifest['files']),'original_inference_freeze_timestamp':parent_record['frozen_at_local'],
            'all5635800_validation_raw_bits_and_all8_metrics_exact':True,'new_inference_claimed':False,'test_labels_read':False})
        return
    assert parent_number in (170,173) and 0.<cfg['weight']<=1. and cfg['sign'] in (-1.,1.)
    leaves=best['native_bank_components'];assert len(leaves) in (1,2)
    assert (len(leaves)==2)==(cfg['stage_kind']=='stock_return_rank_embedding_consensus')
    transform=importlib.import_module(CODECS[cfg['codec']]).transform
    components=[]
    for leaf in leaves:
        bank=Path(leaf['bank']);CONFIG=importlib.import_module(native_stage.BACKENDS[leaf['recipe']][0]).CONFIG
        info=read(bank/'2025/info.json');meta=info['training_meta']
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and info['year']==2025
        assert info['configuration']==CONFIG and meta['last']<meta['cutoff_exclusive']==fold_cutoff(2025) and meta['last_label_end']<=meta['cutoff_exclusive']
        component={'name':leaf['name'],'source_path':str(bank/'2025/model.joblib'),'path':str(CANDIDATE/(leaf['name']+'_final2025.joblib')),'sha256':info['model_sha256'],'configuration':CONFIG,'training_info':info}
        assert sha(component['source_path'])==component['sha256'];pins[component['source_path']]=component['sha256'];components.append(component)
    freeze=Path('E:/赛题五_本机临时/第174轮_20261010/pre_inference_source_freeze_v1');assert not freeze.exists();freeze.mkdir()
    python_sources=sorted(set(ROOT.glob('*.py'))|set(A.glob('*.py'))|set((A/'connected_validation_20261002').glob('*.py'))|set((ROOT/'src').rglob('*.py'))|set((ROOT/'experiments').rglob('*.py')))
    snapshot={}
    for source in python_sources:
        digest=sha(source);target=freeze/'repo'/source.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target);assert sha(target)==sha(source)==digest
        snapshot[source.relative_to(ROOT).as_posix()]={'sha256':digest,'bytes':source.stat().st_size};pins[str(source)]=digest
    import importlib.metadata
    create(freeze/'manifest.json',{'status':'passed_pre_inference_local_Python_source_snapshot','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'files':snapshot,'library_versions':{n:importlib.metadata.version(n) for n in ('numpy','pandas','polars','scikit-learn','joblib','lightgbm','torch')},'test_labels_read':False})
    pins[str(freeze/'manifest.json')]=sha(freeze/'manifest.json')
    # Resolve saved raw-panel locations from the actual recipe's passed own-independent proof.
    own_pointers={'stock_embedding16_cross120_return1d_recent252_small512_BF16_e24':'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json','stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24':'actual_StockRankEmbeddingSmall512_full5_independent_location_v1_20261009.json'}
    neural_folders=[Path(read(A/own_pointers[leaf['recipe']])['output']) for leaf in leaves]
    neural_paths=[folder/'combined_raw.parquet' for folder in neural_folders]
    neural_folder=neural_folders[0];neural_path=neural_paths[0]
    for p in [raw_path,*neural_paths,*[f/'verification.json' for f in neural_folders]]:pins[str(p)]=sha(p)
    with LockedReadHashCache(pins) as scope,installed_transfer():
        frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        neural_frame=pl.read_parquet(neural_path);assert neural_frame.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
        raw=np.load(raw_path,mmap_mode='r');neural=neural_frame['pred_raw'].to_numpy()
        assert cfg['decay'] is None
        if len(leaves)==2:
            import dual_target_daily_rank_consensus_v1_20261010 as dual
            second=pl.read_parquet(neural_paths[1]);assert second.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
            neural=dual.transform(neural,second['pred_raw'].to_numpy(),dates,cfg['mean_weight'])
            del second
        else:assert cfg['stage_kind']=='stock_rank_embedding_rank1d_direct'

        selected=transform(raw,neural,dates,flags,valid,*((cfg['role'],cfg['weight'],cfg['sign']) if cfg['codec']=='CDF' else (cfg['weight'],cfg['protect_fraction'],cfg['sign'])))
        assert hashlib.sha256(memoryview(np.ascontiguousarray(selected)).cast('B')).hexdigest()==best['prediction_numeric_bytes_sha256']
        np.save(OUT/'selected_validation.npy',selected)
        scoring=Path('E:/赛题五_本机临时/第174轮_20261010/selected_scoring/scoring_validation_only');scoring.mkdir(parents=True)
        for filename in ('测试集_X.csv','测试集_Y.csv'):os.link(A/'optimization_20261003_r95/scoring_validation_only'/filename,scoring/filename)
        ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring)
        from exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010 import installed as exact_E_guard
        with exact_E_guard(scoring,OUT/'actual_E_TRAIN_cache_guard_binding_v2_20261010.json'):
            assert score(ctx,selected)==best['metrics']
        capsule=read(ctx.last_official_score_cache['official_metrics_source'])
        create(OUT/'calibrated_csv_official.json',{'status':'passed','metrics':best['metrics'],'csv_sha256':capsule['scope']['submission_csv_sha256'],
            'actual_official_capsule':ctx.last_official_score_cache,'actual_mature_return_mapping':ctx.last_candidate_return_mapping,'test_labels_read':False})
        y=frame['y_ret_1d'].to_numpy().astype(np.float64);cutoff=fold_cutoff(2025);historical=(dates<cutoff)&np.isfinite(y)
        pct=daily_percentile(frame.select('trade_date').to_pandas(),selected)
        create(OUT/'future_return_mapping.json',fit_mapping(pct[historical],y[historical]))
        create(OUT/'causal_validation.json',{'status':'passed','actual_all44_official_controls':str(pilot_path),
            'actual_own_mature_banks_and_full_independent_controls':[str(f/'verification.json') for f in neural_folders],'actual_selected14_native14_cold7_prefit_controls':str(native_out/'verification.json'),
            'actual_selected_full5635800_numeric_bits_match_pilot':True,'final_mapping_training_rows':int(historical.sum()),
            'exclusive_cutoff':cutoff,'new_native_fits':0,'test_labels_read':False})
        graph=deepcopy(parent_prediction['whole_scheme_graph']);rebase_graph(graph)
        graph['cohort_rank_calibration']['future_curve_model']['path']=str(CANDIDATE/'cohort_curve.json')
        graph[GRAPH_KEY]={**cfg,'rank_universe':'all_current_raw_forecasts','first2020_active':True,'sign':cfg['sign'],'invalid_signal_bits_preserved':True,'selected_native14_source':str(native_out/'verification.json'),
            'position':'after_complete_qualified_parent','native_components':components,
            'transformation':'per-day protected-tail parent-value permutation by mature neural ranks; official_Top_v2 additionally applies documented oneULP cutoff-tie lift','codec_module':CODECS[cfg['codec']] ,
            'original_complete_parent_round':parent_number,'original_complete_parent_graph_preserved':True}
        winner=deepcopy(parent_record['winner']);winner.update(metrics=best['metrics'],connected_final_score=best['connected_final_score']);winner[GRAPH_FIELD]=graph
        protocol=deepcopy(scientific_protocol);protocol.update(input_sha256=pins,explicit_parent_round=comparison_parent,
            expected_scored_records=44,status='frozen_selected_StockRankDual174_before_future_inference',current_parameter_authority=GRAPH_FIELD)
        create(OUT/'protocol.json',protocol)
        frozen={Path(p).relative_to(ROOT).as_posix():d for p,d in pins.items() if Path(p).is_relative_to(ROOT)}
        for path in (OUT/'protocol.json',OUT/'selected_validation.npy',OUT/'future_return_mapping.json',ROOT/'active_release.json'):frozen[path.relative_to(ROOT).as_posix()]=sha(path)
        external={p:d for p,d in pins.items() if not Path(p).is_relative_to(ROOT)}
        unique={c['sha256'] for c in parent_prediction['models'].values()}|{c['sha256'] for c in components}
        selection={'status':'frozen_before_test_prediction','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'winner':winner,
            'scored_records':44,'explicit_parent_round':comparison_parent,'actual_scheme_base_round':parent_number,'chosen_postprocessor':cfg,
            'native_component_names':list(dict.fromkeys([*parent_record['native_component_names'],*[c['name'] for c in components if c['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()}]])),
            'actual_expected_unique_native_models':len(unique),'current_parameter_authority':GRAPH_FIELD,
            'actual_official_pilot_source':str(pilot_path),'frozen_sha256':frozen,'frozen_external_input_sha256':external,
            'all_training_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,'test_labels_read':False}
        create(OUT/'selection.json',selection)
        create(OUT/'frozen_before_actual_candidate_inference.json',{'input_sha256':pins,'selection_sha256':sha(OUT/'selection.json'),
            'source_snapshot_manifest_sha256':sha(freeze/'manifest.json'),'parent_curve_sha256':sha(parent_candidate/'cohort_curve.json'),'test_labels_read':False})
        ns=SimpleNamespace(**vars(native_parent));ns.OUT,ns.GRAPH_FIELD=OUT,GRAPH_FIELD;ns.cohort_saved_models=parent_prediction['models']
        assert allowed()
        from predict_stock_rank_dual44_complete_parent_scheme_v1_20261010 import predict
        locked_outputs={str(OUT/n):sha(OUT/n) for n in ('protocol.json','selection.json','selected_validation.npy','future_return_mapping.json')}
        with LockedReadHashCache(locked_outputs) as output_scope:
            from short_content_addressed_native_storage_v2_20261008 import installed as short_storage
            with short_storage(ns,freeze/'model_source_aliases') as alias_contract:
                prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json')
            create(OUT/'short_native_source_aliases_execution.json',alias_contract)
            output_scope.reverify()
        scope.reverify()
        assert (prediction['rows'],prediction['days'],prediction['codes'])==(1599600,344,4650)
        assert len(prediction['models'])==len(storage)==len(unique)
        create(OUT/'verification.json',{'status':'passed_frozen_StockRankDual174_complete_parent_native_independent_and_cold80',
            'input_sha256':pins,'candidate':str(CANDIDATE),'csv_sha256':prediction['csv_sha256'],'selected_configuration':cfg,
            'selected_official_score':best['connected_final_score'],'actual_native_model_storage':storage,'actual_saved_model_count':len(unique),
            'all_inputs_initial_and_final_full_Windows_read_locked_hash':True,'new_native_fits':0,'test_labels_read':False})
        create(OUT/'inference_ready.json',{'status':'passed_actual_selected_new_StockRankDual174_candidate_inference',
            'source_candidate':str(CANDIDATE),'source_release':str(OUT),'selected_configuration':cfg,'best':best,
            'actual_saved_native_models':len(unique),'new_inference_claimed':True,'pre_inference_source_snapshot':str(freeze),'test_labels_read':False})


if __name__=='__main__':main()
