"""Actual own-mature200003-row numerical/resource probe; no validation scores or future inputs."""
from pathlib import Path
import os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/nonflag_HuberIRLS64_actual200k_v1_20261008')


def main():
    import numpy as np,joblib,psutil
    from threadpoolctl import threadpool_limits
    from nonflag_HuberIRLS64_own_window_v1_20261008 import input_paths,load_population,admitted_window
    from nonflag_HuberIRLS64_streamed_v1_20261008 import CONFIGS,fit_streamed,export,predict_native,predict_decoded
    from nonflag_residual_HGB_preprocessing_20261007 import prepare
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    small_path=A/'actual_nonflag_HuberIRLS64_small_location_v2_20261008.json';small=read(small_path)
    small_proof=Path(small['output'])/'verification.json'
    assert sha(small_proof)==small['verification_sha256'] and read(small_proof)['actual_new_synthetic_native_fits']==2
    assert not OUT.exists();OUT.mkdir()
    paths=[Path(__file__),small_path,small_proof,*input_paths([2025])];pins={str(p):sha(p) for p in paths}
    create(OUT/'frozen_before_actual200k_probe.json',{'input_sha256':pins,'configurations':CONFIGS,
        'probe_rows':200003,'own_training_window_year':2025,'future_X_and_Y_read':False,'actual_official_scores':0,
        'benchmark_preprocessing_from_same_full_own2025_training_window_not_validation':True})
    started=time.perf_counter();records=[]
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        population=load_population();window,target,preprocessing,features,info=admitted_window(population,2025)
        raw=window[:200003];y=target[:len(raw)];test=np.asarray(window[-10017:]).copy()
        z=np.column_stack([prepare(raw,preprocessing),np.ones(len(raw))])
        rss_before=psutil.Process().memory_info().rss
        for name,cfg in CONFIGS.items():
            t=time.perf_counter();model,metadata=fit_streamed(raw,preprocessing,y,cfg);elapsed=time.perf_counter()-t
            penalty=np.diag([len(y)*cfg['alpha_per_training_row']]*64+[0.]);beta=np.linalg.solve(z.T@z+penalty,z.T@y)
            oracle_objectives=[]
            for iteration in range(metadata['actual_iterations']):
                r=y-z@beta;w=np.minimum(1.,cfg['delta']/np.maximum(np.abs(r),1e-12))
                beta=np.linalg.solve(z.T@(w[:,None]*z)+penalty,z.T@(w*y))
                r=y-z@beta;a=np.abs(r);rho=np.where(a<=cfg['delta'],.5*r*r,cfg['delta']*(a-.5*cfg['delta']))
                oracle_objectives.append(float(rho.sum()+.5*beta@penalty@beta))
            assert np.allclose(np.r_[model.coef_,model.intercept_],beta,rtol=1e-10,atol=1e-12)
            assert np.allclose([v['training_objective'] for v in metadata['history']],oracle_objectives,rtol=1e-11,atol=1e-8)
            bundle={'model':model,'preprocessing':preprocessing,'features':features};native=OUT/(name+'.joblib');state_path=OUT/(name+'_state.json')
            joblib.dump(bundle,native);create(state_path,export(bundle));saved=joblib.load(native);state=read(state_path)
            value=predict_native(bundle,test)
            for check in (predict_native(saved,test),predict_decoded(state,test)):assert np.array_equal(value.view('u8'),check.view('u8'))
            for count in (0,1,79,8191,8192,10017):
                for check in (predict_native(saved,test[:count]),predict_decoded(state,test[:count])):assert np.array_equal(value[:count].view('u8'),check.view('u8'))
            record={'name':name,'configuration':cfg,'training_rows':len(y),'fit_seconds':elapsed,'metadata':metadata,
                'actual_dense_oracle_coefficients_and_all_objectives_close':True,'native_reload_decoder_and6_prefixes_bits_exact':True,
                'actual_training_inference_rows':len(test),'native_model_sha256':sha(native),'state_sha256':sha(state_path),
                'process_RSS_GiB':psutil.Process().memory_info().rss/2**30,'actual_official_scores':0,'full_annual_model_not_claimed':True}
            create(OUT/(name+'_verification.json'),record);records.append(record)
            print(f'Actual200003-row {name}: fit{elapsed:.3f}s; dense oracle and native/cold controls passed',flush=True)
        scope.reverify()
    create(OUT/'verification.json',{'status':'passed_actual2_own2025_200003row_HuberIRLS64_dense_native_and12_prefix_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_probe_native_fits':2,
        'own_full_window_rows_rechecked':info['training_rows'],'last_training_label_date':info['last_training_label_date'],
        'last_training_label_end':info['last_training_label_end'],'exclusive_cutoff':info['exclusive_cutoff'],
        'RSS_before_fits_GiB':rss_before/2**30,'elapsed_seconds':time.perf_counter()-started,'actual_official_scores':0,
        'no_future_X_or_Y_read':True,'finite_recipe_probe_not_global_resource_boundary':True,'full10_bank_not_yet_admitted':True})
    create(A/'actual_nonflag_HuberIRLS64_actual200k_location_v1_20261008.json',{
        'status':'passed_actual2_own_mature200003row_HuberIRLS64_probe_on_E','output':str(OUT),
        'verification_sha256':sha(OUT/'verification.json'),'actual_official_scores':0})


if __name__=='__main__':main()
