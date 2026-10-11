"""Infer every effective frozen root/layer from copied model bytes."""
from pathlib import Path
from copy import deepcopy
import shutil


def predict(ns,record,candidate_path=None,mapping_path=None):
    import numpy as np
    import pandas as pd
    import polars as pl
    from run import FEATURE_FILE
    from return_mapping import apply_mapping,daily_percentile
    ROOT,OUT,KEYS,read,dump,sha=ns.ROOT,ns.OUT,ns.KEYS,ns.read,ns.dump,ns.sha
    root_model_sources,state_mapping_path=ns.root_model_sources,ns.state_mapping_path
    from whole_scheme_future_runtime_20261004 import copy_models,build_context
    from neural_width_scheme_runtime_20261004 import native_sources
    resolve_native_sources=getattr(ns,"future_native_sources",native_sources)
    candidate=Path(candidate_path) if candidate_path is not None else ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    candidate.mkdir(parents=True,exist_ok=True)
    if (candidate/'verification.json').exists():
        assert sha(candidate/'submission.csv')==read(candidate/'verification.json')['csv_sha256'];return
    winner=record['winner'];graph=deepcopy(winner[ns.GRAPH_FIELD])
    protocol=read(OUT/'protocol.json')
    native=resolve_native_sources(graph);root_sources=root_model_sources(graph)
    for name,info in native.items():
        assert info['sha256']==protocol['future_native_model_sources'][name]['sha256'],name
    for name,info in root_sources.items():
        assert info['sha256']==protocol['future_root_model_sources'][name]['sha256'],name
    # Original full-training models andall recipe parameters were frozen earlier.
    models=copy_models(native,root_sources,candidate)
    copied_native={name:models['whole_'+name] for name in native}
    copied_root={name:models[name] for name in root_sources}
    mappings=read(state_mapping_path())['mappings']
    path=Path(mapping_path) if mapping_path is not None else OUT/'future_return_mapping.json'
    mapping=read(path)
    dump(candidate/'frozen_before_model_inference.json',{'status':'frozen_before_future_inference',
        'whole_scheme_graph':graph,'model_sha256':{key:info['sha256'] for key,info in models.items()},
        'recipe_protocol_sha256':sha(OUT/'protocol.json'),'return_mapping_sha256':sha(path),
        'market_state_mapping_sha256':sha(state_mapping_path()),'new_fulltraining_fits':0,
        'implementation_control_only':winner['connected_final_score'] is None,'test_labels_read':False},immutable=True)
    formal=ROOT/'deliveries/connected_topk0175_20261003'
    inputs=pl.read_parquet(formal/'generation_inputs.parquet')
    features=read(formal/'train_test.json')['features']
    test=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features).sort('trade_date','ts_code').collect()
    assert test.select(KEYS).equals(inputs.select(KEYS))
    ctx,model_checks=build_context(graph,inputs,test,copied_native,copied_root,mappings)
    rank,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
    replay,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.);assert np.array_equal(rank,replay)
    dates=inputs['trade_date'].to_numpy();n=int(np.searchsorted(dates,np.unique(dates)[79],side='right'))
    prefix,prefix_checks=build_context(graph,inputs.head(n),test.head(n),copied_native,copied_root,mappings)
    assert np.array_equal(rank[:n],prefix.predict(prefix.donor(prefix.finished('baseline')),0.,0.)[0])
    mapped=apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),rank))
    assert np.array_equal(pd.Series(rank).groupby(dates).rank().to_numpy(),pd.Series(mapped).groupby(dates).rank().to_numpy())
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    sub=inputs.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    csv=candidate/'submission.csv';sub.write_csv(csv,float_precision=17);parsed=pd.read_csv(csv)
    assert len(parsed)==1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any() and np.isfinite(parsed.pred).all()
    assert np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    assert sub.write_csv(float_precision=17).encode('utf-8')==csv.read_bytes()
    np.save(candidate/'rank_prediction.npy',rank)
    for name in ('role_layer_replay_20261004.py','selected_scheme_graph_20261004.py',
                 'whole_scheme_replay_runtime_20261004.py','whole_scheme_future_runtime_20261004.py',
                 'neural_width_scheme_runtime_20261004.py','neural_width_search_engine_20261004.py',
                 'predict_neural_width_scheme_20261004.py'):
        shutil.copyfile(ROOT/'analysis'/name,candidate/name)
    dump(candidate/'selection.json',record,immutable=True);dump(candidate/'return_mapping.json',mapping,immutable=True)
    dump(candidate/'market_regime_mapping.json',{'mappings':mappings,'fitted_before_future_inference':True},immutable=True)
    dump(candidate/'verification.json',{'status':'passed','csv_sha256':sha(csv),'rows':1599600,'days':344,'codes':4650,
        'models':models,'model_reload_bit_identical':True,'actual_model_reload_controls':model_checks,
        'actual80_day_prefix_model_controls':prefix_checks,'pipeline_replay_bit_identical':True,
        'csv_replay_byte_identical':True,'csv_ranks_unchanged':True,'cold80_day_prefix_bit_identical':True,
        'whole_scheme_graph':graph,'current_parameter_authority':ns.GRAPH_FIELD,'validation_score':winner['connected_final_score'],'test_labels_read':False,
        'new_fulltrain_models':0,'construction':stats,'pruned_member_excluded':True,
        'model_replay_scope':'Effective selected root andevery surviving role layer inferred from actual copied frozen model bytes; no saved final-output foundation substituted.',
        'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']},immutable=True)
