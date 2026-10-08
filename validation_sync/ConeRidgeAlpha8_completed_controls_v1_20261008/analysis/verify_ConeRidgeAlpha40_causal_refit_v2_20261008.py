"""Poison later TRAIN labels, refit all40 heads on unchanged own windows, check saved coefficients."""
from pathlib import Path
import os,sys,time,gc
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/ConeRidgeAlpha40_causal_refit_v2_20261008')


def main():
    service=A/'service_owned_workflows_20261006/nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008'
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(10)
    assert read(service/'service_execution.json')['status']=='passed'
    import numpy as np,joblib
    from threadpoolctl import threadpool_limits
    from nonflag_HuberIRLS64_own_window_v1_20261008 import load_population,admitted_window,input_paths,numeric_sha
    import nonflag_ConeRidgeAlpha8_64_streamed_v1_20261008 as native
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    pointer=A/'actual_nonflag_ConeRidgeAlpha8_64_bank40_location_v2_20261008.json';bank=Path(read(pointer)['output'])
    proof=read(bank/'verification.json');assert proof['actual_native_fits']==40 and proof['actual_full_OOF_heads']==8
    sources=[Path(__file__),Path(native.__file__),pointer,bank/'verification.json',*input_paths(range(2021,2026))]
    for row in proof['actual_models']:sources += [bank/row['name']/f'info_{row["year"]}.json',Path(row['native_model_path'])]
    pins={str(p):sha(p) for p in sources};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_train_label_poison_refits.json',{'input_sha256':pins,'actual_declared_same_configuration_refit_controls':40,
        'new_unique_model_candidates':0,'actual_future_X_and_Y_read':False,'new_official_scores':0})
    records=[];windows=[];started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        population=load_population();original_target=population['target'];kd=population['key_dates']
        for year in range(2021,2026):
            window,target,preprocessing,features,info=admitted_window(population,year)
            cutoff=info['exclusive_cutoff'];mature_indices=np.flatnonzero((kd<cutoff)&population['eligible'])
            assert kd[mature_indices].max()==info['last_training_label_date']<cutoff and info['last_training_label_end']<=cutoff
            poisoned=original_target.copy();future=kd>=cutoff;assert future.any()
            poisoned[future]=np.where(np.arange(len(kd))[future]%2,1e6,-1e6)
            own_poisoned=np.asarray(poisoned[mature_indices],dtype=np.float64)
            assert np.array_equal(own_poisoned.view('u8'),target.view('u8')) and numeric_sha(own_poisoned)==info['training_target_numeric_sha256']
            stats=native.accumulate(window,preprocessing,own_poisoned)
            for name,cfg in native.CONFIGS.items():
                row=read(bank/name/f'info_{year}.json');saved=joblib.load(row['native_model_path']);model,metadata=native.fit_from_statistics(stats,cfg)
                assert saved['features']==features and saved['preprocessing']==preprocessing
                assert np.array_equal(model.coef_.view('u8'),saved['model'].coef_.view('u8'))
                assert np.array_equal(np.array([model.intercept_]).view('u8'),np.array([saved['model'].intercept_]).view('u8'))
                assert np.array_equal(model.nonnegative_parameters_.view('u8'),saved['model'].nonnegative_parameters_.view('u8'))
                assert np.all(model.nonnegative_parameters_>=0.) and metadata['actual_relative_KKT_violation']<1e-10
                bundle={'model':model,'preprocessing':preprocessing,'features':features};test=window[:1000]
                assert np.array_equal(native.predict_native(bundle,test).view('u8'),native.predict_native(saved,test).view('u8'))
                record={'year':year,'name':name,'poisoned_later_TRAIN_rows':int(future.sum()),'own_training_rows':len(target),
                    'own_target_numeric_SHA_unchanged':True,'refit_coefficients_intercept_and_training_prediction_bits_exact':True,
                    'same_configuration_control_not_additional_unique_candidate':True}
                create(OUT/f'control{len(records)+1}.json',record);records.append(record)
            windows.append({'year':year,'cutoff':cutoff,'last_label_date':info['last_training_label_date'],
                'last_label_end':info['last_training_label_end'],'training_rows':len(target),'later_TRAIN_rows_poisoned':int(future.sum())})
            print(f'Coefficient-constrained ridge causal window{year}: eight saved native refits exactly survive poisoning{future.sum()} later TRAIN labels.',flush=True)
            window._mmap.close();del window,target,stats,poisoned,own_poisoned;gc.collect()
        scope.reverify()
    assert len(records)==40 and len(windows)==5
    create(OUT/'verification.json',{'status':'passed_actual5_mature_windows_and40_later_TRAIN_label_poison_native_refit_controls',
        'input_sha256':pins,'windows':windows,'records':records,'actual_causal_same_configuration_refit_controls':40,
        'actual_maturity_windows':5,'elapsed_seconds':time.perf_counter()-started,'new_unique_saved_model_candidates':0,
        'new_official_scores':0,'actual_future_X_and_Y_read':False})
    create(A/'actual_ConeRidgeAlpha40_causal_refit_location_v2_20261008.json',{'status':'passed_actual40_constrained_ridge_causal_refit_controls_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_official_scores':0})


if __name__=='__main__':main()
