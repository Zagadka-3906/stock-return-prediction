"""Replace only the verified idle R62 controller before its protocol exists."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/nystrom_round62_qualified_handoff_20261005'
REGISTRY = ROOT / 'analysis/resumed_rounds_nystrom_locked_20261004.json'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not (ROOT / 'analysis/optimization_20261003_r62/protocol.json').exists()
    assert not (ROOT / 'results/optimization_20261003_r61.json').exists()
    records = read(REGISTRY)
    old = next(r for r in records if r['round'] == 62)
    parent = psutil.Process(old['pid'])
    command = parent.cmdline()
    assert any(old['script'].replace('\\', '/') in p.replace('\\', '/') for p in command)
    assert command[-1] == '62'
    children = parent.children(recursive=True)
    interpreters = [p for p in children if p.cmdline()[1:] == command[1:]]
    assert len(interpreters) == 1 and all(p in interpreters or p.name().lower() == 'conhost.exe' for p in children)
    assert 'Traceback' not in Path(old['stderr']).read_text(encoding='utf-8')
    script = ROOT / 'analysis/run_nystrom_qualified_round62_20261005.py'
    OUT.mkdir(exist_ok=True)
    create(OUT / 'frozen_before_waiting_controller_handoff.json', {
        'status': 'frozen_before_owned_idle_controller_handoff', 'at_local': datetime.now().isoformat(),
        'old_record': old, 'old_owned_pids': [interpreters[0].pid, parent.pid],
        'input_sha256': {str(p): sha(p) for p in (Path(__file__), script,
            ROOT / 'analysis/run_nystrom_codec_locked_pipeline_20261005.py')},
        'reason': 'Original lazy gate sees publication before predecessor provenance scope closes.',
        'scientific_protocol_and_scores_not_yet_created': True, 'new_model_fits': 0, 'test_labels_read': False})
    targets = [interpreters[0], parent]
    for p in targets:
        p.terminate()
    _, alive = psutil.wait_procs(targets, timeout=10)
    assert not alive
    stdout = ROOT / 'analysis/run_logs/round62_qualified_typed_codec_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/round62_qualified_typed_codec_20261005.stderr.log'
    env = os.environ.copy()
    scratch = ROOT / 'tmp/round62_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    for name in ('TMP', 'TEMP', 'TMPDIR'):
        env[name] = str(scratch)
    with stdout.open('xb') as output, stderr.open('xb') as error:
        p = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    new = {**old, 'pid': p.pid, 'script': 'analysis/run_nystrom_qualified_round62_20261005.py', 'script_args': [],
           'stdout': str(stdout), 'stderr': str(stderr), 'launched_at_local': datetime.now().isoformat(),
           'previous_root_pid': old['pid'], 'previous_script': old['script'],
           'status': 'waiting_for_full_qualified_round61', 'qualified_handoff': str(OUT)}
    records = [new if r['round'] == 62 else r for r in records]
    temp = REGISTRY.with_suffix('.qualified.tmp')
    temp.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(REGISTRY)
    create(OUT / 'verification.json', {'status': 'passed_owned_idle_qualified_gate_handoff',
        'at_local': datetime.now().isoformat(), 'new_record': new, 'original_waiting_sources_andlogs_retained': True,
        'full_predecessor_scientific_and_scope_required': True,
        'scientific_algorithms_stages_and_parameters_unchanged': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'launched_round62_full_qualified_gate', 'pid': p.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
