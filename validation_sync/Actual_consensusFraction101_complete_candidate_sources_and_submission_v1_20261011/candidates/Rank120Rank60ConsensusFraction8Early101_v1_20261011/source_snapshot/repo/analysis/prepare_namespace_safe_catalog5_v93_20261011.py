from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
failed=A/'service_owned_workflows_20261006/actual_complete191_plus_completed_raw_TRAIN_score_catalog_v4_20261011/service_execution.json';assert read(failed)['status']=='failed'
s=(A/'build_complete191_plus_completed_raw_TRAIN_score_catalog_v4_20261011.py').read_text(encoding='utf8').replace('榜_v4_20261011','榜_v5_20261011').replace('location_v4_20261011','location_v5_20261011').replace("closed('actual_consensusWeight8_results_selection_main85_v1_20261011')","closed('actual_completed_weight85_full_pipeline90_v1_20261011')")
b=A/'build_complete191_plus_completed_raw_TRAIN_score_catalog_v5_20261011.py';ast.parse(s);assert not b.exists();b.write_text(s,encoding='utf8')
s=(A/'publish_actual_complete191_and_raw_TRAIN_score_catalog_v4_main_v1_20261011.py').read_text(encoding='utf8').replace('catalog_v4','catalog_v5').replace('location_v4','location_v5');p=A/'publish_actual_complete191_and_raw_TRAIN_score_catalog_v5_main_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
proof=A/'actual_namespace_safe_catalog5_admission_v1_20261011.json';create(proof,{'status':'same_formal191_cap_compact_catalog_after_actual_namespace_bridge90_full_candidate_closed_only_new_uncompleted_raw_records_excluded','input_sha256':{str(q):sha(q) for q in [Path(__file__),b,p,failed]},'new_scores':0,'test_labels_read':False})
for name,driver in [('actual_complete191_plus_completed_raw_TRAIN_score_catalog_v5_20261011',b),('actual_complete191_and_raw_TRAIN_score_catalog_v5_main_v1_20261011',p)]:
 assert allowed();r=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
