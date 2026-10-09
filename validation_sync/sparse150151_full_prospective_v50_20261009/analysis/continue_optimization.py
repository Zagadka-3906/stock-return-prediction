"""Training-only optimization after wave39. Keep previous releases immutable.

Freeze the protocol, reproduce the current complete scheme, search its joint
parameters, train two new Top-K seeds, compare complete ensembles, and refine
the best donor. Only the separate selected-prediction stage uses test X.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys
import time

for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[_name] = '8'

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'analysis/connected_validation_20261002'
OUT = ROOT / 'analysis/optimization_20261003'
sys.path[:0] = [str(ROOT), str(HERE)]
YEARS = (2020, 2021, 2022, 2023, 2024)
KEYS = ['ts_code', 'trade_date']
EXPECTED = 0.4459160901521865
WEIGHTS = (0.15, 0.20, 0.25, 0.30, 0.35)
RETENTION = (0.980, 0.982, 0.985, 0.988, 0.990, 0.992)
NEW_SEEDS = (2027, 2028)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def dump(path, value, immutable=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if immutable and path.exists():
        assert read(path) == value, f'Preserve existing record: {path}'
        return
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def log(message):
    print(f'[{time.strftime("%H:%M:%S")}] {message}', flush=True)


def verify_protocol():
    record = read(OUT/'protocol.json')
    for name, digest in record['source_sha256'].items():
        assert sha(ROOT/name) == digest, f'Frozen source changed: {name}'
    for name, digest in record['input_sha256'].items():
        assert sha(ROOT/name) == digest, f'Frozen input changed: {name}'
    return record


def freeze():
    if (OUT/'protocol.json').exists():
        verify_protocol()
        return
    sources = [Path(__file__), ROOT/'后续选模标准.md', ROOT/'evaluate.py', ROOT/'run.py',
               ROOT/'src/scoring.py', ROOT/'experiments/r6_topk.py',
               ROOT/'experiments/revalidate_fold_local.py']
    sources += [HERE/name for name in ('optimize_wave6.py', 'optimize_wave13.py',
                'optimize_wave15.py', 'optimize_wave18.py', 'optimize_wave31.py', 'return_mapping.py')]
    inputs = [ROOT/'data/raw/训练集.csv', ROOT/'data/features.parquet', ROOT/'data/feature_manifest.json',
              HERE/'combined_fold_frame.parquet', HERE/'connected_pred_peer67_slow16.npy',
              HERE/'orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy',
              HERE/'pp_a0_b0_top_only_w0.25_rl1_tcw1.npy',
              ROOT/'deliveries/connected_topk0175_20261003/fold_prediction.npy']
    inputs += [HERE/f'wave36_topk/raw/topk_seed2026_f0.175_{year}.parquet' for year in YEARS]
    inputs += [HERE/f'wave36_topk/raw/info_f0.175_{year}.json' for year in YEARS]
    dump(OUT/'protocol.json', {
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'user_request': '按照这个标准继续寻找优化方案',
        'primary': '2020-2024 concatenated official composite; year-boundary turnover included',
        'selection_rule': 'highest official composite among compliant complete schemes; no extra research gate',
        'baseline': EXPECTED, 'years': list(YEARS),
        'joint_search': {'donor_fraction': 0.175, 'slow16_weights': list(WEIGHTS),
                         'retention_fractions': list(RETENTION)},
        'new_models': {'seeds': list(NEW_SEEDS), 'training_topk_fraction': 0.175,
                       'rounds': 180, 'samples_per_top_stock': 8},
        'ensemble_grid': ['seed2027', 'seed2028', '2026+2027_equal', '2026+2028_equal',
                          'all3_equal', '2026_half_others_quarter'],
        'model_score_parameters': 'joint-search winner before new-seed scores are read',
        'refinement': 'best donor among all compared schemes; baseline/joint-best weight plus/minus0.05 and retention plus/minus0.003, unique Cartesian product',
        'limit_up_shift': [-0.05, 0.0, 0.05, 0.10, 0.20],
        'calibration': 'Causal prior-OOF isotonic each year after2020; first fold uses an affine map fitted from pre2020 training-label moments. Final future-period map fits all historical OOF labels. Strictly increasing maps must preserve ranks exactly.',
        'training_cutoff': 'Existing expanding fold_cutoff removes the last prevalidation trading date; training labels mature before validation starts',
        'all_validation_years_previously_viewed': True,
        'test_labels_read': False, 'test_future_prices_used_for_selection': False,
        'source_sha256': {p.relative_to(ROOT).as_posix(): sha(p) for p in sources},
        'input_sha256': {p.relative_to(ROOT).as_posix(): sha(p) for p in inputs},
    }, immutable=True)
    log('Protocol frozen before candidate scoring or new training')


class Context:
    def __init__(self):
        import numpy as np
        import pandas as pd
        import polars as pl
        import connected_scorer as cs
        from optimize_wave15 import daily_ranks
        self.frame = cs.combined_frame()
        self.label_free = self.frame.with_columns(pl.lit(None, dtype=pl.Float64).alias('y_ret_1d'))
        self.dates = self.frame['trade_date'].to_numpy()
        assert self.dates.min()//10000 == 2020 and self.dates.max()//10000 == 2024
        self.flags = self.frame['flag_limit_up'].to_numpy().astype(np.int64)
        self.valid = self.frame['price_valid'].to_numpy().astype(bool)
        self.codes, unique = pd.factorize(self.frame['ts_code'].to_pandas(), sort=True)
        self.codes = self.codes.astype(np.int64)
        self.n_codes = len(unique)
        self.tie_key = 1-self.codes/max(len(unique)-1, 1)
        self.pdf = self.frame.select(['trade_date', 'flag_limit_up']).to_pandas()
        self.slow_finished = np.load(HERE/'connected_pred_peer67_slow16.npy')
        self.w5a = np.load(HERE/'orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy')
        self.slow = np.load(HERE/'pp_a0_b0_top_only_w0.25_rl1_tcw1.npy')
        self.ranks = {'w5a': daily_ranks(self.w5a, self.valid, self.dates),
                      'slow': daily_ranks(self.slow, self.valid, self.dates)}
        self.scoring = OUT/'scoring_validation_only'
        self.scoring.mkdir(exist_ok=True)
        for name, cols in [('测试集_X.csv', KEYS+['flag_limit_up']), ('测试集_Y.csv', KEYS+['y_ret_1d'])]:
            if not (self.scoring/name).exists():
                self.frame.select(cols).write_csv(self.scoring/name, float_precision=17)

    def finish(self, raw_parts):
        import numpy as np
        import polars as pl
        from optimize_wave6 import make_prediction_param
        from src.scoring import Panel
        parts = []
        for year, raw in zip(YEARS, raw_parts):
            frame = self.label_free.filter(pl.col('trade_date').is_between(year*10000+101, year*10000+1231))
            assert len(frame) == len(raw)
            panel = Panel.from_frame(frame.with_columns(pl.Series('pred_raw', raw)))
            parts.append(make_prediction_param(panel, frame['aux_raw'].to_numpy().astype(np.float64),
                                              'top_only', 0.25, 0.9, 0.3, True, 1.0))
        return np.concatenate(parts)

    def promote(self, name):
        import numpy as np
        import polars as pl
        path = OUT/f'promote_{name}.npy'
        if path.exists():
            return np.load(path)
        raws = []
        for year in YEARS:
            raw_path = (HERE/f'wave36_topk/raw/topk_seed2026_f0.175_{year}.parquet'
                        if name == 'seed2026' else OUT/f'raw/topk_{name}_{year}.parquet')
            raw = pl.read_parquet(raw_path)
            keys = self.frame.filter(pl.col('trade_date').is_between(year*10000+101, year*10000+1231)).select(KEYS)
            assert raw.select(KEYS).equals(keys), (name, year)
            raws.append(raw['pred_raw'].to_numpy().astype(np.float64))
        pred = self.finish(raws)
        np.save(path, pred)
        return pred

    def donor(self, promote):
        import numpy as np
        from optimize_wave18 import lift
        promote = np.where(np.isfinite(promote) & (promote > -9), promote+1e-9*self.tie_key, promote)
        return lift(promote, self.slow_finished, self.pdf)[0]

    def predict(self, donor, weight, retention, delta=0.0):
        import numpy as np
        from optimize_wave15 import weighted_rank_blend
        from optimize_wave13 import build_ab
        blend = weighted_rank_blend([self.w5a, self.slow], [1-weight, weight], self.ranks,
                                    self.valid, self.dates, ('w5a', 'slow'))
        orderer = np.where(blend > -9, blend+1e-9*self.tie_key, blend)+1e-9*self.tie_key
        pred, stats = build_ab(donor, orderer, orderer, self.dates, self.flags,
                               self.codes, self.n_codes, retention)
        pred[self.flags == 1] += delta
        return pred, stats

    def score(self, pred):
        import polars as pl
        from evaluate import evaluate
        self.frame.select(KEYS).with_columns(pl.Series('pred', pred)).write_csv(
            self.scoring/'submission.csv', float_precision=17)
        return {k: float(v) for k,v in evaluate(str(self.scoring/'submission.csv'), str(self.scoring)).items()}


def joint():
    import numpy as np
    verify_protocol()
    ctx = Context()
    donor = ctx.donor(ctx.promote('seed2026'))
    result_path = OUT/'wave40_results.json'
    result = read(result_path) if result_path.exists() else {'status': 'running', 'results': {}}
    baseline, _ = ctx.predict(donor, 0.25, 0.985)
    assert np.array_equal(baseline, np.load(ROOT/'deliveries/connected_topk0175_20261003/fold_prediction.npy'))
    got = ctx.score(baseline)
    assert abs(got['final_score']-EXPECTED) < 1e-12
    result['harness'] = {'prediction_bit_identical': True, 'official_score': got['final_score']}
    for weight, retention in itertools.product(WEIGHTS, RETENTION):
        name = f'w{weight:.3f}_m{retention:.3f}'
        if name in result['results']:
            continue
        pred, stats = ctx.predict(donor, weight, retention)
        metrics = got if (weight, retention) == (0.25, 0.985) else ctx.score(pred)
        item = {'donor': 'seed2026', 'slow16_weight': weight, 'retention': retention, 'limit_up_delta': 0.0,
                'connected_final_score': metrics['final_score'], 'metrics': metrics, 'construction': stats}
        result['results'][name] = item
        dump(result_path, result)
        log(f'wave40 {name}: {metrics["final_score"]:.9f} delta={metrics["final_score"]-EXPECTED:+.9f}')
    result['status'] = 'complete'
    result['best'] = max(result['results'], key=lambda k: result['results'][k]['connected_final_score'])
    dump(result_path, result)
    dump(OUT/'model_comparison_parameters.json', result['results'][result['best']], immutable=True)
    log(f'wave40 completed; best={result["best"]}')


def train():
    import numpy as np
    import polars as pl
    import lightgbm as lgb
    import experiments.r6_topk as rt
    from optimize_wave31 import ObjectiveFrac
    from run import to_matrix, FEATURE_FILE, feature_names
    verify_protocol()
    for year in YEARS:
        paths = [OUT/f'raw/topk_seed{seed}_{year}.parquet' for seed in NEW_SEEDS]
        if all(path.exists() for path in paths):
            for path in paths:
                assert sha(path) == read(path.with_suffix('.json'))['prediction_sha256']
            continue
        frame, features, meta = rt.training_frame(year)
        assert meta['last_date'] < meta['training_cutoff_exclusive'] < year*10000+101
        labels, dates = frame['y_ret_1d'].to_numpy(), frame['trade_date'].to_numpy()
        x = to_matrix(frame, features)
        del frame
        gc.collect()
        valid = (pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train') & pl.col('trade_date').is_between(
            year*10000+101, year*10000+1231)).select(KEYS+feature_names()+['price_valid']).sort('trade_date','ts_code').collect())
        vx = to_matrix(valid, features)
        for seed, path in zip(NEW_SEEDS, paths):
            if path.exists():
                assert sha(path) == read(path.with_suffix('.json'))['prediction_sha256']
                continue
            objective = ObjectiveFrac(dates, labels, seed, 0.175, 8)
            ds = lgb.Dataset(x, label=np.zeros(len(x), dtype=np.float32), feature_name=features, free_raw_data=True)
            params = dict(rt.PARAMS, seed=seed, objective=rt.objective_callback(objective))
            start = time.monotonic()
            def progress(env):
                if (env.iteration+1)%30 == 0:
                    log(f'seed{seed} {year}: {env.iteration+1}/180, {time.monotonic()-start:.0f}s')
            model = lgb.train(params, ds, num_boost_round=180, callbacks=[progress])
            assert model.current_iteration() == objective.iteration == 180
            raw = model.predict(vx, num_threads=8).astype(np.float64)
            raw[~valid['price_valid'].to_numpy()] = -1e6
            path.parent.mkdir(exist_ok=True)
            valid.select(KEYS).with_columns(pl.Series('pred_raw', raw)).write_parquet(path, compression='zstd')
            model_path = path.with_suffix('.txt')
            model_path.write_text(model.model_to_string(), encoding='utf-8')
            reload = lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
            replay = reload.predict(vx, num_threads=8).astype(np.float64)
            replay[~valid['price_valid'].to_numpy()] = -1e6
            assert np.array_equal(raw, replay)
            dump(path.with_suffix('.json'), {'year': year, 'seed': seed, 'fraction': 0.175, 'rounds':180,
                  'training_meta':meta, 'fit_seconds':round(time.monotonic()-start, 1),
                  'prediction_sha256':sha(path), 'model_sha256':sha(model_path),
                  'model_reload_bit_identical':True, 'validation_labels_used_in_fit':False}, immutable=True)
            log(f'seed{seed} {year}: saved and reloaded bit-identically')
            del ds, objective, model, reload, raw, replay
            gc.collect()
        del x, vx, valid, dates, labels
        gc.collect()


def models():
    import numpy as np
    from optimize_wave15 import daily_ranks
    verify_protocol()
    setting = read(OUT/'model_comparison_parameters.json')
    ctx = Context()
    seeds = {seed: ctx.promote(f'seed{seed}') for seed in (2026, *NEW_SEEDS)}
    ranks = {seed: daily_ranks(value, ctx.valid, ctx.dates) for seed,value in seeds.items()}
    patterns = {'seed2027': {2027:1.0}, 'seed2028': {2028:1.0},
                '2026+2027_equal': {2026:0.5,2027:0.5}, '2026+2028_equal': {2026:0.5,2028:0.5},
                'all3_equal': {2026:1/3,2027:1/3,2028:1/3},
                '2026_half_others_quarter': {2026:0.5,2027:0.25,2028:0.25}}
    result_path = OUT/'wave41_results.json'
    result = read(result_path) if result_path.exists() else {'status':'running', 'results':{}}
    for name, weights in patterns.items():
        if name in result['results']:
            continue
        if len(weights) == 1:
            promote = seeds[next(iter(weights))]
        else:
            promote = sum(ranks[seed]*weight for seed,weight in weights.items())
            promote[~ctx.valid] = -10.0
        np.save(OUT/f'promote_{name}.npy', promote)
        pred, stats = ctx.predict(ctx.donor(promote), setting['slow16_weight'], setting['retention'])
        metrics = ctx.score(pred)
        result['results'][name] = {**setting, 'donor':name, 'seed_weights':weights,
                                  'connected_final_score':metrics['final_score'], 'metrics':metrics,
                                  'construction':stats}
        dump(result_path, result)
        log(f'wave41 {name}: {metrics["final_score"]:.9f} delta={metrics["final_score"]-EXPECTED:+.9f}')
    result['status'] = 'complete'
    dump(result_path, result)


def refine():
    verify_protocol()
    ctx = Context()
    all_items = []
    for wave in (40,41):
        r = read(OUT/f'wave{wave}_results.json')
        assert r['status'] == 'complete'
        all_items += list(r['results'].values())
    winner = max(all_items, key=lambda r:r['connected_final_score'])
    base = read(OUT/'model_comparison_parameters.json')
    weights = sorted({0.25, base['slow16_weight'], *[round(winner['slow16_weight']+v, 3) for v in (-0.05,0,0.05)]})
    retention = sorted({0.985, base['retention'], *[round(winner['retention']+v, 3) for v in (-0.003,0,0.003)]})
    refinement_protocol = {'donor':winner['donor'], 'weights':weights, 'retention':retention,
                           'chosen_before_refinement_scores':True}
    dump(OUT/'refinement_protocol.json', refinement_protocol, immutable=True)
    donor = ctx.donor(ctx.promote(winner['donor']))
    result_path = OUT/'wave42_results.json'
    result = read(result_path) if result_path.exists() else {'status':'running', 'results':{}}
    for weight, keep in itertools.product(weights, retention):
        name = f'{winner["donor"]}_w{weight:.3f}_m{keep:.3f}'
        if name in result['results']:
            continue
        pred, stats = ctx.predict(donor, weight, keep)
        metrics = ctx.score(pred)
        result['results'][name] = {**winner, 'slow16_weight':weight, 'retention':keep,
             'connected_final_score':metrics['final_score'], 'metrics':metrics, 'construction':stats}
        dump(result_path, result)
        log(f'wave42 {name}: {metrics["final_score"]:.9f} delta={metrics["final_score"]-EXPECTED:+.9f}')
    winner = max(result['results'].values(), key=lambda r:r['connected_final_score'])
    for delta in (-0.05,0.0,0.05,0.10,0.20):
        name = f'limit_up_delta{delta:+.2f}'
        if name in result['results']:
            continue
        pred, stats = ctx.predict(donor, winner['slow16_weight'], winner['retention'], delta)
        metrics = ctx.score(pred)
        result['results'][name] = {**winner, 'limit_up_delta':delta,
             'connected_final_score':metrics['final_score'], 'metrics':metrics, 'construction':stats}
        dump(result_path, result)
        log(f'wave42 {name}: {metrics["final_score"]:.9f}')
    result['status'] = 'complete'
    dump(result_path, result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('freeze','joint','train','models','refine'))
    args = parser.parse_args()
    globals()[args.stage]()


if __name__ == '__main__':
    main()
