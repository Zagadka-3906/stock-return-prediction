"""Freeze four shared-statistics reorthogonalizedCG recipes and prepare twenty actual annual fits."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import nonflag_KrylovGram64_streamed_v2_20261008 as native
    small=A/'actual_nonflag_KrylovGram64_small_location_v2_20261008.json'
    probe=A/'actual_nonflag_KrylovGram64_actual200k_location_v2_20261008.json';proof=read(Path(read(probe)['output'])/'verification.json')
    assert proof['actual_probe_native_fits']==4 and proof['actual_official_scores']==0
    assert all(row['actual_dense_projected_coefficients_and_intercept_close'] and row['native_reload_decoder_six_prefixes_bits_exact'] for row in proof['records'])
    source=A/'train_nonflag_HuberIRLS64_bank10_v1_20261008.py';text=source.read_text(encoding='utf8')
    # Keep verified maturity, own-window preprocessing, full OOF placement and byte-lock scope.
    text=text.replace('nonflag_HuberIRLS64_bank10','nonflag_KrylovGram64_bank20')
    text=text.replace('nonflag_HuberIRLS64_streamed_v1_20261008','nonflag_KrylovGram64_streamed_v2_20261008')
    text=text.replace('CONFIGS,fit_streamed,export,predict_native,predict_decoded','CONFIGS,accumulate,fit_from_statistics,export,predict_native,predict_decoded')
    text=text.replace('actual_nonflag_HuberIRLS64_actual200k_location_v1_20261008','actual_nonflag_KrylovGram64_actual200k_location_v2_20261008')
    text=text.replace('passed_actual2_own2025_200003row_HuberIRLS64_dense_native_and12_prefix_controls','passed_actual4_own2025_200003row_KrylovGram64_projected_native_and24_prefix_controls')
    text=text.replace("len(probe['records'])==2","len(probe['records'])==4")
    text=text.replace("item['actual_dense_oracle_coefficients_and_all_objectives_close']","item['actual_dense_projected_coefficients_and_intercept_close']")
    text=text.replace("item['native_reload_decoder_and6_prefixes_bits_exact'] and item['fit_seconds']<180","item['native_reload_decoder_six_prefixes_bits_exact']")
    text=text.replace("plan['actual_declared_native_fits']==10","plan['actual_declared_native_fits']==20")
    text=text.replace("'actual_declared_native_fits':10","'actual_declared_native_fits':20").replace("'expected_native_fits':10","'expected_native_fits':20")
    text=text.replace('assert len(records)==10','assert len(records)==20').replace("'actual_native_fits':10","'actual_native_fits':20")
    text=text.replace('passed_actual10_own_mature_HuberIRLS64_native_reload_decoder_and_prefix_controls','passed_actual20_own_mature_KrylovGram64_native_reload_decoder_and_prefix_controls')
    text=text.replace('passed_actual10_own_mature_HuberIRLS64_bank_on_E','passed_actual20_own_mature_KrylovGram64_bank_on_E')
    text=text.replace('passed_actual5635800_nonflag_HuberIRLS64_OOF','passed_actual5635800_nonflag_KrylovGram64_OOF')
    text=text.replace('HuberIRLS64_fit','KrylovGram64_fit').replace('Actual own-mature Huber fit','Actual own-mature reorthogonalizedCG fit').replace('/10:', '/20:')
    text=text.replace("'actual_full_OOF_heads':2","'actual_full_OOF_heads':4")
    needle='            for name,cfg in CONFIGS.items():';assert text.count(needle)==1
    text=text.replace(needle,"            statistics_started=time.perf_counter();statistics=accumulate(window,preprocessing,target);statistics_seconds=time.perf_counter()-statistics_started\n"+needle)
    text=text.replace('fit_streamed(window,preprocessing,target,cfg)','fit_from_statistics(statistics,cfg)')
    needle="'fit_seconds':elapsed,'prediction_control_rows'";assert text.count(needle)==1
    text=text.replace(needle,"'fit_seconds_after_shared_statistics':elapsed,'shared_statistics_seconds':statistics_seconds,'prediction_control_rows'")
    text=text.replace('for count in ((80,260,975) if year<2025 else (1,79,999)):','for count in ((1,80,180) if year<2025 else (1,79,999)):')
    text=text.replace("population['oof_days'][count-1]","np.unique(kd[selected])[min(count,len(np.unique(kd[selected])))-1]")
    text=text.replace("'combined_days_or_training_sample_rows'","'annual_days_or_training_sample_rows'")
    text=text.replace('del window,target,test;gc.collect()','del window,target,test,statistics;gc.collect()')
    target=A/'train_nonflag_KrylovGram64_bank20_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec')
    target.write_text(text,encoding='utf8',newline='\n')
    sources=[Path(__file__),A/'prepare_nonflag_KrylovGram64_bank20_v2_20261008.py',A/'KrylovGram64_reorthogonalized_source_preparation_v2_20261008.json',source,target,Path(native.__file__),small,probe,
        Path(read(small)['output'])/'verification.json',Path(read(probe)['output'])/'verification.json',
        A/'nonflag_HuberIRLS64_own_window_v1_20261008.py',A/'nonflag_residual_HGB_preprocessing_20261007.py',
        A/'memory_bounded_numeric_preparation_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py']
    plan=A/'nonflag_KrylovGram64_bank20_plan_v2_20261008.json'
    create(plan,{'status':'frozen_before_actual20_own_mature_spectral_fits_and_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':{str(p):sha(p) for p in sources},'configurations':native.CONFIGS,'native_fit_years':list(range(2021,2026)),
        'actual_declared_native_fits':20,'target':'provided_y_rank_plus_half_minus_teacher106_daily_average_rank_over_all_N',
        'universe':'valid_nonflag_finite_provided_train_target','training_preprocessing':'identical_verified_own_mature_window_only',
        'purge_days':1,'validation_years':list(range(2020,2025)),'first2020_identity_residual':True,
        'shared_Gram_per_own_window':True,'full_annual_prefix_checks':[1,80,180],
        'final2025_checks_training_only_rows':[1,79,999],'large_outputs_on_E':True,'additional_large_feature_caches':0,
        'actual_official_scores':0,'test_labels_read':False,'global_exhaustion_claimed':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*sources,plan]}
    row=start('nonflag_KrylovGram64_bank20_v2_20261008',target.name,[],pins)
    create(A/'actual_nonflag_KrylovGram64_bank20_hidden_launch_v2_20261008.json',row)
    print('Twenty own-mature reorthogonalizedCG fits frozen and dispatched, one shared Gram per year, CPU2 only.',flush=True)


if __name__=='__main__':main()
