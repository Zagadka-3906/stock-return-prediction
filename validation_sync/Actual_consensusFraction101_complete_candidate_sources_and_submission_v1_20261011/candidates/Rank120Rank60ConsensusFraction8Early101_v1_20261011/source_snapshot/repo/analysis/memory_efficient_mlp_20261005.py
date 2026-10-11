"""Same effective batches and AdamW steps with separately validated memory layouts."""
import gc
import hashlib
import math

MODES = ('baseline', 'accumulate', 'checkpoint', 'combined')


def backward_effective_batch(model, x, y, index, objective, cfg):
    """Accumulate the sample-weighted mean; the caller steps AdamW exactly once."""
    from torch.utils.checkpoint import checkpoint
    mode = cfg.get('memory_mode', 'baseline')
    assert mode in MODES and len(index) > 0
    if mode != 'baseline':
        assert cfg['dropout'] == 0., 'Matched permutation controls require zero dropout.'
    width = cfg['micro_batch_size'] if mode in ('accumulate', 'combined') else len(index)
    assert 0 < width <= cfg['batch_size']
    total = 0.
    for offset in range(0, len(index), width):
        selected = index[offset:offset + width]
        inputs = x[selected]
        output = checkpoint(model, inputs, use_reentrant=False, preserve_rng_state=True) if mode in ('checkpoint', 'combined') else model(inputs)
        loss = objective(output.squeeze(-1), y[selected])
        (loss * (len(selected) / len(index))).backward()
        total += float(loss.detach()) * len(selected)
        del inputs, output, loss
    return total / len(index)


def fit_arrays(x, y, cfg):
    import numpy as np
    import torch
    from train_diverse_backbones_20261003 import network, log
    assert cfg['kind'] == 'mlp' and cfg.get('memory_mode', 'baseline') in MODES
    assert cfg['dropout'] == 0.
    torch.set_num_threads(8)
    torch.manual_seed(cfg['seed'])
    torch.cuda.manual_seed_all(cfg['seed'])
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    mean = np.nanmean(x, axis=0, dtype=np.float64).astype(np.float32)
    mean = np.where(np.isfinite(mean), mean, 0.)
    scale = np.nanstd(x, axis=0, dtype=np.float64).astype(np.float32)
    scale = np.where(np.isfinite(scale) & (scale > 1e-5), scale, 1.)
    clean = np.clip((np.where(np.isfinite(x), x, mean) - mean) / scale, -8., 8.).astype(np.float32)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    xt = torch.from_numpy(clean).to(device)
    if cfg['target'] == 'y_rank':
        low, high, target_scale = 0., 1., 1.
        target = y.astype(np.float32) - .5
    else:
        assert cfg['target'] == 'y_ret_1d'
        low, high = np.quantile(y, [.005, .995])
        target_scale = 20.
        target = (np.clip(y, low, high) * target_scale).astype(np.float32)
    yt = torch.from_numpy(target).to(device)
    model = network(x.shape[1], cfg).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg['learning_rate'], weight_decay=cfg['weight_decay'])
    objective = torch.nn.MSELoss() if cfg['target'] == 'y_rank' else torch.nn.HuberLoss(delta=.5)
    losses, orders, steps = [], [], 0
    for epoch in range(cfg['epochs']):
        model.train()
        order = torch.randperm(len(y), device=device)
        orders.append(hashlib.sha256(order.cpu().numpy().tobytes()).hexdigest())
        total = 0.
        for offset in range(0, len(y), cfg['batch_size']):
            index = order[offset:offset + cfg['batch_size']]
            optimizer.zero_grad(set_to_none=True)
            total += backward_effective_batch(model, xt, yt, index, objective, cfg) * len(index)
            optimizer.step()
            steps += 1
        losses.append(total / len(y))
        if epoch == 0 or (epoch + 1) % 4 == 0:
            log(f"Memory MLP {cfg['memory_mode']} {cfg['target']} epoch{epoch+1}/{cfg['epochs']} mature-training loss={losses[-1]:.8f}")
    assert steps == math.ceil(len(y) / cfg['batch_size']) * cfg['epochs']
    assert all(math.isfinite(value) for value in losses)
    state = {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}
    assert all(torch.isfinite(value).all().item() for value in state.values())
    del xt, yt, model, optimizer
    gc.collect()
    if device == 'cuda':
        torch.cuda.empty_cache()
    return {'kind': 'mlp', 'state': state, 'mean': mean, 'scale': scale,
        'target_bounds': [float(low), float(high)], 'target_scale': target_scale,
        'config': cfg, 'training_losses': losses, 'device': device,
        'memory_execution': {'memory_mode': cfg['memory_mode'], 'effective_batch_size': cfg['batch_size'],
            'micro_batch_size': cfg.get('micro_batch_size'), 'actual_optimizer_steps': steps,
            'actual_epochs': len(losses), 'actual_permutation_sha256': orders,
            'loss_is_sample_weighted_including_uneven_tail': True,
            'checkpoint_non_reentrant': True,
            'floating_point_accumulation_can_change_fitted_weights': True,
            'no_validation_early_stopping': True}}
