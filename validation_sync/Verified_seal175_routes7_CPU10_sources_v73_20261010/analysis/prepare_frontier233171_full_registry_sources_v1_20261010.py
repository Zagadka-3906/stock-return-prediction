"""Fresh registry233, six-view QA82 and main publication sources for both stage types."""
from pathlib import Path
import ast,io,re,tokenize,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
NAMES=['register_Frontier233171_round171_artifacts_v1_20261010.py','publish_Frontier233171_round171_full_validation_v1_20261010.py','optimize_training_round171.py','finalize_training_round171.py','lossless_ranking_runtime_adapter_round171_v2_20261008.py','build_lossless_ranking_display_round171_v2_20261008.py','verify_lossless_ranking_display_round171_v2_20261008.py','collect_full_lossless_round171_qa82_20261010.py']

def source_paths():
    extras=['prepare_frontier233171_full_registry_sources_v1_20261010.py','prepare_frontier233171_selected_candidate_v1_20261010.py','seal_frontier233171_selected_candidate_v1_20261010.py','frontier233171_storage_v1_20261010.py','frontier233171_candidate_sources_preparation_v1_20261010.json','frontier233_after_complete_parent_native_stage_v1_20261010.py','predict_frontier233_complete_parent_scheme_v1_20261010.py','qualify_frontier233_selected_native_stage_v2_20261010.py','normalize_completed_frontier233_after169_and170_v2_20261010.py','frontier233_after169_and170_complete_comparison_predeclared_plan_v2_20261010.json','frontier233_parent_only_native_adapter_actual18_real_TRAIN_CPU_controls_v1_20261010.json','frontier233_dual2020_actual9_TRAIN_native_and_cold_controls_v1_20261010.json','frontier233_actual169_and170_parent_hook_CPU_controls_v1_20261010.json','dual_target_daily_rank_consensus_v1_20261010.py','budgeted_neural_Top_projection_v1_20261010.py','cross120_after_complete169_native_stage_v2_20261010.py','immutable_prepared_rank_panel_cache_v1_20261010.py','immutable_prepared_rank_panel_cache_actual_full_TRAIN_benchmark_v1_20261010.json','exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010.py','exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json','frozen_external_official_capsule_publish_guard_runtime_v1_20261010.py','frozen_external_official_capsule_publish_guard_actual228_CPU_controls_v1_20261010.json','owned_idle_publication_wait_runtime_v1_20261010.py','lossless_chunked_safe_main_runtime_v1_20261009.py','serial_main_publication_mutex_v1_20261009.py','byte_exact_ranking_stream_runtime_v1_20261010.py','byte_exact_publication_encoder_runtime_v1_20261010.py','late_bound_dynamic_snapshot_encoder_runtime_v1_20261010.py','late_bound_snapshot_encoder_actual_CPU_controls_v1_20261010.json','verified_TLS_Git_retry_runtime_v3_20261010.py','byte_exact_ranking_stream_benchmark_v1_20261010.json','byte_exact_publication_encoder_controls_v1_20261010.json']
    return [A/n for n in [*NAMES,*extras]]

def swap(text,before,after,count=1):
    assert text.count(before)==count,(before,text.count(before),count)
    return text.replace(before,after)

