"""Replace the memory-only pause with a tested disk recovery stop for tonight."""
from pathlib import Path
from datetime import datetime
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from scheduled_user_pause_20261007 import read, write, inventory, exact
from shutdown_ready_stop_20261007 import checkpoint_inventory
from run_dependency_queue_v3_20261006 import sha, owned
from handoff_ready_goss_full_execution_20261006 import start_service, pair


def main():
    module = A / 'shutdown_ready_stop_20261007.py'
    helper = A / 'scheduled_user_pause_20261007.py'
    proofs = [A / 'shutdown_ready_stop_preflight_20261007/verification.json',
              A / 'shutdown_ready_stop_preflight_preheld_20261007/verification.json']
    expected = ['passed_actual_hidden_deadline_stop_exact_probe_identities_and_durable_recovery_record',
                'passed_actual_hidden_deadline_stop_preheld_probe_and_durable_recovery_record']
    for path, status in zip(proofs, expected):
        proof = read(path)
        assert proof['status'] == status and proof['module_sha256'] == sha(module)
        assert proof['pause_helper_sha256'] == sha(helper)
    deadline = datetime.fromisoformat('2026-10-07T23:55:00+08:00')
    assert datetime.now().astimezone() < datetime.fromisoformat('2026-10-07T23:45:00+08:00')
    folder = A / 'shutdown_ready_stop_until_manual_continue_20261007'
    assert not folder.exists()
    folder.mkdir()
    old_folder = A / 'user_pause_until_manual_continue_20261007'
    old_row = read(old_folder / 'actual_schedule_activation.json')['guardian_launch']
    old_status = read(old_folder / 'guardian_status.json')
    assert old_status['status'] == 'scheduled_running_until_deadline' and old_status['suspended_entries'] == 0
    assert not (old_folder / 'suspension_journal.json').exists()
    before = inventory(full=True)
    checkpoint = checkpoint_inventory()
    write(folder / 'actual_saved_checkpoint_preparation.json', checkpoint)
    config = {
        'actual_latest_user_instruction': '12点后电脑要关机',
        'actual_previous_resume_reply': '等我明早发送“继续”再恢复',
        'stop_at_local': deadline.isoformat(), 'quiesce_at_local': '2026-10-07T23:45:00+08:00',
        'timezone': 'Asia/Taipei', 'output_folder': str(folder),
        'stop_method': 'verified_process_stop_with_durable_disk_recovery_manifest',
        'automatic_restart_enabled': False, 'execute_Windows_shutdown': False,
        'user_will_shutdown_computer_after_midnight': True,
        'computer_may_be_powered_off_after_project_stop': True,
        'resume_policy': 'only_after_actual_user_continue_after_power_on',
        'unsaved_current_GPU_annual_fit_requires_full_restart_unless_complete_artifact_written_before_stop': True,
        'partial_epochs_not_claimed_saved_or_completed': True,
        'completed_models_results_and_scores_retained_on_D': True,
        'obsolete_memory_pause_schedule': str(old_folder / 'schedule.json'),
        'old_guardian_to_be_administratively_retired': old_row,
        'recovery_instructions': [
            'Read disk_recovery_manifest.json after the actual user continues.',
            'Rehash complete disk artifacts and frozen source pins; preserve all existing scores and receipts.',
            'Create fresh attempt directories for interrupted exclusive output workflows.',
            'Restart only unfinished steps; never treat an incomplete annual fit as a checkpoint.',
            'Do not automatically start tasks on power-on or on a timed morning schedule.']}
    write(folder / 'schedule.json', config)
    pins = {str(module): sha(module), str(helper): sha(helper),
            str(folder / 'schedule.json'): sha(folder / 'schedule.json'),
            **{str(path): sha(path) for path in proofs}}
    new_row = start_service('shutdown_ready_2355_manual_continue_20261007', module.name,
                            ['run', '--folder', str(folder)], pins)
    limit = time.monotonic() + 30
    while not (folder / 'guardian_status.json').exists():
        assert owned(new_row) and time.monotonic() < limit
        time.sleep(.1)
    state = read(folder / 'guardian_status.json')
    assert state['status'] == 'scheduled_shutdown_compatible_stop'
    assert state['guardian']['pid'] == new_row['owned_worker_pid'] and exact(state['guardian']) is not None
    assert new_row['actual_native_console_handle'] == 0 and not new_row['independent_launch_root_in_any_job']
    parent, worker = pair(old_row)
    assert not worker.children()
    worker.terminate()
    worker.wait(timeout=10)
    parent.terminate()
    parent.wait(timeout=10)
    assert not owned(old_row)
    write(Path(old_row['script_args'][0]).parent / 'administrative_supersession_for_shutdown_20261007.json', {
        'status': 'administratively_retired_memory_pause_guardian_for_latest_shutdown_requirement',
        'actual_user_instruction': '12点后电脑要关机', 'original_identity': old_row,
        'successor_identity': new_row, 'scientific_workers_terminated_now': 0,
        'not_claimed_scientifically_or_naturally_completed': True})
    write(old_folder / 'superseded_by_shutdown_plan_20261007.json', {
        'status': 'obsolete_memory_pause_schedule_do_not_use_old_resume_command',
        'current_schedule': str(folder / 'schedule.json'),
        'actual_user_instruction': '12点后电脑要关机'})
    write(folder / 'handoff_committed.json', {
        'status': 'actual_hidden_shutdown_ready_guardian_live_old_memory_guardian_retired',
        'actual_new_guardian': new_row, 'old_memory_guardian': old_row,
        'scientific_workers_terminated_now': 0})
    write(folder / 'actual_schedule_activation.json', {
        'status': 'passed_actual_hidden_shutdown_ready_2355_schedule_and_memory_guardian_supersession',
        'guardian_launch': new_row, 'actual_initial_guardian_state': state,
        'input_sha256': pins, 'scientific_workers_before_handoff': before,
        'actual_checked_saved_annual_years': [r['year'] for r in checkpoint['verified_complete_annual_fits']],
        'real_2355_stop_not_yet_executed': True, 'Windows_shutdown_executed': False,
        'scientific_workers_terminated_now': 0, 'new_native_fits': 0, 'new_quality_scores': 0})
    write(A / 'current_user_runtime_control_20261007.json', {
        'status': 'goal_paused_background_stop_scheduled_for_user_shutdown',
        'actual_user_shutdown_request': '12点后电脑要关机',
        'current_schedule': str(folder / 'schedule.json'),
        'actual_schedule_activation': str(folder / 'actual_schedule_activation.json'),
        'disk_recovery_manifest_expected_after_2355': str(folder / 'disk_recovery_manifest.json'),
        'resume_only_after_user_continue': True, 'automatic_restart_enabled': False,
        'memory_pause_plan_obsolete': True, 'foreground_optimization_still_paused': True})
    print('passed_actual_hidden_shutdown_ready_2355_schedule_and_memory_guardian_supersession')


if __name__ == '__main__':
    main()
