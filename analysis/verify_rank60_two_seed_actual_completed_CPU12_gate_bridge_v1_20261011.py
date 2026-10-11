from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed();p=A/'rank60_two_seed_protected_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json';v=read(p);assert len(v['records'])==12
for source,digest in v['input_sha256'].items():assert sha(source)==digest,source
for row in v['records']:assert sha(A/row['parent'])==row['sha256']
create(A/'rank60_two_seed_actual_completed_CPU12_gate_bridge_admission_v1_20261011.json',{'status':'passed_actual_completed12_CPU_controls_gate_bridge_no_new_tests_claimed','actual_existing_records':12,'new_CPU_tests':0,'input_sha256':{str(p):sha(p)},'new_native_fits':0,'new_scores':0,'test_labels_read':False})
