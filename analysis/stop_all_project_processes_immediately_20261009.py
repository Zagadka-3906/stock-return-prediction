"""Execute the user's immediate stop using the verified process ownership journal."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys
import json

A = Path(__file__).resolve().parent
sys.path.insert(0, str(A))
import user_requested_stop2355_v1_20261009 as current
from scheduled_user_pause_20261007 import read, write, inventory

now = datetime.now(timezone(timedelta(hours=8))).isoformat()
folder = A / ('user_requested_immediate_stop_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
folder.mkdir(exist_ok=False)
config = {
    'output_folder': str(folder), 'stop_at_local': now,
    'actual_user_instruction': '停止所有进程',
    'automatic_restart_enabled': False, 'execute_Windows_shutdown': False,
    'supersedes_previous_2355_schedule': True,
}
write(folder / 'schedule.json', config)
write(folder / 'actual_schedule_activation.json', {
    'status': 'executing_immediate_user_requested_project_stop',
    'at_local': now, 'actual_user_instruction': '停止所有进程',
})
current.core.checkpoint_inventory = current.checkpoint_inventory
current.stop_verified(folder, config, current.core.Journal(folder))
manifest_path = folder / 'disk_recovery_manifest.json'
manifest = read(manifest_path)
manifest['actual_user_shutdown_instruction'] = '停止所有进程'
manifest['immediate_pause_supersedes_previous_scheduled_stop'] = True
manifest['resume_requires_actual_user_continue'] = True
manifest['resume_notes'] = [
    'Round157 core preparation v62 remains unadmitted; quality v2 exclusive output directory already exists. Resolve storage admission with a new immutable attempt before any manual restart.',
    'Do not resume or blindly rerun interrupted immutable workflows.',
]
write(manifest_path, manifest)
for control_name in ('current_user_runtime_control_20261009.json', 'current_user_runtime_control_20261008.json'):
    path = A / control_name
    control = read(path)
    control.update(actual_user_instruction='停止所有进程', immediate_pause=True,
                   goal_pause_required_after_actual_deadline=False,
                   goal_pause_required_now=True, automatic_restart_enabled=False)
    write(path, control)
for job in manifest['jobs_before_stop']['jobs']:
    path = Path(job['launch_definition_path']).parent / 'user_requested2355_interruption_20261008.json'
    if path.is_file():
        record = read(path)
        record.update(actual_user_instruction='停止所有进程',
                      status='administratively_stopped_on_immediate_user_request_not_scientifically_complete')
        write(path, record)
remaining = inventory(full=True)
assert not remaining, 'Owned project process remains alive'
result = {
    'status': 'all_verified_project_processes_stopped',
    'at_local': datetime.now(timezone(timedelta(hours=8))).isoformat(),
    'owned_jobs_stopped': len(manifest['jobs_before_stop']['jobs']),
    'exact_process_identities_stopped': len(manifest['stopped_exact_identities']),
    'remaining_owned_project_jobs': len(remaining),
    'recovery_manifest': str(manifest_path), 'automatic_restart_enabled': False,
}
write(folder / 'guardian_status.json', result)
print(json.dumps(result, ensure_ascii=False))
