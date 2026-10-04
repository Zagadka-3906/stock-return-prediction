"""Freeze the validation winner, verify causal calibration, and make test-X predictions.

Never import or open test Y. Historical delivery files and their pointers stay
unchanged; this is an optimization candidate, with its own reproducible CSV.
"""
from __future__ import annotations

import argparse
import gc
import json
import os
from pathlib import Path
import sys
import time

for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[_name] = '8'

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis'), str(ROOT/'analysis/connected_validation_20261002')]
from continue_optimization import OUT, HERE, YEARS, KEYS, EXPECTED, Context, read, dump, sha, log, verify_protocol

CANDIDATE = ROOT/'candidates/optimization_20261003'
OLD = ROOT/'deliveries/connected_topk0175_20261003'


def selected():
    verify_protocol()
    for path,digest in read(OUT/'fraction_mix_protocol.json')['input_sha256'].items():
        assert sha(ROOT/path) == digest, path
    record = read(OUT/'selection.json')
    assert record['source_sha256'] == sha(Path(__file__))
    for path,digest in record['frozen_sha256'].items():
        assert sha(ROOT/path) == digest, path
    return record


def select():
    import numpy as np
    verify_protocol()
    if (OUT/'selection.json').exists():
        selected()
        return
    rows = []
    for wave in (40,41,42,43):
        records = read(OUT/f'wave{wave}_results.json')
        assert records['status'] == 'complete'
        rows += [{'wave':wave, 'arm':name, **item} for name,item in records['results'].items()]
    rows.sort(key=lambda r:(-r['connected_final_score'], len(r.get('fraction_components',r.get('seed_weights',{2026:1}))), r['wave'], r['arm']))
    winner = rows[0]
    assert winner['connected_final_score'] >= EXPECTED
    ctx = Context()
    pred,stats = ctx.predict(ctx.donor(ctx.promote(winner['donor'])), winner['slow16_weight'],
                             winner['retention'], winner['limit_up_delta'])
    metrics = ctx.score(pred)
    assert abs(metrics['final_score']-winner['connected_final_score']) < 1e-12
    np.save(OUT/'selected_validation.npy', pred)
    paths = [OUT/'protocol.json', OUT/'model_comparison_parameters.json', OUT/'refinement_protocol.json',
             *[OUT/f'wave{wave}_results.json' for wave in (40,41,42,43)],OUT/'fraction_mix_protocol.json',
             OUT/'selected_validation.npy', OUT/f'promote_{winner["donor"]}.npy', ROOT/'active_release.json']
    paths += list((OUT/'raw').glob('*.json'))
    record = {'status':'frozen_before_test_X_prediction', 'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
              'winner':winner, 'baseline_score':EXPECTED, 'score_gain':metrics['final_score']-EXPECTED,
              'new_scored_records':len(rows), 'ranking':rows,
              'selection_rule':'highest compliant connected2020-2024 official composite; exact ties prefer fewer seeds',
              'test_labels_read':False, 'source_sha256':sha(Path(__file__)),
              'old_delivery_preserved':True, 'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in paths}}
    dump(OUT/'selection.json', record, immutable=True)
    log(f'Selected and frozen: {winner["arm"]}, score={metrics["final_score"]:.9f}')


def calibrate():
    from copy import copy
    import numpy as np
    import pandas as pd
    import polars as pl
    from run import fold_cutoff
    from return_mapping import fit_mapping, apply_mapping, daily_percentile
    from experiments.revalidate_fold_local import score_official
    record = selected()
    if (OUT/'causal_validation.json').exists():
        assert sha(OUT/'calibrated_validation.csv') == read(OUT/'causal_validation.json')['csv_sha256']
        return
    ctx = Context()
    pred = np.load(OUT/'selected_validation.npy')
    winner = record['winner']
    promote = ctx.promote(winner['donor'])
    prefixes = []
    unique_dates = np.unique(ctx.dates)
    for day_count in (80, 260, 975):
        last = int(unique_dates[day_count-1])
        n = int(np.searchsorted(ctx.dates,last,side='right'))
        prefix = copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):
            setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.pdf = ctx.pdf.iloc[:n]
        prefix.ranks = {key:value[:n] for key,value in ctx.ranks.items()}
        replay,_ = prefix.predict(prefix.donor(promote[:n]),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
        assert np.array_equal(replay,pred[:n]), f'Future data affected the prefix ending{last}'
        prefixes.append({'through_date':last,'days':day_count,'bit_identical':True})
    training_proofs = []
    for metadata_path in (OUT/'raw').glob('*.json'):
        item = read(metadata_path)
        meta = item['training_meta']
        original = read(HERE/f'wave36_topk/raw/info_f0.175_{item["year"]}.json')['training_meta']
        assert meta == original, f'New seed training rows or original Float64 labels differ: {metadata_path}'
        training_proofs.append({'year':item['year'],'seed':item['seed'],'same_training_keys_and_labels':True,
                                'last_label_date':meta['last_date'],'exclusive_cutoff':meta['training_cutoff_exclusive']})
    pct = daily_percentile(ctx.frame.select('trade_date').to_pandas(), pred)
    y = ctx.frame['y_ret_1d'].to_numpy().astype(np.float64)
    mapped = np.empty_like(pred)
    boundaries = {}
    for year in YEARS:
        mask = ctx.dates//10000 == year
        cutoff = fold_cutoff(year)
        history = (ctx.dates < cutoff) & np.isfinite(y)
        if history.any():
            mapping = fit_mapping(pct[history], y[history])
            mapped[mask] = apply_mapping(mapping, pct[mask])
            source_last = int(ctx.dates[history].max())
            method = 'isotonic trained only on earlier OOF folds and mature labels'
        else:
            labels = (pl.scan_csv(ROOT/'data/raw/训练集.csv', schema_overrides={'trade_date':pl.Int32,'y_ret_1d':pl.Float64},
                                  null_values=['NaN','nan','']).filter((pl.col('trade_date')<cutoff)&pl.col('y_ret_1d').is_finite())
                      .select(['trade_date','y_ret_1d']).collect())
            mean = float(labels['y_ret_1d'].mean())
            scale = float(labels['y_ret_1d'].std())
            assert np.isfinite(mean) and np.isfinite(scale) and scale > 0
            mapped[mask] = mean+0.1*scale*(pct[mask]-0.5)
            mapping = {'type':'affine_training_moments_fallback', 'mean':mean, 'scale':0.1*scale,
                       'rows':len(labels), 'conditional_return_calibration':False}
            source_last = int(labels['trade_date'].max())
            method = 'first-fold distribution-based affine fallback from pre2020 training labels; not fitted conditional mean'
        assert source_last < cutoff < int(ctx.dates[mask].min())
        before = pd.Series(pred[mask]).groupby(ctx.dates[mask]).rank(method='average').to_numpy()
        after = pd.Series(mapped[mask]).groupby(ctx.dates[mask]).rank(method='average').to_numpy()
        assert np.array_equal(before,after), f'Calibration changed ranks in{year}'
        dump(OUT/f'causal_mapping_{year}.json',mapping,immutable=True)
        boundaries[str(year)] = {'mapping_last_label_date':source_last,'exclusive_cutoff':cutoff,
                                'validation_first_date':int(ctx.dates[mask].min()),'method':method,'ranks_identical':True}
    metrics,daily = score_official(ctx.frame,mapped)
    assert abs(metrics['final_score']-record['winner']['connected_final_score']) < 1e-12
    ctx.frame.select(KEYS).with_columns(pl.Series('pred',mapped)).write_csv(OUT/'calibrated_validation.csv',float_precision=17)
    daily.write_csv(OUT/'selected_validation_daily.csv')
    final_map = fit_mapping(pct,y)
    dump(OUT/'future_return_mapping.json',final_map,immutable=True)
    dump(OUT/'causal_validation.json',{'status':'passed','metrics':metrics,'rows':len(ctx.frame),'days':1212,
         'fold_calibration_boundaries':boundaries,'year_boundary_turnover_included':True,'test_labels_read':False,
         'future_append_prefix_invariance':prefixes,'new_model_training_boundary_proofs':training_proofs,
         'csv_sha256':sha(OUT/'calibrated_validation.csv'),'final_map_sha256':sha(OUT/'future_return_mapping.json')},immutable=True)
    log(f'Causal calibration and independent official scoring passed: {metrics["final_score"]:.9f}')


def predict():
    import numpy as np
    import pandas as pd
    import polars as pl
    import lightgbm as lgb
    import experiments.r6_topk as rt
    from optimize_wave31 import ObjectiveFrac
    from optimize_wave6 import make_prediction_param
    from optimize_wave13 import build_ab
    from optimize_wave15 import daily_ranks, weighted_rank_blend
    from optimize_wave18 import lift
    from src.scoring import Panel
    from return_mapping import apply_mapping, daily_percentile
    from run import to_matrix, FEATURE_FILE
    record = selected()
    audit = read(OUT/'causal_validation.json')
    assert audit['status'] == 'passed'
    winner = record['winner']
    if (CANDIDATE/'verification.json').exists():
        assert sha(CANDIDATE/'submission.csv') == read(CANDIDATE/'verification.json')['csv_sha256']
        return
    CANDIDATE.mkdir(parents=True,exist_ok=True)
    components = winner.get('fraction_components',[
        {'seed':int(k),'fraction':0.175,'weight':float(v)} for k,v in winner.get('seed_weights',{'2026':1.0}).items()])
    configs = {f'{int(c["seed"])}_{c["fraction"]:.3f}':c for c in components}
    weights = {key:float(c['weight']) for key,c in configs.items()}
    label_free = pl.read_parquet(OLD/'generation_inputs.parquet').with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    meta = read(OLD/'train_test.json')
    feature = pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+meta['features']).sort('trade_date','ts_code').collect()
    assert feature.select(KEYS).equals(label_free.select(KEYS))
    vx = to_matrix(feature,meta['features'])
    valid = label_free['price_valid'].to_numpy()
    raw_by_seed = {'2026_0.175':label_free['topk_raw'].to_numpy()}
    model_records = {'2026_0.175':{'path':str(OLD/'topk0175_fulltrain.txt'),'sha256':sha(OLD/'topk0175_fulltrain.txt')}}
    # Final training precedes first test inference for new models. Labels through2024 mature by
    # the first prediction, made after the close of2025-01-02, as in the previous release.
    rt.fold_cutoff = lambda year:20250101
    if any(key != '2026_0.175' for key in weights):
        frame,features,training_meta = rt.training_frame(2025)
        assert training_meta['last_date'] == 20241231
        dates,labels = frame['trade_date'].to_numpy(),frame['y_ret_1d'].to_numpy()
        x = to_matrix(frame,features)
        del frame
        gc.collect()
        for key in weights:
            if key == '2026_0.175':
                continue
            seed,frac = int(configs[key]['seed']),float(configs[key]['fraction'])
            model_path = CANDIDATE/f'topk_seed{seed}_f{frac:.3f}_fulltrain.txt'
            if not model_path.exists():
                objective = ObjectiveFrac(dates,labels,seed,frac,8)
                ds = lgb.Dataset(x,label=np.zeros(len(x),dtype=np.float32),feature_name=features,free_raw_data=True)
                start = time.monotonic()
                def progress(env):
                    if (env.iteration+1)%30 == 0:
                        log(f'fulltrain seed{seed}: {env.iteration+1}/180, {time.monotonic()-start:.0f}s')
                model = lgb.train(dict(rt.PARAMS,seed=seed,objective=rt.objective_callback(objective)),ds,
                                  num_boost_round=180,callbacks=[progress])
                assert model.current_iteration() == objective.iteration == 180
                model_path.write_text(model.model_to_string(),encoding='utf-8')
                dump(model_path.with_suffix('.json'),{'seed':seed,'fraction':frac,'training_meta':training_meta,'model_sha256':sha(model_path)},immutable=True)
                raw = model.predict(vx,num_threads=8)
                reloaded = lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
                assert np.array_equal(raw,reloaded.predict(vx,num_threads=8))
                del ds,objective,model,reloaded
                gc.collect()
            reloaded = lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
            raw = reloaded.predict(vx,num_threads=8).astype(np.float64)
            raw[~valid] = -1e6
            raw_by_seed[key] = raw
            np.save(CANDIDATE/f'raw_test_{key}.npy',raw)
            model_records[key] = {'path':str(model_path),'sha256':sha(model_path),'reload_exact':True}
        del x,dates,labels
        gc.collect()
    ar = label_free['aux_raw'].to_numpy()
    test_dates = label_free['trade_date'].to_numpy()
    flags = label_free['flag_limit_up'].to_numpy().astype(np.int64)
    codes,unique = pd.factorize(label_free['ts_code'].to_pandas(),sort=True)
    codes = codes.astype(np.int64)
    key = 1-codes/max(len(unique)-1,1)
    def processed(raw,alpha,bonus):
        panel = Panel.from_frame(label_free.with_columns(pl.Series('pred_raw',raw)))
        return make_prediction_param(panel,ar,'top_only',0.25,alpha,bonus,True,1)
    def construct(raws):
        seeds = {seed:processed(raws[seed],0.9,0.3) for seed in weights}
        if len(weights) == 1:
            promote = seeds[next(iter(weights))]
        else:
            promote = sum(weight*daily_ranks(seeds[seed],valid,test_dates) for seed,weight in weights.items())
            promote[~valid] = -10.0
        promote = np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*key,promote)
        donor,_ = lift(promote,label_free['rank_score'].to_numpy(),label_free.select(['trade_date','flag_limit_up']).to_pandas())
        w5a = processed(label_free['w5a_raw'].to_numpy(),0,0)
        slow = processed(label_free['pred_raw'].to_numpy(),0,0)
        rc = {'w5a':daily_ranks(w5a,valid,test_dates),'slow':daily_ranks(slow,valid,test_dates)}
        weight = winner['slow16_weight']
        blend = weighted_rank_blend([w5a,slow],[1-weight,weight],rc,valid,test_dates,('w5a','slow'))
        orderer = np.where(blend>-9,blend+1e-9*key,blend)+1e-9*key
        pred,stats = build_ab(donor,orderer,orderer,test_dates,flags,codes,len(unique),winner['retention'])
        pred[flags == 1] += winner['limit_up_delta']
        return pred,stats
    pred,stats = construct(raw_by_seed)
    mapping = read(OUT/'future_return_mapping.json')
    mapped = apply_mapping(mapping,daily_percentile(label_free.select('trade_date').to_pandas(),pred))
    assert np.array_equal(pd.Series(pred).groupby(test_dates).rank().to_numpy(),pd.Series(mapped).groupby(test_dates).rank().to_numpy())
    bridge = pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    def submission(values):
        return label_free.select(KEYS).with_columns(pl.Series('pred',values)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    sub = submission(mapped)
    target = CANDIDATE/'submission.csv'
    sub.write_csv(target,float_precision=17)
    parsed = pd.read_csv(target)
    assert len(parsed) == 1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any()
    assert np.isfinite(parsed.pred).all() and np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    # Independent saved-model reload, then a full postprocessing replay to the exact CSV bytes.
    replay_raw = {}
    for seed in weights:
        model = lgb.Booster(model_str=Path(model_records[seed]['path']).read_text(encoding='utf-8'))
        raw = model.predict(vx,num_threads=8)
        raw[~valid] = -1e6
        assert np.array_equal(raw,raw_by_seed[seed])
        replay_raw[seed] = raw
    replay,_ = construct(replay_raw)
    assert np.array_equal(pred,replay)
    rebuilt = submission(apply_mapping(mapping,daily_percentile(label_free.select('trade_date').to_pandas(),replay))).write_csv(float_precision=17).encode('utf-8')
    assert target.read_bytes() == rebuilt
    dump(CANDIDATE/'selection.json',record,immutable=True)
    dump(CANDIDATE/'return_mapping.json',mapping,immutable=True)
    np.save(CANDIDATE/'rank_prediction.npy',pred)
    dump(CANDIDATE/'verification.json',{'status':'passed','rows':len(sub),'days':344,'codes':4650,
         'csv_sha256':sha(target),'validation_score':winner['connected_final_score'],'baseline_score':EXPECTED,
         'test_labels_read':False,'csv_replay_byte_identical':True,'model_reload_bit_identical':True,
         'csv_ranks_unchanged':True,'models':model_records,'construction':stats,
         'selection_frozen_before_test_prediction':True,'label_free_inputs_sha256':sha(OLD/'generation_inputs.parquet'),
         'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json') == record['frozen_sha256']['active_release.json']},immutable=True)
    log(f'Candidate CSV saved and byte-exact replay passed: {target}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=('select','calibrate','predict'))
    args = parser.parse_args()
    globals()[args.stage]()


if __name__ == '__main__':
    main()
