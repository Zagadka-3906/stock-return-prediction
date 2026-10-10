"""Actual gradient, label-independent holdings and mature-pair training controls."""
from pathlib import Path
import hashlib
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
OUT=ROOT/'analysis/portfolio_surrogate_preflight_20261004'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
def create(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)

def main():
    import gc
    import numpy as np
    import polars as pl
    import psutil
    import train_diverse_backbones_20261003 as engine
    import portfolio_surrogate_loss_20261004 as loss
    import torch
    OUT.mkdir(exist_ok=True);assert not (OUT/'frozen_before_controls.json').exists()
    base=ROOT/'analysis/neural_regularization_bank_20261003/rank512_drop000_e32'
    info=read(base/'info_2020.json');model=base/'model_2020.joblib'
    assert sha(model)==info['model_sha256'] and info['status']=='passed'
    sources=[Path(__file__),Path(loss.__file__),Path(engine.__file__),model,base/'info_2020.json',engine.FEATURE_FILE,engine.MANIFEST,
        ROOT/'analysis/neural_regularization_bank_20261003/protocol.json',ROOT/'evaluate.py',ROOT/'后续选模标准.md']
    hashes={str(p.resolve()):sha(p) for p in sources}
    create(OUT/'frozen_before_controls.json',{'status':'frozen_training_proxy_implementation_controls',
        'input_sha256':hashes,'warm_start':'Past-trained512-width no-dropout fold2020 checkpoint; reused unmodified',
        'soft_rank':'Mean sigmoid empirical CDF using up to256 fixed row-order anchors; proxy, not exact Spearman',
        'membership':'Sigmoid caps with48-step threshold root andimplicit gradient; proxy, not exact top-k',
        'turnover':'Continuous overlap; holdings eligibility independent of label availability',
        'relative_temperature':.1,'prototype_learning_rate':.0001,'gradient_clip_norm':1.,
        'prototype_steps_per_variant':2,'variants_turnover_weights':[0.,.3],
        'normalizer_andtarget_scale_reused_from_mature_control':True,
        'no_exact_official_score_claim':True,'new_quality_scores':0,'test_labels_read':False})
    # Check the implicit cap gradient against numerical derivatives at fixed tau.
    s=torch.linspace(-.5,.5,7,dtype=torch.float64,requires_grad=True)
    eligible=torch.ones((1,7),dtype=torch.bool);mass=torch.tensor([3.],dtype=torch.float64);tau=torch.tensor([.07],dtype=torch.float64)
    weight=torch.tensor([.2,-.1,.3,.7,-.4,.8,.1],dtype=torch.float64)
    p=loss.soft_capped_membership(s,eligible,mass,tau);value=(p[0]*weight).sum()
    actual=torch.autograd.grad(value,s)[0];numerical=[];eps=1e-5
    for i in range(7):
        plus=s.detach().clone();minus=s.detach().clone();plus[i]+=eps;minus[i]-=eps
        numerical.append(float(((loss.soft_capped_membership(plus,eligible,mass,tau)[0]*weight).sum()-(loss.soft_capped_membership(minus,eligible,mass,tau)[0]*weight).sum())/(2*eps)))
    assert np.allclose(actual.numpy(),numerical,rtol=2e-6,atol=2e-8)
    assert abs(float(p.sum().detach())-3)<1e-10 and abs(float(actual.sum()))<1e-10
    features=engine.feature_names();cutoff=engine.fold_cutoff(2020);lazy=pl.scan_parquet(engine.FEATURE_FILE)
    available=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)&pl.col('price_valid'))
    dates=available.select('trade_date').unique().sort('trade_date').head(2).collect()['trade_date'].to_list()
    columns=list(dict.fromkeys(engine.KEYS+features+['y_rank','y_ret_1d','flag_limit_up','is_train','price_valid']))
    frame=available.filter(pl.col('trade_date').is_in(dates)).select(columns).sort('trade_date','ts_code').collect()
    future=lazy.filter(pl.col('is_train')&(pl.col('trade_date')>=cutoff)&pl.col('price_valid')).select(columns).head(16).collect()
    combined=pl.concat([frame,future]);poison=combined.with_columns([
        pl.when(pl.col('trade_date')>=cutoff).then(pl.lit(12345.,dtype=combined.schema[c])).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
    assert combined.filter(pl.col('trade_date')<cutoff).equals(poison.filter(pl.col('trade_date')<cutoff))
    keys=OUT/'mature_pair_keys.parquet';frame.select(engine.KEYS).write_parquet(keys)
    bundle=engine.load_bundle(model);x=engine.to_matrix(frame,features)
    clean=np.clip((np.where(np.isfinite(x),x,bundle['mean'])-bundle['mean'])/bundle['scale'],-8,8).astype(np.float32)
    date=frame['trade_date'].to_numpy();day=(date==dates[1]).astype(np.int64)
    codes=frame['ts_code'].to_list();left={c:i for i,c in enumerate(codes) if day[i]==0};right={c:i for i,c in enumerate(codes) if day[i]==1}
    common=sorted(set(left)&set(right));li=np.array([left[c] for c in common]);ri=np.array([right[c] for c in common])
    assert len(left)==int((day==0).sum()) and len(right)==int((day==1).sum())
    assert psutil.virtual_memory().available>4*2**30
    assert torch.cuda.is_available();torch.set_num_threads(8);torch.manual_seed(20261007);torch.cuda.manual_seed_all(20261007)
    torch.use_deterministic_algorithms(True);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    device='cuda';xt=torch.from_numpy(clean).to(device)
    args=[torch.from_numpy(a).to(device) for a in (day,frame['flag_limit_up'].to_numpy(),frame['y_rank'].to_numpy().astype(np.float32),frame['y_ret_1d'].to_numpy().astype(np.float32),li,ri)]
    checks=[];states=[]
    for turnover_weight in (0.,.3):
        torch.cuda.reset_peak_memory_stats();network=engine.network(63,bundle['config']).to(device);network.load_state_dict(bundle['state'])
        optimizer=torch.optim.AdamW(network.parameters(),lr=.0001,weight_decay=.0001);started=time.perf_counter();records=[]
        for step in range(2):
            network.train();optimizer.zero_grad(set_to_none=True);score=network(xt).squeeze(-1);terms=loss.paired_terms(score,*args)
            # Availability of either label may not alter the holdings pool or membership.
            if step==0:
                missing=loss.paired_terms(score.detach(),args[0],args[1],torch.full_like(args[2],torch.nan),torch.full_like(args[3],torch.nan),args[4],args[5])
                assert torch.equal(terms['turnover_eligibility'],missing['turnover_eligibility'])
                assert torch.equal(terms['membership'][2:],missing['membership'][2:])
                assert torch.equal(terms['soft_holdings_overlap'].detach(),missing['soft_holdings_overlap'])
            proxy=loss.objective(terms,turnover_weight);assert torch.isfinite(proxy)
            proxy.backward();assert all(torch.isfinite(p.grad).all() for p in network.parameters() if p.grad is not None)
            torch.nn.utils.clip_grad_norm_(network.parameters(),1.);optimizer.step()
            error=float((terms['membership'].sum(dim=1)-terms['membership_mass_targets']).abs().max().detach())
            assert error<.02
            records.append({'step':step,'training_proxy_loss':float(proxy.detach()),'membership_mass_error':error,
                **{k:float(terms[k].detach()) for k in ('soft_rank_correlation','soft_annual_excess','soft_holdings_overlap')}})
        states.append({k:v.detach().cpu().clone() for k,v in network.state_dict().items()})
        checks.append({'turnover_weight':turnover_weight,'actual_mature_training_steps':records,
            'seconds_including_first_GPU_calls':time.perf_counter()-started,
            'peak_own_tensor_allocated_bytes':torch.cuda.max_memory_allocated(),
            'peak_own_allocator_reserved_bytes':torch.cuda.max_memory_reserved(),
            'host_available_bytes_after_variant':psutil.virtual_memory().available})
        del network,optimizer,score,terms;gc.collect();torch.cuda.empty_cache()
    assert any(not torch.equal(states[0][k],states[1][k]) for k in states[0])
    for path,digest in hashes.items():assert sha(Path(path))==digest,path
    create(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'fixed_tau_implicit_cap_gradient_matches_finite_difference':True,
        'fixed_mass_gradient_sum_zero':True,'actual_mature_pair_rows':len(frame),'training_dates':dates,'cutoff_exclusive':cutoff,
        'future_label_poisoning_cannot_enter_mature_control_pair':True,'holdings_eligibility_andmembership_label_independent':True,
        'turnover_training_variants_produce_distinct_weights':True,'actual_finite_gradient_GPU_training_controls':checks,
        'mature_pair_keys_sha256':sha(keys),'original_checkpoint_unchanged':True,'input_sha256':hashes,
        'new_quality_scores':0,'official_scoring_calls':0,'test_labels_read':False,
        'scope':'Two actual mature training dates andtwo fine-tuning steps pervariant only. Surrogates do not equal official scoring; complete annual training, continuous official final-CSV evaluation andfuture scheme controls remain required.'})
    print('Actual constrained-gradient andmature-pair portfolio training controls passed',flush=True)

if __name__=='__main__':main()
