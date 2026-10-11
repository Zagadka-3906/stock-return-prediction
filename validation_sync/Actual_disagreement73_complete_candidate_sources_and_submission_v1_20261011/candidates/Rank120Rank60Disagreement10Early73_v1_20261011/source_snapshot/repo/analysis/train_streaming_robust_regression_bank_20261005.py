"""Twenty complete mature annual regressor fits with streamed fixed-row inference."""
from pathlib import Path
import gc
import json
import os
import sys
import time
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import streaming_robust_regression_20261005 as core

SOURCE = Path(core.__file__)
OUT = core.OUT
CONFIGS, YEARS, KEYS = core.CONFIGS, core.YEARS, core.KEYS
FEATURE_FILE, MANIFEST = core.FEATURE_FILE, core.MANIFEST
BASELINE = core.BASELINE
read, dump, sha, log, feature_names = core.read, core.dump, core.sha, core.log, core.feature_names
STORAGE = A / 'streaming_robust_regression_storage_20261005.json'
RESOURCE = None


def to_matrix(frame, features):
    import numpy as np
    return np.ascontiguousarray(frame.select(features).to_numpy(), dtype=np.float32)


def verify():
    protocol = read(OUT / 'protocol.json')
    for filename, digest in protocol['input_sha256'].items():
        assert sha(filename) == digest, filename
    return protocol


