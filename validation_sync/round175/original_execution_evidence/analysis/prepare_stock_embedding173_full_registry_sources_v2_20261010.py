"""Actual36-score round173 registry/QA84 inventory with explicit original172 source lineage."""
from pathlib import Path
import io,tokenize,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
NAMES=['register_StockEmbedding173_round173_artifacts_v2_20261010.py','publish_StockEmbedding173_round173_full_validation_v2_20261010.py','optimize_training_round173.py','finalize_training_round173.py','lossless_ranking_runtime_adapter_round173_v2_20261008.py','build_lossless_ranking_display_round173_v2_20261008.py','verify_lossless_ranking_display_round173_v2_20261008.py','collect_full_lossless_round173_qa84_20261010.py']
EXTRAS=['prepare_StockEmbedding173_candidate_and_storage_v1_20261010.py','prepare_StockEmbedding173_selected_candidate_v1_20261010.py','seal_StockEmbedding173_selected_candidate_v1_20261010.py','stock_embedding173_storage_v1_20261010.py','stock_embedding173_candidate_sources_preparation_v1_20261010.json','stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py','stock_embedding_native_stage_and_four_parent_routes_admission_v1_20261010.json','stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json','normalize_completed_stock_embedding36_after172_v1_20261010.py','qualify_stock_embedding36_selected_native14_v1_20261010.py','stock_embedding_complete36_after172_selection_plan_v1_20261010.json','stock_embedding_complete36_and_selected14_sources_admission_v1_20261010.json','stock_embedding_small512_BF16_native_v1_20261010.py','stock_identity_embedding_network_v1_20261010.py','stock_embedding_saved_tensor_decoder_v1_20261010.py','train_stock_embedding_small512_BF16_bank6_checkpoint_yield_v5_20261010.py','verify_stock_embedding_small512_full5_independent_v3_20261010.py','verify_stock_embedding_six_state_native42_v2_20261010.py','actual_stock_embedding_six_state_native42_location_v1_20261010.json','stock_embedding_actual_six_state_native42_completion_main_receipt_v50_20261010.json','stock_embedding_score_original_fixture169_and_actual170172_baseline_route_recovery_v2_20261010.json']
def source_paths():
    from prepare_frontier133172_full_registry_sources_v2_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def route(text):
    from prepare_StockEmbedding173_candidate_and_storage_v1_20261010 import route as scientific_routes
    text=scientific_routes(text)
    pairs={'round172':'round173','_r172':'_r173','_r171':'_r172','第172轮':'第173轮','qa83':'qa84','QA83':'QA84','qa_v83':'qa_v84','Frontier133_selected_native14_v1_20261010':'StockEmbedding36_selected_native14_v1_20261010','frontier133_after171_predeclared_training_only_selection_plan_v1_20261010':'stock_embedding_complete36_after172_selection_plan_v1_20261010','prepare_stock_embedding173_full_registry_sources_v2_20261010':'prepare_stock_embedding173_full_registry_sources_v2_20261010'}
    saved={}
    for i,(old,new) in enumerate(sorted(pairs.items(),key=lambda pair:-len(pair[0]))):
        token=f'__STOCK173_ROUTE_{i}__';text=text.replace(old,token);saved[token]=new
    for token,new in saved.items():text=text.replace(token,new)
    text=tokenize.untokenize([t._replace(string={'172':'173','171':'172','133':'36','83':'84','455':'456'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    text=text.replace('wave455_results','wave456_results').replace('wave455','wave456')
    return text
def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_frontier133172_full_registry_sources_v2_20261010 import NAMES as oldnames
    assert allowed();inputs=[];outputs=[]
    for oldname,newname in zip(oldnames,NAMES):
        source=A/oldname;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        if newname==NAMES[0]:
            assert "'existing_own120_native_bank_fits': 18" in text
            text=text.replace("'existing_own120_native_bank_fits': 18","'existing_own_stock_embedding_native_bank_fits': 6")
            text=text.replace("['cross120_return1d_direct','cross120_mean5_causal_smoothing','cross120_rank5_causal_smoothing','qualified169','qualified170','qualified171']","['stock_embedding_after170','stock_embedding_after172','qualified170','qualified172']")
        if newname==NAMES[1]:
            lines=text.splitlines();found=[i for i,line in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in line];assert len(found)==1
            lines[found[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第173轮：新股票嵌入网络在完整170和172方案上分别17项TRAIN官方评分，加两个完整合格锚点共36条；32项全量Pandas独立控制和96个因果前缀。选择最高S并按真实模型SHA去重，选中参数六状态14项原生、14项冷启动及7项拟合前拒绝检查后冻结；新方案需两次1599600行完整推理和cold80，锚点如实复用已合格候选。六视图QA84及GitHub main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        target=A/newname;assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    for p in source_paths():assert p.exists(),p
    create(A/'stock_embedding173_full_registry_sources_preparation_v2_20261010.json',{'status':'compiled8_fresh36_registry_QA84_and_main_sources_pending_actual_selected36_full_inference','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':36,'expected_full_board':16748,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'prepared_sources':len(outputs),'records':36,'QA':84,'actual_future_dispatch':False},flush=True)
if __name__=='__main__':main()
