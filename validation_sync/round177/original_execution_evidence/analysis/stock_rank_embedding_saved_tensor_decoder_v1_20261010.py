"""Independent embedding lookup and functional saved-tensor FP32 inference."""
def predict_saved_tensors(bundle,x,device=None):
    import numpy as np,torch
    import torch.nn.functional as F
    from stock_identity_embedding_network_v1_20261010 import validate_ids
    cfg=bundle['config'];validate_ids(x)
    assert cfg['recipe']=='own_mature_stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24_v1_20261010'
    assert cfg['predict_batch_size']==8192 and bundle['target_scale']==1. and cfg['target']=='y_rank'
    device=device or ('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(8);torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    expected={'embedding.weight'}|{f'body.{4*i+j}.{k}' for i in range(len(cfg['hidden'])) for j in (0,1) for k in ('weight','bias')}|{f'body.{4*len(cfg["hidden"])}.{k}' for k in ('weight','bias')}
    assert set(bundle['state'])==expected
    tensors={k:v.detach().to(device=device,dtype=torch.float32) for k,v in bundle['state'].items()}
    assert tuple(tensors['embedding.weight'].shape)==(4651,16) and torch.count_nonzero(tensors['embedding.weight'][0]).item()==0
    parts=[]
    with torch.no_grad():
        for left in range(0,len(x),8192):
            raw=x[left:left+8192]
            numerical=np.minimum(np.maximum((np.where(np.isfinite(raw[:,:120]),raw[:,:120],bundle['mean'][:120])-bundle['mean'][:120])/bundle['scale'][:120],-8.),8.).astype(np.float32)
            inputs=np.zeros((8192,121),dtype=np.float32);inputs[:len(raw),:120]=numerical;inputs[:len(raw),120]=raw[:,120]
            inputs=torch.from_numpy(inputs).to(device)
            # Independent direct row selection; native uses an nn.Embedding module.
            value=torch.cat((inputs[:,:120],tensors['embedding.weight'].index_select(0,inputs[:,120].long())),dim=1)
            for i,width in enumerate(cfg['hidden']):
                value=F.linear(value,tensors[f'body.{4*i}.weight'],tensors[f'body.{4*i}.bias'])
                value=F.layer_norm(value,(width,),tensors[f'body.{4*i+1}.weight'],tensors[f'body.{4*i+1}.bias'],eps=1e-5)
                value=F.silu(value)
            i=4*len(cfg['hidden']);value=F.linear(value,tensors[f'body.{i}.weight'],tensors[f'body.{i}.bias'])
            parts.append(value[:,0].cpu().numpy()[:len(raw)].astype(np.float64))
    return (np.concatenate(parts) if parts else np.empty(0,dtype=np.float64))/1.
