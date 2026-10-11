"""Resolve the loaded key provider's real path and launch the already corrected benchmark."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import optimize_training_round12 as provider
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

assert provider.KEYS == ['ts_code', 'trade_date']
driver = A / 'benchmark_actual_wide_GPU_precision3_v2_20261008.py'
compile(driver.read_text(encoding='utf8'), str(driver), 'exec')
paths = [Path(__file__), driver, Path(provider.__file__), ROOT / 'run.py',
    A / 'recover_actual_wide_GPU_benchmark_import_v2_20261008.py',
    A / 'benchmark_actual_wide_GPU_precision3_20261008.py',
    A / 'service_owned_workflows_20261006/actual_wide_GPU_precision3_resource_benchmark_20261008/service_execution.json',
    A / 'service_owned_workflows_20261006/actual_wide_GPU_precision3_resource_benchmark_20261008/stderr.log']
assert all(p.is_file() for p in paths)
pins = {str(p): sha(p) for p in paths}
proof = A / 'actual_wide_GPU_benchmark_import_recovery_v3_20261008.json'
create(proof, {'status': 'resolved_real_loaded_KEYS_module_path_before_any_wide_training',
    'input_sha256': pins, 'actual_provider': str(Path(provider.__file__)),
    'preserved_preparation_failure': "V2 preparation incorrectly expected optimize_training_round12.py in ROOT; actual provider is analysis/optimize_training_round12.py",
    'original_failed_benchmark_retained': True, 'new_quality_scores': 0})
pins[str(proof)] = sha(proof)
row = start('actual_wide_GPU_precision3_resource_benchmark_v2_20261008', driver.name, [], pins)
create(A / 'actual_wide_GPU_precision3_hidden_launch_v2_20261008.json', {'identity': row, 'input_sha256': pins})
print('Corrected wide benchmark launched; all actual input paths checked.', flush=True)
