"""Training proxies only. Official evaluation remains the unchanged evaluate.py."""

def soft_capped_membership(scores,eligible,counts,absolute_tau,iterations=48):
    import torch
    assert scores.ndim==1 and eligible.ndim==2 and eligible.shape[1]==len(scores)
    tau=absolute_tau.reshape(-1,1).detach().clamp_min(1e-8)
    with torch.no_grad():
        present=eligible.any(dim=1)
        low=torch.where(eligible,scores[None,:],torch.inf).min(dim=1).values-20*tau[:,0]
        high=torch.where(eligible,scores[None,:],-torch.inf).max(dim=1).values+20*tau[:,0]
        low=torch.where(present,low,torch.zeros_like(low));high=torch.where(present,high,torch.zeros_like(high))
        for _ in range(iterations):
            middle=(low+high)/2
            p=torch.sigmoid((scores[None,:]-middle[:,None])/tau)*eligible
            above=p.sum(dim=1)>counts
            low=torch.where(above,middle,low);high=torch.where(above,high,middle)
        boundary=(low+high)/2
        p=torch.sigmoid((scores[None,:]-boundary[:,None])/tau)*eligible
        q=p*(1-p)
        w=q/q.sum(dim=1,keepdim=True).clamp_min(1e-12)
    # Implicit threshold derivative preserves the prescribed membership mass.
    correction=(w*scores[None,:]).sum(dim=1)
    boundary=boundary+correction-correction.detach()
    return torch.sigmoid((scores[None,:]-boundary[:,None])/tau)*eligible


def paired_terms(scores,day,flag_limit_up,y_rank,y_ret,common_left,common_right,tau_fraction=.1,anchors=256):
    import torch
    assert torch.isfinite(scores).all()
    days=[day==i for i in (0,1)]
    turnover_masks=torch.stack([mask & (flag_limit_up==0) for mask in days])
    return_masks=turnover_masks & torch.isfinite(y_ret)[None,:]
    masks=torch.cat([return_masks,turnover_masks])
    counts=(masks.sum(dim=1)//10).to(scores.dtype)
    counts=torch.where(masks.any(dim=1),counts.clamp_min(1),counts)
    temperatures=torch.stack([scores[mask].std(correction=0).detach().clamp_min(1e-4)*tau_fraction for mask in days])
    tau=torch.cat([temperatures,temperatures])
    p=soft_capped_membership(scores,masks,counts,tau)
    rank_correlations=[];excess=[]
    safe_return=torch.where(torch.isfinite(y_ret),y_ret,torch.zeros_like(y_ret))
    for i,mask in enumerate(days):
        values=scores[mask];target=y_rank[mask];labelled=torch.isfinite(target)
        if int(labelled.sum())>=30:
            index=torch.linspace(0,len(values)-1,min(anchors,len(values)),device=scores.device).long()
            soft_rank=torch.sigmoid((values[:,None]-values[index][None,:])/temperatures[i]).mean(dim=1)
            a=soft_rank[labelled];b=target[labelled]
            a=a-a.mean();b=b-b.mean()
            rank_correlations.append((a*b).mean()/(a.square().mean()*b.square().mean()).sqrt().clamp_min(1e-8))
        else:rank_correlations.append(scores.sum()*0)
        rmask=return_masks[i]
        e=(safe_return*p[i]).sum()/p[i].sum().clamp_min(1)-(safe_return*rmask).sum()/rmask.sum().clamp_min(1)
        excess.append(torch.where(rmask.sum()>=100,e,scores.sum()*0))
    intersection=(p[2,common_left]*p[3,common_right]).sum()
    union=(p[2].sum()+p[3].sum()-intersection).clamp_min(1e-8)
    overlap=intersection/union
    overlap=torch.where((turnover_masks.sum(dim=1)>=100).all(),overlap,scores.sum()*0)
    return {'soft_rank_correlation':torch.stack(rank_correlations).mean(),
        'soft_annual_excess':torch.stack(excess).mean()*252,
        'soft_holdings_overlap':overlap,'membership':p,'membership_mass_targets':counts,
        'turnover_eligibility':turnover_masks}


def objective(terms,turnover_weight=.3):
    return -(.4*terms['soft_rank_correlation']+.3*terms['soft_annual_excess']+turnover_weight*terms['soft_holdings_overlap'])
