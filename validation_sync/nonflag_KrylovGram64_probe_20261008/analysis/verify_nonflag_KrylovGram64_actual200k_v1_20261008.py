"""Actual matured training probe, independent projected solver and saved-native prefix controls."""
from pathlib import Path
import os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/nonflag_KrylovGram64_actual200k_v1_20261008')

def main():
    import numpy as np,joblib,psutil
    from threadpoolctl import threadpool_limits
    from nonflag_HuberIRLS64_own_window_v1_20261008 import input_paths,load_population,admitted_window
    from verify_nonflag_KrylovGram64_small_v1_20261008 import dense_oracle
    import nonflag_KrylovGram64_streamed_v1_20261008 as native
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    pointer_path=A/'actual_nonflag_KrylovGram64_small_location_v1_20261008.json';pointer=read(pointer_path)
    small_path=Path(pointer['output'])/'verification.json';small=read(small_path)
    assert sha(small_path)==pointer['verification_sha256'] and small['actual_synthetic_native_fits']==12
    sources=[Path(__file__),Path(native.__file__),A/'verify_nonflag_KrylovGram64_small_v1_20261008.py',pointer_path,small_path,*input_paths([2025])]
    pins={str(p):sha(p) for p in sources};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual200k_probe.json',{'input_sha256':pins,'configurations':native.CONFIGS,
        'probe_rows':200003,'own_training_window_year':2025,'future_X_and_Y_read':False,'actual_official_scores':0,
        'preprocessing_from_same_full_own2025_training_window_not_validation':True})
    records=[];started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        population=load_population();window,target,preprocessing,features,info=admitted_window(population,2025)
        raw=window[:200003];y=target[:len(raw)];test=np.asarray(window[-10017:]).copy()
        tick=time.perf_counter();stats=native.accumulate(raw,preprocessing,y);statistics_seconds=time.perf_counter()-tick
        for name,cfg in native.CONFIGS.items():
            tick=time.perf_counter();model,metadata=native.fit_from_statistics(stats,cfg);fit_seconds=time.perf_counter()-tick
            tick=time.perf_counter();coef,intercept=dense_oracle(raw,preprocessing,y,cfg['maximum_iterations'],model.alpha);oracle_seconds=time.perf_counter()-tick
            assert np.allclose(model.coef_,coef,rtol=2e-8,atol=2e-10) and np.isclose(model.intercept_,intercept,rtol=2e-8,atol=2e-10),(name,np.max(np.abs(model.coef_-coef)))
            bundle={'model':model,'preprocessing':preprocessing,'features':features};path=OUT/(name+'.joblib');state_path=OUT/(name+'_state.json')
            joblib.dump(bundle,path);create(state_path,native.export(bundle));saved=joblib.load(path);state=read(state_path)
            value=native.predict_native(bundle,test)
            for count in (0,1,79,8191,8192,10017):
                for check in (native.predict_native(saved,test[:count]),native.predict_decoded(state,test[:count])):
                    assert np.array_equal(value[:count].view('u8'),check.view('u8'))
            row={'name':name,'configuration':cfg,'training_rows':len(y),'shared_statistics_seconds':statistics_seconds,
                'head_fit_seconds_after_shared_statistics':fit_seconds,'independent_dense_projected_seconds':oracle_seconds,'metadata':metadata,
                'actual_dense_projected_coefficients_and_intercept_close':True,'native_reload_decoder_six_prefixes_bits_exact':True,
                'prediction_training_rows':len(test),'native_model_sha256':sha(path),'state_sha256':sha(state_path),
                'process_RSS_GiB':psutil.Process().memory_info().rss/2**30,'actual_official_scores':0,'full_annual_model_not_claimed':True}
            create(OUT/(name+'_verification.json'),row);records.append(row)
            print(f'Actual200003 training-row {name}: shared Gram{statistics_seconds:.3f}s, head{fit_seconds:.4f}s; independent projected solve and6 prefixes passed.',flush=True)
        scope.reverify()
    create(OUT/'verification.json',{'status':'passed_actual4_own2025_200003row_KrylovGram64_projected_native_and24_prefix_controls',
        'input_sha256':pins,'records':records,'actual_probe_native_fits':4,'own_full_window_rows_rechecked':info['training_rows'],
        'last_training_label_date':info['last_training_label_date'],'last_training_label_end':info['last_training_label_end'],
        'exclusive_cutoff':info['exclusive_cutoff'],'shared_statistics_seconds':statistics_seconds,'elapsed_seconds':time.perf_counter()-started,
        'actual_official_scores':0,'no_future_X_or_Y_read':True,'finite_recipe_probe_not_global_resource_boundary':True,
        'full_annual_bank_not_yet_admitted':True})
    create(A/'actual_nonflag_KrylovGram64_actual200k_location_v1_20261008.json',{'status':'passed_actual4_own_mature_krylov200k_probe_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_official_scores':0})

if __name__=='__main__':main()
