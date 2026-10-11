"""Complete61 complementary TRAIN records plus qualified174/181 anchors; QA93 source freeze."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010 as previous
ACTUAL_PARENT='StockRankWide32Embedding181_complete48_family_v7_20261010_resolved_unused'

def route(text):
    actual=read(A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json')['service_aliases']['StockRankWide32Embedding181_complete48_family_v7_20261010']
    mapping={'StockForward20Embedding179_complete48_family_v6_after_Dual25_recovery_v1_20261010':actual,'prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010':Path(__file__).stem,'stock_rank20_embedding180':'stock_rank20_embedding182','StockRank20Embedding180':'StockRank20Embedding182','stock_rank20_embedding48':'stock_rank20_embedding63','StockRank20Embedding48':'StockRank20Embedding63','stock_rank20_embedding_complete48':'stock_rank20_embedding_complete63','StockRank20Embedding180_full48':'StockRank20Embedding182_full63','complete48':'complete63','full48':'full63','pilot48':'pilot63','anchor48':'anchor63','candidate_full48':'candidate_full63','180':'182','179':'181','173':'174','qa91':'qa93','QA91':'QA93','qa_v91':'qa_v93','17062':'17173','463':'465'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    # Standalone counts are this family's scope, never model dimensions or dates.
    for old,new in [(48,63),(44,60),(132,180),(91,93)]:text=re.sub(r'\b'+str(old)+r'\b',str(new),text)
    return text
NAMES=[route(n) for n in previous.NAMES]
EXTRAS=[route(n) for n in previous.EXTRAS[:12]]+previous.EXTRAS[12:]
EXTRAS += ['rank20_after174_complement61_predeclared_plan_v1_20261010.json','run_stock_rank20_embedding_after174_complement61_screen_v1_20261010.py','Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json','route_verified_Dual25_recovery_dependencies_v6_20261010.py','terminal_routes6_candidate_aliases_and_recipe32_actual_CPU_v1_20261010.json']
def source_paths():
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*previous.source_paths()]))
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();inputs=[];outputs=[]
    plan={'status':'predeclared63_rank20_complement61_plus_qualified174181_anchors_before_any_futureX','expected_records':63,'fully_qualified_anchors':[174,181],'families':[{'name':'StockRank20EmbeddingSmall512_after174_high_impact61','base_round':174,'records':61,'stage_kind':'stock_rank20_embedding_rank20mean_direct','actual_service':'actual_stock_rank20_embedding_after174_complement61_screen_v1_20261010','main_receipt':'Rank20_after174_complement61_actual61_v1_20261010_main_receipt.json'}],'expected_full_controls':60,'expected_prefix_controls':180,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','future_X_read_for_selection':False,'test_labels_read':False}
    planpath=A/'stock_rank20_embedding_complete63_after181_selection_plan_v1_20261010.json';create(planpath,plan)
    selected=[n for n in previous.EXTRAS[:9] if n.endswith('.py')]
    for old in [*previous.NAMES,*selected]:
        p=A/old;inputs.append(p);outputs.append(save(route(old),route(p.read_text(encoding='utf8'))))
    # Rank20 backend/decoder and11 parent callbacks are exactly the already
    # qualified sources: new nonidentity stages are applied only after174.
    import stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    normal=importlib.import_module(Path(EXTRAS[0]).stem)
    assert set(normal.RECIPES)==set(stage.BACKENDS)
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,planpath,A/'rank20_after174_complement61_predeclared_plan_v1_20261010.json',A/'stock_rank20_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json']}
    for old in [previous.EXTRAS[9],previous.EXTRAS[10]]:create(A/route(old),{'status':'compiled_exact63_rank20_complement_QA93_before_actual_future_dispatch','input_sha256':pins,'expected_records':63,'expected_full_board':17173,'parent_rounds':[174,181],'new_quality_scores':0,'test_labels_read':False})
    for p in source_paths():assert p.is_file(),p
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(182,181,(465,))
    assert '(182, 93, 63)' in (A/NAMES[-1]).read_text(encoding='utf8')
    for n in selected:importlib.import_module(Path(route(n)).stem)
    proof=A/'stock_rank20_embedding182_full_execution_sources_admission_v1_20261010.json';create(proof,{'status':'compiled_complete63_actual_rank20_complement_QA93_and_main_sources_before_future','input_sha256':pins,'expected_records':63,'expected_full_board':17173,'parent_rounds':[174,181],'new_nonidentity_stage_base_only':174,'preserved_actual_own6_full5_native42_backend_and_original11_callbacks':True,'new_quality_scores':0,'test_labels_read':False})
    tasks=[('actual_stock_rank20_embedding63_after181_normalization_queue_v5_20261010',EXTRAS[0]),('StockRank20Embedding63_selected_native14_v5_20261010',EXTRAS[1]),('StockRank20Embedding182_complete63_family_v6_20261010',EXTRAS[5])]
    for name,n in tasks:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'rank20_complement_complete63_QA93_queued':True,'nonidentity_base_round':174,'existing_rank20_backend_reused_exactly':True,'future_pending':True},flush=True)
if __name__=='__main__':main()
