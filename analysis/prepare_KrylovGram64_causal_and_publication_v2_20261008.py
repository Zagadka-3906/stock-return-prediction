"""Queue real20-refit causality controls and publish every passed or rejected probe to main."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    bank_launch=A/'actual_nonflag_KrylovGram64_bank20_hidden_launch_v3_20261008.json';assert owned(read(bank_launch))
    source=A/'verify_SpectralGram20_causal_refit_v1_20261008.py';text=source.read_text(encoding='utf8')
    text=text.replace('nonflag_SpectralGram64_streamed_v1_20261008','nonflag_KrylovGram64_streamed_v2_20261008')
    text=text.replace('nonflag_SpectralGram64_bank20_location_v1_20261008','nonflag_KrylovGram64_bank20_location_v3_20261008')
    text=text.replace('SpectralGram20_causal_refit_v1_20261008','KrylovGram20_causal_refit_v2_20261008').replace('SpectralGram20_causal_refit_location_v1_20261008','KrylovGram20_causal_refit_location_v2_20261008')
    text=text.replace('read,sha,create','read,sha,create,owned')
    text=text.replace('def main():\n',"def main():\n    service=A/'service_owned_workflows_20261006/nonflag_KrylovGram64_bank20_v3_20261008'\n    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(10)\n    assert read(service/'service_execution.json')['status']=='passed'\n")
    text=text.replace("                assert np.array_equal(model.training_basis_.view('u8'),saved['model'].training_basis_.view('u8'))", "                assert model.actual_iterations_==saved['model'].actual_iterations_")
    text=text.replace('refit_coefficients_intercept_eigen_basis_and_training_prediction_bits_exact','refit_coefficients_intercept_and_training_prediction_bits_exact')
    text=text.replace('Spectral causal','ReorthogonalizedCG causal').replace('passed_actual20_spectral_causal','passed_actual20_reorthogonalizedCG_causal')
    causal=A/'verify_KrylovGram20_causal_refit_v2_20261008.py';assert not causal.exists();compile(text,str(causal),'exec');causal.write_text(text,encoding='utf8',newline='\n')
    source_publisher=A/'publish_nonflag_SpectralGram64_controls_v1_20261008.py';text=source_publisher.read_text(encoding='utf8')
    replacements={
        'nonflag_SpectralGram64_streamed_v1_20261008':'nonflag_KrylovGram64_streamed_v2_20261008',
        'verify_nonflag_SpectralGram64_small_v1_20261008':'verify_nonflag_KrylovGram64_small_v2_20261008',
        'verify_nonflag_SpectralGram64_actual200k_v1_20261008':'verify_nonflag_KrylovGram64_actual200k_v2_20261008',
        'actual_nonflag_SpectralGram64_small_location_v1_20261008':'actual_nonflag_KrylovGram64_small_location_v2_20261008',
        'actual_nonflag_SpectralGram64_actual200k_location_v1_20261008':'actual_nonflag_KrylovGram64_actual200k_location_v2_20261008',
        'actual_nonflag_SpectralGram64_actual200k_hidden_launch_v1_20261008':'actual_nonflag_KrylovGram64_actual200k_hidden_launch_v2_20261008',
        'actual_nonflag_SpectralGram64_bank20_location_v1_20261008':'actual_nonflag_KrylovGram64_bank20_location_v3_20261008',
        'actual_nonflag_SpectralGram64_bank20_hidden_launch_v1_20261008':'actual_nonflag_KrylovGram64_bank20_hidden_launch_v3_20261008',
        'nonflag_SpectralGram64_bank20_plan_v1_20261008':'nonflag_KrylovGram64_bank20_plan_v3_20261008',
        'prepare_nonflag_SpectralGram64_bank20_v1_20261008':'recover_KrylovGram64_bank20_paths_v3_20261008',
        'nonflag_SpectralGram64_bank20_v1_20261008':'nonflag_KrylovGram64_bank20_v3_20261008',
        'nonflag_SpectralGram64_actual200k_v1_20261008':'nonflag_KrylovGram64_actual200k_v2_20261008',
        'nonflag_SpectralGram64_controls_main_v1_20261008':'nonflag_KrylovGram64_controls_main_v2_20261008',
        'SpectralGram64':'KrylovGram64','Spectral64':'ReorthogonalizedCG64','真实SVD数值':'真实独立投影求解',
        "proof['actual_synthetic_native_fits']==8":"proof['actual_synthetic_native_fits']==12",
        "'actual_synthetic_fits':8":"'actual_synthetic_fits':12", "'actual_synthetic_native_fits':8":"'actual_synthetic_native_fits':12"}
    # Longer strings first so that the source names remain unambiguous.
    for before,after in sorted(replacements.items(),key=lambda pair:-len(pair[0])):text=text.replace(before,after)
    marker='    sources=list(dict.fromkeys(sources));';assert text.count(marker)==1
    extra="""    sources += [A/'prepare_KrylovGram64_causal_and_publication_v2_20261008.py',
        A/'prepare_KrylovGram64_reorthogonalized_recovery_v2_20261008.py',A/'KrylovGram64_reorthogonalized_source_preparation_v2_20261008.json',
        A/'prepare_nonflag_KrylovGram64_bank20_v2_20261008.py',A/'prepare_nonflag_KrylovGram64_bank20_actual_v2_20261008.py',
        A/'KrylovGram64_bank20_admin_path_preparation_v3_20261008.json',A/'verify_KrylovGram20_causal_refit_v2_20261008.py',
        A/'nonflag_KrylovGram64_streamed_v1_20261008.py',A/'verify_nonflag_KrylovGram64_small_v1_20261008.py',A/'verify_nonflag_KrylovGram64_actual200k_v1_20261008.py']
    for rejected in ('nonflag_KrylovGram64_actual200k_v1_20261008','nonflag_KrylovGram64_bank20_v2_20261008'):
        rejected_folder=A/'service_owned_workflows_20261006'/rejected
        assert not owned(read(rejected_folder/'native_launch.json')) and read(rejected_folder/'service_execution.json')['status']=='failed'
        sources += list(rejected_folder.glob('*.json'))+list(rejected_folder.glob('*.log'))
    for earlier in ('nonflag_KrylovGram64_small_v1_20261008','nonflag_KrylovGram64_actual200k_v1_20261008'):
        sources += list(Path('E:/赛题五_本机临时',earlier).rglob('*.json'))
