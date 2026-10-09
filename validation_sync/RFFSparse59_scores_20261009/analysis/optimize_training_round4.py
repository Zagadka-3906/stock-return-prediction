"""Waves50-52: refine checkpoint ensembles using historical OOF data only."""
from __future__ import annotations

import argparse
import gc
import itertools
import json
import os
from pathlib import Path
import sys
import time

for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[_name] = '8'
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round3 as previous
from optimize_training_round3 import HERE, YEARS, KEYS, BASE_POST, model_recipe, read, dump, sha, log

OUT = ROOT/'analysis/optimization_20261003_r4'
PREVIOUS = ROOT/'analysis/optimization_20261003_r3'
SECOND = ROOT/'analysis/optimization_20261003_r2'
EXPECTED = 0.4472529347775648
ROUNDS = (90,105,120,180,270)
PAIRS = {(90,180):(0.60,0.65,0.70,0.80,0.85,0.90,0.95),
         (105,180):(0.50,0.65,0.75,0.85,0.90),
         (120,180):(0.65,0.80),(90,270):(0.65,0.80)}
TRIPLES = ((0.15,0.15,0.70),(0.10,0.20,0.70))


def source_raw(rounds,year):
    return (PREVIOUS/f'raw/seed2026_r{rounds}_{year}.parquet' if rounds in (90,105,120)
            else SECOND/f'raw/round_curve31_r{rounds}_{year}.parquet')


def verify():
    record = read(OUT/'protocol.json')
    for name,digest in record['input_sha256'].items():
        assert sha(ROOT/name)==digest,name
    return record


