"""Distinct BF16 training recipe with weighted microbatches and durable epoch restart."""
from pathlib import Path
from contextlib import nullcontext
import copy
import gc
import hashlib
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
import train_diverse_backbones_20261003 as architecture
from epoch_durable_neural_checkpoint_adapter_v2_20261007 import array_sha, cpu_copy

CONFIG = {'kind': 'mlp', 'target': 'y_rank', 'hidden': [2048, 1024, 512],
          'epochs': 64, 'batch_size': 32768, 'microbatch_size': 8192,
          'predict_batch_size': 8192, 'learning_rate': .0005,
          'weight_decay': .0001, 'dropout': 0., 'seed': 20261009,
          'loss': 'TopWeightedHuber', 'huber_delta': .1, 'top_rank_threshold': .9, 'top_sample_weight': 5.,
          'training_precision': 'BF16_autocast_FP32_loss_and_AdamW',
          'recipe': 'own_mature_BF16_medium2048_topweightedhuber010_seed09_e64_weighted_accum_v1_20261009'}


def identity_for(x, y, cfg):
    return {'training_x_sha256': array_sha(x), 'training_y_sha256': array_sha(y),
            'configuration': copy.deepcopy(cfg),
            'native_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'network_source_sha256': hashlib.sha256(Path(architecture.__file__).read_bytes()).hexdigest()}


def write_checkpoint(path, model, optimizer, losses, epoch, identity, device_name):
    import joblib
    import torch
    path = Path(path).resolve()
    assert path.drive.upper() in ('D:', 'E:')
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {'status': 'durable_completed_BF16_micro_epoch_boundary_only',
            'identity': identity, 'device_name': device_name,
            'torch_version': torch.__version__, 'next_epoch': epoch,
            'training_losses': list(losses), 'model_state': cpu_copy(model.state_dict()),
            'optimizer_state': cpu_copy(optimizer.state_dict()),
            'torch_CPU_rng_state': torch.get_rng_state().clone(),
            'torch_CUDA_rng_states': torch.cuda.get_rng_state_all()}
    temporary = path.with_name(path.name + '.part')
    joblib.dump(data, temporary, compress=0)
    with temporary.open('r+b') as stream:
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    del data
    gc.collect()


def fit_arrays(x, y, cfg, checkpoint_path=None, stop_after_epoch=None):
    import joblib
    import numpy as np
    import torch
    assert torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    assert cfg['target'] == 'y_rank' and cfg['training_precision'] == CONFIG['training_precision']
    assert cfg['loss']=='TopWeightedHuber' and cfg['huber_delta']==.1 and cfg['top_rank_threshold']==.9 and cfg['top_sample_weight']==5.
    assert len(x) == len(y) and len(y) > 0 and np.isfinite(y).all()
    assert 0 < cfg['microbatch_size'] <= cfg['batch_size']
    identity = identity_for(x, y, cfg)
    checkpoint = None
    if checkpoint_path is not None and Path(checkpoint_path).exists():
        checkpoint = joblib.load(checkpoint_path)
        assert checkpoint['status'] == 'durable_completed_BF16_micro_epoch_boundary_only'
        assert checkpoint['identity'] == identity
        assert checkpoint['device_name'] == torch.cuda.get_device_name(0)
        assert checkpoint['torch_version'] == torch.__version__
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
    target = y.astype(np.float32) - .5
    xt, yt = torch.from_numpy(clean).cuda(), torch.from_numpy(target).cuda()
    del clean, target
    model = architecture.network(x.shape[1], cfg).cuda()
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg['learning_rate'], weight_decay=cfg['weight_decay'])
    losses, start_epoch = [], 0
    if checkpoint is not None:
        model.load_state_dict(checkpoint['model_state'])
        optimizer.load_state_dict(checkpoint['optimizer_state'])
        losses = checkpoint['training_losses']
        start_epoch = checkpoint['next_epoch']
        assert len(losses) == start_epoch and 0 < start_epoch <= cfg['epochs']
        torch.set_rng_state(checkpoint['torch_CPU_rng_state'])
        torch.cuda.set_rng_state_all(checkpoint['torch_CUDA_rng_states'])
        del checkpoint
        gc.collect()
    epoch_seconds = []
    for epoch in range(start_epoch, cfg['epochs']):
        started = time.monotonic()
        model.train()
        order = torch.randperm(len(y), device='cuda')
        sum_loss = 0.
        for offset in range(0, len(y), cfg['batch_size']):
            index = order[offset:offset + cfg['batch_size']]
            optimizer.zero_grad(set_to_none=True)
            batch_weights=1.+(cfg['top_sample_weight']-1.)*(yt[index]>=cfg['top_rank_threshold']-.5).float()
            denominator=batch_weights.sum()
            for left in range(0, len(index), cfg['microbatch_size']):
                part = index[left:left + cfg['microbatch_size']]
                with torch.autocast('cuda', dtype=torch.bfloat16):
                    pred = model(xt[part]).squeeze(-1)
                loss = weighted_huber_loss(pred.float(),yt[part],denominator)
                assert torch.isfinite(loss).item(), ('nonfinite_training_loss', epoch, offset, left)
                loss.backward()
                sum_loss += float(loss.detach()) * len(index)
            optimizer.step()
        losses.append(sum_loss / len(y))
        assert all(torch.isfinite(p).all().item() for p in model.parameters())
        torch.cuda.synchronize()
        epoch_seconds.append(time.monotonic() - started)
        print(f"BF16 micro8192 epoch {epoch+1}/{cfg['epochs']} loss={losses[-1]:.12g} fit_seconds={epoch_seconds[-1]:.3f}", flush=True)
        if checkpoint_path is not None:
            save_started = time.monotonic()
            write_checkpoint(checkpoint_path, model, optimizer, losses, epoch + 1, identity, torch.cuda.get_device_name(0))
            print(f"durable_epoch={epoch+1} checkpoint_seconds={time.monotonic()-save_started:.3f}", flush=True)
        if stop_after_epoch is not None and epoch + 1 == stop_after_epoch:
            assert checkpoint_path is not None
            return {'status': 'stopped_after_durable_BF16_micro_epoch_for_control',
                    'next_epoch': epoch + 1, 'training_losses': losses}
    state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    del xt, yt, model, optimizer
    gc.collect()
    torch.cuda.empty_cache()
    return {'kind': 'mlp', 'state': state, 'mean': mean, 'scale': scale,
            'target_bounds': [0., 1.], 'target_scale': 1., 'config': dict(cfg),
            'training_losses': losses, 'device': 'cuda', 'recipe_identity': identity,
            'training_epoch_seconds_this_process': epoch_seconds}