"""
    text=text.replace(marker,extra+marker)
    publisher=A/'publish_nonflag_KrylovGram64_controls_v2_20261008.py';assert not publisher.exists();compile(text,str(publisher),'exec');publisher.write_text(text,encoding='utf8',newline='\n')
    files=[Path(__file__),source,source_publisher,causal,publisher,bank_launch,A/'nonflag_KrylovGram64_bank20_plan_v3_20261008.json']
    pins={str(p):sha(p) for p in files}
    create(A/'KrylovGram64_causal_and_publication_preparation_v2_20261008.json',{
        'status':'prepared_same20_refit_causality_and_passed_failed_probe_main_publication','input_sha256':pins,
        'native_numerical_recipe':2,'bank_administration':3,'official_scores':0,'test_labels_read':False})
    row=start('KrylovGram20_causal_refit_controls_v2_20261008',causal.name,[],pins)
    create(A/'actual_KrylovGram20_causal_refit_hidden_launch_v2_20261008.json',row)
    row=start('nonflag_KrylovGram64_probe_and_bank_main_publication_v2_20261008',publisher.name,[],pins)
    create(A/'actual_nonflag_KrylovGram64_controls_main_hidden_launch_v2_20261008.json',row)
    print('Actual20 causality refits queued; passed/rejected probe and full bank evidence queued for main.',flush=True)

if __name__=='__main__':main()
