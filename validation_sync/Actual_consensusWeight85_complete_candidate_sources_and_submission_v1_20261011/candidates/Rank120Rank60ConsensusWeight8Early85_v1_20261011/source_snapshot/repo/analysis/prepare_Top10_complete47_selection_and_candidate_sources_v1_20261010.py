"""Complete selection and frozen inference sources for both predeclared classifier grids."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
RECIPE='stock_top10_embedding16_cross120_top10_BCE_Pos9_recent252_small512_BF16_e24'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    mapping={'StockEmbedding173':'StockTop10Embedding175','stock_embedding173':'stock_top10_embedding175','stock_embedding36':'stock_top10_embedding47','StockEmbedding36':'StockTop10Embedding47','normalize_completed_stock_embedding36_after172':'normalize_completed_stock_top10_embedding47_after174','stock_embedding_complete36_after172':'stock_top10_embedding_complete47_after174','stock_embedding_after_complete_qualified_parent_native_stage_v1':'stock_top10_embedding_after_complete_qualified_parent_native_stage_v2','predict_stock_embedding_complete_qualified_parent_scheme_v1':'predict_stock_top10_embedding_complete_qualified_parent_scheme_v1','stock_embedding_after_complete_qualified_parent_v1':'stock_top10_embedding_after_complete_qualified_parent_v1','stock_embedding16_cross120_return1d_recent252_small512_BF16_e24':RECIPE,'stock_embedding_small512_BF16_bank6_v1':'stock_top10_embedding_small512_BF16_bank6_v1','stock_embedding_return1d_direct':'stock_top10_embedding_BCE_classifier_direct','stock_embedding_native_stage_and_four_parent_routes_admission_v1':'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1','stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1':'stock_top10_actual_six_parent_callback_CPU_controls_v1','actual_StockEmbeddingSmall512_full5_independent_location_v1':'actual_StockTop10EmbeddingSmall512_full5_independent_location_v1','stock_embedding_complete_parent_native_replay_verification':'stock_top10_embedding_complete_parent_native_replay_verification','passed_actual_complete_qualified_parent_stock_embedding_two_full_native_independent_replays_and_cold80':'passed_actual_complete_qualified_parent_stock_top10_embedding_two_full_native_independent_replays_and_cold80','pilot36':'pilot47','normalized36':'normalized47','anchor36':'anchor47','actual36':'actual47','all36':'all47','第173轮':'第175轮'}
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
def main():
    assert allowed();inputs=[];outputs=[]
    plan=A/'stock_top10_embedding_complete47_after174_selection_plan_v1_20261010.json'
    create(plan,{'status':'predeclared_complete47_before_any_classifier_official_score','expected_records':47,'fully_qualified_anchors':[174],'families':[{'name':'StockTop10EmbeddingSmall512_after174_high_impact17','base_round':174,'records':17,'stage_kind':'stock_top10_embedding_BCE_classifier_direct','actual_service':'actual_stock_top10_embedding_after174_fast17_screen_v1_20261010','main_receipt':'stock_top10_embedding17_after174_completion_main_receipt_v59_20261010.json'},{'name':'StockTop10EmbeddingSmall512_after174_large_allocation29','base_round':174,'records':29,'stage_kind':'stock_top10_embedding_BCE_classifier_direct','actual_service':'actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010','main_receipt':'stock_top10_embedding29_after174_completion_main_receipt_v60_20261010.json'}],'expected_full_controls':44,'expected_prefix_controls':132,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','future_X_read_for_selection':False,'test_labels_read':False})
    source=A/'normalize_completed_stock_embedding36_after172_v1_20261010.py';inputs.append(source);text=source.read_text(encoding='utf8')
    text=text.replace('Frontier133172_complete36_family_v2_20261010','StockRankDual174_complete44_family_v2_20261010').replace('actual_stock_embedding_six_state_native42_v2_20261010','actual_stock_top10_embedding_six_state_native42_v1_20261010')
    text=route(text).replace("==36 and plan['fully_qualified_anchors']==[170,172]","==47 and plan['fully_qualified_anchors']==[174]").replace('for number in (170,172):','for number in (174,):').replace('(36,32,96)','(47,44,132)').replace("anchors[172]","anchors[174]").replace("'expected_scored_records':36","'expected_scored_records':47").replace("'actual_nonidentity_full_controls':32","'actual_nonidentity_full_controls':44").replace("'actual_nonidentity_prefix_controls':96","'actual_nonidentity_prefix_controls':132").replace("'actual_comparison_parent_round':172","'actual_comparison_parent_round':174")
    text=text.replace('rank_MLP512_StockEmbedding16_Cross120Recent252ReturnHuber050_seed09_e24','rank_MLP512_StockEmbedding16_Cross120Recent252Top10BCEPos9_seed09_e24')
    normal=save('normalize_completed_stock_top10_embedding47_after174_v1_20261010.py',text);outputs.append(normal)
    source=A/'qualify_stock_embedding36_selected_native14_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace('actual_stock_embedding36_after172_normalization_queue_v1','actual_stock_top10_embedding47_after174_normalization_queue_v1').replace('actual_stock_embedding_six_state_native42_v2','actual_stock_top10_embedding_six_state_native42_v1').replace("len(pilot['records'])==36","len(pilot['records'])==47")
    qualifier=save('qualify_stock_top10_embedding47_selected_native14_v1_20261010.py',text);outputs.append(qualifier)
    source=A/'stock_embedding173_storage_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace('r173','r175').replace('round173','round175').replace('number == 173','number == 175').replace('qa_v84','qa_v86').replace('QA84','QA86')
    storage=save('stock_top10_embedding175_storage_v1_20261010.py',text);outputs.append(storage)
    source=A/'prepare_StockEmbedding173_selected_candidate_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace("len(pilot['records'])==36","len(pilot['records'])==47").replace('parent_number in (170,172)','parent_number in (174,)').replace('expected_scored_records=36','expected_scored_records=47').replace("'scored_records':36","'scored_records':47")
    # Inventory points to the exact CamelCase seal source created below.
    text=text.replace('seal_stock_top10_embedding175_selected_candidate_v1','seal_StockTop10Embedding175_selected_candidate_v1')
    candidate=save('prepare_StockTop10Embedding175_selected_candidate_v1_20261010.py',text);outputs.append(candidate)
    source=A/'seal_StockEmbedding173_selected_candidate_v1_20261010.py';inputs.append(source);seal=save('seal_StockTop10Embedding175_selected_candidate_v1_20261010.py',route(source.read_text(encoding='utf8')));outputs.append(seal)
    normal_module=importlib.import_module(normal.stem);q=importlib.import_module(qualifier.stem);c=importlib.import_module(candidate.stem);s=importlib.import_module(storage.stem)
    assert list(normal_module.RECIPES)==[RECIPE] and q.OUT.name=='stock_top10_embedding47_selected_native14_v1_20261010'
    assert c.GRAPH_KEY=='stock_top10_embedding_after_complete_qualified_parent_v1_20261010' and len(s.OUTPUTS)==6 and s.EBASE.name=='第175轮_20261010'
    # Validate all module imports and all literal local source inventories now.
    import ast
    for p in outputs:
        tree=ast.parse(p.read_text(encoding='utf8'))
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom) and node.module and (A/(node.module+'.py')).exists():importlib.import_module(node.module)
    proof=A/'stock_top10_embedding175_candidate_sources_preparation_v1_20261010.json'
    create(proof,{'status':'compiled_complete47_classifier_selection_selected14_six_E_outputs_full175_candidate_freeze_sources_actual_future_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,plan,A/'stock_top10_actual_six_parent_callback_CPU_controls_v1_20261010.json']},'expected_records':47,'full_controls':44,'prefix_controls':132,'parent_rounds':[174],'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    for name,driver in [('actual_stock_top10_embedding47_after174_normalization_queue_v1_20261010',normal),('StockTop10Embedding47_selected_native14_v1_20261010',qualifier)]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'actual47_selection_queue_started':True,'selected14_queue_started':True,'full175_candidate_sources':'prepared','actual_future_dispatch':False},flush=True)
if __name__=='__main__':main()
