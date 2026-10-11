"""Prepare exact replay for mixed-label, near-pure mixed-label and mixed-window sources."""
from pathlib import Path
import sys,runpy,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();original=A/'rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011.py';base=original.read_text(encoding='utf8')
    near=base.replace('rank5_rank20_mixed_after_complete_qualified_parent_v1_20261011','rank5_rank20_near_pure_after_complete_qualified_parent_v1_20261011').replace('stock_rank5_rank20_mixed_label_horizon_ID16_cross120_recent252_e64','stock_rank5_rank20_near_pure_label_horizon_ID16_cross120_recent252_e64').replace("spec['rank5_weight'] in (.25,.5,.75)","spec['rank5_weight'] in (.03125,.0625,.125)")
    near_source=save('rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011.py',near)
    long=base.replace('rank5_rank20_mixed_after_complete_qualified_parent_v1_20261011','rank20_short_long_after_complete_qualified_parent_v1_20261011').replace('stock_rank5_rank20_mixed_label_horizon_ID16_cross120_recent252_e64','stock_rank20_short_long_mixed_window_ID16_cross120_252_504_e64').replace('stock_rank5_embedding','stock_rank20long_embedding').replace('rank5_weight','long504_weight').replace('rank5_rank20_mixed_raw_average','rank20_short_long_mixed_raw_average')
    long=long.replace("spec['long504_weight'] in (.25,.5,.75)","spec['long504_weight'] in (.0625,.25,.5)")
    long=long.replace("meta['training_calendar_window']==252 and meta['days']<=252","meta['training_calendar_window']==(252,504)[i] and meta['days']<=(252,504)[i]")
    long=long.replace("native.CONFIG['label_horizon_trading_days']==(20,5)[i]","native.CONFIG['label_horizon_trading_days']==20").replace("native.CONFIG['target']==('y_rank_20mean','y_rank_5mean')[i]","native.CONFIG['target']=='y_rank_20mean'")
    window_source=save('rank20_short_long_after_qualified_parent_native_stage_v1_20261011.py',long)
    original_predictor=A/'predict_rank5_rank20_mixed_complete_qualified_parent_scheme_v1_20261011.py';text=original_predictor.read_text(encoding='utf8')
    start=text.index('    import rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011 as cdf');end=text.index("    assert spec['original_complete_parent_round']==175",start)
    text=text[:start]+"    graph=record['winner'][ns.GRAPH_FIELD]\n    stage,key,mix_field=select_stage(graph);spec=deepcopy(graph[key])\n"+text[end:]
    text=text.replace("spec['rank5_weight'] in (.25,.5,.75)","0.<spec[mix_field]<1.")
    text=text.replace("assert member['configuration']['label_horizon_trading_days']==(20,5)[i]","assert member['configuration']['label_horizon_trading_days']==(20,20 if mix_field=='long504_weight' else 5)[i]\n        assert member['configuration']['training_calendar_window']==(252,504 if mix_field=='long504_weight' else 252)[i]")
    selector="""
def select_stage(graph):
    import rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011 as mixed
    import rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011 as near
    import rank20_short_long_after_qualified_parent_native_stage_v1_20261011 as window
    choices=[(mixed,'rank5_weight',(.25,.5,.75)),(near,'rank5_weight',(.03125,.0625,.125)),(window,'long504_weight',(.0625,.25,.5))]
    active=[item for item in choices if item[0].GRAPH_KEY in graph];assert len(active)==1
    stage,field,weights=active[0];spec=graph[stage.GRAPH_KEY]
    assert spec['recipe']==stage.RECIPE and spec['codec']=='CDF' and spec[field] in weights
    return stage,stage.GRAPH_KEY,field

"""
    text=text.replace('def predict(ns,record,candidate,parent_curve_source,mapping_path):',selector+'def predict(ns,record,candidate,parent_curve_source,mapping_path):')
    predictor=save('predict_three_cached_mixed_complete_qualified_parent_scheme_v2_20261011.py',text)
    module=importlib.import_module(predictor.stem);rows=[]
    for filename,field,weights in [('rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011','rank5_weight',(.25,.5,.75)),(near_source.stem,'rank5_weight',(.03125,.0625,.125)),(window_source.stem,'long504_weight',(.0625,.25,.5))]:
        stage=importlib.import_module(filename)
        for weight in weights:
            graph={stage.GRAPH_KEY:{'recipe':stage.RECIPE,'codec':'CDF',field:weight}};chosen,key,mix_field=module.select_stage(graph);assert chosen is stage and key==stage.GRAPH_KEY and mix_field==field
            rows.append({'stage':filename,'component_weight':weight,'field':field,'actual_selector_checked':True})
    failures=[]
    stages=[importlib.import_module(n) for n in ['rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011',near_source.stem,window_source.stem]]
    for graph in [{},{s.GRAPH_KEY:{'recipe':s.RECIPE,'codec':'CDF','rank5_weight':.25} for s in stages[:2]}, {stages[0].GRAPH_KEY:{'recipe':stages[0].RECIPE,'codec':'CDF','rank5_weight':0.}}]:
        try:module.select_stage(graph)
        except AssertionError:failures.append(True)
        else:raise AssertionError('Ambiguous or unplanned component ratio accepted')
    cpu=A/'verify_rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011.py';cpucode=cpu.read_text(encoding='utf8').replace('predict_rank5_rank20_mixed_complete_qualified_parent_scheme_v1_20261011','predict_three_cached_mixed_complete_qualified_parent_scheme_v2_20261011').replace('rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011','three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011')
    cpusource=save('verify_three_cached_mixed_actual_eleven_parent_callbacks_CPU_v2_20261011.py',cpucode);runpy.run_path(str(cpusource),run_name='__main__')
    paths=[Path(__file__),original,original_predictor,near_source,window_source,predictor,cpu,cpusource,A/'three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011.json']
    create(A/'three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011.json',{'status':'passed_actual9_stage_ratio_selectors3_bad_configuration_refusals_and11_parent_callbacks_CPU_only','input_sha256':{str(p):sha(p) for p in paths},'actual_selector_controls':rows,'actual_selector_bad_input_refusals':len(failures),'actual_parent_callback_CPU_count':11,'native_replay_and_future_qualification_pending':True,'label_horizons_per_variant':[[20,5],[20,5],[20,20]],'training_windows_per_variant':[[252,252],[252,252],[252,504]],'equal_training_populations_not_claimed':True,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'actual_selector_controls':len(rows),'bad_input_refusals':len(failures),'actual_parent_callback_CPU_checks':11,'native_and_full_future_checks_pending':True},flush=True)
if __name__=='__main__':main()
