"""Six own mature annual fits for the distinct BF16 recipe; all durable storage on E."""
from pathlib import Path
import gc
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
for key in ('TEMP', 'TMP', 'TMPDIR', 'MPLCONFIGDIR', 'TORCH_HOME', 'TORCHINDUCTOR_CACHE_DIR', 'TRITON_CACHE_DIR', 'CUDA_CACHE_PATH'):
    os.environ[key] = str(OUT / 'tmp' / key)
os.environ['CUDA_CACHE_DISABLE'] = '1'
from run_dependency_queue_v3_20261006 import read, sha, create, owned
import json
import uuid

def write(path, data):
    path = Path(path).resolve()
    assert path.is_relative_to(OUT.resolve()) and path.drive.upper() == 'E:' and path.suffix == '.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.part')
    with temporary.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)

import neural_BF16_micro8192_native_v1_20261008 as native


def main():
    import joblib
    import numpy as np
    import polars as pl
    import psutil
    import torch
    from run import FEATURE_FILE, MANIFEST, feature_names, fold_cutoff, to_matrix
    from optimize_training_round12 import KEYS
    service = A / 'service_owned_workflows_20261006/actual_BF16_micro8192_small32_wide2_restart_control_v1_20261008'
    while not (service / 'native_launch.json').exists() or owned(read(service / 'native_launch.json')): time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    control = Path(read(A / 'actual_BF16_micro_restart_location_20261008.json')['output'])
    assert read(control / 'verification.json')['status'] == 'passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    assert torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    years = (2020, 2021, 2022, 2023, 2024, 2025)
    features = feature_names()
    paths = [Path(__file__), Path(native.__file__), Path(native.architecture.__file__),
             A / 'epoch_durable_neural_checkpoint_adapter_v2_20261007.py',
             ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md',
             FEATURE_FILE, MANIFEST, control / 'verification.json']
    pins = {str(p): sha(p) for p in paths}
    frozen = {'status': 'frozen_distinct_BF16_micro8192_six_mature_annual_fits_before_training',
              'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
              'configuration': native.CONFIG, 'features': features, 'native_fit_years': list(years),
              'all_fits_start_from_own_seed_not_original_FP32_annual_weights': True,
              'preprocessing': 'own mature full fold mean/std, finite imputation, clip[-8,8]',
              'one_day_label_boundary_purged': True, 'validation': 'full annual expanding OOF 2020-2024',
              'inference': 'fixed8192 padded FP32 forward', 'actual_control': str(control / 'verification.json'),
              'checkpoint': 'atomic uncompressed completed epochs with CPU and CUDA RNG and AdamW states',
              'test_labels_read': False, 'new_quality_scores': 0,
              'no_early_stopping_or_validation_adaptive_epochs': True}
    if not OUT.exists():
        OUT.mkdir(parents=True)
        create(OUT / 'protocol.json', frozen)
    else:
        before = read(OUT / 'protocol.json')
        assert before['input_sha256'] == pins and before['configuration'] == native.CONFIG
    create(A / 'actual_BF16_micro8192_bank6_location_v2_20261008.json', {'status': 'authorized_new_recipe_annual_bank_on_E',
        'output': str(OUT), 'protocol_sha256': sha(OUT / 'protocol.json'), 'new_quality_scores': 0})
    lazy = pl.scan_parquet(FEATURE_FILE)
    all_dates = lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    records = []
    for year in years:
        folder = OUT / str(year)
        folder.mkdir(exist_ok=True)
        if (folder / 'info.json').exists():
            info = read(folder / 'info.json')
            assert info['status'] == 'passed_actual_complete_mature_BF16_micro_annual_model'
            assert sha(folder / 'model.joblib') == info['model_sha256']
            if year < 2025: assert sha(folder / 'raw.parquet') == info['prediction_sha256']
            records.append(info)
            continue
        while psutil.virtual_memory().available < 11 * 2**30: time.sleep(15)
        for p, d in pins.items():
            if Path(p) != FEATURE_FILE: assert sha(p) == d, p
        cutoff = fold_cutoff(year)
        # Select only mature training rows before collecting any label or feature array.
        train = native.architecture.training_frame(lazy, cutoff, native.CONFIG).select(KEYS + features + ['y_rank']).sort('trade_date', 'ts_code').collect()
        x, y = to_matrix(train, features), train['y_rank'].to_numpy()
        last = int(train['trade_date'][-1])
        label_end = int(all_dates[np.searchsorted(all_dates, last) + 1])
        assert last < cutoff and label_end <= cutoff and np.isfinite(y).all()
        # Actual future-label poisoning must leave the selected past population unchanged.
        cols = KEYS + features + [c for c in ('y_rank', 'y_ret_1d', 'is_train', 'price_valid') if c not in features]
        past = native.architecture.training_frame(lazy, cutoff, native.CONFIG).select(cols).head(4096).collect()
        later = lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= cutoff)).select(cols).head(1024).collect()
        sample = pl.concat([past, later])
        poisoned = sample.with_columns([pl.when(pl.col('trade_date') >= cutoff).then(pl.lit(12345., dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c) for c in ('y_rank', 'y_ret_1d')])
        assert native.architecture.training_frame(sample.lazy(), cutoff, native.CONFIG).collect().equals(native.architecture.training_frame(poisoned.lazy(), cutoff, native.CONFIG).collect())
        meta = {'rows': len(train), 'first': int(train['trade_date'][0]), 'last': last,
                'days': train['trade_date'].n_unique(), 'cutoff_exclusive': cutoff, 'last_label_end': label_end,
                'features': features, 'training_matrix_sha256': native.array_sha(x),
                'training_target_sha256': native.array_sha(y),
                'training_keys_sha256': native.array_sha(train.select(KEYS).hash_rows(seed=2026).to_numpy()),
                'actual_future_training_label_poisoning_population_exact': True}
        if not (folder / 'frozen_training_inputs.json').exists(): create(folder / 'frozen_training_inputs.json', meta)
        else: assert read(folder / 'frozen_training_inputs.json') == meta
        del train, past, later, sample, poisoned
        gc.collect()
        write(OUT / 'actual_stage.json', {'status': 'actual_mature_annual_BF16_fit', 'year': year,
              'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'completed_annual_models': len(records),
              'training_rows': len(y), 'checkpoint_path': str(folder / 'checkpoint.joblib')})
        print(f"Actual new BF16 annual {year}: {len(y):,} own mature rows, 32 fixed epochs", flush=True)
        started = time.monotonic()
        bundle = native.fit_arrays(x, y, native.CONFIG, folder / 'checkpoint.joblib')
        fit_seconds = time.monotonic() - started
        joblib.dump(bundle, folder / 'model.joblib', compress=0)
        del x, y
        gc.collect()
        info = {'status': 'passed_actual_complete_mature_BF16_micro_annual_model', 'year': year,
                'configuration': native.CONFIG, 'training_meta': meta,
                'fit_seconds_including_checkpoints_this_process': fit_seconds,
                'model_sha256': sha(folder / 'model.joblib'), 'test_labels_read': False}
        if year < 2025:
            valid = lazy.filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(KEYS + features + [c for c in ('price_valid',) if c not in features]).sort('trade_date', 'ts_code').collect()
            vx = to_matrix(valid, features)
            raw = native.predict_arrays(bundle, vx)
            reloaded = joblib.load(folder / 'model.joblib')
            repeated = native.predict_arrays(reloaded, vx)
            assert np.array_equal(raw.view('u8'), repeated.view('u8')) and np.isfinite(raw).all()
            n = min(80 * 4650, len(valid))
            prefix = native.predict_arrays(reloaded, vx[:n])
            assert np.array_equal(prefix.view('u8'), raw[:n].view('u8'))
            raw[~valid['price_valid'].to_numpy()] = -1e6
            valid.select(KEYS).with_columns(pl.Series('pred_raw', raw)).write_parquet(folder / 'raw.parquet')
            info.update(prediction_sha256=sha(folder / 'raw.parquet'), rows=len(valid),
                        actual_full_annual_reload_prediction_bits_exact=True,
                        actual_cold80_prefix_bits_exact=True)
            del valid, vx, raw, repeated, prefix, reloaded
        else:
            info['full_mature_final_fit_no_actual_future_features_read'] = True
        create(folder / 'info.json', info)
        records.append(info)
        del bundle
        gc.collect()
        torch.cuda.empty_cache()
        print(f"Actual BF16 annual {year} saved, reloaded, and verified", flush=True)
    for p, d in pins.items(): assert sha(p) == d, p
    create(OUT / 'verification.json', {'status': 'passed_actual_six_mature_BF16_micro_annual_models',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'actual_native_fits': len(records), 'actual_models': records,
            'full_annual_OOF_reload_and_cold80_bits_exact': True,
            'actual_future_feature_inference_and_official_quality_scores_pending': True,
            'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__': main()
