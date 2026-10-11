"""Validate prospective whole-scheme layer replay against frozen real methods."""
from copy import copy, deepcopy
from pathlib import Path
import ast
import hashlib
import importlib
import json
import os
import sys
import time
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[variable] = '8'
ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'analysis/connected_validation_20261002'
sys.path[:0] = [str(ROOT), str(ROOT/'analysis'), str(HERE)]
import numpy as np
import pandas as pd
import polars as pl
from optimize_wave15 import daily_ranks
from role_layer_replay_20261004 import finish_layer, replay_layers, ROLES

OUT = ROOT/'analysis/role_layer_replay_preflight_20261004'
METHODS = [(25, 'final'), (29, 'linear'), (31, 'regularization'),
           (33, 'stacking'), (35, 'neural_tuning'), (37, 'catboost_tuning'),
           (39, 'expanded_stacking'), (41, 'additive_ridge'),
           (43, 'fourier_ridge'), (45, 'nonlinear_stacking'), (47, 'fourier_tuning')]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, payload):
    assert not path.exists(), path
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


class Context:
    def __init__(self, frame):
        self.frame = frame
        self.dates = frame['trade_date'].to_numpy()
        self.flags = frame['flag_limit_up'].to_numpy().astype(np.int64)
        self.valid = frame['price_valid'].to_numpy()
        self.codes, symbols = pd.factorize(frame['ts_code'].to_numpy(), sort=True)
        self.codes = self.codes.astype(np.int64)
        self.n_codes = len(symbols)
        self.tie_key = 1. - self.codes / max(self.n_codes - 1, 1)
        self.cache = {}
        self.regimes = {}

    def signal(self, name):
        n = len(self.dates)
        if name not in self.cache:
            raw = np.load(ROOT/f'analysis/optimization_20261003_r25/raw/{name}.npy', mmap_mode='r')[:n]
            self.cache[name] = daily_ranks(raw, self.valid, self.dates)
        return self.cache[name]

    def weights_for(self, spec):
        if not spec.get('regime'):
            return spec['weight']
        name = spec['regime']
        if name not in self.regimes:
            self.regimes[name] = np.load(ROOT/f'analysis/market_regime_bank_20261003/{name}.npy', mmap_mode='r')[:len(self.dates)]
        return (spec['low'] + (spec['high']-spec['low'])*self.regimes[name])*(spec['weight']/max(spec['low'], spec['high']))


def legacy(context, base, layer, number, group):
    module = importlib.import_module(f'optimize_training_round{number}')
    setattr(context, group+'_augmentation', deepcopy(layer['specs']))
    setattr(context, group+'_limit_delta', layer['additional_delta'])
    return module.Context.finish_output(context, base, layer['retention'], layer['original_delta'])


