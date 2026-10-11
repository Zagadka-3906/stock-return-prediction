from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
original=A/'publish_actual_disagreement10_score_priority72_observer148_sources_main_v1_20261011.py'
s=original.read_text(encoding='utf8').replace('actual_disagreement10_score_priority72_observer148_sources','actual_checkpoint_cleanup_and_QA_E_relocation74').replace('冻结10项跨时长预测分歧评分优先队列与实际监控148；保留正在运行191和原48项任务，提分后完整候选核验仍必要','记录实际清理12个弃用训练检查点430MB、完整191榜QA页面146MB按字节迁至E保留原路径、条件原生候选73接续清单；不新增科学分数或完成声明')
paths=[Path(__file__),original,*[A/name for name in ['cleanup_unused_medium_completed_checkpoints73_v1_20261011.py','actual_unused_medium_completed_checkpoints73_cleanup_plan_v1_20261011.json','actual_unused_medium_completed_checkpoints73_cleanup_verification_v1_20261011.json','relocate_completed191_QA_pages_to_E_v74_20261011.py','actual_completed191_QA_page_E_relocation74_plan_v1_20261011.json','actual_completed191_QA_page_E_relocation74_verification_v1_20261011.json','save_actual_disagreement73_handoff_v306_20261011.py','actual_disagreement73_conditional_full_native_pipeline_and_checkpoint_cleanup_handoff_v306_20261011.json']]]
tree=ast.parse(s);node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'];s=''.join(lines)
old="'status': 'actual_owned_idle_administrative_queue_only_replaced_original191_and_raw10_scientific_workers_preserved_raw10_and_if_gain_full_native_candidate_prioritized_before_original48_future_records'"
assert old in s;s=s.replace(old,"'status': 'actual_unused_checkpoint430MB_cleanup_and_current_QA_pages146MB_E_relocation_all_weights_info_scores_and_original_paths_preserved_sources_only_no_new_science_completion_claim'")
p=A/'publish_actual_checkpoint_cleanup_and_QA_E_relocation74_main_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
proof=A/'actual_checkpoint_cleanup_and_QA_E_relocation74_main_sources_admission_v1_20261011.json';create(proof,{'status':'actual_completed_storage_actions_source_publication_predeclared','input_sha256':{str(q):sha(q) for q in [*paths,p]},'new_scientific_results_not_claimed':True})
assert allowed();r=start_service('actual_checkpoint_cleanup_and_QA_E_relocation74_main_v1_20261011',p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/'actual_checkpoint_cleanup_and_QA_E_relocation74_main_activation_v1_20261011.json',r)
print({'completed_cleanup_and_relocation_main_publisher_queued':True},flush=True)
