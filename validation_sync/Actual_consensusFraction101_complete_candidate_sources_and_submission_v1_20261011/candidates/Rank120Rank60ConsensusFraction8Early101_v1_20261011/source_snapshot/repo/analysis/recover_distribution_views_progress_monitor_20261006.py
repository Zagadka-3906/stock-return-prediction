"""Preserve the failed observer launch and submit its complete command once."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    frozen = read(A / 'distribution_views_progress_handoff_20261006/frozen_before_handoff.json')
    assert not owned(frozen['old_ownership'])
    for row in frozen['unchanged_scientific_ownership'].values():
        assert owned(row)
    previous = A / 'service_owned_workflows_20261006/progress_monitor_v23'
    assert read(previous / 'launch_result.json')['ReturnValue'] == 21
    assert not (previous / 'native_launch.json').exists()
    definition = read(previous / 'job_definition.json')
    assert 'command_line' not in definition
    for filename, digest in definition['input_sha256'].items():
        assert sha(filename) == digest
    service = A / 'service_owned_workflows_20261006/progress_monitor_v23_recovery'
    assert not service.exists()
    service.mkdir()
    path = service / 'job_definition.json'
    definition.update(name='progress_monitor_v23_recovery',
        command_line=subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'),
            '-B', '-X', 'utf8', str(A / 'run_service_owned_windows_workflow_20261006.py'), str(path)]))
    definition['input_sha256'][str(Path(__file__).resolve())] = sha(__file__)
    create(path, definition)
    create(service / 'preserved_failed_observer_attempt.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'previous_definition': str(previous / 'job_definition.json'),
        'previous_definition_sha256': sha(previous / 'job_definition.json'),
        'actual_failed_launch': read(previous / 'launch_result.json'),
        'reason': 'Incomplete observer-only job definition omitted command_line; WMI returned21 with no created process.',
        'training_scoring_and_queue_workers_preserved': True,
        'new_quality_scores': 0})
    result = launch(path, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(service / 'actual_verified_launch.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
