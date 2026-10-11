"""Run complete native scope as soon as actual maximum-size capacity is proven."""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from run_dependency_queue_v3_20261006 import owned
    service = A / 'service_owned_workflows_20261006/quantile_tree_memmap_capacity'
    def read(path):
        return json.loads(path.read_text(encoding='utf-8-sig'))
    while not (service / 'service_execution.json').exists():
        assert owned(read(service / 'native_launch.json'))
        time.sleep(10)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    while owned(read(service / 'native_launch.json')):
        time.sleep(.2)
    import train_quantile_tree_memmap_bank_20261006 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    protocol = bank.freeze()
    recorder, failure = ResourceSampler(bank.OUT), None
    recorder.start()
    old_sha = bank.sha
    try:
        with LockedReadHashCache(protocol['input_sha256']) as cache:
            bank.sha = cache.sha
            bank.RESOURCE = recorder
            bank.all_oof()
            cache.reverify()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.sha, bank.RESOURCE = old_sha, None
        bank.dump(bank.OUT / 'resource_summary.json', recorder.finish(), immutable=True)
        bank.dump(bank.OUT / 'training_execution_scope.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, 'input_sha256': protocol['input_sha256'],
            'all_original_sources_and_actual_final_native_provenance_locked_for_entire20_fit_scope': True,
            'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    from verify_quantile_tree_memmap_full_future_20261006 import main as future
    future()


if __name__ == '__main__':
    main()
