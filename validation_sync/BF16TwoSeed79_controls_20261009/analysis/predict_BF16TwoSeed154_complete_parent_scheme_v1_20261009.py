"""Execute the complete148 predictor before the frozen equal-weight two-seed neural stage."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os,shutil
PARENT_FILENAME='predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008.py'
def prepared_parent148(text):
    needle='        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value'
    assert text.count(needle)==1
    return text.replace(needle,'        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return TWO_SEED_AFTER_COMPLETE148(context,value)')
def predict(ns,record,candidate,parent_curve_source,mapping_path):
    import numpy as np
    from BF16TwoSeed154_complete_parent_native_stage_v1_20261009 import after_parent,GRAPH_KEY,NAMES
    graph=record['winner'][ns.GRAPH_FIELD];assert 'nonflag_CPU_joint_Cross_Huber_adaptive_complete_parent_CDF' in graph
    spec=deepcopy(graph[GRAPH_KEY]);assert spec['original_complete_parent_round']==148
    components=deepcopy(spec['native_components']);assert [c['name'] for c in components]==list(NAMES)
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True);copies=[]
    for component in components:
        source=Path(component['source_path']);target=candidate/(component['name']+'_final2025.joblib')
        assert ns.sha(source)==component['sha256']
        if not target.exists():
            if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
            else:
                with source.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst,4*1024**2)
        assert ns.sha(target)==component['sha256'];component['path']=str(target);copies.append((source,target))
    calls=[]
    def two_seed_stage(context,parent):
        if not hasattr(context,'_BF16_raw_features'):
            context._BF16_raw_features=np.ascontiguousarray(context._nonflag_raw_features,dtype=np.float32)
            context._BF16_feature_names=context._nonflag_raw_feature_names
        value,report=after_parent(ns,context,parent,spec,components);calls.append(report);return value
    final=candidate/'verification.json';intermediate=candidate/'complete148_before_BF16TwoSeed154_report.json'
    read,dump=ns.read,ns.dump;proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:read(intermediate if Path(path).resolve()==final.resolve() else path)
    proxy.dump=lambda path,value,*args,**kwargs:dump(intermediate if Path(path).resolve()==final.resolve() else path,value,*args,**kwargs)
    source_code=ns.ROOT/'analysis'/PARENT_FILENAME
    namespace={'__file__':str(source_code),'__name__':'actual_complete148_then_two_seed154','TWO_SEED_AFTER_COMPLETE148':two_seed_stage}
    exec(compile(prepared_parent148(source_code.read_text(encoding='utf8')),str(source_code),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[r for r in calls if r['rows']==1599600];cold=[r for r in calls if r['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    assert all(r['native_reload_independent_tensor_forward_and_Pandas_CDF_bits_exact'] and r['two_seed_equal_mean_and_Pandas_arithmetic_bits_exact'] for r in calls)
    before=len(result['models']);existing={r['sha256'] for r in result['models'].values()}
    assert len({c['sha256'] for c in components})==2 and not existing.intersection(c['sha256'] for c in components)
    for i,(component,(source,target)) in enumerate(zip(components,copies)):
        key='BF16_two_seed_full_'+component['name'];assert key not in result['models'];result['models'][key]=component
        storage.append({'key':key,'source':str(source),'target':str(target),'sha256':component['sha256'],'samefile':os.path.samefile(source,target)})
        for field,report in (('actual_model_reload_controls',full[0]),('actual80_day_prefix_model_controls',cold[0])):
            control=deepcopy(report['controls'][i]);control['name']=key;result[field].append(control)
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==before+2
    assert len({r['sha256'] for r in result['models'].values()})==len(result['models'])
    result.update(actual_entire148_then_BF16TwoSeed154_native_independent_replays=True,BF16TwoSeed154_stage_calls=calls,
        complete148_all_original_branches_and_JointCrossHuber_parameters_preserved=True)
    dump(final,result,immutable=True)
    dump(candidate/'BF16TwoSeed154_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete148_and_two_seed154_two_full_native_independent_replays_and_cold80',
        'calls':calls,'actual_saved_model_count':len(result['models']),'actual_native_model_storage':storage,'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
