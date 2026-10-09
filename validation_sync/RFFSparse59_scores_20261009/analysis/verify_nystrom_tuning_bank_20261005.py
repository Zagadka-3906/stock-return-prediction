"""Independent library algebra and actual mature-row admission for every new contrast."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
import train_nystrom_tuning_bank_20261005 as bank


def main():
    import numpy as np
    from sklearn.kernel_approximation import Nystroem
    from sklearn.linear_model import Ridge
    out = ROOT / 'analysis/nystrom_tuning_preflight_20261005'
    out.mkdir(exist_ok=True)
    paths = [Path(__file__), Path(bank.__file__), bank.SOURCE, bank.native.SOURCE, bank.STORAGE,
             bank.engine.FEATURE_FILE, bank.engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
             ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    frozen = {str(p.resolve()): bank.sha(p) for p in paths}
    bank.dump(out / 'frozen_before_controls.json', {'status': 'frozen_before_controls',
        'configurations': bank.CONFIGS, 'input_sha256': frozen,
        'new_quality_scores': 0, 'test_data_read': False}, immutable=True)
    rng = np.random.default_rng(20261005)
    x = rng.normal(size=(33001, 63)).astype(np.float32)
    x[::17, 2] = np.nan
    x[::101, 5] = 50.
    labels = {'y_rank': rng.uniform(-.5, .5, len(x)), 'y_ret_1d': rng.normal(0, .03, len(x))}
    labels['y_ret_1d'][::1000] = 10.
    proofs = []
    for name, cfg in bank.CONFIGS.items():
        y = labels[cfg['target']]
        bundle = bank.fit_arrays(x, y, cfg)
        z = bank.native.standardize(x, bundle['mean'], bundle['scale'], cfg)
        mapper = Nystroem(kernel='rbf', gamma=bundle['gamma'], n_components=cfg['landmark_components'], random_state=cfg['seed'], n_jobs=1).fit(z)
        assert np.array_equal(mapper.component_indices_, bundle['landmark_indices'])
        assert np.array_equal(mapper.normalization_, bundle['normalization'])
        reference_x = np.concatenate([z, np.sqrt(cfg['kernel_mass']) * mapper.transform(z)], axis=1)
        actual_x = bank.native.transform(x, bundle['mean'], bundle['scale'], cfg, bundle['landmarks'], bundle['normalization'], bundle['gamma'])
        basis_error = float(np.max(np.abs(reference_x - actual_x)))
        reference_y = y if bundle['target_bounds'] is None else np.clip(y, *bundle['target_bounds'])
        reference = Ridge(alpha=cfg['ridge_lambda'] * len(x), solver='cholesky').fit(reference_x, reference_y)
        coefficient_error = float(np.max(np.abs(reference.coef_ - bundle['coefficients'])))
        prediction = bank.predict_arrays(bundle, x)
        prediction_error = float(np.max(np.abs(reference.predict(reference_x) - prediction)))
        assert basis_error < 1e-10 and coefficient_error < 1e-10 and prediction_error < 1e-9
        path = out / f'{name}.joblib'
        bank.engine.save_bundle(path, bundle)
        assert np.array_equal(prediction, bank.predict_arrays(bank.engine.load_bundle(path), x))
        counts = (1, 80, 32767, 32768, 32781)
        assert all(np.array_equal(prediction[:count], bank.predict_arrays(bundle, x[:count])) for count in counts)
        permuted = bank.fit_arrays(x, y[::-1].copy(), cfg)
        assert all(np.array_equal(bundle[key], permuted[key]) for key in ('landmark_indices', 'landmarks', 'normalization'))
        maturity = bank.engine.boundary_control(2020, cfg, bank.engine.feature_names())
        assert maturity['status'] == 'passed'
        proofs.append({'model': name, 'basis_max_abs_error': basis_error,
            'coefficient_max_abs_error': coefficient_error, 'prediction_max_abs_error': prediction_error,
            'reload_and_prefix_counts_bit_identical': counts,
            'landmark_basis_unchanged_by_label_permutation': True,
            'actual2020_mature_boundary_control': maturity})
        print('Tuned Nyström numerical and actual maturity control passed: ' + name, flush=True)
        del bundle, z, mapper, reference_x, actual_x, reference, prediction, permuted
        bank.engine.gc.collect()
    for path, digest in frozen.items():
        assert bank.sha(Path(path)) == digest, path
    bank.dump(out / 'verification.json', {
        'status': 'passed_independent_numerical_and_actual_maturity_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'controls': proofs,
        'source_sha256': frozen, 'configurations': len(bank.CONFIGS),
        'actual_annual_fits': 0, 'synthetic_fit_and_actual4096_row_pilots_only': True,
        'new_quality_scores': 0, 'test_data_read': False}, immutable=True)


if __name__ == '__main__':
    main()
