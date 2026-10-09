from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
folder=A/'service_owned_workflows_20261006/AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009'
assert read(folder/'service_execution.json')['status']=='passed' and not owned(read(folder/'native_launch.json'))
assert read(A/'optimization_20261003_r148/full_registration_execution.json')['status']=='passed'
old=A/'recover_actual149152_after_chunked148_v13_20261009.py';new=A/'recover_actual149152_after_chunked148_v14_20261009.py'
s=old.read_text(encoding='utf8').replace('recover_actual149152_after_chunked148_v13_20261009','recover_actual149152_after_chunked148_v14_20261009')
s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v7_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009')
for stem in ('actual149152_after_chunked148_recovery','actual149152_recovery_after_actual148_chunked_main','actual149152_after_chunked148_hidden_launches','actual149152_recovery_waiting_dispatch_launch'):
 s=s.replace(stem+'_v13_20261009',stem+'_v14_20261009')
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
create(A/'actual149152_passed_gate_preparation_v14_20261009.json',{'status':'verified_actual148_full_and_main_pass_before_launch','input_sha256':{str(p):sha(p) for p in (old,new,Path(__file__),folder/'service_execution.json')},'scientific_parameters_changed':False})
print(new)
