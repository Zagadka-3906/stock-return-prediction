"""Append reverse neural CDF after the entire signed/BF16/Cross/Huber parent graph."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os

BACKENDS={
    'Huber':('predict_HuberIRLS64_complete_parent_scheme_v3_20261008.py','HuberIRLS64_complete_parent_native_stage_v3_20261008',True),
    'CrossFamily':('predict_CrossFamily_complete_parent_scheme_v2_20261008.py','CrossFamily_complete_parent_native_stage_v2_20261008',True),
    'BF16':('predict_BF16_complete_parent_rank_scheme_v1_20261008.py','BF16_complete_parent_native_stage_v1_20261008',False),
    'ReverseBayes':('predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py','nonflag_residual_ReverseBayes64_native_stage_20261007',True)}


def prepared_backend(text,backend):
    filename,module,has_teacher=BACKENDS[backend]
    suffix=',GRAPH_KEY' if backend!='ReverseBayes' else ''
    needle=f'    from {module} import after_parent{suffix}';assert text.count(needle)==1
    replacement=f'    from {module} import after_parent as COMPLETE_PARENT_AFTER{suffix}'
    if has_teacher:
        replacement+='''
    def after_parent(ns,context,teacher,parent,spec,components):
        value,report=COMPLETE_PARENT_AFTER(ns,context,teacher,parent,spec,components)
        return REVERSE_BF16_AFTER_COMPLETE_PARENT(context,value),report'''
    else:
        replacement+='''
    def after_parent(ns,context,parent,spec,component):
        value,report=COMPLETE_PARENT_AFTER(ns,context,parent,spec,component)
        return REVERSE_BF16_AFTER_COMPLETE_PARENT(context,value),report'''
    return text.replace(needle,replacement)


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    import numpy as np
    from BF16_reverse_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY
    graph=record['winner'][ns.GRAPH_FIELD];assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph
    spec=deepcopy(graph[GRAPH_KEY]);component=deepcopy(spec['native_component'])
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    source=Path(component['source_path']);target=candidate/(component['name']+'_final2025.joblib')
    assert ns.sha(source)==component['sha256']
    if not target.exists():
        if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
        else:
            import shutil
            with source.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst,1024**2)
    assert ns.sha(target)==component['sha256'];component['path']=str(target)
    calls=[]
    def reverse_stage(context,parent):
        names=context._nonflag_raw_feature_names;features=np.ascontiguousarray(context._nonflag_raw_features,dtype=np.float32)
        assert len(names)==63 and features.shape==(len(parent),63)
        if hasattr(context,'_BF16_raw_features'):
            assert context._BF16_feature_names==names
            assert np.array_equal(context._BF16_raw_features.view('u4'),features.view('u4'))
        context._BF16_raw_features=features;context._BF16_feature_names=names
        value,report=after_parent(ns,context,parent,spec,component);calls.append(report);return value
    if 'nonflag_CPU_HuberIRLS64_complete_parent_CDF' in graph:backend='Huber'
    elif 'nonflag_CPU_CrossFamily_complete_parent_CDF' in graph:backend='CrossFamily'
    elif 'BF16_complete_parent_rank_CDF' in graph:backend='BF16'
    else:backend='ReverseBayes'
    filename,module,has_teacher=BACKENDS[backend];source_code=ns.ROOT/'analysis'/filename
    text=prepared_backend(source_code.read_text(encoding='utf8'),backend)
    final=candidate/'verification.json';intermediate=candidate/'complete_parent_route_before_reverse_BF16_report.json'
    original_read,original_dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:original_read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,data,*args,**kwargs):return original_dump(intermediate if Path(path).resolve()==final.resolve() else path,data,*args,**kwargs)
    proxy.dump=routed_dump
    namespace={'__file__':str(source_code),'__name__':'actual_complete_parent_then_reverse_BF16',
        'REVERSE_BF16_AFTER_COMPLETE_PARENT':reverse_stage}
    exec(compile(text,str(source_code),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[row for row in calls if row['rows']==1599600];cold=[row for row in calls if row['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    assert all(row['native_reload_independent_tensor_forward_and_Pandas_CDF_bits_exact'] for row in calls)
    before=len(result['models']);existing=[key for key,value in result['models'].items() if value['sha256']==component['sha256']]
    assert len(existing)<=1
    if existing:
        added=0;reuse={'existing_model_key':existing[0],'sha256':component['sha256'],'additional_physical_models':0}
    else:
        added=1;reuse=None;key='BF16_reverse_wide_full_'+component['name'];assert key not in result['models']
        result['models'][key]=component
        storage.append({'key':key,'source':str(source),'target':str(target),'sha256':component['sha256'],
            'samefile':os.path.samefile(source,target)})
        for field,report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
            control=deepcopy(report['controls'][0]);control['name']=key;result[field].append(control)
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==before+added
    assert len({model['sha256'] for model in result['models'].values()})==len(result['models'])
    result.update(actual_complete_parent_then_reverse_BF16_full_native_independent_CDF_replay=True,
        reverse_BF16_stage_calls=calls,reverse_BF16_physical_model_reuse=reuse,
        complete_signed_Bayes_optional_BF16_CrossFamily_and_Huber_parent_preserved=True)
    original_dump(final,result,immutable=True)
    original_dump(candidate/'BF16_reverse_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete_parent_and_reverse_BF16_two_full_native_independent_replays_and_cold80',
        'calls':calls,'actual_saved_model_count':len(result['models']),'original_parent_backend':backend,
        'actual_native_model_storage':storage,'additional_unique_physical_models':added,'model_reuse':reuse,
        'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
