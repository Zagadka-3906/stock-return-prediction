"""Full44 registry, immutable16792-row board, six-view QA85 and main-only publication."""
from pathlib import Path
import sys,io,tokenize,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
NAMES=['register_StockRankDual174_round174_artifacts_v2_20261010.py','publish_StockRankDual174_round174_full_validation_v2_20261010.py','optimize_training_round174.py','finalize_training_round174.py','lossless_ranking_runtime_adapter_round174_v2_20261008.py','build_lossless_ranking_display_round174_v2_20261008.py','verify_lossless_ranking_display_round174_v2_20261008.py','collect_full_lossless_round174_qa85_20261010.py']
EXTRAS=['prepare_StockRankDual174_candidate_and_storage_v1_20261010.py','prepare_StockRankDual174_selected_candidate_v1_20261010.py','seal_StockRankDual174_selected_candidate_v1_20261010.py','stock_rank_dual174_storage_v1_20261010.py','stock_rank_dual174_candidate_sources_preparation_v1_20261010.json','stock_rank_dual44_selected_native_stage_v1_20261010.py','predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py','normalize_stock_rank_and_dual44_after173_v2_20261010.py','stock_rank_dual44_after173_selection_plan_v2_20261010.json','qualify_stock_rank_dual44_selected_native14_v1_20261010.py','stock_rank_dual44_selected14_routes_admission_v1_20261010.json','stock_dual_embedding_after_complete_parent_native_stage_v1_20261010.py','stock_dual_embedding_five_parent_hooks_CPU_controls_v1_20261010.json','stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','predict_stock_rank_embedding_complete_qualified_parent_scheme_v1_20261010.py','stock_rank_embedding_actual_five_parent_hooks_CPU_controls_v1_20261010.json','actual_stock_dual_embedding_actual36_native_location_v1_20261010.json','stock_rank_embedding17_after170_completion_main_receipt_v55_20261010.json','stock_rank_embedding_small512_BF16_native_v1_20261010.py','stock_rank_embedding_saved_tensor_decoder_v1_20261010.py']
def source_paths():
    from prepare_stock_embedding173_full_registry_sources_v2_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def route(text):
    from prepare_StockRankDual174_candidate_and_storage_v1_20261010 import route as scientific_route
    text=scientific_route(text)
    pairs={'prepare_stock_embedding173_full_registry_sources_v2_20261010':'prepare_stock_rank_dual174_full_registry_sources_v1_20261010','stock_embedding_complete36_after172_selection_plan_v1_20261010':'stock_rank_dual44_after173_selection_plan_v2_20261010','round173':'round174','_r173':'_r174','_r172':'_r173','qa84':'qa85','QA84':'QA85','qa_v84':'qa_v85','wave456':'wave457','stock_embedding_after170':'stock_rank_embedding_after170','stock_embedding_after172':'stock_dual_embedding_after173','qualified172':'qualified173','number == 173':'number == 174'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)),lambda m:pairs[m.group()],text)
    return tokenize.untokenize([t._replace(string={'173':'174','172':'173','36':'44','84':'85','456':'457'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
def main():
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from prepare_stock_embedding173_full_registry_sources_v2_20261010 import NAMES as oldnames
    assert allowed();inputs=[];outputs=[]
    for oldname,newname in zip(oldnames,NAMES):
        source=A/oldname;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        if newname==NAMES[0]:
            text=text.replace("len(measured['ordered_native_components'])==1","len(measured['ordered_native_components']) in (1,2)")
            text=text.replace("'existing_own_stock_embedding_native_bank_fits': 6","'existing_own_return_and_rank_embedding_native_bank_fits': 12")
        if newname==NAMES[1]:
            text=text.replace("tuple(f['name']+'_screen_v1_20261010' for f in read", "tuple(f['folder'] for f in read")
            lines=text.splitlines();found=[i for i,l in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in l];assert len(found)==1
            lines[found[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第174轮：排名嵌入17项与收益排名互补集成25项TRAIN官方评分，加完全合格170和173锚点共44条；40项完整Pandas独立控制和120个因果前缀。最高S优先，再按真实物理模型数比较。选中单排名或双模型参数14项原生、14项冷启动、7项拟合前拒绝检查，实际保存状态分别6或12。完整冻结后执行两次1599600行推理和cold80，物理模型按SHA去重；合格锚点可如实复用。完整榜16792条，六视图QA85及GitHub main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        dest=A/newname;assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n');outputs.append(dest)
    for p in source_paths():assert p.exists(),p
    create(A/'stock_rank_dual174_full_registry_sources_preparation_v1_20261010.json',{'status':'compiled8_actual44_registry_QA85_main_sources_selected_full_inference_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':44,'expected_full_board':16792,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'prepared_sources':8,'actual_full174_dispatch':False,'QA':85},flush=True)
if __name__=='__main__':main()
