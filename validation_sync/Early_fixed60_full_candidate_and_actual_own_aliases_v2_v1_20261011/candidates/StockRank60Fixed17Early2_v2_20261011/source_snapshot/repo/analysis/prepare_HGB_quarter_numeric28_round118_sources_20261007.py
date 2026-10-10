"""Compose the complete118 sources from unchanged admitted117 prospective templates."""
from pathlib import Path
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_weighted_HGB340_round117_sources_20261007 as base

NAMES={old:old.replace('weighted_HGB340','HGB_quarter_numeric28').replace('round117','round118').replace('qa28','qa29') for old in base.NAMES.values()}

def generate(parent):
    assert parent in (112,116,117)
    maps={**{o[:-3]:n[:-3] for o,n in NAMES.items()},
      'run_weighted_HGB340_round117_full_registration_20261007':'run_HGB_quarter_numeric28_round118_full_registration_20261007',
      'prepare_weighted_HGB340_round117_sources_20261007':Path(__file__).stem,
      'weighted_HGB340_round117_source_preparation_20261007':'HGB_quarter_numeric28_round118_source_preparation_20261007',
      'weighted_HGB340_round117_source_admission_20261007':'HGB_quarter_numeric28_round118_source_admission_20261007',
      'flagged_HGB_weighted_quarters340_plan_20261007':'HGB_quarter_numeric28_plan_20261007',
      'flagged_HGB_weighted_quarters340_official_comparison_20261007':'HGB_quarter_numeric28_official_comparison_20261007',
      'flagged_HGB_weighted_quarters340_selected_release_20261007':'HGB_quarter_numeric28_selected_release_20261007',
      'flagged_HGB_weighted_quarters340_transform_preflight_20261007':'HGB_quarter_numeric28_transform_preflight_20261007',
      'flagged_HGB_weighted_quarters340_scores_github_20261007':'HGB_quarter_numeric28_scores_github_20261007',
      'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007':'prepare_HGB_quarter_numeric28_selected_candidate_20261007',
      'seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007':'seal_HGB_quarter_numeric28_selected_candidate_20261007',
      'run_flagged_HGB_weighted_quarters340_official_comparison_v3_20261007':'run_HGB_quarter_numeric28_official_comparison_20261007',
      'flagged_HGB_weighted_quarters340_official_comparison':'HGB_quarter_numeric28_official_comparison',
      'flagged_HGB_weighted_quarters340_scores_main_publication':'HGB_quarter_numeric28_scores_main_publication',
      'flagged_HGB_weighted_quarters340_selected_candidate_preparation':'HGB_quarter_numeric28_selected_candidate_preparation',
      'flagged_HGB_weighted_quarters340_selected_candidate_sealing':'HGB_quarter_numeric28_selected_candidate_sealing',
      'weighted_HGB340_complete_pipeline_actual_hidden_launches_20261007':'HGB_quarter_numeric28_complete_pipeline_actual_hidden_launches_20261007',
      'weighted_HGB_and_percentile_controls_github_20261007':'HGB_quarter_numeric_audit_github_20261007',
      'passed_actual340_weighted_flagged_HGB_full_official_comparisons':'passed_actual28_HGB_quarter_numeric_full_official_comparisons',
      'optimization_20261003_r117':'optimization_20261003_r118',
      '_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json',
      'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
      'round117_receipt.json':'round118_receipt.json',
      'validation_sync/round117':'validation_sync/round118','round117/':'round118/',"'round117'":"'round118'",
      'round117_full_scope':'round118_full_scope',
      'original_inference_selection_round117.json':'original_inference_selection_round118.json',
      'original_registry_alias_round117.json':'original_registry_alias_round118.json',
      'NUMBER = 117':'NUMBER = 118','number == 117':'number == 118',
      'WAVES = (400,)':'WAVES = (401,)','wave=400':'wave=401','wave400_results':'wave401_results',"'waves': [400]":"'waves': [401]",
      "'round': 117":"'round': 118",'== 340':'== 28',
      "'expected_scored_records': 340":"'expected_scored_records': 28", "'scored_records': 340":"'scored_records': 28",
      "'existing_actual_official_records': 340":"'existing_actual_official_records': 28", "'original_official_pilot_records_registered': 340":"'original_official_pilot_records_registered': 28",
      'lossless_ranking_display_qa_v28_20261007':'lossless_ranking_display_qa_v29_20261007',
      'ranking_display_qa_v28_20261007':'ranking_display_qa_v29_20261007',
      '(117, 28, 340)':'(118, 29, 28)',"namespace['snapshot'](117)":"namespace['snapshot'](118)",
      'actual_complete_QA_version=28':'actual_complete_QA_version=29',"'actual_full_QA_version': 28":"'actual_full_QA_version': 29",
      'all340':'all28','actual340':'actual28','the340':'the28','第117轮340项':'第118轮28项',
      '涨停HGB非等权集成与完整父方案组合':'HGB浮点加法顺序与完整父方案组合',
    }
    result={}
    for old,text in base.generate(112).items():
        new=NAMES[old];text=substitute(text,maps)
        if new.startswith('register_'):
            text=text.replace('explicit_comparison_parent_round=112',f'explicit_comparison_parent_round={parent}').replace("'explicit_parent_round': 112",f"'explicit_parent_round': {parent}")
        if new.startswith('publish_'):
            needle='    for path in extra:';assert text.count(needle)==1
            text=text.replace(needle,"    extra += [A / 'HGB_quarter_numeric28_actual_source_paths_before_registration_20261007.json', A / 'weighted_HGB340_actual_source_paths_before_registration_20261007.json']\n"+needle)
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += (");end=text.index('    previous = sync.git',start)
            text=text[:start]+"""    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮登记28项完整官方比较：112、116、117三个合格锚点，以及两种重复加法顺序乘12幅度和移除涨停HGB分支。'
        '先前数学比例覆盖审计发现这两种写法在完整5635800行预测上与既有等权均值存在浮点差异；本轮补充全部官方八项指标。'
        '每个集成保留四个有序加法槽，原生组件为两个；特征教师仍为106，非涨停和2020输出保留。'
        '合格候选仅按完整官方总分选优；冻结后完成完整原生及独立重放，或核对既有锚点全部封存字节和完整图。'
        '完整榜六视图、45秒浏览器QA29和全部源码参数检查保留；仅main，未读取真实测试标签。\\n').encode('utf-8')
"""+text[end:]
        compile(text,str(A/new),'exec');result[new]=text
    assert len(result)==8
    return result

def main():
    ready_path=A/'HGB_quarter_numeric28_selected_release_20261007/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual28_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'HGB_quarter_numeric28_official_comparison_20261007/verification.json')
    assert len(pilot['records'])==28 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round'];assert parent in (112,116,117)
    proof_path=A/'HGB_quarter_numeric28_round118_source_admission_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual25_controls_and24_prospective118_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists()
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name]
    preparation=A/'HGB_quarter_numeric28_round118_source_preparation_20261007.json';assert not preparation.exists()
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    create(preparation,{'status':'passed_actual28_sealed_candidate_and_admitted_full118_QA29_sources',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
      'round':118,'scored_records':28,'actual_comparison_parent_round':parent,'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
