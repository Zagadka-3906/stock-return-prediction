"""Actual future-training-label poison and independently reconstructed maturity populations; no refit or test labels."""
from pathlib import Path
import os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/HuberIRLS64_10_causal_inputs_v1_20261008')


def main():
    folder=A/'service_owned_workflows_20261006/nonflag_HuberIRLS64_actual_bank10_v1_20261008'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    import numpy as np
    from threadpoolctl import threadpool_limits
    from nonflag_HuberIRLS64_own_window_v1_20261008 import input_paths,load_population,admitted_window,numeric_sha
    bank=Path(read(A/'actual_nonflag_HuberIRLS64_bank10_location_v1_20261008.json')['output']);proof=read(bank/'verification.json')
    assert proof['actual_native_fits']==10 and proof['actual_full_OOF_heads']==2 and proof['actual_official_scores']==0
    sources=[Path(__file__),bank/'verification.json',bank/'frozen_before_actual10_fits.json',
        *input_paths(list(range(2021,2026))),*bank.glob('*/info_*.json')];pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    assert not OUT.exists();OUT.mkdir();create(OUT/'frozen_before_actual_causal_controls.json',{
        'input_sha256':pins,'actual_new_native_fits':0,'actual_official_scores':0,'future_test_X_and_Y_read':False})
    records=[];started=time.perf_counter()
    with threadpool_limits(limits=2):
        population=load_population();kd=population['key_dates'];all_days=population['all_days'];target=population['target']
        available_index=np.searchsorted(all_days,kd)+1
        independent_label_end=np.where(available_index<len(all_days),all_days[np.minimum(available_index,len(all_days)-1)],99999999)
        for year in range(2021,2026):
            window,y,prep,features,info=admitted_window(population,year);cutoff=info['exclusive_cutoff']
            original=(kd<cutoff)&population['eligible']
            mature=(kd<cutoff)&(independent_label_end<=cutoff)&population['eligible']
            assert np.array_equal(original,mature)
            assert numeric_sha(y)==info['training_target_numeric_sha256']
            poison_controls=[]
            for variant in ('nonfinite_nan','huge_finite'):
                poisoned=target.copy();poisoned[kd>=cutoff]=np.nan if variant=='nonfinite_nan' else 1e100
                modified=(kd<cutoff)&np.isfinite(poisoned)&population['frame'].filter(__import__('polars').col('flag_limit_up')!=1)['price_valid'].to_numpy()
                assert np.array_equal(modified,original) and numeric_sha(poisoned[modified])==numeric_sha(y)
                poison_controls.append({'variant':variant,'actual_changed_later_training_rows':int(np.count_nonzero(kd>=cutoff)),
                    'own_training_population_and_target_bytes_unchanged':True})
            for name in proof['configurations']:
                native_info=read(bank/name/f'info_{year}.json')
                for key in ('training_rows','last_training_label_date','last_training_label_end','exclusive_cutoff','training_matrix_numeric_sha256','training_target_numeric_sha256','features'):
                    assert native_info[key]==info[key],(name,year,key)
                assert sha(native_info['native_model_path'])==native_info['native_model_sha256']
                assert native_info['parameters']['target_not_clipped'] and not native_info['parameters']['intercept_penalized']
            item={'year':year,'training_rows':len(y),'last_label_date':info['last_training_label_date'],
                'last_label_end':info['last_training_label_end'],'exclusive_cutoff':cutoff,'independent_next_trading_day_maturity_population_exact':True,
                'every_cached_own_window_row_and_prepared_feature_target_hash_rechecked':True,'poison_controls':poison_controls,
                'both_saved_native_fit_metadata_and_SHA_exact':True,'new_native_refits':0}
            create(OUT/f'year{year}.json',item);records.append(item);window._mmap.close()
            print(f'Actual Huber causal window {year}: independently matured population and two later-label poison variants exact',flush=True)
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual5_Huber_own_windows10_later_label_poison_and10_native_metadata_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,
        'actual_own_window_maturity_controls':5,'actual_future_training_label_poison_controls':10,'actual_native_models_audited':10,
        'own_training_preprocessing_reused_only_after_identical_full_prepared_feature_hashes':True,
        'native_refits_not_claimed_by_input_poison_control':True,'actual_official_scores':0,'elapsed_seconds':time.perf_counter()-started,
        'future_test_X_and_Y_read':False,'complete_selected_future_pipeline_still_unqualified':True})
    create(A/'actual_HuberIRLS64_10_causal_inputs_location_v1_20261008.json',{
        'status':'passed_actual5_maturity10_later_training_label_poison10_native_audits_on_E','output':str(OUT),
        'verification_sha256':sha(OUT/'verification.json'),'actual_official_scores':0})


if __name__=='__main__':main()
