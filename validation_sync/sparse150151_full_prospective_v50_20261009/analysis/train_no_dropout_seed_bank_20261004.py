"""Matched seed/epoch extensions of the actually selected no-dropout signal."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
SOURCE = ROOT / 'analysis/train_diverse_backbones_20261003.py'
spec = importlib.util.spec_from_file_location('isolated_no_dropout_seed_trainer_20261004', SOURCE)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)
OUT = ROOT / 'analysis/no_dropout_seed_bank_20261004'
BASELINE = ROOT / 'analysis/neural_regularization_bank_20261003/rank512_drop000_e32'
PREFLIGHT = ROOT / 'analysis/no_dropout_seed_preflight_20261004/verification.json'
COMMON = {'kind': 'mlp', 'target': 'y_rank', 'batch_size': 32768, 'learning_rate': .001,
    'weight_decay': .0001, 'dropout': 0., 'hidden': [512, 256, 128], 'epochs': 32, 'seed': 20261007}
CONFIGS = {
    'rank512_drop000_seed16_e32': {**COMMON, 'seed': 20261016},
    'rank512_drop000_seed17_e32': {**COMMON, 'seed': 20261017},
    'rank512_drop000_seed18_e32': {**COMMON, 'seed': 20261018},
    'rank512_drop000_seed18_e64': {**COMMON, 'seed': 20261018, 'epochs': 64}}
engine.OUT, engine.CONFIGS = OUT, CONFIGS
read, dump, sha, log = engine.read, engine.dump, engine.sha, engine.log
YEARS = engine.YEARS


def verify():
    return engine.verify()


def freeze():
    if (OUT / 'protocol.json').exists():
        verify()
        return
    assert read(PREFLIGHT)['status'] == 'passed'
    sources = [Path(__file__), SOURCE, PREFLIGHT,
        ROOT / 'analysis/verify_no_dropout_seed_design_20261004.py',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md',
        ROOT / 'results/optimization_20261003_r31.json',
        ROOT / 'analysis/neural_regularization_bank_20261003/protocol.json',
        *[BASELINE / f'info_{year}.json' for year in YEARS]]
    dump(OUT / 'protocol.json', {
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'configurations': CONFIGS, 'features': engine.feature_names(), 'years': YEARS,
        'validation': '2020–2024 annual expanding OOF; original mature-label cutoff',
        'matched_control': 'Actual R31-selected rank512_drop000_e32, seed20261007,32 epochs; control artifacts are reused, never refitted.',
        'design': 'Three additional32-epoch seeds; matched seed20261018 epoch32/64 comparison. All other architecture, learning-rate, regularization and target settings fixed.',
        'provided_rank_target_expression': 'provided_y_rank.astype(float32)-0.5, preserving the original fitter',
        'selection_bias_uncorrected': True, 'all_validation_years_previously_viewed': True,
        'preprocessing': 'Fit mean/std on mature training rows only; fixed padded inference batches.',
        'no_early_stopping_on_validation': True, 'no_feature_selection': True,
        'expected_annual_fits': 20, 'minimum_available_ram_before_each_fit_GiB': 8.,
        'start_reserve_is_scheduling_rule_not_guaranteed_peak': True,
        'test_data_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in sources}}, immutable=True)
    log('Four matched no-dropout seed/epoch configurations frozen')


def train_one(name, year):
    import psutil
    while not (OUT / name / f'info_{year}.json').exists() and psutil.virtual_memory().available < 8 * 2**30:
        time.sleep(10)
    info = engine.train_one(name, year)
    control = read(BASELINE / f'info_{year}.json')
    fields = ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end', 'features',
        'training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256')
    assert all(info['training_meta'][key] == control['training_meta'][key] for key in fields), (name, year)
    return info


def all_oof():
    import numpy as np
    import polars as pl
    freeze()
    features, boundary, prefixes = engine.feature_names(), {}, {}
    for name, cfg in CONFIGS.items():
        for year in YEARS:
            control_path = OUT / f'boundary_control_{name}_{year}.json'
            if not control_path.exists():
                dump(control_path, engine.boundary_control(year, cfg, features), immutable=True)
            boundary[f'{name}_{year}'] = read(control_path)
            info = train_one(name, year)
            prefix_path = OUT / f'prefix_control_{name}_{year}.json'
            if not prefix_path.exists():
                frame = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').head(32781).collect()
                x = engine.to_matrix(frame, features)
                bundle = engine.load_bundle(OUT / name / f'model_{year}.joblib')
                raw = engine.predict_arrays(bundle, x)
                for n in (1, 80, 32767, 32768):
                    assert np.array_equal(raw[:n], engine.predict_arrays(bundle, x[:n])), (name, year, n)
                raw[~frame['price_valid'].to_numpy()] = -1e6
                cached = pl.read_parquet(OUT / name / f'raw_{year}.parquet').head(len(frame))
                assert frame.select(engine.KEYS).equals(cached.select(engine.KEYS))
                assert np.array_equal(raw, cached['pred_raw'].to_numpy())
                dump(prefix_path, {'status': 'passed', 'model': name, 'year': year,
                    'prefix_rows': [1, 80, 32767, 32768], 'rows': len(x),
                    'actual_saved_fold_output_prefix_bit_identical': True,
                    'padded_inference_prefix_bit_identical': True,
                    'training_info_sha256': sha(OUT / name / f'info_{year}.json')}, immutable=True)
            prefixes[f'{name}_{year}'] = read(prefix_path)
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'configurations': CONFIGS, 'years': YEARS,
        'boundary_controls': boundary, 'prefix_controls': prefixes,
        'mature_training_inputs_bit_identical_to_selected_no_dropout_control': True,
        'models_trained': 20, 'new_quality_scores': 0, 'test_data_read': False}, immutable=True)
    log('All20 no-dropout seed/epoch annual fits and actual maturity/prefix controls passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('freeze', 'all', 'train'))
    parser.add_argument('--name', choices=tuple(CONFIGS))
    parser.add_argument('--year', type=int)
    args = parser.parse_args()
    if args.stage == 'freeze':
        freeze()
    elif args.stage == 'all':
        all_oof()
    else:
        assert args.name and args.year in (*YEARS, 2025)
        train_one(args.name, args.year)
