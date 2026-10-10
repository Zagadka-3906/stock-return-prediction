"""Fresh132-record registry sources; preserve all measured scientific predecessors."""
from pathlib import Path
import ast,io,re,tokenize,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
NAMES=['register_Cross120170_round170_artifacts_v1_20261010.py','publish_Cross120170_round170_full_validation_v1_20261010.py','optimize_training_round170.py','finalize_training_round170.py','lossless_ranking_runtime_adapter_round170_v2_20261008.py','build_lossless_ranking_display_round170_v2_20261008.py','verify_lossless_ranking_display_round170_v2_20261008.py','collect_full_lossless_round170_qa81_20261010.py']

def source_paths():
    return [A/n for n in [*NAMES,'prepare_cross120170_full_registry_sources_v1_20261010.py','cross120170_storage_v1_20261010.py','prepare_cross120170_selected_candidate_v2_20261010.py','seal_cross120170_selected_candidate_v1_20261010.py','cross120_after_complete169_native_stage_v2_20261010.py','predict_cross120170_complete169_scheme_v1_20261010.py','qualify_cross120_two_target132_selected_native14_v1_20261010.py','normalize_predeclared_cross120_two_target132_v3_20261010.py','cross120_two_target132_complete_comparison_selection_plan_v1_20261010.json','cross120170_actual_complete169_parent_callback_CPU_controls_v1_20261010.json','cross120_after_complete169_context_encoder_actual_CPU_controls_v2_20261010.json','cross120170_candidate_actual132_and_own_source_routes_preflight_v2_20261010.json','daily_cross_sectional_feature_encoder120_v1_20261010.py','mature_population_cross120_training_matrix_v1_20261010.py','daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json','cross120_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json','cross120_rank5_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json','predict_fast_neural_frontier169_complete_scheme_v2_20261010.py','fast_neural_frontier169_native_stage_v2_20261010.py','exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010.py','exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json','owned_idle_publication_wait_runtime_v1_20261010.py','lossless_chunked_safe_main_runtime_v1_20261009.py','serial_main_publication_mutex_v1_20261009.py','byte_exact_ranking_stream_runtime_v1_20261010.py','byte_exact_publication_encoder_runtime_v1_20261010.py','late_bound_dynamic_snapshot_encoder_runtime_v1_20261010.py','late_bound_snapshot_encoder_actual_CPU_controls_v1_20261010.json','verified_TLS_Git_retry_runtime_v3_20261010.py','neural_BF16_medium2048_cross120recent252forward5huber050_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_cross120recent252forward5huber050_seed09_independent_forward_v2_20261010.py','neural_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_cross120recent252rank5huber050_seed09_independent_forward_v2_20261010.py']]

def route(text):
    pairs={'register_FastNeuralFrontier169_round169_artifacts_v2':'register_Cross120170_round170_artifacts_v1','publish_FastNeuralFrontier169_round169_full_validation_v2':'publish_Cross120170_round170_full_validation_v1','prepare_frontier169_full_registry_sources_v2':'prepare_cross120170_full_registry_sources_v1','FastNeuralFrontier169':'Cross120170','frontier169_storage_v2':'cross120170_storage_v1','fast_neural_frontier228_selection_plan_v1':'cross120_two_target132_complete_comparison_selection_plan_v1','fast_neural_frontier228':'cross120_two_target132','fast_neural_frontier169_native_stage_v2':'cross120_after_complete169_native_stage_v2','frontier169_complete_parent_native_replay_verification':'cross120170_complete_parent_native_replay_verification','round169':'round170','_r169':'_r170','_r168':'_r169','第169轮':'第170轮','qa80':'qa81','QA80':'QA81','qa_v80_20261010':'qa_v81_20261010'}
    saved={}
    for i,(old,new) in enumerate(sorted(pairs.items(),key=lambda x:-len(x[0]))):
        tag=f'__ROUTE132_{i}__';text=text.replace(old,tag);saved[tag]=new
    for tag,new in saved.items():text=text.replace(tag,new)
    for old,new in [('228','132'),('452','453')]:text=re.sub(r'(?<!\d)'+old+r'(?!\d)',new,text)
    text=tokenize.untokenize([t._replace(string={'169':'170','168':'169','80':'81'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    return text

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_frontier169_full_registry_sources_v2_20261010 import NAMES as original_names
    assert allowed();originals=[];new=[]
    for before,after in zip(original_names,NAMES):
        source=A/before;originals.append(source);text=route(source.read_text(encoding='utf8'))
        if after==NAMES[0]:
            text=text.replace('selection.update(winner=winner, ranking=records,','selection.update(winner=winner, ranking=records, scored_records=132,')
            text=text.replace("['recent252returnhuber050','recent252forward20huber050','recent252forward5huber050','recent252rank5huber050','complete167','complete168','qualified167','qualified168']","['cross120recent252forward5huber050','cross120recent252rank5huber050','qualified168','qualified169']")
            text=text.replace('"""Register340 measured residual schemes and alias their real sealed selected candidate.""""','"""Register132 measured full schemes and alias their real sealed selected candidate.""""')
        if after==NAMES[1]:
            lines=text.splitlines()
            matching=[i for i,line in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in line]
            assert len(matching)==1
            lines[matching[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第170轮：新增120维横截面特征的5日收益和5日排名目标两组TRAIN内验证，各65条原始记录，加完整168/169两个合格锚点，共132条。128项非恒等全量控制与384项因果前缀控制；同一2020—2024连续官方评分。新增目标执行完整169后应用新阶段。最高官方S优先，仅选中新增模型执行六组保存状态14项原生与14项冷启动检查，再冻结完整方案执行两次全量1599600推理与cold80；选中已合格锚点则逐项核对原有推理与封装记录并复用。六视图QA81与GitHub main；未读取测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        target=A/after;assert not target.exists(),target;ast.parse(text);target.write_text(text,encoding='utf8');new.append(target)
    create(A/'cross120170_full_registry_source_preparation_v1_20261010.json',{'status':'compiled8_fresh_complete132_registry_QA81_and_publication_sources_two120_TARGET_families_with_per_record_base169_and_qualified168_169_anchors','input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*new]},'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'actual_full170_preflight_registry_QA81_inference_and_main_pending':True})
    print({'prepared_sources':len(new),'records':132,'QA':81,'no_new_scores_or_future_dispatch':True},flush=True)

if __name__=='__main__':main()
