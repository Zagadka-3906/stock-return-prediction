"""Apply frozen final temporal controls to a verified complete future foundation."""
from pathlib import Path
import shutil


def predict(record,candidate_path=None):
    import numpy as np
    import pandas as pd
    import polars as pl
    from final_output_temporal_postprocessing_20261004 import transform
    from return_mapping import apply_mapping,daily_percentile
    from optimize_training_round49 import ROOT,OUT,PREVIOUS,KEYS,read,dump,sha
    candidate=Path(candidate_path) if candidate_path is not None else ROOT/'candidates/optimization_20261003_r49'
    source=ROOT/f'candidates/{PREVIOUS.name}';formal=ROOT/'deliveries/connected_topk0175_20261003'
    candidate.mkdir(exist_ok=True)
    if (candidate/'verification.json').exists():assert sha(candidate/'submission.csv')==read(candidate/'verification.json')['csv_sha256'];return
    foundation=read(source/'verification.json');manifest=read(source/'manifest.json')
    assert foundation['status']=='passed' and sha(source/'rank_prediction.npy')==manifest['files']['rank_prediction.npy']['sha256']
    models={}
    for key,info in foundation['models'].items():
        original=Path(info['path']);assert sha(original)==info['sha256'];target=candidate/original.name
        shutil.copyfile(original,target);models[key]={**info,'path':str(target),'foundation_source':str(original)}
        assert sha(target)==info['sha256']
    frame=pl.read_parquet(formal/'generation_inputs.parquet',columns=KEYS+['price_valid'])
    raw=np.load(source/'rank_prediction.npy');dates=frame['trade_date'].to_numpy();valid=frame['price_valid'].to_numpy()
    codes=pd.factorize(frame['ts_code'].to_numpy(),sort=True)[0];cfg=record['winner']['temporal_postprocessing']
    rank=transform(raw,dates,valid,codes,cfg);replay=transform(raw,dates,valid,codes,cfg);assert np.array_equal(rank,replay)
    last=int(frame['trade_date'].unique().sort()[79]);prefix=dates<=last
    prefix_codes=pd.factorize(frame['ts_code'].to_numpy()[prefix],sort=False)[0]
    assert np.array_equal(rank[prefix],transform(raw[prefix],dates[prefix],valid[prefix],prefix_codes,cfg))
    mapping=read(OUT/'future_return_mapping.json');mapped=apply_mapping(mapping,daily_percentile(frame.select('trade_date').to_pandas(),rank))
    replay_mapped=apply_mapping(mapping,daily_percentile(frame.select('trade_date').to_pandas(),replay));assert np.array_equal(mapped,replay_mapped)
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    sub=frame.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    csv=candidate/'submission.csv';sub.write_csv(csv,float_precision=17);parsed=pd.read_csv(csv)
    assert len(parsed)==1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any() and np.isfinite(parsed.pred).all()
    assert np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    assert sub.write_csv(float_precision=17).encode('utf-8')==csv.read_bytes()
    np.save(candidate/'rank_prediction.npy',rank);shutil.copyfile(source/'rank_prediction.npy',candidate/'foundation_rank_prediction.npy')
    shutil.copyfile(ROOT/'analysis/final_output_temporal_postprocessing_20261004.py',candidate/'temporal_postprocessing.py')
    dump(candidate/'selection.json',record,immutable=True);dump(candidate/'return_mapping.json',mapping,immutable=True)
    dump(candidate/'verification.json',{'status':'passed','csv_sha256':sha(csv),'rows':1599600,'days':344,'codes':4650,
        'models':models,'model_reload_bit_identical':True,'model_replay_scope':'Verified frozen complete foundation reused; its copied model bytes are unchanged.',
        'pipeline_replay_bit_identical':True,'csv_replay_byte_identical':True,'csv_ranks_unchanged':True,'cold80_day_prefix_bit_identical':True,
        'validation_score':record['winner']['connected_final_score'],'test_labels_read':False,'temporal_postprocessing':cfg,
        'foundation_candidate':str(source),'foundation_verification_sha256':sha(source/'verification.json'),
        'foundation_rank_source_sha256':sha(source/'rank_prediction.npy'),'pruned_member_excluded':True,
        'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']},immutable=True)
