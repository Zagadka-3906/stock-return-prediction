"""Read live scoring stacks to locate costs; never inject code or pause workers."""
from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from run_dependency_queue_v3_20261006 import owned


def main():
    out = A / 'round83_readonly_scoring_bottleneck_20261006'
    assert not out.exists()
    row = read(A / 'service_owned_dependency_queue_v4_20261006/activated_jobs/round83/launch.json')
    assert owned(row)
    root = psutil.Process(row['owned_worker_pid'])
    children = [p for p in root.children(recursive=True) if p.name().lower() == 'python.exe']
    assert len(children) == 1
    processes = [root, *children]
    identities = [{'pid': p.pid, 'birth': p.create_time(), 'command': p.cmdline()} for p in processes]
    receipt = read(ROOT / 'tools/readonly_pyspy_diagnostics_20261006/receipt.json')
    binary = Path(receipt['binary'])
    assert sha(binary) == receipt['binary_sha256']
    out.mkdir()
    create(out / 'frozen_before_readonly_sampling.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'actual_owned_round83': row,
        'actual_owned_process_tree_members': identities,
        'source_sha256': sha(__file__), 'diagnostic_binary': receipt,
        'target_processes_not_paused_or_modified': True, 'new_quality_scores': 0,
        'test_labels_read': False})
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    options = dict(cwd=ROOT, stdin=subprocess.DEVNULL, startupinfo=startup,
        creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True, text=True,
        encoding='utf-8', errors='replace', timeout=20)
    observed = []
    for sample in range(3):
        assert owned(row)
        for identity in identities:
            process = psutil.Process(identity['pid'])
            assert process.create_time() == identity['birth'] and process.cmdline() == identity['command']
            result = subprocess.run([str(binary), 'dump', '--pid', str(process.pid), '--nonblocking', '--json'], **options)
            (out / f'sample{sample}_pid{process.pid}.json').write_text(result.stdout, encoding='utf-8')
            (out / f'sample{sample}_pid{process.pid}_stderr.txt').write_text(result.stderr, encoding='utf-8')
            assert result.returncode == 0, result.stderr
            value = json.loads(result.stdout)
            threads = value if isinstance(value, list) else value.get('threads', [value])
            summary = {'at_local': datetime.now().isoformat(timespec='seconds'), 'pid': process.pid,
                'CPU_seconds': sum(process.cpu_times()[:2]), 'RSS_bytes': process.memory_info().rss,
                'stacks': [[{key: frame.get(key) for key in ('name', 'short_filename', 'line')}
                    for frame in thread.get('frames', [])[:10]] for thread in threads if thread.get('frames')]}
            observed.append(summary)
            print(json.dumps(summary, ensure_ascii=False), flush=True)
        if sample < 2:
            time.sleep(10)
    assert owned(row) and sha(binary) == receipt['binary_sha256']
    create(out / 'verification.json', {'status': 'passed_actual_owned_readonly_scoring_stack_observations',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'actual_owned_round83': row,
        'actual_process_identities': identities, 'actual_observations': observed,
        'nonblocking_readonly_sampling': True, 'scoring_not_paused_restarted_or_modified': True,
        'performance_causation_and_acceleration_not_yet_proven': True,
        'new_quality_scores_by_diagnostics': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
