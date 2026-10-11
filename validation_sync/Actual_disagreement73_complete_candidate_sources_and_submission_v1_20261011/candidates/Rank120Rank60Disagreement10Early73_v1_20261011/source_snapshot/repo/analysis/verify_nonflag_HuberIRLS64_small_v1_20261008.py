"""Two real synthetic native fits, an independent dense IRLS oracle, codec and prefix controls; no official scoring."""
from pathlib import Path
import os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/nonflag_HuberIRLS64_small_v1_20261008')


def main():
    import numpy as np,joblib
    from threadpoolctl import threadpool_limits
    from nonflag_residual_HGB_preprocessing_20261007 import fit,prepare
    from nonflag_HuberIRLS64_streamed_v1_20261008 import CONFIGS,fit_streamed,export,predict_native,predict_decoded
    sources=[Path(__file__),A/'nonflag_HuberIRLS64_streamed_v1_20261008.py',A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py']
    pins={str(path):sha(path) for path in sources};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual2_small_fits.json',{'input_sha256':pins,'configurations':CONFIGS,'synthetic_rows':24593,'provided_train_or_future_X_and_Y_read':False,'actual_official_scores':0})
    rng=np.random.default_rng(20261008);raw=rng.normal(size=(24593,64));truth=rng.normal(0.,.015,64)
    y=raw@truth+rng.normal(0.,.06,len(raw));outliers=rng.choice(len(raw),len(raw)//20,replace=False);y[outliers]+=rng.normal(0.,3.,len(outliers))
    raw[1,0]=np.nan;raw[2,1]=np.inf;raw[3,2]=-np.inf
    preprocessing=fit(raw);x=prepare(raw,preprocessing);z=np.column_stack([x,np.ones(len(x))]);features=[f'synthetic_{i}' for i in range(64)]
    test=rng.normal(size=(16397,64));test[0,3]=np.nan;test[1,4]=np.inf;records=[];started=time.perf_counter()
    with threadpool_limits(limits=2):
        for name,cfg in CONFIGS.items():
            t=time.perf_counter();model,metadata=fit_streamed(raw,preprocessing,y,cfg);elapsed=time.perf_counter()-t
            penalty=np.diag([len(y)*cfg['alpha_per_training_row']]*64+[0.])
            beta=np.linalg.solve(z.T@z+penalty,z.T@y)
            dense_objectives=[]
            for iteration in range(metadata['actual_iterations']):
                error=y-z@beta;weights=np.where(np.abs(error)<=cfg['delta'],1.,cfg['delta']/np.abs(error))
                beta=np.linalg.solve(z.T@(z*weights[:,None])+penalty,z.T@(y*weights))
                residual=y-z@beta;absolute=np.abs(residual);loss=np.where(absolute<=cfg['delta'],.5*residual**2,cfg['delta']*(absolute-.5*cfg['delta']))
                dense_objectives.append(float(loss.sum()+.5*beta@penalty@beta))
            actual=np.r_[model.coef_,model.intercept_]
            assert np.allclose(actual,beta,rtol=1e-10,atol=1e-12) and np.allclose([item['training_objective'] for item in metadata['history']],dense_objectives,rtol=1e-11,atol=1e-9)
            bundle={'model':model,'preprocessing':preprocessing,'features':features};path=OUT/(name+'.joblib');state_path=OUT/(name+'_state.json')
            joblib.dump(bundle,path);create(state_path,export(bundle));reloaded=joblib.load(path);state=read(state_path)
            primary=predict_native(bundle,test)
            for value in (predict_native(reloaded,test),predict_decoded(state,test)):assert np.array_equal(primary.view('u8'),value.view('u8'))
            for count in (0,1,79,8191,8192,16397):
                for value in (predict_native(reloaded,test[:count]),predict_decoded(state,test[:count])):assert np.array_equal(primary[:count].view('u8'),value.view('u8'))
            item={'name':name,'fit_seconds':elapsed,'configuration':cfg,'actual_training_rows':len(y),'actual_inference_rows':len(test),
                'independent_dense_IRLS_coefficients_and_all_training_objectives_close':True,'native_reloaded_JSON_decoder_and6_prefixes_bits_exact':True,
                'metadata':metadata,'native_model_sha256':sha(path),'state_sha256':sha(state_path),'new_native_fits':1,'actual_official_scores':0}
            create(OUT/(name+'_verification.json'),item);records.append(item);print(f'Actual synthetic {name}: dense objective/coefficients and saved/decoded/prefix controls passed; fit{elapsed:.3f}s',flush=True)
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual2_small_HuberIRLS64_native_dense_oracle_decoder_and12_prefix_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_new_synthetic_native_fits':2,
        'elapsed_seconds':time.perf_counter()-started,'actual_official_scores':0,'full_own_mature10_model_bank_and_candidate_pipeline_not_yet_admitted':True,
        'provided_train_or_future_X_and_Y_read':False,'global_optimum_or_resource_exhaustion_not_claimed':True})
    create(A/'actual_nonflag_HuberIRLS64_small_location_v1_20261008.json',{'status':'passed_actual2_synthetic_HuberIRLS64_native_controls_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_official_scores':0})


if __name__=='__main__':main()
