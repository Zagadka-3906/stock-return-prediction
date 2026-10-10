"""Stop verified project workers and write a disk recovery manifest before user shutdown.

No Windows shutdown or automatic startup is requested. Partial, unsaved native
fits are recorded as interrupted; they are never declared saved or completed.
"""
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import ctypes
import hashlib
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from scheduled_user_pause_20261007 import read, write, identity, exact, inventory, verified_pair
from shutdown_ready_stop_v2_20261007 import StableJournal as Journal


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def checkpoint_inventory():
    delivery=A/'latest_verified_submission_delivery_v2_20261008.json'
    value=read(delivery)
    assert value['status']=='ready_exact_fully_qualified_main_published_submission_csv'
    progress=[]
    for family,expected in [('JointCrossHuberOrder185',185),('AdaptiveJointCrossHuber242',242),('PureRFFHuber128',128)]:
        folder=A/(family+'_official_comparison_v1_20261008')
        completed=sorted(folder.glob('case*_official.json'))
        progress.append({'family':family,'expected_cases':expected,'actual_saved_official_case_records':len(completed),'complete_score_verification_present':(folder/'verification.json').is_file(),'completed_records_preserved':True})
    return {'status':'previously_fully_verified_disk_delivery_and_saved_score_metadata_retained',
            'latest_fully_verified_delivery':value,'delivery_pointer_sha256':sha(delivery),
            'pending_round_saved_record_counts':progress,'no_new_full_model_or_csv_rehash_claimed_during_stop':True,
            'completed_disk_artifacts_must_be_rehashed_before_resume':True,'partial_unsaved_work_not_claimed_complete':True}


def select_targets(config):
    fixture = config.get('isolated_preflight_target')
    if fixture is not None:
        assert fixture['name'].startswith('shutdown_stop_probe')
        assert fixture['original_driver'] == str(A / 'scheduled_user_pause_20261007.py')
        assert fixture['original_arguments'] == ['probe', '--folder', config['output_folder']]
        return [{'name': fixture['name'], 'launch': fixture}]
    return inventory(full=True)


def recovery_definition(row):
    launch = row['launch']
    path = Path(launch['script_args'][0])
    result = {'name': row['name'], 'original_launch': launch,
              'launch_definition_path': str(path), 'launch_definition_sha256': sha(path),
              'original_driver': launch.get('original_driver', launch.get('original_script')),
              'original_arguments': launch.get('original_arguments', []),
              'must_not_blindly_rerun_existing_exclusive_output_paths': True,
              'new_attempt_required_for_interrupted_immutable_workflows': True,
              'source_and_completed_artifact_checks_required_before_restart': True}
    if path.name == 'job_definition.json':
        definition = read(path)
        result['original_driver'] = definition['driver']
        result['original_arguments'] = definition['arguments']
        result['definition'] = definition
    return result


def stop_verified(folder, config, journal):
    rows = select_targets(config)
    known_pairs = []
    for row in rows:
        pair = verified_pair(row['launch'])
        if pair is not None:
            known_pairs.append({'name': row['name'], 'identities': [identity(p) for p in pair]})
    write(folder / 'actual_jobs_before_stop.json', {
        'at_local': datetime.now().astimezone().isoformat(),
        'jobs': [recovery_definition(row) for row in rows],
        'resume_policy': 'only_after_actual_user_continue_after_power_on',
        'automatic_restart_enabled': False})
    # All workers are frozen before termination, preventing new task dispatch.
    controllers = lambda r: any(word in r['name'] for word in ('queue', 'publisher', 'publication', 'monitor', 'guard'))
    rows.sort(key=lambda r: not controllers(r))
    for row in rows:
        try:
            journal.suspend_pair(row)
        except psutil.NoSuchProcess:
            pass
    journal.data['status'] = 'frozen_for_user_requested_shutdown_stop'
    journal.flush()
    stopped = []
    entries = [entry for entry in journal.data['entries'] if entry['phase'] in ('pending', 'suspended')]
    # Kill dispatchers and independent lease guards first, then scientific workers.
    entries.sort(key=lambda entry: (not any(word in entry['owner'] for word in
                                            ('queue', 'publisher', 'publication', 'monitor', 'guard')),
                                   entry['role'] == 'launch_parent'))
    for entry in entries:
        process = exact(entry['identity'])
        if process is None:
            entry['phase'] = 'already_exited_before_shutdown_stop'
        else:
            assert process.pid != psutil.Process().pid
            process.terminate()
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            entry['phase'] = 'stopped_for_actual_user_shutdown_request'
            stopped.append(entry['identity'])
        journal.flush()
    # A worker previously suspended by a different owner was intentionally not
    # resumed by the journal; it is still an explicitly owned shutdown target.
    for pair in known_pairs:
        for record in pair['identities']:
            process = exact(record)
            if process is not None:
                process.terminate()
                process.wait(timeout=5)
                stopped.append(record)
    remaining = select_targets(config)
    remaining = [row for row in remaining if verified_pair(row['launch']) is not None]
    assert not remaining, 'An owned task is still alive; shutdown readiness not claimed.'
    assert all(exact(record) is None for pair in known_pairs for record in pair['identities'])
    checkpoint = ({'status': 'isolated_probe_no_real_training_artifacts'}
                  if config.get('isolated_preflight_target') else checkpoint_inventory())
    receipts = {}
    if not config.get('isolated_preflight_target'):
        for path in (A / 'github_validation_sync_main_20261005').glob('round*_receipt.json'):
            receipt = read(path)
            if receipt.get('status') == 'pushed_and_remote_head_verified':
                receipts[str(path)] = {'sha256': sha(path), 'round': receipt.get('round'),
                                       'commit': receipt.get('commit'),
                                       'official_score': receipt.get('official_score')}
    write(folder / 'disk_recovery_manifest.json', {
        'status': 'project_workers_stopped_with_disk_recovery_manifest',
        'at_local': datetime.now().astimezone().isoformat(),
        'actual_user_shutdown_instruction': '23:55停止工作',
        'stopped_exact_identities': stopped, 'jobs_before_stop': read(folder / 'actual_jobs_before_stop.json'),
        'completed_native_disk_checkpoints': checkpoint,
        'already_published_full_round_receipts': receipts,
        'partial_unsaved_fits_not_preserved_or_counted_as_complete': True,
        'partial_fit_restart_required_if_no_complete_annual_artifact': True,
        'computer_need_not_remain_on_after_this_stop': True,
        'automatic_restart_enabled': False, 'Windows_shutdown_command_executed': False,
        'resume_requires_actual_user_continue_after_power_on': True,
        'new_native_fits': 0, 'new_quality_scores': 0,
        'scientific_pass_markers_written_for_interrupted_workers': 0})
    for row in rows:
        launch = row['launch']
        output = Path(launch['script_args'][0]).parent
        write(output / 'user_requested2355_interruption_20261008.json', {
            'status': 'administratively_stopped_for_user_shutdown_not_scientifically_complete',
            'actual_user_instruction': '23:55停止工作',
            'original_launch': launch, 'recovery_manifest': str(folder / 'disk_recovery_manifest.json'),
            'partial_unsaved_fit_not_claimed_saved': True})


