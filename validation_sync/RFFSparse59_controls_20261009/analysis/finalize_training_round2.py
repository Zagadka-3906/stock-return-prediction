"""Freeze, causally validate, and generate the best round2 optimization candidate."""
from __future__ import annotations

import argparse
import gc
import os
from pathlib import Path
import shutil
import sys
import time

for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[_name] = '8'

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round2 as experiment
from optimize_training_round2 import OUT, PREVIOUS, EXPECTED, YEARS, KEYS, HERE, read, dump, sha, log, verify

CANDIDATE = ROOT/'candidates/optimization_20261003_r2'
OLD = ROOT/'deliveries/connected_topk0175_20261003'


def selected():
    verify()
    result = read(OUT/'selection.json')
    for path,digest in result['frozen_sha256'].items():
        assert sha(ROOT/path) == digest,path
    return result


class ReleaseContext(experiment.Context):
    def promote(self,name):
        if name == 'seed2026':
            return super().promote(name)
        return self.finished(name)


def select():
    import numpy as np
    verify()
    if (OUT/'selection.json').exists():
        selected()
        return
    raw_metadata = list((OUT/'raw').glob('*.json'))
    assert len(raw_metadata) == 40
    for metadata_path in raw_metadata:
        item = read(metadata_path)
        assert sha(metadata_path.with_suffix('.parquet')) == item['prediction_sha256']
        assert sha(OUT/f'models/{item["family"]}_{item["year"]}.txt') == item['model_sha256']
    rows = []
    for wave in (44,45,46):
        r = read(OUT/f'wave{wave}_results.json')
        assert r['status'] == 'complete'
        rows += [{'wave':wave,'arm':name,**v} for name,v in r['results'].items()]
    rows.sort(key=lambda r:(-r['connected_final_score'],len(r['recipe'].get('components',[1])),r['wave'],r['arm']))
    best = rows[0]
    assert best['connected_final_score'] >= EXPECTED
    ctx = experiment.Context()
    pred,_ = ctx.predict(ctx.donor(ctx.finished(best['donor'])),best['slow16_weight'],best['retention'],best['limit_up_delta'])
    metrics = ctx.score(pred)
    assert abs(metrics['final_score']-best['connected_final_score']) < 1e-12
    np.save(OUT/'selected_validation.npy',pred)
    inputs = [Path(__file__),ROOT/'analysis/finalize_optimization.py',OUT/'protocol.json',
              OUT/'refinement_protocol.json',*[OUT/f'wave{wave}_results.json' for wave in (44,45,46)],
              OUT/'selected_validation.npy',OUT/f'promote_{best["donor"]}.npy',ROOT/'active_release.json',
              OUT/'boundary_maturity.json',OUT/'preservation_check.log']
    inputs += raw_metadata
    dump(OUT/'selection.json',{'status':'frozen_before_test_prediction','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'winner':best,'baseline_score':EXPECTED,'score_gain':metrics['final_score']-EXPECTED,
         'scored_records':len(rows),'ranking':rows,'test_labels_read':False,
         'selection_rule':'highest connected2020-2024 official composite; no other research gate',
         'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in inputs}},immutable=True)
    log(f'Round2 selected {best["donor"]}: {metrics["final_score"]:.9f}')


def calibrate():
    # Reuse the previous causal-calibration and prefix checks in memory.
    # The round2 schema records the fixed seed in its protocol; supply that seed
    # to the shared audit reader without altering historical metadata on disk.
    import finalize_optimization as shared
    def audit_read(path):
        record = read(path)
        if 'family' in record and 'training_meta' in record:
            record = {**record,'seed':2026}
        return record
    shared.OUT = OUT
    shared.Context = ReleaseContext
    shared.selected = selected
    shared.read = audit_read
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
    assert read(OUT/'causal_validation.json')['status'] == 'passed'
    if (CANDIDATE/'verification.json').exists():
        assert sha(CANDIDATE/'submission.csv') == read(CANDIDATE/'verification.json')['csv_sha256']
        return
    CANDIDATE.mkdir(parents=True,exist_ok=True)
    winner = record['winner']
    recipe = winner['recipe']
    inputs = pl.read_parquet(OLD/'generation_inputs.parquet').with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    features = read(OLD/'train_test.json')['features']
    test = (pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features)
            .sort('trade_date','ts_code').collect())
    assert test.select(KEYS).equals(inputs.select(KEYS))
    vx = to_matrix(test,features)
    valid = inputs['price_valid'].to_numpy()
    dates = inputs['trade_date'].to_numpy()
    flags = inputs['flag_limit_up'].to_numpy().astype(np.int64)
    codes,unique = pd.factorize(inputs['ts_code'].to_pandas(),sort=True)
    codes = codes.astype(np.int64)
    key = 1-codes/max(len(unique)-1,1)
    aux = inputs['aux_raw'].to_numpy()
    if recipe['type'] == 'model':
        configs = {'selected':{'seed':2026,'fraction':0.175,'rounds':recipe['rounds'],'params':recipe['params']}}
        weights = {'selected':1.0}
    elif recipe['type'] == 'raw_rank_mix':
        configs = {f'{c["seed"]}_{c["fraction"]:.3f}':{**c,'rounds':180,'params':{}} for c in recipe['components']}
        weights = {k:v['weight'] for k,v in configs.items()}
    else:
        configs = {'baseline':{'seed':2026,'fraction':0.175,'rounds':180,'params':{}}}
        weights = {'baseline':1.0}
    model_records = {}
    raw_inputs = {}
    needed = {name:c for name,c in configs.items() if not(c['seed']==2026 and c['fraction']==0.175 and c['rounds']==180 and not c['params'])}
    rt.fold_cutoff = lambda year:20250101
    if needed:
        frame,training_features,training_meta = rt.training_frame(2025)
        assert training_features == features and training_meta['last_date'] == 20241231
        x = to_matrix(frame,features)
        train_dates,labels = frame['trade_date'].to_numpy(),frame['y_ret_1d'].to_numpy()
        del frame
        gc.collect()
        for name,c in needed.items():
            model_path = CANDIDATE/f'model_{name}.txt'
            if not model_path.exists():
                objective = ObjectiveFrac(train_dates,labels,c['seed'],c['fraction'],8)
                ds = lgb.Dataset(x,label=np.zeros(len(x),dtype=np.float32),feature_name=features,free_raw_data=True)
                start = time.monotonic()
                def progress(env):
                    if (env.iteration+1)%30 == 0:
                        log(f'fulltrain {name}: {env.iteration+1}/{c["rounds"]}, {time.monotonic()-start:.0f}s')
                model = lgb.train(dict(rt.PARAMS,**c['params'],seed=c['seed'],objective=rt.objective_callback(objective)),ds,
                                  num_boost_round=c['rounds'],callbacks=[progress])
                assert model.current_iteration() == objective.iteration == c['rounds']
                model_path.write_text(model.model_to_string(),encoding='utf-8')
                original = model.predict(vx,num_threads=8)
                reloaded = lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
                assert np.array_equal(original,reloaded.predict(vx,num_threads=8))
                dump(model_path.with_suffix('.json'),{'config':c,'training_meta':training_meta,'model_sha256':sha(model_path)},immutable=True)
                del ds,objective,model,reloaded,original
                gc.collect()
            model_records[name] = {'path':str(model_path),'sha256':sha(model_path)}
        del x,labels,train_dates
        gc.collect()
    for name,c in configs.items():
        if name not in model_records:
            model_path = OLD/'topk0175_fulltrain.txt'
            model_records[name] = {'path':str(model_path),'sha256':sha(model_path)}
        model = lgb.Booster(model_str=Path(model_records[name]['path']).read_text(encoding='utf-8'))
        raw = model.predict(vx,num_threads=8).astype(np.float64)
        raw[~valid] = -1e6
        raw_inputs[name] = raw
        if name not in needed:
            assert np.array_equal(raw,inputs['topk_raw'].to_numpy())
    def process(raw,alpha,bonus):
        panel = Panel.from_frame(inputs.with_columns(pl.Series('pred_raw',raw)))
        return make_prediction_param(panel,aux,'top_only',0.25,alpha,bonus,True,1)
    def construct(raws):
        if recipe['type'] == 'raw_rank_mix':
            mixed = sum(weights[name]*daily_ranks(raw,valid,dates) for name,raw in raws.items())
            mixed[~valid] = -10.0
        else:
            mixed = raws[next(iter(raws))]
        promote = process(mixed,0.9,0.3)
        promote = np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*key,promote)
        donor,_ = lift(promote,inputs['rank_score'].to_numpy(),inputs.select(['trade_date','flag_limit_up']).to_pandas())
        w5a,slow = process(inputs['w5a_raw'].to_numpy(),0,0),process(inputs['pred_raw'].to_numpy(),0,0)
        rc = {'w5a':daily_ranks(w5a,valid,dates),'slow':daily_ranks(slow,valid,dates)}
        weight = winner['slow16_weight']
        blend = weighted_rank_blend([w5a,slow],[1-weight,weight],rc,valid,dates,('w5a','slow'))
        orderer = np.where(blend>-9,blend+1e-9*key,blend)+1e-9*key
        rank,stats = build_ab(donor,orderer,orderer,dates,flags,codes,len(unique),winner['retention'])
        rank[flags==1] += winner['limit_up_delta']
        return rank,stats
    rank,stats = construct(raw_inputs)
    mapping = read(OUT/'future_return_mapping.json')
    def mapped(rank):
        value = apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),rank))
        assert np.array_equal(pd.Series(rank).groupby(dates).rank().to_numpy(),pd.Series(value).groupby(dates).rank().to_numpy())
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
    replay_inputs = {}
    for name,info in model_records.items():
        model = lgb.Booster(model_str=Path(info['path']).read_text(encoding='utf-8'))
        raw = model.predict(vx,num_threads=8)
        raw[~valid] = -1e6
        assert np.array_equal(raw,raw_inputs[name])
        replay_inputs[name] = raw
    replay,_ = construct(replay_inputs)
    assert np.array_equal(replay,rank)
    assert submission(mapped(replay)).write_csv(float_precision=17).encode('utf-8') == target.read_bytes()
    dump(CANDIDATE/'selection.json',record,immutable=True)
    dump(CANDIDATE/'return_mapping.json',mapping,immutable=True)
    np.save(CANDIDATE/'rank_prediction.npy',rank)
    assert sha(ROOT/'active_release.json') == record['frozen_sha256']['active_release.json']
    dump(CANDIDATE/'verification.json',{'status':'passed','csv_sha256':sha(target),'rows':len(sub),'days':344,'codes':4650,
         'model_reload_bit_identical':True,'csv_replay_byte_identical':True,'csv_ranks_unchanged':True,
         'models':model_records,'validation_score':winner['connected_final_score'],'test_labels_read':False,
         'old_delivery_pointer_unchanged':True,'construction':stats},immutable=True)
    log(f'Round2 candidate verified: {target}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=('select','calibrate','predict'))
    globals()[parser.parse_args().stage]()


if __name__ == '__main__':
    main()
