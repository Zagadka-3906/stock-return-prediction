"""Waves47-49: saved-tree checkpoints, temporal smoothing, and complete outputs.

Use historical training OOF labels only. Freeze search axes before scoring;
load saved fold models instead of repeating their training.
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
from continue_optimization import Context as BaseContext, HERE, YEARS, KEYS, read, dump, sha, log

OUT = ROOT/'analysis/optimization_20261003_r3'
PREVIOUS = ROOT/'analysis/optimization_20261003_r2'
FIRST = ROOT/'analysis/optimization_20261003'
EXPECTED = 0.44609097824245914
CHECKPOINTS = {2026:(30,60,75,90,105,120,150),2027:(60,90,120),2028:(60,90,120)}
BASE_POST = {'alpha':0.9,'bonus':0.3,'mode':'top_only','weight':0.25,
             'restore_lower':True,'top_current_weight':1.0}
ALPHAS = (0.80,0.85,0.90,0.925,0.95)
BONUSES = (0.15,0.30,0.45)
AUX_WEIGHTS = (0.0,0.125,0.375,0.5)


def source_model(seed,year):
    return (PREVIOUS/f'models/round_curve31_{year}.txt' if seed == 2026
            else FIRST/f'raw/topk_seed{seed}_{year}.txt')


def source_meta(seed,year):
    return (PREVIOUS/f'raw/round_curve31_r180_{year}.json' if seed == 2026
            else FIRST/f'raw/topk_seed{seed}_{year}.json')


def control_raw(seed,year):
    return (PREVIOUS/f'raw/round_curve31_r90_{year}.parquet' if seed == 2026
            else FIRST/f'raw/topk_seed{seed}_{year}.parquet')


def verify():
    protocol = read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():
        assert sha(ROOT/path) == digest,path
    return protocol


def freeze():
    from finalize_training_round2 import selected
    selected()
    if (OUT/'protocol.json').exists():
        verify()
        return
    sources = [Path(__file__),ROOT/'analysis/continue_optimization.py',ROOT/'analysis/optimize_training_round2.py',
               ROOT/'analysis/finalize_training_round2.py',ROOT/'analysis/finalize_optimization.py',
               ROOT/'后续选模标准.md',ROOT/'evaluate.py',ROOT/'run.py',ROOT/'experiments/r6_topk.py',
               ROOT/'src/scoring.py',ROOT/'src/postprocessing.py',HERE/'connected_scorer.py',
               HERE/'optimize_wave31.py',HERE/'optimize_wave6.py',HERE/'optimize_wave13.py',
               HERE/'optimize_wave15.py',HERE/'optimize_wave18.py',HERE/'return_mapping.py',
               ROOT/'data/features.parquet',ROOT/'data/raw/训练集.csv',ROOT/'data/feature_manifest.json',
               PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',
               PREVIOUS/'boundary_maturity.json',ROOT/'active_release.json']
    sources += [path for seed in CHECKPOINTS for year in YEARS
                for path in (source_model(seed,year),source_meta(seed,year),control_raw(seed,year))]
    sources += [HERE/f'wave36_topk/raw/topk_seed2026_f0.175_{year}.parquet' for year in YEARS]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'baseline_score':EXPECTED,'checkpoints':CHECKPOINTS,'checkpoint_models_already_trained':15,
        'fixed_model':{'features':63,'fraction':0.175,'samples':8,'parameters':'original r6 PARAMS'},
        'fixed_initial_postprocessing':BASE_POST,'raw_round_mixture_weights':(0.25,0.5,0.75),
        'mixture_definition':'daily rank mix of seed2026 90 and180 rounds before temporal smoothing',
        'postprocessing':{'alphas':ALPHAS,'bonuses':BONUSES,'auxiliary_weights':AUX_WEIGHTS},
        'output_refinement':{'slow_weights':(0.225,0.25,0.275),'retention':(0.984,0.985,0.986),
                             'limit_up_deltas':(0.075,0.1,0.125)},
        'selection_rule':'highest connected2020-2024 official composite among complete compliant schemes; no additional gate',
        'validation_days':1212,'validation_rows':5635800,'cross_year_turnover_included':True,
        'checkpoint_controls':'all15 source models must reproduce their cached90/180-round raw OOF predictions bit identically',
        'test_labels_read':False,'test_future_prices_used_to_select':False,
        'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'input_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round3 protocol frozen')


class Context(BaseContext):
    def __init__(self):
        super().__init__()
        self.scoring = OUT/'scoring_validation_only'
        self.scoring.mkdir(exist_ok=True)
        for name,cols in [('测试集_X.csv',KEYS+['flag_limit_up']),('测试集_Y.csv',KEYS+['y_ret_1d'])]:
            if not (self.scoring/name).exists():
                self.frame.select(cols).write_csv(self.scoring/name,float_precision=17)

    def raw_parts(self,recipe):
        import polars as pl
        from optimize_wave15 import daily_ranks
        if recipe['type'] == 'raw_rank_mix':
            parts = [self.raw_parts({**component,'type':'model'}) for component in recipe['components']]
            result = []
            for i,year in enumerate(YEARS):
                frame = self.frame.filter(pl.col('trade_date')//10000 == year)
                result.append(sum(c['weight']*daily_ranks(p[i],frame['price_valid'].to_numpy(),frame['trade_date'].to_numpy())
                                  for c,p in zip(recipe['components'],parts)))
            return result
        seed,rounds = recipe['seed'],recipe['rounds']
        result = []
        for year in YEARS:
            path = (HERE/f'wave36_topk/raw/topk_seed2026_f0.175_{year}.parquet' if seed==2026 and rounds==180
                    else OUT/f'raw/seed{seed}_r{rounds}_{year}.parquet')
            raw = pl.read_parquet(path)
            keys = self.frame.filter(pl.col('trade_date')//10000 == year).select(KEYS)
            assert raw.select(KEYS).equals(keys)
            result.append(raw['pred_raw'].to_numpy())
        return result

    def finished(self,name,recipe=None):
        import numpy as np
        import polars as pl
        from optimize_wave6 import make_prediction_param
        from src.scoring import Panel
        path = OUT/f'promote_{name}.npy'
        if path.exists():
            return np.load(path)
        assert recipe is not None
        post = recipe.get('postprocessing',BASE_POST)
        parts = []
        for year,raw in zip(YEARS,self.raw_parts(recipe)):
            frame = self.label_free.filter(pl.col('trade_date')//10000 == year)
            panel = Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw)))
            parts.append(make_prediction_param(panel,frame['aux_raw'].to_numpy(),**post))
        result = np.concatenate(parts)
        np.save(path,result)
        return result


def checkpoint_predictions():
    import lightgbm as lgb
    import numpy as np
    import polars as pl
    from run import FEATURE_FILE,to_matrix,feature_names
    verify()
    (OUT/'raw').mkdir(exist_ok=True)
    for year in YEARS:
        features = feature_names()
        frame = (pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year))
                 .select(KEYS+features+['price_valid']).sort('trade_date','ts_code').collect())
        matrix = to_matrix(frame,features)
        for seed,checkpoints in CHECKPOINTS.items():
            metadata = read(source_meta(seed,year))
            model_path = source_model(seed,year)
            assert sha(model_path) == metadata['model_sha256']
            original_meta = read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
            assert metadata['training_meta'] == original_meta
            model = lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
            assert model.feature_name() == features
            control_rounds = 90 if seed == 2026 else 180
            predicted = model.predict(matrix,num_iteration=control_rounds,num_threads=8)
            predicted[~frame['price_valid'].to_numpy()] = -1e6
            old = pl.read_parquet(control_raw(seed,year))
            assert old.select(KEYS).equals(frame.select(KEYS))
            assert np.array_equal(predicted,old['pred_raw'].to_numpy())
            reloaded = lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
            for rounds in checkpoints:
                path = OUT/f'raw/seed{seed}_r{rounds}_{year}.parquet'
                if path.exists() and path.with_suffix('.json').exists():
                    assert sha(path) == read(path.with_suffix('.json'))['prediction_sha256']
                    continue
                raw = model.predict(matrix,num_iteration=rounds,num_threads=8)
                assert np.array_equal(raw,reloaded.predict(matrix,num_iteration=rounds,num_threads=8))
                raw[~frame['price_valid'].to_numpy()] = -1e6
                frame.select(KEYS).with_columns(pl.Series('pred_raw',raw)).write_parquet(path,compression='zstd')
                dump(path.with_suffix('.json'),{'year':year,'seed':seed,'fraction':0.175,'checkpoint':rounds,
                     'training_meta':original_meta,'source_model':str(model_path),
                     'model_sha256':sha(model_path),'prediction_sha256':sha(path),
                     'model_reload_bit_identical':True,'same_training_keys_and_labels':True,
                     'cached_source_control_bit_identical':True,'control_rounds':control_rounds},immutable=True)
            log(f'seed{seed} {year}: checkpoints and cached source control passed')
            del model,reloaded,predicted,old
            gc.collect()
        del frame,matrix
        gc.collect()


def model_recipe(seed,rounds):
    return {'type':'model','seed':seed,'fraction':0.175,'rounds':rounds,'params':{},'samples':8,
            'postprocessing':dict(BASE_POST)}


def score_record(ctx,name,recipe,weight=0.25,retention=0.985,delta=0.10):
    promote = ctx.finished(name,recipe)
    pred,stats = ctx.predict(ctx.donor(promote),weight,retention,delta)
    metrics = ctx.score(pred)
    log(f'{name}: {metrics["final_score"]:.9f}, gain={metrics["final_score"]-EXPECTED:+.9f}')
    return {'donor':name,'recipe':recipe,'slow16_weight':weight,'retention':retention,'limit_up_delta':delta,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def models():
    import numpy as np
    verify()
    assert len(list((OUT/'raw').glob('*.json'))) == 65
    ctx = Context()
    path = OUT/'wave47_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    baseline = model_recipe(2026,90)
    pred,_ = ctx.predict(ctx.donor(ctx.finished('seed2026_r90',baseline)),0.25,0.985,0.1)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    for seed,checkpoints in CHECKPOINTS.items():
        for rounds in checkpoints:
            name = f'seed{seed}_r{rounds}'
            if name in result['results']:
                continue
            item = score_record(ctx,name,model_recipe(seed,rounds))
            if seed==2026 and rounds==90:
                assert abs(item['connected_final_score']-EXPECTED)<1e-12
            result['results'][name] = item
            dump(path,result)
    for weight in (0.25,0.5,0.75):
        name = f'round90_180_w{weight:.2f}'
        if name in result['results']:
            continue
        recipe = {'type':'raw_rank_mix','components':[dict(model_recipe(2026,90),weight=1-weight),
                                                     dict(model_recipe(2026,180),weight=weight)],
                  'postprocessing':dict(BASE_POST)}
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    result['status'] = 'complete'
    result['baseline_bit_identical'] = True
    dump(path,result)


def smoothing():
    verify()
    previous = read(OUT/'wave47_results.json')
    assert previous['status']=='complete'
    best = max(previous['results'].values(),key=lambda r:r['connected_final_score'])
    dump(OUT/'smoothing_protocol.json',{'winner_before_postprocessing':best,'alphas':ALPHAS,
         'bonuses':BONUSES,'aux_weights':AUX_WEIGHTS},immutable=True)
    ctx = Context()
    path = OUT/'wave48_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    for alpha,bonus in itertools.product(ALPHAS,BONUSES):
        name = f'{best["donor"]}_a{alpha:g}_b{bonus:g}_w0.25'
        if name in result['results']:
            continue
        recipe = {**best['recipe'],'postprocessing':dict(BASE_POST,alpha=alpha,bonus=bonus)}
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    base = max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for weight in AUX_WEIGHTS:
        name = f'{base["donor"]}_aux{weight:g}'
        if name in result['results']:
            continue
        recipe = {**base['recipe'],'postprocessing':dict(base['recipe']['postprocessing'],weight=weight)}
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    result['status'] = 'complete'
    dump(path,result)


def refine():
    verify()
    items = []
    for wave in (47,48):
        record = read(OUT/f'wave{wave}_results.json')
        assert record['status']=='complete'
        items += list(record['results'].values())
    best = max(items,key=lambda r:r['connected_final_score'])
    dump(OUT/'refinement_protocol.json',{'donor':best['donor'],'recipe':best['recipe'],
         'slow_weights':(0.225,0.25,0.275),'retention':(0.984,0.985,0.986),
         'limit_up_deltas':(0.075,0.1,0.125)},immutable=True)
    ctx = Context()
    path = OUT/'wave49_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    for weight,retention in itertools.product((0.225,0.25,0.275),(0.984,0.985,0.986)):
        name = f'order_w{weight:g}_m{retention:g}'
        if name in result['results']:
            continue
        result['results'][name] = score_record(ctx,best['donor'],best['recipe'],weight,retention)
        dump(path,result)
    refined = max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for delta in (0.075,0.1,0.125):
        name = f'limit_shift{delta:g}'
        if name in result['results']:
            continue
        result['results'][name] = score_record(ctx,best['donor'],best['recipe'],
                     refined['slow16_weight'],refined['retention'],delta)
        dump(path,result)
    result['status'] = 'complete'
    dump(path,result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=('freeze','checkpoints','models','smoothing','refine'))
    stage = parser.parse_args().stage
    (checkpoint_predictions if stage=='checkpoints' else globals()[stage])()


if __name__=='__main__':
    main()
