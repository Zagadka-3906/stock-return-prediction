"""Generate116 only after real88 scoring and sealed candidate, check all eight hashes first."""
from pathlib import Path
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_protected_upper_pool_HGB66_round115_sources_20261007 as base
NAMES={name:name.replace('protected_upper_pool_HGB66','flagged_HGB88').replace('round115','round116').replace('qa26','qa27') for name in base.NAMES.values()}

def generate_before_alias_controls(parent):
    assert parent in (112,114,115)
    mappings={**{old[:-3]:new[:-3] for old,new in NAMES.items()},
        'run_protected_upper_pool_HGB66_round115_full_registration_v5_20261007':'run_flagged_HGB88_round116_full_registration_v3_20261007',
        'prepare_protected_upper_pool_HGB66_round115_sources_20261007':Path(__file__).stem,
        'protected_upper_pool_HGB66_round115_source_preparation_20261007':'flagged_HGB88_round116_source_preparation_v3_20261007',
        'protected_upper_pool_HGB66_selected_release_20261007':'flagged_HGB_small_amplitude88_selected_release_v4_20261007',
        'protected_upper_pool_HGB66_official_comparison_v2_20261007':'flagged_HGB_small_amplitude88_official_comparison_v4_20261007',
        'passed_actual66_lower_pool_CPU_HGB_CDF_full_official_comparisons':'passed_actual88_flagged_HGB_small_amplitude_full_official_comparisons',
        'protected_upper_pool_HGB66_scores_v2_github_20261007':'flagged_HGB_small_amplitude88_scores_v4_github_20261007',
        'protected_upper_pool_HGB66_candidate_source_admission_20261007':'flagged_HGB88_round116_source_admission_20261007',
        'prepare_protected_upper_pool_HGB66_selected_candidate_20261007':'prepare_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007',
        'seal_protected_upper_pool_HGB66_selected_candidate_20261007':'seal_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007',
        'predict_protected_upper_pool_CPU_HGB_scheme_20261007':'predict_refined_flagged_CPU_HGB_scheme_20261007',
        'protected_upper_pool_HGB_CDF_transform_20261007':'refine_flagged_HGB_compatible_parent_transform_20261007',
        'protected_upper_pool_HGB_CDF_plan_20261007':'flagged_HGB_small_amplitude88_plan_20261007',
        'protected_upper_pool_HGB_CDF_preflight_20261007':'flagged_HGB_small_amplitude88_transform_preflight_20261007',
        'protected_upper_pool_HGB66_scoring_admission_20261007':'flagged_HGB_small_amplitude88_workflow_admission_20261007',
        'protected_upper_pool_HGB66_candidate_actual_launch_20261007':'flagged_HGB_small_amplitude88_actual_hidden_launches_20261007',
        'protected_upper_pool_HGB_selected_hook_preflight_20261007':'flagged_HGB_small_amplitude88_transform_preflight_20261007',
        'protected_upper_pool_HGB66_selected_candidate_preparation':'flagged_HGB_small_amplitude88_selected_candidate_preparation_v4',
        'protected_upper_pool_HGB66_selected_candidate_sealing':'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4',
        'protected_upper_pool_HGB66_official_comparison_v2':'flagged_HGB_small_amplitude88_official_comparison_v4',
        'protected_upper_pool_HGB66_scores_main_publication_v3':'flagged_HGB_small_amplitude88_scores_main_publication_v4',
        'cpu_full_universe_HGB24_bank_recovery_v2_github_20261007':'flagged_HGB_small_amplitude88_controls_github_20261007',
        'cpu_full_universe_HGB_bank24_recovery_v2_20261007':'cpu_conditional_residual_hgb_bank20_20261007',
        'cpu_full_universe_HGB_native_bank24_v2':'cpu_conditional_residual_hgb_native_bank20',
        'cpu_full_universe_HGB24_bank_evidence_publication_v2':'cpu_conditional_residual_hgb20_bank_evidence_publication',
        'round112_receipt.json':f'round{parent}_receipt.json','_r112':f'_r{parent}',
        'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
        'round115':'round116','_r115':'_r116','NUMBER = 115':'NUMBER = 116',
        'assert number == 115':'assert number == 116',"namespace['snapshot'](115)":"namespace['snapshot'](116)",
        'WAVES = (398,)':'WAVES = (399,)','wave=398':'wave=399','wave398_results':'wave399_results',
        "'waves': [398]":"'waves': [399]",'lossless_ranking_display_qa_v26_20261007':'lossless_ranking_display_qa_v27_20261007',
        'ranking_display_qa_v26_20261007':'ranking_display_qa_v27_20261007','(115, 26, 66)':'(116, 27, 88)',
        'actual_complete_QA_version=26':'actual_complete_QA_version=27',"'actual_full_QA_version': 26":"'actual_full_QA_version': 27",
        "'round': 115":"'round': 116",'== 66':'== 88',"'expected_scored_records': 66":"'expected_scored_records': 88",
        "'existing_actual_official_records': 66":"'existing_actual_official_records': 88", "'scored_records': 66":"'scored_records': 88",
        "'original_official_pilot_records_registered': 66":"'original_official_pilot_records_registered': 88",
        'all66':'all88','actual66':'actual88','the66':'the88','第115轮':'第116轮',
        'Register66':'Register88','66项低分区CPU HGB排序与CDF融合':'88项涨停HGB小权重与完整父方案组合',
    }
    generated={}
    for old,source in base.generate(112).items():
        name=NAMES[old];text=base.substitute(source,mappings)
        if name.startswith('register_'):
            text=text.replace("'original_inference_selection.json' if relative == 'selection.json' else relative", "'original_inference_selection_round116.json' if relative == 'selection.json' else relative")
            text=text.replace("assert measured['upper_boundary_ties_flags_and_invalid_parent_forecasts_bits_preserved'] and measured['lower_forecasts_stay_in_selected_parent_range']",
                "assert measured['all_complete_parent_nonflag_and2020_raw_bits_preserved'] and measured['reference106_feature_teacher_unchanged']")
            start=text.index("        if measured['case'] == pilot['best']['case']:")
            end=text.index('        row = ',start)
            text=text[:start]+"""        if measured['case'] == pilot['best']['case']:
            graph = deepcopy(actual['whole_scheme_graph'])
        elif cfg['model'] is None:
            graph = deepcopy(read(ROOT / f"candidates/optimization_20261003_r{cfg['anchor_round']}/verification.json")['whole_scheme_graph'])
        else:
            graph = deepcopy(read(ROOT / f"candidates/optimization_20261003_r{pilot['actual_scheme_base_round']}/verification.json")['whole_scheme_graph'])
            if cfg['model'] == 'remove_flagged_HGB':
                assert cfg['weight'] == 0. and measured['ordered_native_components'] == []
                graph.pop('conditional_flag_CPU_HGB_residual_CDF', None)
            else:
                graph['conditional_flag_CPU_HGB_residual_CDF'] = {**cfg,
                    'actual_annual_native_bank': measured['native_bank_source'],
                    'ordered_equal_mean_components': measured['ordered_native_components'],
                    'training_teacher_round': 106, 'first2020_identity': True,
                    'position': 'replace_flagged_HGB_before_optional_nonflag_lower_pool_stage',
                    'reference106_core_parameters_and_native_SHA_unchanged': True,
                    'transformation': '106_parent_percentile+weight*ordered_mean_raw_residual;106_parent_inverseCDF;flag_only',
                    'future_candidate_not_inferred_for_nonselected_comparison': True}
"""+text[end:]
            text=text.replace('explicit_comparison_parent_round=112',f'explicit_comparison_parent_round={parent}')
            text=text.replace("'explicit_parent_round': 112",f"'explicit_parent_round': {parent}")
            text=text.replace("'existing_CPU_HGB_native_bank_fits': 24","'existing_CPU_HGB_native_bank_fits': 20")
            text=text.replace('actual24_CPU_FULL_HGB_native_bank_source','actual20_conditional_CPU_HGB_native_bank_source')
            text=text.replace("'protected_upper_pool_HGB_native_replay_verification.json'","'refined_flagged_HGB_native_replay_verification.json'")
            text=text.replace("preserved_scheme_training_parent_round=106,", "preserved_scheme_training_parent_round=106, actual_scheme_base_round=pilot['actual_scheme_base_round'],")
        elif name.startswith('optimize_'):
            text=text.replace('actual_lower_pool_CPU_HGB_CDF_after_complete_qualified_parent','actual_flagged_HGB_small_amplitude_with_complete_compatible_parent')
        elif name.startswith('publish_'):
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += (")
            end=text.index('    previous = sync.git',start)
            text=text[:start]+"""    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮登记88项完整官方比较：112、114、115三个合格锚点，以及84项预定涨停HGB小权重和一项移除涨停HGB的消融。'
        '比较基准按所有锚点完整总分选定；改进方案基底在兼容106模型核心的锚点中选定，两者分别记录。'
        '复用20个既有年度模型，原106特征教师不变；当前完整父方案的非涨停部分和2020预测逐位保留。'
        '只按完整官方总分选择，不设单项或显著性额外门槛。'
        '新方案先冻结再完成1599600行原生及独立解码、两次重放、CSV和冷80日检查。'
        '已有锚点核对逐位预测、8项指标、完整图和封存文件后复用，0新推理。'
        '完整榜六视图和45秒浏览器检查保留，只main，未读取真实测试标签。\\n').encode('utf-8')
"""+text[end:]
        compile(text,str(A/name),'exec');generated[name]=text
    assert len(generated)==8
    return generated

def main():
    ready_path=A/'flagged_HGB_small_amplitude88_selected_release_v4_20261007/selected_candidate_ready_for_registration.json'
    ready=read(ready_path)
    assert ready['status']=='passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'flagged_HGB_small_amplitude88_official_comparison_v4_20261007/verification.json')
    assert len(pilot['records'])==88 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round'];assert parent in (112,114,115)
    assert read(A/'optimization_20261003_r115/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round115_receipt.json')['actual_full_QA_version']==26
    candidate=Path(ready['source_candidate']);assert sha(candidate/'manifest.json')==ready['source_manifest_sha256']
    for relative,info in read(candidate/'manifest.json')['files'].items():assert sha(candidate/relative)==info['sha256'],relative
    assert read(candidate/'verification.json')['whole_scheme_graph']==read(candidate/'selection.json')['winner']['conditional_flag_residual_scheme_graph']
    proof_path=A/'flagged_HGB88_round116_source_admission_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual85_full_controls_and24_prospective116_source_schema_baseline_and_ablation_routes'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists(),name
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name],name
    preparation=A/'flagged_HGB88_round116_source_preparation_v3_20261007.json';assert not preparation.exists()
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    sources=[Path(__file__),A/'run_flagged_HGB88_round116_full_registration_v3_20261007.py',ready_path,proof_path,*[A/n for n in NAMES.values()]]
    create(preparation,{'status':'passed_actual88_sealed_candidate_registry_and_original_QA27_source_routes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'scored_records':88,'round':116,'wave':399,'actual_comparison_parent_round':parent,'actual_scheme_base_round':pilot['actual_scheme_base_round'],
        'all_eight_hashes_checked_before_any_canonical_file_written':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


def generate(parent):
    generated=generate_before_alias_controls(parent)
    for name,text in generated.items():
        if name.startswith('register_'):
            text=text.replace("'original_inference_selection_round116.json' if relative == 'selection.json' else relative", "'original_inference_selection_round116.json' if relative == 'selection.json' else ('original_registry_alias_round116.json' if relative == 'registry_alias_verification.json' else relative)")
            text=text.replace("target = CANDIDATE / 'registration_sources' / source.name", "target = CANDIDATE / 'registration_sources' / 'round116_full_scope' / source.relative_to(ROOT)")
        compile(text,str(A/name),'exec');generated[name]=text
    return generated

if __name__=='__main__':main()