def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'verification.json').exists():
        print((OUT/'verification.json').read_text(encoding='utf-8')); return
    sources = [Path(__file__), ROOT/'analysis/role_layer_replay_20261004.py',
               HERE/'optimize_wave13.py', HERE/'optimize_wave15.py',
               ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet',
               ROOT/'analysis/optimization_20261003_r24/selected_validation.npy',
               ROOT/'analysis/optimization_20261003_r25/selected_validation.npy',
               ROOT/'analysis/optimization_20261003_r25/selection.json',
               ROOT/'analysis/market_regime_bank_20261003/return_dispersion.npy']
    names = ('tail_bce128_e32', 'rank512_seed18_e64')
    sources += [ROOT/f'analysis/optimization_20261003_r25/raw/{name}.npy' for name in names]
    sources += [ROOT/f'analysis/optimize_training_round{number}.py' for number, _ in METHODS]
    inputs = {str(path.resolve()): sha(path) for path in sources}
    dump(OUT/'frozen_before_controls.json', {'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'input_sha256':inputs, 'test_labels_read':False, 'new_quality_scores':0})
    # Check the reference layer implementations really have the same algebra,
    # rather than assuming this from similarly named classes.
    normalized = []
    for number, group in METHODS:
        source = (ROOT/f'analysis/optimize_training_round{number}.py').read_text(encoding='utf-8-sig')
        tree = ast.parse(source)
        method = next(method for node in tree.body if isinstance(node, ast.ClassDef) and node.name=='Context'
                      for method in node.body if isinstance(method, ast.FunctionDef) and method.name=='finish_output')
        snippet = ast.get_source_segment(source, method).replace(group+'_augmentation', 'generic_augmentation').replace(group+'_limit_delta', 'generic_limit_delta')
        normalized.append(ast.dump(ast.parse(snippet), include_attributes=False))
    assert len(set(normalized)) == 1
    frame = pl.read_parquet(ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet',
                            columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
    context = Context(frame)
    foundation = np.load(ROOT/'analysis/optimization_20261003_r24/selected_validation.npy', mmap_mode='r')
    winner = json.loads((ROOT/'analysis/optimization_20261003_r25/selection.json').read_text(encoding='utf-8'))['winner']
    empty = {role:{'model':'none','weight':0.} for role in ROLES}
    selected = {'name':'selected_r25', 'specs':winner['final_augmentation'], 'retention':winner['retention'],
                'original_delta':winner['limit_up_delta'], 'additional_delta':winner['final_limit_delta']}
    cases = [selected, {'name':'inactive_shift', 'specs':empty, 'retention':.984, 'original_delta':.075, 'additional_delta':.004}]
    for membership, state in ((0.,False),(.1,False),(.1,True)):
        specs = deepcopy(empty)
        for role, weight, name in (('membership',membership,names[0]),('top',.1,names[1]),('rest',.25,names[1])):
            specs[role] = {'model':name, 'weight':weight}
            if state:
                specs[role].update(regime='return_dispersion',low=0.,high=.25)
        cases.append({'name':f'roles_membership{membership}_state{state}', 'specs':specs,
                      'retention':.984, 'original_delta':.075, 'additional_delta':.004})
    records = []
    dates = np.unique(context.dates)
    for layer in cases:
        actual, stats = finish_layer(context, foundation, layer['specs'], layer['retention'], layer['original_delta'], layer['additional_delta'])
        references = []
        for number, group in METHODS:
            expected, expected_stats = legacy(context, foundation, layer, number, group)
            assert np.array_equal(actual, expected), (layer['name'], number)
            assert stats == expected_stats
            references.append(number)
        if layer['name']=='selected_r25':
            assert np.array_equal(actual, np.load(ROOT/'analysis/optimization_20261003_r25/selected_validation.npy', mmap_mode='r'))
        poisoned = copy(context)
        poisoned.frame = frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
        assert np.array_equal(actual, finish_layer(poisoned, foundation, layer['specs'], layer['retention'], layer['original_delta'], layer['additional_delta'])[0])
        prefixes = []
        for count in (80,260,975):
            n = int(np.searchsorted(context.dates, dates[count-1], side='right'))
            prefix = Context(frame.head(n))
            result, _ = finish_layer(prefix, foundation[:n], layer['specs'], layer['retention'], layer['original_delta'], layer['additional_delta'])
            assert np.array_equal(actual[:n], result), (layer['name'],count)
            prefixes.append({'days':count, 'cold_signal_and_regime_caches':True, 'bit_identical':True})
        records.append({'case':layer['name'], 'all_11_legacy_layers_exact':references,
                        'label_poisoning_exact':True, 'prefixes':prefixes})
        print(json.dumps(records[-1], ensure_ascii=False), flush=True)
    chain = [deepcopy(cases[2]), deepcopy(cases[3]), deepcopy(cases[4])]
    for index, layer in enumerate(chain):
        layer['name'] = f'chain_{index}'
        layer['original_delta'] = .075 + index*.004
    actual, _ = replay_layers(context, foundation, chain)
    reference = foundation
    for layer, (number, group) in zip(chain, METHODS):
        reference, _ = legacy(context, reference, layer, number, group)
    assert np.array_equal(actual, reference)
    prefixes = []
    for count in (80,260,975):
        n = int(np.searchsorted(context.dates, dates[count-1], side='right'))
        result, _ = replay_layers(Context(frame.head(n)), foundation[:n], chain)
        assert np.array_equal(actual[:n], result)
        prefixes.append({'days':count, 'bit_identical':True})
    for path,digest in inputs.items():
        assert sha(path)==digest,path
    dump(OUT/'verification.json', {'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'validation_rows':len(frame), 'validation_days':len(dates), 'single_layers':records,
         'three_changed_layers_recomputed':True, 'chain_prefixes':prefixes,
         'reference_implementations_ast_equivalent':True, 'selected_r25_output_bit_identical':True,
         'new_quality_scores':0,'test_labels_read':False,'input_sha256':inputs,
         'scope':'Prospective layer kernel only; no claim that full R49 recipe or future inference has been reconstructed.'})
    print('Role-layer replay preflight passed', flush=True)


if __name__=='__main__':
    main()
