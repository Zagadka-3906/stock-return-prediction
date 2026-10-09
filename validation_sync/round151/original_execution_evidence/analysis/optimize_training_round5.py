"""Waves53-55: low-weight seed diversity and complete-output refinement."""
from __future__ import annotations

import argparse
import itertools
import os
from pathlib import Path
import sys
import time

for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[_name] = '8'
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round4 as previous
from optimize_training_round3 import HERE, YEARS, KEYS, BASE_POST, model_recipe, read, dump, sha, log

OUT = ROOT/'analysis/optimization_20261003_r5'
PREVIOUS = ROOT/'analysis/optimization_20261003_r4'
FIRST = ROOT/'analysis/optimization_20261003'
SECOND = ROOT/'analysis/optimization_20261003_r2'
THIRD = ROOT/'analysis/optimization_20261003_r3'
EXPECTED = 0.4473424071299967
CONFIGS = ((2026,90),(2026,180),*itertools.product((2027,2028),(90,120,180)))
EXTRA_WEIGHTS = (0.05,0.10,0.20)
DUAL_WEIGHTS = (0.05,0.10)
SLOW_WEIGHTS = (0.20,0.22,0.24,0.26,0.28)
RETENTION = (0.983,0.9845,0.986)
LIMIT_SHIFTS = (0.095,0.10,0.105)
WAVES = (53,54,55)


def source_raw(seed,rounds,year):
    if seed==2026:
        return previous.source_raw(rounds,year)
    return (FIRST/f'raw/topk_seed{seed}_{year}.parquet' if rounds==180
            else THIRD/f'raw/seed{seed}_r{rounds}_{year}.parquet')


def source_model(seed,year):
    return (SECOND/f'models/round_curve31_{year}.txt' if seed==2026
            else FIRST/f'raw/topk_seed{seed}_{year}.txt')


def verify():
    protocol = read(OUT/'protocol.json')
    for name,digest in protocol['input_sha256'].items():
        assert sha(ROOT/name)==digest,name
    return protocol


def freeze():
    from finalize_training_round4 import selected
    selected()
    if (OUT/'protocol.json').exists():
        verify()
        return
    sources = [Path(__file__),ROOT/'analysis/finalize_training_round5.py',
               ROOT/'analysis/optimize_training_round4.py',ROOT/'analysis/finalize_training_round4.py',
               ROOT/'analysis/optimize_training_round3.py',ROOT/'analysis/continue_optimization.py',
               ROOT/'analysis/finalize_optimization.py',ROOT/'后续选模标准.md',ROOT/'evaluate.py',
               ROOT/'run.py',ROOT/'experiments/r6_topk.py',ROOT/'src/scoring.py',ROOT/'src/postprocessing.py',
               *[HERE/name for name in ('connected_scorer.py','optimize_wave31.py','optimize_wave6.py',
                                       'optimize_wave13.py','optimize_wave15.py','optimize_wave18.py','return_mapping.py')],
               ROOT/'data/features.parquet',ROOT/'data/raw/训练集.csv',ROOT/'data/feature_manifest.json',
               PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',ROOT/'active_release.json',
               HERE/'combined_fold_frame.parquet',HERE/'connected_pred_peer67_slow16.npy',
               HERE/'orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy',
               HERE/'pp_a0_b0_top_only_w0.25_rl1_tcw1.npy']
    sources += [p for seed,rounds in CONFIGS for year in YEARS
                for p in (source_raw(seed,rounds,year),source_raw(seed,rounds,year).with_suffix('.json'))]
    sources += [source_model(seed,year) for seed in (2026,2027,2028) for year in YEARS]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':EXPECTED,'same_validation':'2020-2024 expanding OOF;1212 connected days;5635800 rows',
         'fixed_training':{'fraction':0.175,'samples':8,'features':63,'parameters':'original r6 PARAMS'},
         'source_configs':CONFIGS,'single_seed_components':list(itertools.product((2027,2028),(90,120,180))),
         'single_seed_weights':EXTRA_WEIGHTS,'dual_seed_rounds':(90,180),'each_dual_seed_weight':DUAL_WEIGHTS,
         'base_components':'preserve seed2026 90/180 relative weights25%/75%',
         'initial_output':{'slow16_weight':0.24,'retention':0.9845,'limit_up_delta':0.1},
         'fine_weight_deltas':(-0.025,0,0.025),'fine_definition':'shift total new-seed weight, preserve within-group weights; if baseline leads, shift180-round weight',
         'fine_boundary_clamp':(0.01,0.99),
         'output_grid':{'slow_weights':SLOW_WEIGHTS,'retention':RETENTION,'limit_up_deltas':LIMIT_SHIFTS},
         'expected_scored_records':44,'new_fold_training_required':False,
         'baseline_control':'full prediction and written-CSV score reproduce round4 winner',
         'selection_rule':'highest official connected composite among compliant complete schemes; exact ties prefer fewer models and trees',
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round5 protocol frozen before scoring')


