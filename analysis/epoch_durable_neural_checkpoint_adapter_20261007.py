"""Fresh adapter for epoch-boundary durable checkpoints of the unchanged original training loop."""
from pathlib import Path
import copy,hashlib,inspect,json,os

def array_sha(value):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()

def cpu_copy(node):
    import torch
    if torch.is_tensor(node):return node.detach().cpu().clone()
    if isinstance(node,dict):return {k:cpu_copy(v) for k,v in node.items()}
    if isinstance(node,list):return [cpu_copy(v) for v in node]
    if isinstance(node,tuple):return tuple(cpu_copy(v) for v in node)
    return copy.deepcopy(node)

def save_checkpoint(path,model,optimizer,losses,next_epoch,identity,device):
    import joblib,torch
    path=Path(path).resolve();assert path.drive.upper() in ('D:','E:')
    path.parent.mkdir(parents=True,exist_ok=True)
    data={'status':'durable_completed_epoch_boundary_only','identity':identity,'device':device,
      'next_epoch':next_epoch,'training_losses':list(losses),'model_state':cpu_copy(model.state_dict()),
      'optimizer_state':cpu_copy(optimizer.state_dict()),'torch_CPU_rng_state':torch.get_rng_state().clone(),
      'torch_CUDA_rng_states':torch.cuda.get_rng_state_all() if device=='cuda' else [],
      'completed_native_annual_model_not_claimed':True}
    temporary=path.with_name(path.name+'.part')
    joblib.dump(data,temporary,compress=3)
    with temporary.open('rb') as stream:os.fsync(stream.fileno())
    os.replace(temporary,path)

def identity_for(x,y,cfg,native):
    return {'training_x_sha256':array_sha(x),'training_y_sha256':array_sha(y),
      'configuration':copy.deepcopy(cfg),'original_fit_source_sha256':hashlib.sha256(inspect.getsource(native.fit_arrays).encode()).hexdigest(),
      'adapter_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def install(native):
    """Build a separate function; never overwrite the live native module or its source."""
    source=inspect.getsource(native.fit_arrays)
    declaration='def fit_arrays(x,y,cfg):';assert source.count(declaration)==1
    source=source.replace(declaration,'def fit_arrays_with_checkpoint(x,y,cfg,checkpoint_path,stop_after_epoch=None):')
    needle="    losses=[]\n    for epoch in range(cfg['epochs']):";assert source.count(needle)==1
    preamble="""    identity=IDENTITY_FOR(x,y,cfg,NATIVE)
    losses=[];start_epoch=0
    if Path(checkpoint_path).exists():
        import joblib
        checkpoint=joblib.load(checkpoint_path)
        assert checkpoint['status']=='durable_completed_epoch_boundary_only'
        assert checkpoint['identity']==identity and checkpoint['device']==device
        model.load_state_dict(checkpoint['model_state'])
        optimizer.load_state_dict(checkpoint['optimizer_state'])
        losses=checkpoint['training_losses'];start_epoch=checkpoint['next_epoch']
        assert len(losses)==start_epoch and 0<start_epoch<=cfg['epochs']
        torch.set_rng_state(checkpoint['torch_CPU_rng_state'])
        if device=='cuda':torch.cuda.set_rng_state_all(checkpoint['torch_CUDA_rng_states'])
    for epoch in range(start_epoch,cfg['epochs']):"""
    source=source.replace(needle,preamble)
    needle="        if epoch==0 or (epoch+1)%4==0:log(f\"MLP {cfg['target']} epoch{epoch+1}/{cfg['epochs']} mature-training loss={losses[-1]:.8f}\")"
    assert source.count(needle)==1
    source=source.replace(needle,needle+"\n        SAVE_CHECKPOINT(checkpoint_path,model,optimizer,losses,epoch+1,identity,device)\n        if stop_after_epoch is not None and epoch+1==stop_after_epoch:\n            return {'status':'stopped_after_durable_epoch_for_control','next_epoch':epoch+1,'training_losses':losses}")
    namespace={**vars(native),'__name__':'fresh_epoch_checkpoint_adapter','Path':Path,
      'NATIVE':native,'IDENTITY_FOR':identity_for,'SAVE_CHECKPOINT':save_checkpoint}
    exec(compile(source,str(Path(__file__)),'exec'),namespace)
    return namespace['fit_arrays_with_checkpoint'],hashlib.sha256(source.encode()).hexdigest()
