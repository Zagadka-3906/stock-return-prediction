"""Preserve the old observer and continue actual checks through queued R68."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/actual_monitor_v5_handoff_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    old_run = ROOT / 'analysis/actual_optimization_monitor_run_v4_20261005.json'
    old = read(old_run)
    parent = psutil.Process(old['pid'])
    command = parent.cmdline()
    assert any('monitor_actual_optimization_progress_v4_20261005.py' in p for p in command)
    children = parent.children(recursive=True)
    interpreters = [p for p in children if p.cmdline()[1:] == command[1:]]
    assert len(interpreters) == 1 and all(p in interpreters or p.name().lower() == 'conhost.exe' for p in children)
    script = ROOT / 'analysis/monitor_actual_optimization_progress_v5_20261005.py'
    boundary = ROOT / 'analysis/refresh_optimization_boundary_evidence_v4_20261005.py'
    inputs = dict(old['input_sha256'])
    inputs.update({str(path): sha(path) for path in (Path(__file__), script, boundary, old_run,
        ROOT / 'analysis/refresh_neural16384_cost_evidence_20261005.py', ROOT / 'analysis/refresh_nystrom_tuning_cost_evidence_20261005.py', ROOT / 'analysis/agreement_gate_preflight_v2_20261005/verification.json',
        ROOT / 'analysis/agreement_gate_round64_source_preflight_20261005/verification.json')})
    for path, digest in inputs.items():
        assert sha(path) == digest, path
    snapshots = {}
    for name in ('actual_optimization_monitor_state_20261005.json', 'ongoing_optimization_state.json', 'resume_optimization_20261004.json'):
        path = ROOT / 'analysis' / name
        data = path.read_bytes()
        json.loads(data.decode('utf-8-sig'))
        snapshots[path] = data
    create(OUT / 'frozen_before_observer_handoff.json', {
        'status': 'frozen_before_owned_observer_handoff', 'at_local': datetime.now().isoformat(),
        'input_sha256': inputs, 'old_owned_pids': [interpreters[0].pid, parent.pid],
        'scientific_controllers_and_scores_untouched': True, 'new_model_fits': 0, 'test_labels_read': False})
    for path, data in snapshots.items():
        with (OUT / ('prior_' + path.name)).open('xb') as stream:
            stream.write(data)
    targets = [interpreters[0], parent]
    for p in targets:
        p.terminate()
    _, alive = psutil.wait_procs(targets, timeout=10)
    assert not alive
    restored = []
    for path, data in snapshots.items():
        try:
            read(path)
        except json.JSONDecodeError:
            temp = path.with_suffix('.observer.tmp')
            temp.write_bytes(data)
            temp.replace(path)
            restored.append(str(path))
    stdout = ROOT / 'analysis/run_logs/actual_optimization_monitor_v5_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/actual_optimization_monitor_v5_20261005.stderr.log'
    env = os.environ.copy()
    scratch = ROOT / 'tmp/monitor_v5_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    for name in ('TMP', 'TEMP', 'TMPDIR'):
        env[name] = str(scratch)
    with stdout.open('xb') as output, stderr.open('xb') as error:
        p = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    create(ROOT / 'analysis/actual_optimization_monitor_run_v5_20261005.json', {
        'pid': p.pid, 'script': str(script), 'script_args': [], 'stdout': str(stdout), 'stderr': str(stderr),
        'launched_at_local': datetime.now().isoformat(), 'input_sha256': inputs,
        'monitors_through_actual_qualified_round': 68, 'goal_completion_not_inferred': True})
    create(OUT / 'verification.json', {'status': 'passed_owned_observer_handoff',
        'at_local': datetime.now().isoformat(), 'new_root_pid': p.pid,
        'restored_only_torn_mutable_json_snapshots': restored,
        'scientific_controllers_and_scores_untouched': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'launched_actual_monitor_v5', 'pid': p.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
