"""Run all15 complete native fits after actual GPU controls and GOSS work close."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def dependencies_closed():
    from run_memory_efficient_mlp_gpu_controls_v2_20261005 import owned_live
    GPU = Path(read(A / 'memory_efficient_mlp_storage_20261005.json')['GPU_control_directory'])
    execution = GPU / 'execution_scope.json'
    if execution.exists() and read(execution)['status'] != 'passed':
        raise RuntimeError('Actual16384 GPU memory controls failed; preserve that execution before deciding a repair.')
    if not (GPU / 'verification.json').exists():
        return False
    assert read(GPU / 'verification.json')['status'] == 'passed'
    assert read(GPU / 'verification.json')['actual_matched16384_single_batch_control_fits'] == 4
    GPU_job = read(A / 'memory_efficient_mlp_gpu_recovery_v2_20261005/verification.json')['job']
    if owned_live(GPU_job):
        return False
    GOSS = read(A / 'gradient_sampling_followups_20261005/verification.json')
    bank = Path(read(A / 'gradient_sampling_storage_20261005.json')['output_directory'])
    annual = bank / 'training_execution_scope.json'
    final = A / 'gradient_sampling_future_qa_20261005/resource_summary.json'
    if not annual.exists() or owned_live(GOSS['native']):
        return False
    assert read(annual)['status'] in ('passed', 'failed')
    if read(annual)['status'] == 'passed' and not final.exists():
        return False
    if owned_live(GOSS['future']):
        return False
    if final.exists():
        assert read(final)['status'] in ('passed', 'failed')
    return True


def main():
    run_path = A / 'memory_efficient_neural_bank_run_20261005.json'
    print('Waiting for actual16384 GPU controls and complete GOSS annual/final process closure.', flush=True)
    while not run_path.exists():
        time.sleep(1)
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, digest in read(run_path)['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    while not dependencies_closed():
        time.sleep(10)
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    assert complete_round_evidence(66) is not None
    import psutil
    while psutil.virtual_memory().available < 14 * 2**30:
        time.sleep(10)
    import train_memory_efficient_neural_bank_20261005 as bank
    scratch = Path(bank.read(bank.STORAGE)['temporary_directory'])
    assert scratch.resolve().drive.upper() in ('D:', 'E:')
    scratch.mkdir(parents=True, exist_ok=True)
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    scope = FrozenProvenanceExecutionScope(bank, [Path(__file__), run_path,
        A / 'memory_efficient_mlp_20261005.py', A / 'neural16384_actual_resource_recorder_20261005.py',
        A / 'frozen_provenance_execution_scope_20261004.py', A / 'locked_read_hash_cache_20261004.py'], {
        'script':str(Path(__file__)), 'driver_source_sha256':fresh_sha(Path(__file__)),
        'actual_complete15_annual32epoch_fits_required':True, 'single_step_not_substituted_for_complete_fit':True,
        'actual_GPU_controls_and_GOSS_process_closure_required':True}, A).install()
    from neural16384_actual_resource_recorder_20261005 import ActualResourceRecorder
    recorder = ActualResourceRecorder(bank.OUT)
    original_fit = bank.engine.fit_arrays
    failure, resources = None, None
    try:
        recorder.start()
        bank.engine.fit_arrays = recorder.measured_fit(original_fit)
        bank.engine.resource_recorder = recorder
        bank.all_oof()
        assert bank.read(bank.OUT / 'oof_audit.json')['actual_annual_fits'] == 15
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.engine.fit_arrays = original_fit
        try:
            if recorder.thread is not None:
                resources = recorder.finish()
        finally:
            report = scope.close(failed=failure is not None)
        bank.OUT.mkdir(parents=True, exist_ok=True)
        with (bank.OUT / 'training_execution_scope.json').open('x', encoding='utf-8') as stream:
            json.dump({'status':'passed' if failure is None else 'failed', 'failure':failure, **report,
                'actual_resources':resources, 'full32epoch_effective32768_batch_budget_preserved':True,
                'new_quality_scores':0, 'test_labels_read':False},stream,ensure_ascii=False,indent=2)


if __name__ == '__main__':
    main()
