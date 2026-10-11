"""Replace only the owned observer; preserve actual training, scoring and queues."""
from pathlib import Path
from datetime import datetime
import ctypes
import hashlib
import json
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch

OUT = A / 'distribution_views_progress_handoff_20261006'
SERVICE = A / 'service_owned_workflows_20261006/progress_monitor_v23'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def visible_terminals():
    user = ctypes.WinDLL('user32', use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
    user.EnumWindows.argtypes = [callback_type, ctypes.c_void_p]
    user.IsWindowVisible.argtypes = [ctypes.c_void_p]
    user.GetWindowThreadProcessId.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    user.GetClassNameW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
    user.GetWindowTextW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
    windows = []

    @callback_type
    def collect(handle, _):
        if user.IsWindowVisible(handle):
            kind, title = ctypes.create_unicode_buffer(128), ctypes.create_unicode_buffer(512)
            user.GetClassNameW(handle, kind, 128)
            if kind.value in ('ConsoleWindowClass', 'PseudoConsoleWindow', 'CASCADIA_HOSTING_WINDOW_CLASS'):
                user.GetWindowTextW(handle, title, 512)
                pid = ctypes.c_ulong()
                user.GetWindowThreadProcessId(handle, ctypes.byref(pid))
                windows.append({'pid': pid.value, 'class': kind.value, 'title': title.value})
        return 1

    assert user.EnumWindows(collect, None)
    return windows


def main():
    assert not SERVICE.exists() and not (OUT / 'frozen_before_handoff.json').exists()
    OUT.mkdir(exist_ok=True)
    old = read(A / 'service_owned_workflows_20261006/progress_monitor_v22/native_launch.json')
    assert owned(old)
    root = psutil.Process(old['pid'])
    worker = psutil.Process(old['owned_worker_pid'])
    assert root.create_time() == old['owned_parent_creation_time']
    assert root.cmdline()[-2:] == [old['script'], *old['script_args']]
    assert not worker.children()
    assert [p.pid for p in root.children() if p.name().lower() != 'conhost.exe'] == [worker.pid]
    identities = {}
    for name in ('neural16384_annual', 'dependency_queue_v4', 'main_publisher_v5',
                 'quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue'):
        row = read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        assert owned(row) and row['actual_native_console_handle'] == 0
        identities[name] = row
    queue = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    for name, status in queue['job_ownership'].items():
        if name.startswith('round') and status['owned_live']:
            active = read(A / f'service_owned_dependency_queue_v4_20261006/activated_jobs/{name}/launch.json')
            assert owned(active)
            identities[name] = active
    old_plan = read(A / 'quantile_tree_quality_queue_v2_20261006/plan.json')
    new_plan = read(A / 'quantile_distribution_views_quality_queue_20261006/plan.json')
    assert old_plan['expected_full_records'] == [100, 98]
    assert new_plan['quality_records'] == [124, 138]
    for plan in (old_plan, new_plan):
        for filename, digest in plan['input_sha256'].items():
            assert sha(filename) == digest, filename
    files = dict(read(A / 'service_owned_workflows_20261006/progress_monitor_v22/job_definition.json')['input_sha256'])
    files.update({str(A / name): sha(A / name) for name in (
        'monitor_actual_optimization_progress_v23_20261006.py',
        'run_quantile_distribution_views_quality_queue_20261006.py',
        'qualified_round_recovery_evidence_v3_20261006.py')})
    for filename, digest in files.items():
        assert sha(filename) == digest
        if Path(filename).suffix == '.py':
            compile(Path(filename).read_text(encoding='utf-8-sig'), filename, 'exec')
    before = read(A / 'ongoing_optimization_state.json')
    create(OUT / 'frozen_before_handoff.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'old_ownership': old,
        'unchanged_scientific_ownership': identities, 'input_sha256': files,
        'visible_terminal_windows': visible_terminals(),
        'observed_native_counts': {key: before[key] for key in (
            'actual_new_annual_fits_completed', 'fulltraining_artifacts_ready')},
        'old198_and_new262_grid_sources_verified': True,
        'new_quality_scores_by_handoff': 0})
    SERVICE.mkdir()
    definition = SERVICE / 'job_definition.json'
    create(definition, {'name': 'progress_monitor_v23',
        'driver': str(A / 'monitor_actual_optimization_progress_v23_20261006.py'),
        'arguments': [], 'scratch': str(ROOT / 'tmp/service_owned_progress_monitor_v23'),
        'input_sha256': files,
        'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py')})
    # Exact observer identities checked above. No scientific worker is terminated.
    worker.terminate()
    worker.wait(timeout=15)
    if root.is_running():
        assert root.create_time() == old['owned_parent_creation_time']
        root.terminate()
        root.wait(timeout=15)
    assert not owned(old)
    for row in identities.values():
        assert owned(row)
    actual_launch = launch(definition, Path(
        'C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(OUT / 'actual_observer_launch.json', actual_launch)
    print(json.dumps({'status': 'new_hidden_observer_launched_actual_update_pending',
        'old_observer_closed': True, 'scientific_workers_preserved': list(identities),
        'visible_terminals_before': visible_terminals()}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
