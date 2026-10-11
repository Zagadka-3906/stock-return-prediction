"""Fresh-process restart equivalence for the new BF16 recipe, including the actual wide network."""
from pathlib import Path
import argparse
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = Path('E:/赛题五_本机临时/GPU实测_20261008/BF16_micro_restart_v1')
for key in ('TEMP', 'TMP', 'TMPDIR', 'MPLCONFIGDIR', 'TORCH_HOME', 'TORCHINDUCTOR_CACHE_DIR', 'TRITON_CACHE_DIR', 'CUDA_CACHE_PATH'):
    os.environ[key] = str(OUT / 'tmp' / key)
os.environ['CUDA_CACHE_DISABLE'] = '1'
from run_dependency_queue_v3_20261006 import read, sha, create
import neural_BF16_micro8192_native_v1_20261008 as native


def config(case):
    cfg = dict(native.CONFIG)
    if case == 'small32':
        cfg.update(hidden=[128, 64], epochs=32, batch_size=257, microbatch_size=67, dropout=.05)
    else:
        assert case == 'wide2'
        cfg.update(epochs=2)
    return cfg


def inputs(case):
    import numpy as np
    if case == 'small32':
        rng = np.random.default_rng(20261008)
        x = rng.normal(size=(1024, 63)).astype(np.float32)
        x[::7, 3] = np.nan
        return x, rng.uniform(size=1024).astype(np.float64)
    bank = Path(read(A / 'actual_wide_GPU_precision3_benchmark_location_20261008.json')['output'])
    # Nondivisible outer and microbatch lengths exercise actual weighted tail handling.
    return np.load(bank / 'past_only_features.npy')[:49153], np.load(bank / 'past_only_rank_targets.npy')[:49153]


def phase(case, mode):
    import joblib
    x, y = inputs(case)
    cfg = config(case)
    folder = OUT / case
    if mode == 'original':
        bundle = native.fit_arrays(x, y, cfg)
        joblib.dump(bundle, folder / 'original.joblib', compress=0)
    elif mode == 'first':
        stop = 7 if case == 'small32' else 1
        record = native.fit_arrays(x, y, cfg, folder / 'checkpoint.joblib', stop_after_epoch=stop)
        assert record['next_epoch'] == stop
        create(folder / 'first_actual.json', {'status': 'saved_actual_completed_epoch', 'next_epoch': stop,
                'checkpoint_sha256': sha(folder / 'checkpoint.joblib')})
    elif mode == 'resumed':
        bundle = native.fit_arrays(x, y, cfg, folder / 'checkpoint.joblib')
        joblib.dump(bundle, folder / 'resumed.joblib', compress=0)
    else:
        raise AssertionError(mode)