def provenance():
    verify()
    for seed,rounds in CONFIGS:
        for year in YEARS:
            path = source_raw(seed,rounds,year)
            info = read(path.with_suffix('.json'))
            original = read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
            assert info['training_meta']==original
            model = source_model(seed,year)
            assert sha(path)==info['prediction_sha256'] and sha(model)==info['model_sha256']
            assert info['model_reload_bit_identical']
            dump(OUT/f'raw/source_seed{seed}_r{rounds}_{year}.json',
                 {'year':year,'seed':seed,'checkpoint':rounds,'training_meta':original,
                  'source_prediction':str(path),'source_model':str(model),
                  'prediction_sha256':sha(path),'model_sha256':sha(model),
                  'source_metadata_sha256':sha(path.with_suffix('.json')),
                  'same_training_keys_and_labels':True,'inherited_model_reload_bit_identical':True},immutable=True)
    log('40 source arrays and15 saved fold models verified')


class Context(previous.Context):
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
        result = []
        for year in YEARS:
            if year not in self.year_frames:
                self.year_frames[year] = self.frame.filter(pl.col('trade_date')//10000==year)
            frame = self.year_frames[year]
            parts = []
            for c in recipe['components']:
                assert c['fraction']==0.175 and not c['params']
                key = (c['seed'],c['rounds'],year)
                if key not in self.raw_cache:
                    raw = pl.read_parquet(source_raw(*key))
                    assert raw.select(KEYS).equals(frame.select(KEYS))
                    self.raw_cache[key] = raw['pred_raw'].to_numpy()
                if key not in self.rank_cache:
                    self.rank_cache[key] = daily_ranks(self.raw_cache[key],frame['price_valid'].to_numpy(),frame['trade_date'].to_numpy())
                parts.append(c['weight']*self.rank_cache[key])
            result.append(sum(parts))
        return result

    def finished(self,name,recipe=None):
        import numpy as np
        import polars as pl
        from optimize_wave6 import make_prediction_param
        from src.scoring import Panel
        path = OUT/f'promote_{name}.npy'
        if path.exists():return np.load(path)
        assert recipe is not None
        parts = []
        for year,raw in zip(YEARS,self.raw_parts(recipe)):
            frame = self.label_free.filter(pl.col('trade_date')//10000==year)
            panel = Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw)))
            parts.append(make_prediction_param(panel,frame['aux_raw'].to_numpy(),**recipe['postprocessing']))
        result = np.concatenate(parts)
        np.save(path,result)
        return result


def add_seed_components(extras):
    total = sum(c['weight'] for c in extras)
    assert 0<total<1
    return {'type':'raw_rank_mix','components':[
        dict(model_recipe(2026,90),weight=0.25*(1-total)),
        dict(model_recipe(2026,180),weight=0.75*(1-total)),*extras],
        'postprocessing':dict(BASE_POST)}


