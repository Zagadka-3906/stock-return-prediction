"""Run the actual whole qualified169/170 parent before a frozen two-model or holding stability stage."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os,shutil

def parent_filename(graph):
    from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as stock_key
    if stock_key in graph:return 'predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py'
    from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key133
    if key133 in graph:return 'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py'
    from stock_rank_dual44_selected_native_stage_v1_20261010 import GRAPH_KEY as key233
    from cross120_after_complete169_native_stage_v2_20261010 import GRAPH_KEY as key120
    if key233 in graph:return 'predict_frontier233_complete_parent_scheme_v1_20261010.py'
    return 'predict_cross120170_complete169_scheme_v1_20261010.py' if key120 in graph else 'predict_fast_neural_frontier169_complete_scheme_v2_20261010.py'


def prepared_parent(text):
    candidates=['\n        value,report=after_parent(ns,context,parent,spec,component);calls.append(report);return value','\n        value,report=after_parent(ns,context,parent,spec,components);calls.append(report);return value']
    matches=[needle for needle in candidates if text.count(needle)==1];assert len(matches)==1
    needle=matches[0];return text.replace(needle,needle.replace('return value','return STOCK_DUAL_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT(context,value)'))


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    from stock_rank_dual44_selected_native_stage_v1_20261010 import GRAPH_KEY,after_parent
    graph=record['winner'][ns.GRAPH_FIELD];spec=deepcopy(graph[GRAPH_KEY]);assert spec['anchor_round'] in (169,170,171,172,173)
    components=deepcopy(spec['native_components']);candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    assert len(components) in (1,2) and (len(components)==2)==(spec['stage_kind']=='stock_return_rank_embedding_consensus')
    locations=[]
    for component in components:
        source=Path(component['source_path']);target=candidate/(component['name']+'_final2025.joblib');assert ns.sha(source)==component['sha256']
        if not target.exists():
            if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
            else:
                with source.open('rb') as reader,target.open('xb') as writer:shutil.copyfileobj(reader,writer,4*1024**2)
        assert ns.sha(target)==component['sha256'];component['path']=str(target);locations.append((source,target))
    calls=[]
    def after_whole(context,parent):
        value,report=after_parent(ns,context,parent,spec,components);calls.append(report);return value
    final=candidate/'verification.json';intermediate=candidate/'whole_qualified_parent_before_frontier233.json'
    read,dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,value,*args,**kwargs):return dump(intermediate if Path(path).resolve()==final.resolve() else path,value,*args,**kwargs)
    proxy.dump=routed_dump
    source=ns.ROOT/'analysis'/parent_filename(graph)
    namespace={'__file__':str(source),'__name__':'actual_whole_qualified_parent_then_frontier233','STOCK_DUAL_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT':after_whole}
    exec(compile(prepared_parent(source.read_text(encoding='utf8')),str(source),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[report for report in calls if report['rows']==1599600];cold=[report for report in calls if report['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1 and all(report['native_reload_independent_tensor_and_Pandas_stage_bits_exact'] for report in calls)
    before=len(result['models']);reuse=[]
    for index,(component,(source,target)) in enumerate(zip(components,locations)):
        existing=[key for key,model in result['models'].items() if model['sha256']==component['sha256']];assert len(existing)<=1
        if existing:
            reuse.append({'key':existing[0],'sha256':component['sha256'],'additional_physical_models':0});continue
        key='frontier233_'+component['name'];assert key not in result['models'];result['models'][key]=component
        storage.append({'key':key,'source':str(source),'target':str(target),'sha256':component['sha256'],'samefile':os.path.samefile(source,target)})
        for field,report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
            control=deepcopy(report['controls'][index]);control['name']=key;result[field].append(control)
        reuse.append({'key':key,'sha256':component['sha256'],'additional_physical_models':1})
    count=before+sum(item['additional_physical_models'] for item in reuse)
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==count
    assert len({model['sha256'] for model in result['models'].values()})==count
    result.update(actual_entire_qualified_parent_then_frontier233_native_independent_replays=True,stock_dual_embedding_stage_calls=calls,
        stock_dual_embedding_physical_leaf_reuse=reuse,complete_qualified_parent_all_graph_branches_preserved=True)
    dump(final,result,immutable=True)
    dump(candidate/'stock_rank_dual44_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_whole_qualified_parent_frontier233_two_full_independent_replays_and_cold80','calls':calls,
        'actual_parent_predictor':parent_filename(graph),'actual_saved_model_count':count,'actual_native_model_storage':storage,
        'physical_leaf_reuse':reuse,'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
