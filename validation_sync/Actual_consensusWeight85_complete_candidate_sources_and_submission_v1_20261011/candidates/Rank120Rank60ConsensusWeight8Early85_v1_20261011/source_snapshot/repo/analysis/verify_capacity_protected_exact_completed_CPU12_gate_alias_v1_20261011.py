from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed();closed('actual_rank60_two_capacity_twelve_parent_callbacks_CPU_v1_20261011')
p=A/'rank60_two_capacity_protected_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json';data=read(p)
assert len(data['records'])==12
for source,digest in data['input_sha256'].items():assert sha(source)==digest,source
create(A/'capacity_protected_actual_CPU12_completed_gate_alias_admission_v1_20261011.json',{'status':'passed_reverified_exact_existing_actual12_CPU_callback_expressions_not_new_tests','input_sha256':{str(p):sha(p),str(Path(__file__)):sha(__file__)},'original_actual_service':'actual_rank60_two_capacity_twelve_parent_callbacks_CPU_v1_20261011','new_CPU_tests':0,'new_fits':0,'new_scores':0})
