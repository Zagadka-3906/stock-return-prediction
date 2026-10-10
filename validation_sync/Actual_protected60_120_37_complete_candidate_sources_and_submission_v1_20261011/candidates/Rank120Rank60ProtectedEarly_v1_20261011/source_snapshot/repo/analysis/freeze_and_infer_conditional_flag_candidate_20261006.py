"""Freeze the measured37-case winner and infer its real14 saved models."""
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
OUT = A / 'conditional_flag_rank_release_20261006'
CANDIDATE = ROOT / 'candidates/conditional_flag_rank_20261006'
GRAPH_FIELD = 'conditional_flag_rank_scheme_graph'


def main():
    import psutil
    assert psutil.virtual_memory().available >= 8.5 * 2**30
    assert not OUT.exists() and not CANDIDATE.exists()
    service = A / 'service_owned_workflows_20261006/conditional_flag_rank_official_comparison_v2'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'passed'
    freeze = A / 'conditional_flag_rank_source_freeze_20261006'
    frozen = read(freeze / 'manifest.json')
    assert frozen['status'] == 'passed_pre_inference_local_Python_source_snapshot'
    for relative, info in frozen['files'].items():
        assert sha(ROOT / relative) == sha(freeze / 'repo' / relative) == info['sha256']
    import numpy as np
    import pandas as pd
    import polars as pl
    import optimize_training_round95_v3 as native_parent
    import cohort_rank_calibration_20261006 as curve
    from conditional_flag_rank_transform_20261006 import transform
    from run import fold_cutoff
    from return_mapping import daily_percentile, fit_mapping
    from score_calibrated_candidates_20261003 import score
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    pilot_path = A / 'conditional_flag_rank_official_comparison_v2_20261006/verification.json'
    pilot = read(pilot_path)
    assert pilot['status'] == 'passed_actual37_conditional_flag_full_controls_and_original_official_scores'
    best = min(pilot['records'], key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    cfg = best['configuration']
    assert cfg['weight'] > 0 and best['score_gain_over_parent99'] > 0
    bank = A / 'conditional_flag_rank_bank_v2_20261006'
    final_info = read(bank / cfg['model'] / 'info_2025.json')
    parent = A / 'optimization_20261003_r99'
    pins = {**read(native_parent.OUT / 'protocol.json')['input_sha256'],
        **pilot['input_sha256'], str(pilot_path): sha(pilot_path)}
    pins.update({str(ROOT / relative): info['sha256'] for relative, info in frozen['files'].items()})
    pins[str(freeze / 'manifest.json')] = sha(freeze / 'manifest.json')
    parent_curve = ROOT / 'candidates/cohort_rank_calibration_20261006/cohort_curve.json'
    pins[str(parent_curve)] = sha(parent_curve)
    OUT.mkdir()
    create(OUT / 'selected_parameters_before_final_training.json', {
        'selected_official_case': best, 'selection_rule': 'Highest complete original official S; exact ties prefer lower weight',
        'selected_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'no_future_features_or_labels_read_for_selection': True, 'future_inference_not_started': True})
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d'])
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        raw = np.load(parent / 'selected_validation.npy', mmap_mode='r')
        control = A / 'conditional_flag_rank_official_comparison_v2_20261006'
        p = np.load(control / 'parent_percentile.npy', mmap_mode='r')
        target = np.load(A / 'cohort_rank_calibration_full_controls_20261006/historical_label_percentile.npy', mmap_mode='r')
        annual = read(control / 'annual_common_rank_curves.json')['annual_models']
        predictor = np.load(bank / cfg['model'] / 'flagged_oof_predictions.npy', mmap_mode='r')
        selected = transform(raw, dates, flags, predictor, annual, cfg['weight'], cfg['first_year_slope'], percentile=p)
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
            'actual_selected_full5635800_row_replay_equal_pilot': True,
            'actual_official_capsule': context.last_official_score_cache,
            'actual_mature_return_mapping': context.last_candidate_return_mapping, 'test_labels_read': False})
        cutoff = fold_cutoff(2025)
        final_curve = curve.fit(p, target, flags, dates, cutoff, 32, 0.)
        create(OUT / 'future_common_curve.json', {'model': final_curve,
            'selected_configuration': cfg, 'actual_final_pair_fits': 1,
            'only_global_curve_used': True, 'fitted_before_future_inference': True, 'test_labels_read': False})
        labels = pd.read_csv(scoring / '测试集_Y.csv').sort_values(['trade_date', 'ts_code']).reset_index(drop=True)
        assert np.array_equal(labels.trade_date.to_numpy(), dates)
        y = labels.y_ret_1d.to_numpy(dtype=np.float64)
        history = (dates < cutoff) & np.isfinite(y)
        pct = daily_percentile(frame.select('trade_date').to_pandas(), selected)
        create(OUT / 'future_return_mapping.json', fit_mapping(pct[history], y[history]))
        create(OUT / 'causal_validation.json', {'status': 'passed',
            'actual_all37_causal_controls': str(pilot_path),
            'actual18_native_bank_and_independent_tree_controls': str(bank / 'verification.json'),
            'actual_selected_full_bits_match_original_official_pilot': True,
            'final_training_last_label_date': final_curve['last_training_label_date'],
            'exclusive_cutoff': cutoff, 'final_return_mapping_rows': int(history.sum()),
            'new_native_model_fits_by_qualification': 0, 'test_labels_read': False})
        graph = deepcopy(read(parent / 'selection.json')['winner']['cohort_rank_calibration_scheme_graph'])
        graph['cohort_rank_calibration']['future_curve_model']['path'] = str(CANDIDATE / 'cohort_curve.json')
        graph['conditional_flag_rank'] = {**cfg, 'annual_common_curves_source': str(control / 'annual_common_rank_curves.json'),
            'native_model': {'path': str(CANDIDATE / 'specialist_model.txt'),
                'source_path': final_info['native_model_path'], 'sha256': final_info['native_model_sha256'],
                'independent_dump_path': str(CANDIDATE / 'specialist_model_dump.json'),
                'independent_dump_source_path': final_info['independent_tree_dump_path'],
                'independent_dump_sha256': final_info['independent_tree_dump_sha256'], 'training_info': final_info},
            'future_common_curve': {'path': str(CANDIDATE / 'conditional_common_curve.json'),
                'sha256': sha(OUT / 'future_common_curve.json')},
            'position': 'after_complete_qualified_parent99_graph_and_saved_cohort_curve'}
        winner = deepcopy(read(parent / 'selection.json')['winner'])
        winner.update(metrics=best['metrics'], connected_final_score=best['connected_final_score'])
        winner[GRAPH_FIELD] = graph
        protocol = deepcopy(read(native_parent.OUT / 'protocol.json'))
        protocol.update(status='frozen_selected_conditional_native_candidate_before_future_inference',
            input_sha256=pins, explicit_parent_round=99, expected_scored_records=37,
            selected_conditional_configuration=cfg, new_native_fits_by_qualification=0,
            actual_final_common_curve_pair_fits=1, current_parameter_authority=GRAPH_FIELD)
        create(OUT / 'protocol.json', protocol)
        pinned = {Path(path).relative_to(ROOT).as_posix(): digest for path, digest in pins.items() if Path(path).is_relative_to(ROOT)}
        pinned.update({p.relative_to(ROOT).as_posix(): sha(p) for p in (
            OUT / 'protocol.json', OUT / 'selected_validation.npy', OUT / 'future_common_curve.json',
            OUT / 'future_return_mapping.json', ROOT / 'active_release.json')})
        selection = {'status': 'frozen_before_test_prediction', 'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'winner': winner, 'scored_records': 37, 'explicit_parent_round': 99,
            'baseline_score': pilot['records'][0]['connected_final_score'], 'score_gain': best['score_gain_over_parent99'],
            'current_parameter_authority': GRAPH_FIELD, 'chosen_postprocessor': cfg,
            'actual_official_pilot_source': str(pilot_path), 'frozen_sha256': pinned,
            'all_training_validation_years_previously_viewed': True, 'selection_bias_uncorrected': True,
            'test_labels_read': False}
        create(OUT / 'selection.json', selection)
        create(OUT / 'frozen_before_actual_candidate_inference.json', {
            'input_sha256': pins, 'selection_sha256': sha(OUT / 'selection.json'),
            'future_common_curve_sha256': sha(OUT / 'future_common_curve.json'),
            'future_return_mapping_sha256': sha(OUT / 'future_return_mapping.json'),
            'source_snapshot_manifest_sha256': sha(freeze / 'manifest.json'),
            'selected_official_score': best['connected_final_score'],
            'frozen_at_local': selection['frozen_at_local'], 'test_labels_read': False})
        namespace = SimpleNamespace(**vars(native_parent))
        namespace.OUT, namespace.GRAPH_FIELD = OUT, GRAPH_FIELD
        from predict_conditional_flag_native_scheme_20261006 import predict
        candidate, storage = predict(namespace, selection, CANDIDATE, parent_curve,
            OUT / 'future_common_curve.json', OUT / 'future_return_mapping.json')
        assert (candidate['rows'], candidate['days'], candidate['codes']) == (1599600, 344, 4650)
        assert candidate['model_reload_bit_identical'] and candidate['cold80_day_prefix_bit_identical']
        assert len(candidate['models']) == len(storage) == 14
        create(OUT / 'verification.json', {
            'status': 'passed_frozen_conditional_native14_full_candidate_independent_decoder_and_cold80',
            'input_sha256': pins, 'candidate': str(CANDIDATE), 'csv_sha256': candidate['csv_sha256'],
            'rows': 1599600, 'days': 344, 'stocks': 4650, 'selected_configuration': cfg,
            'selected_official_score': best['connected_final_score'], 'score_gain_over_parent99': best['score_gain_over_parent99'],
            'actual_native_model_storage': storage, 'actual_model_reload_controls': candidate['actual_model_reload_controls'],
            'actual_cold80_model_controls': candidate['actual80_day_prefix_model_controls'],
            'actual_conditional_native_independent_decoder': str(CANDIDATE / 'conditional_native_replay_verification.json'),
            'new_native_model_fits_by_qualification': 0, 'actual_final_common_curve_pair_fits': 1,
            'complete_source_manifest_full_ranking_and_main_qualification_pending': True, 'test_labels_read': False})


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_conditional_native_candidate_inference',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
