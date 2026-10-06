"""Read the actual live trainer stack and scalar loop positions without pausing it."""
from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from run_dependency_queue_v3_20261006 import owned


def main():
    out = A / 'neural16384_readonly_stack_diagnostics_20261006'
    assert not out.exists()
    row = read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    assert owned(row)
    receipt = read(ROOT / 'tools/readonly_pyspy_diagnostics_20261006/receipt.json')
    executable = Path(receipt['binary'])
    assert sha(executable) == receipt['binary_sha256']
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    options = dict(cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True,
        startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW,
        text=True, encoding='utf-8', errors='replace', timeout=20)
    help_result = subprocess.run([str(executable), 'dump', '--help'], **options)
    assert help_result.returncode == 0
    assert all(flag in help_result.stdout for flag in ('--nonblocking', '--locals', '--json'))
    inputs = {str(path.resolve()): sha(path) for path in (Path(__file__),
        A / 'train_diverse_backbones_20261003.py',
        A / 'run_neural16384_full_bank_20261005.py', executable)}
    out.mkdir()
    create(out / 'frozen_before_actual_readonly_sampling.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'actual_owned_trainer': row,
        'input_sha256': inputs, 'actual_verified_diagnostic_binary': receipt,
        'flags': ['dump', '--pid', str(row['owned_worker_pid']), '--nonblocking', '--locals', '--json'],
        'target_process_not_paused_or_modified': True, 'new_model_fits': 0, 'new_quality_scores': 0})
    process = psutil.Process(row['owned_worker_pid'])
    before = {'CPU_seconds': sum(process.cpu_times()[:2]), 'RSS_bytes': process.memory_info().rss}
    result = subprocess.run([str(executable), 'dump', '--pid', str(row['owned_worker_pid']),
        '--nonblocking', '--locals', '--json'], **options)
    (out / 'actual_dump_stdout.json').write_text(result.stdout, encoding='utf-8')
    (out / 'actual_dump_stderr.txt').write_text(result.stderr, encoding='utf-8')
    assert owned(row)
    for path, digest in inputs.items():
        assert sha(path) == digest
    create(out / 'actual_sampling_result.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'returncode': result.returncode,
        'actual_trainer_still_owned': True, 'before': before,
        'after': {'CPU_seconds': sum(process.cpu_times()[:2]), 'RSS_bytes': process.memory_info().rss},
        'source_and_diagnostic_binary_hashes_unchanged': True,
        'nonblocking_flags_used': True, 'hidden_child_creation_flags_used': True,
        'actual_dump_sha256': sha(out / 'actual_dump_stdout.json')})
    if result.returncode:
        print(json.dumps({'status': 'actual_readonly_dump_failed_trainer_preserved',
            'error': result.stderr[:1000], 'returncode': result.returncode}), flush=True)
        return
    value = json.loads(result.stdout)
    threads = value if isinstance(value, list) else value.get('threads', [value])
    frames = []
    for thread in threads:
        for frame in thread.get('frames', []):
            if 'fit_arrays' in str(frame.get('name', frame.get('function', ''))):
                frames.append(frame)
    create(out / 'actual_fit_arrays_frames.json', {'status': 'actual_readonly_dump_collected', 'frames': frames})
    print(json.dumps({'status': 'actual_readonly_dump_collected', 'thread_count': len(threads),
        'fit_arrays_frames': frames, 'trainer_owned_live_after_sampling': True}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
