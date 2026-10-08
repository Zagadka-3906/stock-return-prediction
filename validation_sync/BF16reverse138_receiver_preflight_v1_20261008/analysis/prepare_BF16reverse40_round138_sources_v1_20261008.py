"""Predeclare eight full reverse40 registration/QA49 sources, preserving all qualified parent stages."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_BF16reverse138_complete_receivers_v1_20261008 import adapt
import prepare_BF16wide40_round135_sources_v4_20261008 as original
NAMES={name:name.replace('BF16wide40','BF16reverse40').replace('round135','round138').replace('qa46','qa49') for name in original.NAMES.values()}


def source_paths():
    names=[Path(__file__).name,'prepare_BF16reverse138_complete_receivers_v1_20261008.py','BF16reverse138_receiver_drafts_v1_20261008.json',
        'BF16reverse138_receiver_preparation_v1_20261008.json','BF16reverse40_round138_plan_v1_20261008.json',
        'BF16reverse138_storage_v1_20261008.py','BF16reverse138_D_scoring_scope_v1_20261008.json',
        'verify_BF16reverse138_D_scoring_scope_v1_20261008.py','BF16_reverse_complete_parent_rank_CDF_v1_20261008.py',
        'BF16_reverse_complete_parent_native_stage_v1_20261008.py','predict_BF16_reverse_complete_parent_scheme_v1_20261008.py',
        'BF16_reverse_native_receiver_preparation_v1_20261008.json','BF16_reverse_rank_CDF_synthetic_preflight_v1_20261008/verification.json',
        'prepare_BF16reverse40_round138_plan_and_controls_v1_20261008.py','prepare_BF16_reverse_native_receiver_v1_20261008.py',
        'prepare_BF16_reverse_historical_hooks_v1_20261008.py','verify_BF16_reverse_rank_CDF_full37_v1_20261008.py',
        'verify_BF16_reverse_complete_parent_native_hook3_v1_20261008.py','run_BF16reverse40_official_comparison_v1_20261008.py',
        'prepare_BF16reverse40_selected_candidate_v1_20261008.py','seal_BF16reverse40_selected_candidate_v1_20261008.py',
        'verify_BF16reverse40_round138_sources_v1_20261008.py','verify_BF16reverse40_prospective_routes_v1_20261008.py',
        'run_BF16reverse40_round138_full_registration_v1_20261008.py','publish_BF16reverse40_evidence_v1_20261008.py',
        'queue_BF16reverse138_complete_pipeline_v1_20261008.py','BF16reverse40_prospective_routes_v1_20261008.json',
        'BF16reverse40_actual_controls_index_v1_20261008.json','BF16reverse40_round138_source_admission_v1_20261008.json',
        'BF16reverse40_round138_source_preparation_v1_20261008.json',
        'BF16reverse40_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'BF16reverse40_scores_github_v1_20261008/receipt.json','reverse_BF16_plan_handoff_main_v1_20261008/receipt.json',
        'prepare_BF16wide40_round135_sources_v4_20261008.py','prepare_nonflag_ReverseBayesFine40_round134_sources_v3_20261008.py',
        'neural_BF16_independent_forward_v1_20261008.py','neural_BF16_micro8192_native_v1_20261008.py',
        'predict_HuberIRLS64_complete_parent_scheme_v3_20261008.py','HuberIRLS64_complete_parent_native_stage_v3_20261008.py',
        'predict_CrossFamily_complete_parent_scheme_v2_20261008.py','CrossFamily_complete_parent_native_stage_v2_20261008.py',
        'predict_BF16_complete_parent_rank_scheme_v1_20261008.py','BF16_complete_parent_native_stage_v1_20261008.py',
        'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py',
        'exact_native_JSON_archive_runtime_20261007.py','exact_native_pretty_JSON_archive_20261007.py',
        'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',
        'publish_explicit_parent_training_round_v2_20261005.py','all_forecast_percentile_runtime_20261007.py',
        'cached_official_spearman_runtime_20261007.py','resolve_sealed_scientific_protocol_v2_20261007.py']
    return list(dict.fromkeys(A/name for name in [*names,*NAMES.values()]))


def generate(parent):
    assert parent in (135,136,137);outputs={}
    for old_name,old_text in original.generate(112).items():
        name=NAMES[old_name];text=adapt(old_text)
        if name.startswith('register_'):
            needle="'first2020_active':True,'position':'after_complete_qualified_parent',";assert text.count(needle)==1
            text=text.replace(needle,"'first2020_active':True,'position':'after_complete_qualified_parent','signal_sign_on_valid_rows':-1.,'invalid_signal_bits_preserved':True,")
            before="records.sort(key=lambda r: (-r['connected_final_score'], r['direct_rank_comparison_configuration']['weight'], r['original_comparison_case']))"
            after="records.sort(key=lambda r: (-r['connected_final_score'], r['actual_full_conditional_residual_control']['expected_unique_native_models'], r['direct_rank_comparison_configuration']['weight'], r['original_comparison_case']))"
            assert text.count(before)==1;text=text.replace(before,after)
        if name.startswith('publish_'):
            text=text.replace('112、133、134合格锚点','135、136、137合格锚点').replace('各12神经网络融合权重','各12负向神经预测融合权重')
            text=text.replace('完整父方案所有分支保留','完整父方案的正向神经、跨模型、Huber和其他已有分支全部保留')
            text=text.replace('2020参与新融合。','2020参与新融合；只反转有效预测，无效标记原始位不变；按模型SHA去重计数。')
        text=text.replace('neural_day_average_rank_over_N','valid_reversed_neural_day_average_rank_over_N')
        text=substitute(text,{'_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json',
            'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',"'explicit_parent_round': 112":f"'explicit_parent_round': {parent}",
            'explicit_comparison_parent_round=112':f'explicit_comparison_parent_round={parent}'})
        compile(text,str(A/name),'exec');outputs[name]=text
    assert len(outputs)==8;return outputs


def main():
    ready_path=A/'BF16reverse40_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'BF16reverse40_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==40 and pilot['best']==ready['best']
    proof_path=A/'BF16reverse40_round138_source_admission_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual6_full5GPU37CDF111cold3hooks_and24_prospective138_sources'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'BF16reverse40_round138_source_preparation_v1_20261008.json',{'status':'passed_actual40_sealed_candidate_and_admitted_full138_QA49_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':138,'scored_records':40,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