def main():
    import gc
    import joblib
    import numpy as np
    import psutil
    import subprocess
    import torch
    from hidden_windows_child_creation_20261006 import install as hidden
    assert torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    assert not OUT.exists()
    OUT.mkdir(parents=True)
    benchmark = Path(read(A / 'actual_wide_GPU_precision3_benchmark_location_20261008.json')['output'])
    assert read(benchmark / 'verification.json')['status'] == 'passed_actual_own_mature_subset_wide_GPU_precision3_resource_benchmark'
    paths = [Path(__file__), Path(native.__file__), Path(native.architecture.__file__),
             A / 'epoch_durable_neural_checkpoint_adapter_v2_20261007.py',
             A / 'actual_wide_GPU_precision3_benchmark_location_20261008.json',
             benchmark / 'verification.json', benchmark / 'frozen_before_actual_GPU_benchmark.json',
             benchmark / 'past_only_features.npy', benchmark / 'past_only_rank_targets.npy']
    pins = {str(p): sha(p) for p in paths}
    create(OUT / 'frozen_before_actual_controls.json', {'input_sha256': pins,
            'configurations': {c: config(c) for c in ('small32', 'wide2')},
            'wide_control_rows': 49153, 'new_recipe_not_original_FP32_batch32768': True,
            'full_annual_quality_scores_not_claimed': True, 'test_labels_read': False})
    restore = hidden()
    records = []
    try:
        for case in ('small32', 'wide2'):
            while psutil.virtual_memory().available < 11 * 2**30:
                time.sleep(10)
            folder = OUT / case
            folder.mkdir()
            phases = []
            for mode in ('original', 'first', 'resumed'):
                started = time.monotonic()
                with (folder / (mode + '.stdout.log')).open('wb') as stdout, (folder / (mode + '.stderr.log')).open('wb') as stderr:
                    result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(Path(__file__)), '--case', case, '--phase', mode],
                            stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=600, close_fds=True)
                assert result.returncode == 0, (folder / (mode + '.stderr.log')).read_text(encoding='utf8', errors='replace')
                phases.append({'phase': mode, 'elapsed_seconds': time.monotonic() - started, 'actual_child_exit': result.returncode})
            original, resumed = joblib.load(folder / 'original.joblib'), joblib.load(folder / 'resumed.joblib')
            assert original['training_losses'] == resumed['training_losses']
            assert original['recipe_identity'] == resumed['recipe_identity']
            for key in original['state']:
                assert np.array_equal(original['state'][key].numpy().view('u4'), resumed['state'][key].numpy().view('u4')), key
            for key in ('mean', 'scale'):
                assert np.array_equal(original[key].view('u4'), resumed[key].view('u4')), key
            x, y = inputs(case)
            sample = x[:10017]
            before = native.predict_arrays(original, sample)
            after = native.predict_arrays(resumed, sample)
            prefix = native.predict_arrays(resumed, sample[:min(4097, len(sample))])
            assert np.array_equal(before.view('u8'), after.view('u8'))
            assert np.array_equal(prefix.view('u8'), after[:len(prefix)].view('u8'))
            poisoned = x.copy()
            poisoned[0, 0] += 1.
            rejected = False
            try:
                native.fit_arrays(poisoned, y, config(case), folder / 'checkpoint.joblib')
            except AssertionError:
                rejected = True
            assert rejected
            record = {'case': case, 'status': 'passed_actual_fresh_process_BF16_micro_restart',
                      'configuration': config(case), 'training_rows': len(y), 'phases': phases,
                      'all_training_losses_and_all_weight_bits_exact': True,
                      'preprocessing_and_native_prediction_bits_exact': True,
                      'actual_fixed8192_cold_prefix_bits_exact': True,
                      'changed_training_input_checkpoint_rejected': True,
                      'parameter_count': sum(v.numel() for v in original['state'].values()),
                      'actual_checkpoint_sha256': sha(folder / 'checkpoint.joblib')}
            create(folder / 'verification.json', record)
            records.append(record)
            print(case + ': all losses, parameter bits, preprocessing, replay, prefix, and checkpoint rejection passed', flush=True)
            del original, resumed, x, y, poisoned, before, after, prefix
            gc.collect()
            torch.cuda.empty_cache()
        for p, d in pins.items(): assert sha(p) == d, p
        create(OUT / 'verification.json', {'status': 'passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
                'records': records, 'GPU_device_name': torch.cuda.get_device_name(0),
                'actual_new_complete_annual_fits': 0, 'new_quality_scores': 0,
                'wide32_full_annual_equivalence_not_claimed': True, 'test_labels_read': False})
        create(A / 'actual_BF16_micro_restart_location_20261008.json', {'status': 'actual_controls_passed_on_E_drive',
                'output': str(OUT), 'verification_sha256': sha(OUT / 'verification.json')})
    finally:
        create(OUT / 'actual_hidden_children.json', {'events': restore()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('small32', 'wide2'))
    parser.add_argument('--phase', choices=('original', 'first', 'resumed'))
    args = parser.parse_args()
    if args.phase:
        assert args.case
        phase(args.case, args.phase)
    else:
        main()
