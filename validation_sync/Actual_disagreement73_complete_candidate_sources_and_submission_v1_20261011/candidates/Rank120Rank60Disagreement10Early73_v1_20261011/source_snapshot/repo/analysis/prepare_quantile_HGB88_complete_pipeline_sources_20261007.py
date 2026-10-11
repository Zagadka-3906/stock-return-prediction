"""Compile all119 runtime, admission and main stages before admitting official88 scoring."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    files={
      'publish_HGB_quarter_numeric28_evidence_v3_20261007.py':'publish_quantile_HGB88_evidence_20261007.py',
      'verify_HGB_quarter_numeric28_round118_sources_v3_20261007.py':'verify_quantile_HGB88_round119_sources_20261007.py',
      'run_HGB_quarter_numeric28_round118_full_registration_v2_20261007.py':'run_quantile_HGB88_round119_full_registration_20261007.py'}
    maps={**{o[:-3]:n[:-3] for o,n in files.items()},
      'prepare_HGB_quarter_numeric28_round118_sources_v2_20261007':'prepare_quantile_HGB88_round119_sources_20261007',
      'HGB_quarter_numeric28_round118_source_preparation_20261007':'quantile_HGB88_round119_source_preparation_20261007',
      'HGB_quarter_numeric28_round118_source_admission_20261007':'quantile_HGB88_round119_source_admission_20261007',
      'register_HGB_quarter_numeric28_round118_artifacts_20261007':'register_quantile_HGB88_round119_artifacts_20261007',
      'publish_HGB_quarter_numeric28_round118_full_validation_20261007':'publish_quantile_HGB88_round119_full_validation_20261007',
      'lossless_ranking_runtime_adapter_round118_20261007':'lossless_ranking_runtime_adapter_round119_20261007',
      'collect_full_lossless_round118_qa29_20261007':'collect_full_lossless_round119_qa30_20261007',
      'HGB_quarter_numeric28_plan_20261007':'quantile_HGB88_plan_20261007',
      'HGB_quarter_numeric28_official_comparison_20261007':'quantile_HGB88_official_comparison_20261007',
      'HGB_quarter_numeric28_selected_release_20261007':'quantile_HGB88_selected_release_20261007',
      'HGB_quarter_numeric28_transform_preflight_20261007':'quantile_HGB88_transform_preflight_20261007',
      'HGB_quarter_numeric28_scores_github_20261007':'quantile_HGB88_scores_github_20261007',
      'prepare_HGB_quarter_numeric28_selected_candidate_20261007':'prepare_quantile_HGB88_selected_candidate_20261007',
      'seal_HGB_quarter_numeric28_selected_candidate_20261007':'seal_quantile_HGB88_selected_candidate_20261007',
      'run_HGB_quarter_numeric28_official_comparison_20261007':'run_quantile_HGB88_official_comparison_20261007',
      'HGB_quarter_numeric28_full25_transform_preflight':'quantile_HGB_full85_transform_preflight',
      'HGB_quarter_numeric28_full25_controls_main_publication':'quantile_HGB88_full85_controls_main_publication',
      'HGB_quarter_numeric28_official_comparison':'quantile_HGB88_official_comparison',
      'HGB_quarter_numeric28_scores_main_publication':'quantile_HGB88_scores_main_publication',
      'HGB_quarter_numeric28_selected_candidate_preparation':'quantile_HGB88_selected_candidate_preparation',
      'HGB_quarter_numeric28_selected_candidate_sealing':'quantile_HGB88_selected_candidate_sealing',
      'weighted_HGB340_round117_full_registration':'HGB_quarter_numeric28_round118_full_registration',
      'HGB_quarter_numeric_audit_main_publication_after117':'quantile_HGB_bank20_main_publication_after118',
      'weighted_flagged_HGB_native_hook_preflight_v2':'quantile_HGB_native_hook7_preflight',
      'weighted_flagged_HGB_native_hook_preflight_v2_20261007':'quantile_HGB_native_hook7_preflight_20261007',
      'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007':'predict_refined_quantile_HGB_scheme_v2_20261007',
      'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007':'predict_quantile_HGB_residual_CDF_scheme_v2_20261007',
      'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007':'predict_lower_pool_after_quantile_HGB_scheme_v2_20261007',
      'verify_HGB_quarter_numeric28_transform_v3_20261007':'verify_quantile_HGB88_transform_20261007',
      'HGB_quarter_numeric28_actual_source_paths_before_registration_20261007':'quantile_HGB88_actual_source_paths_before_registration_20261007',
      'HGB_quarter_numeric28_round118_actual_registration_20261007':'quantile_HGB88_round119_actual_registration_20261007',
      'HGB_quarter_numeric28_complete_scope_source_preparation_v3_20261007':'quantile_HGB88_complete_pipeline_source_preparation_20261007',
      'prepare_HGB_quarter_numeric28_complete_scope_v3_20261007':Path(__file__).stem,
      'passed_actual25_full5635800_HGB_quarter_numeric_independent_oracle_and_cold80_260_975_controls':'passed_actual85_full5635800_quantile_HGB_independent_oracle_and_cold80_260_975_controls',
      'passed_actual28_HGB_quarter_numeric_full_official_comparisons':'passed_actual88_quantile_HGB_full_official_comparisons',
      'passed_actual25_controls_and24_prospective118_complete_source_schema_paths_and_graph_routes':'passed_actual85_controls_and24_prospective119_complete_source_schema_paths_and_graph_routes',
      'passed_actual28_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes',
      'passed_actual28_sealed_candidate_and_admitted_full118_QA29_sources':'passed_actual88_sealed_candidate_and_admitted_full119_QA30_sources',
      'optimization_20261003_r118':'optimization_20261003_r119',
      'round118_receipt.json':'round119_receipt.json','HGB_quarter_numeric28_full118_20261007':'quantile_HGB88_full119_20261007',
      'publish(118,':'publish(119,','lossless(118)':'lossless(119)',
      '(112,116,117)':'(112,117,118)','(112, 116, 117)':'(112, 117, 118)',
      'round118_full_scope':'round119_full_scope','original_registry_alias_round118.json':'original_registry_alias_round119.json',
      'validation_sync/round118':'validation_sync/round119',"snapshot'](118)":"snapshot'](119)",
      "QA_version': 29":"QA_version': 30",'collect(118, 29, 28)':'collect(119, 30, 88)',
      'passed_all_actual118_registry':'passed_all_actual119_registry',
      'full118_not_yet_qualified':'full119_not_yet_qualified','full118_future_inference_and_QA29':'full119_future_inference_and_QA30',
      'QA29':'QA30', '完整118':'完整119','full118_registration':'full119_registration',
      "'existing_official_scores_registered':28":"'existing_official_scores_registered':88",
      '==28':'==88','==25':'==85','else 28':'else 88','25 if phase':'85 if phase',
      "'actual_full_control_cases':25":"'actual_full_control_cases':85","'actual_cold_prefix_cases':75":"'actual_cold_prefix_cases':255",
      "'actual_full_transform_controls':25":"'actual_full_transform_controls':85","'actual_native_hook_cases':28":"'actual_native_hook_cases':7",
      "'scored_records':28":"'scored_records':88",
      'passed_actual25_controls':'passed_actual85_controls'}
    paths=[Path(__file__)]
    for old,new in files.items():
        text=substitute((A/old).read_text(encoding='utf8'),maps)
        if old.startswith('publish_'):
            text=text.replace("f'HGB_quarter_numeric28_{phase}_github_20261007'","f'quantile_HGB88_{phase}_github_20261007'")
            text=text.replace("f'validation_sync/HGB_quarter_numeric28_{phase}_20261007'","f'validation_sync/quantile_HGB88_{phase}_20261007'")
            text=text.replace("'published_actual_HGB_quarter_numeric28_'","'published_actual_quantile_HGB88_'")
            text=text.replace("'new_quality_score_records':28 if", "'new_quality_score_records':88 if").replace("'new_quality_scores':28 if", "'new_quality_scores':88 if")
            text=text.replace('HGB浮点顺序补测：2种有序四份组合，各2个唯一原生模型，12种幅度；加3个合格锚点与移除分支，共28项。', '分位数HGB：4单模型及3等权集成各12幅度，加3个合格锚点及消融，共88项。')
            text=text.replace('上传HGB浮点加法顺序的','上传分位数HGB的')
            needle="    if phase=='scores':\n        for row in proof['records']:"
            assert needle in text
            text=text.replace(needle,"    sources += [A/'cached_official_spearman_runtime_20261007.py', A/'exact_cached_official_spearman_v2_20261007.py',\n      A/'exact_cached_validation_spearman_20261007.py',A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json',\n      A/'exact_cached_official_spearman_v2_edge_preflight_20261007/verification.json',A/'benchmark_cached_official_spearman_full_scoring_20261007.py',\n      A/'prepare_cached_official_spearman_full_benchmark_20261007.py',A/'cached_official_spearman_full_benchmark_source_preparation_20261007.json',\n      A/'cached_official_spearman_full12_actual_launch_20261007.json',A/'quantile_HGB_native_hook7_preflight_20261007/verification.json',\n      A/'quantile_HGB88_workflow_source_preparation_20261007.json', A/'quantile_HGB85_full_controls_source_preparation_20261007.json',\n      *list((A/'service_owned_workflows_20261006/cached_official_spearman_full12_benchmark').glob('*.json')),\n      *list((A/'service_owned_workflows_20261006/cached_official_spearman_full12_benchmark').glob('*.log'))]\n"+needle)
        elif old.startswith('verify_'):
            text=text.replace("assert len(read(native)['records'])==28","assert len(read(native)['records'])==7")
            text=text.replace("assert len(plan['ensembles'])==2", "assert len(plan['single_native_heads'])==4 and len(plan['ensembles'])==3")
            text=text.replace("assert len(controls['controls'])==25", "assert len(controls['controls'])==85")
            text=text.replace("and len(controls['controls'])==25", "and len(controls['controls'])==85")
            text=text.replace("for n in (112,116,117)", "for n in (112,117,118)")
            text=text.replace("for parent in (112,116,117)", "for parent in (112,117,118)")
            text=text.replace("examples=[('remove_flagged_HGB',0.,[]),*[(n,.0125,names) for n,names in plan['ensembles'].items()]]", "examples=[('remove_flagged_HGB',0.,[]),*[(n,.0125,[n]) for n in plan['single_native_heads']],*[(n,.0125,names) for n,names in plan['ensembles'].items()]]")
            text=text.replace("assert component['ordered_equal_mean_components']==names and sum(component['ordered_quarter_counts'].values())==4", "assert component['ordered_equal_mean_components']==names and component['ordered_mean_component_count']==len(names)")
            text=text.replace("assert len(component['ordered_quarter_counts']) in (2,3) and component['native_components_unique'] is True", "assert len(names) in (1,2,4) and len(set(names))==len(names) and component['native_components_unique'] is True")
            text=text.replace('len(graph_controls)==9', 'len(graph_controls)==24')
            text=text.replace('expected_scored_records=28','expected_scored_records=88')
            text=text.replace(" and 'expected_scored_records=88' not in candidate", " and 'expected_scored_records=28' not in candidate")
            text=text.replace("'actual_full_transform_controls':25", "'actual_full_transform_controls':85")
            needle="    for p in sources:";assert needle in text
            text=text.replace(needle,"    sources += [Path(generator.base.base.__file__),*[A/n for n in generator.base.base.NAMES],\n      A/'cached_official_spearman_runtime_20261007.py',A/'exact_cached_official_spearman_v2_20261007.py',\n      A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json']\n"+needle)
        else:
            text=text.replace("'完整父方案的HGB浮点加法顺序补测'", "'完整父方案的分位数HGB补充'")
            text=text.replace('预定28项完整官方比较：三个合格锚点、24项浮点加法顺序和一个消融','预定88项完整官方比较：三个合格锚点、84项分位数HGB和一个消融')
        p=A/new;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8');paths += [A/old,p]
    create(A/'quantile_HGB88_complete_pipeline_source_preparation_20261007.json',{'status':'compiled_fresh119_full_registry_runtime_admission_and_phase_publications','input_sha256':{str(p):sha(p) for p in paths},'new_native_fits':0,'new_quality_scores':0})
if __name__=='__main__':main()
