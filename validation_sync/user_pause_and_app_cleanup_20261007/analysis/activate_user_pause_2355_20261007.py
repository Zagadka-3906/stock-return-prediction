"""Install the tested user-requested pause without stopping current scientific workers early."""
from pathlib import Path
from datetime import datetime
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from scheduled_user_pause_20261007 import read, write, inventory, exact
from run_dependency_queue_v3_20261006 import sha, owned
from handoff_ready_goss_full_execution_20261006 import start_service


def main():
    proof = A / 'scheduled_user_pause_integration_preflight_v3_20261007/verification.json'
    verification = read(proof)
    assert verification['status'] == 'passed_actual_hidden_timer_deadline_pause_no_auto_resume_and_manual_same_identity_resume'
    module = A / 'scheduled_user_pause_20261007.py'
    assert verification['module_sha256'] == sha(module)
    folder = A / 'user_pause_until_manual_continue_20261007'
    assert not folder.exists()
    folder.mkdir()
    deadline = datetime.fromisoformat('2026-10-07T23:55:00+08:00')
    assert datetime.now().astimezone() < deadline
    schedule = {
        'actual_user_pause_request': '今晚十二点前暂时停止工作，明早继续',
        'actual_user_resume_reply': '等我明早发送“继续”再恢复',
        'pause_at_local': deadline.isoformat(), 'timezone': 'Asia/Taipei',
        'quiesce_at_local': '2026-10-07T23:50:00+08:00',
        'resume_policy': 'only_after_actual_user_continue',
        'resume_at_local': None, 'automatic_resume_enabled': False,
        'pause_method': 'suspend_verified_owned_processes_and_retain_RAM',
        'new_foreground_exploration_after_setup': False,
        'already_authorized_background_plans_run_until_pause': True,
        'manual_resume_command': [str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                                  str(module), 'resume', '--folder', str(folder), '--user-continue'],
        'resume_command_requires_actual_user_continue_in_chat': True,
        'computer_must_remain_powered_on_to_retain_unsaved_native_training': True,
        'latest_user_application_cleanup_record': str(A / 'user_requested_qemu_two_Java_cleanup_20261007.json'),
        'scientific_goal_not_marked_complete': True}
    write(folder / 'schedule.json', schedule)
    before = inventory(full=True)
    write(folder / 'actual_owned_scientific_workers_before_scheduling.json', {
        'status': 'actual_live_owned_identity_inventory_no_suspension_performed',
        'at_local': datetime.now().astimezone().isoformat(), 'workers': before,
        'scientific_workers_suspended_before_deadline': 0})
    pins = {str(module): sha(module), str(proof): sha(proof),
            str(folder / 'schedule.json'): sha(folder / 'schedule.json')}
    row = start_service('user_pause_2355_wait_manual_continue_20261007', module.name,
                        ['run', '--folder', str(folder)], pins)
    limit = time.monotonic() + 30
    while not (folder / 'guardian_status.json').exists():
        assert owned(row) and time.monotonic() < limit
        time.sleep(.1)
    status = read(folder / 'guardian_status.json')
    assert status['status'] == 'scheduled_running_until_deadline'
    assert status['guardian']['pid'] == row['owned_worker_pid']
    assert exact(status['guardian']) is not None and status['suspended_entries'] == 0
    assert row['actual_native_console_handle'] == 0 and not row['independent_launch_root_in_any_job']
    write(folder / 'actual_schedule_activation.json', {
        'status': 'passed_actual_independent_hidden_pause_guardian_running_for_2355_manual_resume_only',
        'guardian_launch': row, 'actual_initial_guardian_state': status,
        'input_sha256': pins, 'at_local': datetime.now().astimezone().isoformat(),
        'real_deadline_pause_not_yet_executed': True,
        'scientific_workers_suspended_before_deadline': 0,
        'scientific_jobs_terminated': 0, 'new_native_fits': 0, 'new_quality_scores': 0})
    print('passed_actual_independent_hidden_pause_guardian_running_for_2355_manual_resume_only')


if __name__ == '__main__':
    main()
