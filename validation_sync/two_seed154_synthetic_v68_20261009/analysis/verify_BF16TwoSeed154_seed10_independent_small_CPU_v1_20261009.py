"""Actual independent CPU oracle controls on an existing32-epoch small bundle; no GPU work."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def main():
    service=A/'service_owned_workflows_20261006/actual_BF16_medium2048_seed10_restart_control_v1_20261009'
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
    assert read(service/'service_execution.json')['status']=='passed'
    import joblib
    import numpy as np
    import torch
    import neural_BF16_medium2048_seed10_e64_native_v1_20261009 as native
    from neural_BF16_medium2048_seed10_independent_forward_v1_20261009 import predict_saved_tensors
    out = Path('E:/赛题五_本机临时/BF16TwoSeed154_seed10_independent_small_CPU_v1_20261009')
    assert not out.exists();out.mkdir()
    bank = Path(read(A / 'actual_BF16_medium2048_seed10_restart_location_v1_20261009.json')['output'])
    assert read(bank / 'verification.json')['status'] == 'passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    source = bank / 'small32/original.joblib'
    bundle = joblib.load(source)
    assert bundle['config']['epochs'] == 32 and bundle['config']['hidden'] == [128, 64]
    paths = [Path(__file__), A / 'neural_BF16_medium2048_seed10_independent_forward_v1_20261009.py', Path(native.__file__),
             Path(native.architecture.__file__), source, bank / 'verification.json']
    pins = {str(p): sha(p) for p in paths}
    rng = np.random.default_rng(2026100819)
    x = rng.normal(size=(10017, 63)).astype(np.float32)
    x[::17, 4] = np.nan;x[::31, 7] = np.inf;x[::37, 9] = -np.inf
    create(out / 'frozen_before_actual_controls.json', {'input_sha256': pins,
        'feature_sha256': native.array_sha(x), 'rows': len(x), 'prefix_lengths': [0, 1, 4097, 8192],
        'actual_CPU_device_required': True, 'actual_full_wide_annual_equivalence_not_claimed': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    # Scope CPU selection to this fresh, small-fixture process only.
    original_available = torch.cuda.is_available
    torch.cuda.is_available = lambda: False
    try:
        primary = native.predict_arrays(bundle, x)
        independent = predict_saved_tensors(bundle, x, device='cpu')
        assert np.array_equal(primary.view('u8'), independent.view('u8'))
        controls = []
        for n in (0, 1, 4097, 8192):
            native_prefix = native.predict_arrays(bundle, x[:n])
            oracle_prefix = predict_saved_tensors(bundle, x[:n], device='cpu')
            assert np.array_equal(native_prefix.view('u8'), primary[:n].view('u8'))
            assert np.array_equal(oracle_prefix.view('u8'), primary[:n].view('u8'))
            controls.append({'rows': n, 'native_and_independent_prefix_bits_exact': True})
    finally:
        torch.cuda.is_available = original_available
    for p, d in pins.items(): assert sha(p) == d, p
    create(out / 'verification.json', {'status': 'passed_actual_small32_CPU_saved_tensor_independent_forward_and_prefixes',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'rows': len(x), 'output_sha256': native.array_sha(primary), 'controls': controls,
        'native_network_not_called_by_independent_oracle': True,
        'nonfinite_imputation_clip_LayerNorm_SiLU_and_partial_padded_batch_checked': True,
        'new_quality_scores': 0, 'new_native_fits': 0,
        'actual_GPU_wide_and_full_annual_controls_pending': True, 'test_labels_read': False})
    print('CPU independent saved-tensor10017 rows and4 prefixes bit exact; wide annual GPU admission pending.', flush=True)


if __name__ == '__main__':main()
