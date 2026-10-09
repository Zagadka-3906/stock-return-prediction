"""Independent sklearn algebra, actual past-data pilot and prefix/reload controls."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT)]
import train_nystrom_ridge_bank_20261004 as bank

def main():
    import numpy as np
    import polars as pl
    from sklearn.kernel_approximation import Nystroem
    from sklearn.linear_model import Ridge
    folder=ROOT/'analysis/nystrom_ridge_preflight_20261004';folder.mkdir(exist_ok=True)
    assert not (folder/'verification.json').exists()
    frozen={str(p.resolve()):bank.sha(p) for p in (Path(__file__),Path(bank.__file__),bank.SOURCE)}
    bank.dump(folder/'frozen_before_controls.json',{'status':'frozen_before_numerical_controls',
        'input_sha256':frozen,'new_quality_scores':0,'test_data_read':False},immutable=True)
    rng=np.random.default_rng(20261004);x=rng.normal(size=(33001,63)).astype(np.float32)
    x[::17,2]=np.nan;x[::101,5]=50.
    rank=rng.uniform(-.5,.5,len(x));returns=rng.normal(0,.03,len(x));returns[::1000]=10.
    proofs=[]
    for name,cfg in bank.CONFIGS.items():
        target=rank if cfg['target']=='y_rank' else returns;bundle=bank.fit_arrays(x,target,cfg)
        z=bank.standardize(x,bundle['mean'],bundle['scale'],cfg)
        reference_map=Nystroem(kernel='rbf',gamma=bundle['gamma'],n_components=cfg['landmark_components'],random_state=cfg['seed'],n_jobs=1).fit(z)
        assert np.array_equal(reference_map.component_indices_,bundle['landmark_indices'])
        assert np.array_equal(reference_map.components_,bundle['landmarks'])
        assert np.array_equal(reference_map.normalization_,bundle['normalization'])
        reference_basis=np.concatenate([z,np.sqrt(cfg['kernel_mass'])*reference_map.transform(z)],axis=1)
        actual=bank.transform(x,bundle['mean'],bundle['scale'],cfg,bundle['landmarks'],bundle['normalization'],bundle['gamma'])
        basis_error=float(np.max(np.abs(actual-reference_basis)));assert basis_error<1e-10
        labels=target if bundle['target_bounds'] is None else np.clip(target,*bundle['target_bounds'])
        reference=Ridge(alpha=cfg['ridge_lambda']*len(x),solver='cholesky').fit(reference_basis,labels)
        coefficient_error=float(np.max(np.abs(reference.coef_-bundle['coefficients'])))
        intercept_error=abs(float(reference.intercept_)-bundle['intercept'])
        prediction_error=float(np.max(np.abs(reference.predict(reference_basis)-bank.predict_arrays(bundle,x))))
        assert coefficient_error<1e-10 and intercept_error<1e-10 and prediction_error<1e-9
        path=folder/f'{name}.joblib';bank.engine.save_bundle(path,bundle)
        predicted=bank.predict_arrays(bundle,x)
        assert np.array_equal(predicted,bank.predict_arrays(bank.engine.load_bundle(path),x))
        counts=(1,80,32767,32768,32781)
        assert all(np.array_equal(predicted[:n],bank.predict_arrays(bundle,x[:n])) for n in counts)
        changed_y=target[::-1].copy();changed=bank.fit_arrays(x,changed_y,cfg)
        assert np.array_equal(bundle['landmark_indices'],changed['landmark_indices'])
        assert np.array_equal(bundle['landmarks'],changed['landmarks']) and np.array_equal(bundle['normalization'],changed['normalization'])
        actual_boundary=bank.engine.boundary_control(2020,cfg,bank.engine.feature_names())
        assert actual_boundary['status']=='passed'
        proofs.append({'model':name,'sklearn_landmark_indices_basis_andnormalization_bit_identical':True,
            'independent_basis_max_abs_error':basis_error,'independent_coefficient_error':coefficient_error,
            'independent_intercept_error':intercept_error,'independent_prediction_max_abs_error':prediction_error,
            'comparison_tolerances':{'basis_coefficients_intercept':1e-10,'predictions':1e-9},
            'row_prefix_counts':counts,'row_prefix_andreload_bit_identical':True,
            'landmark_sampling_andbasis_unchanged_by_label_permutation':True,
            'actual2020_mature_batch_future_label_poisoning_control':actual_boundary})
        print('Nyström independent and actual past-data controls passed: '+name,flush=True)
    for path,digest in frozen.items():assert bank.sha(Path(path))==digest,path
    bank.dump(folder/'verification.json',{'status':'passed','controls':proofs,
        'actual_annual_fits':0,'synthetic_training_andactual4096_row_boundary_pilots_only':True,
        'test_data_read':False,'new_quality_scores':0,'source_sha256':frozen,
        'frozen_control_sha256':bank.sha(folder/'frozen_before_controls.json'),
        'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)

if __name__=='__main__':main()
