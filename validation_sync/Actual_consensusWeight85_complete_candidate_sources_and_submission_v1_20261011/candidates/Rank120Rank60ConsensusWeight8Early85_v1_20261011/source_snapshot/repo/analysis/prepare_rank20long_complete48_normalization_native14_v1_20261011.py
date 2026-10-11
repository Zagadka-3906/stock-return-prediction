"""Freeze long504 17+29 records and175/187 anchors; execute exact11 CPU callbacks before qualification."""
from pathlib import Path
import sys,re,ast,copy,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
NORMAL='normalize_completed_stock_rank20long_embedding_complete48_after187_v1_20261011'
QUAL='qualify_stock_rank20long_embedding48_selected_native14_v1_20261011'
PRED='predict_stock_rank20long_embedding_complete_qualified_parent_scheme_v1_20261011'
CALL='stock_rank20long_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011'
PLAN='stock_rank20long_embedding_complete48_after187_selection_plan_v1_20261011'

def namespace(text):
    return text.replace('stock_rank20seed10_embedding','stock_rank20long_embedding').replace('StockRank20Seed10Embedding','StockRank20LongEmbedding').replace('STOCK_RANK20SEED10_EMBEDDING','STOCK_RANK20LONG_EMBEDDING').replace('rank20mean_recent252','rank20mean_recent504').replace('Cross120Recent252Rank20Mean_seed10_e64','Cross120Recent504Rank20Mean_seed09_e64')

def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed()
    oldpred=A/'predict_stock_rank20seed10_embedding_complete_qualified_parent_scheme_v1_20261011.py'
    predictor=save(PRED+'.py',namespace(oldpred.read_text(encoding='utf8')));module=importlib.import_module(PRED)
    original_callbacks=A/'stock_rank20seed10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json';rows=[]
    for row in read(original_callbacks)['records']:
        p=A/row['parent'];tree=ast.parse(module.prepared_parent(p.read_text(encoding='utf8')))
        nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def before(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and (e is component or e is components)
            events.append('whole_parent_first');return 22,{}
        def after(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('long504_stage_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=before,STOCK_RANK20LONG_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=after)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_long504_CPU_callback','exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','long504_stage_last']
        rows.append({'parent':p.name,'sha256':sha(p),'actual_callback_order':events,'CPU_stub_only_no_native_or_future_inference_claim':True})
    assert len(rows)==11
    callbacks=A/(CALL+'.json');create(callbacks,{'status':'passed_actual_eleven_complete_parent_callback_expressions_for_long504','records':rows,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),oldpred,predictor,original_callbacks]},'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    oldnormal=A/'normalize_completed_stock_rank20seed10_embedding_complete48_after185_v1_20261011.py'
    text=namespace(oldnormal.read_text(encoding='utf8'))
    oldservice='StockTopPairEmbedding185_complete48_family_v9_complete_references_v9_20261010'
    assert text.count(oldservice)==1;text=text.replace(oldservice,'__ACTUAL_PARENT187_SERVICE__')
    text=re.sub(r'(?<!\d)185(?!\d)','187',text).replace('__ACTUAL_PARENT187_SERVICE__','Rank20TwoSeed187_complete88_family_v2_20261011')
    normalization=save(NORMAL+'.py',text)
    oldqual=A/'qualify_stock_rank20seed10_embedding48_selected_native14_v1_20261011.py'
    text=namespace(oldqual.read_text(encoding='utf8'));text=re.sub(r'(?<!\d)185(?!\d)','187',text)
    qualifier=save(QUAL+'.py',text)
    families=[{'name':f'StockRank20LongEmbeddingSmall512_after175_{kind}',
        'actual_service':f'actual_stock_rank20long_embedding_after175_{driver}_screen_v1_20261010',
        'records':count,'base_round':175,'stage_kind':'stock_rank20long_embedding_rank20mean_direct',
        'main_receipt':'StockRank20Long_objective_native42_official46_main_receipt_v1_20261010.json'}
        for kind,driver,count in [('high_impact17','fast17',17),('large_allocation29','large_allocation29',29)]]
    plan=A/(PLAN+'.json');create(plan,{'status':'predeclared48_long504_records_and175187_qualified_anchors_before_normalization',
        'expected_records':48,'fully_qualified_anchors':[175,187],'families':families,'training_calendar_window':504,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    normal=importlib.import_module(NORMAL)
    import stock_rank20long_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    native=importlib.import_module(next(iter(stage.BACKENDS.values()))[0])
    assert set(normal.RECIPES)==set(stage.BACKENDS)
    assert native.CONFIG['training_calendar_window']==504 and native.CONFIG['epochs']==64 and native.CONFIG['seed']==20261009
    proof=A/'rank20long_complete48_normalization_native14_sources_admission_v1_20261011.json'
    paths=[Path(__file__),oldpred,oldnormal,oldqual,original_callbacks,predictor,normalization,qualifier,callbacks,plan,
        Path(stage.__file__),Path(native.__file__),A/'recent504_rank20_mature_population_actual_CPU_controls_v1_20261011.json',
        A/'stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010.json']
    create(proof,{'status':'compiled_actual48_long504_normalizer_native14_and_actual_CPU11_before_future',
        'input_sha256':{str(p):sha(p) for p in paths},'configuration':native.CONFIG,'anchors':[175,187],
        'actual_callback_CPU_count':11,'expected_records':48,'full188_future_candidate_registry_pipeline_pending':True,
        'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    for name,p in [('actual_stock_rank20long_embedding48_after187_normalization_queue_v1_20261011',normalization),('StockRank20LongEmbedding48_selected_native14_v1_20261011',qualifier)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
    print({'long504_normalization48_native14_queued':True,'actual_callback_CPU_checks':11,'full188_future_pipeline_pending':True},flush=True)

if __name__=='__main__':main()
