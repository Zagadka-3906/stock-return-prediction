from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
s=(A/'verify_actual187_complete_QA_main_finally_bridge56_v1_20261011.py').read_text(encoding='utf8')
s=s.replace("r['round'],r['scored_records'],r['connected_records'],r['actual_full_QA_version']","r['round'],r['scored_records'],r['connected_records']").replace("==(187,88,17490)","==(187,88,17490)")
s=s.replace("for p,d in scope['input_sha256'].items():", "qa=read(A/'lossless_ranking_display_qa_v98_20261010/round187/verification.json');assert qa['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks' and qa['round']==187 and qa['original_full_QA_result']['status']=='passed' and (qa['original_full_QA_result']['connected_records'],qa['original_full_QA_result']['new_round_records'])==(17490,88)\nfor p,d in scope['input_sha256'].items():")
s=s.replace('collision_bridge56_v1_20261011','collision_bridge57_v2_20261011')
p=A/'verify_actual187_complete_QA_main_finally_bridge57_v2_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
t=(A/'start_actual187_bridge56_and_current58_future_v1_20261011.py').read_text(encoding='utf8').replace('verify_actual187_complete_QA_main_finally_bridge56_v1_20261011','verify_actual187_complete_QA_main_finally_bridge57_v2_20261011').replace('actual187_complete_QA_main_finally_bridge56_v1_20261011','actual187_complete_QA_main_finally_bridge57_v2_20261011').replace('actual187_complete_bridge56_activation','actual187_complete_bridge57_activation')
t=t.replace('paths=[Path(__file__),oldproof,bridge,',"paths=[A/'owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011.py',Path(__file__),oldproof,bridge,")
t=t.replace("assert s.count(\"PROOF=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'\")==1;", "s=s.replace(\" data['service_aliases'].update(proof['service_alias_updates']);data['driver_wrappers'].update(proof['driver_wrappers'])\",\" data['service_aliases'].update(proof['service_alias_updates']);data['driver_wrappers'].update(proof['driver_wrappers'])\\n import owned_idle_publication_wait_reboot_identity_v2_20261011 as wait_module\\n from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold as actual_hold\\n wait_module.hold=actual_hold\")\nassert s.count(\"PROOF=A/'actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json'\")==1;")
q=A/'start_actual187_bridge57_and_current58_future_v2_20261011.py';ast.parse(t);assert not q.exists();q.write_text(t,encoding='utf8');print(q,flush=True)
