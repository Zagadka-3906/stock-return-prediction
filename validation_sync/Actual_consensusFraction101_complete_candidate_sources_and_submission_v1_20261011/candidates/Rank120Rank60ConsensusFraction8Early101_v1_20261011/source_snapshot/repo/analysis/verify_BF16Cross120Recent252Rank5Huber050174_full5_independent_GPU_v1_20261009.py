"""After all six fits, check all5,635,800 annual forecasts with an independent saved-tensor oracle."""
from pathlib import Path
import gc
import os
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = Path('E:/赛题五_本机临时/BF16Cross120Recent252Rank5Huber050174_full5_independent_controls_v1_20261009')
for key in ('TEMP', 'TMP', 'TMPDIR', 'MPLCONFIGDIR', 'TORCH_HOME', 'TORCHINDUCTOR_CACHE_DIR', 'TRITON_CACHE_DIR', 'CUDA_CACHE_PATH'):
    os.environ[key] = str(OUT / 'tmp' / key)
os.environ['CUDA_CACHE_DISABLE'] = '1'
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def closed(name):
    service = A / 'service_owned_workflows_20261006' / name
    while not (service / 'native_launch.json').exists() or owned(read(service / 'native_launch.json')): time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed', name


def main():
    closed('actual_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_bank6_v1_20261009')
    closed('BF16Cross120Recent252Rank5Huber050174_independent_small_CPU_v1_20261009')
    import joblib
    import numpy as np
    import polars as pl
    import psutil
    import torch
    from run import FEATURE_FILE, MANIFEST, feature_names, to_matrix
    from optimize_training_round12 import KEYS
    from neural_BF16_medium2048_cross120recent252rank5huber050_seed09_independent_forward_v2_20261010 import predict_saved_tensors
    from neural_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_native_v1_20261009 import array_sha
    bank = Path(read(A / 'actual_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_bank6_location_v1_20261009.json')['output'])
    bank_proof = read(bank / 'verification.json')
    assert bank_proof['status'] == 'passed_actual_six_mature_BF16_micro_annual_models'
    assert bank_proof['actual_native_fits'] == 6 and len(bank_proof['actual_models']) == 6
    assert torch.cuda.is_available()
    small_proof = Path('E:/赛题五_本机临时/BF16Cross120Recent252Rank5Huber050174_independent_small_CPU_v1_20261009/verification.json')
    assert read(small_proof)['status'] == 'passed_actual_small32_CPU_saved_tensor_independent_forward_and_prefixes'
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    features = feature_names();encoded_features=encoder.names(features)[0]
    keys_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    paths = [Path(__file__), A / 'neural_BF16_medium2048_cross120recent252rank5huber050_seed09_independent_forward_v2_20261010.py',
             A / 'neural_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_native_v1_20261009.py', A / 'train_diverse_backbones_20261003.py',
             ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md', FEATURE_FILE, MANIFEST,
             keys_path, small_proof, bank / 'protocol.json', bank / 'verification.json',
             *[bank / str(year) / name for year in range(2020, 2026) for name in ('model.joblib', 'info.json', 'frozen_training_inputs.json')],
             *[bank / str(year) / 'raw.parquet' for year in range(2020, 2025)]]
    pins = {**bank_proof['input_sha256'], **{str(p): sha(p) for p in paths}}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT / 'frozen_before_actual_independent_full_controls.json', {
        'input_sha256': pins, 'years': list(range(2020, 2025)), 'expected_rows_days_stocks': [5635800, 1212, 4650],
        'cold_prefix_days': [80, 160], 'no_native_architecture_calls_in_independent_decoder': True,
        'no_actual_future_features_or_labels_read': True, 'new_quality_scores': 0})
    lazy = pl.scan_parquet(FEATURE_FILE)
    combined = []
    records = []
    for year in range(2020, 2025):
        while psutil.virtual_memory().available < 9 * 2**30: time.sleep(15)
        started = time.monotonic()
        folder = bank / str(year)
        info = read(folder / 'info.json')
        assert info['year'] == year and info['configuration']['hidden'] == [2048, 1024, 512]
        assert info['actual_full_annual_reload_prediction_bits_exact'] and info['actual_cold80_prefix_bits_exact']
        meta = info['training_meta']
        assert meta['last'] < meta['cutoff_exclusive'] < year * 10000 + 101 and meta['last_label_end'] <= meta['cutoff_exclusive']
        assert meta['features'] == encoded_features and meta['raw_features']==features
        frame = lazy.filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
        observed = pl.read_parquet(folder / 'raw.parquet')
        assert observed.select(KEYS).equals(frame.select(KEYS))
        bundle = joblib.load(folder / 'model.joblib')
        assert bundle['config'] == info['configuration'] and len(bundle['training_losses']) == 64
        assert sha(folder / 'model.joblib') == info['model_sha256']
        raw_x = to_matrix(frame,features)
        x = encoder.encode(raw_x,frame['trade_date'].to_numpy(),features)
        feature_oracle=encoder.pandas_oracle(raw_x,frame['trade_date'].to_numpy(),features)
        assert np.array_equal(x.view('u4'),feature_oracle.view('u4'))
        del raw_x,feature_oracle
        expected = observed['pred_raw'].to_numpy()
        decoded = predict_saved_tensors(bundle, x, device='cuda')
        decoded[~frame['price_valid'].to_numpy()] = -1e6
        assert np.array_equal(decoded.view('u8'), expected.view('u8')), ('full_independent_mismatch', year)
        cold = []
        dates = frame['trade_date'].to_numpy()
        for days in (80, 160):
            count = min(days, frame['trade_date'].n_unique()) * 4650
            assert len(np.unique(dates[:count])) == min(days, frame['trade_date'].n_unique())
            prefix = predict_saved_tensors(bundle, x[:count], device='cuda')
            prefix[~frame['price_valid'].to_numpy()[:count]] = -1e6
            assert np.array_equal(prefix.view('u8'), expected[:count].view('u8'))
            cold.append({'days': days, 'rows': count, 'independent_prediction_bits_exact': True})
        combined.append(frame.select(KEYS).with_columns(pl.Series('pred_raw', decoded)))
        record = {'year': year, 'rows': len(frame), 'days': frame['trade_date'].n_unique(),
                  'independent_full_prediction_sha256': array_sha(decoded),
                  'original_saved_native_forecast_sha256': info['prediction_sha256'],
                  'full_original_native_reload_and_independent_bits_exact': True, 'cold_controls': cold,
                  'elapsed_seconds': time.monotonic() - started}
        create(OUT / f'year{year}_verification.json', record)
        records.append(record)
        del frame, observed, bundle, x, expected, decoded, prefix
        gc.collect();torch.cuda.empty_cache()
        print(f'Actual independent medium2048 annual {year}: {record["rows"]:,} rows and80/160-day prefixes bit exact', flush=True)
    all_raw = pl.concat(combined).sort('trade_date', 'ts_code')
    assert len(all_raw) == 5635800 and all_raw['trade_date'].n_unique() == 1212 and all_raw['ts_code'].n_unique() == 4650
    keys_path = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    assert all_raw.select(KEYS).equals(pl.read_parquet(keys_path, columns=KEYS))
    all_raw.write_parquet(OUT / 'combined_raw.parquet')
    for p, d in pins.items(): assert sha(p) == d, p
    create(OUT / 'verification.json', {'status': 'passed_actual_full5_5635800_medium2048_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'records': records,
        'rows_days_stocks': [5635800, 1212, 4650], 'actual_complete_bank_fits': 6,
        'independent_GPU_device': torch.cuda.get_device_name(0),
        'combined_forecast_sha256': sha(OUT / 'combined_raw.parquet'),
        'new_quality_scores': 0, 'actual_future_inference_pending': True, 'test_labels_read': False})
    create(A / 'actual_BF16Cross120Recent252Rank5Huber050174_full5_independent_location_v1_20261009.json', {
        'status': 'actual_complete_wide_annual_independent_controls_passed_on_E', 'output': str(OUT),
        'verification_sha256': sha(OUT / 'verification.json'), 'new_quality_scores': 0})


if __name__ == '__main__':main()