def freeze():
    from finalize_training_round3 import selected
    selected()
    if (OUT/'protocol.json').exists():
        verify()
        return
    sources = [Path(__file__),ROOT/'analysis/optimize_training_round3.py',ROOT/'analysis/finalize_training_round3.py',
               ROOT/'analysis/continue_optimization.py',ROOT/'analysis/finalize_optimization.py',ROOT/'后续选模标准.md',
               ROOT/'evaluate.py',ROOT/'run.py',ROOT/'experiments/r6_topk.py',ROOT/'src/scoring.py',ROOT/'src/postprocessing.py',
               HERE/'connected_scorer.py',HERE/'optimize_wave31.py',HERE/'optimize_wave6.py',HERE/'optimize_wave13.py',
               HERE/'optimize_wave15.py',HERE/'optimize_wave18.py',HERE/'return_mapping.py',
               ROOT/'data/features.parquet',ROOT/'data/raw/训练集.csv',ROOT/'data/feature_manifest.json',
               PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',ROOT/'active_release.json']
    sources += [p for rounds in ROUNDS for year in YEARS
                for p in (source_raw(rounds,year),source_raw(rounds,year).with_suffix('.json'))]
    sources += [SECOND/f'models/round_curve31_{year}.txt' for year in YEARS]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':EXPECTED,'same_validation':'2020-2024 expanding OOF;1212 connected days;5635800 rows',
         'fixed_models':{'seed':2026,'fraction':0.175,'samples':8,'features':63,'rounds':ROUNDS},
         'pair_grid':{f'{a}_{b}':weights for (a,b),weights in PAIRS.items()},
         'triple_rounds':(90,105,180),'triple_weights':TRIPLES,
         'fine_mix_deltas':(-0.05,-0.025,0.0,0.025,0.05),
         'fine_mix_definition':'shift last component weight, preserve relative proportions of earlier components',
         'fine_mix_boundary_clamp':(0.01,0.99),
         'smoothing':{'alphas':(0.875,0.9,0.9125),'bonuses':(0.275,0.3,0.325)},
         'output':{'slow_weights':(0.24,0.25,0.26),'retention':(0.9845,0.985,0.9855),'limit_up_deltas':(0.09,0.1,0.11)},
         'selection_rule':'highest official connected composite among compliant complete schemes; no other gate',
         'expected_scored_records':45,'new_model_training_required_for_search':False,
         'baseline_control':'finished prediction bit identical and actual written-CSV score identical to round3 winner',
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round4 protocol frozen')


def provenance():
    verify()
    for year in YEARS:
        original = read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
        model_path = SECOND/f'models/round_curve31_{year}.txt'
        for rounds in ROUNDS:
            path = source_raw(rounds,year)
            info = read(path.with_suffix('.json'))
            assert info['training_meta']==original
            assert sha(path)==info['prediction_sha256'] and sha(model_path)==info['model_sha256']
            dump(OUT/f'raw/source_r{rounds}_{year}.json',{'year':year,'seed':2026,'checkpoint':rounds,
                 'training_meta':original,'source_prediction':str(path),'source_model':str(model_path),
                 'prediction_sha256':sha(path),'model_sha256':sha(model_path),
                 'source_metadata_sha256':sha(path.with_suffix('.json')),
                 'same_training_keys_and_labels':True,'inherited_model_reload_bit_identical':info['model_reload_bit_identical']},immutable=True)
    log('25 source arrays and their mature-label training metadata verified')


class Context(previous.Context):
    def __init__(self):
        super().__init__()
        self.scoring = OUT/'scoring_validation_only'
        self.scoring.mkdir(exist_ok=True)
        for name,cols in [('测试集_X.csv',KEYS+['flag_limit_up']),('测试集_Y.csv',KEYS+['y_ret_1d'])]:
            if not (self.scoring/name).exists():
                self.frame.select(cols).write_csv(self.scoring/name,float_precision=17)
        self.raw_cache = {}
        self.rank_cache = {}
        self.year_frames = {}

    def raw_parts(self,recipe):
        import polars as pl
        from optimize_wave15 import daily_ranks
        def load(component,year):
            assert component['seed']==2026 and component['fraction']==0.175
            key = (component['rounds'],year)
            if key not in self.raw_cache:
                raw = pl.read_parquet(source_raw(*key))
                if year not in self.year_frames:
                    self.year_frames[year] = self.frame.filter(pl.col('trade_date')//10000==year)
                assert raw.select(KEYS).equals(self.year_frames[year].select(KEYS))
                self.raw_cache[key] = raw['pred_raw'].to_numpy()
            return key,self.raw_cache[key]
        if recipe['type']=='model':
            return [load(recipe,year)[1] for year in YEARS]
        result = []
        for year in YEARS:
            parts = []
            for component in recipe['components']:
                key,raw = load(component,year)
                if key not in self.rank_cache:
                    frame = self.year_frames[year]
                    self.rank_cache[key] = daily_ranks(raw,frame['price_valid'].to_numpy(),frame['trade_date'].to_numpy())
                parts.append(component['weight']*self.rank_cache[key])
            result.append(sum(parts))
        return result

    def finished(self,name,recipe=None):
        import numpy as np
        path = OUT/f'promote_{name}.npy'
        if path.exists():
            return np.load(path)
        assert recipe is not None
        # The existing finishing implementation accepts the dynamic raw_parts
        # method; only its cache destination needs to be different here.
        import polars as pl
        from optimize_wave6 import make_prediction_param
        from src.scoring import Panel
        post = recipe.get('postprocessing',BASE_POST)
        parts = []
        for year,raw in zip(YEARS,self.raw_parts(recipe)):
            frame = self.label_free.filter(pl.col('trade_date')//10000==year)
            panel = Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw)))
            parts.append(make_prediction_param(panel,frame['aux_raw'].to_numpy(),**post))
        result = np.concatenate(parts)
        np.save(path,result)
        return result


def mix_recipe(rounds,weights):
    assert len(rounds)==len(weights) and abs(sum(weights)-1)<1e-12 and all(w>0 for w in weights)
    return {'type':'raw_rank_mix','components':[dict(model_recipe(2026,r),weight=w) for r,w in zip(rounds,weights)],
            'postprocessing':dict(BASE_POST)}


