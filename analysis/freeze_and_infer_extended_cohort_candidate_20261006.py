"""Freeze the measured cohort winner, fit mature final curves, and replay saved models."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[key] = '4'
from run_dependency_queue_v3_20261006 import read, create, sha, owned

OUT = A / 'extended_cohort_rank_calibration_release_20261006'
CANDIDATE = ROOT / 'candidates/extended_cohort_rank_calibration_20261006'
GRAPH_FIELD = 'extended_cohort_rank_calibration_scheme_graph'


def main():
    import psutil
    assert psutil.virtual_memory().available >= 8 * 2**30
    assert not OUT.exists() and not CANDIDATE.exists()
    service = A / 'service_owned_workflows_20261006/extended_cohort_controls_and_scores'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'passed'
    source_freeze = A / 'extended_cohort_rank_calibration_source_freeze_20261006'
    frozen = read(source_freeze / 'manifest.json')
    assert frozen['status'] == 'passed_pre_inference_local_Python_source_snapshot'
    for relative, info in frozen['files'].items():
        assert sha(ROOT / relative) == sha(source_freeze / 'repo' / relative) == info['sha256']
    import numpy as np
    import pandas as pd
    import polars as pl
    import optimize_training_round95_v3 as parent
    import cohort_rank_calibration_v2_20261006 as method
    from run import fold_cutoff
    from return_mapping import daily_percentile, fit_mapping
    from score_calibrated_candidates_20261003 import score
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    pilot_path = A / 'extended_cohort_rank_calibration_official_pilot_20261006/verification.json'
    pilot = read(pilot_path)
    assert pilot['status'] == 'completed_actual66_cohort_original_official_scores_full_qualification_pending'
    best = min(pilot['records'], key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    cfg = best['configuration']
    current = read(A / 'cohort_rank_calibration_release_20261006/verification.json')['selected_official_score']
    assert best['connected_final_score'] >= current
    assert read(A / 'github_validation_sync_main_20261005/round99_receipt.json')['actual_full_QA_version'] == 10
    assert cfg['weight'] > 0. and best['score_gain_over_parent'] > 0.
    pins = {**read(parent.OUT / 'protocol.json')['input_sha256'], **pilot['input_sha256'], str(pilot_path): sha(pilot_path)}
    pins.update({str(ROOT / relative): info['sha256'] for relative, info in frozen['files'].items()})
    pins[str(source_freeze / 'manifest.json')] = sha(source_freeze / 'manifest.json')
    OUT.mkdir()
    scratch = ROOT / 'tmp/cohort_rank_calibration_candidate_20261006'
    scratch.mkdir(exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    create(OUT / 'selected_parameters_before_final_training.json', {
        'selected_official_case': best, 'selection_rule': 'Highest complete original official S; exact ties prefer zero weight',
        'selected_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'no_future_features_or_labels_read_for_selection': True,
        'input_sha256': pins, 'future_inference_not_started': True})
    with LockedReadHashCache(pins):
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d'])
        dates, flags = frame['trade_date'].to_numpy(), frame['flag_limit_up'].to_numpy()
        raw = np.load(parent.OUT / 'selected_validation.npy', mmap_mode='r')
        control = A / 'extended_cohort_rank_calibration_full_controls_20261006'
        p = np.load(control / 'parent_percentile.npy', mmap_mode='r')
        target = np.load(control / 'historical_label_percentile.npy', mmap_mode='r')
        annual = read(Path(best['annual_model_source']))['annual_models']
        selected = method.transform(raw, dates, flags, annual, cfg['weight'], percentile=p)
        np.save(OUT / 'selected_validation.npy', selected)
        import hashlib
        assert hashlib.sha256(memoryview(np.ascontiguousarray(selected)).cast('B')).hexdigest() == best['prediction_numeric_bytes_sha256']
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for filename in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(parent.OUT / 'scoring_validation_only' / filename, scoring / filename)
        ctx = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        assert score(ctx, selected) == best['metrics']
        capsule = read(Path(ctx.last_official_score_cache['official_metrics_source']))
        create(OUT / 'calibrated_csv_official.json', {'status': 'passed', 'metrics': best['metrics'],
            'csv_sha256': capsule['scope']['submission_csv_sha256'],
            'actual_selected_curve_reload_full5635800_row_replay_exact': True,
            'actual_official_capsule': ctx.last_official_score_cache,
            'actual_mature_return_mapping': ctx.last_candidate_return_mapping, 'test_labels_read': False})
        cutoff = fold_cutoff(2025)
        future_model = method.fit(p, target, flags, dates, cutoff, cfg['bins'], cfg['pseudocount'])
        create(OUT / 'future_cohort_curve.json', {'model': future_model,
            'selected_configuration': cfg, 'paired_monotone_curves_fitted': 2,
            'actual_final_postprocessor_fits': 1, 'new_native_base_model_fits': 0,
            'fitted_before_any_future_inference': True, 'test_labels_read': False})
        # The final return map uses original float64 training aliases and only mature rows.
        labels = pd.read_csv(scoring / '测试集_Y.csv').sort_values(['trade_date', 'ts_code']).reset_index(drop=True)
        assert np.array_equal(labels.trade_date.to_numpy(), dates)
        y = labels.y_ret_1d.to_numpy(dtype=np.float64)
        pct = daily_percentile(frame.select('trade_date').to_pandas(), selected)
        history = (dates < cutoff) & np.isfinite(y)
        mapping = fit_mapping(pct[history], y[history])
        create(OUT / 'future_return_mapping.json', mapping)
        create(OUT / 'causal_validation.json', {'status': 'passed',
            'annual_curve_models_source': best['annual_model_source'],
            'actual_full17_causal_controls': str(control / 'verification.json'),
            'actual_selected_full_bits_match_official_pilot': True,
            'final_training_last_label_date': future_model['last_training_label_date'],
            'exclusive_cutoff': cutoff, 'final_return_mapping_rows': int(history.sum()),
            'no_test_labels_used_for_curves_or_mapping': True, 'test_labels_read': False})
        graph = deepcopy(read(parent.OUT / 'selection.json')['winner'][parent.GRAPH_FIELD])
        graph['cohort_rank_calibration'] = {**cfg,
            'annual_models_source': best['annual_model_source'],
            'future_curve_model': {'path': str(CANDIDATE / 'cohort_curve.json'),
                'sha256': sha(OUT / 'future_cohort_curve.json'),
                'last_training_label_date': future_model['last_training_label_date'], 'exclusive_cutoff': cutoff},
            'position': 'after_complete_parent95_graph_including_temporal_transform'}
        winner = deepcopy(read(parent.OUT / 'selection.json')['winner'])
        winner.update(metrics=best['metrics'], connected_final_score=best['connected_final_score'])
        winner[GRAPH_FIELD] = graph
        protocol = deepcopy(read(parent.OUT / 'protocol.json'))
        protocol.update(status='frozen_selected_cohort_candidate_before_future_inference',
            input_sha256=pins, explicit_parent_round=95, expected_scored_records=66,
            selected_cohort_configuration=cfg, new_native_base_model_fits=0,
            actual_final_cohort_calibration_pair_fits=1, current_parameter_authority=GRAPH_FIELD)
        create(OUT / 'protocol.json', protocol)
        pinned = {Path(path).relative_to(ROOT).as_posix(): digest for path, digest in pins.items() if Path(path).is_relative_to(ROOT)}
        pinned.update({p.relative_to(ROOT).as_posix(): sha(p) for p in (
            OUT / 'protocol.json', OUT / 'selected_validation.npy', OUT / 'future_cohort_curve.json',
            OUT / 'future_return_mapping.json', ROOT / 'active_release.json')})
        selection = {'status': 'frozen_before_test_prediction',
            'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'winner': winner,
            'scored_records': 66, 'explicit_parent_round': 95,
            'baseline_score': pilot['records'][0]['connected_final_score'], 'score_gain': best['score_gain_over_parent'],
            'current_parameter_authority': GRAPH_FIELD, 'chosen_postprocessor': cfg,
            'actual_official_pilot_source': str(pilot_path), 'frozen_sha256': pinned,
            'all_training_validation_years_previously_viewed': True, 'selection_bias_uncorrected': True,
            'test_labels_read': False}
        create(OUT / 'selection.json', selection)
        create(OUT / 'frozen_before_actual_candidate_inference.json', {
            'input_sha256': pins, 'selection_sha256': sha(OUT / 'selection.json'),
            'future_curve_model_sha256': sha(OUT / 'future_cohort_curve.json'),
            'future_return_mapping_sha256': sha(OUT / 'future_return_mapping.json'),
            'source_snapshot_manifest_sha256': sha(source_freeze / 'manifest.json'),
            'selected_official_score': best['connected_final_score'],
            'frozen_at_local': selection['frozen_at_local'], 'test_labels_read': False})
        namespace = SimpleNamespace(**vars(parent))
        namespace.OUT, namespace.GRAPH_FIELD = OUT, GRAPH_FIELD
        from predict_cohort_calibrated_scheme_20261006 import predict
        candidate, storage = predict(namespace, selection, CANDIDATE,
            OUT / 'future_cohort_curve.json', OUT / 'future_return_mapping.json')
        assert (candidate['rows'], candidate['days'], candidate['codes']) == (1599600, 344, 4650)
        assert candidate['model_reload_bit_identical'] and candidate['cold80_day_prefix_bit_identical']
        create(OUT / 'verification.json', {'status': 'passed_frozen_cohort_full_native_candidate_curve_codec_replay_and_cold80',
            'input_sha256': pins, 'candidate': str(CANDIDATE), 'csv_sha256': candidate['csv_sha256'],
            'rows': 1599600, 'days': 344, 'stocks': 4650,
            'selected_configuration': cfg, 'selected_official_score': best['connected_final_score'],
            'score_gain': best['score_gain_over_parent'], 'score_gain_over_qualified_round99': best['connected_final_score'] - current, 'actual_native_model_storage': storage,
            'actual_model_reload_controls': candidate['actual_model_reload_controls'],
            'actual_cold80_model_controls': candidate['actual80_day_prefix_model_controls'],
            'actual_postprocessor_curve_reload_and_independent_decoder': str(CANDIDATE / 'cohort_curve_replay_verification.json'),
            'new_native_base_model_fits': 0, 'actual_final_cohort_calibration_pair_fits': 1,
            'complete_source_manifest_full_ranking_and_main_qualification_pending': True,
            'test_labels_read': False})


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_frozen_cohort_candidate_inference',
                'error': f'{type(exc).__name__}: {exc}', 'test_labels_read': False})
        raise