def run(folder):
    config = read(folder / 'schedule.json')
    assert config['output_folder'] == str(folder)
    assert config['automatic_restart_enabled'] is False
    assert config['execute_Windows_shutdown'] is False
    fixture = config.get('isolated_preflight_target')
    if fixture:
        assert folder.name.startswith('shutdown_ready_stop_preflight_')
    deadline = datetime.fromisoformat(config['stop_at_local'])
    quiesce = deadline - timedelta(seconds=.25 if fixture else 120)
    journal = Journal(folder)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.SetThreadExecutionState.argtypes = [ctypes.c_uint32]
    kernel.SetThreadExecutionState.restype = ctypes.c_uint32
    assert kernel.SetThreadExecutionState(0x80000001)
    try:
        while datetime.now().astimezone() < deadline:
            current = datetime.now().astimezone()
            if current >= quiesce:
                for row in select_targets(config):
                    if any(word in row['name'] for word in ('dependency_queue', 'publisher', 'publication')):
                        try:
                            journal.suspend_pair(row, quiet_only=True)
                        except psutil.NoSuchProcess:
                            pass
            write(folder / 'guardian_status.json', {
                'status': 'quiescing_dispatch_before_disk_stop' if current >= quiesce else 'scheduled_shutdown_compatible_stop',
                'guardian': identity(psutil.Process()),
                'at_local': current.isoformat(), 'stop_at_local': deadline.isoformat(),
                'automatic_restart_enabled': False, 'requires_remaining_powered_on_overnight': False,
                'execute_Windows_shutdown': False,
                'suspended_entries': sum(e['phase'] == 'suspended' for e in journal.data['entries'])})
            time.sleep(.05 if fixture else min(10, max(.05, (deadline - current).total_seconds())))
        if not fixture:
            assert (folder / 'handoff_committed.json').exists(), 'Schedule handoff was not committed.'
        stop_verified(folder, config, journal)
        write(folder / 'guardian_status.json', {
            'status': 'finished_project_stop_ready_for_user_computer_shutdown',
            'at_local': datetime.now().astimezone().isoformat(),
            'recovery_manifest': str(folder / 'disk_recovery_manifest.json'),
            'automatic_restart_enabled': False, 'execute_Windows_shutdown': False,
            'system_awake_request_active': False})
    finally:
        kernel.SetThreadExecutionState(0x80000000)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['run', 'checkpoints'])
    parser.add_argument('--folder', type=Path, default=A / 'user_requested_stop2355_until_manual_continue_20261008')
    args = parser.parse_args()
    folder = args.folder.resolve()
    assert folder.is_relative_to(A) and folder.drive.upper() in ('D:', 'E:')
    if args.mode == 'run':
        run(folder)
    else:
        write(folder / 'actual_saved_checkpoint_preparation.json', checkpoint_inventory())


if __name__ == '__main__':
    main()
