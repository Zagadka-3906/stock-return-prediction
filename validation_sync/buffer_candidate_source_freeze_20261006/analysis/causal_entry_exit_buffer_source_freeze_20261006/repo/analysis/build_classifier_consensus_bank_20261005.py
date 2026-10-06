"""Self-contained fixed classifier blends; every native parent fit is reused."""
from pathlib import Path
from types import SimpleNamespace
import gc
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import train_streaming_rank_classifier_bank_v3_20261005 as parent

OUT = A / 'classifier_consensus_bank_20261005'
FUTURE = A / 'classifier_consensus_future_qa_20261005'
PLAN = A / 'classifier_consensus_complete_search_plan_20261005.json'
SOURCE = Path(parent.__file__)
YEARS, KEYS = parent.YEARS, parent.KEYS
FEATURE_FILE, MANIFEST = parent.FEATURE_FILE, parent.MANIFEST
read, dump, sha, log = parent.read, parent.dump, parent.sha, parent.log
names = list(parent.CONFIGS)
binary = [name for name, cfg in parent.CONFIGS.items() if cfg['rank_objective'] == 'top10']
decile = [name for name, cfg in parent.CONFIGS.items() if cfg['rank_objective'] == 'decile']
assert len(binary) == len(decile) == 2


def config(members, sign=1., offset=0.):
    return {'kind': 'classifier_consensus', 'target': 'y_rank', 'chunk_rows': 65536,
        'members': [{'model': name, 'weight': weight} for name, weight in members],
        'output_sign': sign, 'output_offset': offset,
        'fixed_before_complete_quality': True,
        'score_requires_mature_past_return_mapping': True}


CONFIGS = {
    'classifier_binary_mean': config([(name, .5) for name in binary]),
    'classifier_decile_mean': config([(name, .5) for name in decile]),
    **{f'classifier_head_mix_b{int(weight*100):03d}': config(
        [(name, weight/2) for name in binary] + [(name, (1-weight)/2) for name in decile])
       for weight in (.25, .5, .75)},
    'classifier_decile_reflected_mean': config([(name, .5) for name in decile], sign=-1., offset=1.),
}


def predict_arrays(bundle, x):
    import numpy as np
    assert bundle['kind'] == 'classifier_consensus'
    result = np.zeros(len(x), dtype=np.float64)
    for member in bundle['members']:
        result += member['weight'] * parent.core.predict_arrays(member['bundle'], x)
    result = bundle['config']['output_sign'] * result + bundle['config']['output_offset']
    assert np.isfinite(result).all()
    return result


def bundle_from(name, year):
    cfg = CONFIGS[name]
    members, meta, sources = [], None, {}
    for member in cfg['members']:
        folder = parent.OUT / member['model']
        info_path, model_path = folder / f'info_{year}.json', folder / f'model_{year}.joblib'
        info = read(info_path)
        assert info['status'] == 'passed' and info['completed_epochs'] == 32
        assert info['actual_native_sample_counter'] == 1 + 32 * info['training_meta']['rows']
        assert sha(model_path) == info['model_sha256']
        model = parent.core.load_bundle(model_path)
        assert model['classifier'].t_ == info['actual_native_sample_counter']
        meta = info['training_meta'] if meta is None else meta
        assert meta == info['training_meta']
        assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
        members.append({'name': member['model'], 'weight': member['weight'], 'bundle': model,
                        'model_sha256': info['model_sha256']})
        sources[str(info_path)] = sha(info_path)
        sources[str(model_path)] = info['model_sha256']
    assert sum(member['weight'] for member in members) == 1.
    return {'kind': 'classifier_consensus', 'config': cfg, 'members': members,
            'new_model_fits': 0, 'fixed_weights_not_learned': True}, meta, sources


def verify():
    protocol = read(OUT / 'protocol.json')
    for path, digest in protocol['input_sha256'].items():
        assert sha(path) == digest, path
    return protocol


