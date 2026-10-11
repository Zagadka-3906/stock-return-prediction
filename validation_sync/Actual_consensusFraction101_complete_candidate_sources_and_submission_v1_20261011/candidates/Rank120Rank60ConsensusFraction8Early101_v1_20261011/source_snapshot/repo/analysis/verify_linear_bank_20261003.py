"""Check ridge against an independent solver and exact prefix/reload controls."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT)]
import numpy as np
from sklearn.linear_model import Ridge
import train_linear_bank_20261003 as bank


def main():
    folder=ROOT/'analysis/linear_bank_preflight_20261003';folder.mkdir(exist_ok=True)
    assert not (folder/'verification.json').exists()
    rng=np.random.default_rng(20261003)
    x=rng.normal(size=(33001,11)).astype(np.float32);x[::17,2]=np.nan;x[::101,5]=50.
    rank=rng.uniform(-.5,.5,len(x));returns=rng.normal(0,.03,len(x));returns[::1000]=10.
    proofs=[]
    for name,cfg in bank.CONFIGS.items():
        target=rank if cfg['target']=='y_rank' else returns
        bundle=bank.fit_arrays(x,target,cfg)
        transformed=bank.transform(x,bundle['mean'],bundle['scale'],cfg['clip_z'])
        labels=target if bundle['target_bounds'] is None else np.clip(target,*bundle['target_bounds'])
        reference=Ridge(alpha=cfg['ridge_lambda']*len(x),solver='cholesky').fit(transformed,labels)
        coefficient_error=float(np.max(np.abs(bundle['coefficients']-reference.coef_)))
        intercept_error=abs(bundle['intercept']-float(reference.intercept_))
        assert coefficient_error<1e-12 and intercept_error<1e-12
        path=folder/f'{name}.joblib';bank.engine.save_bundle(path,bundle)
        predicted=bank.predict_arrays(bundle,x)
        assert np.array_equal(predicted,bank.predict_arrays(bank.engine.load_bundle(path),x))
        counts=(1,80,32767,32768,32781)
        assert all(np.array_equal(predicted[:n],bank.predict_arrays(bundle,x[:n])) for n in counts)
        proofs.append({'model':name,'independent_coefficient_error':coefficient_error,
                       'independent_intercept_error':intercept_error,'row_prefix_counts':counts,
                       'row_prefix_and_reload_bit_identical':True,'normal_equation_max_abs_residual':bundle['normal_equation_max_abs_residual']})
    payload={'status':'passed','test_data_read':False,'new_model_scores':0,
             'independent_sklearn_normal_equation_comparison':proofs,
             'source_sha256':{str(p.resolve()):bank.sha(p) for p in (Path(__file__),Path(bank.__file__),bank.SOURCE)},
             'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
    bank.dump(folder/'verification.json',payload,immutable=True)
    print(json.dumps({'status':'passed','configurations':len(proofs)},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