def freeze():
    if (OUT / 'protocol.json').exists():
        return verify()
    proof = A / 'streaming_robust_regression_preflight_20261005/verification.json'
    assert read(proof)['status'] == 'passed_actual_streamed_robust_regression_maturity_native_reload_and_prefix_controls'
    inputs = [Path(__file__), SOURCE, STORAGE, proof,
        A / 'run_streaming_robust_regression_bank_20261005.py',
        A / 'verify_streaming_robust_regression_full_future_20261005.py',
        A / 'streaming_rank_classifier_actual_resource_recorder_20261005.py',
        A / 'streaming_robust_regression_bank_run_20261005.json',
        A / 'streaming_robust_regression_future_run_20261005.json',
        A / 'streaming_robust_regression_complete_search_plan_20261005.json',
        FEATURE_FILE, MANIFEST, ROOT / 'data/raw/训练集.csv', ROOT / 'run.py',
        ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    inputs += [core.baseline_path(cfg,year) for cfg in CONFIGS.values() for year in (*YEARS,2025)]
    inputs += [Path(core.shared.__file__)]
    dump(OUT / 'protocol.json', {
        'status': 'frozen_before20_actual_full_annual32pass_regressor_fits',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': CONFIGS,
        'features': feature_names(), 'years': YEARS, 'expected_annual_fits': 20, 'expected_final_fits': 4,
        'validation': 'Same2020-2024 continuous5635800-row1212-day OOF; mature one-day purge.',
        'training': 'Every eligible past row, exactly32 complete partial_fit passes in frozen Parquet physical order; no validation early stopping.',
        'target': 'Paired squared_error and Huber loss on supplied centered rank or one-day-return targets; mean/std fitted on mature past only; no target clipping.',
        'preprocessing': 'Finite past-only feature and target Chan mean/std; impute features, clip standardized features8, keep labels unclipped and inverse-transform outputs; no held-out values fitted.',
        'eligibility': 'is_train and price_valid andfinite selected supplied target anddate strictly below original target-specific mature cutoff.',
        'row_identity': 'Full key multiset SHA256 independently checked against original Polars eligibility filter; stream-order matrix/label hashes explicitly distinct from old date-sorted hashes.',
        'regression_scores_require_mature_past_return_mapping_in_full_official_outputs': True,
        'fixed_row_inference': 'Float64 per-row einsum, past-only inverse target scaling; native prediction tolerance control and exact reload/prefix checks.',
        'minimum_available_host_RAM_before_each_fit_GiB': 3.,
        'reserve_is_this_streaming_family_scheduling_policy_not_original_wide_policy_or_physical_boundary': True,
        'streaming_pre_buffer_false_and_no_readahead': True,
        'all_full_model_fits_and_complete_quality_required_no_small_control_substitution': True,
        'source_documentation': 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html',
        'selection_bias_uncorrected': True, 'test_data_read': False, 'new_quality_scores': 0,
        'input_sha256': {str(path.resolve()): sha(path) for path in inputs}}, immutable=True)
    return read(OUT / 'protocol.json')


def infer_stream(bundle, condition, path):
    import numpy as np
    import pyarrow as pa
    import pyarrow.parquet as pq
    features = feature_names()
    columns = KEYS + ['price_valid'] + features
    writer, rows = None, 0
    try:
        for batch in core.scanner(columns, condition, bundle['config']['chunk_rows']):
            if not len(batch):
                continue
            x = core.matrix(batch, features)
            pred = core.predict_arrays(bundle, x)
            valid = batch.column('price_valid').to_numpy(zero_copy_only=False)
            pred[~valid] = -1e6
            table = pa.Table.from_arrays([batch.column('ts_code'), batch.column('trade_date'), pa.array(pred)],
                                         names=KEYS + ['pred_raw'])
            if writer is None:
                writer = pq.ParquetWriter(path, table.schema, compression='zstd')
            writer.write_table(table)
            rows += len(batch)
        assert rows and writer is not None
    finally:
        if writer is not None:
            writer.close()
    return rows


def train_one(name, year):
    import numpy as np
    import polars as pl
    import pyarrow.dataset as ds
    import psutil
    assert name in CONFIGS and year in (*YEARS, 2025)
    cfg = CONFIGS[name]
    folder = OUT / name
    folder.mkdir(exist_ok=True, parents=True)
    info_path, model_path = folder / f'info_{year}.json', folder / f'model_{year}.joblib'
    raw_path = folder / f'raw_{year}.parquet'
    if info_path.exists():
        info = read(info_path)
        assert sha(model_path) == info['model_sha256']
        if year < 2025:
            assert sha(raw_path) == info['prediction_sha256']
        return info
    while psutil.virtual_memory().available < 3 * 2**30:
        time.sleep(10)
    verify()
    started = time.monotonic()
    if RESOURCE is not None:
        RESOURCE.context = {'stage': 'actual_full_mature32pass_fit', 'model': name, 'year': year}
    bundle, meta, epochs = core.fit_stream(year, cfg)
    fit_seconds = time.monotonic() - started
    assert epochs == [meta['rows']] * 32
    assert bundle['completed_epochs'] == 32 and bundle['actual_native_sample_counter'] == 1 + 32 * meta['rows']
    assert meta['full_selected_row_keys_match_independent_original_filter']
    fit = {'status': 'completed_full_original32passes', 'model': name, 'year': year,
           'configuration': cfg, 'actual_training_rows': meta['rows'], 'actual_feature_count': 63,
           'actual_completed_epochs': 32, 'actual_rows_in_each_epoch': epochs,
           'actual_partial_fit_calls': bundle['actual_partial_fit_calls'],
           'actual_native_sample_counter': bundle['actual_native_sample_counter'],
           'actual_elapsed_seconds': fit_seconds,
           'target_scaling': {'center': bundle['target_center'], 'scale': bundle['target_scale']},
           'parameter_count': int(bundle['regressor'].coef_.size + bundle['regressor'].intercept_.size),
           'coefficient_and_intercept_all_finite': True, 'test_data_read': False}
    with (OUT / 'actual_native_fit_measurements.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(fit, ensure_ascii=False) + '\n')
    core.save_bundle(model_path, bundle)
    info = {'status': 'passed', 'model': name, 'year': year, 'configuration': cfg,
        'training_meta': meta, 'fit_seconds': fit_seconds, 'model_sha256': sha(model_path),
        'completed_epochs': 32, 'actual_native_sample_counter': bundle['actual_native_sample_counter'],
        'target_scaling_learned_from_mature_past': {'center': bundle['target_center'], 'scale': bundle['target_scale']},
        'test_data_read': False}
    if year < 2025:
        if RESOURCE is not None:
            RESOURCE.context = {'stage': 'actual_annual_full_reload_and_cold80_prefix', 'model': name, 'year': year}
        condition = ((ds.field('is_train') == True) & (ds.field('trade_date') >= year * 10000 + 101)
                     & (ds.field('trade_date') < (year + 1) * 10000 + 101))
        scratch = Path(read(STORAGE)['temporary_directory'])
        scratch.mkdir(parents=True, exist_ok=True)
        first, replay = scratch / f'{name}_{year}_first.parquet', scratch / f'{name}_{year}_reload.parquet'
        assert not first.exists() and not replay.exists()
        infer_stream(bundle, condition, first)
        infer_stream(core.load_bundle(model_path), condition, replay)
        frame = pl.read_parquet(first).sort('trade_date', 'ts_code')
        second = pl.read_parquet(replay).sort('trade_date', 'ts_code')
        assert frame.equals(second) and frame['pred_raw'].is_finite().all()
        frame.write_parquet(raw_path)
        prefix_cutoff = int(frame['trade_date'].unique().sort()[79])
        prefix_path = scratch / f'{name}_{year}_cold80.parquet'
        assert not prefix_path.exists()
        infer_stream(core.load_bundle(model_path), condition & (ds.field('trade_date') <= prefix_cutoff), prefix_path)
        prefix = pl.read_parquet(prefix_path).sort('trade_date', 'ts_code')
        assert frame.filter(pl.col('trade_date') <= prefix_cutoff).equals(prefix)
        assert len(frame) == 4650 * frame['trade_date'].n_unique() and frame['ts_code'].n_unique() == 4650
        dump(OUT / f'prefix_control_{name}_{year}.json', {'status': 'passed', 'rows': len(prefix),
            'actual_saved_model_full_reload_and_cold80_day_prefix_bit_identical': True,
            'actual_complete_regression32passes_and_mature_key_eligibility_verified': True,
            'test_data_read': False}, immutable=True)
        info.update(rows=len(frame), prediction_sha256=sha(raw_path), model_reload_bit_identical=True)
        # These three reversible temporary inference copies are exactly reproduced
        # by the immutable model/raw/prefix controls; retain the actual final data.
        for path in (first, replay, prefix_path):
            assert path.resolve().is_relative_to(scratch.resolve())
            path.unlink()
        del frame, second, prefix
    else:
        info['fulltraining_only_test_prediction_not_generated'] = True
    info['elapsed_seconds'] = time.monotonic() - started
    dump(info_path, info, immutable=True)
    del bundle
    gc.collect()
    log(f'Actual streamed {name} fold{year}32passes saved and verified in {info["elapsed_seconds"]:.1f}s')
    return info


def all_oof():
    freeze()
    checks = []
    for name in CONFIGS:
        for year in YEARS:
            info = train_one(name, year)
            checks.append({'model': name, 'year': year, 'training_info_sha256': sha(OUT / name / f'info_{year}.json'),
                           'model_reload_bit_identical': info['model_reload_bit_identical'],
                           'cold_prefix': read(OUT / f'prefix_control_{name}_{year}.json')})
    verify()
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'actual_annual_fits': len(checks),
         'configurations': CONFIGS, 'checks': checks, 'test_data_read': False,
         'complete_final_future_and_official_quality_still_required': True, 'new_quality_scores': 0}, immutable=True)


engine = SimpleNamespace(FEATURE_FILE=FEATURE_FILE, MANIFEST=MANIFEST, KEYS=KEYS,
    feature_names=feature_names, to_matrix=to_matrix, load_bundle=core.load_bundle,
    predict_arrays=core.predict_arrays, fit_arrays=core.fit_arrays, train_one=train_one)
