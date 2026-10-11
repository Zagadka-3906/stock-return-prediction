"""Actual CPU gradient controls and mature pilots, leaving the live GPU fit alone."""
from pathlib import Path
import copy
import hashlib
import json
import math
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'memory_efficient_mlp_preflight_20261005'
sys.path[:0] = [str(ROOT), str(A)]
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
    os.environ[name] = '8'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def gradients():
    import numpy as np
    import torch
    from train_diverse_backbones_20261003 import network
    from memory_efficient_mlp_20261005 import backward_effective_batch
    torch.set_num_threads(8)
    torch.manual_seed(20261007)
    x = torch.randn(137, 63, dtype=torch.float64)
    targets = {'y_rank': torch.linspace(-.49, .49, 137, dtype=torch.float64),
        'y_ret_1d': torch.linspace(-2., 2., 137, dtype=torch.float64)}
    base = {'kind': 'mlp', 'dropout': 0., 'hidden': [64, 32, 16], 'batch_size': 67,
        'micro_batch_size': 17, 'learning_rate': .001, 'weight_decay': .0001, 'epochs': 4, 'seed': 20261007}
    controls = []
    for target, y in targets.items():
        torch.manual_seed(20261007)
        initial = network(63, base).double()
        objective = torch.nn.MSELoss() if target == 'y_rank' else torch.nn.HuberLoss(delta=.5)
        results = {}
        for mode in ('baseline', 'accumulate', 'checkpoint', 'combined'):
            model = copy.deepcopy(initial)
            optimizer = torch.optim.AdamW(model.parameters(), lr=.001, weight_decay=.0001)
            records, batches, steps = [], [], 0
            rng = torch.Generator().manual_seed(20261007)
            for _ in range(base['epochs']):
                order = torch.randperm(len(y), generator=rng)
                for offset in range(0, len(y), base['batch_size']):
                    index = order[offset:offset + base['batch_size']]
                    optimizer.zero_grad(set_to_none=True)
                    if mode == 'baseline':
                        loss = objective(model(x[index]).squeeze(-1), y[index])
                        loss.backward()
                        value = float(loss.detach())
                    else:
                        value = backward_effective_batch(model, x, y, index, objective, dict(base, memory_mode=mode))
                    records.append([p.grad.detach().clone() for p in model.parameters()])
                    batches.append({'rows': len(index), 'loss': value})
                    optimizer.step()
                    steps += 1
            assert steps == 12 and [b['rows'] for b in batches[:3]] == [67, 67, 3]
            results[mode] = {'grads': records, 'batches': batches, 'state': model.state_dict(), 'optimizer_steps': steps}
        original = results['baseline']
        for mode in ('accumulate', 'checkpoint', 'combined'):
            actual = results[mode]
            error = max(float((a - b).abs().max()) for ag, bg in zip(actual['grads'], original['grads']) for a, b in zip(ag, bg))
            state_error = max(float((actual['state'][name] - value).abs().max()) for name, value in original['state'].items())
            assert all(torch.allclose(a, b, atol=1e-11, rtol=1e-9) for ag, bg in zip(actual['grads'], original['grads']) for a, b in zip(ag, bg)), (target, mode, error)
            assert all(torch.allclose(actual['state'][name], value, atol=1e-11, rtol=1e-9) for name, value in original['state'].items()), (target, mode, state_error)
            assert np.allclose([b['loss'] for b in actual['batches']], [b['loss'] for b in original['batches']], atol=1e-11, rtol=1e-9)
            controls.append({'target': target, 'mode': mode, 'dtype': 'float64', 'actual_optimizer_steps': 12,
                'effective_batch_sizes_including_tail': [67, 67, 3], 'accumulation_micro_batch_size': 17,
                'max_gradient_abs_difference': error, 'max_updated_state_abs_difference': state_error,
                'gradient_and_update_tolerance': {'atol': 1e-11, 'rtol': 1e-9}, 'passed': True})
    return controls


