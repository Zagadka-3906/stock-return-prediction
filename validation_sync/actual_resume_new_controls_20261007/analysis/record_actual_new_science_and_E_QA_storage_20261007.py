"""Record actual new solver identities and freshly allocated E-drive QA destinations."""
from pathlib import Path
import sys,time,shutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    aliases=[]
    base=Path('E:/赛题五_本机临时/完整榜QA_20261007').resolve()
    for version in (40,41,42):
        alias=A/f'lossless_ranking_display_qa_v{version}_20261007';target=alias.resolve()
        assert alias.is_junction() and target.is_relative_to(base)
        assert not list(alias.iterdir()),'record only fresh QA output parents before execution'
        aliases.append({'original_D_path':str(alias),'physical_E_target':str(target),'QA_version':version,'actual_NTFS_directory_junction':True,'existing_frozen_sources_not_moved_or_edited':True})
    create(A/'actual_future_QA40_41_42_E_storage_20261007.json',{
      'status':'verified_fresh_QA40_41_42_E_destinations_with_unchanged_D_access_paths','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'aliases':aliases,'D_free_GiB':shutil.disk_usage(ROOT).free/2**30,'E_free_GiB':shutil.disk_usage(base).free/2**30,
      'C_drive_model_data_or_temp_storage_added':False,'recursive_move_or_delete_executed':False,'input_sha256':{str(Path(__file__)):sha(Path(__file__))}})
    entries=[];sources=[Path(__file__)]
    for name,method in [('nonflag_residual_RFF128StreamMid_bank10_20261007','streamed_RBF128_centered_float64_Gram'),('nonflag_residual_EmpiricalBayes64_bank10_20261007','empirical_Bayes_scalar_and_diagonal_centered_Gram64')]:
        bank=A/name;proof=bank/'verification.json';data=read(proof);assert data['actual_native_fits']==len(data['actual_models'])==10
        fits=[];sources.append(proof)
        for info in sorted(bank.glob('*/info_*.json')):
            row=read(info);meta=row['fit_metadata'];assert row['last_training_label_date']<row['exclusive_cutoff'] and row['last_training_label_end']<=row['exclusive_cutoff']
            fits.append({'model':row['name'],'year':row['year'],'exclusive_cutoff':row['exclusive_cutoff'],'last_training_label_date':row['last_training_label_date'],
              'last_training_label_end':row['last_training_label_end'],'training_solver_recipe':meta['training_solver_recipe'],
              'own_mature_training_rows':meta['actual_rows'],'actual_blocks':meta['actual_blocks'],'maximum_actual_block_rows':meta['maximum_actual_block_rows'],
              'actual_iterations':meta.get('actual_iterations'),'native_model_sha256':row['native_model_sha256']})
            sources.append(info)
        assert len(fits)==10
        entries.append({'method':method,'actual_new_mature_native_fits':10,'fits':fits,'actual_native_reload_and_independent_decoder_and_cold_controls':str(proof),
          'full_official_scoring_and_selected_candidate_qualification_require_separate_actual_proofs':True})
    create(A/'actual_new_streamed_RFF_and_empirical_Bayes_scientific_identity_20261007.json',{
      'status':'recorded_actual20_new_mature_native_fits_and_explicit_solver_identities','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'entries':entries,
      'streamed_RBF_is_new_floating_point_accumulation_recipe_not_dense_fit_bit_equivalence':True,
      'Bayes_initial_alpha_field_is_initial_prior_precision_not_fixed_final_Ridge_penalty':True,
      'Bayes_scalar_or_diagonal_prior_and_noise_learned_from_own_mature_training_rows':True,
      'Bayes_custom_empirical_solver_not_sklearn_BayesianRidge_or_ARDRegression_identity':True,
      'legacy_inherited_status_labels_do_not_define_mathematical_model_identity':True,
      'native_predictive_mean_only_posterior_uncertainty_not_used':True,'new_quality_scores_added_by_this_record':0,'selection_bias_uncorrected':True,
      'input_sha256':{str(p):sha(p) for p in sources},'test_labels_read':False})

if __name__=='__main__':main()
