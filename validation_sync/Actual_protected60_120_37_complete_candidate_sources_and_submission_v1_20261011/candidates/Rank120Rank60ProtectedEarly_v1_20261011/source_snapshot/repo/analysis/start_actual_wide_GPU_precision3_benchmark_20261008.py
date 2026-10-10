"""Use the now free GPU for bounded resource evidence, after the actual GPU resume control."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    proof = A / 'epoch_durable_neural_checkpoint_GPU32_preflight_v1_20261008/verification.json'
    assert read(proof)['actual_small_network_GPU_equivalence_verified']
    driver = A / 'benchmark_actual_wide_GPU_precision3_20261008.py'
    pins = {str(p): sha(p) for p in [Path(__file__), driver, proof, A / 'train_diverse_backbones_20261003.py']}
    row = start('actual_wide_GPU_precision3_resource_benchmark_20261008', driver.name, [], pins)
    create(A / 'actual_wide_GPU_precision3_hidden_launch_20261008.json', {
        'status': 'started_bounded_past_only_wide_precision3_resource_benchmark', 'identity': row,
        'input_sha256': pins, 'new_quality_scores': 0, 'full_mature_annual_fit_not_claimed': True})
    print('Started actual wide-network precision3 GPU resource benchmark; artifacts on E.', flush=True)


if __name__ == '__main__':
    main()
