"""Select from44 complete official scores; reuse exact anchor or freeze new native inference."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import hashlib
import os
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
OUT = A / 'CPU_ELASTIC_residual44_selected_release_20261007'
CANDIDATE = ROOT / 'candidates/CPU_ELASTIC_residual44_20261007'
GRAPH_FIELD = 'conditional_flag_residual_scheme_graph'


def closed(name):
    folder = A / 'service_owned_workflows_20261006' / name
    while not (folder / 'native_launch.json').exists() or owned(read(folder / 'native_launch.json')):
        time.sleep(15)
    assert read(folder / 'service_execution.json')['status'] == 'passed', name


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    import psutil
    from run import fold_cutoff
    from full_universe_HGB_percentile_CDF_transform_20261007 import transform
    from score_calibrated_candidates_20261003 import score
    from return_mapping import daily_percentile, fit_mapping
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    assert not OUT.exists()
    OUT.mkdir()
    for name in ('full_universe_ElasticNet44_official_comparison', 'cpu_full_universe_ElasticNet24_scores_evidence_publication_v2'):
        closed(name)
    while psutil.virtual_memory().available < 9 * 2**30:
        time.sleep(15)
    pilot_folder = A / 'full_universe_ElasticNet44_official_comparison_20261007'
    pilot_path = pilot_folder / 'verification.json'
    pilot = read(pilot_path)
    assert pilot['status'] == 'passed_actual44_full_universe_CPU_ElasticNet_CDF_full_official_comparisons'
    assert len(pilot['records']) == 44
    best = min(pilot['records'], key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    assert best == pilot['best']
    cfg = best['configuration']
    parent_candidate = ROOT / 'candidates/simplex_residual47_20261006'
    parent_release = A / 'simplex_residual47_release_20261006'
    parent_record = read(parent_candidate / 'selection.json')
    parent_prediction = read(parent_candidate / 'verification.json')
    parent_manifest = read(parent_candidate / 'manifest.json')
    bank = A / 'cpu_full_universe_ElasticNet_bank24_20261007'
    sources = [Path(__file__), A / 'predict_full_universe_CPU_ElasticNet_rank_CDF_scheme_20261007.py',
        A / 'seal_CPU_ELASTIC_residual44_selected_candidate_20261007.py',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py', A / 'cpu_ElasticNet_independent_linear_codec_20261007.py',
        pilot_path, A / 'cpu_full_universe_ElasticNet24_scores_github_20261007/receipt.json',
        parent_candidate / 'manifest.json', parent_release / 'source_package_verification.json']
    pins = {**pilot['input_sha256'], **{str(p): sha(p) for p in sources}}
    for relative, info in parent_manifest['files'].items():
        path = parent_candidate / relative
        assert sha(path) == info['sha256'], path
        pins[str(path)] = info['sha256']
    create(OUT / 'selected_case_before_future_features.json', {'status': 'selected_by_all44_actual_final_mapped_CSV_official_scores',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'best': best,
        'selection_rule': 'Highest complete original official S; ties lower amplitude then case',
        'new_native_fits_by_qualification': 0, 'future_features_for_new_selected_scheme_not_yet_read': True, 'test_labels_read': False})
    if cfg['model'] is None:
        assert best['case'] == 1 and cfg == {'anchor_round': 106, 'model': None, 'weight': 0., 'universe': None}
        assert best['metrics'] == parent_record['winner']['metrics']
        raw = np.load(A / 'optimization_20261003_r106/selected_validation.npy', mmap_mode='r')
        original = np.load(parent_release / 'selected_validation.npy', mmap_mode='r')
        assert np.array_equal(raw.view(np.uint64), original.view(np.uint64))
        assert hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest() == best['prediction_numeric_bytes_sha256']
        assert parent_prediction['status'] == 'passed' and len(parent_prediction['models']) == 15
        for key in ('model_reload_bit_identical', 'pipeline_replay_bit_identical', 'csv_replay_byte_identical', 'cold80_day_prefix_bit_identical'):
            assert parent_prediction[key]
        assert sha(parent_candidate / 'submission.csv') == parent_prediction['csv_sha256']
        create(OUT / 'inference_ready.json', {'status': 'passed_exact_selected_anchor44_candidate_reuse',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'selected_configuration': cfg, 'best': best,
            'source_candidate': str(parent_candidate), 'source_release': str(parent_release),
            'manifest_sha256': sha(parent_candidate / 'manifest.json'), 'actual_saved_native_models': 15,
            'actual_rehashed_candidate_files': len(parent_manifest['files']),
            'original_inference_freeze_timestamp': parent_record['frozen_at_local'],
            'all5635800_validation_raw_bits_and_all8_metrics_exact': True,
            'new_inference_claimed': False, 'test_labels_read': False})
        return
    assert cfg['anchor_round'] == 106 and cfg['weight'] > 0.
    names = pilot['ensembles'].get(cfg['model'], [cfg['model']])
    assert 1 <= len(names) <= 4 and len(set(names)) == len(names)
    infos = [read(bank / name / 'info_2025.json') for name in names]
    for info in infos:
        assert info['year'] == 2025 and 0 < info['actual_iterations'] <= 2000
        assert info['training_metadata']['last_training_label_date'] < info['training_metadata']['exclusive_cutoff'] == fold_cutoff(2025)
        assert info['training_metadata']['last_training_label_end'] <= info['training_metadata']['exclusive_cutoff']
    freeze = A / 'CPU_ELASTIC_residual44_pre_inference_source_freeze_20261007'
    assert not freeze.exists() and not CANDIDATE.exists()
    freeze.mkdir()
    python_sources = sorted(set(ROOT.glob('*.py')) | set(A.glob('*.py')) |
        set((A / 'connected_validation_20261002').glob('*.py')) | set((ROOT / 'src').rglob('*.py')) |
        set((ROOT / 'experiments').rglob('*.py')))
    snapshot = {}
    for source in python_sources:
        digest = sha(source)
        target = freeze / 'repo' / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(target) == sha(source) == digest
        snapshot[source.relative_to(ROOT).as_posix()] = {'sha256': digest, 'bytes': source.stat().st_size}
        pins[str(source)] = digest
    import importlib.metadata
    create(freeze / 'manifest.json', {'status': 'passed_pre_inference_local_Python_source_snapshot',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'files': snapshot,
        'library_versions': {name: importlib.metadata.version(name) for name in
            ('numpy', 'pandas', 'polars', 'scikit-learn', 'joblib', 'lightgbm', 'torch')},
        'test_labels_read': False})
    pins[str(freeze / 'manifest.json')] = sha(freeze / 'manifest.json')
    for info in infos:
        pins[info['native_model_path']] = info['native_model_sha256']
        pins[info['independent_linear_state_path']] = info['independent_linear_state_sha256']
    prediction_source = pilot_folder / f'{cfg["model"]}_centered_oof_predictions.npy' if cfg['model'] not in pilot['ensembles'] else pilot_folder / f'{cfg["model"]}.npy'
    pins[str(prediction_source)] = sha(prediction_source)
    with LockedReadHashCache(pins) as scope:
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'price_valid', 'y_ret_1d'])
        dates, flags, valid = (frame[k].to_numpy() for k in ('trade_date', 'flag_limit_up', 'price_valid'))
        raw = np.load(A / 'optimization_20261003_r106/selected_validation.npy', mmap_mode='r')
        residual = np.load(prediction_source, mmap_mode='r')
        selected = transform(raw, dates, flags, valid, residual, cfg['weight'], cfg['universe'])
        assert hashlib.sha256(memoryview(np.ascontiguousarray(selected)).cast('B')).hexdigest() == best['prediction_numeric_bytes_sha256']
        np.save(OUT / 'selected_validation.npy', selected)
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for filename in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(A / 'optimization_20261003_r95/scoring_validation_only' / filename, scoring / filename)
        ctx = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        assert score(ctx, selected) == best['metrics']
        capsule = read(ctx.last_official_score_cache['official_metrics_source'])
        create(OUT / 'calibrated_csv_official.json', {'status': 'passed', 'metrics': best['metrics'],
            'csv_sha256': capsule['scope']['submission_csv_sha256'], 'actual_official_capsule': ctx.last_official_score_cache,
            'actual_mature_return_mapping': ctx.last_candidate_return_mapping, 'test_labels_read': False})
        labels = pd.read_csv(scoring / '测试集_Y.csv').sort_values(['trade_date', 'ts_code']).reset_index(drop=True)
        assert np.array_equal(labels.trade_date.to_numpy(), dates)
        cutoff = fold_cutoff(2025)
        y = labels.y_ret_1d.to_numpy(dtype=np.float64)
        historical = (dates < cutoff) & np.isfinite(y)
        pct = daily_percentile(frame.select('trade_date').to_pandas(), selected)
        create(OUT / 'future_return_mapping.json', fit_mapping(pct[historical], y[historical]))
        create(OUT / 'causal_validation.json', {'status': 'passed', 'all44_original_official_controls': str(pilot_path),
            'all24_mature_native_and_independent_numpy_and_prefix_controls': str(bank / 'verification.json'),
            'actual_selected_full5635800_numeric_bits_match_pilot': True, 'final_mapping_training_rows': int(historical.sum()),
            'exclusive_cutoff': cutoff, 'new_native_fits_by_qualification': 0, 'test_labels_read': False})
        graph = deepcopy(parent_prediction['whole_scheme_graph'])
        graph['cohort_rank_calibration']['future_curve_model']['path'] = str(CANDIDATE / 'cohort_curve.json')
        for component in graph['conditional_flag_residual']['native_components']:
            component['path'] = str(CANDIDATE / (component['name'] + '_model.txt'))
            component['independent_dump_path'] = str(CANDIDATE / (component['name'] + '_dump.json'))
        components = [{'name': info['name'], 'source_path': info['native_model_path'], 'sha256': info['native_model_sha256'],
            'path': str(CANDIDATE / (info['name'] + '.joblib')),
            'independent_state_source_path': info['independent_linear_state_path'],
            'independent_state_path': str(CANDIDATE / (info['name'] + '.json')),
            'independent_state_sha256': info['independent_linear_state_sha256'], 'training_info': info} for info in infos]
        graph['full_universe_CPU_ElasticNet_rank_CDF'] = {**cfg, 'native_components': components,
            'ordered_equal_mean_components': names, 'actual2020_native_fold': True,
            'transformation': 'q=(1-weight)*parent_percentile+weight*(ordered_mean_of_each_head_daily_percentile); same-day parent inverseCDF',
            'full_pool_including_nonflag': True, 'each_head_rank_before_ordered_mean': True}
        winner = deepcopy(parent_record['winner'])
        winner.update(metrics=best['metrics'], connected_final_score=best['connected_final_score'])
        winner[GRAPH_FIELD] = graph
        protocol = deepcopy(read(parent_release / 'protocol.json'))
        protocol.update(input_sha256=pins, explicit_parent_round=106, expected_scored_records=44,
            status='frozen_selected_CPU_ELASTIC44_candidate_before_future_inference', current_parameter_authority=GRAPH_FIELD)
        create(OUT / 'protocol.json', protocol)
        frozen = {Path(p).relative_to(ROOT).as_posix(): digest for p, digest in pins.items() if Path(p).is_relative_to(ROOT)}
        for path in (OUT / 'protocol.json', OUT / 'selected_validation.npy', OUT / 'future_return_mapping.json', ROOT / 'active_release.json'):
            frozen[path.relative_to(ROOT).as_posix()] = sha(path)
        selection = {'status': 'frozen_before_test_prediction', 'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'winner': winner, 'scored_records': 44, 'explicit_parent_round': 106, 'chosen_postprocessor': cfg,
            'native_component_names': [*parent_record['native_component_names'], *names], 'new_HGB_component_names': names,
            'current_parameter_authority': GRAPH_FIELD, 'actual_official_pilot_source': str(pilot_path),
            'frozen_sha256': frozen, 'all_training_validation_years_previously_viewed': True,
            'selection_bias_uncorrected': True, 'test_labels_read': False}
        create(OUT / 'selection.json', selection)
        create(OUT / 'frozen_before_actual_candidate_inference.json', {'input_sha256': pins,
            'selection_sha256': sha(OUT / 'selection.json'), 'source_snapshot_manifest_sha256': sha(freeze / 'manifest.json'),
            'parent_curve_sha256': sha(parent_candidate / 'cohort_curve.json'), 'test_labels_read': False})
        locked_outputs = {str(OUT / name): sha(OUT / name) for name in ('protocol.json', 'selection.json', 'selected_validation.npy', 'future_return_mapping.json')}
        import optimize_training_round95_v3 as native_parent
        ns = SimpleNamespace(**vars(native_parent))
        ns.OUT, ns.GRAPH_FIELD = OUT, GRAPH_FIELD
        ns.cohort_saved_models = parent_prediction['models']
        from predict_full_universe_CPU_ElasticNet_rank_CDF_scheme_20261007 import predict
        with LockedReadHashCache(locked_outputs) as output_scope:
            prediction, storage = predict(ns, selection, CANDIDATE, parent_candidate / 'cohort_curve.json', OUT / 'future_return_mapping.json')
            output_scope.reverify()
        scope.reverify()
        assert (prediction['rows'], prediction['days'], prediction['codes']) == (1599600, 344, 4650)
        assert len(prediction['models']) == len(storage) == 15 + len(names)
        create(OUT / 'verification.json', {'status': 'passed_frozen_CPU_ELASTIC44_full_native_parent_independent_numpy_and_cold80',
            'input_sha256': pins, 'candidate': str(CANDIDATE), 'csv_sha256': prediction['csv_sha256'],
            'selected_configuration': cfg, 'selected_official_score': best['connected_final_score'],
            'actual_native_model_storage': storage, 'actual_saved_model_count': len(prediction['models']),
            'all_inputs_initial_and_final_full_Windows_read_locked_hash': True, 'new_native_fits': 0, 'test_labels_read': False})
        create(OUT / 'inference_ready.json', {'status': 'passed_actual_selected_new_CPU_ELASTIC44_candidate_inference',
            'source_candidate': str(CANDIDATE), 'source_release': str(OUT), 'selected_configuration': cfg, 'best': best,
            'actual_saved_native_models': len(prediction['models']), 'new_inference_claimed': True,
            'pre_inference_source_snapshot': str(freeze), 'test_labels_read': False})


if __name__ == '__main__':
    main()
