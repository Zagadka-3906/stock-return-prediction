"""Keep complete signed-Bayes, optional BF16 and CrossFamily stages, then append Huber."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os


def prepared_signed_parent(text):
    needle='    def stage(context,teacher,parent):\n';assert text.count(needle)==1
    return text.replace(needle,needle+'        context._HuberIRLS64_teacher106=teacher\n')


def prepared_backend(text,backend):
    if backend=='CrossFamily':
        needle='    from CrossFamily_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY'
        assert text.count(needle)==1
        replacement=needle.replace('after_parent,GRAPH_KEY','after_parent as PARENT_CROSS_AFTER,GRAPH_KEY')+"""
    def after_parent(ns,context,teacher,parent,spec,components):
        value,report=PARENT_CROSS_AFTER(ns,context,teacher,parent,spec,components)
        return HUBER_AFTER_COMPLETE_PARENT(context,teacher,value),report"""
        return text.replace(needle,replacement)
    if backend=='BF16':
        needle="    text=source_code.read_text(encoding='utf8')";assert text.count(needle)==1
        text=text.replace(needle,needle+'\n    text=PREPARE_SIGNED_PARENT_SOURCE(text)')
        needle='    def neural_stage(context,parent):return after_parent(ns,context,parent,spec,component)';assert text.count(needle)==1
        return text.replace(needle,"""    def neural_stage(context,parent):
        value,report=after_parent(ns,context,parent,spec,component)
        return HUBER_AFTER_COMPLETE_PARENT(context,context._HuberIRLS64_teacher106,value),report""")
    assert backend=='ReverseBayes'
    text=prepared_signed_parent(text)
    needle='        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value';assert text.count(needle)==1
    return text.replace(needle,"""        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report)
        return HUBER_AFTER_COMPLETE_PARENT(context,teacher,value)""")


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    from HuberIRLS64_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY
    graph=record['winner'][ns.GRAPH_FIELD];assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph
    spec=deepcopy(graph[GRAPH_KEY]);components=deepcopy(spec['ordered_native_components'])
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    for component in components:
        for source_field,target_field,digest_field,suffix in (
            ('source_path','path','sha256','.joblib'),('independent_state_source_path','independent_state_path','independent_state_sha256','.json')):
            source=Path(component[source_field]);target=candidate/(component['name']+suffix)
            assert ns.sha(source)==component[digest_field]
            if not target.exists():
                if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
                else:
                    import shutil
                    with source.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst,1024**2)
            assert ns.sha(target)==component[digest_field];component[target_field]=str(target)
    calls=[]
    def huber_stage(context,teacher,parent):
        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value
    if 'nonflag_CPU_CrossFamily_complete_parent_CDF' in graph:
        backend='CrossFamily';filename='predict_CrossFamily_complete_parent_scheme_v1_20261008.py'
    elif 'BF16_complete_parent_rank_CDF' in graph:
        backend='BF16';filename='predict_BF16_complete_parent_rank_scheme_v1_20261008.py'
    else:backend='ReverseBayes';filename='predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py'
    source=ns.ROOT/'analysis'/filename;text=prepared_backend(source.read_text(encoding='utf8'),backend)
    final=candidate/'verification.json';intermediate=candidate/'complete_parent_route_before_HuberIRLS64_report.json'
    original_read,original_dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:original_read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,data,*args,**kwargs):return original_dump(intermediate if Path(path).resolve()==final.resolve() else path,data,*args,**kwargs)
    proxy.dump=routed_dump
    namespace={'__file__':str(source),'__name__':'actual_complete_parent_then_HuberIRLS64',
        'PREPARE_SIGNED_PARENT_SOURCE':prepared_signed_parent,'HUBER_AFTER_COMPLETE_PARENT':huber_stage}
    exec(compile(text,str(source),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[item for item in calls if item['rows']==1599600];cold=[item for item in calls if item['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1 and all(item['native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact'] for item in calls)
    before=len(result['models']);added=[];reused=[]
    for component in components:
        existing=[key for key,value in result['models'].items() if value['sha256']==component['sha256']]
        if existing:
            assert len(existing)==1;reused.append({'head':component['head'],'existing_model_key':existing[0],'sha256':component['sha256']});continue
        key='HuberIRLS64_'+component['head'];assert key not in result['models'];result['models'][key]=component
        storage.append({'key':key,'source':component['source_path'],'target':component['path'],'sha256':component['sha256'],
            'samefile':os.path.samefile(component['source_path'],component['path'])})
        for field,report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
            control=deepcopy(next(item for item in report['controls'] if item['head']==component['head']));control['name']=key;result[field].append(control)
        added.append(component['head'])
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==before+len(added)
    result.update(actual_complete_parent_then_HuberIRLS64_native_and_independent_CDF_replay=True,
        HuberIRLS64_stage_calls=calls,HuberIRLS64_new_physical_heads=added,HuberIRLS64_reused_physical_heads=reused,
        complete_parent_signed_Bayes_and_optional_BF16_and_CrossFamily_preserved=True)
    original_dump(final,result,immutable=True)
    original_dump(candidate/'HuberIRLS64_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete_parent_and_HuberIRLS64_two_full_native_independent_replays_and_cold80',
        'calls':calls,'actual_saved_model_count':len(result['models']),'original_parent_backend':backend,
        'new_physical_heads':added,'reused_physical_heads':reused,'actual_native_model_storage':storage,
        'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
