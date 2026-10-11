"""Complete thirty virtual OOF artifacts and six actual full future controls."""
from pathlib import Path
from datetime import datetime
import gc
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import quantile_distribution_views_20261006 as core
import quantile_distribution_views_future_codec_20261006 as codec

parent = core.parent
engine = parent.engine
CONFIGS, YEARS, KEYS = core.CONFIGS, parent.YEARS, engine.KEYS
OUT = A / 'quantile_distribution_views_bank_20261006'
FUTURE = A / 'quantile_distribution_views_future_qa_20261006'
PLAN = A / 'quantile_distribution_views_complete_plan_20261006.json'
SOURCE = Path(core.__file__)
read, dump, sha, log = parent.read, parent.dump, parent.sha, engine.log
predict_arrays = core.predict_arrays
RESOURCE = None


def sources():
    paths = [Path(__file__), SOURCE, Path(codec.__file__), PLAN,
        A / 'run_quantile_distribution_views_workflow_20261006.py',
        A / 'quantile_distribution_views_model_sources_20261006.py',
        A / 'quantile_tree_future_codec_20261006.py',
        A / 'verify_quantile_distribution_views_preflight_20261006.py',
        A / 'quantile_distribution_views_preflight_20261006/verification.json',
        A / 'quantile_distribution_views_preflight_20261006/execution_scope.json',
        A / 'locked_read_hash_cache_20261004.py',
        A / 'linear_leaf_actual_resource_sampler_20261005.py',
        parent.OUT / 'protocol.json', parent.OUT / 'oof_audit.json',
        parent.OUT / 'training_execution_scope.json',
        A / 'quantile_tree_memmap_future_qa_20261006/verification.json',
        A / 'quantile_tree_memmap_future_qa_20261006/execution_scope.json',
        A / 'quantile_tree_memmap_complete_bank_github_20261006/receipt.json',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / '后续选模标准.md']
    paths += [Path(path) for path in read(parent.OUT / 'protocol.json')['input_sha256']]
    for name in core.MEMBERS:
        for year in (*YEARS, 2025):
            paths += [parent.OUT / name / f'info_{year}.json', parent.OUT / name / f'model_{year}.joblib']
            if year < 2025:
                paths.append(parent.OUT / name / f'raw_{year}.parquet')
        paths.append(A / f'quantile_tree_memmap_future_qa_20261006/{name}_raw.parquet')
    return list(dict.fromkeys(paths))


def verify():
    protocol = read(OUT / 'protocol.json')
    for filename, digest in protocol['input_sha256'].items():
        assert sha(filename) == digest, filename
    return protocol


def freeze():
    assert not OUT.exists() and not FUTURE.exists()
    audit = read(parent.OUT / 'oof_audit.json')
    assert audit['status'] == read(parent.OUT / 'training_execution_scope.json')['status'] == 'passed'
    assert audit['actual_annual_fits'] == 20
    future = read(A / 'quantile_tree_memmap_future_qa_20261006/verification.json')
    assert future['status'] == 'passed' and future['actual_full_final_fits'] == 4
    preflight = read(A / 'quantile_distribution_views_preflight_20261006/verification.json')
    assert preflight['status'] == 'passed_actual_six_distribution_views_native_cold80_independent_codec_and_math_controls'
    assert preflight['actual_native_views_checked'] == 6 and preflight['pilot_weights_written_to_disk'] == 0
    receipt = read(A / 'quantile_tree_memmap_complete_bank_github_20261006/receipt.json')
    assert receipt['status'] == 'pushed_actual_controls_main_only' and receipt['control_status'] == 'passed'
    plan = read(PLAN)
    assert plan['configurations'] == CONFIGS and plan['quality_records'] == {'93': 124, '94': 138}
    OUT.mkdir()
    FUTURE.mkdir()
    protocol = {'status': 'frozen_before_complete30_virtual_annual_outputs_and6_full_future_checks',
        'frozen_at_local': datetime.now().isoformat(), 'configurations': CONFIGS, 'years': YEARS,
        'expected_virtual_annual_outputs': 30, 'expected_virtual_final_outputs': 6,
        'actual_new_native_fits_required': 0, 'unique_native_return_annual_parents_reused': 15,
        'unique_native_return_final_parents_reused': 3,
        'all_original20_annual4_final_native_fits_qualified_before_start': True,
        'original198_quality_records_preserved': True, 'additional_quality_records_required': 262,
        'additional_quality_rounds': [93, 94], 'explicit_parent_rounds': {'93': 92, '94': 93},
        'all6_views_compete_no_extra_risk_or_orientation_gate': True,
        'pointwise_ordering_and_view_transforms_use_no_future_rows_or_labels_or_learned_weights': True,
        'actual_full1599600_row_selfcontained_codec_reload_and_cold80_each_view_required': True,
        'only_official_complete5635800_row_continuous_return_mapped_CSV_score_selects': True,
        'all_previous_training_folds_viewed_selection_bias_uncorrected': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in sources()}}
    dump(OUT / 'protocol.json', protocol, immutable=True)
    return protocol


