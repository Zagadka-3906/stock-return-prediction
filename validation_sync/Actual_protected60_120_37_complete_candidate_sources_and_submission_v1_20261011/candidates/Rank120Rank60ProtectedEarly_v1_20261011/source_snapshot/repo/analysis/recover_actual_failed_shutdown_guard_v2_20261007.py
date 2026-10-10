"""Restore the user's actual deadline after preserving the original pause race failure."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    failed = A / 'service_owned_workflows_20261006/shutdown_ready_2355_manual_continue_20261007'
    assert not owned(read(failed / 'native_launch.json'))
    assert read(failed / 'service_execution.json')['status'] == 'failed'
    assert 'AssertionError' in (failed / 'stderr.log').read_text(encoding='utf8')
    folder = A / 'shutdown_ready_stop_until_manual_continue_20261007'
    paths = [Path(__file__), A / 'shutdown_ready_stop_v2_20261007.py', A / 'shutdown_ready_stop_20261007.py',
             A / 'scheduled_user_pause_20261007.py', folder / 'schedule.json', folder / 'handoff_committed.json',
             failed / 'service_execution.json', failed / 'stderr.log']
    pins = {str(p): sha(p) for p in paths}
    row = start('shutdown_ready_2355_manual_continue_v2_20261007', 'shutdown_ready_stop_v2_20261007.py',
                ['run', '--folder', str(folder)], pins)
    for _ in range(20):
        status = read(folder / 'guardian_status.json')
        if status['guardian']['pid'] == row['owned_worker_pid']:
            assert status['status'] == 'quiescing_dispatch_before_disk_stop'
            assert owned(row)
            create(A / 'actual_failed_shutdown_guard_recovery_v2_20261007.json', {
                'status': 'actual_restarted_guard_live_after_preserved_suspend_race_failure',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
                'new_guard': row, 'actual_fresh_guard_status': status, 'stop_at_local': '2026-10-07T23:55:00+08:00',
                'automatic_restart_enabled': False, 'no_scientific_completion_claimed': True})
            print('Actual replacement guard verified live until 23:55.', flush=True)
            return
        time.sleep(.5)
    raise RuntimeError('Replacement guard heartbeat not verified.')


if __name__ == '__main__':
    main()
