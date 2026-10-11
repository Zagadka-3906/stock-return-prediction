"""Launch an actual recovered R66 after verifying its old handle is terminal."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    registry_path = A / 'resumed_rounds_nystrom_locked_20261004.json'
    registry = read(registry_path)
    old = next(row for row in registry if row['round'] == 66)
    assert not psutil.pid_exists(old['pid'])
    folder = A / 'optimization_20261003_r66'
    failed = read(folder / 'provenance_scope_execution.json')
    assert failed['status'] == 'failed' and failed['failure'].startswith('FileNotFoundError:')
    assert not list(folder.glob('wave*_results.json'))
    proof = A / 'standalone_root_source_adapter_preflight_20261005/verification.json'
    checked = read(proof)
    assert checked['status'] == 'passed_source_resolution_only' and len(checked['checks']) == 10
    for source, expected in checked['source_sha256'].items():
        assert sha(source) == expected, source
    for number in range(63, 75):
        protocol = A / f'optimization_20261003_r{number}/protocol.json'
        if protocol.exists():
            assert str(registry_path) not in read(protocol)['input_sha256']
    script = A / 'resume_round66_root_source_recovery_20261005.py'
    inputs = [Path(__file__), script, A / 'standalone_root_source_adapter_20261005.py',
              A / 'round66_recovery_execution_scope_20261005.py', proof,
              folder / 'protocol.json', folder / 'provenance_scope_execution.json', Path(old['stderr'])]
    run_path = A / 'round66_root_source_recovery_run_20261005.json'
    with run_path.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'frozen_before_actual_R66_root_source_recovery',
                   'input_sha256': {str(p): sha(p) for p in inputs}, 'original_run': old,
                   'original_failed_scope_and_protocol_preserved': True,
                   'expected_scored_records': read(folder / 'protocol.json')['expected_scored_records'],
                   'zero_official_scores_at_restart': True,
                   'downstream_qualification_bridge_still_required': True,
                   'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    scratch = ROOT / 'tmp/round66_root_source_recovery_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMP=str(scratch), TEMP=str(scratch), TMPDIR=str(scratch),
               OMP_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8', MKL_NUM_THREADS='8', POLARS_MAX_THREADS='8')
    stdout, stderr = A / 'run_logs/round66_root_source_recovery_20261005.stdout.log', A / 'run_logs/round66_root_source_recovery_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    job = {**old, 'pid': process.pid, 'script': str(script), 'script_args': [],
           'stdout': str(stdout), 'stderr': str(stderr), 'status': 'actual_recovery_running',
           'prior_original_root_pid': old['pid'], 'at_local': datetime.datetime.now().isoformat()}
    registry = [job if row['round'] == 66 else row for row in registry]
    temporary = registry_path.with_suffix('.r66_recovery.tmp')
    temporary.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(registry_path)
    with (A / 'round66_root_source_recovery_launch_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump(job, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'actual_R66_recovery_launched', 'pid': process.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
