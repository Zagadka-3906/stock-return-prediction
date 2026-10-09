"""Prespecified kernel capacity, lengthscale and penalty contrasts; past-only fits."""
from pathlib import Path
import importlib.util
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
SOURCE = ROOT / 'analysis/train_nystrom_ridge_bank_20261004.py'
spec = importlib.util.spec_from_file_location('isolated_nystrom_tuning_native_20261005', SOURCE)
native = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = native
spec.loader.exec_module(native)
engine = native.engine
read, dump, sha, log = native.read, native.dump, native.sha, native.log
STORAGE = ROOT / 'analysis/nystrom_tuning_storage_20261005.json'
OUT = Path(read(STORAGE)['output_directory']) if STORAGE.exists() else ROOT / 'analysis/nystrom_tuning_bank_20261005'
YEARS = native.YEARS
CONTRASTS = (
    ('n256_s1_l01', 256, 1., .1),
    ('n128_s05_l01', 128, .5, .1),
    ('n128_s2_l01', 128, 2., .1),
    ('n128_s1_l0001', 128, 1., .001),
    ('n128_s1_l1', 128, 1., 1.),
)
CONFIGS = {}
for label, target in (('rank', 'y_rank'), ('return', 'y_ret_1d')):
    for suffix, components, lengthscale, penalty in CONTRASTS:
        CONFIGS[f'{label}_nystrom_tune_{suffix}'] = {
            **next(iter(native.CONFIGS.values())), 'target': target,
            'landmark_components': components, 'lengthscale': lengthscale,
            'ridge_lambda': penalty, 'reserve_available_ram_GiB': 14.,
        }
native.OUT = engine.OUT = OUT
native.CONFIGS = engine.CONFIGS = CONFIGS
fit_arrays, predict_arrays = native.fit_arrays, native.predict_arrays


def verify():
    return engine.verify()


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'protocol.json').exists():
        verify()
        return
    storage = read(STORAGE)
    assert storage['status'] == 'selected_authorized_data_drive' and Path(storage['output_directory']) == OUT
    assert OUT.drive.upper() in ('D:', 'E:')
    proof = ROOT / 'analysis/nystrom_tuning_preflight_20261005/verification.json'
    assert read(proof)['status'] == 'passed_independent_numerical_and_actual_maturity_controls'
    sources = [Path(__file__), SOURCE, native.SOURCE, engine.FEATURE_FILE, engine.MANIFEST,
               ROOT / 'data/raw/训练集.csv', ROOT / 'run.py', ROOT / 'src/features.py',
               ROOT / '后续选模标准.md', STORAGE, proof,
               ROOT / 'analysis/verify_nystrom_tuning_bank_20261005.py',
               ROOT / 'analysis/prepare_nystrom_tuning_bank_20261005.py']
    sources += [ROOT / 'analysis/linear_bank_20261003' / name / f'info_{year}.json'
                for name in ('rank_ridge_l01', 'return_ridge_l01') for year in YEARS]
    dump(OUT / 'protocol.json', {
        'status': 'frozen_before_new_annual_fits_and_quality_scores',
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'configurations': CONFIGS, 'years': YEARS, 'features': engine.feature_names(),
        'expected_annual_fits': len(CONFIGS) * len(YEARS), 'expected_configurations': len(CONFIGS),
        'validation': 'Annual expanding 2020–2024; matching original mature one-day label purge.',
        'contrast': 'One axis at a time versus original128 landmarks, lengthscale1, lambda.1, seed20261004; rank and return targets. No selected new parameter before quality scoring.',
        'preprocessing': 'Unchanged past-fold raw63 mean/std/imputation, clip8; sampled past-row RBF basis, sqrt128 kernel mass; past return quantiles only.',
        'adaptive_search_context': 'R61 role comparisons already inspected; new grid is prespecified after these findings. Reused annual OOF selection bias remains uncorrected.',
        'quality_adoption_requires_complete_output_official_scoring_and_full_checks': True,
        'all_temp_and_outputs_on_authorized_D_or_E_drive': True,
        'reserve14GiB_is_scheduling_policy_not_physical_capacity_boundary': True,
        'test_data_read': False, 'new_quality_scores': 0,
        'input_sha256': {str(p.resolve()): sha(p) for p in sources}}, immutable=True)


def all_oof():
    import numpy as np
    import polars as pl
    import psutil
    freeze()
    features = engine.feature_names()
    proofs = {}
    for name, cfg in CONFIGS.items():
        for year in YEARS:
            while not (OUT / name / f'info_{year}.json').exists() and psutil.virtual_memory().available < cfg['reserve_available_ram_GiB'] * 2**30:
                time.sleep(10)
            boundary = OUT / f'boundary_control_{name}_{year}.json'
            if not boundary.exists():
                dump(boundary, engine.boundary_control(year, cfg, features), immutable=True)
            info = native.train_one(name, year)
            reference = ROOT / 'analysis/linear_bank_20261003' / ('rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01') / f'info_{year}.json'
            baseline = read(reference)
            for field in ('training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256'):
                assert info['training_meta'][field] == baseline['training_meta'][field], field
            prefix_path = OUT / f'prefix_control_{name}_{year}.json'
            if not prefix_path.exists():
                frame = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix = frame.filter(pl.col('trade_date') <= cutoff)
                predictions = predict_arrays(engine.load_bundle(OUT / name / f'model_{year}.joblib'), engine.to_matrix(prefix, features))
                predictions[~prefix['price_valid'].to_numpy()] = -1e6
                saved = pl.read_parquet(OUT / name / f'raw_{year}.parquet').filter(pl.col('trade_date') <= cutoff)
                assert prefix.select(engine.KEYS).equals(saved.select(engine.KEYS))
                assert np.array_equal(predictions, saved['pred_raw'].to_numpy())
                dump(prefix_path, {'status': 'passed', 'rows': len(prefix),
                    'actual_saved_model80_day_prefix_bit_identical': True,
                    'training_matrix_target_andkeys_match_original_mature_reference': True,
                    'reference_info_sha256': sha(reference), 'test_data_read': False}, immutable=True)
                del frame, prefix, predictions, saved
                engine.gc.collect()
            proofs[f'{name}_{year}'] = {'boundary': read(boundary), 'actual_prefix': read(prefix_path)}
    verify()
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'configurations': CONFIGS, 'years': YEARS,
        'boundary_controls': proofs, 'actual_annual_fits': len(CONFIGS) * len(YEARS),
        'new_quality_scores': 0, 'test_data_read': False,
        'fulltraining_future_and_complete_output_quality_not_yet_completed': True}, immutable=True)


if __name__ == '__main__':
    all_oof()
