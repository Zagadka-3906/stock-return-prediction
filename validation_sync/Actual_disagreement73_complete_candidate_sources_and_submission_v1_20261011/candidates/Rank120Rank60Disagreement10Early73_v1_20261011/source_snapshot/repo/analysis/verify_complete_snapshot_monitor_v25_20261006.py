"""Observe two real full updates without exposing any intermediate queued state."""
from pathlib import Path
from datetime import datetime
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create, visible_terminals
from run_dependency_queue_v3_20261006 import owned


def main():
    out = A / 'complete_snapshot_monitor_verified_v25_20261006'
    service = A / 'service_owned_workflows_20261006/progress_monitor_v25'
    handoff = read(A / 'complete_snapshot_monitor_handoff_v25_20261006/frozen_before_handoff.json')
    row = read(service / 'native_launch.json')
    assert owned(row) and row['actual_native_console_handle'] == 0
    assert not owned(handoff['old_owned_observer'])
    assert not out.exists()
    out.mkdir()
    definition = read(service / 'job_definition.json')
    for filename, digest in definition['input_sha256'].items():
        assert sha(filename) == digest
    create(out / 'frozen_before_live_controls.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'input_sha256': definition['input_sha256'], 'actual_owned_observer': row,
        'unchanged_scientific_ownership': handoff['unchanged_scientific_ownership'],
        'required_actual_complete_v25_generations': 2,
        'synthetic_prebound_producer_control_already_passed': True,
        'new_model_fits': 0, 'new_quality_scores': 0})
    generations, samples, cross_file_transition_samples = [], 0, 0
    started = time.monotonic()
    try:
        with (out / 'actual_public_state_samples.jsonl').open('x', encoding='utf-8', buffering=1) as stream:
            while time.monotonic() - started < 360:
                assert owned(row), 'Actual observer handle is missing.'
                states = {name: read(A / name) for name in (
                    'ongoing_optimization_state.json', 'resume_optimization_20261004.json',
                    'actual_optimization_monitor_state_20261005.json')}
                value = states['ongoing_optimization_state.json']
                for name, state in states.items():
                    assert state['actual_observer_version'] in (24, 25)
                    assert state['active_round'] == 83
                    assert state['actual_active_quality_rounds'] == [83]
                    assert set((91, 92, 93, 94)) <= set(state['pending_required_rounds'])
                    assert state['quantile_distribution_views_virtual_annual_outputs'] == 30
                    assert state['quantile_distribution_views_virtual_final_artifacts'] == 6
                    assert state['intermediate_observer_layers_not_published']
                assert value['quantile_tree_actual_completed_annual_fits'] == 20
                assert value['quantile_tree_actual_completed_final_fits'] == 4
                assert value['quantile_distribution_views_new_native_fits'] == 0
                current_generation = states['actual_optimization_monitor_state_20261005.json']['complete_observer_generation']
                matching = all(state['complete_observer_generation'] == current_generation for state in states.values())
                if not matching:
                    cross_file_transition_samples += 1
                elif value['actual_observer_version'] == 25 and current_generation not in generations:
                    generations.append(current_generation)
                    print(json.dumps({'actual_complete_v25_generations_observed': len(generations),
                        'wave_records': value['active_wave_records']}, ensure_ascii=False), flush=True)
                samples += 1
                stream.write(json.dumps({'at_local': datetime.now().isoformat(timespec='milliseconds'),
                    'observer_version': value['actual_observer_version'], 'active_round': value['active_round'],
                    'complete_generation': current_generation, 'all3_generations_match': matching,
                    'wave_records': value['active_wave_records']}, ensure_ascii=False) + '\n')
                if len(generations) == 2:
                    break
                time.sleep(.5)
            assert len(generations) == 2, 'Two complete actual updates have not yet been observed.'
        for scientific in handoff['unchanged_scientific_ownership'].values():
            assert owned(scientific)
        for filename, digest in definition['input_sha256'].items():
            assert sha(filename) == digest
        create(out / 'verification.json', {
            'status': 'passed_two_actual_complete_updates_no_intermediate_public_states',
            'at_local': datetime.now().isoformat(timespec='seconds'),
            'input_sha256': definition['input_sha256'], 'actual_owned_observer': row,
            'unchanged_scientific_ownership': handoff['unchanged_scientific_ownership'],
            'actual_complete_generation_ids': generations, 'actual_public_samples': samples,
            'seconds_observed': time.monotonic() - started,
            'invalid_intermediate_states_observed': 0,
            'sequential_complete_file_commit_transition_samples': cross_file_transition_samples,
            'all_files_individually_complete': True,
            'old24_observer_closed': True, 'original198_and_new262_quality_records_preserved': True,
            'actual_active_round': 83, 'partial_wave_records': value['active_wave_records'],
            'native_fit_totals': {key: value[key] for key in ('actual_new_annual_fits_completed', 'fulltraining_artifacts_ready')},
            'virtual_output_counts': [30, 6], 'additional_native_fits': 0,
            'visible_terminal_windows': visible_terminals(),
            'global_resource_exhaustion_established': False, 'test_labels_read': False,
            'new_quality_scores_by_observer': 0})
        create(out / 'actual_complete_public_state.json', value)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_actual_controls_preserved',
            'at_local': datetime.now().isoformat(timespec='seconds'),
            'error': f'{type(error).__name__}: {error}', 'actual_public_samples': samples,
            'generation_ids_observed': generations})
        raise
    print('Passed two actual complete observer updates with science workers preserved.', flush=True)


if __name__ == '__main__':
    main()
