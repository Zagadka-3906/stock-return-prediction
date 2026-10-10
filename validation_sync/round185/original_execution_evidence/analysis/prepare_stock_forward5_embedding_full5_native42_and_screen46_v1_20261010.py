"""Predeclare forward5-return whole-parent replays and complete TRAIN screening."""
from pathlib import Path
import sys,importlib,ast,copy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
RECIPE='stock_forward5_embedding16_cross120_return5mean_recent252_small512_BF16_e64'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    return text.replace('stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64',RECIPE).replace('stock_rank5_embedding_rank5mean_direct','stock_forward5_embedding_return5mean_direct').replace('stock_rank5_embedding','stock_forward5_embedding').replace('StockRank5Embedding','StockForward5Embedding')
def main():
    assert allowed();inputs=[];outputs=[]
    pairs=[('verify_stock_rank5_embedding_small512_full5_independent_v1_20261010.py','verify_stock_forward5_embedding_small512_full5_independent_v1_20261010.py'),('stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','stock_forward5_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py'),('verify_stock_rank5_embedding_six_state_native42_v1_20261010.py','verify_stock_forward5_embedding_six_state_native42_v1_20261010.py'),('run_stock_rank5_embedding_after171_fast17_screen_v1_20261010.py','run_stock_forward5_embedding_after171_fast17_screen_v1_20261010.py'),('run_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010.py','run_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010.py')]
    for old,new in pairs:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        text=text.replace('(169,170,171,172,173,174,175,176)','(169,170,171,172,173,174,175,176,177)')
        text=text.replace('own_Top10_BCE_large_allocation_and_all_valid_hypotheses','own_forward5_return_Huber_e64_large_allocation_and_all_valid_hypotheses')
        outputs.append(save(new,text))
    full,stage,native42,screen,large=outputs
    m=importlib.import_module(stage.stem);assert list(m.BACKENDS)==[RECIPE]
    assert len(importlib.import_module(screen.stem).cases())==17 and len(importlib.import_module(large.stem).cases())==29
    proof=A/'stock_forward5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_new_forward5_return_own64_full5_native42_17_and29_TRAIN_sources_actual_completion_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_forward5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json']},'recipe':RECIPE,'expected_full_validation_rows':5635800,'native42_saved_states':6,'scored_records':46,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    original=A/'run_stock_rank5_embedding_full5_native42_and_early17_queue_v1_20261010.py';queue=save('run_stock_forward5_embedding_full5_native42_and_early17_queue_v1_20261010.py',route(original.read_text(encoding='utf8')))
    source=A/'predict_stock_rank5_embedding_complete_qualified_parent_scheme_v1_20261010.py';text=route(source.read_text(encoding='utf8')).replace('STOCK_RANK5_EMBEDDING','STOCK_FORWARD5_EMBEDDING').replace('(169,170,171,172,173,174,175,176)','(169,170,171,172,173,174,175,176,177)')
    needle='def parent_filename(graph):\n';assert text.count(needle)==1
    text=text.replace(needle,needle+"    from stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as rank5_key\n    if rank5_key in graph:return 'predict_stock_rank5_embedding_complete_qualified_parent_scheme_v1_20261010.py'\n")
    predictor=save('predict_stock_forward5_embedding_complete_qualified_parent_scheme_v1_20261010.py',text);pred=importlib.import_module(predictor.stem)
    parents=[r['parent'] for r in read(A/'stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1_20261010.json')['records']]+[source.name];rows=[]
    for filename in parents:
        p=A/filename;tree=ast.parse(pred.prepared_parent(p.read_text(encoding='utf8')));nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def previous(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and(e is component or e is components);events.append('whole_parent_first');return 22,{'prior_report':True}
        def appended(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('forward5_return_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=previous,STOCK_FORWARD5_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=appended)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_callback_CPU','exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','forward5_return_last'];rows.append({'parent':filename,'sha256':sha(p),'actual_callback_order':events,'stub_CPU_only_no_saved_model_inference_claimed':True})
    callbacks=A/'stock_forward5_embedding_actual_nine_parent_callbacks_CPU_controls_v1_20261010.json'
    create(callbacks,{'status':'passed_actual_nine_exact_parent_callback_expressions_and_compiled46_TRAIN_cases','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,predictor,proof,screen,large]},'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    publishers=[]
    for old,new,version in [('publish_stock_rank5_embedding_six_state_native42_completion_v64_20261010.py','publish_stock_forward5_embedding_six_state_native42_completion_v67_20261010.py',('v64_20261010','v67_20261010')),('publish_stock_rank5_embedding_after171_completion_v63_20261010.py','publish_stock_forward5_embedding_after171_completion_v66_20261010.py',('v63_20261010','v66_20261010')),('publish_stock_rank5_embedding_after171_large29_completion_v65_20261010.py','publish_stock_forward5_embedding_after171_large29_completion_v68_20261010.py',('v65_20261010','v68_20261010'))]:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8')).replace(*version).replace('stock_forward5_embedding_actual_eight_parent_callbacks_CPU_controls_v1','stock_forward5_embedding_actual_nine_parent_callbacks_CPU_controls_v1').replace('stock_forward5_embedding_complete48_after176_selection_plan_v1','stock_forward5_embedding_complete48_after177_selection_plan_v1')
        publishers.append(save(new,text))
    plan=A/'stock_forward5_embedding_complete48_after177_selection_plan_v1_20261010.json'
    create(plan,{'status':'predeclared_complete48_two_forward5_return_grids_and_qualified171177_anchors_before_new_scores','expected_records':48,'fully_qualified_anchors':[171,177],'families':[{'name':'StockForward5EmbeddingSmall512_after171_high_impact17','base_round':171,'records':17,'stage_kind':'stock_forward5_embedding_return5mean_direct','actual_service':'actual_stock_forward5_embedding_after171_fast17_screen_v1_20261010','main_receipt':'stock_forward5_embedding17_after171_completion_main_receipt_v66_20261010.json'},{'name':'StockForward5EmbeddingSmall512_after171_large_allocation29','base_round':171,'records':29,'stage_kind':'stock_forward5_embedding_return5mean_direct','actual_service':'actual_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010','main_receipt':'stock_forward5_embedding29_after171_completion_main_receipt_v68_20261010.json'}],'expected_full_controls':44,'expected_prefix_controls':132,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','future_X_read_for_selection':False,'test_labels_read':False})
    tasks=[('actual_stock_forward5_embedding_full5_native42_and_early17_queue_v1_20261010',queue),('actual_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010',large),('actual_stock_forward5_embedding_six_state_native42_completion_main_v67_20261010',publishers[0]),('actual_stock_forward5_embedding_after171_completion_main_v66_20261010',publishers[1]),('actual_stock_forward5_embedding_after171_large29_completion_main_v68_20261010',publishers[2])]
    for name,p in tasks:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(plan):sha(plan)});create(A/(name+'_activation.json'),row)
    print({'actual_forward5_full5_native42_screen46_and_main_queues_started':True,'actual_parent_callbacks_CPU':9,'complete48_predeclared':True,'new_scores':0},flush=True)
if __name__=='__main__':main()
