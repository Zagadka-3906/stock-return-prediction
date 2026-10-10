"""Exact original mature rows, ordered on disk; no statistical approximation."""
from pathlib import Path
import gc
import hashlib


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def close(array):
    array.flush()
    array._mmap.close()


def build(engine, year, folder, context=None):
    import numpy as np
    import polars as pl
    import pyarrow.parquet as pq
    folder = Path(folder).resolve()
    assert folder.drive.upper() in ('D:', 'E:') and not folder.exists()
    folder.mkdir(parents=True)
    features, cutoff = engine.feature_names(), engine.fold_cutoff(year)
    lazy = pl.scan_parquet(engine.FEATURE_FILE)
    columns = engine.KEYS + ['y_rank', 'y_ret_1d', 'is_train', 'price_valid']
    keys = lazy.select(columns).with_row_index('_source_row').collect()
    train = engine.training_frame(keys.lazy(), cutoff, {'target': 'y_rank'}).sort('trade_date', 'ts_code').collect()
    ret = engine.training_frame(keys.lazy(), cutoff, {'target': 'y_ret_1d'}).sort('trade_date', 'ts_code').select('_source_row').collect()
    assert np.array_equal(train['_source_row'].to_numpy(), ret['_source_row'].to_numpy())
    rows = len(train)
    lookup = np.full(len(keys), -1, dtype=np.int32)
    lookup[train['_source_row'].to_numpy()] = np.arange(rows, dtype=np.int32)
    dates = train['trade_date'].to_numpy()
    all_dates = keys.filter(pl.col('is_train'))['trade_date'].unique().sort().to_numpy()
    last = int(dates[-1])
    metadata = {'rows': rows, 'days': len(np.unique(dates)), 'first': int(dates[0]), 'last': last,
        'cutoff_exclusive': cutoff, 'last_label_end': int(all_dates[np.searchsorted(all_dates, last) + 1]),
        'validation_year': year, 'training_keys_sha256': engine.array_hash(train.select(engine.KEYS).hash_rows(seed=2026).to_numpy()),
        'features': features}
    assert last < cutoff and metadata['last_label_end'] <= cutoff
    targets = {}
    for target in ('y_rank', 'y_ret_1d'):
        y = train[target].to_numpy()
        assert np.isfinite(y).all()
        path = folder / (target + '.bin')
        with path.open('xb') as stream:
            stream.write(memoryview(np.ascontiguousarray(y)).cast('B'))
        targets[target] = {'path': str(path), 'dtype': str(y.dtype), 'sha256': file_sha(path)}
    del train, ret, keys, dates, all_dates
    gc.collect()
    raw_path = folder / 'original_float32_matrix.bin'
    raw = np.memmap(raw_path, mode='w+', dtype=np.float32, shape=(rows, len(features)))
    source_offset, written = 0, 0
    parquet = pq.ParquetFile(engine.FEATURE_FILE)
    for batch in parquet.iter_batches(batch_size=65536, columns=features, use_threads=False):
        positions = lookup[source_offset:source_offset + len(batch)]
        selected = positions >= 0
        if selected.any():
            frame = pl.from_arrow(batch).filter(pl.Series(selected))
            block = engine.to_matrix(frame, features)
            raw[positions[selected]] = block
            written += len(block)
            if context is not None:
                context.context = {'stage': 'exact_full_mature_matrix_scatter', 'year': year,
                                   'written_rows': written, 'required_rows': rows}
            del frame, block
        source_offset += len(batch)
    assert source_offset == len(lookup) and written == rows
    close(raw)
    del raw, lookup, batch, parquet
    gc.collect()
    metadata['training_matrix_sha256'] = file_sha(raw_path)
    for label, target in (('rank', 'y_rank'), ('return', 'y_ret_1d')):
        reference = engine.ROOT / f'analysis/linear_bank_20261003/{label}_ridge_l01/info_{year}.json'
        expected = engine.read(reference)['training_meta']
        actual = dict(metadata, training_target_sha256=targets[target]['sha256'])
        assert actual == expected, (year, label, [(k, actual.get(k), v) for k, v in expected.items() if actual.get(k) != v])
    return {'year': year, 'folder': str(folder), 'raw_path': str(raw_path), 'shape': [rows, len(features)],
            'training_meta_without_target': metadata, 'targets': targets,
            'rank_and_return_eligible_row_ordinals_bit_identical': True,
            'entire_original_matrix_targets_keys_maturity_metadata_matched': True}


def standardize(core, artifact, cfg, path, context=None):
    import numpy as np
    path = Path(path)
    assert not path.exists()
    raw = np.memmap(artifact['raw_path'], mode='r', dtype=np.float32, shape=tuple(artifact['shape']))
    mean, scale = core.matched.preprocessing(raw)
    clean = np.memmap(path, mode='w+', dtype=np.float32, shape=raw.shape)
    expected = hashlib.sha256()
    for offset in range(0, len(raw), cfg['chunk_rows']):
        block = core.matched.standardize(raw[offset:offset + cfg['chunk_rows']], mean, scale, cfg)
        clean[offset:offset + len(block)] = block
        expected.update(memoryview(block).cast('B'))
        if context is not None:
            context.context = {'stage': 'exact_full_past_mean_std_and_standardized_matrix',
                               'year': artifact['year'], 'written_rows': offset + len(block)}
    close(clean)
    raw._mmap.close()
    del clean, raw, block
    gc.collect()
    actual = file_sha(path)
    assert actual == expected.hexdigest()
    return mean, scale, {'path': str(path), 'sha256': actual,
        'all_original_standardize_blocks_bit_identical': True,
        'original_full_column_numpy_mean_and_std_algorithm_used': True}


def fit_preprocessed(core, artifact, cfg, mean, scale, clean_info):
    import lightgbm as lgb
    import numpy as np
    clean = np.memmap(clean_info['path'], mode='r', dtype=np.float32, shape=tuple(artifact['shape']))
    target_info = artifact['targets'][cfg['target']]
    y = np.memmap(target_info['path'], mode='r', dtype=target_info['dtype'], shape=(len(clean),))
    target = np.asarray(y, dtype=np.float64)
    bounds = None
    if cfg['target'] == 'y_ret_1d':
        bounds = [float(v) for v in np.quantile(target, cfg['return_quantiles'])]
        target = np.clip(target, *bounds)
    params = core.parameters(cfg)
    dataset = lgb.Dataset(clean, label=target, params=params, free_raw_data=True)
    booster = lgb.train(params, dataset, num_boost_round=cfg['num_boost_round'])
    assert booster.current_iteration() == cfg['num_boost_round']
    details = core.matched.leaf_summary(booster)
    assert details['tree_count'] == cfg['num_boost_round'] and details['leaves_with_linear_features'] == 0
    bundle = {'kind': 'lightgbm_quantile_tree', 'config': dict(cfg), 'mean': mean, 'scale': scale,
        'model_string': booster.model_to_string(), 'target_bounds': bounds, 'target_units': cfg['target'],
        'leaf_summary': details, 'no_validation_early_stopping': True,
        'native_training_parameters': params, 'requested_and_actual_boosting_iterations': booster.current_iteration(),
        'past_only_preprocessing': True, 'missing_values_preserved_as_nan': True}
    del booster, dataset, target
    clean._mmap.close()
    y._mmap.close()
    gc.collect()
    return bundle