def score_record(ctx,name,recipe,weight=0.25,retention=0.985,delta=0.1):
    pred,stats = ctx.predict(ctx.donor(ctx.finished(name,recipe)),weight,retention,delta)
    metrics = ctx.score(pred)
    log(f'{name}: {metrics["final_score"]:.9f}, gain={metrics["final_score"]-EXPECTED:+.9f}')
    return {'donor':name,'recipe':recipe,'slow16_weight':weight,'retention':retention,'limit_up_delta':delta,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def mixtures():
    import numpy as np
    verify()
    ctx = Context()
    path = OUT/'wave50_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    baseline = read(PREVIOUS/'selection.json')['winner']['recipe']
    pred,_ = ctx.predict(ctx.donor(ctx.finished('baseline',baseline)),0.25,0.985,0.1)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    if 'baseline' not in result['results']:
        result['results']['baseline'] = score_record(ctx,'baseline',baseline)
        assert abs(result['results']['baseline']['connected_final_score']-EXPECTED)<1e-12
        dump(path,result)
    for rounds,weights in PAIRS.items():
        for weight in weights:
            name = f'round{rounds[0]}_{rounds[1]}_w{weight:g}'
            if name in result['results']:
                continue
            result['results'][name] = score_record(ctx,name,mix_recipe(rounds,(1-weight,weight)))
            dump(path,result)
    for i,weights in enumerate(TRIPLES):
        name = f'triple90_105_180_{i}'
        if name in result['results']:
            continue
        result['results'][name] = score_record(ctx,name,mix_recipe((90,105,180),weights))
        dump(path,result)
    result.update(status='complete',baseline_bit_identical=True)
    dump(path,result)


def fine():
    verify()
    previous = read(OUT/'wave50_results.json')
    assert previous['status']=='complete'
    best = max(previous['results'].values(),key=lambda r:r['connected_final_score'])
    dump(OUT/'fine_mix_protocol.json',{'winner_before_refinement':best,'weight_deltas':(-0.05,-0.025,0,0.025,0.05)},immutable=True)
    ctx = Context()
    path = OUT/'wave51_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    base = best['recipe']['components']
    old_weight = base[-1]['weight']
    for delta in (-0.05,-0.025,0,0.025,0.05):
        weight = min(0.99,max(0.01,old_weight+delta))
        assert 0<weight<1
        name = f'fine_d{delta:+g}_last_w{weight:g}'
        if name in result['results']:
            continue
        components = [dict(c,weight=c['weight']*(1-weight)/(1-old_weight)) for c in base[:-1]]+[dict(base[-1],weight=weight)]
        recipe = dict(best['recipe'],components=components)
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    refined = max(result['results'].values(),key=lambda r:r['connected_final_score'])
    dump(OUT/'smoothing_protocol.json',{'winner_before_smoothing':refined,'alphas':(0.875,0.9,0.9125),
         'bonuses':(0.275,0.3,0.325)},immutable=True)
    for alpha,bonus in itertools.product((0.875,0.9,0.9125),(0.275,0.3,0.325)):
        name = f'{refined["donor"]}_a{alpha:g}_b{bonus:g}'
        if name in result['results']:
            continue
        recipe = dict(refined['recipe'],postprocessing=dict(BASE_POST,alpha=alpha,bonus=bonus))
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    result['status']='complete'
    dump(path,result)


def refine():
    verify()
    items = []
    for wave in (50,51):
        record = read(OUT/f'wave{wave}_results.json')
        assert record['status']=='complete'
        items += list(record['results'].values())
    best = max(items,key=lambda r:r['connected_final_score'])
    dump(OUT/'refinement_protocol.json',{'donor':best['donor'],'recipe':best['recipe'],
         'slow_weights':(0.24,0.25,0.26),'retention':(0.9845,0.985,0.9855),'limit_up_deltas':(0.09,0.1,0.11)},immutable=True)
    ctx = Context()
    path = OUT/'wave52_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    for weight,retention in itertools.product((0.24,0.25,0.26),(0.9845,0.985,0.9855)):
        name = f'order_w{weight:g}_m{retention:g}'
        if name in result['results']:
            continue
        result['results'][name] = score_record(ctx,best['donor'],best['recipe'],weight,retention)
        dump(path,result)
    refined = max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for delta in (0.09,0.1,0.11):
        name = f'limit_shift{delta:g}'
        if name in result['results']:
            continue
        result['results'][name] = score_record(ctx,best['donor'],best['recipe'],refined['slow16_weight'],refined['retention'],delta)
        dump(path,result)
    result['status']='complete'
    dump(path,result)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=('freeze','provenance','mixtures','fine','refine'))
    globals()[parser.parse_args().stage]()


if __name__=='__main__':
    main()
