"""Resume only exact scheduler identities if an outside-job capacity owner exits unexpectedly."""
from pathlib import Path
import json
import sys
import time
import psutil


def exact(row):
    try:
        process = psutil.Process(row['pid'])
        if process.create_time() == row['creation_time'] and process.cmdline() == row['command_line']:
            return process
    except psutil.Error:
        pass
    return None


def main():
    path = Path(sys.argv[1]).resolve()
    assert path.drive.upper() in ('D:', 'E:')
    lease = json.loads(path.read_text(encoding='utf-8'))
    released = Path(lease['release_marker'])
    while not released.exists() and exact(lease['owner']) is not None:
        time.sleep(.5)
    if released.exists():
        return
    resumed = []
    for row in reversed(lease['schedulers']):
        process = exact(row)
        if process is not None:
            process.resume()
            resumed.append(process.pid)
    with path.with_name(path.stem + '_emergency_resume.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'exact_scheduler_resumed_after_capacity_owner_exit',
            'resumed_only_scheduler_pids': resumed, 'scientific_workers_touched': 0,
            'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
