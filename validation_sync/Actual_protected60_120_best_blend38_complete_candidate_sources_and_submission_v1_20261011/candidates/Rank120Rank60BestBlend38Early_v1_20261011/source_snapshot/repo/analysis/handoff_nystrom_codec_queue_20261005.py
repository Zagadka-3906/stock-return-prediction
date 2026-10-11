"""Replace only owned waiting controllers before their protocols exist."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/nystrom_codec_queue_handoff_20261005'
REGISTRY = ROOT / 'analysis/resumed_rounds_nystrom_locked_20261004.json'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    OUT.mkdir(exist_ok=True)
    records = read(REGISTRY)
    old = [r for r in records if r['round'] in (61, 62, 63)]
    assert len(old) == 3
    original_job = read(ROOT / 'analysis/nystrom_ridge_complete_scheme_run_20261004.json')
    assert "KeyError: 'hidden'" in Path(original_job['stderr']).read_text(encoding='utf-8')
    if psutil.pid_exists(original_job['pid']):
        assert not any(original_job['script'].replace('\\', '/') in item.replace('\\', '/')
                       for item in psutil.Process(original_job['pid']).cmdline())
    assert not (ROOT / 'analysis/nystrom_future_codec_recovery_run_20261005.json').exists()
    for name in ['nystrom_future_codec_recovery', 'round61_typed_codec', 'round62_typed_codec', 'round63_typed_codec']:
        assert not any((ROOT / f'analysis/run_logs/{name}_20261005.{kind}.log').exists() for kind in ('stdout', 'stderr'))
    assert not (ROOT / 'analysis/nystrom_ridge_complete_scheme_preflight_20261004/verification.json').exists()
    assert not any((ROOT / f'analysis/optimization_20261003_r{n}/protocol.json').exists() for n in (61, 62, 63))
    targets = []
    for r in old:
        parent = psutil.Process(r['pid'])
        command = parent.cmdline()
        assert any(r['script'].replace('\\', '/') in item.replace('\\', '/') for item in command)
        assert not r['script_args'] or command[-len(r['script_args']):] == r['script_args']
        children = parent.children(recursive=True)
        interpreters = [c for c in children if c.cmdline()[1:] == command[1:]]
        assert len(interpreters) == 1
        assert all(c in interpreters or c.name().lower() == 'conhost.exe' for c in children)
        targets.extend([interpreters[0], parent])
    sources = [Path(__file__), ROOT / 'analysis/nystrom_future_codec_adapter_20261005.py',
               ROOT / 'analysis/recover_nystrom_future_codec_20261005.py',
               ROOT / 'analysis/run_nystrom_codec_locked_pipeline_20261005.py', REGISTRY]
    create(OUT / 'frozen_before_handoff.json', {
        'status': 'frozen_before_owned_waiting_controller_replacement', 'at_local': datetime.now().isoformat(),
        'input_sha256': {str(p): sha(p) for p in sources}, 'original_waiting_records': old,
        'terminated_owned_pids': [p.pid for p in targets], 'scientific_protocols_and_scores_not_yet_created': True,
        'completed_fits_and_partial_checks_retained': True, 'new_model_fits': 0, 'test_labels_read': False})
    # Only the checked interpreter/launcher pairs are stopped; no broad process matching.
    for process in targets:
        process.terminate()
    _, alive = psutil.wait_procs(targets, timeout=10)
    assert not alive
    env = os.environ.copy()
    scratch = ROOT / 'tmp/nystrom_codec_queue_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    wrapper = 'analysis/run_nystrom_codec_locked_pipeline_20261005.py'
    new = []
    for record in old:
        number = record['round']
        stdout = ROOT / f'analysis/run_logs/round{number}_typed_codec_20261005.stdout.log'
        stderr = ROOT / f'analysis/run_logs/round{number}_typed_codec_20261005.stderr.log'
        with stdout.open('xb') as output, stderr.open('xb') as error:
            p = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', wrapper, str(number)],
                                 cwd=ROOT, env=env, stdout=output, stderr=error,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
        entry = {**record, 'pid': p.pid, 'script': wrapper, 'script_args': [str(number)],
                 'stdout': str(stdout), 'stderr': str(stderr), 'launched_at_local': datetime.now().isoformat(),
                 'previous_root_pid': record['pid'], 'previous_script': record['script'],
                 'status': 'waiting_for_actual_typed_codec_recovery_and_predecessor',
                 'codec_queue_handoff': str(OUT / 'frozen_before_handoff.json')}
        new.append(entry)
        for index, item in enumerate(records):
            if item['round'] == number:
                records[index] = entry
    temporary = REGISTRY.with_suffix('.handoff.tmp')
    temporary.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(REGISTRY)
    create(OUT / 'verification.json', {'status': 'passed_owned_waiting_queue_handoff',
        'at_local': datetime.now().isoformat(), 'new_controllers': new,
        'scientific_protocols_and_scores_not_yet_created': True,
        'original_waiting_logs_and_code_retained': True, 'all_new_temporary_paths_on_D': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    recovery = ROOT / 'analysis/recover_nystrom_future_codec_20261005.py'
    stdout = ROOT / 'analysis/run_logs/nystrom_future_codec_recovery_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/nystrom_future_codec_recovery_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        p = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(recovery)],
                             cwd=ROOT, env=env, stdout=output, stderr=error,
                             creationflags=subprocess.CREATE_NO_WINDOW)
    create(ROOT / 'analysis/nystrom_future_codec_recovery_run_20261005.json', {
        'pid': p.pid, 'script': str(recovery), 'script_args': [], 'stdout': str(stdout), 'stderr': str(stderr),
        'source_sha256': sha(recovery), 'launched_at_local': datetime.now().isoformat(),
        'original_failed_stderr': original_job['stderr'],
        'input_sha256': {str(s): sha(s) for s in sources[:-1]}})
    print(json.dumps({'status': 'launched_owned_typed_codec_recovery', 'recovery_pid': p.pid,
                      'queued_round_pids': {r['round']: r['pid'] for r in new}}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
