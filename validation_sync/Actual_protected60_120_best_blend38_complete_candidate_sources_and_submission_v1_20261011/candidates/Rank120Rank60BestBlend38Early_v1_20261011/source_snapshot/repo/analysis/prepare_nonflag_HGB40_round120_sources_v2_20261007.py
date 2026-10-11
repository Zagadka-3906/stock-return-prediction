"""Compose full120 registration, preserving the complete existing flag branch."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_quantile_HGB88_round119_sources_v5_20261007 as base
from prepare_nonflag_HGB40_science_sources_20261007 import MAP as SCIENCE_MAP,FILES
from prepare_nonflag_HGB40_complete_routes_v2_20261007 import mapping

NAMES={old:old.replace('quantile_HGB88','nonflag_HGB40').replace('round119','round120').replace('qa30','qa31') for old in base.NAMES.values()}

def generate(parent):
    assert parent in (112,118,119)
    m={**SCIENCE_MAP,**{o[:-3]:n[:-3] for o,n in NAMES.items()}}
    m.update({old.replace('_v4_20261007','_v5_20261007')[:-3]:new[:-3].replace('_20261007','_v2_20261007') for old,new in FILES.items()})
    m.update({
      'prepare_quantile_HGB88_round119_sources_v5_20261007':Path(__file__).stem,
      'quantile_HGB88_round119_source_admission_v5_20261007':'nonflag_HGB40_round120_source_admission_v2_20261007',
      'quantile_HGB88_round119_source_preparation_v5_20261007':'nonflag_HGB40_round120_source_preparation_v2_20261007',
      'quantile_HGB88_selected_release_v5_20261007':'nonflag_HGB40_selected_release_v2_20261007',
      'quantile_HGB88_official_comparison_v5_20261007':'nonflag_HGB40_official_comparison_v2_20261007',
      'quantile_HGB88_scores_github_v5_20261007':'nonflag_HGB40_scores_github_20261007',
      'quantile_HGB88_round119_full_registration_v5':'nonflag_HGB40_round120_full_registration',
      'run_quantile_HGB88_round119_full_registration_v5_20261007':'run_nonflag_HGB40_round120_full_registration_v2_20261007',
      'quantile_HGB88_selected_candidate_preparation_v5':'nonflag_HGB40_selected_candidate_preparation',
      'quantile_HGB88_selected_candidate_sealing_v5':'nonflag_HGB40_selected_candidate_sealing',
      'quantile_HGB88_official_comparison_v5':'nonflag_HGB40_official_comparison',
      'quantile_HGB88_scores_main_publication_v5':'nonflag_HGB40_scores_main_publication',
      'optimization_20261003_r119':'optimization_20261003_r120',
      'round119_full_scope':'round120_full_scope',
      'original_inference_selection_round119.json':'original_inference_selection_round120.json',
      'original_registry_alias_round119.json':'original_registry_alias_round120.json',
      'round119_receipt.json':'round120_receipt.json',
      'validation_sync/round119':'validation_sync/round120','round119/':'round120/',"'round119'":"'round120'",
      'NUMBER = 119':'NUMBER = 120','number == 119':'number == 120',
      'WAVES = (402,)':'WAVES = (403,)','wave=402':'wave=403','wave402_results':'wave403_results',
      "'waves': [402]":"'waves': [403]", "'round': 119":"'round': 120",
      'lossless_ranking_display_qa_v30_20261007':'lossless_ranking_display_qa_v31_20261007',
      'ranking_display_qa_v30_20261007':'ranking_display_qa_v31_20261007',
      '(119, 30, 88)':'(120, 31, 40)','collect(119, 30, 88)':'collect(120, 31, 40)',
      "namespace['snapshot'](119)":"namespace['snapshot'](120)",
      'actual_complete_QA_version=30':'actual_complete_QA_version=31',"'actual_full_QA_version': 30":"'actual_full_QA_version': 31",
      '== 88':'== 40',"'expected_scored_records': 88":"'expected_scored_records': 40",
      "'scored_records': 88":"'scored_records': 40", "'existing_actual_official_records': 88":"'existing_actual_official_records': 40",
      "'original_official_pilot_records_registered': 88":"'original_official_pilot_records_registered': 40",
      "'existing_CPU_HGB_native_bank_fits': 20":"'existing_CPU_HGB_native_bank_fits': 10",
      'all88':'all40','actual88':'actual40','the88':'the40',
      '_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json','PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
      'quantile_HGB88_actual_source_paths_before_registration_20261007':'nonflag_HGB40_actual_source_paths_before_registration_20261007',
      'quantile_HGB88_complete_pipeline_actual_hidden_launches_v3_20261007':'nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007',
      '分位数HGB与完整父方案组合':'非涨停残差HGB与完整父方案组合',
    })
    result={}
    for old,text in base.generate(112).items():
        new=NAMES[old];text=substitute(text,m)
        if new.startswith('register_'):
            text=text.replace('explicit_comparison_parent_round=112',f'explicit_comparison_parent_round={parent}').replace("'explicit_parent_round': 112",f"'explicit_parent_round': {parent}")
            text=text.replace('all_complete_parent_nonflag_and2020_raw_bits_preserved','all_complete_parent_flag_and2020_raw_bits_preserved')
            text=text.replace('conditional_flag_CPU_HGB_residual_CDF','nonflag_CPU_HGB_residual_CDF')
            text=text.replace('in (1,2,4)','in (1,2)').replace('replace_flagged_HGB_before_optional_nonflag_lower_pool_stage','after_complete_parent_flag_branch')
            text=text.replace('106_parent_inverseCDF;flag_only','106_parent_inverseCDF;nonflag_only')
            needle="        A / 'collect_full_lossless_round120_qa31_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        A / 'nonflag_residual_HGB_native_stage_20261007.py',\n        A / 'nonflag_residual_HGB_CDF_transform_20261007.py',\n        A / 'nonflag_residual_HGB_preprocessing_20261007.py',\n        A / 'nonflag_residual_HGB_native_hook3_preflight_20261007/verification.json',")
        elif new.startswith('publish_'):
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += (");end=text.index('    previous = sync.git',start)
            text=text[:start]+"""    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮登记40项完整官方比较：112、118、119三个合格锚点、两个非涨停残差HGB及其等权集成乘12幅度，以及消融。'
        '实际10年度成熟模型，教师106；保留父方案完整涨停分支和2020输出。'
        '37项5635800行CDF与111冷前缀通过；完整官方八指标选优后冻结，完整候选原生重载、独立解码、两次重放及冷80核对。'
        '完整榜六视图和45秒QA31保留，全部源码参数可核对。仅main，未读取真实测试标签。有限网格不证明优化穷尽。\\n').encode('utf8')
"""+text[end:]
        compile(text,str(A/new),'exec');result[new]=text
    assert len(result)==8
    return result

def main():
    ready_path=A/'nonflag_HGB40_selected_release_v2_20261007/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'nonflag_HGB40_official_comparison_v2_20261007/verification.json')
    assert len(pilot['records'])==40 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round'];proof_path=A/'nonflag_HGB40_round120_source_admission_v2_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual37_controls_and24_prospective120_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists(),name
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name]
    preparation=A/'nonflag_HGB40_round120_source_preparation_v2_20261007.json';assert not preparation.exists()
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(preparation,{'status':'passed_actual40_sealed_candidate_and_admitted_full120_QA31_sources',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':120,'scored_records':40,'actual_comparison_parent_round':parent,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