def route(text):
    pairs={'Cross120170':'Frontier233171','cross120170_storage':'frontier233171_storage','prepare_cross120170_full_registry_sources':'prepare_frontier233171_full_registry_sources','round170':'round171','_r170':'_r171','_r169':'_r170','第170轮':'第171轮','qa81':'qa82','QA81':'QA82','qa_v81':'qa_v82','cross120_two_target132_selected_native14_v1':'frontier233_selected_native_stage_v1','cross120170_complete_parent_native_replay_verification':'frontier233_complete_parent_native_replay_verification','cross120_two_target132_complete_comparison_selection_plan_v1':'frontier233_after169_and170_complete_comparison_predeclared_plan_v2','pilot132':'pilot233'}
    placeholders={}
    for i,(before,after) in enumerate(sorted(pairs.items(),key=lambda x:-len(x[0]))):
        tag=f'__FRONTIER_ROUTE_{i}__';text=text.replace(before,tag);placeholders[tag]=after
    for tag,after in placeholders.items():text=text.replace(tag,after)
    text=re.sub(r'(?<!\d)132(?!\d)','233',text);text=re.sub(r'(?<!\d)453(?!\d)','454',text)
    text=tokenize.untokenize([t._replace(string={'170':'171','169':'170','81':'82'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    return text

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_cross120170_full_registry_sources_v1_20261010 import NAMES as old_names
    assert allowed();inputs=[];outputs=[]
    for before,after in zip(old_names,NAMES):
        source=A/before;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        if after==NAMES[0]:
            text=swap(text,'assert not OUT.exists()',"from frontier233171_storage_v1_20261010 import empty\n    empty(OUT)")
            text=swap(text,'    OUT.mkdir()\n','')
            text=text.replace('passed_normalized233_actual_complete_training_only_official_records','passed_normalized233_actual_TRAIN_official_records_selected_stage_and_frozen_full_inference_pending')
            text=text.replace("cfg['model'] is None","cfg['stage_kind']=='anchor'")
            start=text.index('        else:\n            assert measured[');end=text.index('        capsule = ',start)
            text=text[:start]+'''        else:
            control=read(Path(measured['original_screen_record']).with_name(f"case{measured['original_screen_case']:03d}_controls.json"))
            assert sha(Path(measured['original_screen_record']).with_name(f"case{measured['original_screen_case']:03d}_controls.json"))==measured['control_sha256']
            assert control['full_independent_Pandas_exact'] and [p['days'] for p in control['prefix_controls']]==[80,260,975]
            assert control['numeric_sha256']==measured['prediction_numeric_bytes_sha256']
''' +text[end:]
            start=text.index('            from cross120_after_complete169_native_stage');end=text.index('        row = deepcopy',start)
            text=text[:start]+'''            from frontier233_after_complete_parent_native_stage_v1_20261010 import GRAPH_KEY
            assert GRAPH_KEY not in graph
            assert len(measured['ordered_native_components'])==(2 if cfg['stage_kind']=='dual120_rank_consensus' else 0)
            screen_original=read(measured['original_screen_record']);assert screen_original['metrics']==measured['metrics']
            graph[GRAPH_KEY]={**cfg,'position':'after_complete_qualified_parent','original_complete_parent_round':cfg['anchor_round'],'original_complete_parent_graph_preserved':True,'original_completed_train_only_screen_record':measured['original_screen_record'],'ordered_native_components':measured['ordered_native_components'],'native_bank_components':measured.get('native_bank_components',[]),'future_candidate_not_inferred_for_nonselected_comparison':True}
''' +text[end:]
            text=swap(text,"deepcopy(measured['actual_return_mapping'])","deepcopy(measured.get('actual_return_mapping',read(A/f\"optimization_20261003_r{cfg['anchor_round']}/selection.json\")['winner']['causal_return_mapping']))")
            text=text.replace("[f['stem']", "[f['name']").replace("(f['stem']+", "(f['name']+")
            text=text.replace('all132','all233').replace('actual_all132','actual_all233')
            text=swap(text,"['cross120recent252forward5huber050','cross120recent252rank5huber050','qualified168','qualified169']","['dual120_daily_rank_consensus','parent169_causal_Top_stability','parent170_causal_Top_stability','qualified169','qualified170']")
            text=text.replace("'existing_BF16_wide_native_bank_fits': 6","'existing_own120_native_bank_fits': 12")
        if after==NAMES[1]:
            text=text.replace("f['stem']+","f['name']+")
            text=swap(text,"'Frontier233171_selected_native14_v1_20261010'","'Frontier233_selected_native_stage_v2_20261010'")
            lines=text.splitlines();matches=[i for i,line in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in line];assert len(matches)==1
            lines[matches[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第171轮：193项双目标同日排名集成、完整169及170之后的各19项持仓稳定方案，与两个完整合格锚点，共233条连续TRAIN官方记录；228项全量独立控制与684项因果前缀控制。选择最高官方S，新增阶段按实际类型执行保存模型或纯后处理检查；仅选中方案冻结后运行两次完整推理及cold80。六视图QA82与main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        target=A/after;assert not target.exists(),target;ast.parse(text);target.write_text(text,encoding='utf8');outputs.append(target)
    for path in source_paths():assert path.exists(),path
    create(A/'frontier233171_full_registry_sources_preparation_v1_20261010.json',{'status':'compiled8_fresh233_registry_QA82_and_main_sources_pending_actual_selected233_and_full_inference','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'prepared':len(outputs),'records':233,'QA':82,'actual_future_dispatch':False},flush=True)

if __name__=='__main__':main()