def saved_activation_controls():
    """Measure unique live tensors saved by autograd, excluding input/parameters."""
    import torch
    from train_diverse_backbones_20261003 import network
    from memory_efficient_mlp_20261005 import backward_effective_batch
    torch.manual_seed(20261007)
    x, y = torch.randn(4096, 63), torch.randn(4096)
    cfg = {'kind': 'mlp', 'dropout': 0., 'hidden': [512, 256, 128], 'batch_size': 32768, 'micro_batch_size': 1024}
    initial = network(63, cfg)
    controls = []
    for mode in ('baseline', 'accumulate', 'checkpoint', 'combined'):
        model = copy.deepcopy(initial)
        excluded = {p.untyped_storage().data_ptr() for p in model.parameters()} | {x.untyped_storage().data_ptr(), y.untyped_storage().data_ptr()}
        live, current, peak = {}, 0, 0

        class Saved:
            def __init__(self, tensor):
                nonlocal current, peak
                self.tensor = tensor
                self.pointer = tensor.untyped_storage().data_ptr()
                self.counted = self.pointer not in excluded and tensor.untyped_storage().nbytes() > 0
                if self.counted:
                    if self.pointer not in live:
                        size = tensor.untyped_storage().nbytes()
                        live[self.pointer] = [size, 0]
                        current += size
                    live[self.pointer][1] += 1
                    peak = max(peak, current)

            def __del__(self):
                nonlocal current
                if self.counted:
                    live[self.pointer][1] -= 1
                    if not live[self.pointer][1]:
                        current -= live.pop(self.pointer)[0]

        with torch.autograd.graph.saved_tensors_hooks(Saved, lambda saved: saved.tensor):
            backward_effective_batch(model, x, y, torch.arange(4096), torch.nn.MSELoss(), dict(cfg, memory_mode=mode))
        assert current == 0 and not live
        controls.append({'mode': mode, 'CPU_actual_peak_unique_autograd_saved_nonparameter_bytes': peak,
            'all_saved_control_tensors_released': True,
            'not_total_runtime_memory_or_GPU_peak': True})
    baseline = controls[0]['CPU_actual_peak_unique_autograd_saved_nonparameter_bytes']
    assert all(0 < row['CPU_actual_peak_unique_autograd_saved_nonparameter_bytes'] < baseline for row in controls[1:])
    return controls


