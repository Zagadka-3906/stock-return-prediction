"""Predeclare all eight full-registration receivers; preserve complete parent graphs for every neural case."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_nonflag_ReverseBayesFine40_round134_sources_v3_20261008 as base
FAMILY='BF16wide40'
NAMES={name:name.replace('nonflag_ReverseBayesFine40',FAMILY).replace('round134','round135').replace('qa45','qa46').replace('_20261007','_20261008') for name in base.NAMES.values()}
# Original QA directory convention is preserved for the unchanged collector.
NAMES={old:(new.replace('_20261008','_20261007') if new.startswith(('lossless_','build_lossless_','verify_lossless_','collect_full_')) else new) for old,new in NAMES.items()}


def source_paths():
    names=[Path(__file__).name,'actual_BF16wide135_complete_dependency_recovery_v5_20261008.json','verify_BF16wide135_D_scoring_scope_v2_20261008.py','BF16wide135_D_scoring_scope_v2_20261008.json','actual_BF16wide135_D_scoring_receiver_recovery_v4_20261008.json','run_BF16wide40_official_comparison_v3_20261008.py',
        'prepare_BF16wide40_selected_candidate_v3_20261008.py','seal_BF16wide40_selected_candidate_v3_20261008.py',
        'verify_BF16wide40_round135_sources_v3_20261008.py','verify_BF16wide40_prospective_routes_v4_20261008.py',
        'run_BF16wide40_round135_full_registration_v3_20261008.py','publish_BF16wide40_evidence_v3_20261008.py',
        'queue_BF16wide135_complete_pipeline_v3_20261008.py','prepare_BF16wide135_receivers_v1_20261008.py',
        'BF16wide135_storage_v1_20261008.py','BF16_complete_parent_rank_CDF_v1_20261008.py',
        'BF16_complete_parent_native_stage_v1_20261008.py','predict_BF16_complete_parent_rank_scheme_v1_20261008.py',
        'neural_BF16_independent_forward_v1_20261008.py','neural_BF16_micro8192_native_v1_20261008.py',
        'train_neural_BF16_micro8192_bank6_v2_20261008.py','verify_BF16_full5_independent_GPU_v2_20261008.py',
        'verify_BF16_rank_CDF_full37_v1_20261008.py','verify_BF16_complete_parent_native_hook3_v1_20261008.py',
        'BF16wide40_round135_plan_v1_20261008.json','BF16wide40_prospective_routes_v3_20261008.json',
        'BF16wide135_receiver_preparation_v3_20261008.json','BF16wide40_actual_controls_index_v1_20261008.json',
        'BF16wide40_round135_source_admission_v3_20261008.json','BF16wide40_round135_source_preparation_v3_20261008.json',
        'BF16wide40_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'BF16wide40_scores_github_v3_20261008/receipt.json',
        'exact_native_JSON_archive_runtime_20261007.py','exact_native_pretty_JSON_archive_20261007.py',
        'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',
        'publish_explicit_parent_training_round_v2_20261005.py','all_forecast_percentile_runtime_20261007.py',
        'cached_official_spearman_runtime_20261007.py','resolve_sealed_scientific_protocol_v2_20261007.py']
    return [A/n for n in [*names,*NAMES.values()]]


def convert(text):
    mapping={'nonflag_ReverseBayesFine40':FAMILY,'round134':'round135','full134':'full135','actual134':'actual135',
        'prospective134':'prospective135','_r134':'_r135','NUMBER = 134':'NUMBER = 135','number == 134':'number == 135',
        'qa45':'qa46','QA45':'QA46','qa_v45':'qa_v46','WAVES = (417,)':'WAVES = (418,)',
        'wave=417':'wave=418','wave417_results':'wave418_results',"'waves': [417]":"'waves': [418]",
        "'round': 134":"'round': 135",'(134, 45, 40)':'(135, 46, 40)',"namespace['snapshot'](134)":"namespace['snapshot'](135)",
        'actual_complete_QA_version=45':'actual_complete_QA_version=46',"actual_full_QA_version': 45":"actual_full_QA_version': 46",
        'publish(134,':'publish(135,','lossless(134)':'lossless(135)',
        'passed_actual40_nonflag_ReverseBayes64_full_official_comparisons':'passed_actual40_BF16_complete_parent_rank_CDF_full_official_comparisons',
        'admit_empty_E_display_junction_v1_20261008':'BF16wide135_storage_v1_20261008'}
    value=substitute(text,mapping)
    value=value.replace('from BF16wide135_storage_v1_20261008 import ensure\n','from BF16wide135_storage_v1_20261008 import ensure_display as ensure\n')
    # Rename family paths and generated Python receivers, without changing old parent source identifiers.
    value=value.replace('BF16wide40_official_comparison_v1_20261007','BF16wide40_official_comparison_v3_20261008')
    value=value.replace('BF16wide40_selected_release_v1_20261007','BF16wide40_selected_release_v1_20261008')
    value=value.replace('BF16wide40_scores_github_v1_20261007','BF16wide40_scores_github_v3_20261008')
    for old,new in NAMES.items():
        previous=old.replace('nonflag_ReverseBayesFine40',FAMILY).replace('round134','round135').replace('qa45','qa46')
        value=value.replace(previous,new).replace(previous.removesuffix('.py'),new.removesuffix('.py'))
    return value


def generate(parent):
    assert parent in (112,133,134)
    result={NAMES[name]:convert(text) for name,text in base.generate(112).items()}
    for name,text in result.items():
        if name.startswith('register_'):
            text=text.replace('    assert not OUT.exists() and not CANDIDATE.exists()',
                "    assert not OUT.exists()\n    from BF16wide135_storage_v1_20261008 import empty\n    empty(CANDIDATE)")
            text=text.replace('    CANDIDATE.mkdir()\n','')
            start=text.index('    sources = [');end=text.index('    pins = ',start)
            text=text[:start]+"    from prepare_BF16wide40_round135_sources_v3_20261008 import source_paths\n    sources=source_paths()\n"+text[end:]
            text=text.replace("assert measured['all_complete_parent_flag_and2020_raw_bits_preserved'] and measured['reference106_feature_teacher_unchanged']",
                "assert measured['whole_complete_parent_branches_preserved_before_new_stage'] and measured['invalid_and_declared_unselected_raw_bits_preserved']")
            start=text.index("            graph.pop('nonflag_CPU_HGB_residual_CDF',None)");end=text.index('        row = ',start)
            text=text[:start]+'''            assert 'BF16_complete_parent_rank_CDF' not in graph
            if cfg['weight']==0.:
                assert cfg['model']=='zero_BF16_rank_identity' and measured['ordered_native_components']==[]
            else:
                assert measured['first2020_active'] and measured['ordered_native_components']==[cfg['model']]
                graph['BF16_complete_parent_rank_CDF']={**cfg,'rank_universe':cfg['universe'],
                    'first2020_active':True,'position':'after_complete_qualified_parent',
                    'actual_annual_native_bank':measured['native_bank_source'],
                    'original_complete_parent_round':pilot['actual_scheme_base_round'],
                    'original_complete_parent_graph_preserved':True,
                    'transformation':'inverseCDF_parent((1-weight)*parent_day_average_rank_over_N+weight*neural_day_average_rank_over_N)',
                    'future_candidate_not_inferred_for_nonselected_comparison':True}
''' +text[end:]
            text=text.replace("'existing_CPU_Ridge_native_bank_fits': 10","'existing_BF16_wide_native_bank_fits': 6")
            text=text.replace("'actual10_nonflag_CPU_Ridge_native_bank_source': str(A / 'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json')",
                "'actual6_BF16_wide_native_bank_source': str(A/'BF16wide40_actual_controls_index_v1_20261008.json')")
            text=text.replace("'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A / 'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json')",
                "'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A/'BF16wide40_actual_controls_index_v1_20261008.json')")
            text=text.replace("'nonflag_residual_ReverseBayes64_native_replay_verification.json' if READY", "'BF16_complete_parent_native_replay_verification.json' if READY")
        if name.startswith('publish_'):
            start=text.index('    extra = [');end=text.index('    for path in extra:',start)
            text=text[:start]+'''    from prepare_BF16wide40_round135_sources_v3_20261008 import source_paths
    extra=source_paths()+[ROOT/'candidates/optimization_20261003_r135/registry_alias_verification.json',Path(ready['source_candidate'])/'manifest.json']
    for folder in (A/'BF16wide40_selected_release_v1_20261008',Path(ready['source_release']),A/'BF16wide40_official_comparison_v3_20261008'):
        extra += list(folder.glob('*.json'))
    for name in ('BF16wide40_official_comparison_v3_20261008','BF16wide40_scores_main_publication_v3_20261008',
        'BF16wide40_selected_candidate_preparation_v3_20261008','BF16wide40_selected_candidate_sealing_v3_20261008'):
        folder=A/'service_owned_workflows_20261006'/name
        extra += list(folder.glob('*.json'))+list(folder.glob('*.log'))
''' +text[end:]
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += (");end=text.index("    previous = ",start)
            text=text[:start]+'''    payload[(prefix/'README.md').as_posix()] += ('\\n本轮40项：112、133、134合格锚点；全体有效、非涨停有效、涨停有效三组各12神经网络融合权重；零权重恒等对照。'
        '使用六个独立成熟窗口BF16宽网络，原生FP32固定8192推理与独立张量前向核对，完整父方案所有分支保留，2020参与新融合。'
        '37项完整5635800行及111冷前缀；官方连续八指标选优；新候选冻结后执行两次完整推理、独立复核和冷80，锚点则如实记录零新推理复用。'
        '保留完整榜六视图45秒QA46，仅main；未读取实际测试标签，选模偏差未校正，有限网格不证明穷尽。\\n').encode('utf8')
''' +text[end:]
            text=text.replace('登记第134轮40项反向贝叶斯残差幅度加密完整验证并发布完整榜与QA46','登记第135轮40项完整父方案与BF16宽网络融合并发布完整榜与QA46')
        if name=='optimize_training_round135.py':
            text=text.replace("'actual_flagged_HGB_small_amplitude_with_complete_compatible_parent'","'actual_complete_parent_BF16_rank_CDF_or_exact_qualified_anchor'")
        if name=='finalize_training_round135.py':
            marker="    assert sha(record['original_frozen_selection_source'])"
            text=text.replace(marker,"    for path,digest in record['frozen_external_input_sha256'].items():assert sha(path)==digest,path\n"+marker)
        overrides={'_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json',
            'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',"'explicit_parent_round': 112":f"'explicit_parent_round': {parent}",
            'explicit_comparison_parent_round=112':f'explicit_comparison_parent_round={parent}'}
        text=substitute(text,overrides)
        compile(text,str(A/name),'exec');result[name]=text
    assert len(result)==8
    return result


def main():
    ready_path=A/'BF16wide40_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'BF16wide40_official_comparison_v1_20261008/verification.json')
    assert len(pilot['records'])==40 and pilot['best']==ready['best']
    proof_path=A/'BF16wide40_round135_source_admission_v3_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual6_full5GPU37CDF111cold3hooks_and24_prospective135_sources'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists()
        assert hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'BF16wide40_round135_source_preparation_v3_20261008.json',{'status':'passed_actual40_sealed_candidate_and_admitted_full135_QA46_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':135,'scored_records':40,
        'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
