"""Compile fresh28 workflows and25 controls without altering admitted340 sources."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    files={
      'verify_flagged_HGB_weighted_quarters340_transform_20261007.py':'verify_HGB_quarter_numeric28_transform_20261007.py',
      'run_flagged_HGB_weighted_quarters340_official_comparison_v3_20261007.py':'run_HGB_quarter_numeric28_official_comparison_20261007.py',
      'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007.py':'prepare_HGB_quarter_numeric28_selected_candidate_20261007.py',
      'seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007.py':'seal_HGB_quarter_numeric28_selected_candidate_20261007.py',
      'publish_weighted_HGB340_evidence_20261007.py':'publish_HGB_quarter_numeric28_evidence_20261007.py'}
    routes={**{n[:-3]:v[:-3] for n,v in files.items()},
      'flagged_HGB_weighted_quarters340_plan_20261007':'HGB_quarter_numeric28_plan_20261007',
      'flagged_HGB_weighted_quarters340_transform_preflight_20261007':'HGB_quarter_numeric28_transform_preflight_20261007',
      'flagged_HGB_weighted_quarters340_official_comparison_20261007':'HGB_quarter_numeric28_official_comparison_20261007',
      'flagged_HGB_weighted_quarters340_selected_release_20261007':'HGB_quarter_numeric28_selected_release_20261007',
      'flagged_HGB_weighted_quarters340_pre_inference_source_freeze_20261007':'HGB_quarter_numeric28_pre_inference_source_freeze_20261007',
      'candidates/flagged_HGB_weighted_quarters340_20261007':'candidates/HGB_quarter_numeric28_20261007',
      'flagged_HGB_weighted_quarters340_scores_github_20261007':'HGB_quarter_numeric28_scores_github_20261007',
      'weighted_flagged_HGB_full337_transform_preflight_v3':'HGB_quarter_numeric28_full25_transform_preflight',
      'flagged_HGB_weighted_quarters340_official_comparison':'HGB_quarter_numeric28_official_comparison',
      'flagged_HGB_weighted_quarters340_scores_main_publication':'HGB_quarter_numeric28_scores_main_publication',
      'flagged_HGB_weighted_quarters340_selected_candidate_preparation':'HGB_quarter_numeric28_selected_candidate_preparation',
      'flagged_HGB_weighted_quarters340_selected_candidate_sealing':'HGB_quarter_numeric28_selected_candidate_sealing',
      'weighted_HGB340_full337_controls_main_publication':'HGB_quarter_numeric28_full25_controls_main_publication',
      'prepare_weighted_HGB340_round117_sources_20261007':'prepare_HGB_quarter_numeric28_round118_sources_20261007',
      'run_weighted_HGB340_round117_full_registration_20261007':'run_HGB_quarter_numeric28_round118_full_registration_20261007',
      'verify_weighted_HGB340_round117_sources_20261007':'verify_HGB_quarter_numeric28_round118_sources_20261007',
      'passed_actual337_full5635800_weighted_flagged_HGB_independent_oracle_and_cold80_260_975_controls':'passed_actual25_full5635800_HGB_quarter_numeric_independent_oracle_and_cold80_260_975_controls',
      'passed_actual340_weighted_flagged_HGB_full_official_comparisons':'passed_actual28_HGB_quarter_numeric_full_official_comparisons',
      'passed_exact_selected_anchor340_candidate_reuse':'passed_exact_selected_anchor28_candidate_reuse',
      'passed_actual_selected_new_weighted_flagged_HGB340_candidate_inference':'passed_actual_selected_new_HGB_quarter_numeric28_candidate_inference',
      'passed_actual340_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual28_selected_candidate_full_graph_and_metrics_and_source_bytes',
      'passed_frozen_weighted_flagged_HGB340_complete_native_parent_independent_and_cold80':'passed_frozen_HGB_quarter_numeric28_complete_native_parent_independent_and_cold80',
      'frozen_selected_weighted_flagged_HGB340_before_future_inference':'frozen_selected_HGB_quarter_numeric28_before_future_inference',
      'selected_by_all340_actual_official_scores':'selected_by_all28_actual_official_scores',
      'actual_all340_official_controls':'actual_all28_official_controls',
      'passed_actual_pre_inference_source_snapshot_and_weighted_flagged_HGB340_native_candidate':'passed_actual_pre_inference_source_snapshot_and_HGB_quarter_numeric28_native_candidate',
      '(112,115,116)':'(112,116,117)','((112,23),(115,26),(116,27))':'((112,23),(116,27),(117,28))',
      "'protected_upper_pool_HGB66_round115_full_registration_v5'":"'flagged_HGB88_round116_full_registration_v2'",
      "'flagged_HGB88_round116_full_registration_v2'":"'weighted_HGB340_round117_full_registration'",
      'expected_scored_records=340':'expected_scored_records=28','==340':'==28','==337':'==25',':340':':28',
      "'expected_cases':340":"'expected_cases':28",'all337_nonanchors':'all25_nonanchors',
      'all337_weighted_and_ablation':'all25_weighted_and_ablation',
      'candidate_full_future_freeze_native_replays_QA28_and_main_pending':'candidate_full_future_freeze_native_replays_QA29_and_main_pending',
      'future_candidate_and_full117_qualification_pending':'future_candidate_and_full118_qualification_pending',
      'actual_future_inference_or_full117_QA28_not_claimed':'actual_future_inference_or_full118_QA29_not_claimed',
      'actual_future_inference_or_full116_QA27_not_claimed':'actual_future_inference_or_full118_QA29_not_claimed',
    }
    paths=[Path(__file__)]
    for old,new in files.items():
        text=substitute((A/old).read_text(encoding='utf8'),routes)
        if old.startswith('verify_'):
            text=text.replace('for85 branch refinements','for25 numerical branch refinements')
        elif old.startswith('run_'):
            text=text.replace('Score340','Score28').replace('full117_qualification','full118_qualification')
        elif old.startswith('prepare_'):
            text=text.replace('best of340','best of28')
        elif old.startswith('publish_'):
            text=text.replace('337 if phase','25 if phase').replace('else 340','else 28').replace('340 if phase','28 if phase')
            text=text.replace("f'weighted_HGB340_{phase}_github_20261007'","f'HGB_quarter_numeric28_{phase}_github_20261007'")
            text=text.replace("f'validation_sync/weighted_HGB340_{phase}_20261007'","f'validation_sync/HGB_quarter_numeric28_{phase}_20261007'")
            text=text.replace("'published_actual_weighted_HGB340_'","'published_actual_HGB_quarter_numeric28_'")
            text=text.replace("'actual_full_control_cases':337","'actual_full_control_cases':25").replace("'actual_cold_prefix_cases':1011","'actual_cold_prefix_cases':75")
            text=text.replace("'full117_not_yet_qualified'","'full118_not_yet_qualified'")
            text=text.replace('加权HGB集成：28种四份组合，每种2至3个唯一原生模型，12种幅度；加3个合格锚点与移除分支，共340项。','HGB浮点顺序补测：2种有序四份组合，各2个唯一原生模型，12种幅度；加3个合格锚点与移除分支，共28项。')
            text=text.replace('完整117资格','完整118资格').replace('QA28及完整榜','QA29及完整榜')
            text=text.replace('非等权HGB集成的','HGB浮点加法顺序的')
            text=text.replace("    closed('weighted_HGB_and_percentile_controls_main_publication')","    closed('HGB_quarter_numeric_audit_main_publication_after117')")
        p=A/new;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');paths += [A/old,p]
    create(A/'HGB_quarter_numeric28_workflow_source_preparation_20261007.json',{'status':'compiled_five_fresh28_workflows_before_full118_admission',
      'input_sha256':{str(p):sha(p) for p in paths},'routes':routes,'new_native_fits':0,'new_quality_scores':0,
      'full118_pipeline_and_all25_controls_still_required':True})

if __name__=='__main__':main()