def freeze():
    OUT.mkdir(exist_ok=True)
    if (OUT / 'protocol.json').exists():
        return verify()
    assert read(parent.OUT / 'oof_audit.json')['actual_annual_fits'] == 20
    assert read(A / 'classifier_consensus_preflight_20261005/verification.json')['status'] == 'passed_actual_native_parent_consensus_reload_and_prefix'
    assert read(A / 'classifier_consensus_direct_router_preflight_20261005/verification.json')['status'] == 'passed_actual_consensus_and_inherited_routes'
    assert read(A / 'streaming_rank_classifier_future_qa_v3_20261005/verification.json')['actual_fulltraining_fits'] == 4
    paths = [Path(__file__), SOURCE, parent.SOURCE, PLAN,
        A / 'classifier_consensus_preflight_20261005/verification.json',
        A / 'classifier_consensus_direct_router_preflight_20261005/verification.json',
        A / 'run_classifier_consensus_bank_20261005.py',
        A / 'classifier_consensus_model_sources_20261005.py',
        A / 'classifier_consensus_future_codec_adapter_20261005.py',
        A / 'verify_classifier_consensus_preflight_20261005.py',
        A / 'verify_classifier_consensus_full_future_20261005.py',
        A / 'classifier_consensus_bank_run_20261005.json', A / 'classifier_consensus_future_run_20261005.json',
        A / 'streaming_classifier_actual_annual_completion_audit_20261005/verification.json',
        A / 'streaming_classifier_actual_final_completion_audit_20261005/verification.json',
        A / 'streaming_classifier_signal_complementarity_20261005/verification.json',
        parent.OUT / 'protocol.json', parent.OUT / 'oof_audit.json', parent.OUT / 'training_execution_scope.json',
        A / 'connected_validation_20261002/combined_fold_frame.parquet', FEATURE_FILE, MANIFEST, ROOT / '后续选模标准.md']
    paths += list(parent.OUT.glob('*/info_*.json')) + list(parent.OUT.glob('*/model_*.joblib'))
    paths += list(parent.OUT.glob('*/raw_202[0-4].parquet'))
    paths += [Path(path) for path in read(parent.OUT / 'protocol.json')['input_sha256']]
    dump(OUT / 'protocol.json', {
        'status': 'frozen_before30_actual_full_virtual_annual_outputs',
        'configurations': CONFIGS, 'years': YEARS, 'expected_virtual_annual_outputs': 30,
        'expected_new_native_fits': 0, 'reused_native_annual_fits': 20, 'reused_native_final_fits': 4,
        'all_six_fixed_composites_including_explicit_reflection_compete': True,
        'correlation_diagnostic_is_not_a_selection_gate': True,
        'actual_model_reload_and_real80_day_prefix_required_for_each_artifact': True,
        'actual6_fullfuture_and_complete_official_quality_still_required': True,
        'test_labels_read': False, 'new_quality_scores': 0,
        'input_sha256': {str(path.resolve()): sha(path) for path in dict.fromkeys(paths)}}, immutable=True)
    return read(OUT / 'protocol.json')


