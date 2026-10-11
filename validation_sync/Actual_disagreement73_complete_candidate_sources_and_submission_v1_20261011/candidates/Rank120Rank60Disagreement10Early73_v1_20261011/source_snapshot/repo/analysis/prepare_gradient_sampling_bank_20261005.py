"""Freeze six new sampling contrasts and launch using only authorized D/E storage."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    assert not (A / 'gradient_sampling_bank_run_20261005.json').exists()
    usage = {drive: psutil.disk_usage(drive).free for drive in ('D:/', 'E:/')}
    threshold = 20 * 2**30
    drive = 'D:/' if usage['D:/'] >= threshold else 'E:/'
    assert usage[drive] >= threshold
    output = A / 'gradient_sampling_bank_20261005' if drive == 'D:/' else Path('E:/赛题五计算存储/gradient_sampling_bank_20261005')
    scratch = ROOT / 'tmp/gradient_sampling_20261005' if drive == 'D:/' else Path('E:/赛题五计算存储/tmp/gradient_sampling_20261005')
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    create(A / 'gradient_sampling_storage_20261005.json', {
        'status': 'selected_authorized_data_drive', 'output_directory': str(output),
        'temporary_directory': str(scratch), 'drive_free_bytes_at_selection': usage,
        'D_to_E_fallback_threshold_bytes': threshold, 'threshold_is_storage_policy': True,
        'project_data_on_C_forbidden': True, 'user_authorized_E_if_D_insufficient': True})
    import sys
    sys.path.insert(0, str(A))
    import train_gradient_sampling_bank_20261005 as bank
    create(A / 'gradient_sampling_complete_search_plan_20261005.json', {
        'status': 'prespecified_GOSS_native_and_complete_output_comparisons',
        'model_configurations': bank.CONFIGS, 'expected_annual_fits': 30,
        'expected_complete_final_fits': 6,
        'planned_quality_rounds': [75, 76], 'actual_previous_selection_required': {'75': 74, '76': 75},
        'planned_records': {'75': 124, '76': 138}, 'planned_waves': {'75': [304, 305, 306, 307], '76': [308, 309, 310]},
        'roles': ['membership', 'top', 'rest'], 'role_weights': [.005, .025, .075, .2],
        'standalone_replaces_existing_root_and_layers': True,
        'same_continuous_official_validation_required': '2020–2024;5635800rows;1212days;annual turnover continuous',
        'candidate_fullcoverage_and_causal_controls_required': True,
        'no_validation_early_stopping': True,
        'matched_existing_constant_leaf_controls': ['rank_lgb_constant_r300', 'return_lgb_constant_r300'],
        'GOSS_rates_are_only_deliberate_training_parameter_contrast': True,
        'historical_DART_attempts_already_covered': True,
        'native_method_reference': 'https://lightgbm.readthedocs.io/en/stable/Parameters.html#data_sample_strategy',
        'full16384_annual_attempt_closed_before_GOSS_full_fits': True,
        '14GiB_fit_reserve_is_scheduling_policy_not_hardware_boundary': True,
        'quality_generator_preflight_and_full_fits_not_yet_completed': True,
        'new_quality_scores': 0, 'test_labels_read': False,
        'global_resource_exhaustion_established': False})
    script = A / 'run_gradient_sampling_bank_20261005.py'
    sources = (Path(__file__), script, A / 'prepare_gradient_sampling_sources_20261005.py',
        A / 'train_gradient_sampling_bank_20261005.py', A / 'verify_gradient_sampling_bank_20261005.py',
        A / 'gradient_sampling_resource_recorder_20261005.py',
        A / 'gradient_sampling_storage_20261005.json', A / 'gradient_sampling_complete_search_plan_20261005.json')
    stdout = A / 'run_logs/gradient_sampling_bank_20261005.stdout.log'
    stderr = A / 'run_logs/gradient_sampling_bank_20261005.stderr.log'
    env = dict(os.environ)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[key] = '8'
    with stdout.open('xb') as out, stderr.open('xb') as err:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
    create(A / 'gradient_sampling_bank_run_20261005.json', {
        'status': 'actual_preflight_then_serialized30_annual_fits', 'pid': process.pid,
        'script': str(script), 'stdout': str(stdout), 'stderr': str(stderr),
        'at_local': datetime.now().isoformat(),
        'input_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        'planned_configurations': 6, 'planned_annual_fits': 30,
        'fulltraining_and_quality_are_separate_pending_steps': True, 'test_labels_read': False})
    print(json.dumps({'status': 'launched_actual_native_controls', 'pid': process.pid, 'output': str(output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
