"""Full47 registry, immutable16839-record board, QA86 and actual main publication."""
from pathlib import Path
import sys,io,tokenize,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
NAMES=['register_StockTop10Embedding175_round175_artifacts_v2_20261010.py','publish_StockTop10Embedding175_round175_full_validation_v2_20261010.py','optimize_training_round175.py','finalize_training_round175.py','lossless_ranking_runtime_adapter_round175_v2_20261008.py','build_lossless_ranking_display_round175_v2_20261008.py','verify_lossless_ranking_display_round175_v2_20261008.py','collect_full_lossless_round175_qa86_20261010.py']
EXTRAS=['prepare_Top10_complete47_selection_and_candidate_sources_v1_20261010.py','admit_exact_Top10_47_service_routes_v2_20261010.py','prepare_StockTop10Embedding175_selected_candidate_v2_20261010.py','seal_StockTop10Embedding175_selected_candidate_v1_20261010.py','stock_top10_embedding175_storage_v1_20261010.py','stock_top10_embedding175_candidate_sources_preparation_v2_20261010.json','stock_top10_embedding_after_complete_qualified_parent_native_stage_v2_20261010.py','predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010.py','stock_top10_actual_six_parent_callback_CPU_controls_v1_20261010.json','stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json','normalize_completed_stock_top10_embedding47_after174_v2_20261010.py','qualify_stock_top10_embedding47_selected_native14_v2_20261010.py','stock_top10_embedding_complete47_after174_selection_plan_v1_20261010.json','stock_top10_embedding_small512_BF16_native_v2_20261010.py','stock_identity_embedding_network_v1_20261010.py','stock_top10_embedding_saved_tensor_decoder_v1_20261010.py','train_stock_top10_embedding_small512_BF16_bank6_memory_guard_v3_20261010.py','verify_stock_top10_embedding_small512_full5_independent_v2_20261010.py','verify_stock_top10_embedding_six_state_native42_v2_20261010.py','run_stock_top10_embedding_after174_fast17_screen_v1_20261010.py','run_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010.py']
def source_paths():
    from prepare_stock_rank_dual174_full_registry_sources_v1_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def route(text):
    from prepare_Top10_complete47_selection_and_candidate_sources_v1_20261010 import route as science
    text=science(text)
    mapping={'round173':'round175','_r173':'_r175','_r172':'_r174','qa84':'qa86','QA84':'QA86','qa_v84':'qa_v86','wave456':'wave458','qualify_stock_top10_embedding47_selected_native14_v1_20261010':'qualify_stock_top10_embedding47_selected_native14_v2_20261010','StockTop10Embedding47_selected_native14_v1_20261010':'StockTop10Embedding47_selected_native14_v2_20261010','prepare_StockTop10Embedding175_selected_candidate_v1_20261010':'prepare_StockTop10Embedding175_selected_candidate_v2_20261010','stock_top10_embedding175_candidate_sources_preparation_v1_20261010':'stock_top10_embedding175_candidate_sources_preparation_v2_20261010','actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010':'actual_stock_top10_embedding_own_training_queue_v3_20261010','actual_stock_embedding_six_state_native42_v2_20261010':'actual_stock_top10_embedding_six_state_native42_v1_20261010','Frontier133172_complete133_family_v2_20261010':'StockRankDual174_complete44_family_v2_20261010','run_StockTop10Embedding175_complete_family_v3_20261010':'run_StockTop10Embedding175_complete_family_v1_20261010','run_StockTop10Embedding175_full_registration_v3_20261010':'run_StockTop10Embedding175_full_registration_v1_20261010','verify_StockTop10Embedding175_full36_preflight_v3_20261010':'verify_StockTop10Embedding175_full47_preflight_v1_20261010','stock_top10_embedding175_full_family_preflight_v3_20261010':'stock_top10_embedding175_full_family_preflight_v1_20261010'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=tokenize.untokenize([t._replace(string={'173':'175','172':'174','36':'47','84':'86','456':'458','32':'44','96':'132'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    text=text.replace('in (170,174)','in (174,)')
    return text
def main():
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from prepare_stock_embedding173_full_registry_sources_v2_20261010 import NAMES as oldnames
    assert allowed();inputs=[];outputs=[]
    for old,new in zip(oldnames,NAMES):
        source=A/old;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        if new==NAMES[0]:text=text.replace("'existing_own_stock_embedding_native_bank_fits': 6","'existing_own_stock_Top10_BCE_native_bank_fits': 6").replace("['stock_embedding_after170','stock_embedding_after172','qualified170','qualified172']","['classifier_tiny_and_protected17','classifier_large_allocation29','qualified174']")
        if new==NAMES[1]:
            lines=text.splitlines();matches=[i for i,line in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in line];assert len(matches)==1
            lines[matches[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第175轮：独立Top10分类BCE正类权重9网络，17项小权重和尾部保护、29项大权重及全有效股票融合，加第174轮完整合格基线共47条TRAIN官方记录。44项完整Pandas控制、132个因果前缀；最高官方S优先，物理模型SHA去重；选中方案六状态14原生、14冷启动、7拟合前拒绝检查。冻结后两次1599600行完整推理和cold80，或如实复用合格基线。完整榜16839条、六视图QA86和GitHub main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        target=A/new;assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    # Exact literal inventories must be available before future dispatch.
    for p in source_paths():assert p.exists(),p
    create(A/'stock_top10_embedding175_full_registry_sources_preparation_v2_20261010.json',{'status':'compiled8_exact47_full_registry_QA86_main_sources_actual_selected_inference_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':47,'expected_full_board':16839,'new_quality_scores':0,'test_labels_read':False})
    sources=[('run_StockEmbedding173_complete_family_v3_20261010.py','run_StockTop10Embedding175_complete_family_v1_20261010.py'),('run_StockEmbedding173_full_registration_v3_20261010.py','run_StockTop10Embedding175_full_registration_v1_20261010.py'),('verify_StockEmbedding173_full36_preflight_v3_20261010.py','verify_StockTop10Embedding175_full47_preflight_v1_20261010.py')]
    for old,new in sources:
        source=A/old;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        text=text.replace('passed_complete133_actual_capsules','passed_complete47_actual_capsules')
        if new.startswith('run_StockTop10Embedding175_full_registration'):
            text=text.replace("publish(175,'一日收益与因果平滑共133项完整验证','conditional_flag_residual_causal_checks.json',['已实际完成81项一日收益和49项因果平滑，加169/170/171合格锚点，共133条；连续官方S优先'])","publish(175,'Top10分类共47项完整验证','conditional_flag_residual_causal_checks.json',['实际17项原筛选、29项大权重融合和第174轮合格基线；连续官方S优先'])")
        p=A/new;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p)
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    assignments=literal_assignments(A/'optimize_training_round175.py');assert (assignments['NUMBER'],assignments['PREVIOUS_NUMBER'],assignments['WAVES'])==(175,174,(458,))
    create(A/'stock_top10_embedding175_full_execution_sources_admission_v1_20261010.json',{'status':'compiled_actual47_family_candidate2_full_registry_QA86_main_pipeline_before_future_dispatch','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':47,'expected_full_board':16839,'new_quality_scores':0,'actual_future_dispatch_not_started':True,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    p=A/'run_StockTop10Embedding175_complete_family_v1_20261010.py';row=start_service('StockTop10Embedding175_complete47_family_v1_20261010',p.name,[],{str(p):sha(p)})
    create(A/'actual_StockTop10Embedding175_complete47_family_activation_v1_20261010.json',row)
    print({'actual_full175_queue_started':True,'records':47,'board':16839,'QA':86},flush=True)
if __name__=='__main__':main()
