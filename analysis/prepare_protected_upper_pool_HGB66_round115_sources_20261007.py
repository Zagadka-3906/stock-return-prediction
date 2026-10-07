"""Generate full round115 only after actual sealing; precheck all eight hashes before any write."""
from pathlib import Path
import hashlib
import re
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

NAMES={
    'register_CPU_FULL_HGB44_round113_artifacts_20261007.py':'register_protected_upper_pool_HGB66_round115_artifacts_20261007.py',
    'optimize_training_round113.py':'optimize_training_round115.py',
    'finalize_training_round113.py':'finalize_training_round115.py',
    'publish_CPU_FULL_HGB44_round113_full_validation_20261007.py':'publish_protected_upper_pool_HGB66_round115_full_validation_20261007.py',
    'build_lossless_ranking_display_round113_20261007.py':'build_lossless_ranking_display_round115_20261007.py',
    'verify_lossless_ranking_display_round113_20261007.py':'verify_lossless_ranking_display_round115_20261007.py',
    'lossless_ranking_runtime_adapter_round113_20261007.py':'lossless_ranking_runtime_adapter_round115_20261007.py',
    'collect_full_lossless_round113_qa24_20261007.py':'collect_full_lossless_round115_qa26_20261007.py',
}


def substitute(text,mappings):
    return re.sub('|'.join(map(re.escape,sorted(mappings,key=len,reverse=True))),lambda m:mappings[m.group()],text)


