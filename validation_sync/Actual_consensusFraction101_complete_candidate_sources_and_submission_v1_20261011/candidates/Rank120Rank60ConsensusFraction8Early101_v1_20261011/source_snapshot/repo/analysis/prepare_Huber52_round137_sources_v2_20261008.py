"""Generate eight complete52-case registry/QA48 receivers without changing ancestor source bytes."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_Huber137_complete_receivers_v2_20261008 import adapt
import prepare_CrossFamily94_round136_sources_v2_20261008 as original
NAMES={name:name.replace('CrossFamily94','Huber52').replace('round136','round137').replace('qa47','qa48') for name in original.NAMES.values()}


def source_paths():
    names=[Path(__file__).name,'recover_multiyear_136137_queues_v1_20261008.py','multiyear136137_queue_recovery_v1_20261008.json','verify_multiyear_residual_native_calendar_v1_20261008.py','multiyear_residual_native_preparation_v1_20261008.json','actual_multiyear_residual_calendar_location_v1_20261008.json','prepare_Huber137_complete_receivers_v1_20261008.py','Huber137_receiver_drafts_v1_20261008.json',
        'Huber137_receiver_preparation_v2_20261008.json','Huber52_round137_receiver_contract_v1_20261008.json',
        'HuberIRLS64_52_round137_plan_v2_20261008.json','HuberIRLS64_bounded_plan_recheck_v2_20261008.json',
        'Huber137_storage_v1_20261008.py','Huber52_complete_parent_receiver_codec_v1_20261008.py',
        'HuberIRLS64_complete_parent_CDF_v1_20261008.py','HuberIRLS64_complete_parent_native_stage_v3_20261008.py',
        'predict_HuberIRLS64_complete_parent_scheme_v3_20261008.py','nonflag_HuberIRLS64_streamed_v1_20261008.py',
        'nonflag_HuberIRLS64_own_window_v1_20261008.py','prepare_Huber52_receiver_contract_v1_20261008.py',
        'run_Huber52_official_comparison_v2_20261008.py','prepare_Huber52_selected_candidate_v2_20261008.py',
        'seal_Huber52_selected_candidate_v2_20261008.py','verify_Huber52_round137_sources_v2_20261008.py',
        'verify_Huber52_prospective_routes_v2_20261008.py','run_Huber52_round137_full_registration_v2_20261008.py',
        'publish_Huber52_evidence_v2_20261008.py','queue_Huber137_complete_pipeline_v2_20261008.py',
        'verify_HuberIRLS64_49_current_parent_v3_20261008.py','verify_Huber137_D_scoring_scope_v1_20261008.py',
        'Huber137_D_scoring_scope_v1_20261008.json','Huber52_prospective_routes_v2_20261008.json',
        'Huber52_actual_controls_index_v2_20261008.json','Huber52_round137_source_admission_v2_20261008.json',
        'Huber52_round137_source_preparation_v2_20261008.json',
        'Huber52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json','Huber52_scores_github_v1_20261008/receipt.json',
        'prepare_CrossFamily94_round136_sources_v3_20261008.py','prepare_BF16wide40_round135_sources_v4_20261008.py',
        'exact_native_JSON_archive_runtime_20261007.py','exact_native_pretty_JSON_archive_20261007.py',
        'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',
        'publish_explicit_parent_training_round_v2_20261005.py','all_forecast_percentile_runtime_20261007.py',
        'cached_official_spearman_runtime_20261007.py','resolve_sealed_scientific_protocol_v2_20261007.py',
        'HuberIRLS64_historical_controls_main_v2_20261008/receipt.json','HuberIRLS64_causal_handoff_main_v3_20261008/receipt.json']
    return list(dict.fromkeys(A/name for name in [*names,*NAMES.values()]))


def generate(parent):
    assert parent in (134,135,136)
    outputs={}
    for old_name,old_text in original.generate(112).items():
        name=NAMES[old_name];text=adapt(old_text)
        if name.startswith('register_'):
            text=text.replace("len(measured['ordered_native_components']) in (2,4)","len(measured['ordered_native_components']) in (1,2)")
            text=text.replace("'existing_CrossFamily_saved_native_heads': 30","'existing_Huber_saved_native_heads': 10")
            text=text.replace("'actual30_CrossFamily_saved_native_heads_source'","'actual10_Huber_saved_native_heads_source'")
        if name.startswith('publish_'):
            start=text.index("    payload[(prefix/'README.md').as_posix()] += (");end=text.index('    previous = ',start)
            text=text[:start]+'''    payload[(prefix/'README.md').as_posix()] += ('\\n本轮52项：134、135、136合格锚点；两种固定Huber残差及其等权均值，各有正负方向，八种幅度共48项，另有零幅度恒等对照。'
        '两个残差头共10个成熟年度模型，使用相同自身成熟64维特征与提供的训练目标；实际保存、重载、独立JSON解码和冷前缀一致。'
        '五个独立标签成熟窗口、10项后续训练标签扰动检查通过；48个新增变换接在完整父方案全部原有分支之后，包括已有BF16和跨模型分支。'
        '49项完整5635800行与147冷前缀、18历史原生接入；52项原始官方连续八指标选优。'
        '选中方案冻结后两次完整1599600行原生与独立推理、冷80；锚点复用如实记录零新推理。'
        '完整榜原始六视图45秒QA48，仅main。没有实际测试标签；选模偏差未校正；有限网格不证明方向或资源穷尽。\\n').encode('utf8')
''' +text[end:]
        text=substitute(text,{'_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json',
            'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',"'explicit_parent_round': 112":f"'explicit_parent_round': {parent}",
            'explicit_comparison_parent_round=112':f'explicit_comparison_parent_round={parent}'})
        assert 'prepare_Huber52_round137_sources_v2_20261008' in text or not name.startswith(('register_','publish_'))
        compile(text,str(A/name),'exec');outputs[name]=text
    assert len(outputs)==8
    return outputs


def main():
    ready_path=A/'Huber52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual52_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'Huber52_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==52 and pilot['best']==ready['best']
    proof_path=A/'Huber52_round137_source_admission_v2_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual10_heads49_current_CDF147cold18hooks_and24_prospective137_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'Huber52_round137_source_preparation_v2_20261008.json',{'status':'passed_actual52_sealed_candidate_and_admitted_full137_QA48_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':137,'scored_records':52,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(path):sha(path) for path in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
