"""Freeze and launch four signed constrained-ridge heads on five own mature windows."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    folder=A/'service_owned_workflows_20261006/nonflag_ConeRidge64_actual200k_v2_20261008'
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    import nonflag_ConeRidge64_streamed_v1_20261008 as native
    small=A/'actual_nonflag_ConeRidge64_small_location_v2_20261008.json'
    probe=A/'actual_nonflag_ConeRidge64_actual200k_location_v2_20261008.json'
    proof_path=Path(read(probe)['output'])/'verification.json';proof=read(proof_path)
    assert sha(proof_path)==read(probe)['verification_sha256'] and proof['actual_probe_native_fits']==4
    assert proof['actual_official_scores']==0
    assert all(row['actual_dense_BVLS_coefficients_and_intercept_close'] and row['native_reload_decoder_six_prefixes_bits_exact'] for row in proof['records'])
    source=A/'train_nonflag_SpectralGram64_bank20_v1_20261008.py'
    text=source.read_text(encoding='utf8').replace('SpectralGram64','ConeRidge64').replace('dense_SVD','dense_BVLS')
    text=text.replace('actual_nonflag_ConeRidge64_actual200k_location_v1_20261008','actual_nonflag_ConeRidge64_actual200k_location_v2_20261008')
    text=text.replace('frozen_before_actual10_fits','frozen_before_actual20_fits')
    text=text.replace('Ten CPU2 fixed-Huber fits','Twenty CPU2 coefficient-constrained ridge fits').replace('own-mature spectral fit','own-mature constrained ridge fit')
    target=A/'train_nonflag_ConeRidge64_bank20_v1_20261008.py'
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    sources=[Path(__file__),source,target,Path(native.__file__),small,probe,
        Path(read(small)['output'])/'verification.json',proof_path,
        A/'verify_nonflag_ConeRidge64_small_v2_20261008.py',A/'verify_nonflag_ConeRidge64_actual200k_v2_20261008.py',
        A/'nonflag_SpectralGram64_streamed_v1_20261008.py',A/'nonflag_HuberIRLS64_own_window_v1_20261008.py',
        A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py']
    plan=A/'nonflag_ConeRidge64_bank20_plan_v1_20261008.json'
    create(plan,{'status':'frozen_before_actual20_own_mature_constrained_ridge_fits_and_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'configurations':native.CONFIGS,'native_fit_years':list(range(2021,2026)),'actual_declared_native_fits':20,
        'target':'provided_y_rank_plus_half_minus_teacher106_daily_average_rank_over_all_N',
        'universe':'valid_nonflag_finite_provided_train_target','training_preprocessing':'verified_identical_own_mature_window_only',
        'purge_days':1,'validation_years':list(range(2020,2025)),'first2020_identity_residual':True,
        'shared_centered_Gram_per_own_window':True,'native_64dim_NNLS_and_KKT_constraints':True,
        'full_annual_prefix_checks':[1,80,180],'final2025_checks_training_only_rows':[1,79,999],
        'large_outputs_on_E':True,'additional_large_feature_caches':0,'actual_official_scores':0,
        'test_labels_read':False,'global_exhaustion_claimed':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*sources,plan]}
    row=start('nonflag_ConeRidge64_bank20_v1_20261008',target.name,[],pins)
    create(A/'actual_nonflag_ConeRidge64_bank20_hidden_launch_v1_20261008.json',row)
    print('Twenty own-mature constrained ridge fits frozen and dispatched; CPU2, E outputs, no console.',flush=True)

if __name__=='__main__':main()