def generate(parent):
    assert parent in (112,113,114)
    mappings={**{k[:-3]:v[:-3] for k,v in NAMES.items()},
        'run_CPU_FULL_HGB44_round113_full_registration_v4_20261007':'run_protected_upper_pool_HGB66_round115_full_registration_20261007',
        'prepare_CPU_FULL_HGB44_round113_sources_v4_20261007':Path(__file__).stem,
        'CPU_FULL_HGB44_round113_source_preparation_v4_20261007':'protected_upper_pool_HGB66_round115_source_preparation_20261007',
        'CPU_FULL_HGB_residual44_selected_release_recovery_v2_20261007':'protected_upper_pool_HGB66_selected_release_20261007',
        'full_universe_HGB44_official_comparison_v3_20261007':'protected_upper_pool_HGB66_official_comparison_v2_20261007',
        'passed_actual44_full_universe_CPU_HGB_CDF_full_official_comparisons':'passed_actual66_lower_pool_CPU_HGB_CDF_full_official_comparisons',
        'cpu_full_universe_HGB24_scores_recovery_v2_github_20261007':'protected_upper_pool_HGB66_scores_v2_github_20261007',
        'CPU_FULL_HGB44_selected_candidate_source_admission_20261007':'protected_upper_pool_HGB66_candidate_source_admission_20261007',
        'prepare_CPU_FULL_HGB_residual44_selected_candidate_v2_20261007':'prepare_protected_upper_pool_HGB66_selected_candidate_20261007',
        'seal_CPU_FULL_HGB_residual44_selected_candidate_v2_20261007':'seal_protected_upper_pool_HGB66_selected_candidate_20261007',
        'predict_full_universe_CPU_HGB_rank_CDF_scheme_20261007':'predict_protected_upper_pool_CPU_HGB_scheme_20261007',
        'full_universe_HGB_selected_hook_preflight_20261007':'protected_upper_pool_HGB_selected_hook_preflight_20261007',
        'CPU_FULL_HGB44_selected_candidate_preparation_v2':'protected_upper_pool_HGB66_selected_candidate_preparation',
        'CPU_FULL_HGB44_selected_candidate_sealing_v2':'protected_upper_pool_HGB66_selected_candidate_sealing',
        'full_universe_HGB44_official_comparison_v3':'protected_upper_pool_HGB66_official_comparison_v2',
        'cpu_full_universe_HGB24_scores_evidence_publication_v2':'protected_upper_pool_HGB66_scores_main_publication_v3',
        'round112_receipt.json':f'round{parent}_receipt.json','_r112':f'_r{parent}',
        'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
        'round113':'round115','_r113':'_r115','NUMBER = 113':'NUMBER = 115',
        'assert number == 113':'assert number == 115',"namespace['snapshot'](113)":"namespace['snapshot'](115)",
        'WAVES = (396,)':'WAVES = (398,)','wave=396':'wave=398','wave396_results':'wave398_results',
        "'waves': [396]":"'waves': [398]",'lossless_ranking_display_qa_v24_20261007':'lossless_ranking_display_qa_v26_20261007',
        'ranking_display_qa_v24_20261007':'ranking_display_qa_v26_20261007','(113, 24, 44)':'(115, 26, 66)',
        'actual_complete_QA_version=24':'actual_complete_QA_version=26',"'actual_full_QA_version': 24":"'actual_full_QA_version': 26",
        "'round': 113":"'round': 115",'== 44':'== 66',"'expected_scored_records': 44":"'expected_scored_records': 66",
        "'existing_actual_official_records': 44":"'existing_actual_official_records': 66", "'scored_records': 44":"'scored_records': 66",
        "'original_official_pilot_records_registered': 44":"'original_official_pilot_records_registered': 66",
        'all44':'all66','actual44':'actual66','the44':'the66','official44':'official66','第113轮':'第115轮',
    }
    generated={}
    for old,new in NAMES.items():
        original=(A/old).read_text(encoding='utf8');effective={k:v for k,v in mappings.items() if k in original}
        text=substitute(original,effective)
        if old.startswith('register_'):
            text=text.replace("measured['qualified_anchor_all_metrics_exact']","measured['qualified_anchor_all8_metrics_exact']")
            text=text.replace("assert measured['full_pool_transformation_including_nonflag_and2020_actual_native_forecasts'] and measured['actual2020_native_fold_used_in_nonanchor_scheme']",
                "assert measured['upper_boundary_ties_flags_and_invalid_parent_forecasts_bits_preserved'] and measured['lower_forecasts_stay_in_selected_parent_range']")
            start=text.index("        if measured['case'] == pilot['best']['case']:")
            end=text.index('        row = ',start)
            text=text[:start]+f"""        if measured['case'] == pilot['best']['case']:
            graph = deepcopy(actual['whole_scheme_graph'])
        elif cfg['model'] is None:
            graph = deepcopy(read(ROOT / f"candidates/optimization_20261003_r{{cfg['anchor_round']}}/verification.json")['whole_scheme_graph'])
        else:
            graph = deepcopy(read(ROOT / 'candidates/optimization_20261003_r{parent}/verification.json')['whole_scheme_graph'])
            graph['protected_upper_pool_CPU_HGB_CDF'] = {{**cfg,
                'actual_annual_native_bank': measured['native_bank_source'],
                'ordered_native_components': measured['ordered_native_components'],
                'position': 'after_complete_qualified_parent_graph',
                'strict_boundary_ties_outside_lower_pool': True,
                'pool_uses_only_current_forecasts_flags_and_price_valid': True,
                'transformation': 'ordered_mean_of_within_lower_pool_head_percentiles; convex_mix; lower_pool_parent_inverseCDF',
                'official_Top_invariance_not_assumed': True,
                'future_candidate_not_inferred_for_nonselected_comparison': True}}
"""+text[end:]
            text=text.replace('explicit_comparison_parent_round=112',f'explicit_comparison_parent_round={parent}')
            text=text.replace("'explicit_parent_round': 112",f"'explicit_parent_round': {parent}")
            text=text.replace("pilot['ensembles']","pilot['components']")
            text=text.replace("'actual_new_CPU_FULL_HGB_native_bank_fits': 24, 'saved_selected_parent_models': 15",
                f"'existing_CPU_HGB_native_bank_fits': 24, 'saved_selected_parent_models': len(read(ROOT / 'candidates/optimization_20261003_r{parent}/verification.json')['models'])")
            text=text.replace("str(SOURCE_CANDIDATE / 'conditional_residual_native_replay_verification.json')",
                "str(SOURCE_CANDIDATE / ('protected_upper_pool_HGB_native_replay_verification.json' if READY['new_inference_claimed'] else 'verification.json'))")
            needle="        A / 'predict_protected_upper_pool_CPU_HGB_scheme_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        A / 'protected_upper_pool_HGB_CDF_transform_20261007.py',")
        elif old.startswith('optimize_'):
            text=text.replace("'actual_full_pool_CPU_HGB_rank_CDF_comparison_after_complete_parent106_or_explicit_anchor_graph'",
                "'actual_lower_pool_CPU_HGB_CDF_after_complete_qualified_parent'" )
        elif old.startswith('finalize_'):
            start=text.index("    graph = record['winner'][GRAPH_FIELD]")
            end=text.index("    for relative, digest",start)
            text=text[:start]+"""    original = read(record['original_frozen_selection_source'])
    assert record['winner'][GRAPH_FIELD] == original['winner'][GRAPH_FIELD]
    assert record['winner']['metrics'] == original['winner']['metrics']
"""+text[end:]
        elif old.startswith('publish_'):
            needle="        A / 'predict_protected_upper_pool_CPU_HGB_scheme_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        A / 'protected_upper_pool_HGB_CDF_transform_20261007.py',\n        A / 'protected_upper_pool_HGB66_candidate_actual_launch_20261007.json',")
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += (")
            end=text.index('    previous = sync.git',start)
            text=text[:start]+"""    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮登记66项原始完整官方评分：112至114三个合格锚点和63项低分区HGB排序/CDF方案。'
        '父方案在本轮评分前按三者完整官方总分确定，完全同分取最早者。'
        '只在当前非涨停、价格有效、预测可用股票的严格低分子池重排，整个边界并列组保留。'
        '只按完整官方总分选择，不设Top、最差年份或显著性淘汰条件。'
        '已有24个完整HGB模型复用；若产生新方案，实际冻结后完成完整1599600行、原生模型/独立解码、两次重放、CSV及冷80日检查。'
        '若选中已有锚点，则逐位预测、全部8项指标、完整方案和封存字节核对后复用，0新推理。'
        '具体路径和原冻结时间见selected_candidate_ready_for_registration.json。'
        '完整榜六视图与45秒浏览器检查均保留，只main，未读真实测试标签。\\n').encode('utf-8')
"""+text[end:]
        else:
            assert substitute(text,{v:k for k,v in effective.items()})==original,old
        compile(text,str(A/new),'exec');generated[new]=text
    assert len(generated)==8
    return generated


def main():
    ready_path=A/'protected_upper_pool_HGB66_selected_release_20261007/selected_candidate_ready_for_registration.json'
    ready=read(ready_path)
    assert ready['status']=='passed_actual66_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'protected_upper_pool_HGB66_official_comparison_v2_20261007/verification.json')
    parent=pilot['actual_comparison_parent_round'];assert pilot['best']==ready['best'] and len(pilot['records'])==66
    assert read(A/'github_validation_sync_main_20261005/round114_receipt.json')['actual_full_QA_version']==25
    assert read(A/'optimization_20261003_r114/full_registration_execution.json')['status']=='passed'
    candidate=Path(ready['source_candidate']);assert sha(candidate/'manifest.json')==ready['source_manifest_sha256']
    for relative,info in read(candidate/'manifest.json')['files'].items():assert sha(candidate/relative)==info['sha256'],relative
    assert read(candidate/'verification.json')['whole_scheme_graph']==read(candidate/'selection.json')['winner']['conditional_flag_residual_scheme_graph']
    proof_path=A/'protected_upper_pool_HGB66_candidate_source_admission_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual_native_hook_and24_prospective_source_AST_hashes_schema_and_parent_baseline_controls'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(parent)
    # Verify the whole batch before touching any canonical source, unlike old per-file writes.
    for name,text in generated.items():
        assert not (A/name).exists(),name
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name],name
    preparation=A/'protected_upper_pool_HGB66_round115_source_preparation_20261007.json';assert not preparation.exists()
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    pins={str(A/n):sha(A/n) for n in [*NAMES,*NAMES.values(),Path(__file__).name,'run_protected_upper_pool_HGB66_round115_full_registration_20261007.py']}
    pins[str(ready_path)]=sha(ready_path);pins[str(proof_path)]=sha(proof_path)
    create(preparation,{'status':'passed_actual66_sealed_candidate_registry_and_original_QA26_source_routes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'scored_records':66,'round':115,'wave':398,
        'actual_comparison_parent_round':parent,'all_eight_hashes_checked_before_any_canonical_file_written':True,
        'all_original_six_views_full_parameters_sources_and45second_browser_checks_preserved':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
