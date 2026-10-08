"""Independent dense augmented bounded least squares and exact saved/native prefix controls."""
from pathlib import Path
import os,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/nonflag_ConeRidge64_small_v2_20261008')

def dense_oracle(raw,preprocessing,y,cfg,alpha):
    import numpy as np
    from scipy.optimize import lsq_linear
    from nonflag_residual_HGB_preprocessing_20261007 import prepare
    x=prepare(raw,preprocessing);center=x.mean(axis=0);mean=float(y.mean())
    augmented=np.vstack(((x-center)*cfg['feature_sign'],np.eye(64)*np.sqrt(alpha)))
    target=np.concatenate((y-mean,np.zeros(64)))
    result=lsq_linear(augmented,target,bounds=(0.,np.inf),method='bvls',tol=1e-12,max_iter=256)
    raw_min=float(np.min(result.x));boundary_tolerance=2e-12
    assert result.success and np.isfinite(result.x).all() and raw_min>=-boundary_tolerance,(result.message,raw_min)
    # BVLS can return roundoff below its lower bound; validate before projecting that oracle value.
    positive=np.maximum(result.x,0.)
    gradient=augmented.T@(augmented@positive-target);rhs=augmented.T@target
    active=positive>boundary_tolerance
    active_violation=float(np.max(np.abs(gradient[active]))) if active.any() else 0.
    inactive_violation=float(np.max(np.maximum(-gradient[~active],0.))) if (~active).any() else 0.
    relative_kkt=max(active_violation,inactive_violation)/max(1.,float(np.max(np.abs(rhs))))
    assert relative_kkt<1e-10,relative_kkt
    coef=cfg['feature_sign']*positive
    return coef,float(mean-center@coef),{'dense_BVLS_success':True,'iterations':int(result.nit),
        'optimality':float(result.optimality),'raw_minimum_parameter':raw_min,'allowed_boundary_roundoff':boundary_tolerance,
        'projected_negative_parameters':int(np.count_nonzero(result.x<0.)),
        'maximum_boundary_projection':float(np.max(np.abs(positive-result.x))),
        'independent_dense_relative_KKT_violation':relative_kkt,'native_solver_and_comparison_tolerances_unchanged':True}

def main():
    import numpy as np,joblib
    from threadpoolctl import threadpool_limits
    from nonflag_residual_HGB_preprocessing_20261007 import fit_preprocessing
    import nonflag_ConeRidge64_streamed_v1_20261008 as native
    sources=[Path(__file__),Path(native.__file__),A/'nonflag_SpectralGram64_streamed_v1_20261008.py',
        A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py']
    pins={str(p):sha(p) for p in sources};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_synthetic_controls.json',{'input_sha256':pins,'configurations':native.CONFIGS,
        'actual_official_scores':0,'actual_training_fits':0,'future_X_and_Y_read':False})
    rng=np.random.default_rng(2026100822);records=[]
    with threadpool_limits(limits=2):
        for label,n in (('full_rank_missing',173),('multi_block_collinear',17003),('zero_target',177)):
            raw=rng.normal(size=(n,64));raw[::11,5]=np.nan;raw[::17,9]=np.inf
            if label=='multi_block_collinear':raw[:,60]=raw[:,3];raw[:,61]=raw[:,4]*2.;raw[:,62]=1.;raw[:,63]=0.
            y=np.zeros(n) if label=='zero_target' else .04*raw[:,3]-.025*raw[:,8]+rng.normal(scale=.2,size=n)
            preprocessing=fit_preprocessing(raw);stats=native.accumulate(raw,preprocessing,y)
            test=rng.normal(size=(10017,64));test[::19,5]=np.nan;test[::23,8]=-np.inf
            for name,cfg in native.CONFIGS.items():
                model,metadata=native.fit_from_statistics(stats,cfg);coef,intercept,oracle=dense_oracle(raw,preprocessing,y,cfg,model.alpha)
                assert np.allclose(model.coef_,coef,rtol=2e-8,atol=2e-10) and np.isclose(model.intercept_,intercept,rtol=2e-8,atol=2e-10),(label,name,np.max(np.abs(model.coef_-coef)))
                bundle={'model':model,'preprocessing':preprocessing,'features':[f'f{i}' for i in range(63)]+['qualified106_current_forecast_average_rank_over_N']}
                path=OUT/(label+'_'+name+'.joblib');state_path=path.with_suffix('.json');joblib.dump(bundle,path);create(state_path,native.export(bundle))
                value=native.predict_native(bundle,test);saved=joblib.load(path);state=read(state_path)
                for count in (0,1,79,8191,8192,10017):
                    for check in (native.predict_native(saved,test[:count]),native.predict_decoded(state,test[:count])):
                        assert np.array_equal(value[:count].view('u8'),check.view('u8'))
                records.append({'population':label,'training_rows':n,'name':name,'configuration':cfg,'metadata':metadata,'oracle':oracle,
                    'independent_dense_BVLS_coefficients_and_intercept_close':True,'native_reload_decoder_six_prefix_bits_exact':True,
                    'model_sha256':sha(path),'state_sha256':sha(state_path)})
        for p,digest in pins.items():assert sha(p)==digest,p
    create(OUT/'verification.json',{'status':'passed_actual12_synthetic_ConeRidge64_dense_BVLS_and72_prefix_controls',
        'input_sha256':pins,'records':records,'actual_synthetic_native_fits':12,'actual_prefix_controls':72,
        'actual_official_scores':0,'future_X_and_Y_read':False,'own_annual_training_not_claimed':True})
    create(A/'actual_nonflag_ConeRidge64_small_location_v2_20261008.json',{'status':'passed_actual12_constrained_ridge_small_controls_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_official_scores':0})
    print('Twelve constrained native fits passed independent dense BVLS and72 saved prefix controls.',flush=True)

if __name__=='__main__':main()
