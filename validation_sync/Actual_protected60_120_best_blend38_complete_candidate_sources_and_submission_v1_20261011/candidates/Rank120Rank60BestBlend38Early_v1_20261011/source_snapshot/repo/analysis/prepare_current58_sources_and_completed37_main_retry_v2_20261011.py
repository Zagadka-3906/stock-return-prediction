from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
old=A/'publish_actual_rank120_rank60_protected37_completed_main_v1_20261011.py';s=old.read_text(encoding='utf8')
s=s.replace('Actual_rank120_rank60_protected37_completed_TRAIN_records_main_v1_20261011','Actual_rank120_rank60_protected37_completed_TRAIN_records_main_v2_20261011').replace('from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold','from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold')
p=A/'publish_actual_rank120_rank60_protected37_completed_main_v2_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
r=start_service('actual_rank120_rank60_protected37_completed_main_v2_20261011',p.name,[],{str(p):sha(p),str(A/'owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011.py'):sha(A/'owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011.py')})
proof=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json';data=read(proof)
paths=[Path(x) for x in data['input_sha256'] if Path(x).suffix in ('.py','.json','.md')]
paths += [Path(__file__),proof,p,A/'publication_dynamic_idle_boundary_actual_CPU_controls_v3_20261011.json',A/'verify_publication_dynamic_idle_boundary_controls_v3_20261011.py',A/'actual187_completed_QA_main_only_finally_log_collision_bridge57_v2_20261011.json',A/'prepare_verified_early37_alternate_submission_delivery_v1_20261011.py']
t=(A/'publish_actual_rank60_seed10_own6_and_two_seed37_predeclared_sources_main_v1_20261011.py').read_text(encoding='utf8')
lines=t.splitlines();lines=[('    paths=[Path(p) for p in '+repr([str(q) for q in dict.fromkeys(paths)])+']') if line.strip().startswith('paths=') else line for line in lines]
t='\n'.join(lines)+'\n';t=t.replace('Actual_rank60_seed10_own6_and_two_seed37_predeclared_sources','Actual_current58_and_completed187_bridge57_sources').replace('from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold','from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold')
t=t.replace('predeclared_seed10_mature60day_own6_full5_native42_direct33_and_two_seed37_original_seed9_models_not_reused_for_training','actual187_all_QA_main_completed_finally_log_failure_preserved_current58_idle_only_future_gates_22_publication_paths_and_three_boundary_CPU_controls')
t=t.replace('预声明60日第二种子六年度训练与33项直接方案、37项双种子组合；未完成模型不计入核验','第187轮实际QA与main完成回执；修复后续发布目录与空闲边界竞态；保留失败记录与全部原始模型评分')
q=A/'publish_actual_current58_and_completed187_bridge57_sources_main_v1_20261011.py';ast.parse(t);assert not q.exists();q.write_text(t,encoding='utf8')
sr=start_service('actual_current58_and_completed187_bridge57_sources_main_v1_20261011',q.name,[],{str(q):sha(q),str(Path(__file__)):sha(__file__)})
create(A/'actual_current58_and_completed37_main_retry_activation_v2_20261011.json',{'actual_completed37_publication_retry':r,'current58_sources':sr,'new_fits_or_scores':0})
print({'completed37_publication_retry':True,'current58_source_publication_queued':True},flush=True)
