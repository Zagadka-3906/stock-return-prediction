"""Complete48 mean20 daily-rank qualification, inference, QA91 and verified main routes."""
from pathlib import Path
import sys,re,ast,copy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import admit_StockForward20Embedding179_complete48_pipeline_v2_20261010 as previous
def route(text):
    mapping={'StockForward5Embedding178_complete48_family_v5_20261010':'StockForward20Embedding179_complete48_family_v6_after_Dual25_recovery_v1_20261010','admit_StockForward20Embedding179_complete48_pipeline_v2_20261010':Path(__file__).stem,'stock_forward20_embedding179':'stock_rank20_embedding180','StockForward20Embedding179':'StockRank20Embedding180','stock_forward20_embedding':'stock_rank20_embedding','StockForward20Embedding':'StockRank20Embedding','STOCK_FORWARD20_EMBEDDING':'STOCK_RANK20_EMBEDDING','return20mean':'rank20mean','return20_mean':'rank20_mean','Forward20Mean':'Rank20Mean','ten_parent':'eleven_parent','179':'180','178':'179','qa90':'qa91','QA90':'QA91','qa_v90':'qa_v91','17014':'17062','462':'463'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=re.sub(r'\b90\b','91',text)
    return text.replace('二十日平均收益Huber目标','二十日平均收益的截面排名Huber目标').replace('forward20_return','rank20_rank')
NAMES=[route(n) for n in previous.NAMES]
EXTRAS=[route(n) for n in previous.EXTRAS]
def source_paths():
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*previous.source_paths()]))
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();inputs=[];outputs=[]
    original=A/'predict_stock_forward20_embedding_complete_qualified_parent_scheme_v1_20261010.py';inputs.append(original)
    text=route(original.read_text(encoding='utf8'));needle='def parent_filename(graph):\n';assert text.count(needle)==1
    text=text.replace(needle,needle+"    from stock_forward20_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as previous_key\n    if previous_key in graph:return 'predict_stock_forward20_embedding_complete_qualified_parent_scheme_v1_20261010.py'\n")
    text=text.replace('(169,170,171,172,173,174,175,176,177,179)','(169,170,171,172,173,174,175,176,177,178,179)')
    predictor=save('predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py',text);outputs.append(predictor);pred=importlib.import_module(predictor.stem)
    parents=[r['parent'] for r in read(A/'stock_forward20_embedding_actual_ten_parent_callbacks_CPU_controls_v1_20261010.json')['records']]+[original.name];rows=[]
    for filename in parents:
        p=A/filename;tree=ast.parse(pred.prepared_parent(p.read_text(encoding='utf8')));nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def before(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and (e is component or e is components);events.append('whole_parent_first');return 22,{}
        def after(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('rank20_stage_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=before,STOCK_RANK20_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=after)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_CPU_callback', 'exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','rank20_stage_last'];rows.append({'parent':filename,'sha256':sha(p),'actual_callback_order':events,'stub_CPU_only_no_saved_model_inference_claimed':True})
    callbacks=A/'stock_rank20_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261010.json';create(callbacks,{'status':'passed_actual_eleven_complete_parent_callback_expressions','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,predictor]},'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    plan=read(A/'stock_forward20_embedding_complete48_after178_selection_plan_v1_20261010.json')
    plan['status']='predeclared48_rank20_two_grids173_and_qualified173179_anchors_before_new_scores';plan['fully_qualified_anchors']=[173,179]
    for f in plan['families']:
        f.update(name=f['name'].replace('StockForward20','StockRank20'),stage_kind='stock_rank20_embedding_rank20mean_direct',actual_service=f['actual_service'].replace('stock_forward20','stock_rank20'))
        f['main_receipt']=f['main_receipt'].replace('stock_forward20','stock_rank20').replace('v73_','v77_').replace('v75_','v79_')
    planpath=A/'stock_rank20_embedding_complete48_after179_selection_plan_v1_20261010.json';create(planpath,plan)
    # Same scientific controls, native vocabulary and all actual rows; every output is new and exclusive.
    selected=[n for n in previous.EXTRAS if n.endswith('.py') and ('179' in n or 'after178_v5' in n or 'selected_native14_v5' in n)]
    for old in [*previous.NAMES,*selected]:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        text=text.replace('prepare_stock_rank20_embedding_full5_native42_screen46_v1','prepare_stock_rank20_embedding_full5_native42_and_screen46_v1')
        outputs.append(save(route(old),text))
    # Inventory uses the actual existing preparation entry name, not the old mean-return spelling.
    for i,n in enumerate(EXTRAS):EXTRAS[i]=n.replace('prepare_stock_rank20_embedding_full5_native42_screen46_v1','prepare_stock_rank20_embedding_full5_native42_and_screen46_v1')
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,planpath,callbacks]}
    for old in [previous.EXTRAS[9],previous.EXTRAS[10]]:create(A/route(old),{'status':'compiled_exact48_rank20_QA91_before_actual_future_dispatch','input_sha256':pins,'expected_records':48,'expected_full_board':17062,'parent_rounds':[173,179],'new_quality_scores':0,'test_labels_read':False})
    for p in source_paths():assert p.is_file(),p
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(180,179,(463,))
    assert '(180, 91, 48)' in (A/NAMES[-1]).read_text(encoding='utf8')
    for n in selected:importlib.import_module(Path(route(n)).stem)
    proof=A/'stock_rank20_embedding180_full_execution_sources_admission_v1_20261010.json';create(proof,{'status':'compiled_complete48_own_rank20_QA91_and_main_sources_before_future','input_sha256':pins,'expected_records':48,'expected_full_board':17062,'parent_rounds':[173,179],'actual_parent_service':'StockForward20Embedding179_complete48_family_v6_after_Dual25_recovery_v1_20261010','new_quality_scores':0,'test_labels_read':False})
    publications=[]
    for old,new,oldver,newver in [('publish_stock_forward20_embedding_after173_completion_v73_20261010.py','publish_stock_rank20_embedding_after173_completion_v77_20261010.py','v73_20261010','v77_20261010'),('publish_stock_forward20_embedding_six_state_native42_completion_v74_20261010.py','publish_stock_rank20_embedding_six_state_native42_completion_v78_20261010.py','v74_20261010','v78_20261010'),('publish_stock_forward20_embedding_after173_large29_completion_v75_20261010.py','publish_stock_rank20_embedding_after173_large29_completion_v79_20261010.py','v75_20261010','v79_20261010')]:
        text=route((A/old).read_text(encoding='utf8')).replace(oldver,newver);publications.append(save(new,text))
    tasks=[('actual_stock_rank20_embedding48_after179_normalization_queue_v5_20261010','normalize_completed_stock_rank20_embedding_complete48_after179_v5_20261010.py'),('StockRank20Embedding48_selected_native14_v5_20261010','qualify_stock_rank20_embedding48_selected_native14_v5_20261010.py'),('StockRank20Embedding180_complete48_family_v6_20261010','run_StockRank20Embedding180_complete_family_v6_20261010.py'),('actual_stock_rank20_embedding_after173_completion_main_v77_20261010',publications[0].name),('actual_stock_rank20_embedding_six_state_native42_completion_main_v78_20261010',publications[1].name),('actual_stock_rank20_embedding_after173_large29_completion_main_v79_20261010',publications[2].name)]
    for name,n in tasks:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'rank20_complete48_main_and_QA91_queues_started':True,'callbacks_actual_CPU':11,'future_pending':True},flush=True)
if __name__=='__main__':main()
