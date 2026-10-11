"""Freeze the actual50-case winner and replay its saved parent and residual heads."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import hashlib
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '2'
from run_dependency_queue_v3_20261006 import read, create, sha, owned
OUT = A / 'robust_residual50_release_20261006'
CANDIDATE = ROOT / 'candidates/robust_residual50_20261006'
GRAPH_FIELD = 'conditional_flag_residual_scheme_graph'


def main():
    import psutil
    assert psutil.virtual_memory().available >= 8.5 * 2**30
    assert not OUT.exists() and not CANDIDATE.exists()
    service = A / 'service_owned_workflows_20261006/robust_conditional_residual_comparison50_v2'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'passed'
    freeze = A / 'robust_residual50_source_freeze_20261006'
    frozen = read(freeze / 'manifest.json')
    assert frozen['status'] == 'passed_pre_inference_local_Python_source_snapshot'
    for relative, info in frozen['files'].items():
        assert sha(ROOT / relative) == sha(freeze / 'repo' / relative) == info['sha256']
    import numpy as np
    import pandas as pd
    import polars as pl
    import optimize_training_round95_v3 as native_parent
    from conditional_flag_residual_extrapolation_transform_20261006 import transform
    from run import fold_cutoff
    from return_mapping import daily_percentile, fit_mapping
    from score_calibrated_candidates_20261003 import score
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    pilot_folder = A / 'robust_conditional_residual_comparison50_v2_20261006'
    pilot_path = pilot_folder / 'verification.json'
    pilot = read(pilot_path)
    assert pilot['status'] == 'passed_actual50_matched_L1_Huber_residual_and_ensemble_full_official_comparisons'
    best = min(pilot['records'], key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    cfg = best['configuration']
    assert cfg['weight'] > 0 and best['score_gain_over_parent100'] >= 0
    bank = A / 'conditional_residual128_256_bank40_20261006'
    reference = A / 'conditional_flag_residual_bank_20261006'
    names = pilot['ensembles'].get(cfg['model'], [cfg['model']])
    robust = A / 'robust_conditional_residual_bank20_v2_20261006'
    def component_bank(name):
        if name.startswith('robust_residual_'):
            assert name.endswith('_e128')
            return robust
        assert name.startswith('flag_residual_') and name.endswith(('_e64', '_e128', '_e256'))
        return reference if name.endswith('_e64') else bank
    assert names
    component_banks = {n: component_bank(n) for n in names}
    infos = [read(component_banks[n] / n / 'info_2025.json') for n in names]
    assert [i['name'] for i in infos] == names
    for n, i in zip(names, infos):
        assert Path(i['native_model_path']).resolve().parent == (component_banks[n] / n).resolve()

    parent = A / 'optimization_20261003_r100'
    parent_curve = ROOT / 'candidates/extended_cohort_rank_calibration_20261006/cohort_curve.json'
    pins = {**read(native_parent.OUT / 'protocol.json')['input_sha256'],
        **pilot['input_sha256'], str(pilot_path): sha(pilot_path), str(parent_curve): sha(parent_curve)}
    pins.update({str(ROOT / relative): info['sha256'] for relative, info in frozen['files'].items()})
    pins[str(freeze / 'manifest.json')] = sha(freeze / 'manifest.json')
    predictor_source = (component_banks[cfg['model']] / cfg['model'] / 'flagged_oof_predictions.npy' if cfg['model'] not in pilot['ensembles']
        else pilot_folder / f'{cfg["model"]}.npy')
    pins[str(predictor_source)] = sha(predictor_source)
    for path in [bank / 'verification.json', reference / 'verification.json',
        robust / 'verification.json', A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',
        *[component_banks[n] / n / 'info_2025.json' for n in names]]:
        pins[str(path)] = sha(path)
    assert best['connected_final_score'] >= pilot['records'][1]['connected_final_score']

    OUT.mkdir()
    create(OUT / 'selected_parameters_before_final_mapping.json', {
        'selected_official_case': best, 'native_component_names': names,
        'selection_rule': 'Highest complete original official S; exact ties prefer lower weight then case',
        'selected_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'no_future_features_or_labels_read_for_selection': True, 'future_inference_not_started': True,
        'parent_cohort_curve_and_native_final_models_already_mature_and_saved': True})
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d'])
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        raw = np.load(parent / 'selected_validation.npy', mmap_mode='r')
        residual = np.load(predictor_source, mmap_mode='r')
        selected = transform(raw, dates, flags, residual, cfg['weight'])
        np.save(OUT / 'selected_validation.npy', selected)
        assert hashlib.sha256(memoryview(np.ascontiguousarray(selected)).cast('B')).hexdigest() == best['prediction_numeric_bytes_sha256']
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for filename in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(native_parent.OUT / 'scoring_validation_only' / filename, scoring / filename)
        context = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        assert score(context, selected) == best['metrics']
        capsule = read(Path(context.last_official_score_cache['official_metrics_source']))
        create(OUT / 'calibrated_csv_official.json', {'status': 'passed', 'metrics': best['metrics'],
            'csv_sha256': capsule['scope']['submission_csv_sha256'],
            'actual_selected_full5635800_row_native_ensemble_replay_equals_pilot': True,
            'actual_official_capsule': context.last_official_score_cache,
            'actual_mature_return_mapping': context.last_candidate_return_mapping, 'test_labels_read': False})
        cutoff = fold_cutoff(2025)
        parent_model = read(parent_curve)['model']
        assert parent_model['last_training_label_date'] < parent_model['exclusive_cutoff'] == cutoff
        labels = pd.read_csv(scoring / '测试集_Y.csv').sort_values(['trade_date', 'ts_code']).reset_index(drop=True)
        assert np.array_equal(labels.trade_date.to_numpy(), dates)
        y = labels.y_ret_1d.to_numpy(dtype=np.float64)
        history = (dates < cutoff) & np.isfinite(y)
        pct = daily_percentile(frame.select('trade_date').to_pandas(), selected)
        create(OUT / 'future_return_mapping.json', fit_mapping(pct[history], y[history]))
        create(OUT / 'causal_validation.json', {'status': 'passed',
            'actual_all50_causal_controls': str(pilot_path),
            'actual40_reference_native_and_independent_tree_controls': str(bank / 'verification.json'),
            'actual20_matched_L1_Huber_native_and_independent_tree_controls': str(robust / 'verification.json'),
            'actual19_fresh_native_fits_and1_preserved_reused_fit': read(robust / 'verification.json'),
            'actual_original64_reference_native_and_independent_controls': str(reference / 'verification.json'),
            'actual_selected_full_bits_match_original_official_pilot': True,
            'final_native_models_source': infos, 'exclusive_cutoff': cutoff,
            'final_return_mapping_rows': int(history.sum()), 'new_native_fits_by_qualification': 0,
            'parent_cohort_curve_reused_no_new_curve_fit': True, 'test_labels_read': False})
        graph = deepcopy(read(parent / 'selection.json')['winner']['extended_cohort_rank_calibration_scheme_graph'])
        graph['cohort_rank_calibration']['future_curve_model']['path'] = str(CANDIDATE / 'cohort_curve.json')
        components = [{'name': info['name'], 'path': str(CANDIDATE / f'{info["name"]}_model.txt'),
            'source_path': info['native_model_path'], 'sha256': info['native_model_sha256'],
            'independent_dump_path': str(CANDIDATE / f'{info["name"]}_dump.json'),
            'independent_dump_source_path': info['independent_tree_dump_path'],
            'independent_dump_sha256': info['independent_tree_dump_sha256'], 'training_info': info} for info in infos]
        graph['conditional_flag_residual'] = {**cfg, 'native_components': components,
            'ensemble_rule': 'declared component order sum then divide by component count',
            'position': 'after_complete_qualified_parent100_graph_and_saved_cohort_curve',
            'first2020_identity': True, 'parent95_daily_percentile_is_label_free_prediction_feature': True}
        winner = deepcopy(read(parent / 'selection.json')['winner'])
        winner.update(metrics=best['metrics'], connected_final_score=best['connected_final_score'])
        winner[GRAPH_FIELD] = graph
        protocol = deepcopy(read(native_parent.OUT / 'protocol.json'))
        protocol.update(status='frozen_selected_conditional_residual_candidate_before_future_inference',
            input_sha256=pins, explicit_parent_round=100, expected_scored_records=50,
            selected_conditional_configuration=cfg, native_component_names=names,
            new_native_fits_by_qualification=0, new_parent_curve_fits_by_qualification=0,
            current_parameter_authority=GRAPH_FIELD)
        create(OUT / 'protocol.json', protocol)
        pinned = {Path(path).relative_to(ROOT).as_posix(): digest for path, digest in pins.items() if Path(path).is_relative_to(ROOT)}
        pinned.update({p.relative_to(ROOT).as_posix(): sha(p) for p in (
            OUT / 'protocol.json', OUT / 'selected_validation.npy', OUT / 'future_return_mapping.json', ROOT / 'active_release.json')})
        selection = {'status': 'frozen_before_test_prediction', 'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'winner': winner, 'scored_records': 50, 'explicit_parent_round': 100,
            'baseline_score': pilot['records'][0]['connected_final_score'], 'score_gain': best['score_gain_over_parent100'],
            'selected74_anchor_score': pilot['records'][1]['connected_final_score'],
            'score_gain_over_selected74_anchor': best['connected_final_score'] - pilot['records'][1]['connected_final_score'],
            'selected_component_bank_paths': {n: str(component_banks[n]) for n in names},
            'current_parameter_authority': GRAPH_FIELD, 'chosen_postprocessor': cfg, 'native_component_names': names,
            'actual_official_pilot_source': str(pilot_path), 'frozen_sha256': pinned,
            'all_training_validation_years_previously_viewed': True, 'selection_bias_uncorrected': True, 'test_labels_read': False}
        create(OUT / 'selection.json', selection)
        create(OUT / 'frozen_before_actual_candidate_inference.json', {
            'input_sha256': pins, 'selection_sha256': sha(OUT / 'selection.json'),
            'parent_curve_sha256': sha(parent_curve), 'future_return_mapping_sha256': sha(OUT / 'future_return_mapping.json'),
            'source_snapshot_manifest_sha256': sha(freeze / 'manifest.json'),
            'selected_official_score': best['connected_final_score'],
            'frozen_at_local': selection['frozen_at_local'], 'test_labels_read': False})
        namespace = SimpleNamespace(**vars(native_parent))
        namespace.OUT, namespace.GRAPH_FIELD = OUT, GRAPH_FIELD
        from predict_robust_residual50_native_scheme_20261006 import predict
        candidate, storage = predict(namespace, selection, CANDIDATE, parent_curve, OUT / 'future_return_mapping.json')
        assert (candidate['rows'], candidate['days'], candidate['codes']) == (1599600, 344, 4650)
        assert candidate['model_reload_bit_identical'] and candidate['cold80_day_prefix_bit_identical']
        assert len(candidate['models']) == len(storage) == 13 + len(names)
        create(OUT / 'verification.json', {
            'status': 'passed_frozen_conditional_residual_full_saved_model_candidate_and_independent_decoder_and_cold80',
            'input_sha256': pins, 'candidate': str(CANDIDATE), 'csv_sha256': candidate['csv_sha256'],
            'rows': 1599600, 'days': 344, 'stocks': 4650, 'selected_configuration': cfg,
            'selected_official_score': best['connected_final_score'], 'score_gain_over_parent100': best['score_gain_over_parent100'],
            'actual_native_model_storage': storage, 'actual_saved_model_count': len(candidate['models']),
            'actual_model_reload_controls': candidate['actual_model_reload_controls'],
            'actual_cold80_model_controls': candidate['actual80_day_prefix_model_controls'],
            'actual_residual_native_independent_decoder': str(CANDIDATE / 'conditional_residual_native_replay_verification.json'),
            'new_native_fits_by_qualification': 0, 'new_parent_curve_fits_by_qualification': 0,
            'complete_source_manifest_full_ranking_and_main_qualification_pending': True, 'test_labels_read': False})


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_conditional_residual_candidate_inference',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
