"""Preserve the signed-Bayes and optional BF16 parent, append cross-family native CDF inference."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os


def prepared_parent_source(text):
    needle='    def stage(context,teacher,parent):\n'
    assert text.count(needle)==1
    return text.replace(needle,needle+'        context._CrossFamily_teacher106=teacher\n')


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    import numpy as np
    from CrossFamily_complete_parent_native_stage_v1_20261008 import after_parent as PARENT_CROSS_AFTER,GRAPH_KEY
    def after_parent(ns,context,teacher,parent,spec,components):
        value,report=PARENT_CROSS_AFTER(ns,context,teacher,parent,spec,components)
        return HUBER_AFTER_COMPLETE_PARENT(context,teacher,value),report
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    graph=record['winner'][ns.GRAPH_FIELD]
    assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph
    spec=deepcopy(graph[GRAPH_KEY]);components=deepcopy(spec['ordered_native_components'])
    for component in components:
        for source_field,target_field,digest_field,suffix in (
            ('source_path','path','sha256','.joblib'),
            ('independent_state_source_path','independent_state_path','independent_state_sha256','.json')):
            source=Path(component[source_field]);target=candidate/(component['name']+suffix)
            assert ns.sha(source)==component[digest_field]
            if not target.exists():
                if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
                else:
                    with source.open('rb') as src,target.open('xb') as dst:
                        import shutil
                        shutil.copyfileobj(src,dst,1024**2)
            assert ns.sha(target)==component[digest_field];component[target_field]=str(target)
    calls=[]
    def cross_stage(context,teacher,parent):
        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value
    bf16='BF16_complete_parent_rank_CDF' in graph
    source=ns.ROOT/'analysis'/('predict_BF16_complete_parent_rank_scheme_v1_20261008.py' if bf16 else 'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py')
    text=source.read_text(encoding='utf8')
    if bf16:
        needle="    text=source_code.read_text(encoding='utf8')";assert text.count(needle)==1
        text=text.replace(needle,needle+'\n    text=PREPARE_SIGNED_PARENT_SOURCE(text)')
        needle='    def neural_stage(context,parent):return after_parent(ns,context,parent,spec,component)';assert text.count(needle)==1
        text=text.replace(needle,'    def neural_stage(context,parent):\n        value,report=after_parent(ns,context,parent,spec,component)\n        value=CROSS_AFTER_COMPLETE_PARENT(context,context._CrossFamily_teacher106,value)\n        return value,report')
    else:
        text=prepared_parent_source(text)
        needle='        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value';assert text.count(needle)==1
        text=text.replace(needle,'        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report)\n        return CROSS_AFTER_COMPLETE_PARENT(context,teacher,value)')
    final=candidate/'verification.json';intermediate=candidate/'complete_parent_route_before_CrossFamily_report.json'
    original_read,original_dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:original_read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,data,*args,**kwargs):return original_dump(intermediate if Path(path).resolve()==final.resolve() else path,data,*args,**kwargs)
    proxy.dump=routed_dump
    namespace={'__file__':str(source),'__name__':'actual_complete_parent_then_CrossFamily',
        'PREPARE_SIGNED_PARENT_SOURCE':prepared_parent_source,'CROSS_AFTER_COMPLETE_PARENT':cross_stage}
    exec(compile(text,str(source),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[row for row in calls if row['rows']==1599600];cold=[row for row in calls if row['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    assert all(row['native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact'] for row in calls)
    before=len(result['models']);new_heads=[];reused_heads=[]
    for component in components:
        existing=[key for key,value in result['models'].items() if value['sha256']==component['sha256']]
        if existing:
            assert len(existing)==1
            reused_heads.append({'head':component['head'],'existing_model_key':existing[0],'sha256':component['sha256'],'additional_physical_models':0})
            continue
        key='crossfamily_'+component['head'];assert key not in result['models']
        result['models'][key]=component
        storage.append({'key':key,'source':component['source_path'],'target':component['path'],'sha256':component['sha256'],'samefile':os.path.samefile(component['source_path'],component['path'])})
        for field,source_report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
            control=deepcopy(next(row for row in source_report['controls'] if row['head']==component['head']));control['name']=key
            result[field].append(control)
        new_heads.append(component['head'])
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==before+len(new_heads)
    result.update(actual_complete_parent_then_CrossFamily_native_and_independent_CDF_replay=True,
        CrossFamily_stage_calls=calls,CrossFamily_reused_physical_heads=reused_heads,CrossFamily_new_physical_heads=new_heads,
        all_original_parent_and_optional_BF16_checks_preserved=True)
    original_dump(final,result,immutable=True)
    original_dump(candidate/'CrossFamily_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete_parent_and_CrossFamily_two_full_native_independent_replays_and_cold80',
        'calls':calls,'actual_saved_model_count':len(result['models']),'original_parent_backend':source.name,
        'parent_has_BF16_stage':bf16,'new_physical_heads':new_heads,'reused_physical_heads':reused_heads,
        'actual_native_model_storage':storage,'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
