"""Defer matched real16384-width GPU controls until the current GPU work closes."""
from pathlib import Path
from datetime import datetime
import gc
import hashlib
import json
import os
import sys
import time
import traceback
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
RUN = A / 'memory_efficient_mlp_gpu_control_run_v2_20261005.json'
STATE = A / 'memory_efficient_mlp_gpu_control_state_v2_20261005.json'
sys.path[:0] = [str(ROOT), str(A)]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def owned_live(job):
    try:
        process = psutil.Process(job['pid'])
        command = process.cmdline()
    except psutil.NoSuchProcess:
        return False
    if job['script'] not in command:
        return False  # A reused PID belongs to a different task.
    return not job.get('script_args') or command[-len(job['script_args']):] == job['script_args']


def original_gpu_work_closed():
    annual_job = read(A / 'recovery_qualified_workflow_handoff_20261005/verification.json')['jobs'][0]
    final_job = read(A / 'neural16384_full_followup_launch_receipt_20261005.json')['future']
    annual = A / 'neural16384_full_bank_20261005/training_execution_scope.json'
    final = A / 'neural16384_full_future_qa_20261005/resource_summary.json'
    if not annual.exists() or owned_live(annual_job):
        return False
    status = read(annual)['status']
    assert status in ('passed', 'failed')
    if status == 'passed' and not final.exists():
        return False
    if owned_live(final_job):
        return False
    if final.exists():
        assert read(final)['status'] in ('passed', 'failed')
    return True


def main():
    run = read(RUN)
    for source, expected in run['input_sha256'].items():
        assert sha(source) == expected, source
    storage = read(A / 'memory_efficient_mlp_storage_20261005.json')
    output, scratch = Path(storage['GPU_control_directory']), Path(storage['temporary_directory'])
    assert output.resolve().drive.upper() in ('D:', 'E:') and scratch.resolve().drive.upper() in ('D:', 'E:')
    scratch.mkdir(parents=True, exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        os.environ[key] = '8'

    def state(stage, **extra):
        value = {'status': 'running', 'stage': stage, 'pid': os.getpid(), 'at_local': datetime.now().isoformat(),
            'native_original32epoch_training_untouched': True, 'new_quality_scores': 0,
            'test_labels_read': False, **extra}
        temporary = STATE.with_suffix('.tmp')
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(STATE)
        print(json.dumps(value, ensure_ascii=False), flush=True)

    state('waiting_for_actual_original_GPU_annual_and_final_process_closure_then14GiB_host_reserve')
    while not original_gpu_work_closed():
        time.sleep(10)
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    assert not output.exists(), 'Preserve prior execution and use a new version.'
    output.mkdir(parents=True)
    import numpy as np
    import torch
    import polars as pl
    import train_diverse_backbones_20261003 as native
    from memory_efficient_mlp_20261005 import fit_arrays
    from neural16384_actual_resource_recorder_20261005 import ActualResourceRecorder
    assert torch.cuda.is_available()
    proof = read(A / 'memory_efficient_mlp_preflight_20261005/verification.json')
    assert proof['status'].startswith('passed')
    cfg = dict(run['matched_original_configuration'], epochs=1, micro_batch_size=4096)
    features, cutoff = native.feature_names(), native.fold_cutoff(2020)
    frame = native.training_frame(pl.scan_parquet(native.FEATURE_FILE), cutoff, cfg).select(native.KEYS + features + ['y_rank']).head(32768).collect()
    assert len(frame) == 32768 and frame['trade_date'].max() < cutoff
    x, y = native.to_matrix(frame, features), frame['y_rank'].to_numpy()
    sources = [Path(__file__), RUN, A / 'memory_efficient_mlp_20261005.py', A / 'train_diverse_backbones_20261003.py',
        A / 'memory_efficient_mlp_preflight_20261005/verification.json', native.FEATURE_FILE, native.MANIFEST,
        A / 'neural16384_full_bank_20261005/training_execution_scope.json']
    final_closure = A / 'neural16384_full_future_qa_20261005/resource_summary.json'
    if final_closure.exists():
        sources.append(final_closure)
    inputs = {str(path): sha(path) for path in sources}
    create(output / 'protocol.json', {'status': 'frozen_before_actual_matched16384_GPU_single_batch_controls',
        'input_sha256': inputs, 'configuration': cfg, 'modes': list(run['modes']),
        'training_rows': 32768, 'effective_batch_size': 32768, 'actual_epochs_per_control': 1,
        'single_step_is_not_complete_annual_training': True, 'mature_cutoff_exclusive': cutoff,
        'actual_input_matrix_sha256': native.array_hash(x), 'actual_target_sha256': native.array_hash(y),
        'full32epoch_annual_and_final_models_and_official_quality_still_required': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    recorder = ActualResourceRecorder(output)
    checks, failure, resources = [], None, None
    baseline_state = None
    try:
        recorder.start()
        for mode in run['modes']:
            state('actual16384_GPU_single_batch_control', mode=mode)
            current = dict(cfg, memory_mode=mode)
            recorder.context = {'stage': 'actual16384_single_step_memory_layout_control', 'memory_mode': mode}
            fitter = native.fit_arrays if mode == 'baseline' else fit_arrays
            bundle = recorder.measured_fit(fitter)(x, y, current)
            assert len(bundle['training_losses']) == 1 and all(torch.isfinite(value).all().item() for value in bundle['state'].values())
            if mode == 'baseline':
                baseline_state = {name: value.clone() for name, value in bundle['state'].items()}
            difference = max(float((bundle['state'][name] - value).abs().max()) for name, value in baseline_state.items())
            model = output / f'{mode}_actual16384_one_step.joblib'
            native.save_bundle(model, bundle)
            raw = native.predict_arrays(bundle, x[:131])
            assert np.array_equal(raw, native.predict_arrays(native.load_bundle(model), x[:131]))
            assert np.array_equal(raw[:80], native.predict_arrays(native.load_bundle(model), x[:80]))
            checks.append({'mode': mode, 'model_sha256': sha(model), 'actual_rows': 32768,
                'actual_hidden': cfg['hidden'], 'actual_one_epoch_one_effective_AdamW_step': True,
                'actual_model_reload_and80_record_prefix_bit_identical': True,
                'max_one_step_state_abs_difference_from_matched_baseline': difference,
                'GPU_timing_and_allocator_peak_are_control_scope_only': True,
                'complete_annual_fit_and_official_quality_not_performed': True})
            del bundle, raw
            gc.collect()
            torch.cuda.empty_cache()
        assert all(sha(path) == digest for path, digest in inputs.items())
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        state('failed', status='failed', failure=failure, traceback=traceback.format_exc())
        raise
    finally:
        if recorder.thread is not None:
            resources = recorder.finish()
        create(output / 'execution_scope.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'input_sha256': inputs, 'actual_resources': resources,
            'completed_controls': checks, 'new_quality_scores': 0, 'test_labels_read': False,
            'no_global_physical_boundary_or_full_training_completion_claimed': True})
    create(output / 'verification.json', {'status': 'passed', 'checks': checks,
        'actual_matched16384_single_batch_control_fits': len(checks), 'actual_full_annual_fits': 0,
        'input_sha256': inputs, 'GPU_single_step_measurement_does_not_establish_full_fit_or_best_model': True,
        'full_32epoch_15_annual3_final_and_official_quality_followup_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    state('completed_actual16384_GPU_controls_full_annual_official_validation_pending', status='completed')


if __name__ == '__main__':
    main()
