"""Waves44-46: raw-before-smoothing mixtures and Top-K model capacity/learning curves.

Training-only connected official scoring. Two disjoint worker groups may train
independently; no test labels or test-price-derived targets are read.
"""
from __future__ import annotations

import argparse
import gc
import itertools
import os
from pathlib import Path
import sys
import time

for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[_name] = '8'

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
from continue_optimization import Context as PreviousContext, HERE, YEARS, KEYS, read, dump, sha, log
from continue_optimization import verify_protocol as verify_previous_protocol

OUT = ROOT/'analysis/optimization_20261003_r2'
PREVIOUS = ROOT/'analysis/optimization_20261003'
EXPECTED = 0.4459608624088246
CONFIGS = {
    'round_curve31': {'params':{},'checkpoints':[90,180,270]},
    'slow_lr31': {'params':{'learning_rate':0.025},'checkpoints':[180,360]},
    'leaves63': {'params':{'num_leaves':63},'checkpoints':[90,180]},
    'regularized31': {'params':{'min_data_in_leaf':600,'lambda_l2':20.0},'checkpoints':[180]},
}
GROUPS = {'A':('round_curve31','leaves63'),'B':('slow_lr31','regularized31')}
RAW_MIXES = {
    'raw_seed2026_2027_equal': [(2026,0.175,0.5),(2027,0.175,0.5)],
    'raw_seed2026_2028_equal': [(2026,0.175,0.5),(2028,0.175,0.5)],
    'raw_all3_equal': [(2026,0.175,1/3),(2027,0.175,1/3),(2028,0.175,1/3)],
    'raw_frac0175_020_w025': [(2026,0.175,0.75),(2026,0.20,0.25)],
    'raw_frac0175_020_w050': [(2026,0.175,0.5),(2026,0.20,0.5)],
    'raw_frac0175_015_w025': [(2026,0.175,0.75),(2026,0.15,0.25)],
    'raw_frac0175_025_w025': [(2026,0.175,0.75),(2026,0.25,0.25)],
}


def cached_raw(seed,frac,year):
    if frac == 0.175:
        return (HERE/f'wave36_topk/raw/topk_seed2026_f0.175_{year}.parquet' if seed == 2026
                else PREVIOUS/f'raw/topk_seed{seed}_{year}.parquet')
    return HERE/f'wave31_topk/raw/topk_seed{seed}_f{frac:.2f}_{year}.parquet'


def verify():
    record = read(OUT/'protocol.json')
    for name,digest in record['input_sha256'].items():
        assert sha(ROOT/name) == digest, name
    return record


def freeze():
    verify_previous_protocol()
    if (OUT/'protocol.json').exists():
        verify()
        return
    sources = [Path(__file__),ROOT/'analysis/continue_optimization.py',ROOT/'后续选模标准.md',
               ROOT/'run.py',ROOT/'evaluate.py',ROOT/'experiments/r6_topk.py',
               HERE/'optimize_wave31.py',HERE/'optimize_wave6.py',HERE/'optimize_wave13.py',
               HERE/'optimize_wave15.py',HERE/'optimize_wave18.py',HERE/'return_mapping.py',
               ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'data/raw/训练集.csv',
               PREVIOUS/'selected_validation.npy',PREVIOUS/'selection.json']
    sources += [cached_raw(seed,frac,year) for seed,frac in sorted({(s,f) for c in RAW_MIXES.values() for s,f,w in c}) for year in YEARS]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'baseline_score':EXPECTED,'selection_rule':'highest compliant connected2020-2024 official composite; no extra gate',
        'all_years_previously_viewed':True,'models':CONFIGS,'groups':GROUPS,
        'fixed_training':{'seed':2026,'fraction':0.175,'samples':8,'features':63},
        'raw_mixes':{name:[{'seed':s,'fraction':f,'weight':w} for s,f,w in c] for name,c in RAW_MIXES.items()},
        'fixed_complete_scheme':{'slow16_weight':0.25,'retention':0.985,'limit_up_delta':0.10},
        'checkpoint_control':'round_curve31 at180 must reproduce old raw predictions exactly in every year',
        'raw_mixture_control':'rank-normalized unblended seed2026 must reproduce the finished baseline exactly',
        'refinement':'highest donor across raw mixtures, checkpoints and baseline; ordering weights0.20/0.25/0.30 x retention0.982/0.985/0.988; limit shifts0.05/0.10/0.15',
        'scoring':'unmodified evaluate.py on actual written validation CSVs;1212 connected days and cross-year turnover',
        'test_labels_read':False,'test_future_prices_used_to_select':False,
        'input_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round2 protocol frozen')


