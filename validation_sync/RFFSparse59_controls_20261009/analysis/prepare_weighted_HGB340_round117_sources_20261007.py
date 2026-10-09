"""Generate the full117 pipeline from completed116 sources, after sealed340 admission."""
from pathlib import Path
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

NAMES={
 'register_flagged_HGB88_round116_artifacts_v2_20261007.py':'register_weighted_HGB340_round117_artifacts_20261007.py',
 'publish_flagged_HGB88_round116_full_validation_v2_20261007.py':'publish_weighted_HGB340_round117_full_validation_20261007.py',
 'optimize_training_round116.py':'optimize_training_round117.py',
 'finalize_training_round116.py':'finalize_training_round117.py',
 'lossless_ranking_runtime_adapter_round116_20261007.py':'lossless_ranking_runtime_adapter_round117_20261007.py',
 'build_lossless_ranking_display_round116_20261007.py':'build_lossless_ranking_display_round117_20261007.py',
 'verify_lossless_ranking_display_round116_20261007.py':'verify_lossless_ranking_display_round117_20261007.py',
 'collect_full_lossless_round116_qa27_20261007.py':'collect_full_lossless_round117_qa28_20261007.py'}

def generate(parent):
    assert parent in (112,115,116)
    mappings={**{old[:-3]:new[:-3] for old,new in NAMES.items()},
      'run_flagged_HGB88_round116_full_registration_v4_20261007':'run_weighted_HGB340_round117_full_registration_20261007',
      'prepare_flagged_HGB88_round116_sources_v3_20261007':Path(__file__).stem,
      'flagged_HGB88_round116_source_preparation_v3_20261007':'weighted_HGB340_round117_source_preparation_20261007',
      'flagged_HGB88_round116_source_admission_20261007':'weighted_HGB340_round117_source_admission_20261007',
      'flagged_HGB_small_amplitude88_selected_release_v4_20261007':'flagged_HGB_weighted_quarters340_selected_release_20261007',
      'flagged_HGB_small_amplitude88_official_comparison_v4_20261007':'flagged_HGB_weighted_quarters340_official_comparison_20261007',
      'flagged_HGB_small_amplitude88_scores_v4_github_20261007':'flagged_HGB_weighted_quarters340_scores_github_20261007',
      'flagged_HGB_small_amplitude88_transform_preflight_20261007':'flagged_HGB_weighted_quarters340_transform_preflight_20261007',
      'flagged_HGB_small_amplitude88_plan_20261007':'flagged_HGB_weighted_quarters340_plan_20261007',
      'flagged_HGB_small_amplitude88_workflow_admission_20261007':'weighted_HGB340_round117_source_admission_20261007',
      'flagged_HGB_small_amplitude88_actual_hidden_launches_20261007':'weighted_HGB340_complete_pipeline_actual_hidden_launches_20261007',
      'flagged_HGB_small_amplitude88_controls_github_20261007':'weighted_HGB_and_percentile_controls_github_20261007',
      'prepare_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007':'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007',
      'seal_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007':'seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007',
      'predict_refined_flagged_CPU_HGB_scheme_20261007':'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007',
      'flagged_HGB_small_amplitude88_official_comparison_v4':'flagged_HGB_weighted_quarters340_official_comparison',
      'flagged_HGB_small_amplitude88_scores_main_publication_v4':'flagged_HGB_weighted_quarters340_scores_main_publication',
      'flagged_HGB_small_amplitude88_selected_candidate_preparation_v4':'flagged_HGB_weighted_quarters340_selected_candidate_preparation',
      'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4':'flagged_HGB_weighted_quarters340_selected_candidate_sealing',
      'refined_flagged_HGB_native_replay_verification.json':'weighted_refined_flagged_HGB_native_replay_verification.json',
      'passed_actual88_flagged_HGB_small_amplitude_full_official_comparisons':'passed_actual340_weighted_flagged_HGB_full_official_comparisons',
      'frozen_before_actual_controls_and_official_scores.json':'frozen_before_actual_full_controls_and_official_scores.json',
      'round112_receipt.json':f'round{parent}_receipt.json','_r112':f'_r{parent}',
      'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
      'optimization_20261003_r116':'optimization_20261003_r117',
      'round116_full_scope':'round117_full_scope',
      'original_inference_selection_round116.json':'original_inference_selection_round117.json',
      'original_registry_alias_round116.json':'original_registry_alias_round117.json',
      'round116_receipt.json':'round117_receipt.json',
      'validation_sync/round116':'validation_sync/round117',
      'round116/':'round117/',"'round116'":"'round117'",'round116/full':'round117/full',
      'NUMBER = 116':'NUMBER = 117','number == 116':'number == 117',
      'WAVES = (399,)':'WAVES = (400,)','wave=399':'wave=400','wave399_results':'wave400_results',
      "'waves': [399]":"'waves': [400]", "'round': 116":"'round': 117",
      'lossless_ranking_display_qa_v27_20261007':'lossless_ranking_display_qa_v28_20261007',
      'ranking_display_qa_v27_20261007':'ranking_display_qa_v28_20261007',
      '(116, 27, 88)':'(117, 28, 340)','collect(116, 27, 88)':'collect(117, 28, 340)',
      "namespace['snapshot'](116)":"namespace['snapshot'](117)",
      'actual_complete_QA_version=27':'actual_complete_QA_version=28',"'actual_full_QA_version': 27":"'actual_full_QA_version': 28",
      '== 88':'== 340',"'expected_scored_records': 88":"'expected_scored_records': 340",
      "'scored_records': 88":"'scored_records': 340", "'existing_actual_official_records': 88":"'existing_actual_official_records': 340",
      "'original_official_pilot_records_registered': 88":"'original_official_pilot_records_registered': 340",
      'all88':'all340','actual88':'actual340','the88':'the340','第116轮88项':'第117轮340项',
      'Register88':'Register340','涨停HGB小权重与完整父方案组合':'涨停HGB非等权集成与完整父方案组合',
    }
    generated={}
    for old,new in NAMES.items():
        text=(A/old).read_text(encoding='utf8')
        if old.startswith('register_'):
            text='\n'.join(line for line in text.splitlines() if not line.startswith("    sources += [A/'recover_flagged_HGB88_round116_source_paths_v2"))+'\n'
        elif old.startswith('publish_'):
            text='\n'.join(line for line in text.splitlines() if not line.startswith("    extra += [A/'register_flagged_HGB88_round116_artifacts_v2"))+'\n'
        text=substitute(text,mappings)
        if new.startswith('register_'):
            text=text.replace('explicit_comparison_parent_round=112',f'explicit_comparison_parent_round={parent}').replace("'explicit_parent_round': 112",f"'explicit_parent_round': {parent}")
            needle="'ordered_equal_mean_components': measured['ordered_native_components'],"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n                    'ordered_quarter_counts': {n: measured['ordered_native_components'].count(n) for n in dict.fromkeys(measured['ordered_native_components'])},\n                    'native_components_unique': True,")
            text=text.replace("'future_candidate_not_inferred_for_nonselected_comparison': True}","'future_candidate_not_inferred_for_nonselected_comparison': True}\n                assert len(measured['ordered_native_components']) == 4\n                assert 2 <= len(set(measured['ordered_native_components'])) <= 3")
            needle="        A / 'collect_full_lossless_round117_qa28_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        A / 'flagged_HGB_weighted_quarters340_plan_20261007.json',\n        A / 'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',\n        A / 'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',\n        A / 'run_flagged_HGB_weighted_quarters340_official_comparison_v3_20261007.py',\n        A / 'all_forecast_percentile_runtime_20261007.py',\n        A / 'exact_numpy_all_forecast_percentiles_20261007.py',")
        elif new.startswith('publish_'):
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += (")
            end=text.index('    previous = sync.git',start)
            text=text[:start]+"""    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮登记340项完整官方比较：112、115、116三个合格锚点、28种预定非等权四份集成乘12权重，以及移除涨停HGB的消融。'
        '每个集成保留四个有序加法槽，原生模型只保存与推理2至3个唯一组件。'
        '复用20个既有年度模型，特征教师为106；全部5635800行与1011冷前缀控制不读取测试答案。'
        '以完整官方总分选优，冻结后推理；已有合格锚点按逐位输出、8指标、完整图和全部封存字节核对后复用。'
        '完整榜六视图、45秒浏览器QA28和全部源码参数审计保留；仅main。有限网格通过不等于优化穷尽。\\n').encode('utf-8')
"""+text[end:]
        compile(text,str(A/new),'exec');generated[new]=text
    assert len(generated)==8
    return generated

def main():
    ready_path=A/'flagged_HGB_weighted_quarters340_selected_release_20261007/selected_candidate_ready_for_registration.json'
    ready=read(ready_path);assert ready['status']=='passed_actual340_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'flagged_HGB_weighted_quarters340_official_comparison_20261007/verification.json')
    assert len(pilot['records'])==340 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round'];assert parent in (112,115,116)
    proof_path=A/'weighted_HGB340_round117_source_admission_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual337_controls_and24_prospective117_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists()
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name]
    preparation=A/'weighted_HGB340_round117_source_preparation_20261007.json';assert not preparation.exists()
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    create(preparation,{'status':'passed_actual340_sealed_candidate_and_admitted_full117_QA28_sources',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
      'round':117,'scored_records':340,'actual_comparison_parent_round':parent,'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