def train_one(name, year):
    """Only create a self-contained frozen transform artifact; never fit an estimator."""
    import numpy as np
    verify()
    folder = OUT / name
    info = read(folder / f'info_{year}.json')
    assert info['status'] == 'passed' and info['configuration'] == CONFIGS[name]
    assert sha(folder / f'model_{year}.joblib') == info['model_sha256']
    bundle = engine.load_bundle(folder / f'model_{year}.joblib')
    assert bundle['config'] == CONFIGS[name] and bundle['new_model_fits'] == 0
    for filename, digest in info['parent_source_sha256'].items():
        assert sha(filename) == digest
    if year < 2025:
        assert sha(folder / f'raw_{year}.parquet') == info['prediction_sha256']
        assert info['actual_cold80_selfcontained_reload_bit_identical']
    return info


def prefix_frame(year):
    import polars as pl
    base = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year))
    cutoff = int(base.select('trade_date').unique().sort('trade_date').collect()['trade_date'][79])
    features = engine.feature_names()
    return base.filter(pl.col('trade_date') <= cutoff).select(KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()


def all_oof():
    import numpy as np
    import polars as pl
    proof = verify()
    annual_checks, final_checks = [], []
    for year in YEARS:
        if RESOURCE is not None:
            RESOURCE.context = {'stage': 'actual_complete_annual_fixed_distribution_views_and_cold80', 'year': year}
        frames = [pl.read_parquet(parent.OUT / member / f'raw_{year}.parquet') for member in core.MEMBERS]
        keys = frames[0].select(KEYS)
        reference = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(KEYS + ['price_valid']).sort('trade_date', 'ts_code').collect()
        assert keys.equals(reference.select(KEYS))
        assert all(frame.select(KEYS).equals(keys) for frame in frames)
        heads = np.stack([frame['pred_raw'].to_numpy() for frame in frames])
        valid = reference['price_valid'].to_numpy()
        prefix = prefix_frame(year)
        assert len(prefix) == 372000 and prefix.select(KEYS).equals(keys.head(len(prefix)))
        x = engine.to_matrix(prefix, engine.feature_names())
        for name, cfg in CONFIGS.items():
            folder = OUT / name
            folder.mkdir(exist_ok=True)
            assert not (folder / f'info_{year}.json').exists()
            bundle, meta, bindings = core.bundle_from(name, year)
            assert (meta['features'], meta['validation_year']) == (engine.feature_names(), year)
            model = folder / f'model_{year}.joblib'
            engine.save_bundle(model, bundle)
            reloaded = engine.load_bundle(model)
            assert reloaded['config'] == bundle['config'] and reloaded['new_model_fits'] == 0
            assert all(a['bundle']['model_string'] == b['bundle']['model_string'] for a, b in zip(bundle['members'], reloaded['members']))
            raw, independent = core.from_heads(cfg, heads), codec.from_heads(cfg, heads)
            assert np.array_equal(raw, independent)
            raw[~valid] = -1e6
            cold = codec.predict_arrays(reloaded, x)
            cold[~prefix['price_valid'].to_numpy()] = -1e6
            assert np.array_equal(cold, raw[:len(prefix)])
            output = folder / f'raw_{year}.parquet'
            keys.with_columns(pl.Series('pred_raw', raw)).write_parquet(output)
            bindings.update({str((parent.OUT / member / f'raw_{year}.parquet').resolve()): sha(parent.OUT / member / f'raw_{year}.parquet') for member in core.MEMBERS})
            info = {'status': 'passed', 'model': name, 'year': year, 'configuration': cfg,
                'training_meta': meta, 'parent_source_sha256': bindings,
                'model_sha256': sha(model), 'prediction_sha256': sha(output), 'rows': len(keys),
                'model_reload_bit_identical': True,
                'reload_scope': 'All embedded native model strings byte-identical; entire annual two independent pointwise transforms match full native-reload-qualified parent predictions; actual372000row selfcontained cold80 matches.',
                'actual_cold80_selfcontained_reload_bit_identical': True,
                'actual_entire_annual_independent_pointwise_transform_bit_identical': True,
                'virtual_artifact_not_new_native_fit': True, 'new_model_fits': 0, 'fit_seconds': 0.,
                'actual_reused_native_parents': 3, 'new_quality_scores': 0, 'test_labels_read': False}
            dump(folder / f'info_{year}.json', info, immutable=True)
            annual_checks.append({'model': name, 'year': year, 'rows': len(keys), 'cold80_rows': len(prefix),
                'model_sha256': info['model_sha256'], 'prediction_sha256': info['prediction_sha256'], 'new_model_fits': 0})
            print(__import__('json').dumps({'status': 'passed_actual_complete_annual_distribution_view', **annual_checks[-1]}), flush=True)
            del raw, independent, cold, bundle, reloaded
        del frames, keys, reference, heads, prefix, x
        gc.collect()
    for name, cfg in CONFIGS.items():
        folder = OUT / name
        bundle, meta, bindings = core.bundle_from(name, 2025)
        engine.save_bundle(folder / 'model_2025.joblib', bundle)
        info = {'status': 'passed', 'model': name, 'year': 2025, 'configuration': cfg,
            'training_meta': meta, 'parent_source_sha256': bindings,
            'model_sha256': sha(folder / 'model_2025.joblib'), 'new_model_fits': 0, 'fit_seconds': 0.,
            'fulltraining_only_test_prediction_not_generated': True, 'virtual_artifact_not_new_native_fit': True,
            'actual_reused_native_parents': 3, 'new_quality_scores': 0, 'test_labels_read': False}
        dump(folder / 'info_2025.json', info, immutable=True)
        final_checks.append({'model': name, 'model_sha256': info['model_sha256'], 'new_model_fits': 0})
    for name in CONFIGS:
        keys = pl.concat([pl.read_parquet(OUT / name / f'raw_{year}.parquet', columns=KEYS) for year in YEARS])
        assert (len(keys), keys['trade_date'].n_unique(), keys['ts_code'].n_unique()) == (5635800, 1212, 4650)
        assert not keys.is_duplicated().any() and keys.equals(keys.sort('trade_date', 'ts_code'))
    assert len(annual_checks) == 30 and len(final_checks) == 6
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'actual_virtual_annual_outputs': 30,
        'actual_virtual_final_artifacts': 6, 'unique_native_annual_parents_reused': 15,
        'unique_native_final_parents_reused': 3, 'new_model_fits': 0,
        'all6_complete5635800row1212day4650code_continuous_keys_passed': True,
        'annual_checks': annual_checks, 'final_checks': final_checks,
        'required_complete_quality_records': 262, 'original198_preserved': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


def all_future():
    import numpy as np
    import polars as pl
    assert read(OUT / 'oof_audit.json')['status'] == 'passed'
    features = engine.feature_names()
    frame = pl.scan_parquet(engine.FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
    assert (len(frame), frame['trade_date'].n_unique(), frame['ts_code'].n_unique()) == (1599600, 344, 4650)
    native = [pl.read_parquet(A / f'quantile_tree_memmap_future_qa_20261006/{member}_raw.parquet') for member in core.MEMBERS]
    assert all(part.select(KEYS).equals(frame.select(KEYS)) for part in native)
    heads = np.stack([part['pred_raw'].to_numpy() for part in native])
    valid = frame['price_valid'].to_numpy()
    x = engine.to_matrix(frame, features)
    checks = []
    for name, cfg in CONFIGS.items():
        if RESOURCE is not None:
            RESOURCE.context = {'stage': 'all1599600_future_rows_actual_selfcontained_reload_and_cold80', 'model': name}
        info = read(OUT / name / 'info_2025.json')
        assert info['training_meta']['cutoff_exclusive'] <= int(frame['trade_date'].min())
        model = OUT / name / 'model_2025.joblib'
        dump(FUTURE / f'{name}_frozen_before_actual_inference.json', {
            'model_sha256': sha(model), 'configuration': cfg, 'rows': len(frame),
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
        direct = codec.predict_arrays(engine.load_bundle(model), x)
        direct[~valid] = -1e6
        saved = core.from_heads(cfg, heads)
        saved[~valid] = -1e6
        assert np.array_equal(direct, saved)
        cold = core.predict_arrays(engine.load_bundle(model), x[:372000])
        cold[~valid[:372000]] = -1e6
        assert np.array_equal(direct[:372000], cold)
        path = FUTURE / f'{name}_raw.parquet'
        frame.select(KEYS).with_columns(pl.Series('pred_raw', direct)).write_parquet(path)
        checks.append({'model': name, 'rows': len(frame), 'days': 344, 'codes': 4650,
            'model_sha256': info['model_sha256'], 'raw_sha256': sha(path),
            'actual_whole_future_selfcontained_independent_codec_bit_identical': True,
            'actual_cold80_reload372000_rows_bit_identical': True,
            'new_model_fits': 0, 'test_labels_read': False})
        print(__import__('json').dumps({'status': 'passed_actual_complete_future_distribution_view', 'model': name, 'rows': len(frame)}), flush=True)
        del direct, saved, cold
        gc.collect()
    dump(FUTURE / 'verification.json', {'status': 'passed', 'actual_full_future_views': 6,
        'actual_native_fits': 0, 'checks': checks, 'all6_entire_future_and_cold80_passed': True,
        'required_complete_quality_records': 262, 'original198_preserved': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
