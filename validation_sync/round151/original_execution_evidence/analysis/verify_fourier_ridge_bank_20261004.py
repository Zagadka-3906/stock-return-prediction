"""Independently check fixed projections, ridge solve, reload and padded prefixes."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT)]
import numpy as np
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import Ridge
import train_fourier_ridge_bank_20261004 as bank


def main():
    folder=ROOT/'analysis/fourier_ridge_preflight_20261004';folder.mkdir(exist_ok=True)
    assert not (folder/'verification.json').exists()
    rng=np.random.default_rng(20261004);x=rng.normal(size=(33001,11)).astype(np.float32)
    x[::17,2]=np.nan;x[::101,5]=50.
    rank=rng.uniform(-.5,.5,len(x));returns=rng.normal(0,.03,len(x));returns[::1000]=10.
    proofs=[]
    for name,cfg in bank.CONFIGS.items():
        target=rank if cfg['target']=='y_rank' else returns;bundle=bank.fit_arrays(x,target,cfg)
        z=np.clip((np.where(np.isfinite(x),x,bundle['mean'])-bundle['mean'])/bundle['scale'],-cfg['clip_z'],cfg['clip_z'])
        sampler=RBFSampler(gamma=bundle['gamma'],n_components=cfg['random_components'],random_state=cfg['seed']).fit(z[:1])
        assert np.array_equal(sampler.random_weights_,bundle['random_weights'])
        assert np.array_equal(sampler.random_offset_,bundle['random_phase'])
        reference_basis=np.concatenate([z,sampler.transform(z)*np.sqrt(cfg['random_components'])],axis=1)
        actual=bank.transform(x,bundle['mean'],bundle['scale'],cfg,bundle['random_weights'],bundle['random_phase'])
        basis_error=float(np.max(np.abs(actual-reference_basis)));assert basis_error<1e-12
        labels=target if bundle['target_bounds'] is None else np.clip(target,*bundle['target_bounds'])
        reference=Ridge(alpha=cfg['ridge_lambda']*len(x),solver='cholesky').fit(reference_basis,labels)
        coefficient_error=float(np.max(np.abs(reference.coef_-bundle['coefficients'])))
        intercept_error=abs(float(reference.intercept_)-bundle['intercept'])
        assert coefficient_error<1e-12 and intercept_error<1e-12
        path=folder/f'{name}.joblib';bank.engine.save_bundle(path,bundle)
        predicted=bank.predict_arrays(bundle,x)
        assert np.array_equal(predicted,bank.predict_arrays(bank.engine.load_bundle(path),x))
        counts=(1,80,32767,32768,32781)
        assert all(np.array_equal(predicted[:n],bank.predict_arrays(bundle,x[:n])) for n in counts)
        proofs.append({'model':name,'sklearn_random_weights_and_phase_bit_identical':True,
            'independent_basis_max_abs_error':basis_error,'independent_coefficient_error':coefficient_error,
            'independent_intercept_error':intercept_error,'comparison_tolerance':1e-12,
            'row_prefix_counts':counts,'row_prefix_and_reload_bit_identical':True,
            'normal_equation_max_abs_residual':bundle['normal_equation_max_abs_residual']})
    bank.dump(folder/'verification.json',{'status':'passed','test_data_read':False,'new_model_scores':0,
        'raw_features':63,'random_features':128,'basis_columns':191,'seed':20261004,
        'random_projection_does_not_use_feature_values_or_targets':True,'controls':proofs,
        'source_sha256':{str(p.resolve()):bank.sha(p) for p in (Path(__file__),Path(bank.__file__),bank.SOURCE)},
        'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('All six Fourier ridge independent basis, solver andprefix controls passed.',flush=True)


if __name__=='__main__':main()
