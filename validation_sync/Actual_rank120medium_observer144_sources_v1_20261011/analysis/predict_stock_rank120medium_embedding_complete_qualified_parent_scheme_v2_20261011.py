"""Execute all of157 before the frozen protected-tail stage; count physical neural leaves once."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os
def parent_filename(graph):
    from predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v2_20261011 import parent_filename as complete_parent
    return complete_parent(graph)


def prepared_parent(text):
    candidates=['\n        value,report=after_parent(ns,context,parent,spec,component);calls.append(report);return value','\n        value,report=after_parent(ns,context,parent,spec,components);calls.append(report);return value']
    matches=[needle for needle in candidates if text.count(needle)==1];assert len(matches)==1
    needle=matches[0];return text.replace(needle,needle.replace('return value','return STOCK_RANK10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT(context,value)'))


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    from stock_rank120medium_embedding_after_complete_qualified_parent_native_stage_v2_20261011 import after_parent,GRAPH_KEY
    graph=record['winner'][ns.GRAPH_FIELD];spec=deepcopy(graph[GRAPH_KEY])
    assert spec['original_complete_parent_round'] in (169,170,171,172,173,174,175,176,177,178,179,183)
    assert 'BF16_flag_after152157_complete_parent_rank_CDF' in graph
    component=deepcopy(spec['native_component']);source=Path(component['source_path'])
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    target=candidate/(component['name']+'_final2025.joblib');assert ns.sha(source)==component['sha256']
    if not target.exists():
        if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
        else:
            import shutil
            with source.open('rb') as reader,target.open('xb') as writer:shutil.copyfileobj(reader,writer,4*1024**2)
    assert ns.sha(target)==component['sha256'];component['path']=str(target)
    calls=[]
    def tail_stage(context,parent):
        value,report=after_parent(ns,context,parent,spec,component);calls.append(report);return value
    final=candidate/'verification.json';intermediate=candidate/'whole_qualified_parent_before_stock_rank120medium_embedding.json'
    read,dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,value,*args,**kwargs):return dump(intermediate if Path(path).resolve()==final.resolve() else path,value,*args,**kwargs)
    proxy.dump=routed_dump
    source_code=ns.ROOT/'analysis'/parent_filename(graph)
    namespace={'__file__':str(source_code),'__name__':'actual_complete169_then_cross120',
        'STOCK_RANK10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT':tail_stage}
    exec(compile(prepared_parent(source_code.read_text(encoding='utf8')),str(source_code),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[r for r in calls if r['rows']==1599600];cold=[r for r in calls if r['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    assert all(r['native_reload_independent_tensor_forward_and_Pandas_tail_bits_exact'] for r in calls)
    existing=[k for k,m in result['models'].items() if m['sha256']==component['sha256']];assert len(existing)<=1
    before=len(result['models'])
    if existing:
        physical_key=existing[0]
        assert ns.sha(result['models'][physical_key]['path'])==component['sha256']
        reused={'existing_physical_model_key':physical_key,'sha256':component['sha256'],'additional_physical_models':0}
    else:
        physical_key='stock_rank120medium_embedding_after_qualified_parent_'+component['name'];assert physical_key not in result['models']
        result['models'][physical_key]=component
        storage.append({'key':physical_key,'source':str(source),'target':str(target),'sha256':component['sha256'],'samefile':os.path.samefile(source,target)})
        for field,report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
            control=deepcopy(report['controls'][0]);control['name']=physical_key;result[field].append(control)
        reused={'existing_physical_model_key':None,'sha256':component['sha256'],'additional_physical_models':1}
    count=before+reused['additional_physical_models']
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==count
    assert len({m['sha256'] for m in result['models'].values()})==count
    result.update(actual_entire_qualified_parent_then_stock_rank120medium_embedding_native_independent_replays=True,protected_tail_stage_calls=calls,
        protected_tail_physical_leaf_reuse=reused,complete_qualified_parent_all_original_graph_branches_preserved=True)
    dump(final,result,immutable=True)
    dump(candidate/'stock_rank120medium_embedding_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete_qualified_parent_stock_rank120medium_embedding_two_full_native_independent_replays_and_cold80',
        'calls':calls,'actual_saved_model_count':count,'actual_native_model_storage':storage,'physical_leaf_reuse':reused,
        'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
