"""Independent saved-tensor Linear/LayerNorm/SiLU inference, without constructing a native network."""
import gc
import os
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'


def predict_saved_tensors(bundle, x, device=None):
    import numpy as np
    import torch
    import torch.nn.functional as functional
    config = bundle['config']
    assert config['recipe'] == 'own_mature_BF16_medium2048_forward20huber050_seed09_e64_weighted_accum_v1_20261009'
    assert config['training_precision'] == 'BF16_autocast_FP32_loss_and_AdamW'
    assert config['predict_batch_size'] == 8192 and bundle['kind'] == 'mlp'
    assert x.ndim == 2 and x.shape[1] == len(bundle['mean']) == len(bundle['scale'])
    device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
    assert device in ('cuda', 'cpu')
    torch.set_num_threads(8)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    state = bundle['state']
    hidden = config['hidden']
    expected = {f'{4*i+offset}.{part}' for i in range(len(hidden)) for offset in (0, 1) for part in ('weight', 'bias')}
    expected |= {f'{4*len(hidden)}.{part}' for part in ('weight', 'bias')}
    assert set(state) == expected
    for i, width in enumerate(hidden):
        previous = x.shape[1] if i == 0 else hidden[i-1]
        assert tuple(state[f'{4*i}.weight'].shape) == (width, previous)
        assert tuple(state[f'{4*i+1}.weight'].shape) == (width,)
    assert tuple(state[f'{4*len(hidden)}.weight'].shape) == (1, hidden[-1])
    tensors = {key: value.detach().to(device=device, dtype=torch.float32) for key, value in state.items()}
    parts = []
    with torch.no_grad():
        for left in range(0, len(x), 8192):
            raw = x[left:left+8192]
            finite = np.where(np.isfinite(raw), raw, bundle['mean'])
            normalized = (finite - bundle['mean']) / bundle['scale']
            clean = np.minimum(np.maximum(normalized, -8.), 8.).astype(np.float32)
            inputs = np.zeros((8192, x.shape[1]), dtype=np.float32)
            inputs[:len(raw)] = clean
            value = torch.from_numpy(inputs).to(device)
            for i, width in enumerate(hidden):
                value = functional.linear(value, tensors[f'{4*i}.weight'], tensors[f'{4*i}.bias'])
                value = functional.layer_norm(value, (width,), tensors[f'{4*i+1}.weight'], tensors[f'{4*i+1}.bias'], eps=1e-5)
                value = functional.silu(value)
            value = functional.linear(value, tensors[f'{4*len(hidden)}.weight'], tensors[f'{4*len(hidden)}.bias'])
            parts.append(value[:, 0].cpu().numpy()[:len(raw)].astype(np.float64))
    tensors.clear()
    if len(x): del value
    gc.collect()
    if device == 'cuda': torch.cuda.empty_cache()
    assert config['target']=='y_ret_20mean' and config['return_target_scale']==100. and bundle['target_scale']==100.
    return (np.concatenate(parts) if parts else np.empty(0,dtype=np.float64))/100.

