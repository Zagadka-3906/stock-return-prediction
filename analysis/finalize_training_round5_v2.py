"""Freeze the round5 winner, verify causal calibration, and generate test-X CSV."""
from __future__ import annotations

import argparse
import gc
import os
from pathlib import Path
import sys
import time

for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[_name] = '8'
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round5 as experiment
from optimize_training_round5 import OUT, PREVIOUS, EXPECTED, YEARS, KEYS, HERE, BASE_POST, read, dump, sha, log, verify

CANDIDATE = ROOT/'candidates/optimization_20261003_r5'
OLD = ROOT/'deliveries/connected_topk0175_20261003'
OLD90 = ROOT/'candidates/optimization_20261003_r2'


def selected():
    verify()
    assert sha(Path(__file__))==read(OUT/'release_amendment.json')['corrected_finalizer_sha256']
    record = read(OUT/'selection.json')
    for path,digest in record['frozen_sha256'].items():
        assert sha(ROOT/path) == digest,path
    return record


class ReleaseContext(experiment.Context):
    def promote(self,name):
        return self.finished(name)


def select():
    import numpy as np
    verify()
    assert sha(Path(__file__))==read(OUT/'release_amendment.json')['corrected_finalizer_sha256']
    if (OUT/'selection.json').exists():
        selected()
        return
    metadata_files = list((OUT/'raw').glob('*.json'))
    assert len(metadata_files)==40
    for path in metadata_files:
        item = read(path)
        assert sha(item['source_prediction'])==item['prediction_sha256']
        assert sha(item['source_model'])==item['model_sha256']
    rows = []
    for wave in (53,54,55):
        record = read(OUT/f'wave{wave}_results.json')
        assert record['status']=='complete'
        rows += [{'wave':wave,'arm':name,**value} for name,value in record['results'].items()]
    def key(row):
        components = row['recipe'].get('components',[row['recipe']])
        return (-row['connected_final_score'],len(components),sum(c['rounds'] for c in components),row['wave'],row['arm'])
    rows.sort(key=key)
    assert len(rows)==44
    best = rows[0]
    assert best['connected_final_score']>=EXPECTED
    ctx = experiment.Context()
    pred,_ = ctx.predict(ctx.donor(ctx.finished(best['donor'],best['recipe'])),best['slow16_weight'],
                         best['retention'],best['limit_up_delta'])
    metrics = ctx.score(pred)
    assert abs(metrics['final_score']-best['connected_final_score'])<1e-12
    np.save(OUT/'selected_validation.npy',pred)
    inputs = [Path(__file__),ROOT/'analysis/finalize_optimization.py',OUT/'protocol.json',
              OUT/'fine_mix_protocol.json',OUT/'refinement_protocol.json',OUT/'release_amendment.json',
              *[OUT/f'wave{wave}_results.json' for wave in (53,54,55)],
              OUT/'selected_validation.npy',OUT/f'promote_{best["donor"]}.npy',ROOT/'active_release.json',
              OLD/'generation_inputs.parquet',OLD/'train_test.json',OLD/'topk0175_fulltrain.txt',
              OLD90/'model_selected.txt',OLD90/'model_selected.json',*metadata_files]
    dump(OUT/'selection.json',{'status':'frozen_before_test_prediction',
         'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'winner':best,'baseline_score':EXPECTED,
         'score_gain':metrics['final_score']-EXPECTED,'scored_records':len(rows),'ranking':rows,
         'selection_rule':'highest connected2020-2024 official composite; exact ties prefer fewer models and fewer trees',
         'test_labels_read':False,'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in inputs}},immutable=True)
    log(f'Round5 selected {best["donor"]}: {metrics["final_score"]:.9f}')


def calibrate():
    import finalize_optimization as shared
    shared.OUT = OUT
    shared.Context = ReleaseContext
    shared.selected = selected
    shared.read = read
    shared.calibrate()


def predict():
    import numpy as np
    import pandas as pd
    import polars as pl
    import lightgbm as lgb
    import experiments.r6_topk as rt
    from optimize_wave31 import ObjectiveFrac
    from optimize_wave6 import make_prediction_param
    from optimize_wave13 import build_ab
    from optimize_wave15 import daily_ranks,weighted_rank_blend
    from optimize_wave18 import lift
    from src.scoring import Panel
    from return_mapping import apply_mapping,daily_percentile
    from run import FEATURE_FILE,to_matrix
    record = selected()
    assert read(OUT/'causal_validation.json')['status']=='passed'
    if (CANDIDATE/'verification.json').exists():
        assert sha(CANDIDATE/'submission.csv')==read(CANDIDATE/'verification.json')['csv_sha256']
        return
    CANDIDATE.mkdir(parents=True,exist_ok=True)
    winner = record['winner']
    recipe = winner['recipe']
    post = recipe.get('postprocessing',BASE_POST)
    inputs = pl.read_parquet(OLD/'generation_inputs.parquet').with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    features = read(OLD/'train_test.json')['features']
    test = (pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features)
            .sort('trade_date','ts_code').collect())
    assert test.select(KEYS).equals(inputs.select(KEYS))
    vx = to_matrix(test,features)
    valid,dates = inputs['price_valid'].to_numpy(),inputs['trade_date'].to_numpy()
    flags = inputs['flag_limit_up'].to_numpy().astype(np.int64)
    codes,unique = pd.factorize(inputs['ts_code'].to_pandas(),sort=True)
    codes = codes.astype(np.int64)
    tie = 1-codes/max(len(unique)-1,1)
    aux = inputs['aux_raw'].to_numpy()
    components = recipe['components'] if recipe['type']=='raw_rank_mix' else [dict(recipe,weight=1.0)]
    configs = {f'seed{c["seed"]}_f{c["fraction"]:.3f}_r{c["rounds"]}':c for c in components}
    needed = {name:c for name,c in configs.items() if not(c['seed']==2026 and c['fraction']==0.175 and c['rounds']<=180 and not c['params'])}
    rt.fold_cutoff = lambda year:20250101
    training_meta = read(OLD/'train_test.json')['training']
    if needed:
        frame,training_features,training_meta = rt.training_frame(2025)
        assert training_features==features and training_meta==read(OLD/'train_test.json')['training']
        x = to_matrix(frame,features)
        train_dates,labels = frame['trade_date'].to_numpy(),frame['y_ret_1d'].to_numpy()
        del frame
        gc.collect()
    models = {}
    for name,c in configs.items():
        path = CANDIDATE/f'model_{name}.txt'
        if not path.exists():
            if name not in needed:
                source = OLD/'topk0175_fulltrain.txt'
                model = lgb.Booster(model_str=source.read_text(encoding='utf-8'))
                assert model.current_iteration()==180
                original = model.predict(vx,num_iteration=c['rounds'],num_threads=8)
                reference90 = lgb.Booster(model_str=(OLD90/'model_selected.txt').read_text(encoding='utf-8'))
                assert np.array_equal(model.predict(vx,num_iteration=90,num_threads=8),reference90.predict(vx,num_threads=8))
                source_record = {'method':'reuse independently verified full-training tree prefix',
                                 'source_model':str(source),'source_sha256':sha(source),
                                 'prefix90_matches_separately_trained90_bit_identically':True}
                del reference90
            else:
                objective = ObjectiveFrac(train_dates,labels,c['seed'],c['fraction'],c.get('samples',8))
                ds = lgb.Dataset(x,label=np.zeros(len(x),dtype=np.float32),feature_name=features,free_raw_data=True)
                start = time.monotonic()
                def progress(env):
                    if (env.iteration+1)%30==0:
                        log(f'fulltrain {name}: {env.iteration+1}/{c["rounds"]}, {time.monotonic()-start:.0f}s')
                model = lgb.train(dict(rt.PARAMS,**c['params'],seed=c['seed'],objective=rt.objective_callback(objective)),
                                  ds,num_boost_round=c['rounds'],callbacks=[progress])
                assert model.current_iteration()==objective.iteration==c['rounds']
                original = model.predict(vx,num_threads=8)
                source_record = {'method':'fit selected configuration on all mature historical training labels'}
                del objective,ds
            path.write_text(model.model_to_string(num_iteration=c['rounds']),encoding='utf-8')
            replay = lgb.Booster(model_str=path.read_text(encoding='utf-8'))
            assert replay.current_iteration()==c['rounds']
            assert np.array_equal(original,replay.predict(vx,num_threads=8))
            dump(path.with_suffix('.json'),{'config':c,'training_meta':training_meta,'provenance':source_record,
                 'model_sha256':sha(path),'reload_bit_identical':True},immutable=True)
            del model,replay,original
            gc.collect()
        metadata = read(path.with_suffix('.json'))
        assert metadata['model_sha256']==sha(path) and metadata['config']==c
        models[name] = {'path':str(path),'sha256':sha(path),'rounds':c['rounds'],
                        'provenance':metadata['provenance']}
    if needed:
        del x,labels,train_dates
        gc.collect()
    raw_inputs = {}
    for name,info in models.items():
        model = lgb.Booster(model_str=Path(info['path']).read_text(encoding='utf-8'))
        raw = model.predict(vx,num_threads=8)
        raw[~valid] = -1e6
        raw_inputs[name] = raw
    def process(raw,settings):
        panel = Panel.from_frame(inputs.with_columns(pl.Series('pred_raw',raw)))
        return make_prediction_param(panel,aux,**settings)
    def construct(raws):
        if recipe['type']=='raw_rank_mix':
            mixed = sum(configs[name]['weight']*daily_ranks(raw,valid,dates) for name,raw in raws.items())
            mixed[~valid] = -10.0
        else:
            mixed = raws[next(iter(raws))]
        promote = process(mixed,post)
        promote = np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*tie,promote)
        donor,_ = lift(promote,inputs['rank_score'].to_numpy(),inputs.select(['trade_date','flag_limit_up']).to_pandas())
        order_settings = dict(BASE_POST,alpha=0,bonus=0)
        w5a,slow = process(inputs['w5a_raw'].to_numpy(),order_settings),process(inputs['pred_raw'].to_numpy(),order_settings)
        ranks = {'w5a':daily_ranks(w5a,valid,dates),'slow':daily_ranks(slow,valid,dates)}
        weight = winner['slow16_weight']
        blend = weighted_rank_blend([w5a,slow],[1-weight,weight],ranks,valid,dates,('w5a','slow'))
        orderer = np.where(blend>-9,blend+1e-9*tie,blend)+1e-9*tie
        rank,stats = build_ab(donor,orderer,orderer,dates,flags,codes,len(unique),winner['retention'])
        rank[flags==1] += winner['limit_up_delta']
        return rank,stats
    rank,stats = construct(raw_inputs)
    mapping = read(OUT/'future_return_mapping.json')
    def mapped(raw):
        value = apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),raw))
        assert np.array_equal(pd.Series(raw).groupby(dates).rank().to_numpy(),pd.Series(value).groupby(dates).rank().to_numpy())
        return value
    bridge = pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    def submission(value):
        return inputs.select(KEYS).with_columns(pl.Series('pred',value)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    sub = submission(mapped(rank))
    target = CANDIDATE/'submission.csv'
    sub.write_csv(target,float_precision=17)
    parsed = pd.read_csv(target)
    assert len(parsed)==1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any()
    assert np.isfinite(parsed.pred).all() and np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    replay_raw = {}
    for name,info in models.items():
        model = lgb.Booster(model_str=Path(info['path']).read_text(encoding='utf-8'))
        raw = model.predict(vx,num_threads=8)
        raw[~valid] = -1e6
        assert np.array_equal(raw,raw_inputs[name])
        replay_raw[name] = raw
    replay,_ = construct(replay_raw)
    assert np.array_equal(rank,replay)
    assert submission(mapped(replay)).write_csv(float_precision=17).encode('utf-8')==target.read_bytes()
    dump(CANDIDATE/'selection.json',record,immutable=True)
    dump(CANDIDATE/'return_mapping.json',mapping,immutable=True)
    np.save(CANDIDATE/'rank_prediction.npy',rank)
    assert sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']
    dump(CANDIDATE/'verification.json',{'status':'passed','csv_sha256':sha(target),'rows':len(sub),'days':344,'codes':4650,
         'model_reload_bit_identical':True,'csv_replay_byte_identical':True,'csv_ranks_unchanged':True,
         'models':models,'validation_score':winner['connected_final_score'],'test_labels_read':False,
         'old_delivery_pointer_unchanged':True,'construction':stats},immutable=True)
    log(f'Round5 candidate verified: {target}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=('select','calibrate','predict'))
    globals()[parser.parse_args().stage]()


if __name__=='__main__':
    main()
