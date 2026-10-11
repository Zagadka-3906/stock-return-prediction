"""Sync actual36 native/cold controls, retain all12-state selected replay as pending."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    pointer=A/'actual_stock_dual_embedding_actual36_native_location_v1_20261010.json';folder=Path(read(pointer)['output']);proof=read(folder/'verification.json')
    assert (proof['actual_native_cases'],proof['actual_cold_cases'],len(proof['prefit_rejections']))==(36,36,3)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    src=A/'publish_stock_dual_embedding_complete44_preparation_main_v38_20261010.py';text=src.read_text(encoding='utf8')
    idx=text.index('    import publish_classifier_consensus_workflows')
    files=[pointer,*folder.glob('*.json'),A/'stock_rank_dual44_selected_native_stage_v1_20261010.py',A/'prepare_stock_rank_dual44_selected14_routes_v1_20261010.py',A/'predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py',A/'qualify_stock_rank_dual44_selected_native14_v1_20261010.py',A/'stock_rank_dual44_selected14_routes_admission_v1_20261010.json',A/'actual_stock_rank_dual44_selected_native14_activation_v1_20261010.json',Path(__file__)]
    text=text[:idx]+'    paths += ['+','.join('Path('+repr(str(f))+')' for f in files)+']\n'+text[idx:]
    text=text.replace('StockDualEmbedding_complete44_dependency_audit_v38','StockDualEmbedding_actual36_and_selected44_v39').replace('StockDualEmbedding_complete44_dependency_audit_main_v38','StockDualEmbedding_actual36_and_selected44_main_v39').replace('StockDualEmbedding_complete44_dependency_audit_main_receipt_v38','StockDualEmbedding_actual36_and_selected44_main_receipt_v39')
    text=text.replace('passed_actual_dual_five_nested_CPU_hooks_predeclared44_comparison_corrected172_completion_bridge_and_unique_main57_receipt_native36_and_full174_pending','passed_actual_dual_four_saved_states_three_calendars36_native36_cold3_prefit_controls_dynamic_selected44_one_or_two_bank14_routes_queued_full174_pending')
    text=text.replace('保存收益排名双模型五条真实嵌套回调验证、44项完整比较预声明、172实际完成依赖桥接和独立57主分支回执路径修复','保存收益排名互补嵌入36项真实原生36项冷启动及3项拟合前拒绝验证，以及44项完整比较后动态单模型或双模型14项选中参数验证流程')
    dest=A/'publish_stock_dual_embedding_actual36_and_selected44_main_v39_20261010.py';assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_stock_dual_embedding_actual36_and_selected44_main_v39_20261010',dest.name,[],{str(dest):sha(dest)})
    create(A/'actual_stock_dual_embedding_actual36_and_selected44_main_activation_v39_20261010.json',row)
    src=A/'monitor_fast_optimization_v51_20261010.py';text=src.read_text(encoding='utf8')
    text=text.replace('    families=[',"    jobs += ['StockRankDual44_selected_native14_v1_20261010','actual_stock_dual_embedding_actual36_and_selected44_main_v39_20261010']\n    families=[")
    text=text.replace('optimization_live_progress_v51','optimization_live_progress_v52').replace('actual_optimization_fast_runtime_handoff_v85','actual_optimization_fast_runtime_handoff_v87').replace('high_impact_additional_validation_rankings_v23','high_impact_additional_validation_rankings_v24')
    monitor=A/'monitor_fast_optimization_v52_20261010.py';assert not monitor.exists();compile(text,str(monitor),'exec');monitor.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_fast_optimization_progress_v52_20261010',monitor.name,[],{str(monitor):sha(monitor)});create(A/'actual_fast_optimization_progress_activation_v52_20261010.json',row)
    while not (A/'optimization_live_progress_v52_20261010.json').exists():assert owned(row);time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v51_20261010/native_launch.json'),'Observer52 adds actual selected44 qualification and completed36 publication; no scientific task changed.')
    create(A/'actual_optimization_fast_runtime_handoff_v86_20261010.json',{'status':'active_actual193_and_dual36_completed_positive_rank17_and_selected44_native14_queued','deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],'previous_handoff':str(A/'actual_optimization_fast_runtime_handoff_v84_20261010.json'),'actual_progress_observer':52,'rank17_partial_best_S':.4513546761402885,'rank17_scoring_not_claimed_complete':True,'dual36_actual_native_cold_prefit_passed':[36,36,3],'actual_selected44_service':'StockRankDual44_selected_native14_v1_20261010','selected44_graph_key':'stock_rank_dual44_after_complete_parent_v1_20261010','selected44_predictor':'predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py','normalizer44_actual_version':2,'selected44_proof_saved_states_single6_dual12':True,'full174_candidate_freeze_storage_seal_registry_QA85_main_pipeline_not_yet_built':True,'expected_full174_board_records':16792,'stock173_native14_and_full_candidate_pending':True,'complete44_source_publication_actual_version':39,'global_boundary_not_proven':True,'test_labels_read':False})
    print({'actual_dual36_main_publication':39,'actual_observer':52,'full174_pipeline_pending':True},flush=True)
if __name__=='__main__':main()
