"""Execute complete183, replay both physical seed bundles, then apply the frozen joint codec."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os,importlib,shutil
from predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v2_20261011 import parent_filename

def prepared_parent(text):
    candidates=['\n        value,report=after_parent(ns,context,parent,spec,component);calls.append(report);return value',
        '\n        value,report=after_parent(ns,context,parent,spec,components);calls.append(report);return value']
    matches=[needle for needle in candidates if text.count(needle)==1];assert len(matches)==1
    needle=matches[0]
    return text.replace(needle,needle.replace('return value','return RANK120_RANK60_PROTECTED_AFTER_WHOLE_QUALIFIED_PARENT(context,value)'))

def predict(ns,record,candidate,parent_curve_source,mapping_path):
    import rank120_rank60_consensus_after_qualified183_native_stage81_v1_20261011 as cdf
    graph=record['winner'][ns.GRAPH_FIELD]
    keys=[s.GRAPH_KEY for s in (cdf,) if s.GRAPH_KEY in graph];assert len(keys)==1
    key=keys[0];stage=cdf;spec=deepcopy(graph[key])
    assert spec['original_complete_parent_round']==183
    assert 'BF16_flag_after152157_complete_parent_rank_CDF' in graph
    assert spec['recipe']==stage.RECIPE and spec['disagreement_penalty'] in (.5,.75,1.,2.)
    component=deepcopy(spec['native_component']);members=component['horizon_components']
    assert len(members)==2 and len({m['sha256'] for m in members})==2
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    bindings=[]
    for i,member in enumerate(members):
        assert member['configuration']['seed']==20261009
        assert member['configuration']['label_horizon_trading_days']==(60,120)[i]
        source=Path(member['source_path']);target=candidate/(member['name']+'_final2025.joblib')
        assert ns.sha(source)==member['sha256']
        if not target.exists():
            if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
            else:
                with source.open('rb') as reader,target.open('xb') as writer:shutil.copyfileobj(reader,writer,4*1024**2)
        assert ns.sha(target)==member['sha256'];member['path']=str(target);bindings.append((source,target))
    calls=[]
    def after_whole(context,parent):
        value,report=stage.after_parent(ns,context,parent,spec,component);calls.append(report);return value
    final=candidate/'verification.json';intermediate=candidate/'whole_qualified_parent_before_rank60_rank20_mixed.json'
    read,dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,value,*args,**kwargs):
        return dump(intermediate if Path(path).resolve()==final.resolve() else path,value,*args,**kwargs)
    proxy.dump=routed_dump
    source_code=ns.ROOT/'analysis'/parent_filename(graph)
    namespace={'__file__':str(source_code),'__name__':'actual_complete183_then_mixed_horizon',
        'RANK120_RANK60_PROTECTED_AFTER_WHOLE_QUALIFIED_PARENT':after_whole}
    exec(compile(prepared_parent(source_code.read_text(encoding='utf8')),str(source_code),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[r for r in calls if r['rows']==1599600];cold=[r for r in calls if r['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    assert all(r['native_reload_two_independent_decoders_scalar_mix_and_Pandas_protected_tail_bits_exact'] for r in calls)
    assert all(len(r['controls'])==2 for r in calls)
    before=len(result['models']);reused=[]
    for i,member in enumerate(members):
        source,target=bindings[i]
        existing=[k for k,m in result['models'].items() if m['sha256']==member['sha256']];assert len(existing)<=1
        if existing:
            physical_key=existing[0];assert ns.sha(result['models'][physical_key]['path'])==member['sha256']
            reused.append({'existing_physical_model_key':physical_key,'sha256':member['sha256'],'additional_physical_models':0})
        else:
            physical_key='rank120_rank60_protected_after_qualified_parent_'+member['name'];assert physical_key not in result['models']
            result['models'][physical_key]=member
            storage.append({'key':physical_key,'source':str(source),'target':str(target),'sha256':member['sha256'],'samefile':os.path.samefile(source,target)})
            for field,report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
                control=deepcopy(report['controls'][i]);assert control['sha256']==member['sha256'];control['name']=physical_key;result[field].append(control)
            reused.append({'existing_physical_model_key':None,'sha256':member['sha256'],'additional_physical_models':1})
    count=before+sum(r['additional_physical_models'] for r in reused)
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==count
    assert len({m['sha256'] for m in result['models'].values()})==count
    result.update(actual_entire_qualified_parent_then_mixed_horizon_native_independent_replays=True,
        mixed_horizon_stage_calls=calls,mixed_horizon_physical_leaf_reuse=reused,complete_qualified_parent_all_original_graph_branches_preserved=True)
    dump(final,result,immutable=True)
    dump(candidate/'rank120_rank60_protected_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete183_mixed_horizon_two_full_native_independent_scalar_mix_and_cold80',
        'calls':calls,'actual_saved_model_count':count,'actual_native_model_storage':storage,'physical_leaf_reuse':reused,
        'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
