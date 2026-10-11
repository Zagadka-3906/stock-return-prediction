from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
for name,driver,args in [('actual_completed_weight84_namespace_bridge90_v1_20261011','audit_completed_weight84_and_fraction88_namespace_bridges90_v1_20261011.py',['weight84']),('actual_completed_weight85_full_pipeline90_v1_20261011','run_completed_screen_namespace_safe_pipeline90_v1_20261011.py',['weight84']),('actual_completed_fraction88_namespace_bridge91_v1_20261011','audit_completed_weight84_and_fraction88_namespace_bridges90_v1_20261011.py',['fraction88']),('actual_completed_fraction89_full_pipeline92_v1_20261011','run_completed_screen_namespace_safe_pipeline90_v1_20261011.py',['fraction88'])]:
 assert allowed();p=A/driver;r=start_service(name,driver,args,{str(p):sha(p)});create(A/(name+'_activation.json'),r)
