"""Prepare immutable round116 routing from original full eight-file QA templates."""
from pathlib import Path
import ast
import hashlib
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
import prepare_protected_upper_pool_HGB66_round115_sources_20261007 as original

GENERATOR='prepare_flagged_HGB88_round116_sources_20261007.py'
DRIVER='run_flagged_HGB88_round116_full_registration_20261007.py'
PROOF='flagged_HGB88_round116_source_admission_20261007.json'

def main():
    generator=A/GENERATOR;driver=A/DRIVER;verifier=A/'verify_flagged_HGB88_round116_sources_20261007.py'
    assert all(not p.exists() for p in (generator,driver,verifier))
    text='''"""Generate116 only after real88 scoring and sealed candidate, check all eight hashes first."""
from pathlib import Path
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_protected_upper_pool_HGB66_round115_sources_20261007 as base
NAMES={name:name.replace('protected_upper_pool_HGB66','flagged_HGB88').replace('round115','round116').replace('qa26','qa27') for name in base.NAMES.values()}

def generate(parent):
    assert parent in (112,114,115)
    mappings={**{old[:-3]:new[:-3] for old,new in NAMES.items()},
        'run_protected_upper_pool_HGB66_round115_full_registration_20261007':'run_flagged_HGB88_round116_full_registration_20261007',
        'prepare_protected_upper_pool_HGB66_round115_sources_20261007':Path(__file__).stem,
        'protected_upper_pool_HGB66_round115_source_preparation_20261007':'flagged_HGB88_round116_source_preparation_20261007',
        'protected_upper_pool_HGB66_selected_release_20261007':'flagged_HGB_small_amplitude88_selected_release_20261007',
        'protected_upper_pool_HGB66_official_comparison_v2_20261007':'flagged_HGB_small_amplitude88_official_comparison_20261007',
        'passed_actual66_lower_pool_CPU_HGB_CDF_full_official_comparisons':'passed_actual88_flagged_HGB_small_amplitude_full_official_comparisons',
        'protected_upper_pool_HGB66_scores_v2_github_20261007':'flagged_HGB_small_amplitude88_scores_github_20261007',
        'protected_upper_pool_HGB66_candidate_source_admission_20261007':'flagged_HGB88_round116_source_admission_20261007',
        'prepare_protected_upper_pool_HGB66_selected_candidate_20261007':'prepare_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007',
        'seal_protected_upper_pool_HGB66_selected_candidate_20261007':'seal_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007',
        'predict_protected_upper_pool_CPU_HGB_scheme_20261007':'predict_refined_flagged_CPU_HGB_scheme_20261007',
        'protected_upper_pool_HGB_CDF_transform_20261007':'refine_flagged_HGB_compatible_parent_transform_20261007',
        'protected_upper_pool_HGB_CDF_plan_20261007':'flagged_HGB_small_amplitude88_plan_20261007',
        'protected_upper_pool_HGB_CDF_preflight_20261007':'flagged_HGB_small_amplitude88_transform_preflight_20261007',
        'protected_upper_pool_HGB66_scoring_admission_20261007':'flagged_HGB_small_amplitude88_workflow_admission_20261007',
        'protected_upper_pool_HGB66_candidate_actual_launch_20261007':'flagged_HGB_small_amplitude88_actual_hidden_launches_20261007',
        'protected_upper_pool_HGB_selected_hook_preflight_20261007':'flagged_HGB_small_amplitude88_transform_preflight_20261007',
        'protected_upper_pool_HGB66_selected_candidate_preparation':'flagged_HGB_small_amplitude88_selected_candidate_preparation',
        'protected_upper_pool_HGB66_selected_candidate_sealing':'flagged_HGB_small_amplitude88_selected_candidate_sealing',
        'protected_upper_pool_HGB66_official_comparison_v2':'flagged_HGB_small_amplitude88_official_comparison',
        'protected_upper_pool_HGB66_scores_main_publication_v3':'flagged_HGB_small_amplitude88_scores_main_publication',
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
            text=text.replace('preserved_scheme_training_parent_round=106,','preserved_scheme_training_parent_round=106, actual_scheme_base_round=pilot[\'actual_scheme_base_round\'],')
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
    ready_path=A/'flagged_HGB_small_amplitude88_selected_release_20261007/selected_candidate_ready_for_registration.json'
    ready=read(ready_path)
    assert ready['status']=='passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'flagged_HGB_small_amplitude88_official_comparison_20261007/verification.json')
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
    preparation=A/'flagged_HGB88_round116_source_preparation_20261007.json';assert not preparation.exists()
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\\n') as stream:stream.write(text)
    sources=[Path(__file__),A/'run_flagged_HGB88_round116_full_registration_20261007.py',ready_path,proof_path,*[A/n for n in NAMES.values()]]
    create(preparation,{'status':'passed_actual88_sealed_candidate_registry_and_original_QA27_source_routes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'scored_records':88,'round':116,'wave':399,'actual_comparison_parent_round':parent,'actual_scheme_base_round':pilot['actual_scheme_base_round'],
        'all_eight_hashes_checked_before_any_canonical_file_written':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
'''
    compile(text,str(generator),'exec')
    with generator.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    source=A/'run_protected_upper_pool_HGB66_round115_full_registration_20261007.py'
    runtime=source.read_text(encoding='utf8')
    substitutions={
        'protected_upper_pool_HGB66_official_comparison_v2':'flagged_HGB_small_amplitude88_official_comparison',
        'protected_upper_pool_HGB66_scores_main_publication_v3':'flagged_HGB_small_amplitude88_scores_main_publication',
        'protected_upper_pool_HGB66_selected_candidate_sealing':'flagged_HGB_small_amplitude88_selected_candidate_sealing',
        'CPU_ELASTIC44_round114_full_registration_v3':'protected_upper_pool_HGB66_round115_full_registration',
        'protected_upper_pool_HGB66_selected_release_20261007':'flagged_HGB_small_amplitude88_selected_release_20261007',
        'prepare_protected_upper_pool_HGB66_round115_sources_20261007':GENERATOR[:-3],
        'register_protected_upper_pool_HGB66_round115_artifacts_20261007':'register_flagged_HGB88_round116_artifacts_20261007',
        'publish_protected_upper_pool_HGB66_round115_full_validation_20261007':'publish_flagged_HGB88_round116_full_validation_20261007',
        'protected_upper_pool_HGB66_round115_actual_registration_20261007':'flagged_HGB88_round116_actual_registration_20261007',
        'protected_upper_pool_HGB66_full115_20261007':'flagged_HGB88_full116_20261007',
        'optimization_20261003_r115':'optimization_20261003_r116','(112,113,114)':'(112,114,115)',
        'publish(115,':'publish(116,','lossless(115)':'lossless(116)',
        'lossless_ranking_runtime_adapter_round115_20261007':'lossless_ranking_runtime_adapter_round116_20261007',
        'passed_actual66_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes',
        "'existing_official_scores_registered':66":"'existing_official_scores_registered':88",
        '完整父方案后的低分区HGB排序与CDF优化':'完整父方案的涨停HGB小权重优化',
        '预定66项完整官方比较：三个合格锚点和63个低分区方案':'预定88项完整官方比较：三个合格锚点、84项小权重和一个消融',
        'lower_pool_HGB66_full115':'flagged_HGB88_full116','Register66':'Register88','QA26':'QA27'}
    runtime=original.substitute(runtime,substitutions)
    compile(runtime,str(driver),'exec')
    with driver.open('x',encoding='utf8',newline='\n') as f:f.write(runtime)
    # Reuse the baseline metadata regression harness, not its claimed historical native hook.
    source=A/'verify_protected_upper_pool_HGB66_round115_sources_20261007.py'
    check=source.read_text(encoding='utf8')
    mappings={
        'prepare_protected_upper_pool_HGB66_round115_sources_20261007':GENERATOR[:-3],
        'run_protected_upper_pool_HGB66_round115_full_registration_20261007':DRIVER[:-3],
        'protected_upper_pool_HGB_selected_hook_preflight':'flagged_HGB_small_amplitude88_transform_preflight',
        'passed_actual_historical603_features_native_HGB_lower_pool_hook_and_whole_day_prefix_controls':'passed_actual85_full5635800_flagged_HGB_small_amplitude_independent_oracle_and_cold80_260_975_controls',
        'protected_upper_pool_HGB66_candidate_source_admission_20261007':PROOF[:-5],
        'prepare_protected_upper_pool_HGB66_selected_candidate_20261007':'prepare_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007',
        'seal_protected_upper_pool_HGB66_selected_candidate_20261007':'seal_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007',
        'predict_protected_upper_pool_CPU_HGB_scheme_20261007':'predict_refined_flagged_CPU_HGB_scheme_20261007',
        'protected_upper_pool_HGB_CDF_transform_20261007':'refine_flagged_HGB_compatible_parent_transform_20261007',
        'run_protected_upper_pool_HGB66_official_comparison_v2_20261007':'run_flagged_HGB_small_amplitude88_official_comparison_20261007',
        'register_protected_upper_pool_HGB66_round115_artifacts_20261007':'register_flagged_HGB88_round116_artifacts_20261007',
        '(112,113,114)':'(112,114,115)',
        'passed_actual_native_hook_and24_prospective_source_AST_hashes_schema_and_parent_baseline_controls':'passed_actual85_full_controls_and24_prospective116_source_schema_baseline_and_ablation_routes',
        "'actual_historical_hook_cases':63":"'actual_full_training_transform_controls':85",
        "'canonical115_sources_written'":"'canonical116_sources_written'",'QA26':'QA27',
        'all_eight_hashes_checked_before_any_production_write':'all_eight_hashes_checked_before_any_production_write'}
    check=original.substitute(check,mappings)
    check=check.replace("assert len(hook['records'])==63","assert hook['actual_full5635800_controls']==85")
    check=check.replace('*[A/n for n in generator.NAMES]', '*[A/n for n in original.NAMES], A/\'prepare_flagged_HGB88_round116_pipeline_20261007.py\'')
    check=check.replace('    import prepare_flagged_HGB88_round116_sources_20261007 as generator','    import prepare_flagged_HGB88_round116_sources_20261007 as generator\n    import prepare_protected_upper_pool_HGB66_round115_sources_20261007 as original')
    # Actual nonselected graph routing: ablation drops only flagged HGB; optional lower graph survives.
    injection="""        branch_start=generated['register_flagged_HGB88_round116_artifacts_20261007.py'].index(\"        if measured['case'] == pilot['best']['case']:\")
        branch_end=generated['register_flagged_HGB88_round116_artifacts_20261007.py'].index('        row = ',branch_start)
        branch=generated['register_flagged_HGB88_round116_artifacts_20261007.py'][branch_start:branch_end]
        branch_code=compile('if True:\\n'+branch,'actual_prospective116_graph_branch','exec')
        fake={'core':{'native_SHA':'preserved106'},'conditional_flag_CPU_HGB_residual_CDF':{'old':True},'protected_upper_pool_CPU_HGB_CDF':{'keep':True}}
        for model,weight,names in [('remove_flagged_HGB',0.,[]),('flagged_residual_hgb7_absolute',.0125,['flagged_residual_hgb7_absolute'])]:
            cfg={'model':model,'weight':weight,'anchor_round':112,'universe':'all_current_raw_forecasts'}
            measured={'case':7,'native_bank_source':'existing20','ordered_native_components':names}
            ns={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':112},'deepcopy':deepcopy,'read':lambda path:{'whole_scheme_graph':fake},'ROOT':ROOT}
            exec(branch_code,ns);graph=ns['graph']
            assert graph['core']==fake['core'] and graph['protected_upper_pool_CPU_HGB_CDF']==fake['protected_upper_pool_CPU_HGB_CDF']
            if model=='remove_flagged_HGB':assert 'conditional_flag_CPU_HGB_residual_CDF' not in graph
            else:assert graph['conditional_flag_CPU_HGB_residual_CDF']['training_teacher_round']==106
"""
    check=check.replace('        function=next(n for n in registry.body',injection+'        function=next(n for n in registry.body')
    compile(check,str(verifier),'exec')
    with verifier.open('x',encoding='utf8',newline='\n') as f:f.write(check)
    create(A/'flagged_HGB88_round116_pipeline_preparation_20261007.json',{'status':'compiled_three_prospective_pipeline_sources_not_admitted_or_launched',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),generator,driver,verifier)},'canonical116_sources_written':0,'new_native_fits':0,'new_quality_scores':0})
    print({'status':'compiled','pipeline_sources':3},flush=True)

if __name__=='__main__':main()
