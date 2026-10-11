"""Add the validation-key input pin before the lazy full GPU oracle ever starts computing."""
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import pair
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    old = A / 'verify_BF16_full5_independent_GPU_v1_20261008.py'
    new = A / 'verify_BF16_full5_independent_GPU_v2_20261008.py'
    identity_path = A / 'service_owned_workflows_20261006/BF16_independent_full5_GPU_controls_v1_20261008/native_launch.json'
    row = read(identity_path);assert owned(row)
    assert owned(read(A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json'))
    assert not Path('E:/赛题五_本机临时/neural_BF16_full5_independent_controls_v1_20261008').exists()
    spy = ROOT / 'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    stack = subprocess.run([str(spy), 'dump', '--pid', str(row['owned_worker_pid'])],
        capture_output=True, text=True, encoding='utf8', check=True,
        creationflags=subprocess.CREATE_NO_WINDOW).stdout
    assert 'closed (verify_BF16_full5_independent_GPU_v1_20261008.py:' in stack, 'Replace only a lazy pre-GPU waiter.'
    text = old.read_text(encoding='utf8')
    text = text.replace('neural_BF16_full5_independent_controls_v1_20261008', 'neural_BF16_full5_independent_controls_v2_20261008')
    text = text.replace('actual_BF16_full5_independent_location_v1_20261008', 'actual_BF16_full5_independent_location_v2_20261008')
    needle = '    paths = [Path(__file__),'
    assert text.count(needle) == 1
    text = text.replace(needle, "    keys_path=A/'connected_validation_20261002/combined_fold_frame.parquet'\n" + needle)
    text = text.replace('             small_proof, bank /', '             keys_path, small_proof, bank /')
    compile(text, str(new), 'exec');assert not new.exists();new.write_text(text, encoding='utf8', newline='\n')
    proof = A / 'actual_BF16_full_oracle_key_pin_recovery_v2_20261008.json'
    pins = {str(p): sha(p) for p in [Path(__file__), old, new, identity_path]}
    create(proof, {'status': 'replaced_only_pre_GPU_lazy_oracle_to_pin_validation_keys_before_any_independent_forecast',
        'original_identity': row, 'actual_lazy_stack_before_replacement': stack, 'input_sha256': pins,
        'scientific_training_scoring_or_active_GPU_computation_stopped': 0,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    parent, worker = pair(row)
    assert all(p.pid == worker.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
    worker.terminate();worker.wait(timeout=10)
    if parent.is_running():parent.terminate();parent.wait(timeout=10)
    assert not owned(row)
    pins[str(proof)] = sha(proof)
    new_row = start('BF16_independent_full5_GPU_controls_v2_20261008', new.name, [], pins)
    create(A / 'actual_BF16_full_oracle_key_pin_hidden_launch_v2_20261008.json', {
        'status': 'started_key_pinned_lazy_full5_independent_GPU_controls', 'identity': new_row,
        'input_sha256': pins, 'original_training_worker_preserved': True, 'new_quality_scores': 0})
    print('Added exact validation-key provenance before any GPU oracle computation; training unchanged.', flush=True)


if __name__ == '__main__':main()
