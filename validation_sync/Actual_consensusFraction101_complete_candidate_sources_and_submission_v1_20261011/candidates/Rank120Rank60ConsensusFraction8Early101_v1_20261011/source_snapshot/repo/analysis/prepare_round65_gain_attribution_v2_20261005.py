"""Preserve the failed auxiliary audit and launch its corrected version."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    old = ROOT / 'analysis/audit_limit_up_score_gain_round65_20261005.py'
    new = ROOT / 'analysis/audit_limit_up_score_gain_round65_v2_20261005.py'
    run = ROOT / 'analysis/round65_limit_up_gain_audit_v2_run_20261005.json'
    assert not new.exists() and not run.exists()
    text = '\n'.join(line for line in old.read_text(encoding='utf-8').splitlines()
                     if 'promote_baseline.npy' not in line) + '\n'
    text = text.replace('round65_limit_up_gain_audit_20261005', 'round65_limit_up_gain_audit_v2_20261005')
    text = text.replace('assert len(a) == len(b) == 5635800 and np.array_equal(a, promoted)',
                        'assert len(a) == len(b) == 5635800')
    text = text.replace('baseline_replayed_from_previous_selected_vector_bit_identical',
                        'baseline_vector_read_directly_from_previous_frozen_selection')
    ast.parse(text)
    new.write_text(text, encoding='utf-8', newline='')
    previous_error = ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_20261005.stderr.log'
    startup_error = ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_v2_20261005.stderr.log'
    repair = {'status': 'preserved_auxiliary_failures_and_corrected_source_v2',
              'at_local': datetime.datetime.now().isoformat(),
              'reason': 'promote_baseline.npy is an internal current-round cache; use the actual previous frozen selected_validation.npy as baseline.',
              'original_source_sha256': sha(old), 'original_failed_stderr_sha256': sha(previous_error),
              'new_source_sha256': sha(new),
              'shell_startup_failure_preserved': str(startup_error),
              'shell_startup_failure_sha256': sha(startup_error),
              'official_score_and_scientific_source_unchanged': True,
              'new_quality_scores': 0, 'test_labels_read': False}
    (ROOT / 'analysis/round65_limit_up_gain_audit_v2_repair_20261005.json').write_text(
        json.dumps(repair, ensure_ascii=False, indent=2), encoding='utf-8')
    scratch = ROOT / 'tmp/round65_limit_up_gain_audit_v2_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMP=str(scratch), TEMP=str(scratch), TMPDIR=str(scratch),
               OMP_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8', MKL_NUM_THREADS='8', POLARS_MAX_THREADS='8')
    stdout = ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_v2_repaired_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/round65_limit_up_gain_audit_v2_repaired_20261005.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        child = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(new)],
                                 cwd=ROOT, env=env, stdout=output, stderr=error,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
    receipt = {'status': 'launched_corrected_actual_training_validation_attribution',
               'at_local': datetime.datetime.now().isoformat(), 'pid': child.pid,
               'script': str(new), 'stdout': str(stdout), 'stderr': str(stderr),
               'input_sha256': {str(new): sha(new), str(Path(__file__)): sha(__file__)},
               'original_failure_preserved': True, 'new_model_fits': 0,
               'new_quality_scores': 0, 'test_labels_read': False}
    run.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
