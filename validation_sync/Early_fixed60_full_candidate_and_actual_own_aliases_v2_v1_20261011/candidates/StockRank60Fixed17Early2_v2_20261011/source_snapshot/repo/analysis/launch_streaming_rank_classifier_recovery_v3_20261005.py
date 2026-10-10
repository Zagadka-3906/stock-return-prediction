"""Freeze corrected V3 sources, then launch complete annual and final fits."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'streaming_rank_classifier_followups_v3_20261005'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    proof = A / 'streaming_rank_classification_preflight_v3_20261005/verification.json'
    checked = read(proof)
    assert checked['status'].startswith('passed') and checked['actual_small32epoch_fits'] == 16
    assert checked['readonly_full1694259_key_regression']['repaired_full_key_digest_matches_independent_writable_copy']
    for filename, digest in checked['input_sha256'].items():
        if Path(filename).suffix in ('.py', '.json', '.md'):
            assert sha(filename) == digest, filename
    retained = A / 'streaming_rank_classifier_recovery_v3_20261005/original_failure_retained.json'
    for filename, digest in read(retained)['input_sha256'].items():
        assert sha(filename) == digest, filename
    native = A / 'run_streaming_rank_classifier_bank_v3_20261005.py'
    future = A / 'verify_streaming_rank_classifier_full_future_v3_20261005.py'
    inputs = [Path(__file__), native, future, proof, retained,
        A / 'streaming_rank_classification_v3_20261005.py',
        A / 'train_streaming_rank_classifier_bank_v3_20261005.py',
        A / 'streaming_rank_classifier_actual_resource_recorder_20261005.py',
        A / 'streaming_rank_classifier_storage_v3_20261005.json',
        A / 'streaming_rank_classifier_complete_search_plan_20261005.json',
        A / 'locked_read_hash_cache_20261004.py']
    bindings = {str(path): sha(path) for path in inputs}
    bank_run = A / 'streaming_rank_classifier_bank_run_v3_20261005.json'
    create(bank_run, {'status': 'frozen_before20_actual_full_streamed32pass_annual_fits_V3',
        'input_sha256': bindings, 'full_fit_count': 20, 'original_terminal_attempt_preserved': True,
        'model_configurations_and_full32passes_unchanged': True,
        'pilot_fits_excluded': True, 'test_labels_read': False, 'new_quality_scores': 0})
    create(A / 'streaming_rank_classifier_future_run_v3_20261005.json', {
        'status': 'frozen_before4_actual_full_mature_final32pass_fits_V3',
        'input_sha256': {**bindings, str(bank_run): sha(bank_run)},
        'full_fit_count': 4, 'actual_full_future_rows_required': 1599600,
        'pilot_fits_excluded': True, 'test_labels_read': False, 'new_quality_scores': 0})
    OUT.mkdir()
    env = dict(os.environ, CUDA_VISIBLE_DEVICES='-1')
    scratch = read(A / 'streaming_rank_classifier_storage_v3_20261005.json')['temporary_directory']
    assert Path(scratch).drive.upper() in ('D:', 'E:')
    Path(scratch).mkdir(parents=True, exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = scratch
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '2'
    jobs = {}
    for role, script in (('native', native), ('future', future)):
        stdout = A / f'run_logs/streaming_rank_classifier_{role}_v3_20261005.stdout.log'
        stderr = A / f'run_logs/streaming_rank_classifier_{role}_v3_20261005.stderr.log'
        with stdout.open('xb') as output, stderr.open('xb') as error:
            process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
                cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
        jobs[role] = {'pid': process.pid, 'script': str(script), 'script_args': [],
            'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.datetime.now().isoformat()}
        create(OUT / f'{role}_launch.json', jobs[role])
    time.sleep(3)
    for role, job in jobs.items():
        parent = psutil.Process(job['pid'])
        assert job['script'] in parent.cmdline()
        children = [p for p in parent.children(recursive=True)
                    if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
        assert len(children) == 1 and not Path(job['stderr']).read_bytes()
        job['owned_worker_pid'] = children[0].pid
        job['owned_worker_creation_time'] = children[0].create_time()
    create(OUT / 'verification.json', {'status': 'passed_owned20_full_annual4_full_final_V3_jobs_launched',
        'at_local': datetime.datetime.now().isoformat(), **jobs,
        'full_annual_fits_required': 20, 'full_final_fits_required': 4,
        'actual_completed_full_annual_fits_at_launch': 0, 'small_control_fits_excluded': 16,
        'actual1694259_readonly_key_regression_passed': True,
        'original_failed_full32pass_attempt_retained': True,
        'prior_GPU_jobs_unchanged': True, 'only_publication_branch': 'main',
        'source_sha256': bindings, 'test_labels_read': False, 'new_quality_scores': 0})
    print(json.dumps({'status': 'passed', 'native': jobs['native'], 'future': jobs['future']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
