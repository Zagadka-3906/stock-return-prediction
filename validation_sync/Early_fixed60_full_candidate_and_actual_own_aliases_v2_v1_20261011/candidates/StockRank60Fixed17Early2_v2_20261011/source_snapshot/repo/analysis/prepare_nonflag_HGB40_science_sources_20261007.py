"""Create complete nonflag comparison and inference scopes from admitted quantile prototypes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

FILES={
 'run_quantile_HGB88_official_comparison_v4_20261007.py':'run_nonflag_HGB40_official_comparison_20261007.py',
 'prepare_quantile_HGB88_selected_candidate_v4_20261007.py':'prepare_nonflag_HGB40_selected_candidate_20261007.py',
 'seal_quantile_HGB88_selected_candidate_v4_20261007.py':'seal_nonflag_HGB40_selected_candidate_20261007.py',
 'run_quantile_HGB88_round119_full_registration_v4_20261007.py':'run_nonflag_HGB40_round120_full_registration_20261007.py',
 'publish_quantile_HGB88_evidence_v4_20261007.py':'publish_nonflag_HGB40_evidence_20261007.py',
 'run_quantile_HGB88_admitted_comparison_v4_20261007.py':'run_nonflag_HGB40_admitted_comparison_20261007.py'}

MAP={**{o[:-3]:n[:-3] for o,n in FILES.items()},
 'prepare_quantile_HGB88_round119_sources_v4_20261007':'prepare_nonflag_HGB40_round120_sources_20261007',
 'quantile_HGB88_plan_20261007':'nonflag_HGB40_plan_20261007',
 'quantile_HGB88_official_comparison_v4_20261007':'nonflag_HGB40_official_comparison_20261007',
 'quantile_HGB88_selected_release_v4_20261007':'nonflag_HGB40_selected_release_20261007',
 'quantile_HGB88_pre_inference_source_freeze_v4_20261007':'nonflag_HGB40_pre_inference_source_freeze_20261007',
 'quantile_HGB88_round119_source_preparation_v4_20261007':'nonflag_HGB40_round120_source_preparation_20261007',
 'quantile_HGB88_round119_source_admission_v4_20261007':'nonflag_HGB40_round120_source_admission_20261007',
 'quantile_HGB88_round119_actual_registration_v4_20261007':'nonflag_HGB40_round120_actual_registration_20261007',
 'quantile_HGB88_transform_preflight_20261007':'nonflag_residual_HGB37_transform_preflight_20261007',
 'quantile_HGB_native_bank20_v2_20261007':'nonflag_residual_HGB_bank10_20261007',
 'quantile_HGB88_scores_github_v4_20261007':'nonflag_HGB40_scores_github_20261007',
 'quantile_HGB88_controls_github_v4_20261007':'nonflag_HGB40_controls_github_20261007',
 'quantile_HGB88_{phase}_github_v4_20261007':'nonflag_HGB40_{phase}_github_20261007',
 'candidates/quantile_HGB88_20261007':'candidates/nonflag_HGB40_20261007',
 'predict_refined_quantile_HGB_scheme_v2_20261007':'predict_nonflag_residual_HGB_complete_scheme_20261007',
 'quantile_refined_HGB_native_replay_verification.json':'nonflag_residual_HGB_native_replay_verification.json',
 'passed_actual_quantile_full_refined_graph_saved_native_independent_two_replays_and_cold80':'passed_actual_complete_parent_and_nonflag_HGB_two_full_replays_independent_and_cold80',
 'passed_actual85_full5635800_quantile_HGB_independent_oracle_and_cold80_260_975_controls':'passed_actual37_full5635800_nonflag_residual_HGB_independent_CDF_and111_cold_controls',
 'passed_actual88_quantile_HGB_full_official_comparisons':'passed_actual40_nonflag_HGB_full_official_comparisons',
 'passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes',
 'passed_actual85_controls_and24_prospective119_complete_source_schema_paths_and_graph_routes':'passed_actual37_controls_and24_prospective120_complete_source_schema_paths_and_graph_routes',
 'flagged_oof_predictions.npy':'nonflag_oof_predictions.npy',
 'remove_flagged_HGB':'remove_nonflag_HGB',
 'all_complete_parent_nonflag_and2020_raw_bits_preserved':'all_complete_parent_flag_and2020_raw_bits_preserved',
 'passed_actual_selected_new_quantile_HGB88_candidate_inference':'passed_actual_selected_new_nonflag_HGB40_candidate_inference',
 'passed_exact_selected_anchor88_candidate_reuse':'passed_exact_selected_anchor40_candidate_reuse',
 'passed_frozen_quantile_HGB88_complete_native_parent_independent_and_cold80':'passed_frozen_nonflag_HGB40_complete_native_parent_independent_and_cold80',
}
for service in ['round119_source_admission','full85_controls_main_publication','official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round119_full_registration']:
    MAP['quantile_HGB88_'+service+'_v4']='nonflag_HGB40_'+service.replace('round119','round120').replace('full85','full37')

def main():
    generated={}
    for old,new in FILES.items():
        text=substitute((A/old).read_text(encoding='utf8'),MAP)
        text=text.replace('(112,117,118)','(112,118,119)').replace('(112, 117, 118)','(112, 118, 119)')
        text=text.replace('==88','==40').replace('== 88','== 40').replace('=88','=40').replace(':88',':40').replace(': 88',': 40')
        text=text.replace('expected_scored_records=88','expected_scored_records=40')
        text=text.replace('all88','all40').replace('actual88','actual40').replace('all85','all37')
        text=text.replace('CPU_quantile_HGB','nonflag_residual_HGB').replace('new_quality_score_records\':88','new_quality_score_records\':40')
        text=text.replace('candidate_full_future_freeze_native_replays_QA30','candidate_full_future_freeze_native_replays_QA31')
        text=text.replace('full119_qualification','full120_qualification').replace('full119_future','full120_future')
        text=text.replace('quantile_HGB88_complete_pipeline_actual_hidden_launches_v3_20261007','nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007')
        if old.startswith('run_quantile_HGB88_official'):
            needle='    from refine_flagged_HGB_compatible_parent_transform_20261007 import prepare,apply_prepared,transform,compatible'
            assert text.count(needle)==1
            text=text.replace(needle,'    from nonflag_residual_HGB_CDF_transform_20261007 import prepare,apply_prepared,transform\n    from refine_flagged_HGB_compatible_parent_transform_20261007 import compatible')
            text=text.replace("'quantile_HGB_full85_transform_preflight'","'nonflag_residual_HGB37_transform_preflight'")
            text=text.replace("'weighted_HGB340_round117_full_registration_v2','HGB_quarter_numeric28_round118_full_registration_v4'","'HGB_quarter_numeric28_round118_full_registration_v4','quantile_HGB88_round119_full_registration_v4'")
            text=text.replace('((112,23),(117,28),(118,29))','((112,23),(118,29),(119,30))')
            text=text.replace('==20','==10').replace('== 20','== 10').replace("'existing_native_bank_fits':20","'existing_native_bank_fits':10")
            text=text.replace('eligible=[n for n in parents if compatible(graphs[n],reference_graph)]',"eligible=[n for n in parents if compatible(graphs[n],reference_graph) and 'protected_upper_pool_CPU_HGB_CDF' not in graphs[n]]")
            text=text.replace("A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',","A/'nonflag_residual_HGB_CDF_transform_20261007.py',A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',")
            text=text.replace('nonflag=flags!=1','preserved=flags==1').replace('values[nonflag]','values[preserved]').replace('parent[nonflag]','parent[preserved]')
        elif old.startswith('prepare_'):
            text=text.replace('from refine_flagged_HGB_compatible_parent_transform_20261007 import transform','from nonflag_residual_HGB_CDF_transform_20261007 import transform')
            text=text.replace("==128","==96")
            text=text.replace("assert info['parameters']['loss']=='quantile' and info['parameters']['quantile'] in (.25,.75)","assert info['parameters']['loss'] in ('squared_error','absolute_error')")
            text=text.replace("graph['conditional_flag_CPU_HGB_residual_CDF']={**cfg", "graph['nonflag_CPU_HGB_residual_CDF']={**cfg")
            text=text.replace("graph.pop('conditional_flag_CPU_HGB_residual_CDF',None)","graph.pop('nonflag_CPU_HGB_residual_CDF',None)")
            text=text.replace("if not key.startswith('conditional_cpu_hgb_')", "if not key.startswith('nonflag_cpu_hgb_')")
            text=text.replace("if not n.startswith(('flagged_residual_hgb','flagged_quantile_hgb'))", "if not n.startswith('nonflag_residual_hgb')")
        elif old.startswith('seal_'):
            text=text.replace('quantile_refined_HGB_native_replay_verification.json','nonflag_residual_HGB_native_replay_verification.json')
        elif old.startswith('run_quantile_HGB88_round'):
            text=text.replace("'HGB_quarter_numeric28_round118_full_registration_v4',", "'quantile_HGB88_round119_full_registration_v4',")
            text=text.replace('register_quantile_HGB88_round119_artifacts_20261007','register_nonflag_HGB40_round120_artifacts_20261007')
            text=text.replace('optimization_20261003_r119','optimization_20261003_r120')
            text=text.replace('lossless_ranking_runtime_adapter_round119_20261007','lossless_ranking_runtime_adapter_round120_20261007')
            text=text.replace('publish_quantile_HGB88_round119_full_validation_20261007','publish_nonflag_HGB40_round120_full_validation_20261007')
            text=text.replace('lossless(119)','lossless(120)').replace('publish(119,','publish(120,')
            text=text.replace('quantile_HGB88_actual_source_paths_before_registration_20261007','nonflag_HGB40_actual_source_paths_before_registration_20261007')
            text=text.replace('quantile_HGB88_full119_20261007','nonflag_HGB40_full120_20261007')
        elif old.startswith('publish_'):
            text=text.replace("closed('quantile_HGB_bank20_main_publication_after118_v4')", "closed('quantile_HGB88_round119_full_registration_v4')")
            text=text.replace("closed('HGB_quarter_numeric28_round118_full_registration_v4')", "closed('quantile_HGB88_round119_full_registration_v4')")
            text=text.replace("'quantile_HGB_full85_transform_preflight'", "'nonflag_residual_HGB37_transform_preflight'")
            text=text.replace("assert len(proof['controls'])==85", "assert len(proof['controls'])==37")
            text=text.replace('quantile_HGB88_round119_full_registration_v4','quantile_HGB88_round119_full_registration_v4')
        compile(text,str(A/new),'exec');generated[new]=text
    for n in generated:assert not (A/n).exists(),n
    for n,text in generated.items():
        with (A/n).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'nonflag_HGB40_science_source_preparation_20261007.json',{
      'status':'compiled_nonflag40_scoring_sealed_protocol_inference_and_qualification_prototypes',
      'input_sha256':{str(A/n):sha(A/n) for n in generated},'new_native_fits':0,'new_quality_scores':0,
      'actual120_source_admission_not_yet_claimed':True,'test_labels_read':False})

if __name__=='__main__':main()
