"""Predeclare eight112-case registry and QA50 sources for every eligible full parent."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_HuberCrossFamily139_complete_receivers_v1_20261008 import adapt
import prepare_CrossFamily94_round136_sources_v4_20261008 as original
NAMES={name:name.replace('CrossFamily94','HuberCrossFamily112').replace('round136','round139').replace('qa47','qa50') for name in original.NAMES.values()}


def source_paths():
    names=[Path(__file__).name,'prepare_HuberCrossFamily139_complete_receivers_v1_20261008.py',
        'HuberCrossFamily139_receiver_drafts_v1_20261008.json','HuberCrossFamily139_receiver_preparation_v1_20261008.json',
        'HuberCrossFamily112_round139_plan_v1_20261008.json','HuberCrossFamily139_storage_v1_20261008.py',
        'HuberCrossFamily_complete_parent_CDF_v1_20261008.py','HuberCrossFamily_complete_parent_native_stage_v1_20261008.py',
        'predict_HuberCrossFamily_complete_parent_scheme_v1_20261008.py',
        'run_HuberCrossFamily112_official_comparison_v1_20261008.py','prepare_HuberCrossFamily112_selected_candidate_v1_20261008.py',
        'seal_HuberCrossFamily112_selected_candidate_v1_20261008.py','run_HuberCrossFamily112_round139_full_registration_v1_20261008.py',
        'verify_HuberCrossFamily112_round139_sources_v1_20261008.py','verify_HuberCrossFamily112_prospective_routes_v1_20261008.py',
        'publish_HuberCrossFamily112_evidence_v1_20261008.py','queue_HuberCrossFamily139_complete_pipeline_v1_20261008.py',
        'verify_HuberCrossFamily109_current_parent_v1_20261008.py','verify_HuberCrossFamily139_D_scoring_scope_v1_20261008.py',
        'HuberCrossFamily139_D_scoring_scope_v1_20261008.json','HuberCrossFamily112_prospective_routes_v1_20261008.json',
        'HuberCrossFamily112_actual_controls_index_v1_20261008.json','HuberCrossFamily112_round139_source_admission_v1_20261008.json',
        'HuberCrossFamily112_round139_source_preparation_v1_20261008.json',
        'HuberCrossFamily112_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'HuberCrossFamily112_scores_github_v1_20261008/receipt.json',
        'predict_BF16_reverse_complete_parent_scheme_v1_20261008.py','BF16_reverse_complete_parent_native_stage_v1_20261008.py',
        'BF16_reverse_complete_parent_rank_CDF_v1_20261008.py','predict_HuberIRLS64_complete_parent_scheme_v3_20261008.py',
        'HuberIRLS64_complete_parent_native_stage_v3_20261008.py','predict_CrossFamily_complete_parent_scheme_v2_20261008.py',
        'CrossFamily_complete_parent_native_stage_v2_20261008.py','predict_BF16_complete_parent_rank_scheme_v1_20261008.py',
        'BF16_complete_parent_native_stage_v1_20261008.py','predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py',
        'nonflag_residual_ReverseBayes64_native_stage_20261007.py','nonflag_HuberIRLS64_streamed_v1_20261008.py',
        'verify_HuberCrossFamily109_parent134_historical_v1_20261008.py','verify_HuberCrossFamily18_native_historical_hooks_v1_20261008.py',
        'verify_HuberCrossFamily_multiyear_native_calendar_v1_20261008.py','HuberCrossFamily139_native_receiver_preflight_v1_20261008.json',
        'publish_HuberCrossFamily139_preliminary_v1_20261008.py','HuberCrossFamily139_preliminary_historical_main_v1_20261008/receipt.json',
        'prepare_CrossFamily94_round136_sources_v4_20261008.py','prepare_BF16wide40_round135_sources_v4_20261008.py',
        'exact_native_JSON_archive_runtime_20261007.py','exact_native_pretty_JSON_archive_20261007.py',
        'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',
        'publish_explicit_parent_training_round_v2_20261005.py','all_forecast_percentile_runtime_20261007.py',
        'cached_official_spearman_runtime_20261007.py','resolve_sealed_scientific_protocol_v2_20261007.py']
    return list(dict.fromkeys(A/name for name in [*names,*NAMES.values()]))


def generate(parent):
    assert parent in (136,137,138)
    outputs={}
    for old_name,old_text in original.generate(112).items():
        name=NAMES[old_name];text=adapt(old_text)
        if name.startswith('register_'):
            text=text.replace("len(measured['ordered_native_components']) in (2,4)","len(measured['ordered_native_components']) in (2,3)")
        if name.startswith('publish_'):
            first=text.index("    payload[(prefix/'README.md').as_posix()] += (");last=text.index('    previous = ',first)
            text=text[:first]+'''    payload[(prefix/'README.md').as_posix()] += ('\\n本轮112项：136、137、138三个完整合格锚点，六类Huber与Ridge、RFF、贝叶斯组合，三种比例和六种幅度共108项及零幅度对照。'
        '复用五个残差头的25个成熟年度模型；五个年度共同样本窗口、64维特征和提供目标数值SHA相等。'
        '109个完整5635800行与327冷前缀检查、18个历史原生接入及18冷前缀；固定2025模型18跨年日历及36按日检查。'
        '新变换位于完整父方案全部原有分支之后，保留正反神经、Cross和Huber；2020、涨停和无效行保持原始位。'
        '按原始官方S及全部八指标选优，同分按物理模型SHA并集计数、幅度和case排序。'
        '选中新方案全图、映射和Python源冻结后两次完整1599600行原生及独立推理、冷80；锚点如实记录零新推理。'
        '全部完整榜六视图45秒QA50，仅main；未读取实际测试标签。有限网格不证明优化或资源穷尽。\\n').encode('utf8')
''' +text[last:]
        text=substitute(text,{'_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json',
            'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',"'explicit_parent_round': 112":f"'explicit_parent_round': {parent}",
            'explicit_comparison_parent_round=112':f'explicit_comparison_parent_round={parent}'})
        compile(text,str(A/name),'exec');outputs[name]=text
    assert len(outputs)==8
    return outputs


def main():
    ready_path=A/'HuberCrossFamily112_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual112_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'HuberCrossFamily112_official_comparison_v1_20261008/verification.json')
    assert len(pilot['records'])==112 and pilot['best']==ready['best']
    proof_path=A/'HuberCrossFamily112_round139_source_admission_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual25_heads109_current_CDF327cold18hooks_and24_prospective139_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'HuberCrossFamily112_round139_source_preparation_v1_20261008.json',{
        'status':'passed_actual112_sealed_candidate_and_admitted_full139_QA50_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':139,'scored_records':112,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(path):sha(path) for path in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
