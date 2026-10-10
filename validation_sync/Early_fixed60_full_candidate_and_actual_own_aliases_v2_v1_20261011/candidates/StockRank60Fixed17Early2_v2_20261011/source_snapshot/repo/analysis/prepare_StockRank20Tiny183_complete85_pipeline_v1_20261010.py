"""Frozen82 tight-weight comparisons and3 qualified anchors; full85/QA94 route."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_StockRank20Complement182_complete63_pipeline_v1_20261010 as previous
def route(text):
    actual=read(A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json')['service_aliases']['StockRankWide32Embedding181_complete48_family_v7_20261010']
    mapping={actual:'StockRank20Embedding182_complete63_family_v6_20261010','prepare_StockRank20Complement182_complete63_pipeline_v1_20261010':Path(__file__).stem,'stock_rank20_embedding182':'stock_rank20_embedding183','StockRank20Embedding182':'StockRank20Embedding183','stock_rank20_embedding63':'stock_rank20_embedding85','StockRank20Embedding63':'StockRank20Embedding85','stock_rank20_embedding_complete63':'stock_rank20_embedding_complete85','complete63':'complete85','full63':'full85','pilot63':'pilot85','anchor63':'anchor85','182':'183','181':'182','qa93':'qa94','QA93':'QA94','qa_v93':'qa_v94','17173':'17258','465':'466'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    for old,new in [(63,85),(60,80),(180,240),(93,94)]:text=re.sub(r'\b'+str(old)+r'\b',str(new),text)
    return text.replace('[174,182]','[174,175,182]').replace('(174,182)','(174,175,182)')
NAMES=[route(n) for n in previous.NAMES]
EXTRAS=[route(n) for n in previous.EXTRAS[:12]]+previous.EXTRAS[12:]
EXTRAS += ['rank20_tiny_CDF82_after174175_predeclared_plan_v1_20261010.json','run_stock_rank20_embedding_after174_tiny_CDF41_screen_v1_20261010.py','run_stock_rank20_embedding_after175_tiny_CDF41_screen_v1_20261010.py','publish_rank20_tinyCDF82_stages_main_v68_20261010.py']
def source_paths():
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*previous.source_paths()]))
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();inputs=[];outputs=[]
    plan={'status':'predeclared85_rank20_tiny_CDF82_plus_qualified174175182_anchors_before_any_futureX','expected_records':85,'fully_qualified_anchors':[174,175,182],'families':[{'name':f'StockRank20EmbeddingSmall512_after{parent}_tiny_CDF41','base_round':parent,'records':41,'stage_kind':'stock_rank20_embedding_rank20mean_direct','actual_service':f'actual_stock_rank20_embedding_after{parent}_tiny_CDF41_screen_v1_20261010','main_receipt':f'Rank20_tinyCDF41_after{parent}_main_receipt_v{version}_20261010.json'} for parent,version in ((174,69),(175,70))],'expected_full_controls':80,'expected_prefix_controls':240,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','future_X_read_for_selection':False,'test_labels_read':False}
    planpath=A/'stock_rank20_embedding_complete85_after182_selection_plan_v1_20261010.json';create(planpath,plan)
    selected=[n for n in previous.EXTRAS[:9] if n.endswith('.py')]
    for old in [*previous.NAMES,*selected]:
        p=A/old;inputs.append(p);outputs.append(save(route(old),route(p.read_text(encoding='utf8'))))
    import stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    normal=importlib.import_module(Path(EXTRAS[0]).stem)
    assert set(normal.RECIPES)==set(stage.BACKENDS)
    normalized=(A/EXTRAS[0]).read_text(encoding='utf8');candidate=(A/EXTRAS[3]).read_text(encoding='utf8')
    assert 'for number in (174,175,182):' in normalized and 'parent_number in (174,175,182)' in candidate
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,planpath,A/'rank20_tiny_CDF82_after174175_predeclared_plan_v1_20261010.json']}
    for old in [previous.EXTRAS[9],previous.EXTRAS[10]]:create(A/route(old),{'status':'compiled_exact85_rank20_tiny_CDF_QA94_before_actual_future_dispatch','input_sha256':pins,'expected_records':85,'expected_full_board':17258,'parent_rounds':[174,175,182],'new_quality_scores':0,'test_labels_read':False})
    for p in source_paths():assert p.is_file(),p
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(183,182,(466,))
    assert '(183, 94, 85)' in (A/NAMES[-1]).read_text(encoding='utf8')
    for n in selected:importlib.import_module(Path(route(n)).stem)
    proof=A/'stock_rank20_embedding183_full_execution_sources_admission_v1_20261010.json';create(proof,{'status':'compiled_complete85_actual_rank20_tight82_QA94_main_sources_before_future','input_sha256':pins,'expected_records':85,'expected_full_board':17258,'parent_rounds':[174,175,182],'nonidentity_stage_bases':[174,175],'preserved_actual_own6_full5_native42_backend_and_original11_callbacks':True,'new_quality_scores':0,'test_labels_read':False})
    tasks=[('actual_stock_rank20_embedding85_after182_normalization_queue_v5_20261010',EXTRAS[0]),('StockRank20Embedding85_selected_native14_v5_20261010',EXTRAS[1]),('StockRank20Embedding183_complete85_family_v6_20261010',EXTRAS[5])]
    for name,n in tasks:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'rank20_tight82_complete85_QA94_queued':True,'qualified_anchors':[174,175,182],'existing_rank20_backend_reused_exactly':True,'future_pending':True},flush=True)
if __name__=='__main__':main()
