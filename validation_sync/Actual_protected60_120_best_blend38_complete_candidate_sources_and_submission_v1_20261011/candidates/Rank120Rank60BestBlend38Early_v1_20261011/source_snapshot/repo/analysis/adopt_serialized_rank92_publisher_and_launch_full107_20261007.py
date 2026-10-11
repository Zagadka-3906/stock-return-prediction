"""Transfer only an idle publisher; allow CPU92 and full107 QA to run independently."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import start_service, pair
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    out = A / 'rank92_main_writer_serialization_handoff_20261007'
    assert not out.exists()
    out.mkdir()
    proof = A / 'lowalpha50_round107_preparation_20261007.json'
    pins = {**read(proof)['input_sha256'], str(proof): sha(proof)}
    for p in (Path(__file__), A / 'publish_direct_rank92_scores_after_round107_20261007.py'):
        pins[str(p)] = sha(p)
    for path, digest in pins.items():
        assert sha(path) == digest, path
    old_folder = A / 'service_owned_workflows_20261006/single_host_rank92_scores_evidence_publication'
    old = read(old_folder / 'native_launch.json')
    assert owned(old) and not (old_folder / 'service_execution.json').exists()
    assert not (A / 'single_host_rank36_scores_github_20261007').exists()
    preserved = {n: read(A / f'service_owned_workflows_20261006/{n}/native_launch.json') for n in
        ('neural16384_annual', 'direct_flag_rank92_official_comparison',
         'quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue')}
    assert all(owned(r) for r in preserved.values())
    create(out / 'frozen_before_administrative_handoff.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'old_idle_publisher': old, 'scientific_workers_to_preserve': preserved,
        'new_writer_waits_actual107_service_terminal_after_main7_resume': True,
        'actual92_grid_and_official_science_unchanged': True, 'test_labels_read': False})
    parent, worker, boundary = suspended_idle(old, '    wait_closed (publish_single_host_rank36_evidence_20261007.py:24)')
    retired = False
    try:
        assert not worker.children()
        assert not (A / 'single_host_rank36_scores_github_20261007').exists()
        create(out / 'actual_old_publisher_idle_stack_before_and_after_hold.json', boundary)
        parent2, worker2 = pair(old)
        assert (parent.pid, worker.pid) == (parent2.pid, worker2.pid)
        worker.terminate()
        worker.wait(timeout=15)
        parent.terminate()
        parent.wait(timeout=15)
        retired = True
        create(old_folder / 'administrative_supersession_for_full107_20261007.json', {
            'status': 'administratively_retired_exact_idle_helper_not_scientifically_complete',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'identity': old,
            'reason': 'Transfer all unchanged92 main publication to a writer serialized behind full107; no score publication had started.',
            'actual_idle_stack_proof': str(out / 'actual_old_publisher_idle_stack_before_and_after_hold.json'),
            'scientific_workers_stopped_or_restarted': 0})
        publisher = start_service('single_host_rank92_scores_after_full107',
            'publish_direct_rank92_scores_after_round107_20261007.py', [], pins)
        registration = start_service('lowalpha50_round107_full_registration',
            'run_lowalpha50_round107_full_registration_20261007.py', [], pins)
        assert all(owned(r) for r in preserved.values())
        create(out / 'verification.json', {'status': 'passed_exact_idle_publisher_transferred_and_full107_started_all_scientists_preserved',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'actual_successor_publisher': publisher,
            'actual_full107_registration': registration, 'preserved_scientific_workers': preserved,
            'input_sha256': pins, 'old_helper_not_claimed_scientifically_complete': True,
            'new_quality_scores_by_handoff': 0, 'scientific_workers_stopped_or_restarted': 0, 'test_labels_read': False})
        print({'full107_pid': registration['owned_worker_pid'], 'serialized_scores92_publisher_pid': publisher['owned_worker_pid']}, flush=True)
    finally:
        if not retired:
            for process in (parent, worker):
                if process.is_running():
                    process.resume()


if __name__ == '__main__':
    main()
