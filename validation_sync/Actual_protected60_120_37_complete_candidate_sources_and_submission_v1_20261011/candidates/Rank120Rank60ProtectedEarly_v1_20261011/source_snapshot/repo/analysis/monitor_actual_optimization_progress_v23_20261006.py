"""Observe all six fixed views and262 additional records without counting new native fits."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import monitor_actual_optimization_progress_v22_20261006 as previous
from atomic_optimization_observer_writes_20261005 import write
from run_dependency_queue_v3_20261006 import owned

original_update = previous.update


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def update():
    state = original_update()
    value = read(A / 'ongoing_optimization_state.json')
    unchanged_native_counts = {key: value[key] for key in (
        'actual_new_annual_fits_completed', 'fulltraining_artifacts_ready')}
    import qualified_round_recovery_evidence_v3_20261006 as qualification
    pending = [number for number in (93, 94) if qualification.complete_round_evidence(number) is None]
    controls = {}
    for name in ('quantile_distribution_views_preflight', 'quantile_distribution_views_full_workflow',
                 'quantile_distribution_views_complete_publication', 'quantile_distribution_views_quality_queue'):
        path = A / f'service_owned_workflows_20261006/{name}/native_launch.json'
        row = read(path)
        item = {'pid': row['owned_worker_pid'], 'creation_time': row['owned_worker_creation_time'],
            'owned_live_now': owned(row)}
        terminal = path.parent / 'service_execution.json'
        item['terminal_status'] = read(terminal)['status'] if terminal.exists() else None
        if item['owned_live_now']:
            process = psutil.Process(row['owned_worker_pid'])
            item.update(RSS_bytes=process.memory_info().rss, CPU_seconds=sum(process.cpu_times()[:2]))
        controls[name] = item
    bank = A / 'quantile_distribution_views_bank_20261006'
    configs = read(A / 'quantile_distribution_views_complete_plan_20261006.json')['configurations']
    virtual, final = [], []
    for name, cfg in configs.items():
        for year in range(2020, 2026):
            path = bank / name / f'info_{year}.json'
            if not path.exists():
                continue
            info = read(path)
            if info['status'] != 'passed' or info['configuration'] != cfg:
                continue
            assert info['new_model_fits'] == 0 and info['virtual_artifact_not_new_native_fit']
            assert info['actual_reused_native_parents'] == 3
            model = path.parent / f'model_{year}.joblib'
            assert sha(model) == info['model_sha256']
            meta = info['training_meta']
            assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
            if year < 2025:
                assert info['actual_cold80_selfcontained_reload_bit_identical']
                assert info['actual_entire_annual_independent_pointwise_transform_bit_identical']
                assert sha(path.parent / f'raw_{year}.parquet') == info['prediction_sha256']
            item = {'model': name, 'year': year, 'saved_model_sha256': info['model_sha256'],
                'new_native_fits': 0, 'actual_native_parents_reused': 3}
            (virtual if year < 2025 else final).append(item)
    proof = bank / 'verification.json'
    closed = (controls['quantile_distribution_views_full_workflow']['terminal_status'] == 'passed'
        and not controls['quantile_distribution_views_full_workflow']['owned_live_now']
        and proof.exists() and read(proof)['status'] == 'passed')
    if closed:
        assert len(virtual) == 30 and len(final) == 6
        assert read(proof)['actual_new_native_fits'] == 0
    qstate = read(A / 'quantile_distribution_views_quality_queue_20261006/state.json')
    current = qstate.get('current_quality_job')
    if current and current['round'] in pending and owned(current):
        number = current['round']
        stage = read(A / f'ongoing_optimization_r{number}_state.json')
        waves, scores = {}, []
        for path in (A / f'optimization_20261003_r{number}').glob('wave*_results.json'):
            payload = read(path)
            waves[path.stem] = len(payload['results'])
            scores.extend(item['connected_final_score'] for item in payload['results'].values())
        value.update(round=number, active_round=number, stage=stage['stage'], status=stage['status'],
            active_wave_records=waves, active_partial_score=max(scores, default=None),
            actual_active_quality_rounds=[number], active_root_pid_live=True, active_root_command_owned=True)
    all_pending = sorted(set(value['pending_required_rounds']) | set(pending))
    value.update(actual_progress_monitor=str(Path(__file__).relative_to(ROOT)),
        pending_required_rounds=all_pending,
        quantile_distribution_views_virtual_annual_outputs=len(virtual),
        quantile_distribution_views_virtual_final_artifacts=len(final),
        quantile_distribution_views_new_native_fits=0,
        quantile_distribution_views_complete_native_codec_scope_passed=closed,
        quantile_distribution_views_actual_virtual_artifact_records=virtual + final,
        quantile_distribution_views_expected_virtual_annual_outputs=30,
        quantile_distribution_views_expected_virtual_final_artifacts=6,
        quantile_distribution_views_pending_quality_rounds=pending,
        quantile_distribution_views_expected_full_official_records=262,
        quantile_distribution_views_quality_stage=qstate['stage'],
        quantile_distribution_views_actual_ownership=controls,
        quantile_distribution_views_synthetic_generator_values_excluded_from_official_scores=True,
        all_previous198_quantile_records_preserved=True,
        virtual_composites_excluded_from_additional_native_fit_totals=True,
        global_resource_exhaustion_established=False,
        updated_at_local=datetime.now().isoformat(timespec='seconds'))
    assert {key: value[key] for key in unchanged_native_counts} == unchanged_native_counts
    value['queued_rounds'] = [number for number in all_pending if number not in value.get('actual_active_quality_rounds', [])]
    value['current_recovered_worker_ownership'].update(controls)
    for filename in ('ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
        write(A / filename, value)
    state.update(actual_observer_version=23, pending_required_rounds=all_pending,
        actual_active_quality_rounds=value.get('actual_active_quality_rounds', []),
        quantile_distribution_views_virtual_annual_outputs=len(virtual),
        quantile_distribution_views_virtual_final_artifacts=len(final),
        quantile_distribution_views_new_native_fits=0,
        quantile_distribution_views_closed_and_verified=closed,
        quantile_distribution_views_pending_quality_rounds=pending,
        quantile_distribution_views_actual_ownership=controls,
        at_local=datetime.now().isoformat(timespec='seconds'))
    write(A / 'actual_optimization_monitor_state_20261005.json', state)
    print(json.dumps({'actual_observer_version': 23, 'actual_virtual_annual_outputs': len(virtual),
        'actual_virtual_final_artifacts': len(final), 'additional_native_fits': 0,
        'pending_additional_quality_rounds': pending,
        'actual_active_quality_rounds': value.get('actual_active_quality_rounds', [])}), flush=True)
    return state


def main():
    previous.update = update
    previous.main()


if __name__ == '__main__':
    main()
