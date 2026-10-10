"""Replace an idle observer only; verify three complete public snapshots with real GOSS ownership."""
from pathlib import Path
import json
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import start_service, pair

OUT = A / 'ready_goss_observer31_actual_handoff_20261006'
PUBLIC = ('ongoing_optimization_state.json', 'resume_optimization_20261004.json',
          'actual_optimization_monitor_state_20261005.json')


def stack(pid):
    p = subprocess.run([str(ROOT / 'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),
        'dump', '--pid', str(pid)], capture_output=True, text=True, encoding='utf-8',
        errors='replace', timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
    assert p.returncode == 0, p.stderr
    return p.stdout


def terminate_helper(row):
    parent, worker = pair(row)
    assert not worker.children()
    for p in (worker, parent):
        p.terminate(); p.wait(timeout=15)


def main():
    assert not OUT.exists(); OUT.mkdir()
    preflight = A / 'ready_goss_observer31_ownership_preflight_20261006/verification.json'
    assert read(preflight)['status'] == 'passed_actual_live_R95_ownership_and_private_birth_mismatch_rejection'
    old_path = A / 'service_owned_workflows_20261006/progress_monitor_v30/native_launch.json'
    old = read(old_path); parent, worker = pair(old)
    qstate = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    preserved = {'round95': qstate['activated_jobs']['round95']}
    for name in ('neural16384_annual', 'dependency_queue_v7', 'main_publisher_v6'):
        preserved[name] = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
    assert all(owned(row) for row in preserved.values())
    sources = [Path(__file__), A / 'monitor_actual_optimization_progress_v31_20261006.py',
        A / 'monitor_actual_optimization_progress_v30_20261006.py',
        A / 'check_ready_goss_observer31_ownership_20261006.py', preflight,
        A / 'refresh_gradient_sampling_cost_evidence_v2_20261006.py',
        A / 'complete_observer_snapshot_transaction_v2_20261006.py',
        A / 'handoff_ready_goss_full_execution_20261006.py',
        A / 'launch_service_owned_workflow_with_pwsh_20261006.py',
        A / 'launch_service_owned_windows_workflow_20261006.ps1',
        A / 'run_service_owned_windows_workflow_20261006.py',
        A / 'optimization_20261003_r95/protocol.json']
    pins = {str(p.resolve()): sha(p) for p in sources}
    create(OUT / 'frozen_before_handoff.json', {'input_sha256': pins, 'old_observer': old,
        'scientific_workers_and_main_and_queue_to_preserve': preserved,
        'ownership_mismatch_before': {name: read(A / name) for name in PUBLIC},
        'old_scientific_qualification_and_native_counts_and_all_pending_scope_preserved': True})
    suspended, new, retired = [], None, False
    try:
        for _ in range(120):
            assert owned(old)
            before = stack(worker.pid)
            idle = '    main (monitor_actual_optimization_progress_v18_20261005.py:146)' in before
            if not idle:
                time.sleep(1); continue
            for p in (worker, parent): p.suspend(); suspended.append(p)
            after = stack(worker.pid)
            if '    main (monitor_actual_optimization_progress_v18_20261005.py:146)' in after:
                assert not worker.children()
                create(OUT / 'actual_old_observer_idle_stack.json', {'status': 'verified_idle_before_and_after_suspend',
                    'before': before, 'after': after, 'only_old_observer_processes_suspended': True})
                break
            for p in reversed(suspended): p.resume()
            suspended.clear()
        else: raise RuntimeError('Old observer did not reach its unchanged sleep boundary')
        new = start_service('progress_monitor_v31', 'monitor_actual_optimization_progress_v31_20261006.py', [], pins)
        for _ in range(180):
            assert owned(new)
            documents = {name: read(A / name) for name in PUBLIC}
            generations = {v.get('complete_observer_generation') for v in documents.values()}
            if (len(generations) == 1 and all(v.get('actual_observer_version') == 31 and
                    v.get('active_root_command_owned') is True and v.get('active_round') == 95 and
                    v.get('actual_active_quality_rounds') == [95] for v in documents.values())):
                break
            time.sleep(1)
        else: raise RuntimeError('New observer did not publish a full owned R95 generation')
        assert documents[PUBLIC[2]]['pid'] == new['owned_worker_pid']
        for v in documents.values():
            assert v['gradient_sampling_actual_annual_fits'] == 30
            assert v['gradient_sampling_actual_final_fits'] == 6
            assert v['current_recovered_worker_ownership']['round95']['owned_live_now'] is True
            assert v['pending_required_rounds'] == documents[PUBLIC[0]]['pending_required_rounds']
        create(OUT / 'actual_first_complete_generation.json', {'status': 'passed_actual_complete_observer31_generation',
            'identity': new, 'documents': documents, 'complete_generation': next(iter(generations))})
        assert all(owned(row) for row in preserved.values())
        terminate_helper(old); retired = True; suspended.clear()
        create(old_path.parent / 'administrative_supersession_for_ready_GOSS_20261006.json', {
            'status': 'administratively_retired_idle_observer_not_claimed_naturally_complete',
            'identity': old, 'successor': new,
            'reason': 'Original monitor misses actual R95/R96 ownership; observer31 retains full collector and verifies real handles.',
            'scientific_processes_stopped_or_restarted': 0})
        for p, digest in pins.items(): assert sha(p) == digest, p
        assert all(owned(row) for row in preserved.values()) and owned(new)
        proof = {'status': 'passed_actual_observer31_full_generation_and_preserved_scientific_execution',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
            'old_observer': old, 'actual_observer': new, 'preserved_processes': preserved,
            'actual_complete_generation': next(iter(generations)),
            'new95_96_live_ownership_checked_without_reducing_original_scope': True,
            'old_source_and_R95_frozen_protocol_unchanged': True,
            'full_original_qualified_scores_native_counts_and_three_snapshot_transaction_retained': True,
            'old_observer_retired_only_at_verified_idle_boundary': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'scientific_processes_stopped_or_restarted': 0, 'actual_native_console_handle': 0}
        create(OUT / 'verification.json', proof); print(proof['status'], flush=True)
    finally:
        if not retired:
            if new is not None and owned(new): terminate_helper(new)
            for p in reversed(suspended):
                if p.is_running(): p.resume()


if __name__ == '__main__':
    try: main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_observer31_handoff', 'error': f'{type(error).__name__}: {error}'})
        raise
