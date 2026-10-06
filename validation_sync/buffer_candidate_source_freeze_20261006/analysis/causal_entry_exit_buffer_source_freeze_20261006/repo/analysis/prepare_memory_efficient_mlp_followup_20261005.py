"""Freeze the actual follow-up and launch an owned GPU-control waiter on D/E."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    receipt_path = A / 'memory_efficient_mlp_followup_launch_20261005.json'
    assert not receipt_path.exists()
    proof_path = A / 'memory_efficient_mlp_preflight_20261005/verification.json'
    proof = read(proof_path)
    assert proof['status'].startswith('passed')
    for source, expected in proof['source_sha256'].items():
        assert sha(source) == expected, source
    observation = A / 'neural16384_actual_shared_memory_observation_20261005/verification.json'
    assert read(observation)['status'].startswith('passed')
    output = A / 'memory_efficient_mlp_gpu_controls_20261005'
    scratch = ROOT / 'tmp/memory_efficient_mlp_20261005'
    if shutil.disk_usage('D:/').free < 20 * 2**30:
        output = Path('E:/赛题五计算存储/memory_efficient_mlp_gpu_controls_20261005')
        scratch = Path('E:/赛题五计算存储/tmp/memory_efficient_mlp_20261005')
    scratch.mkdir(parents=True, exist_ok=True)
    storage_path = A / 'memory_efficient_mlp_storage_20261005.json'
    create(storage_path, {'GPU_control_directory': str(output), 'temporary_directory': str(scratch),
        'D_primary_E_fallback': True, 'admission_disk_reserve_is_policy_not_physical_boundary': True})
    base = read(A / 'neural16384_full_complete_search_plan_20261005.json')['model_configurations']['rank16384_drop000_seed07_e32']
    configurations = {f'rank16384_{mode}_seed07_e32': dict(base, memory_mode=mode, micro_batch_size=4096)
        for mode in ('accumulate', 'checkpoint', 'combined')}
    plan = A / 'memory_efficient_mlp_complete_search_plan_20261005.json'
    create(plan, {'status': 'CPU_controls_passed_GPU_measurement_queued_full_native_and_quality_sources_pending',
        'model_configurations': configurations, 'original_width_and_effective_batch_and32epochs_retained': True,
        'same_seed_learning_rate_weight_decay_and_original63_features': True,
        'expected_complete_annual_fits': 15, 'expected_complete_final_fits': 3,
        'official_connected_validation_required_before_adoption': True,
        'remaining_full_native_and_quality_entrypoints_must_be_prepared': True,
        'future_label_controls_are_not_complete_annual_fits': True,
        'all_existing_actual_annual_final_jobs_and_protocols_preserved': True,
        'numerical_roundoff_is_not_assumed_to_preserve_official_score': True,
        'no_validation_early_stopping': True, 'test_labels_read': False,
        'all_years_viewed_selection_bias_uncorrected': True,
        'documentation': ['https://docs.pytorch.org/docs/2.11/checkpoint.html',
            'https://docs.pytorch.org/docs/2.11/notes/amp_examples.html#gradient-accumulation']})
    driver = A / 'run_memory_efficient_mlp_gpu_controls_20261005.py'
    run_path = A / 'memory_efficient_mlp_gpu_control_run_20261005.json'
    sources = [Path(__file__), driver, A / 'memory_efficient_mlp_20261005.py',
        A / 'train_diverse_backbones_20261003.py', A / 'neural16384_actual_resource_recorder_20261005.py',
        proof_path, observation, storage_path, plan,
        A / 'recovery_qualified_workflow_handoff_20261005/verification.json',
        A / 'neural16384_full_followup_launch_receipt_20261005.json']
    create(run_path, {'status': 'frozen_before_owned_deferred_matched_GPU_controls',
        'input_sha256': {str(path): sha(path) for path in sources},
        'matched_original_configuration': base, 'modes': ['baseline', 'accumulate', 'checkpoint', 'combined'],
        'control_epochs': 1, 'actual_control_rows': 32768,
        'full32epoch_annual_and_final_budget_not_replaced_by_single_step_controls': True,
        'wait_for_actual_original_GPU_annual_and_final_closure': True, 'only_publication_branch': 'main',
        'new_quality_scores': 0, 'test_labels_read': False})
    env = dict(os.environ)
    env.pop('CUDA_VISIBLE_DEVICES', None)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    stdout = A / 'run_logs/memory_efficient_mlp_gpu_controls_20261005.stdout.log'
    stderr = A / 'run_logs/memory_efficient_mlp_gpu_controls_20261005.stderr.log'
    with stdout.open('xb') as output_log, stderr.open('xb') as error_log:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(driver)],
            cwd=ROOT, env=env, stdout=output_log, stderr=error_log, creationflags=subprocess.CREATE_NO_WINDOW)
    job = {'pid': process.pid, 'script': str(driver), 'script_args': [],
        'stdout': str(stdout), 'stderr': str(stderr), 'at_local': datetime.now().isoformat(), 'run': str(run_path)}
    create(receipt_path, {'status': 'launched_owned_GPU_control_waiter', 'job': job,
        'source_sha256': {str(path): sha(path) for path in (driver, run_path)},
        'full_native_and_official_quality_followup_still_pending': True})
    time.sleep(5)
    assert str(driver) in psutil.Process(process.pid).cmdline()
    assert not stderr.read_text(encoding='utf-8')
    create(A / 'memory_efficient_mlp_followup_verification_20261005.json', {
        'status': 'passed_actual_CPU_controls_and_owned_deferred_GPU_job', 'job': job,
        'actual_small_CPU_control_fits_completed': proof['actual_small_control_fits'],
        'actual_gradient_and_update_controls': len(proof['gradient_controls']),
        'actual_16384_GPU_fits_completed': 0, 'actual_complete_annual_fits': 0,
        'source_sha256': {str(path): sha(path) for path in sources + [run_path, receipt_path]},
        'no_current_native_training_or_model_or_source_modified': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'GPU_control_root_pid': process.pid, 'full_native_and_quality_sources_pending': True}), flush=True)


if __name__ == '__main__':
    main()
