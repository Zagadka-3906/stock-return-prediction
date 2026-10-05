"""Freeze and launch the full20/4 native tasks, then complete198 quality jobs."""
from pathlib import Path
import datetime
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'streaming_robust_regression_followups_20261005'


def main():
    import train_streaming_robust_regression_bank_20261005 as bank
    from finalize_main_branch_consolidation_20261005 import owned_pair
    from predict_ready_robust_reference_scheme_20261005 import source_names
    assert not OUT.exists()
    proofs = [A / name / 'verification.json' for name in (
        'streaming_robust_regression_preflight_20261005',
        'ready_robust_reference_generator_preflight_20261005',
        'ready_robust_reference_execution_preflight_20261005',
        'streaming_robust_regression_direct_router_preflight_20261005')]
    for path in proofs:
        value = bank.read(path)
        assert value['status'].startswith('passed')
        for source, digest in value.get('source_sha256', {}).items():
            assert bank.sha(source) == digest, source
    sources = [Path(__file__), Path(bank.__file__), bank.SOURCE, Path(bank.core.shared.__file__), bank.STORAGE, *proofs,
        A / 'run_streaming_robust_regression_bank_20261005.py',
        A / 'verify_streaming_robust_regression_full_future_20261005.py',
        A / 'streaming_rank_classifier_actual_resource_recorder_20261005.py',
        A / 'locked_read_hash_cache_20261004.py', A / 'launch_ready_robust_reference_quality_20261005.py',
        A / 'streaming_robust_regression_complete_search_plan_20261005.json',
        A / 'ready_robust_reference_complete_plan_20261005.json']
    sources += [A / name for number in (87, 88) for name in source_names(number)]
    bindings = {str(path.resolve()): bank.sha(path) for path in dict.fromkeys(sources)}
    for name, status in (
        ('streaming_robust_regression_bank_run_20261005.json', 'frozen_before20_complete_actual_mature_annual_fits'),
        ('streaming_robust_regression_future_run_20261005.json', 'frozen_before4_complete_actual_mature_final_fits_and_future_X_controls')):
        bank.dump(A / name, {'status': status, 'input_sha256': bindings,
            'small_controls_not_replacing_full_actual_work': True,
            'classification_future_QA_required_before_annual_fit_admission': True,
            'test_labels_read': False, 'new_quality_scores': 0}, immutable=True)
    OUT.mkdir()
    scratch = Path(bank.read(bank.STORAGE)['temporary_directory'])
    scratch.mkdir(parents=True, exist_ok=True)
    assert scratch.resolve().drive.upper() in ('D:', 'E:')
    env = dict(os.environ)
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        env[variable] = str(scratch)
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[variable] = '2'
    jobs = []
    for kind, name in (
        ('annual', 'run_streaming_robust_regression_bank_20261005.py'),
        ('future', 'verify_streaming_robust_regression_full_future_20261005.py')):
        driver = A / name
        stdout, stderr = A / f'run_logs/streaming_robust_regression_{kind}_20261005.stdout.log', A / f'run_logs/streaming_robust_regression_{kind}_20261005.stderr.log'
        with stdout.open('xb') as output, stderr.open('xb') as error:
            process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(driver)],
                cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
        job = {'kind': kind, 'pid': process.pid, 'script': str(driver), 'script_args': [],
            'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.datetime.now().isoformat()}
        bank.dump(OUT / f'{kind}_launch.json', job, immutable=True)
        time.sleep(3)
        parent, worker = owned_pair(process.pid, driver, [])
        assert not stderr.read_bytes()
        job.update(owned_worker_pid=worker.pid, owned_worker_creation_time=worker.create_time())
        jobs.append(job)
    bank.dump(OUT / 'verification.json', {'status': 'passed_actual_owned_full_native_workflows_launched',
        'source_sha256': bindings, 'native_jobs': jobs,
        'expected_full_annual_fits': 20, 'expected_full_final_fits': 4,
        'actual_full_fits_at_launch': 0, 'actual_preflight_small32pass_fits': 16,
        'all_original_jobs_and_scheduling_policies_preserved': True,
        'test_labels_read': False, 'new_quality_scores': 0}, immutable=True)
    import launch_ready_robust_reference_quality_20261005 as quality
    quality.main()
    print(json.dumps({'status': 'actual_full_robust_native_and_complete_quality_workflows_launched',
                      'native_jobs': jobs, 'required_full_official_records': 198}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
