"""Prepare fresh133 registry, QA83 and complete main publication sources."""
from pathlib import Path
import ast,io,re,tokenize,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
NAMES=['register_Frontier133172_round172_artifacts_v1_20261010.py','publish_Frontier133172_round172_full_validation_v1_20261010.py','optimize_training_round172.py','finalize_training_round172.py','lossless_ranking_runtime_adapter_round172_v2_20261008.py','build_lossless_ranking_display_round172_v2_20261008.py','verify_lossless_ranking_display_round172_v2_20261008.py','collect_full_lossless_round172_qa83_20261010.py']

def source_paths():
    from prepare_frontier233171_full_registry_sources_v1_20261010 import source_paths as older
    extras=['prepare_frontier133172_full_registry_sources_v1_20261010.py','prepare_frontier133172_selected_candidate_v2_20261010.py','seal_frontier133172_selected_candidate_v1_20261010.py','frontier133172_storage_v1_20261010.py','frontier133172_candidate_sources_preparation_v1_20261010.json','frontier133172_actual_candidate_explicit_universe_admission_v2_20261010.json','frontier133_after_complete_qualified_parent_native_stage_v1_20261010.py','predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py','qualify_frontier133_selected_native14_v1_20261010.py','normalize_completed_frontier133_after171_v1_20261010.py','frontier133_after171_predeclared_training_only_selection_plan_v1_20261010.json','frontier133_actual_three_nested_parent_hooks_CPU_controls_v1_20261010.json','frontier133_actual42_TRAIN_native_and84_cold_controls_v1_20261010.json','run_Cross120Smoothed_after170_high_impact49_screen_v1_20261010.py','causal_neural_rank_smoothing_v1_20261010.py','cross120_smoothed49_actual13950_TRAIN_CPU_controls_v1_20261010.json','neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_cross120recent252returnhuber050_seed09_independent_forward_v1_20261009.py']
    return list(dict.fromkeys([*[A/n for n in NAMES+extras],*older()]))

def route(text):
    pairs={'Frontier233171':'Frontier133172','frontier233171_storage':'frontier133172_storage','prepare_frontier233171_full_registry_sources':'prepare_frontier133172_full_registry_sources','round171':'round172','_r171':'_r172','_r170':'_r171','第171轮':'第172轮','qa82':'qa83','QA82':'QA83','qa_v82':'qa_v83','frontier233_selected_native_stage_v1':'frontier133_selected_native14_v1','frontier233_complete_parent_native_replay_verification':'frontier133_complete_parent_native_replay_verification','frontier233_after169_and170_complete_comparison_predeclared_plan_v2':'frontier133_after171_predeclared_training_only_selection_plan_v1','pilot233':'pilot133'}
    replacements={}
    for i,(before,after) in enumerate(sorted(pairs.items(),key=lambda x:-len(x[0]))):
        tag=f'__FRONTIER133_ROUTE_{i}__';text=text.replace(before,tag);replacements[tag]=after
    for tag,after in replacements.items():text=text.replace(tag,after)
    text=re.sub(r'(?<!\d)233(?!\d)','133',text);text=re.sub(r'(?<!\d)454(?!\d)','455',text)
    return tokenize.untokenize([t._replace(string={'171':'172','170':'171','82':'83'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_frontier233171_full_registry_sources_v1_20261010 import NAMES as oldnames
    assert allowed();inputs=[];outputs=[]
    for before,after in zip(oldnames,NAMES):
        source=A/before;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        text=text.replace('passed_normalized133_actual_TRAIN_official_records_selected_stage_and_frozen_full_inference_pending','passed_normalized133_actual_TRAIN_official_records_selected_stage_and_full_inference_pending')
        if after==NAMES[0]:
            text=text.replace('from frontier233_after_complete_parent_native_stage_v1_20261010 import GRAPH_KEY','from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY')
            needle="len(measured['ordered_native_components'])==(2 if cfg['stage_kind']=='dual120_rank_consensus' else 0)";assert text.count(needle)==1;text=text.replace(needle,"len(measured['ordered_native_components'])==1")
            text=text.replace("'existing_own120_native_bank_fits': 12","'existing_own120_native_bank_fits': 18")
            needle="['dual120_daily_rank_consensus','parent169_causal_Top_stability','parent170_causal_Top_stability','qualified169','qualified170']";assert text.count(needle)==1;text=text.replace(needle,"['cross120_return1d_direct','cross120_mean5_causal_smoothing','cross120_rank5_causal_smoothing','qualified169','qualified170','qualified171']")
            text=text.replace('all233','all133').replace('actual_all233','actual_all133')
        if after==NAMES[1]:
            text=text.replace('Frontier233_selected_native_stage_v2_20261010','Frontier133_selected_native14_v1_20261010')
            lines=text.splitlines();matching=[i for i,line in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in line];assert len(matching)==1
            lines[matching[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第172轮：81项120维一日收益与49项120维预测因果平滑验证，加169/170/171三个完整合格锚点，共133条连续TRAIN官方记录；128项全量独立控制与384项因果前缀控制。选择最高S，按实际保存状态SHA去重模型，只对选中方案执行六组14项原生与14项冷启动检查，再冻结并运行两次完整推理和cold80。六视图QA83与main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        target=A/after;assert not target.exists(),target;ast.parse(text);target.write_text(text,encoding='utf8');outputs.append(target)
    for p in source_paths():assert p.exists(),p
    create(A/'frontier133172_full_registry_sources_preparation_v1_20261010.json',{'status':'compiled8_fresh133_registry_QA83_and_main_sources_pending_actual_selected133_and_full_inference','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'prepared_sources':len(outputs),'records':133,'QA':83,'actual_future_dispatch':False},flush=True)

if __name__=='__main__':main()
