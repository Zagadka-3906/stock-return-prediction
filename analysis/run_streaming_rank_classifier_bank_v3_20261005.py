"""Execute every complete classifier year under original input read locks."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))


def main():
    import train_streaming_rank_classifier_bank_v3_20261005 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from streaming_rank_classifier_actual_resource_recorder_20261005 import ActualCPUResourceRecorder
    run = bank.read(A / 'streaming_rank_classifier_bank_run_v3_20261005.json')
    for filename, digest in run['input_sha256'].items():
        assert bank.sha(filename) == digest, filename
    bank.freeze()
    inputs = bank.read(bank.OUT / 'protocol.json')['input_sha256']
    original_sha = bank.sha
    cache = LockedReadHashCache(inputs)
    recorder = ActualCPUResourceRecorder(bank.OUT)
    failure, resources, report = None, None, None
    try:
        with cache:
            bank.sha = cache.sha
            bank.RESOURCE = recorder
            recorder.start()
            bank.all_oof()
            cache.reverify()
            report = {'all_frozen_inputs_full_rehash_passed': True, 'actual_source_and_data_read_locks_held': True,
                      'input_sha256': inputs}
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.sha = original_sha
        bank.RESOURCE = None
        if recorder.thread is not None:
            resources = recorder.finish()
        bank.dump(bank.OUT / 'training_execution_scope.json', {
            'status': 'passed' if failure is None else 'failed', 'failure': failure,
            'read_scope': report, 'all_hash_bindings_restored': True, 'actual_resources': resources,
            'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