def score_record(ctx,name,recipe,weight=0.24,retention=0.9845,delta=0.1):
    pred,stats = ctx.predict(ctx.donor(ctx.finished(name,recipe)),weight,retention,delta)
    metrics = ctx.score(pred)
    log(f'{name}: {metrics["final_score"]:.9f}, gain={metrics["final_score"]-EXPECTED:+.9f}')
    return {'donor':name,'recipe':recipe,'slow16_weight':weight,'retention':retention,'limit_up_delta':delta,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def mixtures():
    import numpy as np
    verify()
    ctx = Context()
    path = OUT/'wave53_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    baseline = read(PREVIOUS/'selection.json')['winner']['recipe']
    pred,_ = ctx.predict(ctx.donor(ctx.finished('baseline',baseline)),0.24,0.9845,0.1)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    if 'baseline' not in result['results']:
        result['results']['baseline'] = score_record(ctx,'baseline',baseline)
        assert abs(result['results']['baseline']['connected_final_score']-EXPECTED)<1e-12
        dump(path,result)
    for seed,rounds,weight in itertools.product((2027,2028),(90,120,180),EXTRA_WEIGHTS):
        name = f'add_seed{seed}_r{rounds}_w{weight:g}'
        if name in result['results']:continue
        recipe = add_seed_components([dict(model_recipe(seed,rounds),weight=weight)])
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    for rounds,weight in itertools.product((90,180),DUAL_WEIGHTS):
        name = f'add_both_r{rounds}_each_w{weight:g}'
        if name in result['results']:continue
        recipe = add_seed_components([dict(model_recipe(seed,rounds),weight=weight) for seed in (2027,2028)])
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    result.update(status='complete',baseline_bit_identical=True)
    dump(path,result)


def fine():
    verify()
    coarse = read(OUT/'wave53_results.json')
    assert coarse['status']=='complete'
    best = max(coarse['results'].values(),key=lambda r:r['connected_final_score'])
    dump(OUT/'fine_mix_protocol.json',{'winner_before_refinement':best,'weight_deltas':(-0.025,0,0.025)},immutable=True)
    ctx = Context()
    path = OUT/'wave54_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    parts = best['recipe']['components']
    boundary = 2 if len(parts)>2 else 1
    before,after = parts[:boundary],parts[boundary:]
    old = sum(c['weight'] for c in after)
    for delta in (-0.025,0,0.025):
        weight = min(0.99,max(0.01,old+delta))
        name = f'fine_group_w{weight:g}'
        if name in result['results']:continue
        components = [dict(c,weight=c['weight']*(1-weight)/(1-old)) for c in before]
        components += [dict(c,weight=c['weight']*weight/old) for c in after]
        recipe = dict(best['recipe'],components=components)
        result['results'][name] = score_record(ctx,name,recipe)
        dump(path,result)
    result['status']='complete'
    dump(path,result)


def refine():
    verify()
    items = []
    for wave in (53,54):
        record = read(OUT/f'wave{wave}_results.json')
        assert record['status']=='complete'
        items += list(record['results'].values())
    best = max(items,key=lambda r:r['connected_final_score'])
    dump(OUT/'refinement_protocol.json',{'donor':best['donor'],'recipe':best['recipe'],
         'slow_weights':SLOW_WEIGHTS,'retention':RETENTION,'limit_up_deltas':LIMIT_SHIFTS},immutable=True)
    ctx = Context()
    path = OUT/'wave55_results.json'
    result = read(path) if path.exists() else {'status':'running','results':{}}
    for weight,retention in itertools.product(SLOW_WEIGHTS,RETENTION):
        name = f'order_w{weight:g}_m{retention:g}'
        if name in result['results']:continue
        result['results'][name] = score_record(ctx,best['donor'],best['recipe'],weight,retention)
        dump(path,result)
    refined = max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for delta in LIMIT_SHIFTS:
        name = f'limit_shift{delta:g}'
        if name in result['results']:continue
        result['results'][name] = score_record(ctx,best['donor'],best['recipe'],refined['slow16_weight'],refined['retention'],delta)
        dump(path,result)
    result['status']='complete'
    dump(path,result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=('freeze','provenance','mixtures','fine','refine','all'))
    stage = parser.parse_args().stage
    for name in (('freeze','provenance','mixtures','fine','refine') if stage=='all' else (stage,)):
        globals()[name]()


if __name__=='__main__':main()
