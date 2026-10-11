"""Exercise actual past data, linear coefficients, saved native models and causality."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
import train_linear_leaf_bank_20261005 as bank


def manual_native_prediction(booster, values):
    """Reconstruct predictions from dumped leaves and native leaf assignments."""
    import numpy as np
    assignments = booster.predict(values, pred_leaf=True, num_threads=1)
    trees = booster.dump_model()['tree_info']
    assert assignments.shape == (len(values), len(trees))
    result = np.zeros(len(values), dtype=np.float64)
    for index, tree in enumerate(trees):
        nodes, leaves = [tree['tree_structure']], {}
        while nodes:
            node = nodes.pop()
            if 'split_index' in node:
                nodes.extend((node['left_child'], node['right_child']))
            else:
                leaves[node['leaf_index']] = node
        for row, leaf_index in enumerate(assignments[:, index]):
            leaf = leaves[int(leaf_index)]
            features = leaf.get('leaf_features', [])
            if features and np.isfinite(values[row, features]).all():
                result[row] += leaf['leaf_const'] + sum(
                    float(values[row, feature]) * coefficient
                    for feature, coefficient in zip(features, leaf['leaf_coeff']))
            else:
                result[row] += leaf['leaf_value']
    return result


def main():
    import lightgbm as lgb
    import numpy as np
    import polars as pl
    out = ROOT / 'analysis/linear_leaf_preflight_20261005'
    out.mkdir(exist_ok=True)
    if (out / 'verification.json').exists():
        proof = bank.read(out / 'verification.json')
        for source, expected in proof['source_sha256'].items():
            assert bank.sha(source) == expected, source
        return proof
    paths = [Path(__file__), Path(bank.__file__), bank.SOURCE, bank.STORAGE,
        bank.engine.FEATURE_FILE, bank.engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    frozen = {str(p.resolve()): bank.sha(p) for p in paths}
    bank.dump(out / 'frozen_before_controls.json', {'status': 'frozen_before_actual_controls',
        'configurations': bank.CONFIGS, 'input_sha256': frozen,
        'new_quality_scores': 0, 'test_data_read': False}, immutable=True)
    features = bank.engine.feature_names()
    lazy = pl.scan_parquet(bank.engine.FEATURE_FILE)
    cutoff = bank.engine.fold_cutoff(2020)
    controls, predictions = [], {}
    for name, cfg in bank.CONFIGS.items():
        past = bank.engine.training_frame(lazy, cutoff, cfg).select(
            bank.engine.KEYS + features + [cfg['target']]).head(4096).collect()
        assert len(past) == 4096 and int(past['trade_date'].max()) < cutoff
        x, y = bank.engine.to_matrix(past, features), past[cfg['target']].to_numpy()
        pilot = dict(cfg, num_boost_round=48)
        bundle = bank.fit_arrays(x, y, pilot)
        values = bank.predict_arrays(bundle, x)
        assert np.isfinite(values).all()
        model = out / f'{name}.joblib'
        bank.engine.save_bundle(model, bundle)
        assert np.array_equal(values, bank.predict_arrays(bank.engine.load_bundle(model), x))
        counts = (1, 80, 257, 1024, 4095)
        assert all(np.array_equal(values[:count], bank.predict_arrays(bundle, x[:count])) for count in counts)
        probe = x[:128].copy()
        probe[::5, 2] = np.nan
        probe[::7, 5] = np.inf
        probe[::11, 8] = bundle['mean'][8]
        z = bank.standardize(probe, bundle['mean'], bundle['scale'], pilot)
        assert np.isnan(z[::5, 2]).all() and np.isnan(z[::7, 5]).all()
        # A valid value at the past mean yields a valid zero, never a missing sentinel.
        assert np.isfinite(z[::11, 8]).all()
        booster = lgb.Booster(model_str=bundle['model_string'])
        expected = manual_native_prediction(booster, z)
        actual = bank.predict_arrays(bundle, probe)
        manual_error = float(np.max(np.abs(expected - actual)))
        assert np.isfinite(actual).all() and manual_error < 1e-10, (name, manual_error)
        maturity = bank.boundary_control(2020, cfg, features)
        assert maturity['status'] == 'passed'
        controls.append({'model': name, 'actual_past_rows': len(past),
            'training_keys_sha256': bank.engine.array_hash(past.select(bank.engine.KEYS).hash_rows(seed=2026).to_numpy()),
            'training_matrix_sha256': bank.engine.array_hash(x), 'training_target_sha256': bank.engine.array_hash(y),
            'actual48_round_native_leaf_summary': bundle['leaf_summary'],
            'dumped_leaf_formula_and_missing_fallback_max_abs_error': manual_error,
            'reload_and_prefix_counts_bit_identical': counts,
            'missing_values_preserved_and_valid_zero_not_missing': True,
            'actual_future_label_poison_maturity_control': maturity,
            'model_sha256': bank.sha(model), 'new_actual_annual_fits': 0})
        predictions[name] = values
        print('Actual linear-leaf controls passed: ' + name, flush=True)
        del past, x, y, bundle, booster
        bank.engine.gc.collect()
    for label in ('rank', 'return'):
        group = [predictions[f'{label}_lgb_{suffix}_r300'] for suffix in ('constant', 'linear_l1', 'linear_l10')]
        assert all(not np.array_equal(group[a], group[b]) for a, b in ((0, 1), (0, 2), (1, 2)))
    for path, expected in frozen.items():
        assert bank.sha(path) == expected, path
    proof = {'status': 'passed_actual_linear_leaf_maturity_native_reload_and_prefix_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'controls': controls, 'source_sha256': frozen,
        'configurations': len(bank.CONFIGS), 'actual_annual_fits': 0,
        'actual4096_row48_round_pilots_and_poison_controls_only': True,
        'both_targets_all_three_matched_configurations_produce_distinct_predictions': True,
        'new_quality_scores': 0, 'test_data_read': False}
    bank.dump(out / 'verification.json', proof, immutable=True)
    return proof


if __name__ == '__main__':
    main()
