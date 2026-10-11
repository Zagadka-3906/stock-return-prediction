"""Reuse verified past-only raw feature windows for ten low-cost Ridge fits."""
from pathlib import Path
import os,sys,time,gc,hashlib
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'): os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from atomic_optimization_observer_writes_20261005 import write

def numeric_sha(x):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(x)).cast('B')).hexdigest()

def main():
    import numpy as np,polars as pl,psutil,joblib
    from nonflag_residual_RFF128_codec_20261007 import make_model
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    from nonflag_residual_HGB_preprocessing_20261007 import prepare
    from nonflag_residual_RFF128_codec_20261007 import export,predict_native,predict_decoded
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    admission=A/'nonflag_residual_RFF128Hi10_source_admission_v1_20261007.json'; proof=read(admission)
    assert proof['status']=='passed_actual2_RFF128Hi_codec_controls_and10_past_only_fit_admission'
    for p,d in proof['input_sha256'].items(): assert sha(p)==d,p
    plan=read(A/'nonflag_residual_RFF128Hi10_plan_20261007.json')
    out=A/'nonflag_residual_RFF128Hi_bank10_20261007'; assert not out.exists(); out.mkdir()
    bank=A/'nonflag_residual_HGB_bank10_20261007'; old=read(bank/'verification.json')
    assert old['actual_native_fits']==10 and old['status'].startswith('passed_actual10_')
    alignment=read(bank/'actual_teacher_target_and_key_alignment.json')
    raw_path=Path(alignment['feature_cache']); assert sha(raw_path)==alignment['feature_cache_sha256']
    cache=raw_path.parent
    paths=[Path(p) for p in proof['input_sha256']]
    paths += [bank/'verification.json',bank/'actual_teacher_target_and_key_alignment.json',raw_path,
              A/'connected_validation_20261002/combined_fold_frame.parquet',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'run.py']
    for year in plan['native_fit_years']:
        info_path=bank/'nonflag_residual_hgb7_squared'/f'info_{year}.json'
        info=read(info_path); paths.extend([info_path,Path(info['native_model_path']),cache/f'mature_training_features64_{year}.npy'])
        assert sha(info['native_model_path'])==info['native_model_sha256']
    pins={str(p):sha(p) for p in dict.fromkeys(paths)}
    create(out/'frozen_before_actual_training.json',{'input_sha256':pins,'plan':plan,'new_large_feature_caches':0,
        'test_labels_read':False,'actual_declared_native_fits':10,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    records=[]; started=time.perf_counter()
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        full=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid']).with_row_index('oof_position')
        assert (len(full),full['trade_date'].n_unique(),full['ts_code'].n_unique())==(5635800,1212,4650)
        keys=full.filter(pl.col('flag_limit_up')!=1)
        positions=keys['oof_position'].to_numpy(); kd=keys['trade_date'].to_numpy(); valid=keys['price_valid'].to_numpy()
        raw=np.load(raw_path,mmap_mode='r'); assert raw.shape==(len(keys),64)
        assert numeric_sha(np.asarray(raw[:,63]))==alignment['teacher_feature_numeric_sha256']
        labels=keys.select('ts_code','trade_date').join(pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('trade_date')>=20200101)).select('ts_code','trade_date','y_rank').collect(),on=['ts_code','trade_date'],how='left',validate='1:1',maintain_order='left')
        y=labels['y_rank'].to_numpy().astype(float)+.5-raw[:,63]
        assert numeric_sha(y)==alignment['target_numeric_sha256']
        eligible=np.isfinite(y)&valid; del labels; gc.collect()
        raw._mmap.close();raw=None;gc.collect()
        all_days=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        oof_days=full['trade_date'].unique().sort().to_numpy()
        outputs={}
        for name in plan['configurations']:
            (out/name).mkdir(); outputs[name]=np.lib.format.open_memmap(out/name/'nonflag_oof_predictions.npy',mode='w+',dtype=np.float64,shape=(len(full),)); outputs[name][:]=0.; outputs[name].flush()
        for year in plan['native_fit_years']:
            cutoff=fold_cutoff(year); train=(kd<cutoff)&eligible; indices=np.flatnonzero(train)
            old_info=read(bank/'nonflag_residual_hgb7_squared'/f'info_{year}.json')
            last=int(kd[indices].max()); label_end=int(all_days[np.searchsorted(all_days,last)+1])
            assert len(indices)==old_info['training_rows'] and last==old_info['last_training_label_date'] and label_end<=cutoff
            while psutil.virtual_memory().available<14*2**30:
                write(out/'actual_stage.json',{'status':'waiting_for_at_least14GiB_available_RAM','available_RAM_GiB':psutil.virtual_memory().available/2**30,'actual_completed_native_fits':len(records),'expected_fits':10}); time.sleep(10)
            assert raw is None
            raw=np.load(raw_path,mmap_mode='r')
            window=np.load(cache/f'mature_training_features64_{year}.npy',mmap_mode='r')
            saved_hgb=joblib.load(old_info['native_model_path']); prep=saved_hgb['preprocessing']; feature_names=saved_hgb['features']; del saved_hgb
            assert window.shape==(len(indices),64)
            # Confirm every cached row has the same key-aligned provided features.
            for left in range(0,len(indices),8192):
                part=raw[indices[left:left+8192]]
                assert np.array_equal(window[left:left+len(part)].view('u8'),part.view('u8'))
            bx=prepare(window,prep); train_y=y[train]
            assert numeric_sha(bx)==old_info['training_matrix_numeric_sha256']
            assert numeric_sha(train_y)==old_info['training_target_numeric_sha256']
            selected=kd//10000==year; selected_positions=positions[selected]
            if year<2025: test=np.asarray(raw[selected])
            else: test=np.asarray(window[:1000]).copy()
            assert not np.shares_memory(bx,window) and not np.shares_memory(test,raw) and not np.shares_memory(test,window)
            raw._mmap.close();raw=None
            window._mmap.close();window=None;gc.collect()
            for name,cfg in plan['configurations'].items():
                params={**cfg,'alpha':len(indices)*cfg['alpha_per_training_row']}
                write(out/'actual_stage.json',{'status':'actual_nonflag_RFF128Hi_training','name':name,'year':year,'training_rows':len(indices),'actual_completed_native_fits':len(records),'expected_fits':10,'available_RAM_GiB':psutil.virtual_memory().available/2**30})
                t=time.perf_counter(); model=make_model(cfg,len(indices)).fit(bx,train_y); fit_seconds=time.perf_counter()-t
                native=out/name/f'model_{year}.joblib'; state_path=out/name/f'independent_random_fourier_linear_state_{year}.json'
                bundle={'model':model,'preprocessing':prep,'features':feature_names}; joblib.dump(bundle,native); create(state_path,export(bundle))
                saved=joblib.load(native); state=read(state_path); actual=np.empty(len(test),dtype=np.float64)
                for left in range(0,len(test),65536):
                    block=test[left:left+65536]; value=predict_native(bundle,block)
                    assert np.array_equal(value.view('u8'),predict_native(saved,block).view('u8'))
                    assert np.array_equal(value.view('u8'),predict_decoded(state,block).view('u8'))
                    actual[left:left+len(block)]=value
                controls=[]
                if year<2025:
                    outputs[name][selected_positions]=actual; outputs[name].flush()
                    for count in (80,260,975):
                        n=int(np.count_nonzero(kd[selected]<=oof_days[count-1]))
                        for left in range(0,n,65536):
                            right=min(n,left+65536); cold=predict_native(saved,test[left:right]); decoded=predict_decoded(state,test[left:right])
                            assert np.array_equal(cold.view('u8'),actual[left:right].view('u8')) and np.array_equal(cold.view('u8'),decoded.view('u8'))
                        controls.append({'days':count,'actual_nonflag_rows':n,'native_and_independent_prefix_bits_exact':True})
                item={'name':name,'year':year,'parameters':params,'features':feature_names,'training_rows':len(indices),
                    'last_training_label_date':last,'last_training_label_end':label_end,'exclusive_cutoff':cutoff,
                    'training_matrix_numeric_sha256':old_info['training_matrix_numeric_sha256'],'training_target_numeric_sha256':old_info['training_target_numeric_sha256'],
                    'native_model_path':str(native),'native_model_sha256':sha(native),'independent_random_fourier_linear_state_path':str(state_path),'independent_random_fourier_linear_state_sha256':sha(state_path),
                    'preprocessing_reused_from_identical_own_mature_window':True,'fit_seconds':fit_seconds,'prediction_control_rows':len(test),
                    'native_reload_independent_all_prediction_bits_exact':True,'actual_cold_prefix_controls':controls,'new_native_fits':1,'test_labels_read':False}
                create(out/name/f'info_{year}.json',item); records.append(item); print({'name':name,'year':year,'actual_fits':len(records),'fit_seconds':fit_seconds},flush=True)
                del model,bundle,saved,state,actual; gc.collect()
            del bx,window,train_y,test,indices; gc.collect()
        for name,array in outputs.items():
            assert np.all(array[full['flag_limit_up'].to_numpy()==1]==0.) and np.all(array[full['trade_date'].to_numpy()<20210101]==0.) and np.isfinite(array).all()
            array.flush(); create(out/name/'oof_verification.json',{'status':'passed_actual5635800_nonflag_residual_RFF128Hi_OOF','rows':len(array),'prediction_array_sha256':sha(out/name/'nonflag_oof_predictions.npy'),'flagged_and2020_zero_residual':True,'test_labels_read':False})
        assert len(records)==10; scope.reverify()
    create(out/'verification.json',{'status':'passed_actual10_nonflag_residual_RFF128Hi_mature_native_reload_independent_and_prefix_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'configurations':plan['configurations'],'actual_models':records,'actual_native_fits':10,'elapsed_seconds':time.perf_counter()-started,
        'new_large_feature_caches':0,'actual_official_scores':0,'future_candidate_and_complete_round_not_yet_qualified':True,'test_labels_read':False})
if __name__=='__main__': main()
