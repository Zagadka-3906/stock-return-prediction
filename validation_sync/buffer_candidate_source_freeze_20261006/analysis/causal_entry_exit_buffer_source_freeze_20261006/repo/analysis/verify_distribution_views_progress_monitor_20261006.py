"""Require an actual updated observer and unchanged owned scientific workers."""
from pathlib import Path
from datetime import datetime
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import owned
from handoff_distribution_views_progress_monitor_20261006 import visible_terminals, sha, create, read


def main():
    out = A / 'distribution_views_progress_handoff_20261006'
    assert not (out / 'verification.json').exists()
    frozen = read(out / 'frozen_before_handoff.json')
    assert not owned(frozen['old_ownership'])
    current = read(A / 'service_owned_workflows_20261006/progress_monitor_v23_recovery/native_launch.json')
    assert owned(current) and current['actual_native_console_handle'] == 0
    assert current['independent_launch_root_in_any_job'] is False
    state = read(A / 'actual_optimization_monitor_state_20261005.json')
    value = read(A / 'ongoing_optimization_state.json')
    assert state['actual_observer_version'] == 23
    assert value['actual_progress_monitor'].endswith('monitor_actual_optimization_progress_v23_20261006.py')
    assert value['quantile_distribution_views_virtual_annual_outputs'] == 30
    assert value['quantile_distribution_views_virtual_final_artifacts'] == 6
    assert value['quantile_distribution_views_new_native_fits'] == 0
    assert value['quantile_distribution_views_complete_native_codec_scope_passed']
    assert value['quantile_tree_actual_completed_annual_fits'] == 20
    assert value['quantile_tree_actual_completed_final_fits'] == 4
    assert value['virtual_composites_excluded_from_additional_native_fit_totals']
    assert all(n in value['pending_required_rounds'] for n in (91, 92, 93, 94))
    assert value['quantile_distribution_views_expected_full_official_records'] == 262
    assert value['quantile_tree_expected_full_official_records'] == 198
    assert value['actual_active_quality_rounds'] == [83]
    for row in frozen['unchanged_scientific_ownership'].values():
        assert owned(row)
    definition = read(A / 'service_owned_workflows_20261006/progress_monitor_v23_recovery/job_definition.json')
    for filename, digest in definition['input_sha256'].items():
        assert sha(filename) == digest
    visible = visible_terminals()
    create(out / 'verification.json', {
        'status': 'passed_actual_v23_update_and_scientific_workers_preserved',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'actual_owned_observer': current, 'unchanged_scientific_workers': frozen['unchanged_scientific_ownership'],
        'old_observer_closed': True, 'input_sha256': definition['input_sha256'],
        'actual_native_annual_final': [20, 4], 'actual_virtual_annual_final': [30, 6],
        'additional_native_fits_from_virtual_views': 0,
        'original198_and_additional262_official_quality_plans_preserved': True,
        'actual_active_quality_rounds': value['actual_active_quality_rounds'],
        'actual_partial_wave_records': value['active_wave_records'],
        'partial_scores_not_qualified_completion': True,
        'native_counter_snapshot': {key: value[key] for key in (
            'actual_new_annual_fits_completed', 'fulltraining_artifacts_ready')},
        'visible_terminal_windows': visible,
        'failed_observer_launch_preserved_and_recovered': True,
        'new_quality_scores_by_observer': 0, 'test_labels_read': False,
        'global_resource_exhaustion_established': False})
    create(out / 'actual_progress_snapshot.json', value)
    create(out / 'actual_observer_snapshot.json', state)
    print(json.dumps({'status': 'passed', 'visible_terminals': len(visible),
        'actual_active_quality_rounds': value['actual_active_quality_rounds'],
        'wave_records': value['active_wave_records']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
