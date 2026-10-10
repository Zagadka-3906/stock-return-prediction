"""Date-local rank-gap weighted pair loss; dates never enter inference features."""
def date_groups(dates):
    import numpy as np
    d=np.asarray(dates)
    assert d.ndim==1 and len(d)>0 and np.issubdtype(d.dtype,np.integer)
    assert np.all(d[1:]>=d[:-1]), 'Training dates must be sorted'
    boundaries=np.r_[0,np.flatnonzero(d[1:]!=d[:-1])+1,len(d)]
    sizes=np.diff(boundaries)
    return np.repeat(boundaries[:-1],sizes),np.repeat(sizes,sizes)

def loss(pred,partner_pred,target,partner_target,temperature,aux_weight,delta):
    import torch
    assert temperature>0 and aux_weight>=0 and delta>0
    gap=target-partner_target
    emphasis=torch.where(torch.maximum(target,partner_target)>.4,10.,1.)
    pair=emphasis*torch.nn.functional.softplus(-gap.sign()*(pred-partner_pred)/temperature)*gap.abs()
    return pair.mean()+aux_weight*torch.nn.functional.huber_loss(pred,target,delta=delta)
