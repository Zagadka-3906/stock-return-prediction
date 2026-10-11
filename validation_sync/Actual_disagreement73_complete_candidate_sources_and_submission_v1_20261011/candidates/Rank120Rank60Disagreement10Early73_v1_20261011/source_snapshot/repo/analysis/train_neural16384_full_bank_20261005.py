"""Matched complete annual16384-wide fits, beyond the completed one-step controls."""
from pathlib import Path
import importlib.util
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
SOURCE = ROOT / 'analysis/train_diverse_backbones_20261003.py'
spec = importlib.util.spec_from_file_location('isolated_neural16384_full_20261005', SOURCE)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)
read, dump, sha, log = engine.read, engine.dump, engine.sha, engine.log
STORAGE = ROOT / 'analysis/neural16384_full_storage_20261005.json'
OUT = Path(read(STORAGE)['output_directory'])
BASELINE = ROOT / 'analysis/neural_regularization_bank_20261003/rank512_drop000_e32'
CONFIGS = {'rank16384_drop000_seed07_e32': {
    'kind': 'mlp', 'target': 'y_rank', 'batch_size': 32768, 'learning_rate': .001,
    'weight_decay': .0001, 'dropout': 0., 'hidden': [16384, 8192, 4096],
    'epochs': 32, 'seed': 20261007}}
engine.OUT, engine.CONFIGS = OUT, CONFIGS
YEARS = engine.YEARS


def verify():
    return engine.verify()


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'protocol.json').exists():
        verify()
        return
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    assert complete_round_evidence(66) is not None
    frontier = ROOT / 'analysis/neural_width_frontier_20261004/verification.json'
    proof = read(frontier)
    control = next(row for row in proof['execution_controls'] if row['width'] == 16384)
    assert control['status'] == 'completed' and control['child_result']['status'] == 'one_step_completed'
    sources = [Path(__file__), SOURCE, STORAGE, frontier,
        ROOT / 'analysis/run_neural16384_full_bank_20261005.py',
        ROOT / 'analysis/neural16384_actual_resource_recorder_20261005.py',
        ROOT / 'analysis/neural16384_full_run_20261005.json',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md',
        ROOT / 'analysis/optimization_20261003_r66/provenance_scope_execution.json',
        ROOT / 'results/optimization_20261003_r66.json',
        *[BASELINE / f'info_{year}.json' for year in YEARS]]
    dump(OUT / 'protocol.json', {'status': 'frozen_before_actual_complete_annual_training',
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': CONFIGS,
        'features': engine.feature_names(), 'years': YEARS, 'expected_annual_fits': 5,
        'validation': '2020–2024 annual expanding OOF; original mature one-day label purge.',
        'matched_control': 'Actual512-wide seed20261007 no-dropout32-epoch configuration; only width changes.',
        'provided_rank_target_expression': 'provided_y_rank.astype(float32)-0.5, original fitter unchanged.',
        'full_fit_evidence_required_one_step_not_a_substitute': True,
        'minimum_available_host_RAM_before_each_fit_GiB': 14.,
        'reserve_is_scheduling_policy_not_physical_boundary': True,
        'quality_and_final_future_inference_are_separate_pending_steps': True,
        'no_validation_early_stopping': True, 'selection_bias_uncorrected': True,
        'new_quality_scores': 0, 'test_data_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in sources}}, immutable=True)


def all_oof():
    import gc
    import numpy as np
    import polars as pl
    import psutil
    freeze()
    features = engine.feature_names()
    checks = []
    for name, cfg in CONFIGS.items():
        for year in YEARS:
            while not (OUT / name / f'info_{year}.json').exists() and psutil.virtual_memory().available < 14 * 2**30:
                time.sleep(10)
            boundary = OUT / f'boundary_control_{name}_{year}.json'
            if hasattr(engine, 'resource_recorder'):
                engine.resource_recorder.context = {'stage': 'actual4096_row_future_label_poison_control', 'model': name, 'year': year}
            if not boundary.exists():
                dump(boundary, engine.boundary_control(year, cfg, features), immutable=True)
            if hasattr(engine, 'resource_recorder'):
                engine.resource_recorder.context = {'stage': 'actual_complete_annual_fit_and_reload', 'model': name, 'year': year}
            info = engine.train_one(name, year)
            baseline = read(BASELINE / f'info_{year}.json')
            for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end',
                        'features', 'training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256'):
                assert info['training_meta'][key] == baseline['training_meta'][key], key
            prefix_path = OUT / f'prefix_control_{name}_{year}.json'
            if not prefix_path.exists():
                frame = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix = frame.filter(pl.col('trade_date') <= cutoff)
                values = engine.predict_arrays(engine.load_bundle(OUT / name / f'model_{year}.joblib'), engine.to_matrix(prefix, features))
                values[~prefix['price_valid'].to_numpy()] = -1e6
                saved = pl.read_parquet(OUT / name / f'raw_{year}.parquet').filter(pl.col('trade_date') <= cutoff)
                assert prefix.select(engine.KEYS).equals(saved.select(engine.KEYS))
                assert np.array_equal(values, saved['pred_raw'].to_numpy())
                dump(prefix_path, {'status': 'passed', 'rows': len(prefix),
                    'actual_saved_model_cold80_day_prefix_bit_identical': True,
                    'matched512_mature_training_matrices_targets_andkeys_exact': True,
                    'test_data_read': False}, immutable=True)
                del frame, prefix, values, saved
                gc.collect()
            checks.append({'model': name, 'year': year, 'boundary': read(boundary), 'prefix': read(prefix_path)})
    verify()
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'actual_annual_fits': 5,
        'configurations': CONFIGS, 'checks': checks,
        'complete_output_quality_and_final_future_controls_pending': True,
        'new_quality_scores': 0, 'test_data_read': False}, immutable=True)
