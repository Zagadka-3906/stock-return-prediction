"""Read-only visible-terminal and exact-owned workflow status snapshot."""
from pathlib import Path
from datetime import datetime
import ctypes
import json
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'

def main():
    user = ctypes.WinDLL('user32', use_last_error=True)
    cbtype = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
    user.EnumWindows.argtypes = [cbtype, ctypes.c_void_p]
    user.IsWindowVisible.argtypes = [ctypes.c_void_p]
    user.GetWindowThreadProcessId.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    user.GetClassNameW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
    windows = []
    @cbtype
    def visit(handle, _):
        if user.IsWindowVisible(handle):
            kind = ctypes.create_unicode_buffer(128)
            user.GetClassNameW(handle, kind, 128)
            if kind.value in ('PseudoConsoleWindow', 'ConsoleWindowClass', 'CASCADIA_HOSTING_WINDOW_CLASS'):
                pid = ctypes.c_ulong()
                user.GetWindowThreadProcessId(handle, ctypes.byref(pid))
                windows.append({'pid': pid.value, 'class': kind.value})
        return 1
    assert user.EnumWindows(visit, None)
    workers = []
    for name, path in [
        ('round95', A/'service_owned_dependency_queue_v4_20261006/activated_jobs/round95/launch.json'),
        *[(name, A/f'service_owned_workflows_20261006/{name}/native_launch.json')
          for name in ('neural16384_annual', 'main_publisher_v6', 'progress_monitor_v31')],
    ]:
        row = json.loads(path.read_text(encoding='utf-8'))
        pid = row['owned_worker_pid']
        result = {'name': name, 'pid': pid, 'live_matching_identity': False}
        try:
            p = psutil.Process(pid)
            assert p.create_time() == row['owned_worker_creation_time']
            assert str(row['script']) in p.cmdline()
            result.update(live_matching_identity=True, cpu_seconds=sum(p.cpu_times()[:2]),
                          RSS_bytes=p.memory_info().rss,
                          child_pids=[child.pid for child in p.children(recursive=True)])
        except (psutil.Error, AssertionError) as exc:
            result['identity_error'] = type(exc).__name__
        workers.append(result)
    waves = []
    for wave in (371, 372, 373, 374):
        path = A/f'optimization_20261003_r95/wave{wave}_results.json'
        if path.exists():
            row = json.loads(path.read_text(encoding='utf-8'))
            values = list(row['results'].values())
            waves.append({'wave': wave, 'status': row['status'], 'records': len(values),
                          'best_actual_score': max(v['connected_final_score'] for v in values) if values else None})
    value = {'at_local': datetime.now().isoformat(timespec='seconds'),
             'visible_terminal_count': len(windows), 'visible_terminals': windows,
             'workers': workers, 'round95_waves': waves,
             'available_RAM_GiB': psutil.virtual_memory().available/2**30,
             'disk_free_GiB': {drive: psutil.disk_usage(drive+':/').free/2**30 for drive in ('D', 'E')},
             'processes_closed_or_restarted': 0, 'windows_changed': False}
    out = A/f"windows_and_work_status_{datetime.now():%Y%m%d_%H%M%S}.json"
    with out.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(value, ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
