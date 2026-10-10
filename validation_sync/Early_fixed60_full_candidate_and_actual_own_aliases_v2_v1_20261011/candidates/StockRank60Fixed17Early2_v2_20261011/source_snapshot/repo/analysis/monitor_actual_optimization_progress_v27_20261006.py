"""Observe actual GOSS models and the current owned queue in one complete public generation."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys
import uuid

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import monitor_actual_optimization_progress_v23_20261006 as previous
from complete_observer_snapshot_transaction_v2_20261006 import transaction
from run_dependency_queue_v3_20261006 import owned

original_update = previous.update


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def current_dependency():
    state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    for version in (6, 5, 4):
        path = A / f'service_owned_workflows_20261006/dependency_queue_v{version}/native_launch.json'
        if not path.exists():
            continue
        row = read(path)
        if row['owned_worker_pid'] == state['pid'] and owned(row):
            assert row['actual_native_console_handle'] == 0
            return path, row
    raise FileNotFoundError('Reobserve actual shared queue ownership; never infer a restart from this observation.')


def goss_snapshot():
    configs = read(A / 'gradient_sampling_complete_search_plan_20261005.json')['model_configurations']
    origins = {
        'capacity': A / 'gradient_sampling_memmap_capacity_v3_20261006',
        'complete_bank': A / 'gradient_sampling_memmap_complete_bank_v3_20261006',
        'canonical_bank': Path(read(A / 'gradient_sampling_storage_20261005.json')['output_directory'])}
    unique, records = {}, []
    for origin, folder in origins.items():
        for name, cfg in configs.items():
            for year in range(2020, 2026):
                info_path = folder / name / f'info_{year}.json'
                if not info_path.exists():
                    continue
                info = read(info_path)
                if info.get('status') not in ('passed', 'passed_actual_full_native_fit'):
                    continue
                assert info['configuration'] == cfg
                assert info.get('actual_native_boosting_iterations', info.get('actual_native_iterations')) == 300
                model = info_path.parent / f'model_{year}.joblib'
                assert sha(model) == info['model_sha256']
                label = 'rank' if cfg['target'] == 'y_rank' else 'return'
                meta = info['training_meta']
                assert meta == read(A / f'linear_bank_20261003/{label}_ridge_l01/info_{year}.json')['training_meta']
                assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
                if year < 2025:
                    assert info['new_model_fits'] == 1 and info['native_data_sample_strategy'] == 'goss'
                    assert info['model_reload_bit_identical'] and info['full_independent_codec_and_cold80_37day_bit_identical']
                    assert sha(info_path.parent / f'raw_{year}.parquet') == info['prediction_sha256']
                elif origin == 'capacity':
                    assert info['new_model_fits'] == 1 and info['native_parameters']['data_sample_strategy'] == 'goss'
                    assert read(info_path.parent / 'future_verification.json')['status'] == 'passed'
                else:
                    assert info['copied_file_is_not_an_additional_native_fit']
                item = {'model': name, 'year': year, 'origin': origin,
                    'model_sha256': info['model_sha256'], 'info_sha256': sha(info_path),
                    'source_info': str(info_path), 'actual_training_rows': meta['rows'],
                    'actual_native_iterations': 300, 'fit_seconds': info['fit_seconds']}
                key = name, year
                if key in unique:
                    assert unique[key]['model_sha256'] == item['model_sha256'], 'Conflicting copies cannot be counted as one fit.'
                else:
                    unique[key] = item
                records.append(item)
    annual = [row for row in unique.values() if row['year'] < 2025]
    final = [row for row in unique.values() if row['year'] == 2025]
    assert len(annual) <= 30 and len(final) <= 6
    stage = 'waiting_actual_native_model_evidence'
    resource_path = origins['complete_bank'] / 'actual_resource_samples.jsonl'
    resource = None
    if resource_path.exists():
        with resource_path.open('rb') as stream:
            stream.seek(max(0, resource_path.stat().st_size - 65536))
            lines = stream.read().decode('utf-8').splitlines()
        for line in reversed(lines):
            try:
                sample = json.loads(line)
                if sample.get('context', {}).get('stage'):
                    resource, stage = sample, sample['context']['stage']
                    break
            except json.JSONDecodeError:
                continue
    future = A / 'gradient_sampling_memmap_future_qa_v3_20261006/verification.json'
    promotion = A / 'gradient_sampling_memmap_native_promotion_20261006/verification.json'
    closed = future.exists() and read(future)['status'] == 'passed'
    exposed = promotion.exists() and read(promotion)['status'] == 'passed'
    if closed:
        assert len(annual) == 30 and len(final) == 6
        assert read(origins['complete_bank'] / 'oof_audit.json')['actual_annual_fits'] == 30
        stage = 'actual_full36_native_and_complete_future_verified_waiting_main_and_original_routes'
    if exposed:
        assert closed
        stage = 'actual_full36_native_and_complete_future_verified_main_published_original_routes_exposed'
    services = {}
    for name in ('gradient_sampling_memmap_complete_workflow_v3', 'gradient_sampling_memmap_complete_bank_v3_publication',
                 'gradient_sampling_native_queue_handoff_v6', 'gradient_sampling_native_queue_handoff_v6_publication'):
        folder = A / f'service_owned_workflows_20261006/{name}'
        row = read(folder / 'native_launch.json')
        live = owned(row)
        item = {'owned_live_now': live, 'pid': row['owned_worker_pid'], 'creation_time': row['owned_worker_creation_time'],
            'terminal_status': read(folder / 'service_execution.json')['status'] if (folder / 'service_execution.json').exists() else None}
        if live:
            process = psutil.Process(row['owned_worker_pid'])
            item.update(RSS_bytes=process.memory_info().rss, CPU_seconds=sum(process.cpu_times()[:2]))
        services[name] = item
    return {'gradient_sampling_actual_annual_fits': len(annual), 'gradient_sampling_actual_final_fits': len(final),
        'gradient_sampling_expected_annual_fits': 30, 'gradient_sampling_expected_final_fits': 6,
        'gradient_sampling_actual_unique_model_records': list(unique.values()),
        'gradient_sampling_duplicate_model_records_excluded': len(records) - len(unique),
        'gradient_sampling_fully_completed_five_year_configurations': sum(sum(r['model'] == name for r in annual) == 5 for name in configs),
        'gradient_sampling_full_native_stage': stage, 'gradient_sampling_latest_actual_resource_sample': resource,
        'gradient_sampling_complete_future_controls_passed': closed, 'gradient_sampling_original_routes_exposed': exposed,
        'gradient_sampling_actual_ownership': services, 'gradient_sampling_required_quality_rounds': [75, 76],
        'gradient_sampling_expected_full_quality_records': 262,
        'gradient_sampling_copies_and_small_control_fits_excluded_from_native_counts': True}


def seed_verified_cost_inventory(pending):
    # GOSS has a separate verified collector. Other native family changes still
    # trigger the original complete cost inventory producer.
    state_path = A / 'actual_optimization_monitor_state_20261005.json'
    prior = read(state_path)
    banks = [p for p in A.glob('*bank_*') if p.is_dir()]
    external = Path(read(A / 'memory_efficient_neural_storage_20261005.json')['output_directory'])
    if external not in banks:
        banks.append(external)
    inventory = sorted((str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p), p.stat().st_size, p.stat().st_mtime_ns)
        for bank in banks for p in bank.glob('*/info_*.json'))
    current = json.dumps(inventory, separators=(',', ':'))
    validated = prior.get('cost_inventory_key')
    if validated is None:
        return
    old = json.loads(validated)
    retained = lambda rows: [list(row) for row in rows if 'gradient_sampling' not in row[0].lower()]
    if retained(old) == retained(inventory):
        prior['cost_inventory_key'] = current
        prior['only_GOSS_artifact_changes_observed_independently_without_legacy_full_rescan'] = True
        pending[state_path] = prior


def update():
    with transaction() as (pending, commit):
        queue_path, queue = current_dependency()
        value_path = A / 'ongoing_optimization_state.json'
        initial = read(value_path)
        initial['dependency_queue_registry'] = queue_path.relative_to(ROOT).as_posix()
        pending[value_path] = initial
        seed_verified_cost_inventory(pending)
        state = original_update()
        value = pending[value_path]
        actual = goss_snapshot()
        cost = read(A / 'optimization_fit_cost_evidence_20261004.json')
        names = {r['model'] for r in actual['gradient_sampling_actual_unique_model_records']}
        cost_rows = [r for r in cost['models'] if r['model'] in names]
        counted_annual = sum(r['new_annual_fits'] for r in cost_rows)
        counted_final = sum(bool(r.get('fulltraining') and r['fulltraining'].get('status') == 'passed') for r in cost_rows)
        counted_five_year = sum(r['new_annual_fits'] == 5 for r in cost_rows)
        assert counted_annual <= actual['gradient_sampling_actual_annual_fits']
        assert counted_final <= actual['gradient_sampling_actual_final_fits']
        value['actual_new_annual_fits_completed'] += actual['gradient_sampling_actual_annual_fits'] - counted_annual
        value['fulltraining_artifacts_ready'] += actual['gradient_sampling_actual_final_fits'] - counted_final
        value['five_year_configuration_count'] += actual['gradient_sampling_fully_completed_five_year_configurations'] - counted_five_year
        value.update(actual, actual_progress_monitor=str(Path(__file__).relative_to(ROOT)), actual_observer_version=27,
            dependency_queue_registry=queue_path.relative_to(ROOT).as_posix(),
            actual_current_dependency_queue_identity=queue,
            actual_GOSS_additional_annual_fits_over_legacy_cost_inventory=actual['gradient_sampling_actual_annual_fits'] - counted_annual,
            actual_GOSS_additional_final_fits_over_legacy_cost_inventory=actual['gradient_sampling_actual_final_fits'] - counted_final,
            global_resource_exhaustion_established=False, updated_at_local=datetime.now().isoformat(timespec='seconds'))
        value['current_recovered_worker_ownership'].update(actual['gradient_sampling_actual_ownership'])
        pending[A / 'resume_optimization_20261004.json'] = dict(value)
        state.update(actual, actual_observer_version=27, dependency_queue_registry=value['dependency_queue_registry'],
            actual_new_annual_fits_completed=value['actual_new_annual_fits_completed'],
            fulltraining_artifacts_ready=value['fulltraining_artifacts_ready'],
            at_local=datetime.now().isoformat(timespec='seconds'))
        pending[A / 'actual_optimization_monitor_state_20261005.json'] = state
        generation = uuid.uuid4().hex
        commit(generation)
    print(json.dumps({'actual_observer_version': 27, 'complete_observer_generation': generation,
        'actual_active_quality_rounds': value['actual_active_quality_rounds'],
        'GOSS_actual_annual_fits': actual['gradient_sampling_actual_annual_fits'],
        'GOSS_actual_final_fits': actual['gradient_sampling_actual_final_fits'],
        'actual_current_dependency_pid': queue['owned_worker_pid']}), flush=True)
    return state


def main():
    previous.update = update
    previous.main()


if __name__ == '__main__':
    main()
