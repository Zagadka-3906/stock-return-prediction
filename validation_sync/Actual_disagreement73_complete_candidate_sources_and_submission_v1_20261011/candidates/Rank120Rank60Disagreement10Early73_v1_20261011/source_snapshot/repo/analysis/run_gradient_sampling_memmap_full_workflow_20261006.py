"""Wait for actual six largest-window closures, then execute all30 annual models and full future QA."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, create
    from run_dependency_queue_v3_20261006 import owned
    capacity = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity'
    while not (capacity / 'service_execution.json').exists():
        assert owned(read(capacity / 'native_launch.json')), 'Capacity worker disappeared without terminal evidence.'
        time.sleep(10)
    assert read(capacity / 'service_execution.json')['status'] == 'passed'
    while owned(read(capacity / 'native_launch.json')):
        time.sleep(.2)
    import train_gradient_sampling_memmap_bank_20261006 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    protocol = bank.freeze()
    recorder, failure = ResourceSampler(bank.OUT), None
    recorder.start()
    try:
        with LockedReadHashCache(protocol['input_sha256']):
            bank.RESOURCE = recorder
            bank.all_oof()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.RESOURCE = None
        create(bank.OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, **recorder.finish()})
        create(bank.OUT / 'training_execution_scope.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'input_sha256': protocol['input_sha256'],
            'actual30_annual_fit_scope_and_original_sources_and_shared_buffers_locked': True,
            'small_control_fits_and_reused_final_copies_excluded_from_new_fit_counts': True,
            'new_quality_scores': 0, 'test_labels_read': False})
    from verify_gradient_sampling_memmap_full_future_20261006 import main as future
    future()


if __name__ == '__main__':
    main()
