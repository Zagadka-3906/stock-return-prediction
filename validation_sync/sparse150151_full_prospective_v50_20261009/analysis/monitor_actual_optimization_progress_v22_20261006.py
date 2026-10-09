"""Observe exact-memory native progress and preserved complete quality scope from owned handles."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import monitor_actual_optimization_progress_v20_20261006 as previous
from atomic_optimization_observer_writes_20261005 import write
from run_dependency_queue_v3_20261006 import owned

original_update = previous.update


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def update():
    base_state = original_update()
    value = read(A / 'ongoing_optimization_state.json')
    import qualified_round_recovery_evidence_v3_20261006 as qualification
    pending = []
    for number in (91, 92):
        if qualification.complete_round_evidence(number) is None:
            pending.append(number)
    controls = {}
    for name in ('quantile_tree_full_workflow', 'quantile_tree_quality_queue', 'main_publisher_v5', 'quantile_tree_memmap_capacity', 'quantile_tree_memmap_complete_workflow', 'quantile_tree_memmap_native_promotion', 'quantile_tree_quality_queue_v2'):
        path = A / f'service_owned_workflows_20261006/{name}/native_launch.json'
        if not path.exists():
            controls[name] = {'launch_not_yet_recorded': True}
            continue
        row = read(path)
        controls[name] = {'pid': row['owned_worker_pid'], 'creation_time': row['owned_worker_creation_time'],
                          'owned_live_now': owned(row)}
        if controls[name]['owned_live_now']:
            p = psutil.Process(row['owned_worker_pid'])
            controls[name].update(RSS_bytes=p.memory_info().rss, CPU_seconds=sum(p.cpu_times()[:2]))
    storage = read(A / 'quantile_tree_storage_20261006.json')
    bank = Path(storage['output_directory'])
    annual, final = [], []
    configs = read(A / 'quantile_tree_candidate_plan_20261006.json')['configurations']
    for name in configs:
        for year in range(2020, 2026):
            path = bank / name / f'info_{year}.json'
            if not path.exists():
                continue
            info = read(path)
            if info.get('status') != 'passed' or info.get('actual_native_boosting_iterations') != 300:
                continue
            model = path.parent / f'model_{year}.joblib'
            if not model.exists():
                continue
            with model.open('rb') as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != info['model_sha256']:
                    continue
            reference_name = 'rank_ridge_l01' if configs[name]['target'] == 'y_rank' else 'return_ridge_l01'
            reference = read(A / f'linear_bank_20261003/{reference_name}/info_{year}.json')['training_meta']
            if any(info['training_meta'][key] != reference[key] for key in (
                'rows', 'training_matrix_sha256', 'training_target_sha256',
                'training_keys_sha256', 'last_label_end', 'cutoff_exclusive', 'features')):
                continue
            (annual if year < 2025 else final).append({'model': name, 'year': year,
                'actual_training_rows': info['training_meta']['rows'], 'native_iterations': 300,
                'saved_model_sha256': info['model_sha256']})
    qstate_path = A / 'quantile_tree_quality_queue_v2_20261006/state.json'
    qstate = read(qstate_path) if qstate_path.exists() else {'stage': 'not_yet_launched'}
    native_state = read(A / 'quantile_tree_native_full_workflow_20261006/state.json')
    config_names = set(configs)
    observed_native = {}
    for origin, root in (('capacity', A / 'quantile_tree_memmap_capacity_20261006'),
                         ('complete_bank', A / 'quantile_tree_memmap_complete_bank_20261006')):
        records = []
        for name in config_names:
            for path in (root / name).glob('info_202*.json'):
                info = read(path)
                if info.get('status') not in ('passed', 'passed_actual_full_native_fit') or info.get('actual_native_boosting_iterations') != 300:
                    continue
                year = info['year']
                model = path.parent / f'model_{year}.joblib'
                if not model.exists():
                    continue
                with model.open('rb') as stream:
                    if hashlib.file_digest(stream, 'sha256').hexdigest() != info['model_sha256']:
                        continue
                reference_name = 'rank_ridge_l01' if configs[name]['target'] == 'y_rank' else 'return_ridge_l01'
                if info['training_meta'] != read(A / f'linear_bank_20261003/{reference_name}/info_{year}.json')['training_meta']:
                    continue
                records.append({'model': name, 'year': year, 'original_mature_rows': info['training_meta']['rows'],
                    'native_iterations': 300, 'saved_model_sha256': info['model_sha256'],
                    'is_source_copy_not_additional_native_fit': bool(info.get('copied_file_is_not_an_additional_native_fit'))})
        observed_native[origin] = records
    capacity_proof = A / 'quantile_tree_memmap_capacity_20261006/verification.json'
    future_proof = A / 'quantile_tree_memmap_future_qa_20261006/verification.json'
    promotion_proof = A / 'quantile_tree_memmap_native_promotion_20261006/verification.json'
    # The same final model can occur in capacity, bank and exposure directories.
    # Count unique model/year/bytes identities, never directory copies as fits.
    annual_by_key = {(row['model'], row['year']): row for row in annual}
    final_by_key = {(row['model'], row['year']): row for row in final}
    for row in observed_native['complete_bank'] + observed_native['capacity']:
        item = {'model': row['model'], 'year': row['year'], 'actual_training_rows': row['original_mature_rows'],
                'native_iterations': 300, 'saved_model_sha256': row['saved_model_sha256']}
        group = annual_by_key if row['year'] < 2025 else final_by_key
        key = row['model'], row['year']
        if key in group:
            assert group[key]['saved_model_sha256'] == row['saved_model_sha256']
        else:
            group[key] = item
    annual, final = list(annual_by_key.values()), list(final_by_key.values())
    if promotion_proof.exists() and read(promotion_proof)['status'] == 'passed':
        native_state = {'stage': 'actual_full24_native_and_complete_future_verified_and_exposed'}
    elif future_proof.exists() and read(future_proof)['status'] == 'passed':
        native_state = {'stage': 'actual_full24_native_and_complete_future_waiting_closure_main_and_exposure'}
    else:
        sample_path = A / ('quantile_tree_memmap_complete_bank_20261006/actual_resource_samples.jsonl'
            if (A / 'quantile_tree_memmap_complete_bank_20261006/protocol.json').exists()
            else 'quantile_tree_memmap_capacity_20261006/actual_resource_samples.jsonl')
        if sample_path.exists():
            with sample_path.open('rb') as stream:
                stream.seek(max(0, sample_path.stat().st_size - 65536))
                lines = stream.read().decode('utf-8').splitlines()
            for line in reversed(lines):
                try:
                    latest = json.loads(line)
                    native_state = {'stage': latest['context']['stage'], 'actual_resource_context': latest['context']}
                    break
                except (json.JSONDecodeError, KeyError):
                    continue
    value.update(quantile_tree_measured_capacity_native_models=observed_native['capacity'],
        quantile_tree_memmap_completed_annual_models=[row for row in observed_native['complete_bank'] if row['year'] < 2025],
        quantile_tree_memmap_completed_final_model_copies=[row for row in observed_native['complete_bank'] if row['year'] == 2025],
        quantile_tree_memmap_expected_annual_fits=20,
        quantile_tree_actual_capacity_completed_final_fits=len(observed_native['capacity']),
        quantile_tree_actual_memmap_completed_annual_fits=sum(row['year'] < 2025 for row in observed_native['complete_bank']),
        quantile_tree_complete_capacity_control_passed=capacity_proof.exists() and read(capacity_proof)['status'] == 'passed_actual_four_largest_full_native_fits_and_complete_future_controls',
        quantile_tree_complete_memmap_future_control_passed=future_proof.exists() and read(future_proof)['status'] == 'passed',
        quantile_tree_actual_native_artifact_promotion_passed=promotion_proof.exists() and read(promotion_proof)['status'] == 'passed',
        native_model_copies_excluded_from_new_fit_totals=True,
        current_complete_quantile_quality_queue=str(qstate_path.relative_to(ROOT)))
    current = qstate.get('current_quality_job')
    active = current and current['round'] in pending and owned(current)
    if active:
        number = current['round']
        stage = read(A / f'ongoing_optimization_r{number}_state.json')
        waves, scores = {}, []
        for path in (A / f'optimization_20261003_r{number}').glob('wave*_results.json'):
            payload = read(path)
            waves[path.stem] = len(payload['results'])
            scores.extend(row['connected_final_score'] for row in payload['results'].values())
        value.update(round=number, active_round=number, stage=stage['stage'], status=stage['status'],
            active_wave_records=waves, active_partial_score=max(scores, default=None),
            actual_active_quality_rounds=[number], active_root_pid_live=True, active_root_command_owned=True)
    all_pending = sorted(set(value.get('pending_required_rounds', base_state['pending_required_rounds'])) | set(pending))
    value.update(actual_progress_monitor=str(Path(__file__).relative_to(ROOT)),
        pending_required_rounds=all_pending,
        quantile_tree_full_native_stage=native_state['stage'], quantile_tree_quality_stage=qstate['stage'],
        quantile_tree_actual_completed_annual_fits=len(annual), quantile_tree_actual_completed_final_fits=len(final),
        quantile_tree_expected_annual_fits=20, quantile_tree_expected_final_fits=4,
        quantile_tree_pending_official_rounds=pending, quantile_tree_expected_full_official_records=198,
        quantile_tree_actual_model_fit_records=annual + final,
        quantile_tree_actual_native_and_quality_ownership=controls,
        quantile_tree_native_pilot_fits_excluded_from_full_model_counts=True,
        quantile_tree_generator_ordering_values_excluded_from_official_scores=True,
        global_resource_exhaustion_established=False,
        updated_at_local=datetime.now().isoformat(timespec='seconds'))
    value['actual_new_annual_fits_completed'] += len(annual)
    value['fulltraining_artifacts_ready'] += len(final)
    value['five_year_configuration_count'] += sum(
        sum(row['model'] == name for row in annual) == 5 for name in configs)
    value['queued_rounds'] = [n for n in all_pending if n not in value.get('actual_active_quality_rounds', [])]
    value['current_recovered_worker_ownership'].update(controls)
    for name in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
        write(A / name, value)
    base_state.update(actual_observer_version=22,
        pending_required_rounds=all_pending, actual_active_quality_rounds=value.get('actual_active_quality_rounds', []),
        quantile_tree_native_stage=native_state['stage'], quantile_tree_quality_stage=qstate['stage'],
        quantile_tree_actual_completed_annual_fits=len(annual), quantile_tree_actual_completed_final_fits=len(final),
        quantile_tree_actual_ownership=controls,
        quantile_tree_capacity_actual_final_fits=len(observed_native['capacity']),
        quantile_tree_memmap_actual_annual_fits=sum(row['year'] < 2025 for row in observed_native['complete_bank']),
        native_copies_excluded_from_new_fit_totals=True, at_local=datetime.now().isoformat(timespec='seconds'))
    write(A / 'actual_optimization_monitor_state_20261005.json', base_state)
    print(json.dumps({'actual_observer_version': 22, 'quantile_actual_full_annual_fits': len(annual),
        'quantile_actual_full_final_fits': len(final), 'quantile_pending_quality_rounds': pending,
        'actual_active_quality_rounds': value.get('actual_active_quality_rounds', [])}), flush=True)
    return base_state


def main():
    previous.update = update
    previous.main()


if __name__ == '__main__':
    main()
