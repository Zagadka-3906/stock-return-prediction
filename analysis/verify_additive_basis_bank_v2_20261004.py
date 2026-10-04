"""Independent layout arithmetic, solver, router andreal batch-boundary checks."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT)]
import numpy as np
from sklearn.linear_model import Ridge
import train_additive_basis_bank_20261004 as bank
import additive_basis_model_sources_20261004 as router


def main():
    folder=ROOT/'analysis/additive_basis_preflight_v2_20261004';folder.mkdir(exist_ok=True)
    assert not (folder/'verification.json').exists()
    sources=[Path(__file__),Path(bank.__file__),Path(router.__file__),bank.SOURCE,Path(bank.original.__file__),ROOT/'analysis/verify_additive_basis_bank_20261004.py',ROOT/'analysis/additive_basis_preflight_20261004/frozen_before_controls.json']
    inputs={str(p.resolve()):bank.sha(p) for p in sources}
    bank.dump(folder/'frozen_before_controls.json',{'input_sha256':inputs,
        'fixed_configurations':bank.CONFIGS,'test_data_read':False,'new_quality_scores':0},immutable=True)
    rng=np.random.default_rng(20261004);x=rng.normal(size=(33001,11)).astype(np.float32)
    x[::17,2]=np.nan;x[::101,5]=50.;rank=rng.uniform(-.5,.5,len(x));returns=rng.normal(0,.03,len(x));returns[::1000]=10.
    checks=[]
    assert bank.engine is not bank.original.engine and bank.original.engine.OUT==bank.original.OUT
    old_dirs={name:router.previous.source_dir(name) for name in router.previous.CONFIGS}
    for name,cfg in bank.CONFIGS.items():
        bundle=bank.fit_arrays(x,rank if cfg['target']=='y_rank' else returns,cfg)
        z=bank.transform(x,bundle['mean'],bundle['scale'],cfg['clip_z'],cfg['hinge_knots'])
        values=np.clip((np.where(np.isfinite(x),x,bundle['mean'])-bundle['mean'])/bundle['scale'],-cfg['clip_z'],cfg['clip_z'])
        independent=np.array([[v for v in row]+[max(v-k,0.) for k in cfg['hinge_knots'] for v in row] for row in values[:83]])
        assert np.array_equal(z[:83],independent) and z.shape[1]==11*(1+len(cfg['hinge_knots']))
        y=rank if cfg['target']=='y_rank' else np.clip(returns,*bundle['target_bounds'])
        reference=Ridge(alpha=cfg['ridge_lambda']*len(x),solver='cholesky').fit(z,y)
        error=float(np.max(np.abs(bundle['coefficients']-reference.coef_)))
        intercept_error=abs(bundle['intercept']-float(reference.intercept_))
        prediction_error=float(np.max(np.abs(bank.predict_arrays(bundle,x)-reference.predict(z))))
        assert error<1e-12 and intercept_error<1e-11 and prediction_error<1e-12
        path=folder/f'{name}.joblib';bank.engine.save_bundle(path,bundle)
        p=bank.predict_arrays(bundle,x);assert np.array_equal(p,router.predict_arrays(router.load_bundle(path),x))
        for n in (1,80,32767,32768,32781):assert np.array_equal(p[:n],bank.predict_arrays(bundle,x[:n]))
        assert router.source_dir(name)==bank.OUT/name
        checks.append({'model':name,'knots':cfg['hinge_knots'],'coefficient_error':error,'intercept_error':intercept_error,'prediction_error':prediction_error,
            'reload_router_andbatch_prefix_bit_identical':True,'normal_equation_max_abs_residual':bundle['normal_equation_max_abs_residual']})
    assert old_dirs=={name:router.source_dir(name) for name in router.previous.CONFIGS}
    assert bank.original.engine.OUT==bank.original.OUT
    for path,digest in inputs.items():assert bank.sha(path)==digest,path
    bank.dump(folder/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'numerical_comparison_tolerances':{'coefficients':1e-12,'intercept':1e-11,'predictions':1e-12},
        'configurations':checks,'expanded_columns':{'narrow':252,'wide5':378},
        'basis_knots_fixed_before_any_scoring':bank.LAYOUTS,'existing_model_bank_paths_unchanged':True,
        'isolated_training_engine_does_not_mutate_existing_bank':True,
        'independent_basis_andridge_solver_checks_passed':True,'input_sha256':inputs,
        'scope':'Synthetic numerical androuting controls only; real60 annual fits, future inference andofficial complete-output quality checks remain required.',
        'test_data_read':False,'new_quality_scores':0},immutable=True)
    print('Twelve fixed additive basis configurations passed independent preflight',flush=True)


if __name__=='__main__':main()
