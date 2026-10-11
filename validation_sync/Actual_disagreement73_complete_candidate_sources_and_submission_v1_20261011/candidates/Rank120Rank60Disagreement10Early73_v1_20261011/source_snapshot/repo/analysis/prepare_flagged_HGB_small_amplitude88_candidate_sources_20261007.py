"""Prepare fresh selection/sealing routes for the reference106-compatible flag refinement."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def replace_once(text,old,new):
    assert text.count(old)==1,old
    return text.replace(old,new)


def main():
    prepare=A/'prepare_flagged_HGB_small_amplitude88_selected_candidate_20261007.py'
    seal=A/'seal_flagged_HGB_small_amplitude88_selected_candidate_20261007.py'
    assert not prepare.exists() and not seal.exists()
    original=A/'prepare_protected_upper_pool_HGB66_selected_candidate_20261007.py'
    text=original.read_text(encoding='utf8')
    pairs={
        'protected_upper_pool_HGB66_selected_release_20261007':'flagged_HGB_small_amplitude88_selected_release_20261007',
        'protected_upper_pool_HGB66_20261007':'flagged_HGB_small_amplitude88_20261007',
        'protected_upper_pool_HGB_selected_hook_preflight':'flagged_HGB_small_amplitude88_transform_preflight',
        'protected_upper_pool_HGB66_official_comparison_v2':'flagged_HGB_small_amplitude88_official_comparison',
        'protected_upper_pool_HGB66_scores_main_publication_v3':'flagged_HGB_small_amplitude88_scores_main_publication',
        'passed_actual66_lower_pool_CPU_HGB_CDF_full_official_comparisons':'passed_actual88_flagged_HGB_small_amplitude_full_official_comparisons',
        'passed_actual_historical603_features_native_HGB_lower_pool_hook_and_whole_day_prefix_controls':'passed_actual85_full5635800_flagged_HGB_small_amplitude_independent_oracle_and_cold80_260_975_controls',
        'protected_upper_pool_HGB66_scores_v2_github_20261007':'flagged_HGB_small_amplitude88_scores_github_20261007',
        'predict_protected_upper_pool_CPU_HGB_scheme_20261007':'predict_refined_flagged_CPU_HGB_scheme_20261007',
        'seal_protected_upper_pool_HGB66_selected_candidate_20261007':'seal_flagged_HGB_small_amplitude88_selected_candidate_20261007',
        'protected_upper_pool_HGB_CDF_transform_20261007':'refine_flagged_HGB_compatible_parent_transform_20261007',
        'cpu_full_universe_HGB_bank24_recovery_v2_20261007':'cpu_conditional_residual_hgb_bank20_20261007',
        'cpu_numerical_HGB_large_batch_codec_v2_20261007':'cpu_conditional_residual_hgb_codec_20261007',
        'protected_upper_pool_HGB66_pre_inference_source_freeze_20261007':'flagged_HGB_small_amplitude88_pre_inference_source_freeze_20261007',
        'selected_by_all66_actual_official_scores':'selected_by_all88_actual_official_scores',
        'passed_exact_selected_anchor66_candidate_reuse':'passed_exact_selected_anchor88_candidate_reuse',
        'actual_all66_official_controls':'actual_all88_official_controls',
        'actual24_mature_native_independent_prefix_controls':'actual20_mature_native_independent_prefix_controls',
        'frozen_selected_lower_pool_HGB66_before_future_inference':'frozen_selected_flagged_HGB88_before_future_inference',
        'passed_frozen_lower_pool_HGB66_complete_native_parent_independent_and_cold80':'passed_frozen_flagged_HGB88_complete_native_parent_independent_and_cold80',
        'passed_actual_selected_new_lower_pool_HGB66_candidate_inference':'passed_actual_selected_new_flagged_HGB88_candidate_inference',
    }
    for old,new in pairs.items():text=text.replace(old,new)
    text=text.replace('==66','==88').replace('scored_records=66','scored_records=88').replace("'scored_records':66","'scored_records':88")
    text=replace_once(text,"parent_number=pilot['actual_comparison_parent_round']", "comparison_parent=pilot['actual_comparison_parent_round']\n    parent_number=cfg['anchor_round'] if cfg['model'] is None else pilot['actual_scheme_base_round']")
    text=replace_once(text,'parent_number in (112,113,114)','parent_number in (112,114,115)')
    text=replace_once(text,"meta=info['training_metadata']","meta=info")
    text=replace_once(text,"info['actual_iterations']==96","info['actual_iterations']==64")
    text=replace_once(text,"heads_paths=[bank/name/'raw_oof_predictions.npy' for name in names]",
        "heads_paths=[bank/name/'flagged_oof_predictions.npy' for name in names]\n    reference_path=A/'optimization_20261003_r106/selected_validation.npy'\n    pins[str(reference_path)]=sha(reference_path)")
    text=replace_once(text,"selected=transform(raw,dates,flags,valid,heads,cfg['weight'],cfg['lower_fraction'])", "reference=np.load(reference_path,mmap_mode='r')\n        residual=np.zeros(len(raw),dtype=np.float64)\n        for head in heads:residual+=head\n        if heads:residual/=len(heads)\n        selected=transform(raw,reference,dates,flags,valid,residual,cfg['weight'],cfg['universe'])")
    start=text.index("        graph['protected_upper_pool_CPU_HGB_CDF']={")
    end=text.index('        winner=',start)
    text=text[:start]+"""        if names:
            graph['conditional_flag_CPU_HGB_residual_CDF']={**cfg,'native_components':components,
                'ordered_equal_mean_components':names,'first2020_identity':True,
                'training_teacher_round':106,'current_prediction_teacher_exact106_core':True}
        else:
            assert cfg['model']=='remove_flagged_HGB' and cfg['weight']==0.
            graph.pop('conditional_flag_CPU_HGB_residual_CDF',None)
