"""Compare44 predeclared full-universe CPU HGB schemes using full continuous official scoring."""
from pathlib import Path
from types import SimpleNamespace
import gc
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
from atomic_optimization_observer_writes_20261005 import write

OUT = A / 'full_universe_HGB44_official_comparison_v2_20261007'
BANK = A / 'cpu_full_universe_HGB_bank24_20261007'


def numeric_sha(values):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()


def main():
    import psutil
    assert not OUT.exists()
    OUT.mkdir()
    service = A / 'service_owned_workflows_20261006/cpu_full_universe_HGB_native_bank24'
    identity = read(service / 'native_launch.json')
    while owned(identity):
        time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    completed = A / 'service_owned_workflows_20261006/direct_rank_micro74_round109_full_registration'
    while not (completed / 'native_launch.json').exists() or owned(read(completed / 'native_launch.json')):
        time.sleep(15)
    assert read(completed / 'service_execution.json')['status'] == 'passed'
    assert read(A / 'optimization_20261003_r109/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round109_receipt.json')['actual_full_QA_version'] == 20
    completed89 = A / 'service_owned_workflows_20261006/classifier_consensus_round89_status_recovery_main_publication'
    while not (completed89 / 'native_launch.json').exists() or owned(read(completed89 / 'native_launch.json')):
        time.sleep(15)
    assert read(completed89 / 'service_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round89_receipt.json')['actual_full_QA_version'] == 4
    completed111 = A / 'service_owned_workflows_20261006/CPU_HGB44_round112_full_registration'
    while not (completed111 / 'native_launch.json').exists() or owned(read(completed111 / 'native_launch.json')):
        time.sleep(15)
    assert read(completed111 / 'service_execution.json')['status'] == 'passed'
    assert read(A / 'optimization_20261003_r112/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round112_receipt.json')['actual_full_QA_version'] == 23
    bank = read(BANK / 'verification.json')
    assert bank['status'] == 'passed_actual24_full_universe_CPU_HGB_native_reloads_and_original256_new8192_independent_full_prefix_controls'
    assert len(bank['actual_models']) == bank['actual_native_fits'] == 24
    while True:
        state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
        live = {n: r for n, r in state['activated_jobs'].items() if n.startswith('round') and owned(r)}
        available = psutil.virtual_memory().available / 2**30
        write(OUT / 'waiting_status.json', {'status': 'waiting_for_local_RAM_and_no_original_official_writer',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'actual_live_original_rounds': list(live), 'available_RAM_GiB': available})
        if not live and available >= 9:
            break
        time.sleep(15)
    import numpy as np
    import polars as pl
    from full_universe_HGB_percentile_CDF_transform_20261007 import prepare, apply_prepared, transform, centered_daily_forecast
    from score_calibrated_candidates_20261003 import score
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    plan_path = A / 'cpu_full_universe_HGB_bank24_plan_20261007.json'
    plan = read(plan_path)
    names = list(bank['configurations'])
    assert names == list(plan['configurations']) and len(names) == 4
    ensembles = {'rank_pair': names[:2], 'return_pair': names[2:], 'all_four': names}
    universes=['all_current_raw_forecasts']
    amplitudes=plan['planned_official_comparison']['weights']
    cases = [{'anchor_round': 100, 'model': None, 'weight': 0., 'universe': None},
             {'anchor_round': 106, 'model': None, 'weight': 0., 'universe': None}]
    cases += [{'anchor_round': 106, 'model': name, 'weight': weight, 'universe': universe}
        for name in [*names, *ensembles] for universe in universes
        for weight in amplitudes]
    assert len(cases) == 44
    parents = {n: A / f'optimization_20261003_r{n}' for n in (100, 106)}
    sources = [Path(__file__), plan_path, A / 'full_universe_HGB_percentile_CDF_transform_20261007.py',
        BANK / 'verification.json', *BANK.glob('*/raw_oof_predictions.npy'),
        *BANK.glob('*/info_*.json'), *BANK.glob('*/model_*.joblib'), *BANK.glob('*/independent_hist_tree_state_*.json'),
        A / 'connected_validation_20261002/combined_fold_frame.parquet',
        A / 'score_calibrated_candidates_20261003.py', A / 'connected_validation_20261002/return_mapping.py',
        A / 'official_validation_csv_parse_cache_20261003.py',
        A / 'cross_round_official_score_reuse_20261003.py', ROOT / 'evaluate.py', ROOT / '后续选模标准.md',
        A / 'optimization_20261003_r95/scoring_validation_only/测试集_X.csv',
        A / 'optimization_20261003_r95/scoring_validation_only/测试集_Y.csv']
    for number, parent in parents.items():
        sources += [parent / 'selected_validation.npy', parent / 'selection.json',
            parent / 'calibrated_csv_official.json',
            A / f'github_validation_sync_main_20261005/round{number}_receipt.json']
    sources += [A / 'direct_flag_centered_rank_CDF_transform_20261007.py', A / 'cpu_conditional_residual_hgb_codec_20261007.py', A / 'cpu_numerical_HGB_large_batch_codec_v2_20261007.py', A / 'cpu_conditional_residual_mlp_codec_20261007.py', A / 'train_cpu_full_universe_HGB_bank24_20261007.py', A / 'cpu_full_universe_HGB_bank24_admission_20261007.json', A / 'cpu_full_universe_HGB63_codec_preflight_20261007/verification.json', A / 'github_validation_sync_main_20261005/round89_receipt.json', A / 'official_date_index_dataframe_adapter_20261007.py', A / 'official_date_index_speed_benchmark_20261007/verification.json', A / 'optimization_20261003_r109/full_registration_execution.json', A / 'github_validation_sync_main_20261005/round109_receipt.json']
    sources += [A / 'optimization_20261003_r112/full_registration_execution.json', A / 'github_validation_sync_main_20261005/round112_receipt.json']
    pins = {**bank['input_sha256'], **{str(p): sha(p) for p in sources}}
    baseline = {n: read(p / 'calibrated_csv_official.json')['metrics'] for n, p in parents.items()}
    create(OUT / 'frozen_before_actual_controls_and_official_scores.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'cases': cases, 'ensembles': ensembles, 'explicit_base_qualified_round': 106,
        'baseline_official_metrics': baseline, 'rows_days_stocks': [5635800, 1212, 4650],
        'all44_final_past_return_mapped_CSVs_original_official_scored': True,
        'current_price_valid_from_t_features_no_future_label_mask_for_CDF': True,
        'CDF_for_pool_values': 'average_rank/N; inverse knots1/N..1',
        'CDF_for_outside_price_valid_pool_values': 'insertion_index/N',
        'all_full_pool_raw_forecast_ranks_and_80_260_975_prefixes_required': True,
        'cached_CDF_must_equal_fresh_full_transform_for_each_head_and_universe': True,
        'all_weights_have_three_independently_reconstructed_CDF_prefixes': True,
        'actual_mature_native2020_fold_forecasts_required': True,
        'ordered_means_operate_on_each_head_same_day_centered_percentile_not_mixed_target_units': True,
        'no_extra_single_metric_worst_year_or_significance_elimination': True,
        'selection_rule': 'Highest complete original official S; exact ties prefer lower weight then case',
        'new_native_fits_by_comparison': 0, 'test_labels_read': False})
    records = []
    with LockedReadHashCache(pins):
        rank_dates=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['trade_date'])['trade_date'].to_numpy()
        raw_head_paths={n:BANK/n/'raw_oof_predictions.npy' for n in names}
        head_paths={}
        for name,path in raw_head_paths.items():
            raw_head=np.load(path,mmap_mode='r');values=centered_daily_forecast(raw_head,rank_dates)
            destination=OUT/f'{name}_centered_oof_predictions.npy';np.save(destination,values);head_paths[name]=destination
            create(OUT/f'{name}_normalization_verification.json',{'status':'passed_current_day_full_pool_forecast_average_rank_over_N_centered','raw_bank_source':str(path),'raw_bank_sha256':sha(path),'centered_forecast_sha256':sha(destination),'target_scale_not_mixed_with_other_head_targets':True,'test_labels_read':False})
            del values,raw_head
        for name,components in ensembles.items():
            values=np.zeros(5635800,dtype=np.float64)
            for component in components:values+=np.load(head_paths[component],mmap_mode='r')
            values/=len(components);path=OUT/f'{name}.npy';np.save(path,values);head_paths[name]=path
            create(OUT/f'{name}_verification.json',{'status':'passed_declared_ordered_equal_mean_of_centered_daily_forecasts','components':components,'prediction_array_sha256':sha(path),'new_native_fits':0,'test_labels_read':False});del values
        frame = pl.read_parquet(A / 'connected_validation_20261002/combined_fold_frame.parquet',
            columns=['ts_code', 'trade_date', 'flag_limit_up', 'price_valid', 'y_ret_1d'])
        dates, flags, valid = (frame[c].to_numpy() for c in ('trade_date', 'flag_limit_up', 'price_valid'))
        assert len(frame) == 5635800 and frame['trade_date'].n_unique() == 1212
        raw = np.load(parents[106] / 'selected_validation.npy', mmap_mode='r')
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir()
        for filename in ('测试集_X.csv', '测试集_Y.csv'):
            os.link(A / 'optimization_20261003_r95/scoring_validation_only' / filename, scoring / filename)
        ctx = SimpleNamespace(frame=frame, dates=dates, scoring=scoring)
        days, starts = np.unique(dates, return_index=True)
        ends = np.r_[starts[1:], len(dates)]
        prepared = {universe: prepare(raw, dates, flags, valid, universe)
            for universe in universes}
        checked_heads=set()
        for name,components in {**{n:[n] for n in names},**ensembles}.items():
            full=np.load(head_paths[name],mmap_mode='r')
            for count in (80,260,975):
                n=int(ends[count-1]);cold=np.zeros(n,dtype=np.float64)
                for component in components:
                    source=np.load(raw_head_paths[component],mmap_mode='r')
                    cold+=centered_daily_forecast(source[:n],dates[:n])
                cold/=len(components)
                assert np.array_equal(cold.view('u8'),np.asarray(full[:n]).view('u8'))
            create(OUT/f'{name}_daily_rank_prefix_controls.json',{'status':'passed_actual_independent_daily_rank_and_ordered_mean80_260_975_prefix_bits','components':components,'days':[80,260,975],'test_labels_read':False})
        for index, cfg in enumerate(cases):
            if cfg['model'] is None:
                values = np.asarray(np.load(parents[cfg['anchor_round']] / 'selected_validation.npy', mmap_mode='r'))
                prefix_passed = False
                all_nonflag = False
            else:
                prediction = np.load(head_paths[cfg['model']], mmap_mode='r')
                values = apply_prepared(raw, prediction, cfg['weight'], prepared[cfg['universe']])
                if (cfg['model'], cfg['universe']) not in checked_heads:
                    independent_full = transform(raw, dates, flags, valid, prediction, cfg['weight'], cfg['universe'])
                    assert np.array_equal(independent_full.view(np.uint64), values.view(np.uint64))
                    checked_heads.add((cfg['model'], cfg['universe']))
                    del independent_full
                # Same-day arrays used by subsequent weights are immutable;
                # replay controls still run independently for every case.
                for count in (80, 260, 975):
                    n = int(ends[count-1])
                    cold = transform(raw[:n], dates[:n], flags[:n], valid[:n],
                        prediction[:n], cfg['weight'], cfg['universe'])
                    assert np.array_equal(cold.view(np.uint64), values[:n].view(np.uint64))
                    del cold
                prefix_passed=True
                all_nonflag=False
            write(OUT / 'actual_stage.json', {'status': 'actual_complete_official_scoring',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'case': index,
                'configuration': cfg, 'actual_completed_cases': len(records), 'expected_cases': 44})
            from official_date_index_dataframe_adapter_20261007 import installed
            with installed(scoring / 'submission.csv') as actual_date_index:
                metrics = score(ctx, values)
            assert actual_date_index['date_index_lookups'] in (0, 1212)
            if cfg['model'] is None:
                assert metrics == baseline[cfg['anchor_round']], 'Qualified anchor must reproduce all original metrics'
            capsule = Path(ctx.last_official_score_cache['official_metrics_source'])
            item = {'case': index, 'configuration': cfg, 'metrics': metrics,
                'connected_final_score': metrics['final_score'],
                'score_gain_over_best106': metrics['final_score'] - baseline[106]['final_score'],
                'prediction_numeric_bytes_sha256': numeric_sha(values),
                'official_date_index_runtime': dict(actual_date_index), 'official_score_cache': ctx.last_official_score_cache, 'official_metric_capsule_sha256': sha(capsule),
                'actual_return_mapping': ctx.last_candidate_return_mapping,
                'full_pool_transformation_including_nonflag_and2020_actual_native_forecasts': cfg['model'] is not None,
                'actual_cold80_260_975_bits_exact': prefix_passed,
                'actual2020_native_fold_used_in_nonanchor_scheme': cfg['model'] is not None,
                'qualified_anchor_all_metrics_exact': cfg['model'] is None,
                'native_bank_source': str(BANK / 'verification.json'),
                'ensemble_components': ensembles.get(cfg['model']), 'test_labels_read': False,
                'full_frozen_candidate_and_complete_ranking_still_required': True}
            create(OUT / f'case{index:02d}_official.json', item)
            records.append(item)
            print({'case': index, 'official_score': metrics['final_score'],
                'gain_over_best106': item['score_gain_over_best106']}, flush=True)
            del values
            if cfg['model']:
                del prediction
            gc.collect()
        for path, digest in pins.items():
            assert sha(Path(path)) == digest, path
    best = min(records, key=lambda r: (-r['connected_final_score'], r['configuration']['weight'], r['case']))
    create(OUT / 'verification.json', {'status': 'passed_actual44_full_universe_CPU_HGB_CDF_full_official_comparisons',
        'input_sha256': pins, 'records': records, 'best': best, 'ensembles': ensembles,
        'existing_native_bank_fits': 24, 'new_native_fits_by_comparison': 0,
        'new_quality_score_records': 44, 'actual_cached_CDF_full_replay_heads': len(checked_heads),
        'all42_nonanchor_cases_have_actual_three_cold_prefix_controls': True,
        'test_labels_read': False, 'full_candidate_and_complete_ranking_and_main_publication_pending': True,
        'global_feasible_direction_or_resource_boundary_not_established': True})


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_local_conditional_residual_hgb44_comparison',
                'error': f'{type(error).__name__}: {error}', 'test_labels_read': False})
        raise