class Context(PreviousContext):
    def __init__(self):
        super().__init__()
        self.scoring = OUT/'scoring_validation_only'
        self.scoring.mkdir(exist_ok=True)
        for name,cols in [('测试集_X.csv',KEYS+['flag_limit_up']),('测试集_Y.csv',KEYS+['y_ret_1d'])]:
            if not (self.scoring/name).exists():
                self.frame.select(cols).write_csv(self.scoring/name,float_precision=17)

    def finished(self,name):
        import numpy as np
        import polars as pl
        path = OUT/f'promote_{name}.npy'
        if path.exists():
            return np.load(path)
        if name == 'baseline':
            result = self.promote('seed2026')
        else:
            parts = []
            for year in YEARS:
                raw = pl.read_parquet(OUT/f'raw/{name}_{year}.parquet')
                keys = self.frame.filter(pl.col('trade_date')//10000 == year).select(KEYS)
                assert raw.select(KEYS).equals(keys)
                parts.append(raw['pred_raw'].to_numpy())
            result = self.finish(parts)
        np.save(path,result)
        return result


def score_record(ctx,name,promote,recipe,weight=0.25,retention=0.985,delta=0.10):
    pred,stats = ctx.predict(ctx.donor(promote),weight,retention,delta)
    metrics = ctx.score(pred)
    log(f'{name}: {metrics["final_score"]:.9f}, delta={metrics["final_score"]-EXPECTED:+.9f}')
    return {'donor':name,'recipe':recipe,'slow16_weight':weight,'retention':retention,'limit_up_delta':delta,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def rawmix():
    import numpy as np
    import polars as pl
    from optimize_wave15 import daily_ranks
    verify()
    ctx = Context()
    baseline = ctx.finished('baseline')
    pred,_ = ctx.predict(ctx.donor(baseline),0.25,0.985,0.10)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    metrics = ctx.score(pred)
    assert abs(metrics['final_score']-EXPECTED) < 1e-12
    path = OUT/'wave44_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{},'harness':{'baseline_bit_identical':True,'score':metrics['final_score']}}
    if 'baseline' not in result['results']:
        result['results']['baseline'] = {'donor':'baseline','recipe':{'type':'baseline'},'slow16_weight':0.25,
              'retention':0.985,'limit_up_delta':0.10,'connected_final_score':metrics['final_score'],'metrics':metrics}
    cache = {}
    def load(seed,frac,year):
        key = (seed,frac,year)
        if key not in cache:
            raw = pl.read_parquet(cached_raw(seed,frac,year))
            frame = ctx.frame.filter(pl.col('trade_date')//10000 == year)
            assert raw.select(KEYS).equals(frame.select(KEYS))
            cache[key] = daily_ranks(raw['pred_raw'].to_numpy(),frame['price_valid'].to_numpy(),frame['trade_date'].to_numpy())
        return cache[key]
    control = ctx.finish([load(2026,0.175,year) for year in YEARS])
    assert np.array_equal(control,baseline), 'Raw-rank normalization changed the unblended baseline'
    result['harness']['raw_rank_normalization_bit_identical'] = True
    for name,components in RAW_MIXES.items():
        if name in result['results']:
            continue
        mixed = [sum(w*load(s,f,year) for s,f,w in components) for year in YEARS]
        promote = ctx.finish(mixed)
        np.save(OUT/f'promote_{name}.npy',promote)
        recipe = {'type':'raw_rank_mix','components':[{'seed':s,'fraction':f,'weight':w} for s,f,w in components]}
        result['results'][name] = score_record(ctx,name,promote,recipe)
        dump(path,result)
    result['status'] = 'complete'
    dump(path,result)


def train(group):
    import numpy as np
    import polars as pl
    import lightgbm as lgb
    import experiments.r6_topk as rt
    from optimize_wave31 import ObjectiveFrac
    from run import to_matrix, FEATURE_FILE, feature_names
    verify()
    if group not in GROUPS:
        raise ValueError('Training needs an explicit disjoint worker groupA or B')
    (OUT/'raw').mkdir(exist_ok=True)
    (OUT/'models').mkdir(exist_ok=True)
    for year in YEARS:
        families = GROUPS[group]
        def complete(family):
            model_path = OUT/f'models/{family}_{year}.txt'
            for rounds in CONFIGS[family]['checkpoints']:
                path = OUT/f'raw/{family}_r{rounds}_{year}.parquet'
                if not path.exists() or not path.with_suffix('.json').exists():
                    return False
                meta = read(path.with_suffix('.json'))
                assert sha(path) == meta['prediction_sha256']
                assert sha(model_path) == meta['model_sha256']
            return True
        if all(complete(family) for family in families):
            continue
        frame,features,meta = rt.training_frame(year)
        original = read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
        assert meta == original
        labels,dates = frame['y_ret_1d'].to_numpy(),frame['trade_date'].to_numpy()
        x = to_matrix(frame,features)
        del frame
        gc.collect()
        valid = (pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000 == year))
                 .select(KEYS+feature_names()+['price_valid']).sort('trade_date','ts_code').collect())
        vx = to_matrix(valid,features)
        for family in families:
            if complete(family):
                continue
            config = CONFIGS[family]
            rounds = max(config['checkpoints'])
            objective = ObjectiveFrac(dates,labels,2026,0.175,8)
            ds = lgb.Dataset(x,label=np.zeros(len(x),dtype=np.float32),feature_name=features,free_raw_data=True)
            params = dict(rt.PARAMS,**config['params'],objective=rt.objective_callback(objective))
            start = time.monotonic()
            def progress(env):
                if (env.iteration+1)%30 == 0:
                    log(f'{family} {year}: {env.iteration+1}/{rounds}, {time.monotonic()-start:.0f}s')
            model = lgb.train(params,ds,num_boost_round=rounds,callbacks=[progress])
            assert model.current_iteration() == objective.iteration == rounds
            model_path = OUT/f'models/{family}_{year}.txt'
            assert not model_path.exists(),f'Preserve completed model: {model_path}'
            model_path.write_text(model.model_to_string(),encoding='utf-8')
            reload = lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
            for checkpoint in config['checkpoints']:
                raw = model.predict(vx,num_iteration=checkpoint,num_threads=8).astype(np.float64)
                replay = reload.predict(vx,num_iteration=checkpoint,num_threads=8).astype(np.float64)
                assert np.array_equal(raw,replay)
                raw[~valid['price_valid'].to_numpy()] = -1e6
                control = None
                if family == 'round_curve31' and checkpoint == 180:
                    original_raw = pl.read_parquet(cached_raw(2026,0.175,year))
                    assert original_raw.select(KEYS).equals(valid.select(KEYS))
                    assert np.array_equal(raw,original_raw['pred_raw'].to_numpy()),f'180-round control mismatch{year}'
                    control = True
                path = OUT/f'raw/{family}_r{checkpoint}_{year}.parquet'
                assert not path.exists()
                valid.select(KEYS).with_columns(pl.Series('pred_raw',raw)).write_parquet(path,compression='zstd')
                dump(path.with_suffix('.json'),{'family':family,'checkpoint':checkpoint,'year':year,
                     'training_meta':meta,'parameter_overrides':config['params'],'training_rounds':rounds,
                     'same_training_keys_and_labels':True,'model_reload_bit_identical':True,
                     'original_180_round_control':control,'fit_seconds':round(time.monotonic()-start,1),
                     'prediction_sha256':sha(path),'model_sha256':sha(model_path)},immutable=True)
            log(f'{family} {year}: all checkpoints saved and reloaded exactly')
            del model,reload,ds,objective,raw,replay
            gc.collect()
        del x,vx,valid,labels,dates
        gc.collect()


def models():
    verify()
    ctx = Context()
    path = OUT/'wave45_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    for family,config in CONFIGS.items():
        for rounds in config['checkpoints']:
            name = f'{family}_r{rounds}'
            if name in result['results']:
                continue
            recipe = {'type':'model','family':family,'rounds':rounds,'params':config['params'],
                      'seed':2026,'fraction':0.175,'samples':8}
            item = score_record(ctx,name,ctx.finished(name),recipe)
            if family == 'round_curve31' and rounds == 180:
                assert abs(item['connected_final_score']-EXPECTED) < 1e-12
            result['results'][name] = item
            dump(path,result)
    result['status'] = 'complete'
    dump(path,result)


def refine():
    verify()
    ctx = Context()
    items = []
    for wave in (44,45):
        record = read(OUT/f'wave{wave}_results.json')
        assert record['status'] == 'complete'
        items += list(record['results'].values())
    best = max(items,key=lambda r:r['connected_final_score'])
    dump(OUT/'refinement_protocol.json',{'donor':best['donor'],'recipe':best['recipe'],
         'weights':[0.20,0.25,0.30],'retention':[0.982,0.985,0.988],'delta':[0.05,0.10,0.15]},immutable=True)
    promote = ctx.finished(best['donor'])
    path = OUT/'wave46_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    for weight,retention in itertools.product((0.20,0.25,0.30),(0.982,0.985,0.988)):
        name = f'{best["donor"]}_w{weight:.2f}_m{retention:.3f}'
        if name in result['results']:
            continue
        item = score_record(ctx,best['donor'],promote,best['recipe'],weight,retention)
        result['results'][name] = item
        dump(path,result)
    refined = max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for delta in (0.05,0.10,0.15):
        name = f'limit_shift{delta:.2f}'
        if name in result['results']:
            continue
        result['results'][name] = score_record(ctx,best['donor'],promote,best['recipe'],
                         refined['slow16_weight'],refined['retention'],delta)
        dump(path,result)
    result['status'] = 'complete'
    dump(path,result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=('freeze','rawmix','train','models','refine'))
    parser.add_argument('--group',choices=('A','B'))
    args = parser.parse_args()
    if args.stage == 'train':
        train(args.group)
    else:
        globals()[args.stage]()


if __name__ == '__main__':
    main()
