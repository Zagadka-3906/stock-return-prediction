"""Prepare340 exact weighted comparisons and complete selected inference; admission remains separate."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def write_new(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    return p

def main():
    routes={
        'flagged_HGB_small_amplitude88_transform_preflight_20261007':'flagged_HGB_weighted_quarters340_transform_preflight_20261007',
        'flagged_HGB_small_amplitude88_transform_preflight':'weighted_flagged_HGB_full337_transform_preflight',
        'flagged_HGB_small_amplitude88_plan_20261007':'flagged_HGB_weighted_quarters340_plan_20261007',
        'flagged_HGB_small_amplitude88_official_comparison_v4_20261007':'flagged_HGB_weighted_quarters340_official_comparison_20261007',
        'flagged_HGB_small_amplitude88_official_comparison_v4':'flagged_HGB_weighted_quarters340_official_comparison',
        'flagged_HGB_small_amplitude88_scores_main_publication_v4':'flagged_HGB_weighted_quarters340_scores_main_publication',
        'flagged_HGB_small_amplitude88_selected_candidate_preparation_v4':'flagged_HGB_weighted_quarters340_selected_candidate_preparation',
        'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4':'flagged_HGB_weighted_quarters340_selected_candidate_sealing',
        'flagged_HGB_small_amplitude88_scores_v4_github_20261007':'flagged_HGB_weighted_quarters340_scores_github_20261007',
        'flagged_HGB_small_amplitude88_selected_release_v4_20261007':'flagged_HGB_weighted_quarters340_selected_release_20261007',
        'flagged_HGB_small_amplitude88_pre_inference_source_freeze_v4_20261007':'flagged_HGB_weighted_quarters340_pre_inference_source_freeze_20261007',
        'candidates/flagged_HGB_small_amplitude88_20261007':'candidates/flagged_HGB_weighted_quarters340_20261007',
        'run_flagged_HGB_small_amplitude88_official_comparison_v4_20261007':'run_flagged_HGB_weighted_quarters340_official_comparison_20261007',
        'prepare_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007':'prepare_flagged_HGB_weighted_quarters340_selected_candidate_20261007',
        'seal_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007':'seal_flagged_HGB_weighted_quarters340_selected_candidate_20261007',
        'predict_refined_flagged_CPU_HGB_scheme_20261007':'predict_refined_weighted_flagged_CPU_HGB_scheme_20261007',
        'passed_actual85_full5635800_flagged_HGB_small_amplitude_independent_oracle_and_cold80_260_975_controls':'passed_actual337_full5635800_weighted_flagged_HGB_independent_oracle_and_cold80_260_975_controls',
        'passed_actual88_flagged_HGB_small_amplitude_full_official_comparisons':'passed_actual340_weighted_flagged_HGB_full_official_comparisons',
        'passed_exact_selected_anchor88_candidate_reuse':'passed_exact_selected_anchor340_candidate_reuse',
        'passed_actual_selected_new_flagged_HGB88_candidate_inference':'passed_actual_selected_new_weighted_flagged_HGB340_candidate_inference',
        'passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual340_selected_candidate_full_graph_and_metrics_and_source_bytes',
        'passed_frozen_flagged_HGB88_complete_native_parent_independent_and_cold80':'passed_frozen_weighted_flagged_HGB340_complete_native_parent_independent_and_cold80',
        'frozen_selected_flagged_HGB88_before_future_inference':'frozen_selected_weighted_flagged_HGB340_before_future_inference',
        'selected_by_all88_actual_official_scores':'selected_by_all340_actual_official_scores',
        'actual_all88_official_controls':'actual_all340_official_controls',
        'actual_future_inference_or_full116_QA27_not_claimed':'actual_future_inference_or_full117_QA28_not_claimed',
        'full116_qualification_pending':'full117_qualification_pending',
        'candidate_full_future_freeze_native_replays_QA27_and_main_pending':'candidate_full_future_freeze_native_replays_QA28_and_main_pending',
        'refined_flagged_HGB_native_replay_verification.json':'weighted_refined_flagged_HGB_native_replay_verification.json',
        'passed_actual_full_refined_graph_saved_native_independent_two_replays_and_cold80':'passed_actual_weighted_full_refined_graph_saved_native_independent_two_replays_and_cold80',
        'passed_actual_pre_inference_source_snapshot_and_refined_flagged_HGB88_native_candidate':'passed_actual_pre_inference_source_snapshot_and_weighted_flagged_HGB340_native_candidate',
        '(112,114,115)':'(112,115,116)',
        '==88':'==340',':88':':340','all85_nonanchors':'all337_nonanchors','Score88':'Score340',
        "'expected_cases':88":"'expected_cases':340",
    }
    prototype=A/'predict_refined_flagged_CPU_HGB_scheme_20261007.py'
    text=substitute(prototype.read_text(encoding='utf8'),routes)
    text=text.replace("module='predict_protected_upper_pool_CPU_HGB_scheme_20261007'", "module='predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_20261007' if 'conditional_flag_CPU_HGB_residual_CDF' in graph else 'predict_protected_upper_pool_CPU_HGB_scheme_20261007'")
    text=text.replace("module='predict_conditional_CPU_HGB_residual_CDF_scheme_20261007'","module='predict_flagged_CPU_HGB_weighted_quarters_scheme_20261007'")
    helper=write_new('predict_refined_weighted_flagged_CPU_HGB_scheme_20261007.py',text)
    paths=[Path(__file__),helper,prototype];jobs=[]
    copies=[('run_flagged_HGB_small_amplitude88_official_comparison_v4_20261007.py','run_flagged_HGB_weighted_quarters340_official_comparison_20261007.py','flagged_HGB_weighted_quarters340_official_comparison'),
        ('prepare_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007.py','prepare_flagged_HGB_weighted_quarters340_selected_candidate_20261007.py','flagged_HGB_weighted_quarters340_selected_candidate_preparation'),
        ('seal_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007.py','seal_flagged_HGB_weighted_quarters340_selected_candidate_20261007.py','flagged_HGB_weighted_quarters340_selected_candidate_sealing')]
    for old,new,name in copies:
        original=A/old;text=substitute(original.read_text(encoding='utf8'),routes)
        if old.startswith('run_'):
            text=text.replace("'CPU_ELASTIC44_round114_full_registration_v3','protected_upper_pool_HGB66_round115_full_registration_v5'", "'protected_upper_pool_HGB66_round115_full_registration_v5','flagged_HGB88_round116_full_registration'")
            text=text.replace('((112,23),(114,25),(115,26))','((112,23),(115,26),(116,27))')
            before="for name in [*plan['single_native_heads'],*plan['ensembles']]";assert text.count(before)==1
            text=text.replace(before,"for name in plan['ensembles']")
            text=text.replace("read(p/'calibrated_csv_official.json')","read(p/'calibrated_csv_official.json')")
        elif old.startswith('prepare_'):
            before="infos=[read(bank/name/'info_2025.json') for name in names]";assert text.count(before)==1
            text=text.replace(before,"infos=[read(bank/name/'info_2025.json') for name in dict.fromkeys(names)]")
            needle="        if names:\n            graph['conditional_flag_CPU_HGB_residual_CDF']=";assert text.count(needle)==1
            text=text.replace(needle,"        if names:\n            assert len(names)==4 and 2<=len(set(names))<=3\n            assert len(components)==len(set(names))\n            graph['conditional_flag_CPU_HGB_residual_CDF']=")
            text=text.replace("'current_prediction_teacher_exact106_core':True", "'current_prediction_teacher_exact106_core':True,'ordered_quarter_counts':{name:names.count(name) for name in dict.fromkeys(names)},'native_components_unique':True")
        p=write_new(new,text);paths.extend([original,p]);jobs.append({'name':name,'driver':new,'arguments':[]})
    create(A/'weighted_flagged_HGB340_workflow_source_preparation_20261007.json',{'status':'compiled_four_complete340_scoring_and_selected_native_workflows_not_admitted_or_launched',
        'input_sha256':{str(p):sha(p) for p in paths},'routes':routes,'jobs':jobs,'native_component_storage_unique_not_repeated_slots':True,
        'full337_preflight_and_actual28_native_hook_required_before_scoring':True,'full117_registry_and_QA28_pipeline_still_to_be_prepared':True,
        'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    print({'status':'compiled_four_future340_workflows','new_quality_scores':0},flush=True)

if __name__=='__main__':main()
