"""Replace only the idle owned publisher and check real historical receipt handling."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync = watcher.sync
OUT = ROOT / 'analysis/main_sync_monotone_handoff_20261005'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    receipt = sync.read(sync.OUT / 'launch_receipt.json')
    parent = psutil.Process(receipt['pid'])
    command = parent.cmdline()
    assert receipt['script'] in command
    children = parent.children(recursive=True)
    workers = [p for p in children if p.cmdline()[1:] == command[1:]]
    assert len(workers) == 1 and all(p in workers or p.name().lower() == 'conhost.exe' for p in children)
    state = sync.read(sync.OUT / 'state.json')
    assert state['status'] == 'monitoring_completed_validations' and state['pid'] == workers[0].pid
    assert state['branch'] == 'main' and not (ROOT / 'results/optimization_20261003_r62.json').exists()
    original = Path(receipt['script'])
    old_run = sync.read(sync.OUT / 'run.json')
    assert digest(original) == old_run['input_sha256'][str(original)]
    script = ROOT / 'analysis/watch_validations_main_v2_20261005.py'
    delegate = ROOT / 'analysis/sync_validated_rounds_main_20261005.py'
    OUT.mkdir(exist_ok=True)
    create(OUT / 'frozen_before_owned_handoff.json', {
        'status': 'frozen_before_owned_idle_publisher_handoff', 'at_local': sync.now(),
        'old_launch_receipt': receipt, 'old_state': state,
        'old_owned_pids': [workers[0].pid, parent.pid],
        'source_sha256': {str(p): digest(p) for p in (Path(__file__), script, delegate, original)},
        'reason': 'Historical receipts must not move main back or prevent processing future completed rounds.'})
    owned = [workers[0], parent]
    for process in owned:
        process.terminate()
    _, alive = psutil.wait_procs(owned, timeout=10)
    assert not alive
    tip = sync.git('rev-parse', 'refs/heads/main', cwd=ROOT)
    index = ROOT / '.git/index'
    index_sha = digest(index)
    working_status = sync.git('status', '--porcelain', '--untracked-files=no', cwd=ROOT)
    prior = sync.read(ROOT / 'analysis/github_main_consolidation_20261005/verification.json')['previous_validation_head']
    watcher.advance_source_index(prior)
    watcher.advance_source_index(tip)
    assert sync.git('rev-parse', 'refs/heads/main', cwd=ROOT) == tip
    assert digest(index) == index_sha
    assert sync.git('status', '--porcelain', '--untracked-files=no', cwd=ROOT) == working_status
    create(sync.OUT / 'run_v2.json', {'status': 'frozen_before_main_v2_observer_launch',
        'at_local': sync.now(), 'branch': 'main', 'previous_source_retained': str(original),
        'input_sha256': {str(p): digest(p) for p in (script, delegate, Path(__file__))},
        'actual_older_and_current_receipts_leave_newer_main_and_source_index_unchanged': True})
    scratch = ROOT / 'tmp/github_main_sync_20261005'
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    stdout = ROOT / 'analysis/run_logs/github_validation_main_v2_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/github_validation_main_v2_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    create(OUT / 'verification.json', {'status': 'passed_actual_history_receipts_and_owned_observer_handoff',
        'at_local': sync.now(), 'actual_prior_commit': prior, 'actual_current_main_commit': tip,
        'source_index_sha256_unchanged': index_sha, 'new_pid': process.pid, 'script': str(script),
        'stdout': str(stdout), 'stderr': str(stderr), 'old_owned_publisher_stopped': True,
        'old_source_receipts_and_protocol_retained': True, 'new_quality_scores': 0,
        'test_labels_read': False})
    print(json.dumps({'status': 'passed_real_receipt_controls_v2_launched', 'pid': process.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
