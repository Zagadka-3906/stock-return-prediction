"""Build self-contained mature-model mixtures; no parent or ensemble fitting."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
import train_linear_leaf_bank_20261005 as parent

SOURCE = Path(parent.__file__)
engine = parent.engine
read, dump, sha, log = parent.read, parent.dump, parent.sha, parent.log
PLAN = ROOT / 'analysis/linear_leaf_ensemble_complete_search_plan_20261005.json'
STORAGE = ROOT / 'analysis/linear_leaf_ensemble_storage_20261005.json'
OUT = Path(read(STORAGE)['output_directory']) if STORAGE.exists() else ROOT / 'analysis/linear_leaf_ensemble_bank_20261005'
CONFIGS = read(PLAN)['model_configurations']
YEARS = parent.YEARS


def verify():
    protocol = read(OUT / 'protocol.json')
    for source, expected in protocol['input_sha256'].items():
        assert sha(source) == expected, source
    return protocol


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'protocol.json').exists():
        verify()
        return
    audit = parent.OUT / 'oof_audit.json'
    execution = parent.OUT / 'training_execution_scope.json'
    assert read(audit)['status'] == read(execution)['status'] == 'passed'
    assert read(audit)['actual_annual_fits'] == 30
    proof = ROOT / 'analysis/linear_leaf_ensemble_complementarity_v2_20261005/verification.json'
    assert read(proof)['status'] == 'passed_actual_five_year_mixture_native_reload_and_prefix_controls'
    paths = [Path(__file__), SOURCE, PLAN, STORAGE, proof, parent.OUT / 'protocol.json', audit, execution,
        ROOT / 'analysis/run_linear_leaf_ensemble_bank_20261005.py',
        ROOT / 'analysis/prepare_linear_leaf_ensemble_bank_20261005.py',
        ROOT / 'analysis/linear_leaf_ensemble_bank_run_20261005.json',
        ROOT / 'analysis/connected_validation_20261002/combined_fold_frame.parquet',
        engine.FEATURE_FILE, ROOT / '后续选模标准.md']
    paths += [Path(path) for path in read(parent.OUT / 'protocol.json')['input_sha256']]
    paths += list(parent.OUT.glob('*/info_202[0-4].json'))
    paths += list(parent.OUT.glob('*/model_202[0-4].joblib'))
    paths += list(parent.OUT.glob('*/raw_202[0-4].parquet'))
    paths += list(parent.OUT.glob('prefix_control_*.json')) + list(parent.OUT.glob('boundary_control_*.json'))
    dump(OUT / 'protocol.json', {'status': 'frozen_before_actual40_virtual_annual_output_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': CONFIGS, 'years': YEARS,
        'features': engine.feature_names(), 'expected_virtual_annual_artifacts': 40,
        'expected_new_annual_fits': 0, 'actual_parent_annual_fits': 30,
        'method': 'Fixed raw-score averages of mature same-target native300round parent trees.',
        'ensemble_weights_not_learned_or_changed': True,
        'all8_rank_and_return_composites_require_actual80_day_native_prefix_and_reload': True,
        'small_rank_only_preflight_not_substituted_for_all8_virtual_models': True,
        'return_units_same_as_parent_outputs_before_training_only_final_mapping': True,
        'complete_output_official_quality_and_fullfuture_checks_pending': True,
        'selection_bias_uncorrected': True, 'test_labels_read': False, 'new_quality_scores': 0,
        'input_sha256': {str(path.resolve()): sha(path) for path in dict.fromkeys(paths)}}, immutable=True)


def predict_arrays(bundle, x):
    import numpy as np
    assert bundle['kind'] == 'linear_leaf_ensemble'
    result = np.zeros(len(x), dtype=np.float64)
    for member in bundle['members']:
        assert member['weight'] > 0
        result += member['weight'] * parent.predict_arrays(member['bundle'], x)
    assert np.isfinite(result).all()
    return result


def train_one(name, year):
    """Compatibility name for artifact construction: actual new fits always zero."""
    import numpy as np
    import polars as pl
    import joblib
    import psutil
    verify()
    cfg = CONFIGS[name]
    folder = OUT / name
    folder.mkdir(exist_ok=True)
    info_path, model_path = folder / f'info_{year}.json', folder / f'model_{year}.joblib'
    raw_path = folder / f'raw_{year}.parquet'
    if info_path.exists():
        info = read(info_path)
        assert info['new_model_fits'] == 0 and sha(model_path) == info['model_sha256']
        if year < 2025:
            assert sha(raw_path) == info['prediction_sha256']
        return info
    while psutil.virtual_memory().available < 4 * 2**30:
        time.sleep(10)
    started = time.monotonic()
    members, metadata, source_bindings, raw = [], None, {}, None
    reference = None
    if year < 2025:
        reference = pl.scan_parquet(ROOT / 'analysis/connected_validation_20261002/combined_fold_frame.parquet').filter(
            pl.col('trade_date') // 10000 == year).select(engine.KEYS + ['price_valid']).collect()
        raw = np.zeros(len(reference), dtype=np.float64)
    for member in cfg['members']:
        assert member['weight'] > 0 and parent.CONFIGS[member['model']]['target'] == cfg['target']
        source = parent.OUT / member['model']
        info = read(source / f'info_{year}.json')
        assert info['status'] == 'passed' and info['new_model_fits'] == 1
        assert info['training_meta']['last'] < info['training_meta']['cutoff_exclusive']
        assert info['training_meta']['last_label_end'] <= info['training_meta']['cutoff_exclusive']
        metadata = info['training_meta'] if metadata is None else metadata
        assert info['training_meta'] == metadata
        model = source / f'model_{year}.joblib'
        assert sha(model) == info['model_sha256']
        members.append({'name': member['model'], 'weight': member['weight'],
                        'bundle': engine.load_bundle(model), 'model_sha256': info['model_sha256']})
        source_bindings[str(source / f'info_{year}.json')] = sha(source / f'info_{year}.json')
        source_bindings[str(model)] = info['model_sha256']
        if year < 2025:
            path = source / f'raw_{year}.parquet'
            assert sha(path) == info['prediction_sha256']
            frame = pl.read_parquet(path)
            assert frame.select(engine.KEYS).equals(reference.select(engine.KEYS))
            raw += member['weight'] * frame['pred_raw'].to_numpy()
            source_bindings[str(path)] = info['prediction_sha256']
    assert sum(member['weight'] for member in members) == 1.
    bundle = {'kind': 'linear_leaf_ensemble', 'config': cfg, 'members': members,
              'target_units': cfg['target'], 'new_model_fits': 0}
    engine.save_bundle(model_path, bundle)
    info = {'status': 'passed', 'model': name, 'year': year, 'configuration': cfg,
        'training_meta': metadata, 'new_model_fits': 0, 'fit_seconds': 0.,
        'model_sha256': sha(model_path), 'parent_source_sha256': source_bindings,
        'actual_complete_native_parent_models': len(members),
        'weights_fixed_before_any_new_official_quality': True,
        'test_data_read': False, 'virtual_artifact_not_an_independent_model_fit': True}
    if year < 2025:
        valid = reference['price_valid'].to_numpy()
        raw[~valid] = -1e6
        reference.select(engine.KEYS).with_columns(pl.Series('pred_raw', raw)).write_parquet(raw_path)
        dates = reference['trade_date'].unique().sort()
        cutoff = int(dates[79])
        prefix = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') &
            (pl.col('trade_date') // 10000 == year) & (pl.col('trade_date') <= cutoff)).select(
                engine.KEYS + engine.feature_names() + ['price_valid']).sort('trade_date', 'ts_code').collect()
        x = engine.to_matrix(prefix, engine.feature_names())
        predicted = predict_arrays(bundle, x)
        replay = predict_arrays(engine.load_bundle(model_path), x)
        assert np.array_equal(predicted, replay)
        predicted[~prefix['price_valid'].to_numpy()] = -1e6
        assert prefix.select(engine.KEYS).equals(reference.filter(pl.col('trade_date') <= cutoff).select(engine.KEYS))
        assert np.array_equal(predicted, raw[:len(prefix)])
        info.update(prediction_sha256=sha(raw_path), rows=len(reference), model_reload_bit_identical=True,
            actual80_day_native_composite_prefix_bit_identical=True,
            inherited_parent_mature_training_matrices_targets_andkeys_exact=True)
    else:
        info['fulltraining_only_test_prediction_not_generated'] = True
    info['elapsed_seconds'] = time.monotonic() - started
    dump(info_path, info, immutable=True)
    log(f'Actual virtual ensemble {name} year{year}: native fits0; artifact {info["elapsed_seconds"]:.1f}s')
    del bundle, members, raw, reference
    engine.gc.collect()
    return info


def all_oof():
    freeze()
    checks = []
    for name in CONFIGS:
        for year in YEARS:
            info = train_one(name, year)
            checks.append({'model': name, 'year': year, 'info_sha256': sha(OUT / name / f'info_{year}.json'),
                'actual80_day_native_prefix_and_reload_exact': info['actual80_day_native_composite_prefix_bit_identical'],
                'new_model_fits': info['new_model_fits']})
    verify()
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'actual_virtual_annual_outputs': 40,
        'actual_annual_fits': 0, 'actual_parent_annual_fits': 30, 'checks': checks,
        'fullfuture_and_complete_output_official_quality_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    all_oof()