def infer_stream(bundle, condition, path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    features = parent.feature_names()
    writer, rows = None, 0
    try:
        for batch in parent.core.scanner(KEYS + ['price_valid'] + features, condition, 65536):
            if not len(batch):
                continue
            pred = predict_arrays(bundle, parent.core.matrix(batch, features))
            pred[~batch.column('price_valid').to_numpy(zero_copy_only=False)] = -1e6
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
    """Create a fixed artifact; no estimator fit call occurs here."""
    import numpy as np
    import polars as pl
    import psutil
    import pyarrow.dataset as ds
    verify()
    while psutil.virtual_memory().available < 4 * 2**30:
        time.sleep(10)
    folder = OUT / name
    folder.mkdir(exist_ok=True)
    model_path, info_path = folder / f'model_{year}.joblib', folder / f'info_{year}.json'
    if info_path.exists():
        info = read(info_path)
        assert info['status'] == 'passed' and info['configuration'] == CONFIGS[name]
        assert sha(model_path) == info['model_sha256']
        for source, digest in info['parent_source_sha256'].items():
            assert sha(source) == digest, source
        if year < 2025:
            assert sha(folder / f'raw_{year}.parquet') == info['prediction_sha256']
            assert info['model_reload_bit_identical'] and info['actual_cold80_day_native_ensemble_bit_identical']
        return info
    started = time.monotonic()
    bundle, meta, sources = bundle_from(name, year)
    parent.core.save_bundle(model_path, bundle)
    info = {'status': 'passed', 'model': name, 'year': year, 'configuration': CONFIGS[name],
        'training_meta': meta, 'new_model_fits': 0, 'fit_seconds': 0.,
        'model_sha256': sha(model_path), 'parent_source_sha256': sources,
        'actual_reused_native_parents': len(bundle['members']),
        'virtual_artifact_not_new_native_fit': True, 'test_data_read': False}
    if year < 2025:
        reference = (pl.scan_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet')
            .filter(pl.col('trade_date') // 10000 == year).select(KEYS + ['price_valid']).collect())
        raw = np.zeros(len(reference), dtype=np.float64)
        for member in CONFIGS[name]['members']:
            path = parent.OUT / member['model'] / f'raw_{year}.parquet'
            native_info = read(parent.OUT / member['model'] / f'info_{year}.json')
            assert sha(path) == native_info['prediction_sha256']
            frame = pl.read_parquet(path)
            assert frame.select(KEYS).equals(reference.select(KEYS))
            raw += member['weight'] * frame['pred_raw'].to_numpy()
            sources[str(path)] = native_info['prediction_sha256']
        raw = CONFIGS[name]['output_sign'] * raw + CONFIGS[name]['output_offset']
        raw[~reference['price_valid'].to_numpy()] = -1e6
        assert np.isfinite(raw).all()
        output = folder / f'raw_{year}.parquet'
        reference.select(KEYS).with_columns(pl.Series('pred_raw', raw)).write_parquet(output)
        prefix_cutoff = int(reference['trade_date'].unique().sort()[79])
        prefix_path = folder / f'prefix_control_{year}.parquet'
        condition = ((ds.field('is_train') == True) & (ds.field('trade_date') >= year*10000+101)
                     & (ds.field('trade_date') <= prefix_cutoff))
        infer_stream(parent.core.load_bundle(model_path), condition, prefix_path)
        prefix = pl.read_parquet(prefix_path).sort('trade_date', 'ts_code')
        expected = pl.read_parquet(output).filter(pl.col('trade_date') <= prefix_cutoff)
        assert prefix.equals(expected)
        assert prefix_path.resolve().is_relative_to(OUT.resolve())
        prefix_path.unlink()
        info.update(rows=len(reference), prediction_sha256=sha(output), model_reload_bit_identical=True,
                    actual_cold80_day_native_ensemble_bit_identical=True)
    else:
        info['fulltraining_only_test_prediction_not_generated'] = True
    info['elapsed_seconds'] = time.monotonic()-started
    dump(info_path, info, immutable=True)
    log(f'Actual classifier consensus {name} year{year}: reused parents; native fits0; {info["elapsed_seconds"]:.1f}s')
    gc.collect()
    return info


def all_oof():
    freeze()
    checks = []
    for name in CONFIGS:
        for year in YEARS:
            info = train_one(name, year)
            assert info['actual_cold80_day_native_ensemble_bit_identical']
            checks.append({'model': name, 'year': year, 'info_sha256': sha(OUT/name/f'info_{year}.json'),
                           'new_native_fits': 0, 'actual_cold80_and_model_reload_passed': True})
    verify()
    dump(OUT/'oof_audit.json', {'status': 'passed', 'actual_virtual_annual_outputs': 30,
        'actual_annual_fits': 0, 'reused_native_annual_fits': 20, 'checks': checks,
        'complete_official_quality_still_pending': True, 'test_labels_read': False, 'new_quality_scores': 0}, immutable=True)


engine = SimpleNamespace(FEATURE_FILE=FEATURE_FILE, MANIFEST=MANIFEST, KEYS=KEYS,
    feature_names=parent.feature_names, to_matrix=parent.to_matrix, load_bundle=parent.core.load_bundle,
    save_bundle=parent.core.save_bundle, predict_arrays=predict_arrays)
