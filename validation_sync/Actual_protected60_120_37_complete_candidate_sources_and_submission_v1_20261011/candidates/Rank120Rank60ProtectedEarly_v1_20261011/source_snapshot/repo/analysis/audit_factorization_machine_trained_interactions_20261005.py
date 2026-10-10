"""Independently replay all complete annual FM models as explicit feature pairs."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
import train_factorization_machine_bank_20261005 as bank

OUT = ROOT / 'analysis/factorization_machine_trained_interaction_audit_20261005'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    import numpy as np
    import polars as pl

    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'frozen_before_controls.json').exists()
    protocol_path = bank.OUT / 'protocol.json'
    protocol = bank.read(protocol_path)
    features = protocol['features']
    assert len(features) == 63 and protocol['configurations'] == bank.CONFIGS
    bindings = {str(Path(__file__).resolve()): sha(__file__),
                str(protocol_path.resolve()): sha(protocol_path),
                str(bank.STORAGE.resolve()): sha(bank.STORAGE)}
    bindings.update(protocol['input_sha256'])
    # These are actual files, including the original training-only data identity.
    for source, expected in bindings.items():
        assert sha(source) == expected, source
    bank.dump(OUT / 'frozen_before_controls.json', {
        'status': 'frozen_before_independent_complete_model_pair_formula_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': bindings, 'expected_complete_annual_models': 30,
        'real_validation_X_rows_per_model': 131,
        'independent_standardization_and_explicit_offdiagonal_pairs': True,
        'does_not_fit_models_or_select_hyperparameters': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    pending = {(name, year) for name in bank.CONFIGS for year in bank.YEARS}
    probes, predictions, controls, artifacts = {}, {}, [], {}
    while pending:
        ready = sorted((name, year) for name, year in pending
                       if (bank.OUT / name / f'info_{year}.json').exists())
        if not ready:
            time.sleep(5)
            continue
        for name, year in ready:
            info_path = bank.OUT / name / f'info_{year}.json'
            info = bank.read(info_path)
            cfg = bank.CONFIGS[name]
            assert info['status'] == 'passed' and info['new_model_fits'] == 1
            assert info['configuration'] == cfg and info['completed_training_epochs'] == 32
            reference = bank.read(ROOT / 'analysis/linear_bank_20261003' /
                                  ('rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01') /
                                  f'info_{year}.json')
            for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end',
                        'features', 'training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256'):
                assert info['training_meta'][key] == reference['training_meta'][key], (name, year, key)
            model_path = info_path.parent / f'model_{year}.joblib'
            raw_path = info_path.parent / f'raw_{year}.parquet'
            assert sha(model_path) == info['model_sha256']
            assert sha(raw_path) == info['prediction_sha256']
            for source in (info_path, model_path, raw_path):
                artifacts[str(source.resolve())] = sha(source)
            bundle = bank.engine.load_bundle(model_path)
            assert bundle['kind'] == 'factorization_machine' and bundle['config'] == cfg
            assert bundle['device'] == 'cpu' and bundle['target_units'] == cfg['target']
            assert len(bundle['training_losses']) == 32 and np.isfinite(bundle['training_losses']).all()
            weights = bundle['weights']
            linear, factors = np.asarray(weights['linear'], dtype=np.float64), np.asarray(weights['factors'], dtype=np.float64)
            assert linear.shape == (63,) and factors.shape == (63, cfg['latent_factors'])
            assert sum(value.size for value in weights.values()) == 64 + 63 * cfg['latent_factors']
            assert all(np.isfinite(value).all() for value in weights.values())
            if year not in probes:
                probes[year] = pl.scan_parquet(bank.engine.FEATURE_FILE).filter(
                    pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(
                    list(dict.fromkeys(bank.engine.KEYS + features + ['price_valid']))).sort(
                    'trade_date', 'ts_code').head(131).collect()
            frame = probes[year]
            x = bank.engine.to_matrix(frame, features)
            # Do not call the production preprocessing helper in the reference formula.
            clean = np.where(np.isfinite(x), np.asarray(x, dtype=np.float64), bundle['mean'])
            z = np.clip((clean - bundle['mean']) / bundle['scale'], -cfg['clip_z'], cfg['clip_z']).astype(np.float32).astype(np.float64)
            first = np.full(len(z), float(weights['bias']), dtype=np.float64)
            for i in range(63):
                first += z[:, i] * linear[i]
            gram = factors @ factors.T
            interaction = np.zeros(len(z), dtype=np.float64)
            for i in range(63):
                for j in range(i + 1, 63):
                    interaction += gram[i, j] * z[:, i] * z[:, j]
            expected = (first + interaction) / bundle['target_scale']
            native = bank.predict_arrays(bundle, x)
            error = float(np.max(np.abs(expected - native)))
            assert error < 1e-10, (name, year, error)
            offdiagonal = gram.copy()
            np.fill_diagonal(offdiagonal, 0.)
            energy = float(np.linalg.norm(offdiagonal))
            if cfg['latent_factors'] == 0:
                assert energy == 0. and np.array_equal(interaction, np.zeros(len(z)))
            else:
                assert energy > 0. and np.any(interaction != 0.)
            native[~frame['price_valid'].to_numpy()] = -1e6
            saved = pl.scan_parquet(raw_path).sort('trade_date', 'ts_code').head(131).collect()
            assert frame.select(bank.engine.KEYS).equals(saved.select(bank.engine.KEYS))
            assert np.array_equal(native, saved['pred_raw'].to_numpy())
            predictions[(name, year)] = native
            controls.append({'model': name, 'year': year, 'actual_complete_training_rows': info['training_meta']['rows'],
                             'completed_training_epochs': 32, 'actual_parameter_count': bundle['actual_parameter_count'],
                             'explicit_feature_pair_max_error': error, 'offdiagonal_interaction_coefficient_norm': energy,
                             'raw_actual131_row_saved_prediction_bit_identical': True,
                             'past_rows_targets_and_keys_sha256_match_first_order_reference': True})
            pending.remove((name, year))
            print(f'Actual complete model interaction replay passed: {name}/{year}; remaining={len(pending)}', flush=True)
    for label in ('rank', 'return'):
        for year in bank.YEARS:
            group = [predictions[(f'{label}_fm_k{k}_e32', year)] for k in (0, 8, 32)]
            assert all(not np.array_equal(group[a], group[b]) for a, b in ((0, 1), (0, 2), (1, 2)))
    scope_path = bank.OUT / 'training_execution_scope.json'
    while not scope_path.exists():
        time.sleep(5)
    assert bank.read(scope_path)['status'] == 'passed'
    artifacts[str(scope_path.resolve())] = sha(scope_path)
    for source, expected in {**bindings, **artifacts}.items():
        assert sha(source) == expected, source
    bank.dump(OUT / 'verification.json', {
        'status': 'passed_all30_actual_complete_models_independent_pair_formula_and_saved_predictions',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source_sha256': bindings,
        'artifact_sha256': artifacts, 'actual_complete_annual_model_count': 30, 'controls': controls,
        'first_order_has_zero_offdiagonal_interactions': True,
        'both_second_order_ranks_have_nonzero_interactions_for_each_year_and_target': True,
        'all_three_factor_ranks_distinct_for_each_year_and_target': True,
        'diagnostic_is_not_a_quality_selection_gate': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