def mature_pilots():
    import numpy as np
    import polars as pl
    import torch
    import train_diverse_backbones_20261003 as native
    from memory_efficient_mlp_20261005 import fit_arrays
    assert not torch.cuda.is_available(), 'The active wide-model GPU fit must remain isolated.'
    features, cutoff = native.feature_names(), native.fold_cutoff(2020)
    cols = native.KEYS + features + [c for c in ('y_rank', 'y_ret_1d', 'is_train', 'price_valid') if c not in features]
    lazy = pl.scan_parquet(native.FEATURE_FILE)
    base = {'kind': 'mlp', 'target': 'y_rank', 'hidden': [512, 256, 128], 'epochs': 32,
        'batch_size': 32768, 'learning_rate': .001, 'weight_decay': .0001, 'dropout': 0., 'seed': 20261007}
    past = native.training_frame(lazy, cutoff, base).select(cols).head(4096).collect()
    future = lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= cutoff)).select(cols).head(1024).collect()
    sample = pl.concat([past, future])
    poisoned = sample.with_columns([pl.when(pl.col('trade_date') >= cutoff).then(pl.lit(12345., dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c) for c in ('y_rank', 'y_ret_1d')])
    clean = native.training_frame(sample.lazy(), cutoff, base).collect()
    changed = native.training_frame(poisoned.lazy(), cutoff, base).collect()
    assert clean.equals(changed) and clean['trade_date'].max() < cutoff
    x, y = native.to_matrix(clean, features), clean['y_rank'].to_numpy()
    original = native.fit_arrays(x, y, base)
    controls = []
    original_state = original['state']
    actual_fit_count = 1
    for mode in ('baseline', 'accumulate', 'checkpoint', 'combined'):
        cfg = dict(base, memory_mode=mode, micro_batch_size=1024)
        started = time.monotonic()
        bundle = fit_arrays(x, y, cfg)
        actual_fit_count += 1
        elapsed = time.monotonic() - started
        assert len(bundle['training_losses']) == 32 and bundle['memory_execution']['actual_optimizer_steps'] == 32
        assert np.array_equal(bundle['mean'], original['mean']) and np.array_equal(bundle['scale'], original['scale'])
        for key in ('target_bounds', 'target_scale'):
            assert bundle[key] == original[key]
        error = max(float((bundle['state'][name] - value).abs().max()) for name, value in original_state.items())
        if mode in ('baseline', 'checkpoint'):
            assert all(torch.equal(bundle['state'][name], value) for name, value in original_state.items()), (mode, error)
        model = OUT / f'{mode}_512wide4096row32epoch.joblib'
        native.save_bundle(model, bundle)
        replay = native.load_bundle(model)
        pred = native.predict_arrays(bundle, x[:131])
        assert np.array_equal(pred, native.predict_arrays(replay, x[:131])) and np.isfinite(pred).all()
        assert np.array_equal(pred[:80], native.predict_arrays(native.load_bundle(model), x[:80]))
        if mode != 'baseline':
            small = dict(cfg, epochs=1)
            first = fit_arrays(x, y, small)
            second = fit_arrays(native.to_matrix(changed, features), changed['y_rank'].to_numpy(), small)
            actual_fit_count += 2
            assert all(torch.equal(first['state'][name], second['state'][name]) for name in first['state'])
            assert np.array_equal(first['mean'], second['mean']) and np.array_equal(first['scale'], second['scale'])
            assert np.array_equal(native.predict_arrays(first, x[:131]), native.predict_arrays(second, x[:131]))
        controls.append({'mode': mode, 'device': 'cpu', 'actual_rows': len(y), 'actual_hidden': cfg['hidden'],
            'actual_epochs': 32, 'effective_batch_size': 32768, 'actual_optimizer_steps': 32,
            'last_batch_loss_weighting_gradient_control_separately_passed': True,
            'model_sha256': sha(model), 'actual_CPU_fit_seconds': elapsed,
            'max_32epoch_state_abs_difference_from_original': error,
            'bit_identical_to_original_fitter': mode in ('baseline', 'checkpoint'),
            'actual_reload_and80_record_prefix_bit_identical': True,
            'actual_future_label_poisoned_past_refit_bit_identical': mode != 'baseline',
            'annual_complete_fit_not_performed': True, '16384_width_or_GPU_benchmark_not_performed': True})
    permutations = [native.load_bundle(OUT / f'{mode}_512wide4096row32epoch.joblib')['memory_execution']['actual_permutation_sha256'] for mode in ('baseline', 'accumulate', 'checkpoint', 'combined')]
    assert all(order == permutations[0] for order in permutations)
    return controls, actual_fit_count, {'year': 2020, 'mature_cutoff_exclusive': cutoff,
        'past_input_matrix_sha256': native.array_hash(x), 'past_target_sha256': native.array_hash(y),
        'all4_exact_training_permutations_matched': True, 'original63_features': features}


def main():
    assert not OUT.exists(), 'Preserve controls and use a versioned new execution for repairs.'
    OUT.mkdir()
    control_path = OUT / 'frozen_before_controls.json'
    sources = [Path(__file__), A / 'memory_efficient_mlp_20261005.py', A / 'train_diverse_backbones_20261003.py', ROOT / 'run.py', ROOT / '后续选模标准.md']
    inputs = {str(path): sha(path) for path in sources}
    with control_path.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'frozen_before_actual_CPU_controls', 'input_sha256': inputs,
            'gradient_tolerance': {'atol': 1e-11, 'rtol': 1e-9}, 'full_effective_batches_and_adam_steps_retained': True,
            'real_mature_pilot_rows': 4096, 'pilot_width': [512, 256, 128], 'pilot_epochs': 32,
            'CPU_only_controls_do_not_establish_GPU_memory_or_full_fit_boundary': True,
            'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    try:
        gradient_controls = gradients()
        activation_controls = saved_activation_controls()
        pilots, count, maturity = mature_pilots()
        assert all(sha(path) == digest for path, digest in inputs.items())
        with (OUT / 'verification.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': 'passed_actual_gradients_saved_tensors_and_mature_CPU_pilots',
                'gradient_controls': gradient_controls, 'saved_tensor_controls': activation_controls,
                'mature_pilots': pilots, 'mature_training': maturity, 'actual_small_control_fits': count,
                'source_sha256': inputs, 'actual_full_annual_fits': 0, 'actual_16384_GPU_fits': 0,
                'native_models_live_fit_and_all_frozen_sources_preserved': True,
                'microbatch_numerical_roundoff_requires_independent_full_official_quality_validation': True,
                'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
        print('Memory efficient MLP actual CPU controls passed; no full annual or16384 GPU fit claimed', flush=True)
    except BaseException as error:
        with (OUT / 'failure.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': 'failed', 'error': f'{type(error).__name__}: {error}', 'input_sha256': inputs}, stream, ensure_ascii=False, indent=2)
        raise


if __name__ == '__main__':
    main()
