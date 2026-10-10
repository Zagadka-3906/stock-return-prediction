"""Replay frozen complete-foundation predictions plus separately fitted role signals."""
from pathlib import Path
import shutil


def predict(record,candidate_path=None):
    import numpy as np
    import pandas as pd
    import polars as pl
    from run import FEATURE_FILE,to_matrix
    from optimize_wave15 import daily_ranks
    from return_mapping import apply_mapping,daily_percentile
    import fourier_ridge_model_sources_20261004 as trainer
    from optimize_training_round43 import ROOT,OUT,FOUNDATION,KEYS,Context,read,dump,sha,log
    candidate=Path(candidate_path) if candidate_path is not None else ROOT/'candidates/optimization_20261003_r43';formal=ROOT/'deliveries/connected_topk0175_20261003'
    foundation_candidate=ROOT/f'candidates/{FOUNDATION.name}';winner=record['winner']
    candidate.mkdir(parents=True,exist_ok=True)
    foundation=read(foundation_candidate/'verification.json');assert foundation['status']=='passed'
    source_base=foundation_candidate/'rank_prediction.npy';manifest=read(foundation_candidate/'manifest.json')
    assert sha(source_base)==manifest['files']['rank_prediction.npy']['sha256']
    models={}
    for key,info in foundation['models'].items():
        source=Path(info['path']);assert sha(source)==info['sha256'];target=candidate/source.name
        shutil.copyfile(source,target);assert sha(target)==info['sha256']
        models[key]={**info,'path':str(target),'foundation_source':str(source)}
    used=sorted({spec['model'] for spec in winner['fourier_ridge_augmentation'].values() if spec['weight']>0})
    # Additional final fits finish before test feature inference.
    full_info={name:trainer.train_one(name,2025) for name in used}
    for info in full_info.values():
        meta=info['training_meta'];assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
    inputs=pl.read_parquet(formal/'generation_inputs.parquet').with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    features=read(formal/'train_test.json')['features']
    frame=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features).sort('trade_date','ts_code').collect()
    assert frame.select(KEYS).equals(inputs.select(KEYS));x=to_matrix(frame,features)
    dates=inputs['trade_date'].to_numpy();valid=inputs['price_valid'].to_numpy()
    base=np.load(source_base);assert len(base)==len(inputs)
    ctx=Context.__new__(Context);ctx.dates=dates;ctx.valid=valid;ctx.flags=inputs['flag_limit_up'].to_numpy().astype(np.int64)
    ctx.codes,unique=pd.factorize(inputs['ts_code'].to_pandas(),sort=True);ctx.codes=ctx.codes.astype(np.int64)
    ctx.n_codes=len(unique);ctx.tie_key=1-ctx.codes/max(ctx.n_codes-1,1)
    ctx.fourier_ridge_augmentation=winner['fourier_ridge_augmentation'];ctx.fourier_ridge_limit_delta=winner['fourier_ridge_limit_delta'];ctx._final_cache={}
    for name in used:
        info=full_info[name];assert info['training_meta']['features']==features
        source=trainer.model_path(name,2025);assert sha(source)==info['model_sha256']
        raw=trainer.predict_arrays(trainer.load_bundle(source),x,dates=dates,valid=valid)
        replay=trainer.predict_arrays(trainer.load_bundle(source),x,dates=dates,valid=valid)
        assert np.array_equal(raw,replay) and np.isfinite(raw).all();raw[~valid]=-1e6
        ctx._final_cache[name]=daily_ranks(raw,valid,dates)
        target=candidate/f'model_final_{name}.joblib';shutil.copyfile(source,target);assert sha(target)==info['model_sha256']
        models['final_'+name]={'path':str(target),'sha256':sha(target),'training_info':info,'reload_bit_identical':True,'original':str(source)}
    rank,stats=ctx.finish_output(base,winner['retention'],winner['limit_up_delta']+winner.get('final_limit_delta',0.)+winner.get('linear_limit_delta',0.)+winner.get('regularization_limit_delta',0.)+winner.get('stacking_limit_delta',0.)+winner.get('neural_tuning_limit_delta',0.)+winner.get('catboost_tuning_limit_delta',0.)+winner.get('expanded_stacking_limit_delta',0.)+winner.get('additive_ridge_limit_delta',0.))
    replay,_=ctx.finish_output(np.load(source_base),winner['retention'],winner['limit_up_delta']+winner.get('final_limit_delta',0.)+winner.get('linear_limit_delta',0.)+winner.get('regularization_limit_delta',0.)+winner.get('stacking_limit_delta',0.)+winner.get('neural_tuning_limit_delta',0.)+winner.get('catboost_tuning_limit_delta',0.)+winner.get('expanded_stacking_limit_delta',0.)+winner.get('additive_ridge_limit_delta',0.));assert np.array_equal(rank,replay)
    mapping=read(OUT/'future_return_mapping.json');mapped=apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),rank))
    assert np.array_equal(pd.Series(rank).groupby(dates).rank().to_numpy(),pd.Series(mapped).groupby(dates).rank().to_numpy())
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    sub=inputs.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    target=candidate/'submission.csv';sub.write_csv(target,float_precision=17);parsed=pd.read_csv(target)
    assert len(parsed)==1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any() and np.isfinite(parsed.pred).all()
    assert np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    assert sub.write_csv(float_precision=17).encode('utf-8')==target.read_bytes()
    np.save(candidate/'rank_prediction.npy',rank);shutil.copyfile(source_base,candidate/'foundation_rank_prediction.npy')
    dump(candidate/'selection.json',record,immutable=True);dump(candidate/'return_mapping.json',mapping,immutable=True)
    dump(candidate/'verification.json',{'status':'passed','csv_sha256':sha(target),'rows':len(sub),'days':344,'codes':4650,
         'models':models,'model_reload_bit_identical':True,'pipeline_replay_bit_identical':True,'csv_replay_byte_identical':True,
         'csv_ranks_unchanged':True,'validation_score':winner['connected_final_score'],'test_labels_read':False,
         'foundation_candidate':str(foundation_candidate),'foundation_verification_sha256':sha(foundation_candidate/'verification.json'),
         'foundation_rank_source_sha256':sha(source_base),'frozen_foundation_predictions_reused':True,
         'fourier_ridge_augmentation':winner['fourier_ridge_augmentation'],'fourier_ridge_limit_delta':winner['fourier_ridge_limit_delta'],
         'new_fulltrain_models':len(used),'construction':stats,'pruned_member_excluded':True,
         'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']},immutable=True)
    log(f'Round43 complete-output role candidate verified: {target}')
