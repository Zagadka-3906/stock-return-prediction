"""Construct every fixed annual consensus under immutable input read locks."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))


def main():
    import build_classifier_consensus_bank_20261005 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from streaming_rank_classifier_actual_resource_recorder_20261005 import ActualCPUResourceRecorder
    run = bank.read(A / 'classifier_consensus_bank_run_20261005.json')
    for filename, digest in run['input_sha256'].items():
        assert bank.sha(filename) == digest, filename
    bank.freeze()
    inputs = bank.read(bank.OUT / 'protocol.json')['input_sha256']
    original_sha = bank.sha
    cache = LockedReadHashCache(inputs)
    recorder = ActualCPUResourceRecorder(bank.OUT)
    failure, resources = None, None
    try:
        with cache:
            bank.sha = cache.sha
            recorder.context = {'stage': 'actual_virtual_annual_outputs_no_native_fits'}
            recorder.start()
            bank.all_oof()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.sha = original_sha
        if recorder.thread is not None:
            resources = recorder.finish()
        bank.dump(bank.OUT / 'construction_execution_scope.json', {
            'status': 'passed' if failure is None else 'failed', 'failure': failure,
            'all_inputs_full_rehash_and_read_locks_held': failure is None,
            'all_hash_bindings_restored': True, 'input_sha256': inputs,
            'actual_resources': resources, 'new_native_fits': 0,
            'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
