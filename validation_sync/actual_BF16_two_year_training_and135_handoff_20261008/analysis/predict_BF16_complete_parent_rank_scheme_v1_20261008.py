"""Retain the complete signed-Bayes parent replay and append a real wide-neural rank-CDF stage."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    import numpy as np
    from run import to_matrix
    from BF16_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    graph=record['winner'][ns.GRAPH_FIELD]
    assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in graph
    spec=deepcopy(graph[GRAPH_KEY]);component=deepcopy(spec['native_component'])
    source=Path(component['source_path']);target=candidate/(component['name']+'_final2025.joblib')
    assert ns.sha(source)==component['sha256']
    if not target.exists():
        if source.resolve().drive.upper()==target.parent.resolve().drive.upper():os.link(source,target)
        else:
            import shutil
            shutil.copyfile(source,target)
    assert ns.sha(target)==component['sha256'];component['path']=str(target)
    calls=[]
    source_code=ns.ROOT/'analysis/predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py'
    text=source_code.read_text(encoding='utf8')
    needle='        context._nonflag_raw_features=test.select(names).to_numpy().astype(np.float64);context._nonflag_raw_feature_names=names'
    assert text.count(needle)==1
    text=text.replace(needle,needle+'\n        context._BF16_raw_features=BF16_MATRIX(test,names);context._BF16_feature_names=names')
    needle='        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value'
    assert text.count(needle)==1
    replacement='        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report)\n' \
        '        value,wide_report=BF16_AFTER_COMPLETE_PARENT(context,value)\n' \
        '        BF16_CALLS.append(wide_report)\n' \
        '        return value'
    text=text.replace(needle,replacement)
    original_read,original_dump=ns.read,ns.dump
    final=candidate/'verification.json';intermediate=candidate/'complete_signed_Bayes_parent_route_before_BF16_report.json'
    proxy=SimpleNamespace(**vars(ns))
    proxy.read=lambda path:original_read(intermediate if Path(path).resolve()==final.resolve() else path)
    def routed_dump(path,data,*args,**kwargs):
        return original_dump(intermediate if Path(path).resolve()==final.resolve() else path,data,*args,**kwargs)
    proxy.dump=routed_dump
    def neural_stage(context,parent):return after_parent(ns,context,parent,spec,component)
    namespace={'__file__':str(source_code),'__name__':'actual_complete_parent_then_BF16_rank_CDF',
               'BF16_MATRIX':to_matrix,'BF16_AFTER_COMPLETE_PARENT':neural_stage,'BF16_CALLS':calls}
    exec(compile(text,str(source_code),'exec'),namespace)
    result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    full=[item for item in calls if item['rows']==1599600]
    cold=[item for item in calls if item['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    assert all(item['native_reload_independent_tensor_forward_and_Pandas_CDF_bits_exact'] for item in calls)
    before=len(result['models']);key='BF16_wide_full_'+component['name']
    result['models'][key]=component
    storage.append({'key':key,'source':str(source),'target':str(target),'sha256':component['sha256'],
                    'samefile':os.path.samefile(source,target)})
    result['actual_model_reload_controls'].extend(full[0]['controls'])
    result['actual80_day_prefix_model_controls'].extend(cold[0]['controls'])
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])==before+1
    result.update(actual_complete_parent_then_BF16_full_native_independent_tensor_CDF_replay=True,
                  BF16_stage_calls=calls,original_parent_checks_before_BF16_stage_preserved=True)
    original_dump(final,result,immutable=True)
    original_dump(candidate/'BF16_complete_parent_native_replay_verification.json',{
        'status':'passed_actual_complete_parent_and_BF16_two_full_native_independent_replays_and_cold80',
        'calls':calls,'actual_saved_model_count':len(result['models']),
        'original_complete_parent_backend':'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007',
        'actual_native_model_storage':storage,'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage

