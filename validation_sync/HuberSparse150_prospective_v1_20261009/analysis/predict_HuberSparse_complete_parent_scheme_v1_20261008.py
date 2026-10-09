"""Append fixed Huber cross-family heads after the entire qualified parent graph."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os

BACKENDS={
    'ReverseBF16':('predict_BF16_reverse_complete_parent_scheme_v1_20261008.py','BF16_reverse_complete_parent_native_stage_v1_20261008',False),
    'Huber':('predict_HuberIRLS64_complete_parent_scheme_v3_20261008.py','HuberIRLS64_complete_parent_native_stage_v3_20261008',True),
    'CrossFamily':('predict_CrossFamily_complete_parent_scheme_v2_20261008.py','CrossFamily_complete_parent_native_stage_v2_20261008',True),
    'BF16':('predict_BF16_complete_parent_rank_scheme_v1_20261008.py','BF16_complete_parent_native_stage_v1_20261008',False),
    'ReverseBayes':('predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py','nonflag_residual_ReverseBayes64_native_stage_20261007',True)}


def backend_for(graph):
    for key,name in (('BF16_reverse_complete_parent_rank_CDF','ReverseBF16'),
        ('nonflag_CPU_HuberIRLS64_complete_parent_CDF','Huber'),
        ('nonflag_CPU_CrossFamily_complete_parent_CDF','CrossFamily'),
        ('BF16_complete_parent_rank_CDF','BF16')):
        if key in graph:return name
    assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph
    return 'ReverseBayes'


def prepared_backend(text,backend):
    filename,module,has_teacher=BACKENDS[backend]
    suffix=',GRAPH_KEY' if backend!='ReverseBayes' else ''
    needle=f'    from {module} import after_parent{suffix}';assert text.count(needle)==1
    replacement=f'    from {module} import after_parent as COMPLETE_PARENT_AFTER{suffix}'
    if has_teacher:
        replacement+='''
    def after_parent(ns,context,teacher,parent,spec,components):
        value,report=COMPLETE_PARENT_AFTER(ns,context,teacher,parent,spec,components)
        return HUBER_CROSS_AFTER_COMPLETE_PARENT(context,value,teacher),report'''
    else:
        replacement+='''
    def after_parent(ns,context,parent,spec,component):
        value,report=COMPLETE_PARENT_AFTER(ns,context,parent,spec,component)
        return HUBER_CROSS_AFTER_COMPLETE_PARENT(context,value,None),report'''
    return text.replace(needle,replacement)


def teacher_capture(original):
    def captured(ns,context,teacher,parent,spec,components):
        context._HuberSparse_teacher106=teacher
        return original(ns,context,teacher,parent,spec,components)
    return captured


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    import numpy as np
    import nonflag_residual_ReverseBayes64_native_stage_20261007 as signed_stage
    from HuberSparse_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY
    graph=record['winner'][ns.GRAPH_FIELD];assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph
    spec=deepcopy(graph[GRAPH_KEY]);components=deepcopy(spec['ordered_native_components'])
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    for component in components:
        for source_field,target_field,digest_field,suffix in (
            ('source_path','path','sha256','.joblib'),
            ('independent_state_source_path','independent_state_path','independent_state_sha256','.json')):
            source=Path(component[source_field]);target=candidate/(component['name']+suffix)
            assert ns.sha(source)==component[digest_field]
            if not target.exists():
                if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
                else:
                    import shutil
                    with source.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst,1024**2)
            assert ns.sha(target)==component[digest_field];component[target_field]=str(target)
    calls=[]
    def cross_stage(context,parent,passed_teacher):
        teacher=context._HuberSparse_teacher106
        if passed_teacher is not None:
            assert np.array_equal(np.asarray(passed_teacher).view('u8'),np.asarray(teacher).view('u8'))
        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value
    backend=backend_for(graph);filename,module,has_teacher=BACKENDS[backend]
    source_code=ns.ROOT/'analysis'/filename;text=prepared_backend(source_code.read_text(encoding='utf8'),backend)
    final=candidate/'verification.json';intermediate=candidate/'complete_parent_route_before_HuberSparse_report.json'
    original_read,original_dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:original_read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,data,*args,**kwargs):return original_dump(intermediate if Path(path).resolve()==final.resolve() else path,data,*args,**kwargs)
    proxy.dump=routed_dump
    namespace={'__file__':str(source_code),'__name__':'actual_complete_parent_then_HuberSparse',
        'HUBER_CROSS_AFTER_COMPLETE_PARENT':cross_stage}
    exec(compile(text,str(source_code),'exec'),namespace)
    original_signed=signed_stage.after_parent
    # Only this isolated candidate worker changes its imported function reference; restore even on failure.
    signed_stage.after_parent=teacher_capture(original_signed)
    try:result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    finally:signed_stage.after_parent=original_signed
    assert signed_stage.after_parent is original_signed
    full=[row for row in calls if row['rows']==1599600];cold=[row for row in calls if row['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    assert all(row['native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact'] for row in calls)
    before=len(result['models']);new_heads=[];reused_heads=[]
    for component in components:
        existing=[key for key,value in result['models'].items() if value['sha256']==component['sha256']]
        assert len(existing)<=1
        if existing:
            reused_heads.append({'head':component['head'],'existing_model_key':existing[0],'sha256':component['sha256'],'additional_physical_models':0})
            continue
        key='HuberSparse_'+component['head'];assert key not in result['models'];result['models'][key]=component
        storage.append({'key':key,'source':component['source_path'],'target':component['path'],'sha256':component['sha256'],
            'samefile':os.path.samefile(component['source_path'],component['path'])})
        for field,source_report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
            control=deepcopy(next(row for row in source_report['controls'] if row['head']==component['head']));control['name']=key
            result[field].append(control)
        new_heads.append(component['head'])
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==before+len(new_heads)
    assert len({value['sha256'] for value in result['models'].values()})==len(result['models'])
    result.update(actual_complete_parent_then_HuberSparse_native_and_independent_CDF_replay=True,
        HuberSparse_stage_calls=calls,HuberSparse_reused_physical_heads=reused_heads,
        HuberSparse_new_physical_heads=new_heads,complete_signed_Bayes_BF16_Cross_Huber_reverse_BF16_parent_preserved=True,
        original_teacher106_capture_restored_after_worker_inference=True)
    original_dump(final,result,immutable=True)
    original_dump(candidate/'HuberSparse_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete_parent_and_HuberSparse_two_full_native_independent_replays_and_cold80',
        'calls':calls,'actual_saved_model_count':len(result['models']),'original_parent_backend':backend,
        'actual_native_model_storage':storage,'new_physical_heads':new_heads,'reused_physical_heads':reused_heads,
        'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
