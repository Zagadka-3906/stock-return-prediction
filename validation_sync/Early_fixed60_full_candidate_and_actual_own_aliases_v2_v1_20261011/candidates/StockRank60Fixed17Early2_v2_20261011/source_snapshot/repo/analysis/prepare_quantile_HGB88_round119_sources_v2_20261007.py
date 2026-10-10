"""Compose prospective complete119 registry, six-view QA30 and main publication sources."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,create,sha
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_HGB_quarter_numeric28_round118_sources_v2_20261007 as base
NAMES={old:old.replace('HGB_quarter_numeric28','quantile_HGB88').replace('round118','round119').replace('qa29','qa30') for old in base.NAMES.values()}
def generate(parent):
    assert parent in (112,117,118)
    maps={**{o[:-3]:n[:-3] for o,n in NAMES.items()},
      'run_HGB_quarter_numeric28_round118_full_registration_v2_20261007':'run_quantile_HGB88_round119_full_registration_v2_20261007',
      'prepare_HGB_quarter_numeric28_round118_sources_v2_20261007':Path(__file__).stem,
      'HGB_quarter_numeric28_round118_source_preparation_20261007':'quantile_HGB88_round119_source_preparation_20261007',
      'HGB_quarter_numeric28_round118_source_admission_20261007':'quantile_HGB88_round119_source_admission_20261007',
      'HGB_quarter_numeric28_plan_20261007':'quantile_HGB88_plan_20261007',
      'HGB_quarter_numeric28_official_comparison_20261007':'quantile_HGB88_official_comparison_20261007',
      'HGB_quarter_numeric28_selected_release_20261007':'quantile_HGB88_selected_release_20261007',
      'HGB_quarter_numeric28_transform_preflight_20261007':'quantile_HGB88_transform_preflight_20261007',
      'HGB_quarter_numeric28_scores_github_20261007':'quantile_HGB88_scores_github_20261007',
      'prepare_HGB_quarter_numeric28_selected_candidate_20261007':'prepare_quantile_HGB88_selected_candidate_20261007',
      'seal_HGB_quarter_numeric28_selected_candidate_20261007':'seal_quantile_HGB88_selected_candidate_20261007',
      'run_HGB_quarter_numeric28_official_comparison_20261007':'run_quantile_HGB88_official_comparison_20261007',
      'HGB_quarter_numeric28_official_comparison':'quantile_HGB88_official_comparison',
      'HGB_quarter_numeric28_scores_main_publication':'quantile_HGB88_scores_main_publication',
      'HGB_quarter_numeric28_selected_candidate_preparation':'quantile_HGB88_selected_candidate_preparation',
      'HGB_quarter_numeric28_selected_candidate_sealing':'quantile_HGB88_selected_candidate_sealing',
      'HGB_quarter_numeric28_complete_pipeline_actual_hidden_launches_20261007':'quantile_HGB88_complete_pipeline_actual_hidden_launches_20261007',
      'HGB_quarter_numeric_audit_github_20261007':'quantile_HGB_bank20_github_20261007',
      'cpu_conditional_residual_hgb_bank20_20261007':'quantile_HGB_native_bank20_v2_20261007',
      'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007':'predict_refined_quantile_HGB_scheme_v2_20261007',
      'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007':'predict_quantile_HGB_residual_CDF_scheme_v2_20261007',
      'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007':'predict_lower_pool_after_quantile_HGB_scheme_v2_20261007',
      'weighted_refined_flagged_HGB_native_replay_verification.json':'refined_quantile_HGB_native_replay_verification.json',
      'passed_actual28_HGB_quarter_numeric_full_official_comparisons':'passed_actual88_quantile_HGB_full_official_comparisons',
      'optimization_20261003_r118':'optimization_20261003_r119',
      '_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json',
      'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
      'round118_receipt.json':'round119_receipt.json','validation_sync/round118':'validation_sync/round119',
      'round118/':'round119/',"'round118'":"'round119'",'round118_full_scope':'round119_full_scope',
      'original_inference_selection_round118.json':'original_inference_selection_round119.json',
      'original_registry_alias_round118.json':'original_registry_alias_round119.json',
      'NUMBER = 118':'NUMBER = 119','number == 118':'number == 119',
      'WAVES = (401,)':'WAVES = (402,)','wave=401':'wave=402','wave401_results':'wave402_results',"'waves': [401]":"'waves': [402]",
      "'round': 118":"'round': 119",'== 28':'== 88',
      "'expected_scored_records': 28":"'expected_scored_records': 88","'scored_records': 28":"'scored_records': 88",
      "'existing_actual_official_records': 28":"'existing_actual_official_records': 88","'original_official_pilot_records_registered': 28":"'original_official_pilot_records_registered': 88",
      'lossless_ranking_display_qa_v29_20261007':'lossless_ranking_display_qa_v30_20261007',
      'ranking_display_qa_v29_20261007':'ranking_display_qa_v30_20261007',
      '(118, 29, 28)':'(119, 30, 88)',"namespace['snapshot'](118)":"namespace['snapshot'](119)",
      'actual_complete_QA_version=29':'actual_complete_QA_version=30',"'actual_full_QA_version': 29":"'actual_full_QA_version': 30",
      'all28':'all88','actual28':'actual88','the28':'the88','第118轮28项':'第119轮88项',
      'HGB浮点加法顺序与完整父方案组合':'分位数HGB与完整父方案组合'}
    result={}
    for old,text in base.generate(112).items():
        new=NAMES[old];text=substitute(text,maps)
        if new.startswith('register_'):
            text=text.replace('explicit_comparison_parent_round=112',f'explicit_comparison_parent_round={parent}').replace("'explicit_parent_round': 112",f"'explicit_parent_round': {parent}")
            text=text.replace("'ordered_quarter_counts': {n: measured['ordered_native_components'].count(n) for n in dict.fromkeys(measured['ordered_native_components'])},", "'ordered_mean_component_count': len(measured['ordered_native_components']),")
            text=text.replace("assert len(measured['ordered_native_components']) == 4\n                assert 2 <= len(set(measured['ordered_native_components'])) <= 3", "assert len(measured['ordered_native_components']) in (1,2,4)\n                assert len(set(measured['ordered_native_components'])) == len(measured['ordered_native_components'])")
            needle="        A / 'exact_numpy_all_forecast_percentiles_20261007.py',"
            assert needle in text
            text=text.replace(needle,needle+"\n        A / 'quantile_HGB_large_batch_codec_20261007.py',\n        A / 'cached_official_spearman_runtime_20261007.py',\n        A / 'exact_cached_official_spearman_v2_20261007.py',")
        if new.startswith('publish_'):
            text=text.replace("A / 'HGB_quarter_numeric28_actual_source_paths_before_registration_20261007.json'", "A / 'quantile_HGB88_actual_source_paths_before_registration_20261007.json'")
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += (");end=text.index('    previous = sync.git',start)
            text=text[:start]+"""    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮登记88项完整官方比较：112、117、118三个合格锚点，四个分位数HGB单模型和三种等权集成各12幅度，以及移除涨停HGB的消融。'
        '20个年度原生模型均实际训练并通过独立解码；分位数0.25或0.75、叶节点7或15、128次迭代。'
        '全部5635800行85项独立CDF及255个历史前缀控制；特征教师106，非涨停和2020输出保留。'
        '仅按完整官方总分选优，冻结后完成完整原生及独立推理，或核对既有锚点全部封存字节。'
        '完整榜六视图、45秒浏览器QA30、源码参数审计和main同步保留。有限网格不等于优化穷尽。\\n').encode('utf8')
"""+text[end:]
        compile(text,str(A/new),'exec');result[new]=text
    return result
def main():
    ready_path=A/'quantile_HGB88_selected_release_20261007/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'quantile_HGB88_official_comparison_20261007/verification.json');assert len(pilot['records'])==88 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round'];proof_path=A/'quantile_HGB88_round119_source_admission_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual85_controls_and24_prospective119_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists();assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name]
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    create(A/'quantile_HGB88_round119_source_preparation_20261007.json',{'status':'passed_actual88_sealed_candidate_and_admitted_full119_QA30_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},'round':119,'scored_records':88,'actual_comparison_parent_round':parent,'new_native_fits':0,'new_quality_scores':0})
if __name__=='__main__':main()
