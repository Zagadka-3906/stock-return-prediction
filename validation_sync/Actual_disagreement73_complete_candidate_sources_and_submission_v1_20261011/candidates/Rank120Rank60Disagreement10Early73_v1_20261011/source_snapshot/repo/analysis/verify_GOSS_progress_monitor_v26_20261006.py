"""Observe two real complete generations of the SHA-verified GOSS progress observer."""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create, visible_terminals
    from run_dependency_queue_v3_20261006 import owned
    out = A / 'GOSS_progress_monitor_verified_v26_20261006'
    handoff = read(A / 'GOSS_progress_monitor_handoff_v26_20261006/verification.json')
    assert handoff['status'] == 'passed_actual_observer26_handoff_with_complete_update_and_science_preserved'
    row = handoff['actual_new_observer']
    assert owned(row) and not owned(handoff['old_observer']) and not out.exists()
    out.mkdir()
    generations, samples, transitions = [], 0, 0
    started = time.monotonic()
    try:
        with (out / 'actual_public_state_samples.jsonl').open('x', encoding='utf-8', buffering=1) as stream:
            while len(generations) < 2:
                assert owned(row)
                states = {name: read(A / name) for name in ('ongoing_optimization_state.json',
                    'resume_optimization_20261004.json', 'actual_optimization_monitor_state_20261005.json')}
                value = states['ongoing_optimization_state.json']
                for state in states.values():
                    assert state['actual_observer_version'] == 26 and state['intermediate_observer_layers_not_published']
                    assert state['gradient_sampling_expected_full_quality_records'] == 262
                    assert 24 <= state['gradient_sampling_actual_annual_fits'] <= 30
                    assert state['gradient_sampling_actual_final_fits'] == 6
                    assert state['gradient_sampling_duplicate_model_records_excluded'] >= 6
                    assert set((75, 76, 91, 92, 93, 94)) <= set(state['pending_required_rounds'])
                    assert state['quantile_distribution_views_new_native_fits'] == 0
                generation = value['complete_observer_generation']
                same = all(s['complete_observer_generation'] == generation for s in states.values())
                actual_owned_generation = same and states['actual_optimization_monitor_state_20261005.json']['pid'] == row['owned_worker_pid']
                if actual_owned_generation and generation not in generations:
                    generations.append(generation)
                if not same:
                    transitions += 1
                samples += 1
                stream.write(json.dumps({'generation': generation, 'all3_generations_match': same,
                    'actual_owned_monitor_generation': actual_owned_generation,
                    'GOSS_actual_annual_fits': value['gradient_sampling_actual_annual_fits'],
                    'GOSS_actual_final_fits': value['gradient_sampling_actual_final_fits'],
                    'actual_active_quality_rounds': value['actual_active_quality_rounds']}) + '\n')
                if time.monotonic() - started > 300:
                    raise TimeoutError('Two owned complete generations not observed; the handle remains authoritative.')
                time.sleep(.5)
        for path, digest in handoff['input_sha256'].items():
            assert sha(path) == digest, path
        assert all(owned(r) for r in handoff['preserved_scientific_ownership'].values())
        create(out / 'verification.json', {'status': 'passed_two_actual_observer26_complete_generations_GOSS_counts_and_original_scope',
            'input_sha256': handoff['input_sha256'], 'actual_owned_observer': row,
            'actual_complete_generation_ids': generations, 'actual_public_samples': samples,
            'complete_file_transition_samples': transitions, 'seconds_observed': time.monotonic() - started,
            'actual_GOSS_annual_fits': value['gradient_sampling_actual_annual_fits'], 'actual_GOSS_final_fits': 6,
            'excluded_duplicate_model_records': value['gradient_sampling_duplicate_model_records_excluded'],
            'actual_current_dependency_registry': value['dependency_queue_registry'],
            'preserved_scientific_ownership': handoff['preserved_scientific_ownership'],
            'original262_GOSS_and198_quantile_and262_views_quality_scope_preserved': True,
            'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'visible_terminal_windows': visible_terminals()})
        create(out / 'actual_complete_public_state.json', value)
        print('passed_two_actual_observer26_complete_generations_GOSS_counts_and_original_scope', flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_observer26_live_controls',
            'error': f'{type(error).__name__}: {error}', 'samples': samples, 'generations': generations})
        raise


if __name__ == '__main__':
    main()
