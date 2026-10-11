"""Predeclare eight full94-case registration/QA47 receivers while preserving every complete parent branch."""
from pathlib import Path
import hashlib,io,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_BF16wide40_round135_sources_v4_20261008 as base
NAMES={name:name.replace('BF16wide40','CrossFamily94').replace('round135','round136').replace('qa46','qa47') for name in base.NAMES.values()}


def source_paths():
    names=[Path(__file__).name,'CrossFamily94_round136_plan_v1_20261008.json','CrossFamily136_storage_v1_20261008.py',
        'CrossFamily_complete_parent_CDF_v1_20261008.py','CrossFamily_complete_parent_native_stage_v1_20261008.py','predict_CrossFamily_complete_parent_scheme_v1_20261008.py',
        'run_CrossFamily94_official_comparison_v1_20261008.py','prepare_CrossFamily94_selected_candidate_v1_20261008.py','seal_CrossFamily94_selected_candidate_v1_20261008.py',
        'verify_CrossFamily94_round136_sources_v1_20261008.py','verify_CrossFamily94_prospective_routes_v1_20261008.py','run_CrossFamily94_round136_full_registration_v1_20261008.py',
        'publish_CrossFamily94_evidence_v1_20261008.py','queue_CrossFamily136_complete_pipeline_v1_20261008.py','prepare_CrossFamily136_receiver_drafts_v1_20261008.py',
        'verify_CrossFamily91_current_parent_v1_20261008.py','verify_CrossFamily136_D_scoring_scope_v1_20261008.py','CrossFamily136_D_scoring_scope_v1_20261008.json',
        'CrossFamily94_prospective_routes_v1_20261008.json','CrossFamily136_receiver_preparation_v1_20261008.json','CrossFamily94_actual_controls_index_v1_20261008.json',
        'CrossFamily94_round136_source_admission_v1_20261008.json','CrossFamily94_round136_source_preparation_v1_20261008.json',
        'CrossFamily94_selected_release_v1_20261008/selected_candidate_ready_for_registration.json','CrossFamily94_scores_github_v1_20261008/receipt.json',
        'exact_native_JSON_archive_runtime_20261007.py','exact_native_pretty_JSON_archive_20261007.py','exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',
        'publish_explicit_parent_training_round_v2_20261005.py','all_forecast_percentile_runtime_20261007.py','cached_official_spearman_runtime_20261007.py',
        'resolve_sealed_scientific_protocol_v2_20261007.py','run_CrossFamily94_official_comparison_v1_20261008.py']
    return list(dict.fromkeys(A/name for name in [*names,*NAMES.values()]))


def convert(text):
    mapping={'BF16wide40':'CrossFamily94','BF16wide135_storage_v1_20261008':'CrossFamily136_storage_v1_20261008',
        'round135':'round136','full135':'full136','actual135':'actual136','prospective135':'prospective136','_r135':'_r136',
        'NUMBER = 135':'NUMBER = 136','number == 135':'number == 136','qa46':'qa47','QA46':'QA47','qa_v46':'qa_v47',
        'WAVES = (418,)':'WAVES = (419,)','wave=418':'wave=419','wave418_results':'wave419_results',"'waves': [418]":"'waves': [419]",
        "'round': 135":"'round': 136",'(135, 46, 40)':'(136, 47, 94)',"namespace['snapshot'](135)":"namespace['snapshot'](136)",
        'actual_complete_QA_version=46':'actual_complete_QA_version=47',"actual_full_QA_version': 46":"actual_full_QA_version': 47",
        'publish(135,':'publish(136,','lossless(135)':'lossless(136)',
        'passed_actual40_BF16_complete_parent_rank_CDF_full_official_comparisons':'passed_actual94_CrossFamily_complete_parent_full_official_comparisons',
        "len(pilot['records']) == 40":"len(pilot['records']) == 94","'expected_scored_records': 40":"'expected_scored_records': 94",
        'prepare_BF16wide40_round135_sources_v4_20261008':'prepare_CrossFamily94_round136_sources_v1_20261008'}
    # Replace specific source name before the generic family/round mapping.
    value=substitute(text,mapping)
    for stem in ('prepare_CrossFamily94_round136_sources','run_CrossFamily94_official_comparison','prepare_CrossFamily94_selected_candidate',
        'seal_CrossFamily94_selected_candidate','verify_CrossFamily94_round136_sources','publish_CrossFamily94_evidence','run_CrossFamily94_round136_full_registration'):
        value=value.replace(stem+'_v4_20261008',stem+'_v1_20261008')
    # In these eight registration/QA receivers, every numeric40 is the scope's record count.
    # Existing bank40 path strings and original52-model evidence stay byte-for-byte unchanged.
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    value=tokenize.untokenize([token._replace(string='94') if token.type==tokenize.NUMBER and token.string=='40' else token for token in tokens])
    value=value.replace('passed_actual40_scores_controls_and_sealed_selected_model_candidate_registered','passed_actual94_scores_controls_and_sealed_selected_model_candidate_registered')
    value=value.replace('actual_complete_parent_BF16_rank_CDF_or_exact_qualified_anchor','actual_complete_parent_CrossFamily_CDF_or_exact_qualified_anchor')
    value=value.replace('登记第135轮40项完整父方案与BF16宽网络融合并发布完整榜与QA47','登记第136轮94项跨模型完整方案并发布完整榜与QA47')
    return value


