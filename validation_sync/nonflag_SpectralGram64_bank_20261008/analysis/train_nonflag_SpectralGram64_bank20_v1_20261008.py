"""Ten CPU2 fixed-Huber fits on verified own-mature teacher106 residual windows; no quality scores."""
from pathlib import Path
import os,sys,time,gc
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/nonflag_SpectralGram64_bank20_v1_20261008')


def main():
    import numpy as np,joblib,psutil
    from threadpoolctl import threadpool_limits
    from nonflag_HuberIRLS64_own_window_v1_20261008 import input_paths,load_population,admitted_window,atomic
    from nonflag_SpectralGram64_streamed_v1_20261008 import CONFIGS,accumulate,fit_from_statistics,export,predict_native,predict_decoded
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    plan_path=A/'nonflag_SpectralGram64_bank20_plan_v1_20261008.json';plan=read(plan_path)
    assert plan['native_fit_years']==list(range(2021,2026)) and plan['configurations']==CONFIGS and plan['actual_declared_native_fits']==20
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    probe_pointer=A/'actual_nonflag_SpectralGram64_actual200k_location_v1_20261008.json'
    pointer=read(probe_pointer);probe_path=Path(pointer['output'])/'verification.json';probe=read(probe_path)
    assert sha(probe_path)==pointer['verification_sha256']
    assert probe['status']=='passed_actual4_own2025_200003row_SpectralGram64_dense_SVD_native_and24_prefix_controls'
    assert len(probe['records'])==4 and probe['actual_official_scores']==0
    for item in probe['records']:
        assert item['configuration']==CONFIGS[item['name']] and item['actual_dense_SVD_coefficients_and_intercept_close']
        assert item['native_reload_decoder_six_prefixes_bits_exact']
    for path,digest in probe['input_sha256'].items():assert sha(path)==digest,path
    paths=[Path(__file__),plan_path,probe_pointer,probe_path,*input_paths(plan['native_fit_years'])]
    pins={str(path):sha(path) for path in dict.fromkeys(paths)}
    alignment=read(A/'nonflag_residual_HGB_bank10_20261007/actual_teacher_target_and_key_alignment.json')
    assert pins[str(Path(alignment['feature_cache']))]==alignment['feature_cache_sha256']
    assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual10_fits.json',{'input_sha256':pins,'plan':plan,'actual200k_probe_sha256':sha(probe_path),
        'own_mature_feature_and_target_alignment_rechecked_before_every_year':True,'test_labels_read':False,
        'actual_declared_native_fits':20,'actual_official_scores':0,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    records=[];started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        while psutil.virtual_memory().available<8*2**30:
            atomic(OUT/'actual_stage.json',{'status':'waiting_for8GiB_before_population','actual_completed_native_fits':0});time.sleep(10)
        population=load_population();frame=population['frame'];kd=population['key_dates'];outputs={}
        for name in CONFIGS:
            (OUT/name).mkdir();array=np.lib.format.open_memmap(OUT/name/'nonflag_oof_predictions.npy',mode='w+',dtype=np.float64,shape=(len(frame),))
            array[:]=0.;array.flush();outputs[name]=array
        for year in plan['native_fit_years']:
            while psutil.virtual_memory().available<6*2**30:
                atomic(OUT/'actual_stage.json',{'status':'waiting_for6GiB_before_streamed_fit','year':year,
                    'actual_completed_native_fits':len(records),'available_RAM_GiB':psutil.virtual_memory().available/2**30});time.sleep(10)
            window,target,preprocessing,features,old_info=admitted_window(population,year)
            selected=kd//10000==year;positions=population['positions'][selected]
            test=np.asarray(population['raw'][selected]) if year<2025 else np.asarray(window[:1000]).copy()
            statistics_started=time.perf_counter();statistics=accumulate(window,preprocessing,target);statistics_seconds=time.perf_counter()-statistics_started
            for name,cfg in CONFIGS.items():
                atomic(OUT/'actual_stage.json',{'status':'actual_own_mature_streamed_SpectralGram64_fit','name':name,'year':year,
                    'training_rows':len(target),'actual_completed_native_fits':len(records),'expected_native_fits':20,
                    'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'available_RAM_GiB':psutil.virtual_memory().available/2**30})
                t=time.perf_counter();model,metadata=fit_from_statistics(statistics,cfg);elapsed=time.perf_counter()-t
                native=OUT/name/f'model_{year}.joblib';state_path=OUT/name/f'independent_linear_state_{year}.json'
                bundle={'model':model,'preprocessing':preprocessing,'features':features};joblib.dump(bundle,native);create(state_path,export(bundle))
                saved=joblib.load(native);state=read(state_path);actual=np.empty(len(test),dtype=np.float64)
                for left in range(0,len(test),65536):
                    block=test[left:left+65536];value=predict_native(bundle,block)
                    assert np.array_equal(value.view('u8'),predict_native(saved,block).view('u8'))
                    assert np.array_equal(value.view('u8'),predict_decoded(state,block).view('u8'));actual[left:left+len(block)]=value
                cold=[]
                if year<2025:
                    outputs[name][positions]=actual;outputs[name].flush()
                for count in ((1,80,180) if year<2025 else (1,79,999)):
                    n=int(np.count_nonzero(kd[selected]<=np.unique(kd[selected])[min(count,len(np.unique(kd[selected])))-1])) if year<2025 else count
                    for left in range(0,n,65536):
                        right=min(n,left+65536);value=predict_native(saved,test[left:right]);decoded=predict_decoded(state,test[left:right])
                        assert np.array_equal(value.view('u8'),actual[left:right].view('u8')) and np.array_equal(value.view('u8'),decoded.view('u8'))
                    cold.append({'annual_days_or_training_sample_rows':count,'actual_rows':n,'native_reload_decoder_bits_exact':True})
                item={'name':name,'year':year,'parameters':model.get_params(),'features':features,'training_rows':len(target),
                    'last_training_label_date':old_info['last_training_label_date'],'last_training_label_end':old_info['last_training_label_end'],
                    'exclusive_cutoff':old_info['exclusive_cutoff'],'training_matrix_numeric_sha256':old_info['training_matrix_numeric_sha256'],
                    'training_target_numeric_sha256':old_info['training_target_numeric_sha256'],'native_model_path':str(native),
                    'native_model_sha256':sha(native),'independent_linear_state_path':str(state_path),'independent_linear_state_sha256':sha(state_path),
                    'preprocessing_reused_from_identical_own_mature_window':True,'every_cached_training_row_rechecked':True,
                    'fit_seconds_after_shared_statistics':elapsed,'shared_statistics_seconds':statistics_seconds,'prediction_control_rows':len(test),'native_reload_independent_all_prediction_bits_exact':True,
                    'actual_cold_prefix_controls':cold,'training_solver_metadata':metadata,'new_native_fits':1,
                    'actual2025_controls_use_only1000_training_rows':year==2025,'test_labels_read':False}
                create(OUT/name/f'info_{year}.json',item);records.append(item)
                print(f'Actual own-mature spectral fit {len(records)}/20: {name} {year}, {len(target)} rows, {elapsed:.3f}s; saved/native/decoder/cold controls exact',flush=True)
                del model,bundle,saved,state,actual;gc.collect()
            window._mmap.close();del window,target,test,statistics;gc.collect()
        flags=frame['flag_limit_up'].to_numpy();dates=population['dates']
        for name,array in outputs.items():
            assert np.isfinite(array).all() and np.all(array[flags==1]==0.) and np.all(array[dates<20210101]==0.)
            array.flush();create(OUT/name/'oof_verification.json',{'status':'passed_actual5635800_nonflag_SpectralGram64_OOF',
                'rows':len(array),'days':1212,'stocks':4650,'prediction_array_sha256':sha(OUT/name/'nonflag_oof_predictions.npy'),
                'flagged_and2020_zero_residual':True,'actual_annual_native_reload_independent_and_cold_controls':True,
                'actual_official_scores':0,'test_labels_read':False})
        assert len(records)==20;scope.reverify()
    create(OUT/'verification.json',{'status':'passed_actual20_own_mature_SpectralGram64_native_reload_decoder_and_prefix_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'configurations':CONFIGS,'actual_models':records,
        'actual_native_fits':20,'actual_full_OOF_heads':4,'elapsed_seconds':time.perf_counter()-started,'new_large_feature_caches':0,
        'actual_official_scores':0,'full_selected_candidate_complete_round_and_future_inference_not_yet_qualified':True,
        'no_future_X_or_Y_read':True,'finite_recipe_not_global_optimization_exhaustion':True})
    create(A/'actual_nonflag_SpectralGram64_bank20_location_v1_20261008.json',{
        'status':'passed_actual20_own_mature_SpectralGram64_bank_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),
        'actual_native_fits':20,'actual_official_scores':0})


if __name__=='__main__':main()
