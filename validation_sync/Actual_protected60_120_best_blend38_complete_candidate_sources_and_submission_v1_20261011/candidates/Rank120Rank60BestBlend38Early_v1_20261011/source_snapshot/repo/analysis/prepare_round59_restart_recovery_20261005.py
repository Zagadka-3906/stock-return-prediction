"""Verify preserved R59 inputs and completed scores before launching recovery."""
from pathlib import Path
from datetime import datetime
import hashlib
import importlib.metadata
import json
import math
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from locked_read_hash_cache_20261004 import fresh_sha
from identical_official_score_cache_20261003 import canonical


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    out = ROOT / 'analysis/round59_restart_recovery_20261005'
    out.mkdir(exist_ok=True)
    assert not (out / 'pre_resume_verification.json').exists()
    original = ROOT / 'analysis/optimization_20261003_r59'
    registry_path = ROOT / 'analysis/resumed_rounds_nystrom_locked_20261004.json'
    registry = read(registry_path)
    old = next(r for r in registry if r['round'] == 59)
    assert not psutil.pid_exists(old['pid'])
    assert not (original / 'provenance_scope_execution.json').exists()
    frozen = read(original / 'protocol.json')['input_sha256']
    for path, digest in frozen.items():
        assert fresh_sha(path) == digest, path
    wave = read(original / 'wave247_results.json')
    assert wave['status'] == 'running' and len(wave['results']) == 41
    preserved = out / 'wave247_before_restart_resume.json'
    create(preserved, wave)
    create(out / 'previous_registry.json', registry)
    create(out / 'previous_round_state.json', read(ROOT / 'analysis/ongoing_optimization_r59_state.json'))
    inputs = {}
    for key, row in wave['results'].items():
        event = row['official_score_cache']
        source = Path(event['official_metrics_source'])
        cached = read(source)
        assert cached['metrics'] == row['metrics'], key
        assert hashlib.sha256(canonical(cached['scope'])).hexdigest() == event['cache_key'], key
        assert hashlib.sha256(canonical(cached['metrics'])).hexdigest() == cached['metrics_sha256'], key
        assert cached['scope']['versions'] == {name: importlib.metadata.version(name) for name in ('numpy', 'pandas', 'polars', 'scipy')}
        metrics = row['metrics']
        assert len(metrics) == 8 and all(math.isfinite(v) for v in metrics.values())
        score = .4 * metrics['ic_mean'] + .3 * metrics['annual_excess'] + .3 * (1 - metrics['mean_turnover'])
        assert abs(score - row['connected_final_score']) < 1e-12
        assert row['connected_final_score'] == metrics['final_score']
        assert row['causal_return_mapping']['test_labels_read'] is False
        scoring = Path(row['parallel_execution']['private_scoring_directory'])
        paths = [scoring / '测试集_X.csv', scoring / '测试集_Y.csv', ROOT / 'evaluate.py', ROOT / 'src/scoring.py', ROOT / 'analysis/identical_official_score_cache_20261003.py']
        for path in paths:
            digest = inputs.setdefault(str(path.resolve()), fresh_sha(path))
            assert cached['scope']['inputs_sha256'][path.name] == digest, path
        inputs[str(source.resolve())] = fresh_sha(source)
    helper = ROOT / 'analysis/resume_round59_after_restart_20261005.py'
    for path in (Path(__file__), helper, preserved, original / 'protocol.json', out / 'previous_registry.json', out / 'previous_round_state.json'):
        inputs[str(path.resolve())] = fresh_sha(path)
    create(out / 'pre_resume_verification.json', {
        'status': 'passed', 'at_local': datetime.now().isoformat(timespec='seconds'),
        'host_boot_at_local': datetime.fromtimestamp(psutil.boot_time()).isoformat(timespec='seconds'),
        'previous_root_pid_absent': old['pid'], 'original_scope_completion_absent': True,
        'freshly_verified_original_frozen_inputs': len(frozen),
        'completed_score_records_preserved': len(wave['results']),
        'all8_metrics_official_cache_bindings_and_formula_verified': True,
        'recovery_input_sha256': inputs, 'new_model_fits': 0, 'test_labels_read': False,
    })
    logs = ROOT / 'analysis/run_logs'
    stdout = logs / 'round59_restart_recovery_20261005.stdout.log'
    stderr = logs / 'round59_restart_recovery_20261005.stderr.log'
    with stdout.open('x') as output, stderr.open('x') as error:
        proc = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', str(helper)], cwd=ROOT,
                                stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    replacement = {**old, 'pid': proc.pid, 'previous_root_pid': old['pid'],
        'script': str(helper.relative_to(ROOT)), 'script_args': [],
        'stdout': str(stdout), 'stderr': str(stderr),
        'launched_at_local': datetime.now().isoformat(timespec='seconds'),
        'restart_recovery_preflight': str((out / 'pre_resume_verification.json').relative_to(ROOT)),
        'status': 'resuming_preserved_frozen_protocol_after_host_restart'}
    create(out / 'run.json', replacement)
    registry[registry.index(old)] = replacement
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'launched', 'pid': proc.pid, 'verified_frozen_inputs': len(frozen), 'preserved_score_records': 41}), flush=True)


if __name__ == '__main__':
    main()
