"""Predeclare eight52-case full registry/QA51 receivers, retaining every parent branch."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_SpectralGram140_complete_receivers_v1_20261008 import adapt
import prepare_HuberCrossFamily112_round139_sources_v1_20261008 as original
NAMES={name:name.replace('HuberCrossFamily112','SpectralGram52').replace('round139','round140').replace('qa50','qa51') for name in original.NAMES.values()}


def source_paths():
    names=[Path(__file__).name,'prepare_SpectralGram140_complete_receivers_v1_20261008.py',
        'SpectralGram140_receiver_drafts_v1_20261008.json','SpectralGram140_receiver_preparation_v1_20261008.json',
        'SpectralGram52_round140_plan_v1_20261008.json','SpectralGram140_storage_v1_20261008.py',
        'SpectralGram64_complete_parent_CDF_v1_20261008.py','SpectralGram64_complete_parent_native_stage_v1_20261008.py',
        'predict_SpectralGram64_complete_parent_scheme_v1_20261008.py','nonflag_SpectralGram64_streamed_v1_20261008.py',
        'run_SpectralGram52_official_comparison_v1_20261008.py','prepare_SpectralGram52_selected_candidate_v1_20261008.py',
        'seal_SpectralGram52_selected_candidate_v1_20261008.py','run_SpectralGram52_round140_full_registration_v1_20261008.py',
        'verify_SpectralGram52_round140_sources_v1_20261008.py','verify_SpectralGram52_prospective_routes_v1_20261008.py',
        'verify_SpectralGram52_prospective_routes_v2_20261008.py','SpectralGram140_prospective_count_reference_recovery_v2_20261008.json',
        'publish_SpectralGram52_evidence_v1_20261008.py','queue_SpectralGram140_complete_pipeline_v1_20261008.py',
        'verify_SpectralGram49_current_parent_v1_20261008.py','verify_SpectralGram140_D_scoring_scope_v1_20261008.py',
        'SpectralGram140_D_scoring_scope_v1_20261008.json','SpectralGram52_prospective_routes_v1_20261008.json',
        'SpectralGram52_actual_controls_index_v1_20261008.json','SpectralGram52_round140_source_admission_v1_20261008.json',
        'SpectralGram52_round140_source_preparation_v1_20261008.json',
        'SpectralGram52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'SpectralGram52_scores_github_v1_20261008/receipt.json',
        'predict_HuberCrossFamily_complete_parent_scheme_v1_20261008.py','HuberCrossFamily_complete_parent_native_stage_v1_20261008.py',
        'HuberCrossFamily_complete_parent_CDF_v1_20261008.py','predict_BF16_reverse_complete_parent_scheme_v1_20261008.py',
        'BF16_reverse_complete_parent_native_stage_v1_20261008.py','BF16_reverse_complete_parent_rank_CDF_v1_20261008.py',
        'predict_HuberIRLS64_complete_parent_scheme_v3_20261008.py','HuberIRLS64_complete_parent_native_stage_v3_20261008.py',
        'predict_CrossFamily_complete_parent_scheme_v2_20261008.py','CrossFamily_complete_parent_native_stage_v2_20261008.py',
        'predict_BF16_complete_parent_rank_scheme_v1_20261008.py','BF16_complete_parent_native_stage_v1_20261008.py',
        'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py','nonflag_residual_ReverseBayes64_native_stage_20261007.py',
        'verify_SpectralGram49_parent134_historical_v1_20261008.py','verify_SpectralGram24_native_historical_hooks_v1_20261008.py',
        'verify_SpectralGram24_native_historical_hooks_v2_20261008.py','SpectralGram140_historical_hook_scope_recovery_v2_20261008.json',
        'verify_SpectralGram_multiyear_native_calendar_v1_20261008.py','SpectralGram140_native_receiver_preflight_v1_20261008.json',
        'verify_SpectralGram20_causal_refit_v1_20261008.py','publish_SpectralGram140_historical_causal_v1_20261008.py',
        'SpectralGram140_historical_causal_main_v1_20261008/receipt.json',
        'prepare_HuberCrossFamily112_round139_sources_v1_20261008.py','prepare_HuberCrossFamily139_complete_receivers_v1_20261008.py',
        'prepare_CrossFamily94_round136_sources_v4_20261008.py','prepare_BF16wide40_round135_sources_v4_20261008.py',
        'exact_native_JSON_archive_runtime_20261007.py','exact_native_pretty_JSON_archive_20261007.py',
        'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',
        'publish_explicit_parent_training_round_v2_20261005.py','all_forecast_percentile_runtime_20261007.py',
        'cached_official_spearman_runtime_20261007.py','resolve_sealed_scientific_protocol_v2_20261007.py']
    return list(dict.fromkeys(A/name for name in [*names,*NAMES.values()]))


def generate(parent):
    assert parent in (137,138,139);outputs={}
    for old_name,old_text in original.generate(136).items():
        name=NAMES[old_name];text=adapt(old_text)
        if name.startswith('register_'):text=text.replace("len(measured['ordered_native_components']) in (2,3)","len(measured['ordered_native_components'])==1")
        if name.startswith('publish_'):
            first=text.index("    payload[(prefix/'README.md').as_posix()] += (");last=text.index('    previous = ',first)
            text=text[:first]+'''    payload[(prefix/'README.md').as_posix()] += ('\\n本轮52项：137、138、139三个完整合格锚点；四种主成分截断维度的正负方向，六种幅度共48项及零幅度恒等对照。'
        '20个自身成熟年度模型，共享各自训练窗口的Gram及特征基底；提供目标、预处理和基底拟合均限制在自身成熟训练窗口。'
        '实际独立稠密SVD、原生重载和完整OOF复核通过；五个成熟窗口及20个后续训练标签扰动原生重新拟合保持逐位一致。'
        '49完整5635800行及147冷前缀，24历史原生及24冷接入，固定2025模型24跨年及48按日检查通过。'
        '新变换保留全部已有分支，位于完整父方案之后。官方S和全部八指标选优；同分按唯一模型SHA、幅度和case排序。'
        '选中新方案完整源、图和映射冻结后两次完整1599600行原生与独立推理、冷80；锚点如实记录零新推理。'
        '完整榜六视图45秒QA51，仅main。未读取实际测试标签；有限网格不证明方向及资源穷尽。\\n').encode('utf8')
''' +text[last:]
        text=substitute(text,{'_r136':f'_r{parent}','round136_receipt.json':f'round{parent}_receipt.json',
            'PREVIOUS_NUMBER = 136':f'PREVIOUS_NUMBER = {parent}',"'explicit_parent_round': 136":f"'explicit_parent_round': {parent}",
            'explicit_comparison_parent_round=136':f'explicit_comparison_parent_round={parent}'})
        compile(text,str(A/name),'exec');outputs[name]=text
    assert len(outputs)==8;return outputs


def main():
    ready_path=A/'SpectralGram52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual52_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'SpectralGram52_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==52 and pilot['best']==ready['best']
    proof_path=A/'SpectralGram52_round140_source_admission_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual20_heads49_current_CDF147cold24hooks_and24_prospective140_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'SpectralGram52_round140_source_preparation_v1_20261008.json',{
        'status':'passed_actual52_sealed_candidate_and_admitted_full140_QA51_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':140,'scored_records':52,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_unique_native_candidates_by_registration':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