"""+text[end:]
    text=replace_once(text,'explicit_parent_round=parent_number','explicit_parent_round=comparison_parent')
    text=text.replace("'explicit_parent_round':parent_number","'explicit_parent_round':comparison_parent, 'actual_scheme_base_round':parent_number")
    text=replace_once(text,"unique=set(c['sha256'] for c in parent_prediction['models'].values())|set(c['sha256'] for c in components)",
        "unique={c['sha256'] for key,c in parent_prediction['models'].items() if not key.startswith('conditional_cpu_hgb_')}|{c['sha256'] for c in components}")
    text=replace_once(text,"[*parent_record['native_component_names'],*names]", "*[[]]" ) if False else text
    text=replace_once(text,"[*parent_record['native_component_names'],*names]", "*[[]]" ) if False else text
    text=replace_once(text,"list(dict.fromkeys([*parent_record['native_component_names'],*names]))",
        "list(dict.fromkeys([*[n for n in parent_record['native_component_names'] if not n.startswith('flagged_residual_hgb')],*names]))")
    compile(text,str(prepare),'exec')
    # Anchor reuse may select115 while the graph being refined is112. Preserve its actual source.
    original_seal=A/'seal_protected_upper_pool_HGB66_selected_candidate_20261007.py'
    sealed=original_seal.read_text(encoding='utf8')
    for old,new in {**pairs,
        'protected_upper_pool_HGB66_selected_candidate_preparation':'flagged_HGB_small_amplitude88_selected_candidate_preparation',
        'passed_actual66_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes',
        'actual_protected_upper_pool_HGB_native_independent_CDF_replay':'pipeline_replay_bit_identical',
        'protected_upper_pool_HGB_native_replay_verification.json':'refined_flagged_HGB_native_replay_verification.json',
        'passed_actual_complete_saved_parent_and_lower_HGB_two_full_replays_independent_decoder_and_cold80':'passed_actual_full_refined_graph_saved_native_independent_two_replays_and_cold80',
        'passed_actual_pre_inference_source_snapshot_and_lower_pool_HGB66_native_candidate':'passed_actual_pre_inference_source_snapshot_and_refined_flagged_HGB88_native_candidate',
    }.items():sealed=sealed.replace(old,new)
    compile(sealed,str(seal),'exec')
    for path,contents in ((prepare,text),(seal,sealed)):
        with path.open('x',encoding='utf8',newline='\n') as stream:stream.write(contents)
    create(A/'flagged_HGB_small_amplitude88_candidate_source_preparation_20261007.json',{
        'status':'passed_two_fresh_selected_candidate_source_compiles_only',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),original,original_seal,prepare,seal,A/'predict_refined_flagged_CPU_HGB_scheme_20261007.py')},
        'new_native_fits':0,'new_quality_scores':0,'actual_future_inference_and_qualification_not_claimed':True,'test_labels_read':False})
    print({'fresh_selected_candidate_sources':2,'new_native_fits':0,'new_quality_scores':0},flush=True)


if __name__=='__main__':main()
