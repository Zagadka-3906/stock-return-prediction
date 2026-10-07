"""Replay complete parent106/flag native graph then nonflag residuals, preserving all checks."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import os
def predict(ns,record,candidate,parent_curve_source,mapping_path):
    import numpy as np
    import whole_scheme_future_runtime_20261004 as runtime
    from nonflag_residual_ReverseBayes64_native_stage_20261007 import after_parent
    candidate=Path(candidate);candidate.mkdir(parents=True,exist_ok=True)
    graph=record['winner'][ns.GRAPH_FIELD];spec=graph['nonflag_CPU_ReverseBayes64_residual_CDF'];components=deepcopy(spec['native_components'])
    assert 'protected_upper_pool_CPU_HGB_CDF' not in graph,'This selected parent must preserve the qualified106 nonflag teacher graph'
    for c in components:
        for src,dst,digest,suffix in [('source_path','path','sha256','.joblib'),('independent_state_source_path','independent_state_path','independent_state_sha256','.json')]:
            source=Path(c[src]);target=candidate/(c['name']+suffix);assert ns.sha(source)==c[digest]
            if not target.exists():
                if source.drive.upper()==target.drive.upper():os.link(source,target)
                else:
                    import shutil
                    shutil.copyfile(source,target)
            assert ns.sha(target)==c[digest];c[dst]=str(target)
    calls=[];original_build=runtime.build_context
    def build(graph,inputs,test,*args,**kwargs):
        context,checks=original_build(graph,inputs,test,*args,**kwargs)
        assert test.select(['ts_code','trade_date']).equals(inputs.select(['ts_code','trade_date'])) and not {'y_ret_1d','y_rank'}&set(test.columns)
        names=list(test.columns[2:]);assert len(names)==63
        context._nonflag_raw_features=test.select(names).to_numpy().astype(np.float64);context._nonflag_raw_feature_names=names
        return context,checks
    def stage(context,teacher,parent):
        value,report=after_parent(ns,context,teacher,parent,spec,components);calls.append(report);return value
    if 'conditional_flag_CPU_HGB_residual_CDF' in graph:
        flag=graph['conditional_flag_CPU_HGB_residual_CDF']
        if 'ordered_quarter_counts' in flag:module='predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007'
        elif all(c['training_info']['parameters']['loss']=='quantile' for c in flag['native_components']):module='predict_quantile_HGB_residual_CDF_scheme_v2_20261007'
        else:module='predict_conditional_CPU_HGB_residual_CDF_scheme_20261007'
        source=ns.ROOT/'analysis'/f'{module}.py';text=source.read_text(encoding='utf8')
        needle="    text = text.replace(needle, '        values = CPU_HGB_AFTER_PARENT(context, values)\\n' + needle)"
        assert text.count(needle)==1
        replacement="""    text = text.replace(needle, '        nonflag_teacher106 = values\\n        values = CPU_HGB_AFTER_PARENT(context, values)\\n' + needle)
    assert text.count('        return values\\n') == 1
    text = text.replace('        return values\\n', '        values = NONFLAG_AFTER_PARENT(context, nonflag_teacher106, values)\\n        return values\\n')"""
        text=text.replace(needle,replacement)
        needle="'CPU_HGB_AFTER_PARENT': after_parent}";assert text.count(needle)==1
        text=text.replace(needle,"'CPU_HGB_AFTER_PARENT': after_parent, 'NONFLAG_AFTER_PARENT': NONFLAG_AFTER_PARENT}")
    else:
        module='predict_simplex_residual47_native_scheme_20261006';source=ns.ROOT/'analysis'/f'{module}.py';text=source.read_text(encoding='utf8')
        needle='        return values\n';assert text.count(needle)==1;text=text.replace(needle,'        return NONFLAG_AFTER_PARENT(context, values, values)\n')
    original_read,original_dump=ns.read,ns.dump;final=candidate/'verification.json';intermediate=candidate/'parent_flag_native_checks_before_nonflag_report.json'
    proxy=SimpleNamespace(**vars(ns));proxy.read=lambda path:original_read(intermediate if Path(path).resolve()==final.resolve() else path)
    def dump(path,data,*args,**kwargs):return original_dump(intermediate if Path(path).resolve()==final.resolve() else path,data,*args,**kwargs)
    proxy.dump=dump
    namespace={'__file__':str(source),'__name__':'actual_complete_parent_and_nonflag_residual','NONFLAG_AFTER_PARENT':stage}
    exec(compile(text,str(source),'exec'),namespace);runtime.build_context=build
    try:result,storage=namespace['predict'](proxy,record,candidate,parent_curve_source,mapping_path)
    finally:runtime.build_context=original_build
    full=[r for r in calls if r['rows']==1599600];cold=[r for r in calls if r['rows']==80*4650]
    assert len(full)>=2 and len(cold)>=1
    for c in components:
        result['models']['nonflag_cpu_reverse_bayes64_'+c['name']]=c
        storage.append({'key':'nonflag_cpu_reverse_bayes64_'+c['name'],'source':c['source_path'],'target':c['path'],'sha256':c['sha256'],'samefile':os.path.samefile(c['source_path'],c['path'])})
    result['actual_model_reload_controls'].extend(full[0]['controls']);result['actual80_day_prefix_model_controls'].extend(cold[0]['controls'])
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])
    result.update(actual_nonflag_residual_ReverseBayes64_native_independent_and_CDF_replay=True,nonflag_stage_calls=calls,
      original_parent_model_checks_are_intermediate_before_nonflag_stage=True,original_parent_backend=module)
    original_dump(final,result,immutable=True)
    original_dump(candidate/'nonflag_residual_ReverseBayes64_native_replay_verification.json',{'status':'passed_actual_complete_parent_and_nonflag_ReverseBayes64_two_full_replays_independent_and_cold80',
      'calls':calls,'actual_models':len(result['models']),'original_parent_backend':module,'actual_native_model_storage':storage,'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage
