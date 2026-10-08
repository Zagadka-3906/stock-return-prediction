"""Prepare the same audited own-window bank plumbing for the new reorthogonalizedCG recipe."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    source=A/'prepare_nonflag_SpectralGram64_bank20_v1_20261008.py'
    text=source.read_text(encoding='utf8')
    for before,after in (
        ('nonflag_SpectralGram64_streamed_v1_20261008','nonflag_KrylovGram64_streamed_v2_20261008'),
        ('nonflag_SpectralGram64_small_location_v1_20261008','nonflag_KrylovGram64_small_location_v2_20261008'),
        ('nonflag_SpectralGram64_actual200k_location_v1_20261008','nonflag_KrylovGram64_actual200k_location_v2_20261008'),
        ('nonflag_SpectralGram64_bank20_hidden_launch_v1_20261008','nonflag_KrylovGram64_bank20_hidden_launch_v2_20261008'),
        ('nonflag_SpectralGram64_bank20_location_v1_20261008','nonflag_KrylovGram64_bank20_location_v2_20261008'),
        ('nonflag_SpectralGram64_bank20_plan_v1_20261008','nonflag_KrylovGram64_bank20_plan_v2_20261008'),
        ('nonflag_SpectralGram64_bank20_v1_20261008','nonflag_KrylovGram64_bank20_v2_20261008'),
        ('SpectralGram64','KrylovGram64'),
        ('actual_dense_SVD_coefficients_and_intercept_close','actual_dense_projected_coefficients_and_intercept_close'),
        ('200003row_KrylovGram64_dense_SVD_native_and24_prefix_controls','200003row_KrylovGram64_projected_native_and24_prefix_controls'),
        ('shared_Gram_and_eigen_basis_per_own_window','shared_Gram_per_own_window'),
        ('shared Gram and eigen basis','shared Gram'),('shared-statistics spectral','shared-statistics reorthogonalizedCG'),
        ('Twenty own-mature spectral','Twenty own-mature reorthogonalizedCG'),('own-mature spectral','own-mature reorthogonalizedCG')):
        text=text.replace(before,after)
    # Keep the dependency on the audited preprocessing and lineage explicitly in this generator's plan.
    text=text.replace('sources=[Path(__file__),source,target,Path(native.__file__),small,probe,',
        "sources=[Path(__file__),A/'prepare_nonflag_KrylovGram64_bank20_v2_20261008.py',A/'KrylovGram64_reorthogonalized_source_preparation_v2_20261008.json',source,target,Path(native.__file__),small,probe,")
    target=A/'prepare_nonflag_KrylovGram64_bank20_actual_v2_20261008.py'
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    namespace={'__file__':str(target),'__name__':'actual_krylov_bank_preparation'}
    exec(compile(text,str(target),'exec'),namespace);namespace['main']()
    create(A/'KrylovGram64_bank20_preparation_lineage_v2_20261008.json',{
        'status':'prepared_frozen20_own_mature_reorthogonalizedCG_fits_from_audited_bank_plumbing',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target]},'actual_official_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
