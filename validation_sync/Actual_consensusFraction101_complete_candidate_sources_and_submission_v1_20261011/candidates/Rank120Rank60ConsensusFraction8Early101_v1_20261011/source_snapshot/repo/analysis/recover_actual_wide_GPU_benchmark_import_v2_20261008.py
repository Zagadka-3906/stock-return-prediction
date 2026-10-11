"""Preserve the pre-training import failure and correct the actual key constant provider."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    failed = A / 'service_owned_workflows_20261006/actual_wide_GPU_precision3_resource_benchmark_20261008'
    assert not owned(read(failed / 'native_launch.json'))
    assert read(failed / 'service_execution.json')['status'] == 'failed'
    assert 'cannot import name' in (failed / 'stderr.log').read_text(encoding='utf8')
    original = A / 'benchmark_actual_wide_GPU_precision3_20261008.py'
    new = A / 'benchmark_actual_wide_GPU_precision3_v2_20261008.py'
    text = original.read_text(encoding='utf8')
    needle = 'from run import FEATURE_FILE, MANIFEST, KEYS, feature_names, fold_cutoff, to_matrix'
    assert text.count(needle) == 1
    text = text.replace(needle, 'from run import FEATURE_FILE, MANIFEST, feature_names, fold_cutoff, to_matrix\n    from optimize_training_round12 import KEYS')
    text = text.replace('wide16384_micro8192_precision3_v1', 'wide16384_micro8192_precision3_v2')
    compile(text, str(new), 'exec')
    from optimize_training_round12 import KEYS
    assert KEYS == ['ts_code', 'trade_date']
    assert not new.exists()
    new.write_text(text, encoding='utf8', newline='\n')
    paths = [Path(__file__), original, new, ROOT / 'run.py', ROOT / 'optimize_training_round12.py',
        failed / 'service_execution.json', failed / 'stderr.log',
        A / 'epoch_durable_neural_checkpoint_GPU32_preflight_v1_20261008/verification.json']
    pins = {str(p): sha(p) for p in paths}
    create(A / 'actual_wide_GPU_benchmark_import_recovery_v2_20261008.json', {
        'status': 'corrected_actual_KEYS_provider_before_any_wide_training_or_data_collection',
        'input_sha256': pins, 'original_failed_source_and_status_retained': True,
        'same_numerical_recipe_as_predeclared_V1': True, 'new_quality_scores': 0})
    row = start('actual_wide_GPU_precision3_resource_benchmark_v2_20261008', new.name, [], pins)
    create(A / 'actual_wide_GPU_precision3_hidden_launch_v2_20261008.json', {'identity': row, 'input_sha256': pins})
    print('Wide benchmark V2 launched with verified actual key provider.', flush=True)


if __name__ == '__main__':
    main()
