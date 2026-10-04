"""Frozen standalone model full fit, test-X replay and calibrated candidate CSV."""
from pathlib import Path
import shutil


def predict(record):
    import numpy as np
    import pandas as pd
    import polars as pl
    from run import FEATURE_FILE,to_matrix
    from src.scoring import Panel
    from optimize_wave6 import make_prediction_param
    from return_mapping import apply_mapping,daily_percentile
    import pairwise_model_sources_20261003 as trainer
    from optimize_training_round27 import ROOT,OUT,KEYS,Context,read,dump,sha,log
    candidate=ROOT/'candidates/optimization_20261003_r27';formal=ROOT/'deliveries/connected_topk0175_20261003'
    winner=record['winner'];spec=winner['standalone'];name=spec['model']
    candidate.mkdir(parents=True,exist_ok=True)
    # Final training (including every ensemble child) finishes before opening test feature rows.
    info=trainer.train_one(name,2025);meta=info['training_meta']
    assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
    inputs=pl.read_parquet(formal/'generation_inputs.parquet').with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    features=read(formal/'train_test.json')['features'];assert meta['features']==features
    frame=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features).sort('trade_date','ts_code').collect()
    assert frame.select(KEYS).equals(inputs.select(KEYS));x=to_matrix(frame,features)
    dates=inputs['trade_date'].to_numpy();valid=inputs['price_valid'].to_numpy()
    source_model=trainer.model_path(name,2025);assert sha(source_model)==info['model_sha256']
    raw=trainer.predict_arrays(trainer.load_bundle(source_model),x,dates=dates,valid=valid)
    replay=trainer.predict_arrays(trainer.load_bundle(source_model),x,dates=dates,valid=valid)
    assert np.array_equal(raw,replay) and np.isfinite(raw).all();raw[~valid]=-1e6
    ctx=Context.__new__(Context);ctx.standalone=spec;ctx.standalone_replacement=True;ctx.dates=dates;ctx.valid=valid
    ctx.flags=inputs['flag_limit_up'].to_numpy().astype(np.int64)
    ctx.codes,unique=pd.factorize(inputs['ts_code'].to_pandas(),sort=True);ctx.codes=ctx.codes.astype(np.int64)
    ctx.n_codes=len(unique);ctx.tie_key=1-ctx.codes/max(ctx.n_codes-1,1)
    def construct():
        promote=make_prediction_param(Panel.from_frame(inputs.with_columns(pl.Series('pred_raw',raw))),
                                      inputs['aux_raw'].to_numpy(),**spec['postprocessing'])
        return ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    rank,stats=construct();replay,_=construct();assert np.array_equal(rank,replay)
    mapping=read(OUT/'future_return_mapping.json');mapped=apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),rank))
    assert np.array_equal(pd.Series(rank).groupby(dates).rank().to_numpy(),pd.Series(mapped).groupby(dates).rank().to_numpy())
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    sub=inputs.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    target=candidate/'submission.csv';sub.write_csv(target,float_precision=17);parsed=pd.read_csv(target)
    assert len(parsed)==1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any() and np.isfinite(parsed.pred).all()
    assert np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    assert sub.write_csv(float_precision=17).encode('utf-8')==target.read_bytes()
    model=candidate/f'model_standalone_{name}.joblib';shutil.copyfile(source_model,model);assert sha(model)==info['model_sha256']
    np.save(candidate/'rank_prediction.npy',rank)
    dump(candidate/'selection.json',record,immutable=True);dump(candidate/'return_mapping.json',mapping,immutable=True)
    dump(candidate/'verification.json',{'status':'passed','csv_sha256':sha(target),'rows':len(sub),'days':344,'codes':4650,
         'models':{'standalone_'+name:{'path':str(model),'sha256':sha(model),'training_info':info,'reload_bit_identical':True,'original':str(source_model)}},
         'model_reload_bit_identical':True,'pipeline_replay_bit_identical':True,'csv_replay_byte_identical':True,
         'csv_ranks_unchanged':True,'validation_score':winner['connected_final_score'],'test_labels_read':False,
         'complete_standalone_model':True,'standalone':spec,'previous_model_predictions_used':False,'construction':stats,
         'source_predictions_sha256':{},'pruned_member_excluded':True,
         'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']},immutable=True)
    log(f'Round27 standalone candidate verified: {target}')