def predict_arrays(bundle, x):
    """Fixed 8192-row FP32 inference; padding permits unchanged earlier row predictions."""
    import numpy as np
    import torch
    assert bundle['config']['recipe'] == CONFIG['recipe']
    torch.set_num_threads(8)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = architecture.network(x.shape[1], bundle['config']).to(device)
    model.load_state_dict(bundle['state'])
    model.eval()
    batch = bundle['config']['predict_batch_size']
    parts = []
    with torch.no_grad():
        for left in range(0, len(x), batch):
            raw = x[left:left + batch]
            clean = np.clip((np.where(np.isfinite(raw), raw, bundle['mean']) - bundle['mean']) / bundle['scale'], -8., 8.).astype(np.float32)
            if len(clean) < batch:
                padded = np.zeros((batch, x.shape[1]), dtype=np.float32)
                padded[:len(clean)] = clean
                clean = padded
            values = model(torch.from_numpy(clean).to(device)).squeeze(-1).cpu().numpy()[:len(raw)]
            parts.append(values.astype(np.float64))
    del model
    gc.collect()
    if device == 'cuda': torch.cuda.empty_cache()
    return np.concatenate(parts) if parts else np.empty(0, dtype=np.float64)


def weighted_huber_loss(pred,target,denominator=None):
    import torch
    pred=pred.float();target=target.float()
    weights=1.+4.*(target>=.4).float()
    total=weights.sum() if denominator is None else denominator
    assert total>0
    return (torch.nn.functional.huber_loss(pred,target,delta=.1,reduction='none')*weights).sum()/total