def generate(parent):
    assert parent in (112,134,135)
    result={NAMES[name]:convert(text) for name,text in base.generate(112).items()}
    for name,text in result.items():
        if name.startswith('register_'):
            start=text.index('    from prepare_');end=text.index('    pins = ',start)
            text=text[:start]+"    from prepare_CrossFamily94_round136_sources_v1_20261008 import source_paths\n    sources=source_paths()\n"+text[end:]
            start=text.index("            assert 'BF16_complete_parent_rank_CDF' not in graph");end=text.index('        row = ',start)
            text=text[:start]+'''            assert 'nonflag_CPU_CrossFamily_complete_parent_CDF' not in graph
            if cfg['weight']==0.:
                assert cfg['model']=='zero_CrossFamily_residual_identity' and measured['ordered_native_components']==[]
            else:
                assert measured['first2020_identity'] and len(measured['ordered_native_components']) in (2,4)
                graph['nonflag_CPU_CrossFamily_complete_parent_CDF']={**cfg,'amplitude':cfg['weight'],
                    'universe':cfg['universe'],'first2020_identity':True,'position':'after_complete_qualified_parent',
                    'teacher_feature':'qualified106_current_forecast_average_rank_over_N',
                    'ordered_native_component_heads':measured['ordered_native_components'],
                    'actual_annual_native_bank':measured['native_bank_source'],
                    'original_complete_parent_round':pilot['actual_scheme_base_round'],
                    'original_complete_parent_graph_preserved':True,
                    'transformation':'inverseCDF_complete_parent(parent_day_average_rank_over_N+amplitude*ordered_signed_nested_residual_mixture)',
                    'future_candidate_not_inferred_for_nonselected_comparison':True}
''' +text[end:]
            old="records.sort(key=lambda r: (-r['connected_final_score'], r['direct_rank_comparison_configuration']['weight'], r['original_comparison_case']))"
            new="records.sort(key=lambda r: (-r['connected_final_score'], r['actual_full_conditional_residual_control']['expected_unique_native_models'], r['direct_rank_comparison_configuration']['weight'], r['original_comparison_case']))"
            assert text.count(old)==1;text=text.replace(old,new)
            text=text.replace("'existing_BF16_wide_native_bank_fits': 6","'existing_CrossFamily_saved_native_heads': 30")
            text=text.replace("'actual6_BF16_wide_native_bank_source'","'actual30_CrossFamily_saved_native_heads_source'")
            text=text.replace("'BF16_complete_parent_native_replay_verification.json' if READY","'CrossFamily_complete_parent_native_replay_verification.json' if READY")
            text=text.replace('all40_full_numeric','all94_full_numeric').replace('actual_all40_controls','actual_all94_controls')
        if name.startswith('publish_'):
            start=text.index('    from prepare_');end=text.index('    for path in extra:',start)
            text=text[:start]+'''    from prepare_CrossFamily94_round136_sources_v1_20261008 import source_paths
    extra=source_paths()+[ROOT/'candidates/optimization_20261003_r136/registry_alias_verification.json',Path(ready['source_candidate'])/'manifest.json']
    for folder in (A/'CrossFamily94_selected_release_v1_20261008',Path(ready['source_release']),A/'CrossFamily94_official_comparison_v1_20261008'):
        extra += list(folder.glob('*.json'))
    for name in ('CrossFamily94_official_comparison_v1_20261008','CrossFamily94_scores_main_publication_v1_20261008',
        'CrossFamily94_selected_candidate_preparation_v1_20261008','CrossFamily94_selected_candidate_sealing_v1_20261008'):
        folder=A/'service_owned_workflows_20261006'/name
        extra += list(folder.glob('*.json'))+list(folder.glob('*.log'))
''' +text[end:]
            start=text.index("    payload[(prefix/'README.md').as_posix()] += (");end=text.index('    previous = ',start)
            text=text[:start]+'''    payload[(prefix/'README.md').as_posix()] += ('\\n本轮94项：112、134、135合格锚点，五类跨模型配对、三种混合比例、六种幅度共90项及零幅度恒等对照。'
        '六个既有残差头共30个成熟年度模型，特征64及标签逐行复核，原生、重载、独立JSON解码一致。'
        '新变换接在完整父方案全部分支之后，保留已有BF16分支；2020、涨停和无效行原始位不变。'
        '91项完整5635800行和273冷前缀，官方连续八指标选优；选中方案冻结后两次完整推理、独立复核和冷80，锚点如实记录零新推理。'
        '全部完整榜六视图45秒QA47，仅main；未读取实际测试标签，选模偏差未校正，有限网格不证明穷尽。\\n').encode('utf8')
''' +text[end:]
        overrides={'_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json','PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
            "'explicit_parent_round': 112":f"'explicit_parent_round': {parent}",'explicit_comparison_parent_round=112':f'explicit_comparison_parent_round={parent}'}
        text=substitute(text,overrides)
        compile(text,str(A/name),'exec');result[name]=text
    assert len(result)==8
    return result


def main():
    ready_path=A/'CrossFamily94_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual94_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'CrossFamily94_official_comparison_v1_20261008/verification.json')
    assert len(pilot['records'])==94 and pilot['best']==ready['best']
    proof_path=A/'CrossFamily94_round136_source_admission_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual30_heads91_current_CDF273cold15hooks_and24_prospective136_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'CrossFamily94_round136_source_preparation_v1_20261008.json',{'status':'passed_actual94_sealed_candidate_and_admitted_full136_QA47_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':136,'scored_records':94,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(path):sha(path) for path in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
