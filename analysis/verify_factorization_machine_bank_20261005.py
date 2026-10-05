"""Real past-row FM formula, analytic-gradient, saved-prefix and future-poison controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_factorization_machine_bank_20261005 as bank
def pair_formula(bundle,x):
    import numpy as np
    z=bank.standardize(x,bundle['mean'],bundle['scale'],bundle['config']).astype(np.float64)
    w=bundle['weights'];linear=np.asarray(w['linear'],dtype=np.float64);factors=np.asarray(w['factors'],dtype=np.float64)
    values=np.full(len(z),float(w['bias']),dtype=np.float64)
    for i in range(z.shape[1]):values+=linear[i]*z[:,i]
    interaction=factors@factors.T
    for i in range(z.shape[1]):
        for j in range(i+1,z.shape[1]):values+=interaction[i,j]*z[:,i]*z[:,j]
    return values/bundle['target_scale']
def gradient_control(cfg):
    import numpy as np,torch
    torch.manual_seed(90210);rng=np.random.default_rng(90210)
    x=rng.normal(size=(17,63));upstream=rng.normal(size=17)
    model=bank.network(63,cfg).double()
    with torch.no_grad():model.bias.fill_(.13);model.linear.copy_(torch.from_numpy(rng.normal(size=63)*.01))
    factors=model.factors.detach().numpy().copy()
    model(torch.from_numpy(x)).mul(torch.from_numpy(upstream)).sum().backward()
    bias_error=abs(float(model.bias.grad)-float(upstream.sum()))
    linear_error=float(np.max(np.abs(model.linear.grad.numpy()-(x*upstream[:,None]).sum(0))))
    factor_error=0.
    if cfg['latent_factors']:
        latent=x@factors;expected=np.zeros_like(factors)
        for i in range(63):expected[i]=(upstream[:,None]*x[:,i,None]*(latent-x[:,i,None]*factors[i])).sum(0)
        factor_error=float(np.max(np.abs(model.factors.grad.numpy()-expected)))
    else:assert model.factors.grad is None
    assert max(bias_error,linear_error,factor_error)<1e-10
    return {'analytic_bias_gradient_error':bias_error,'analytic_linear_gradient_error':linear_error,'analytic_offdiagonal_factor_gradient_error':factor_error}
def main():
    import numpy as np,polars as pl,torch
    out=ROOT/'analysis/factorization_machine_preflight_20261005';out.mkdir(exist_ok=True)
    if (out/'verification.json').exists():
        proof=bank.read(out/'verification.json')
        for source,digest in proof['source_sha256'].items():assert bank.sha(source)==digest,source
        return proof
    sources=[Path(__file__),Path(bank.__file__),bank.SOURCE,bank.STORAGE,bank.engine.FEATURE_FILE,bank.engine.MANIFEST,ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md']
    bindings={str(p.resolve()):bank.sha(p) for p in sources}
    bank.dump(out/'frozen_before_controls.json',{'status':'frozen_before_actual_formula_gradient_and_past_model_controls','configurations':bank.CONFIGS,'input_sha256':bindings,'new_quality_scores':0,'test_labels_read':False},immutable=True)
    features=bank.engine.feature_names();lazy=pl.scan_parquet(bank.engine.FEATURE_FILE);cutoff=bank.engine.fold_cutoff(2020)
    controls=[];predictions={}
    for name,cfg in bank.CONFIGS.items():
        past=bank.engine.training_frame(lazy,cutoff,cfg).select(bank.engine.KEYS+features+[cfg['target']]).head(4096).collect()
        assert len(past)==4096 and int(past['trade_date'].max())<cutoff
        x=bank.engine.to_matrix(past,features);y=past[cfg['target']].to_numpy();pilot=dict(cfg,epochs=4)
        gradients=gradient_control(pilot);bundle=bank.fit_arrays(x,y,pilot)
        assert bundle['actual_parameter_count']==64+63*cfg['latent_factors'] and len(bundle['training_losses'])==4
        values=bank.predict_arrays(bundle,x);path=out/f'{name}.joblib';bank.engine.save_bundle(path,bundle)
        assert np.array_equal(values,bank.predict_arrays(bank.engine.load_bundle(path),x))
        counts=(1,80,257,1024,4095)
        assert all(np.array_equal(values[:count],bank.predict_arrays(bank.engine.load_bundle(path),x[:count])) for count in counts)
        probe=x[:128].copy();probe[::5,2]=np.nan;probe[::7,5]=np.inf;probe[::11,8]=0.
        z=bank.standardize(probe,bundle['mean'],bundle['scale'],pilot);assert np.isfinite(z).all() and (z[::5,2]==0.).all() and (z[::7,5]==0.).all()
        expected=pair_formula(bundle,probe);actual=bank.predict_arrays(bundle,probe);error=float(np.max(np.abs(actual-expected)));assert error<1e-10,(name,error)
        maturity=bank.boundary_control(2020,cfg,features);assert maturity['status']=='passed'
        controls.append({'model':name,'actual_past_rows':4096,'pilot_epochs':4,'actual_parameter_count':bundle['actual_parameter_count'],'training_device':bundle['device'],'explicit_offdiagonal_pair_formula_max_error':error,**gradients,'native_saved_model_prefix_counts_bit_identical':counts,'actual_future_label_poison_control':maturity,'model_sha256':bank.sha(path),'actual_complete_annual_fits':0})
        predictions[name]=values;print('Actual FM controls passed: '+name,flush=True)
        del past,x,y,bundle;bank.engine.gc.collect()
    for label in ('rank','return'):
        group=[predictions[f'{label}_fm_k{k}_e32'] for k in (0,8,32)]
        assert all(not np.array_equal(group[a],group[b]) for a,b in ((0,1),(0,2),(1,2)))
    for source,digest in bindings.items():assert bank.sha(source)==digest,source
    proof={'status':'passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'source_sha256':bindings,'controls':controls,'actual_annual_fits':0,'actual4096_row4_epoch_controls_not_complete32_epoch_fits':True,'first_order_and_both_factor_ranks_distinct_for_each_target':True,'new_quality_scores':0,'test_labels_read':False}
    bank.dump(out/'verification.json',proof,immutable=True);return proof
if __name__=='__main__':main()
