"""Predeclare complete rank5 coverage and execute whole-parent callback admission."""
from pathlib import Path
import sys,ast,copy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    source=A/'run_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('stock_top10_embedding','stock_rank5_embedding').replace('StockTop10Embedding','StockRank5Embedding').replace('stock_rank5_embedding16_cross120_top10_BCE_Pos9_recent252_small512_BF16_e24','stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64').replace('actual_stock_rank5_embedding_early171_six_state_native42_v3_20261010','actual_stock_rank5_embedding_six_state_native42_v1_20261010').replace('actual_stock_rank5_embedding_early171_six_state_native42_location_v3_20261010','actual_stock_rank5_embedding_six_state_native42_location_v1_20261010')
    needle="    closed('Frontier233171_complete233_family_v2_20261010')";assert text.count(needle)==1
    text=text.replace(needle,"    closed('actual_stock_rank5_embedding_after171_fast17_screen_v1_20261010')\n"+needle)
    large=save('run_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010.py',text)
    assert len(importlib.import_module(large.stem).cases())==29
    source=A/'predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010.py';text=source.read_text(encoding='utf8').replace('stock_top10_embedding','stock_rank5_embedding').replace('STOCK_TOP10_EMBEDDING','STOCK_RANK5_EMBEDDING').replace('stock_rank5_embedding_after_complete_qualified_parent_native_stage_v2','stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1').replace('(169,170,171,172,173,174)','(169,170,171,172,173,174,175,176)')
    needle='def parent_filename(graph):\n';text=text.replace(needle,needle+"    from stock_top10_embedding_after_complete_qualified_parent_native_stage_v2_20261010 import GRAPH_KEY as top_key\n    if top_key in graph:return 'predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010.py'\n")
    predictor=save('predict_stock_rank5_embedding_complete_qualified_parent_scheme_v1_20261010.py',text);pred=importlib.import_module(predictor.stem)
    parents=['predict_fast_neural_frontier169_complete_scheme_v2_20261010.py','predict_cross120170_complete169_scheme_v1_20261010.py','predict_frontier233_complete_parent_scheme_v1_20261010.py','predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py','predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py','predict_stock_rank_embedding_complete_qualified_parent_scheme_v1_20261010.py','predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py','predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010.py'];rows=[]
    for filename in parents:
        p=A/filename;tree=ast.parse(pred.prepared_parent(p.read_text(encoding='utf8')));nodes=[n for n in ast.walk(tree)if isinstance(n,ast.FunctionDef)and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def previous(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and(e is component or e is components);events.append('whole_parent_first');return 22,{'prior_report':True}
        def appended(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('rank5_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=previous,STOCK_RANK5_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=appended)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_callback_CPU','exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','rank5_last'];rows.append({'parent':filename,'sha256':sha(p),'actual_callback_order':events,'stub_CPU_only_no_saved_model_inference_claimed':True})
    proof=A/'stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1_20261010.json'
    create(proof,{'status':'passed_actual_eight_exact_parent_callback_expressions_and_compiled_original29_large_cases','records':rows,'input_sha256':{str(p):sha(p)for p in [Path(__file__),source,predictor,large,A/'stock_rank5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json']},'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    plan=A/'stock_rank5_embedding_complete48_after176_selection_plan_v1_20261010.json'
    create(plan,{'status':'predeclared_complete48_two_rank5_grids_and_qualified171176_anchors_before_new_rank5_scores','expected_records':48,'fully_qualified_anchors':[171,176],'families':[{'name':'StockRank5EmbeddingSmall512_after171_high_impact17','base_round':171,'records':17,'stage_kind':'stock_rank5_embedding_rank5mean_direct','actual_service':'actual_stock_rank5_embedding_after171_fast17_screen_v1_20261010','main_receipt':'stock_rank5_embedding17_after171_completion_main_receipt_v63_20261010.json'},{'name':'StockRank5EmbeddingSmall512_after171_large_allocation29','base_round':171,'records':29,'stage_kind':'stock_rank5_embedding_rank5mean_direct','actual_service':'actual_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010','main_receipt':'stock_rank5_embedding29_after171_completion_main_receipt_v65_20261010.json'}],'expected_full_controls':44,'expected_prefix_controls':132,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','future_X_read_for_selection':False,'test_labels_read':False})
    sourcepub=A/'publish_stock_top10_embedding_after171_large_allocation29_completion_v62_20261010.py';text=sourcepub.read_text(encoding='utf8')
    text=text.replace('stock_top10_embedding','stock_rank5_embedding').replace('StockTop10Embedding','StockRank5Embedding').replace('v61_20261010','v65_20261010').replace('actual_stock_rank5_embedding_early171_six_state_native42_location_v3','actual_stock_rank5_embedding_six_state_native42_location_v1').replace('after171_large_allocation29_screen_v2','after171_large_allocation29_screen_v1')
    start=text.index('    paths=[');end=text.index('    bank=Path(',start)
    text=text[:start]+"    paths=[Path(__file__),*native.glob('*.json'),A/'stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1_20261010.json',A/'stock_rank5_embedding_complete48_after176_selection_plan_v1_20261010.json',A/'run_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010.py',*screen.glob('*.json')]\n    for admission in ('stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json','stock_rank5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json','stock_rank5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'):\n        paths += [A/admission,*[Path(p) for p in read(A/admission)['input_sha256'] if Path(p).suffix=='.py']]\n"+text[end:]
    pub=save('publish_stock_rank5_embedding_after171_large29_completion_v65_20261010.py',text)
    for name,p in [('actual_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010',large),('actual_stock_rank5_embedding_after171_large29_completion_main_v65_20261010',pub)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(plan):sha(plan)});create(A/(name+'_activation.json'),row)
    print({'rank5_large29_and_main65_queues_started':True,'actual_parent_callback_CPU_controls':8,'complete48_predeclared':True},flush=True)
if __name__=='__main__':main()
