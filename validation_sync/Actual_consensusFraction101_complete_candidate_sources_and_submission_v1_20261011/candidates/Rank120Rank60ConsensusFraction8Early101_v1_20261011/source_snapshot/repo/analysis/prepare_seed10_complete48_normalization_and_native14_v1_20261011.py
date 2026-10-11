"""Freeze real seed10 17+29 screens with175/185 anchors; qualify the winner before future use."""
from pathlib import Path
import sys,re,ast,copy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
NORMAL='normalize_completed_stock_rank20seed10_embedding_complete48_after185_v1_20261011'
QUAL='qualify_stock_rank20seed10_embedding48_selected_native14_v1_20261011'
PRED='predict_stock_rank20seed10_embedding_complete_qualified_parent_scheme_v1_20261011'
CALL='stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011'
PLAN='stock_rank20seed10_embedding_complete48_after185_selection_plan_v1_20261011'
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def namespace(text):
    return text.replace('stock_rank20_embedding','stock_rank20seed10_embedding').replace('StockRank20Embedding','StockRank20Seed10Embedding').replace('STOCK_RANK20_EMBEDDING','STOCK_RANK20SEED10_EMBEDDING')
def main():
    assert allowed();sources=[];outputs=[]
    original=A/'predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py';sources.append(original)
    predictor=save(PRED+'.py',namespace(original.read_text(encoding='utf8')));outputs.append(predictor)
    module=importlib.import_module(PRED)
    oldcallbacks=A/'stock_rank20_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261010.json';sources.append(oldcallbacks)
    rows=[]
    for row in read(oldcallbacks)['records']:
        p=A/row['parent'];tree=ast.parse(module.prepared_parent(p.read_text(encoding='utf8')))
        nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def before(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and (e is component or e is components)
            events.append('whole_parent_first');return 22,{}
        def after(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('seed10_stage_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=before,STOCK_RANK20SEED10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=after)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_CPU_callback','exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','seed10_stage_last']
        rows.append({'parent':p.name,'sha256':sha(p),'actual_callback_order':events,'stub_CPU_only_no_saved_model_inference_claimed':True})
    create(A/(CALL+'.json'),{'status':'passed_actual_eleven_complete_parent_callback_expressions','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,predictor,oldcallbacks]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    oldnormal=A/'normalize_completed_stock_rank20_embedding_complete48_after179_v5_20261010.py';sources.append(oldnormal)
    text=namespace(oldnormal.read_text(encoding='utf8')).replace('179','185').replace('173','175')
    text=text.replace('stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261010',CALL)
    text=text.replace('stock_rank20seed10_embedding_complete48_after185_selection_plan_v1_20261010',PLAN)
    oldservice='StockForward20Embedding185_complete48_family_v6_after_Dual25_recovery_v1_20261010'
    assert text.count(oldservice)==1
    routes=A/'PairTop184185_complete_reference_routes_v9_20261010.json';actual185=read(routes)['service_aliases']['StockTopPairEmbedding185_complete48_family_v9_20261010']
    text=text.replace(oldservice,actual185)
    text=text.replace('Cross120Recent252Rank20Mean_seed09_e64','Cross120Recent252Rank20Mean_seed10_e64')
    normalization=save(NORMAL+'.py',text);outputs.append(normalization)
    oldqual=A/'qualify_stock_rank20_embedding48_selected_native14_v5_20261010.py';sources.append(oldqual)
    text=namespace(oldqual.read_text(encoding='utf8')).replace('179','185')
    text=text.replace('normalize_completed_stock_rank20seed10_embedding_complete48_after185_v5_20261010',NORMAL)
    text=text.replace('predict_stock_rank20seed10_embedding_complete_qualified_parent_scheme_v1_20261010',PRED)
    text=text.replace('stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261010',CALL)
    text=text.replace('actual_stock_rank20seed10_embedding48_after185_normalization_queue_v5_20261010','actual_stock_rank20seed10_embedding48_after185_normalization_queue_v1_20261011')
    qualifier=save(QUAL+'.py',text);outputs.append(qualifier)
    families=[{'name':f'StockRank20Seed10EmbeddingSmall512_after175_{kind}',
        'actual_service':f'actual_stock_rank20seed10_embedding_after175_{driver}_screen_v1_20261010','records':count,'base_round':175,
        'stage_kind':'stock_rank20seed10_embedding_rank20mean_direct','main_receipt':'StockRank20Seed10_objective_native42_official46_main_receipt_v1_20261010.json'}
        for kind,driver,count in [('high_impact17','fast17',17),('large_allocation29','large_allocation29',29)]]
    plan=A/(PLAN+'.json')
    create(plan,{'status':'predeclared48_seed10_records_and175185_qualified_anchors_before_normalization','expected_records':48,
        'fully_qualified_anchors':[175,185],'families':families,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    normal=importlib.import_module(NORMAL);qual=importlib.import_module(QUAL)
    import stock_rank20seed10_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    assert set(normal.RECIPES)==set(stage.BACKENDS) and qual.OUT.name=='stock_rank20seed10_embedding48_selected_native14_v1_20261010'
    proof=A/'seed10_complete48_normalization_native14_sources_admission_v1_20261011.json'
    create(proof,{'status':'compiled_actual48_normalizer_and_native14_sources_callback11_passed_full186_registry_not_created_yet',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*sources,*outputs,plan,A/(CALL+'.json'),routes]},
        'anchors':[175,185],'actual_prior185_service':actual185,'planned_records':48,'new_quality_scores':0,'new_native_fits':0,
        'complete186_future_pipeline_pending':True,'actual_future_X_read':False,'test_labels_read':False})
    for name,p in [('actual_stock_rank20seed10_embedding48_after185_normalization_queue_v1_20261011',normalization),('StockRank20Seed10Embedding48_selected_native14_v1_20261011',qualifier)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
    print({'normalization48_and_native14_queued':True,'actual_callback_CPU_checks':11,'full186_future_dispatch_not_created':True},flush=True)
if __name__=='__main__':main()
