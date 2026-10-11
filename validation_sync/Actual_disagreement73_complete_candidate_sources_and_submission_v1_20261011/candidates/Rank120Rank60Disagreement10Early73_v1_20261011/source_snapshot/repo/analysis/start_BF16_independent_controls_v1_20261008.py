"""Start small CPU control and a lazy GPU oracle that cannot overlap the six actual fits."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    sources = [Path(__file__), A / 'neural_BF16_independent_forward_v1_20261008.py',
               A / 'verify_BF16_independent_small_CPU_v1_20261008.py',
               A / 'verify_BF16_full5_independent_GPU_v1_20261008.py',
               A / 'neural_BF16_micro8192_native_v1_20261008.py',
               A / 'actual_BF16_micro_restart_location_20261008.json']
    pins = {str(p): sha(p) for p in sources}
    jobs = [('BF16_independent_small_CPU_preflight_v1_20261008', 'verify_BF16_independent_small_CPU_v1_20261008.py'),
            ('BF16_independent_full5_GPU_controls_v1_20261008', 'verify_BF16_full5_independent_GPU_v1_20261008.py')]
    rows = {name: start(name, driver, [], pins) for name, driver in jobs}
    create(A / 'actual_BF16_independent_controls_hidden_launches_v1_20261008.json', {
        'status': 'started_CPU_small_control_and_lazily_gated_full5_GPU_independent_controls',
        'launches': rows, 'input_sha256': pins, 'new_quality_scores_by_launch': 0,
        'full_independent_GPU_work_waits_all6_actual_annual_fits': True, 'test_labels_read': False})
    print('Small CPU oracle started; full5 GPU oracle waits all6 fits without overlap.', flush=True)


if __name__ == '__main__':main()
