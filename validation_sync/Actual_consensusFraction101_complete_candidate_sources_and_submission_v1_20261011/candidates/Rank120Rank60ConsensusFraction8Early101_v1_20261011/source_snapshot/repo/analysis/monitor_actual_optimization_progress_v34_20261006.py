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
    for version in (10, 9, 8, 7, 6, 5, 4):
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
                 'gradient_sampling_native_queue_handoff_v9', 'gradient_sampling_native_queue_handoff_v9_publication'):
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



def augment_ready_goss_ownership(value, state, queue, queue_state=None):
    qstate = read(A / 'service_owned_dependency_queue_v4_20261006/state.json') if queue_state is None else queue_state
    assert qstate['pid'] == queue['owned_worker_pid']
    active, identities = {}, {}
    for number in (95, 96, 97):
        name = f'round{number}'
        row = qstate['activated_jobs'].get(name)
        if row is None:
            continue
        live = owned(row)
        identities[name] = {'owned_live_now': live, 'pid': row['owned_worker_pid'],
                            'creation_time': row['owned_worker_creation_time']}
        if live:
            p = psutil.Process(row['owned_worker_pid'])
            identities[name].update(RSS_bytes=p.memory_info().rss, CPU_seconds=sum(p.cpu_times()[:2]))
            if number in value['pending_required_rounds']:
                active[number] = row
    value['current_recovered_worker_ownership'].update(identities)
    numbers = sorted(set(value.get('actual_active_quality_rounds', [])) | set(active))
    value['actual_active_quality_rounds'] = numbers
    if numbers and numbers[0] in active:
        number, row = numbers[0], active[numbers[0]]
        stage = read(A / f'ongoing_optimization_r{number}_state.json')
        waves, scores, workers = {}, [], []
        for path in (A / f'optimization_20261003_r{number}').glob('wave*_results.json'):
            payload = read(path)
            waves[path.stem] = len(payload['results'])
            scores.extend(r['connected_final_score'] for r in payload['results'].values())
        for p in psutil.Process(row['owned_worker_pid']).children(recursive=True):
            try:
                command = ' '.join(p.cmdline())
                if 'multiprocessing.spawn' in command and '--multiprocessing-fork' in command:
                    workers.append(p.pid)
            except psutil.Error:
                pass
        value.update(round=number, active_round=number, stage=stage['stage'], status=stage['status'],
            active_root_pid_live=True, active_root_command_owned=True,
            active_wave_records=waves, active_partial_score=max(scores, default=None),
            active_official_worker_pids=workers, active_official_workers=len(workers))
    value['queued_rounds'] = [n for n in value['pending_required_rounds'] if n not in numbers]
    self_path = A / 'service_owned_workflows_20261006/progress_monitor_v34/native_launch.json'
    if self_path.exists():
        identity = read(self_path)
        value['current_progress_monitor_identity'] = identity
        value['current_recovered_worker_ownership']['progress_monitor_v34'] = {
            'owned_live_now': owned(identity), 'pid': identity['owned_worker_pid'],
            'creation_time': identity['owned_worker_creation_time']}
    state.update(active_round=value['active_round'], active_stage=value['stage'], active_status=value['status'],
        active_root_command_owned=value.get('active_root_command_owned', False),
        active_root_pid_live=value.get('active_root_pid_live', False),
        active_wave_records=value['active_wave_records'], active_partial_score=value['active_partial_score'],
        actual_active_quality_rounds=numbers, current_recovered_worker_ownership=value['current_recovered_worker_ownership'],
        queued_rounds=value['queued_rounds'])

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
        value.update(actual, actual_progress_monitor=str(Path(__file__).relative_to(ROOT)), actual_observer_version=34,
            dependency_queue_registry=queue_path.relative_to(ROOT).as_posix(),
            actual_current_dependency_queue_identity=queue,
            actual_GOSS_additional_annual_fits_over_legacy_cost_inventory=actual['gradient_sampling_actual_annual_fits'] - counted_annual,
            actual_GOSS_additional_final_fits_over_legacy_cost_inventory=actual['gradient_sampling_actual_final_fits'] - counted_final,
            global_resource_exhaustion_established=False, updated_at_local=datetime.now().isoformat(timespec='seconds'))
        value['current_recovered_worker_ownership'].update(actual['gradient_sampling_actual_ownership'])
        import qualified_round_recovery_evidence_v3_20261006 as qualification
        joint_pending = qualification.complete_round_evidence(97) is None
        all_pending = sorted(set(value['pending_required_rounds']) | ({97} if joint_pending else set()))
        value.update(pending_required_rounds=all_pending,
            joint_membership_retention_expected_official_records=151,
            joint_membership_retention_pending_rounds=[97] if joint_pending else [],
            joint_membership_retention_new_native_fits=0)
        state.update(pending_required_rounds=all_pending,
            joint_membership_retention_expected_official_records=151,
            joint_membership_retention_pending_rounds=value['joint_membership_retention_pending_rounds'],
            joint_membership_retention_new_native_fits=0)
        augment_ready_goss_ownership(value, state, queue)
        pending[A / 'resume_optimization_20261004.json'] = dict(value)
        state.update(actual, actual_observer_version=34, dependency_queue_registry=value['dependency_queue_registry'],
            actual_new_annual_fits_completed=value['actual_new_annual_fits_completed'],
            fulltraining_artifacts_ready=value['fulltraining_artifacts_ready'],
            at_local=datetime.now().isoformat(timespec='seconds'))
        pending[A / 'actual_optimization_monitor_state_20261005.json'] = state
        generation = uuid.uuid4().hex
        commit(generation)
    print(json.dumps({'actual_observer_version': 34, 'complete_observer_generation': generation,
        'actual_active_quality_rounds': value['actual_active_quality_rounds'],
        'GOSS_actual_annual_fits': actual['gradient_sampling_actual_annual_fits'],
        'GOSS_actual_final_fits': actual['gradient_sampling_actual_final_fits'],
        'actual_current_dependency_pid': queue['owned_worker_pid']}), flush=True)
    return state



def with_actual_GOSS_cost_schema(function):
    def call():
        import refresh_gradient_sampling_cost_evidence_20261005 as legacy
        import refresh_gradient_sampling_cost_evidence_v2_20261006 as actual
        from atomic_optimization_observer_writes_20261005 import operational_writes
        old = legacy.main
        legacy.main = actual.main
        try:
            with operational_writes('refresh_gradient_sampling_cost_evidence_v2_20261006'):
                return function()
        finally:
            legacy.main = old
    return call


update = with_actual_GOSS_cost_schema(update)

def main():
    previous.update = update
    previous.main()


if __name__ == '__main__':
    main()
