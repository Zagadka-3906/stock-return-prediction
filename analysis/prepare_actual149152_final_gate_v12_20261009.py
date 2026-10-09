from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'recover_actual149152_after_chunked148_v11_20261009.py';new=A/'recover_actual149152_after_chunked148_v12_20261009.py'
s=old.read_text(encoding='utf8')
s=s.replace('recover_actual149152_after_chunked148_v11_20261009','recover_actual149152_after_chunked148_v12_20261009')
s=s.replace('actual149152_after_chunked148_recovery_v11_20261009','actual149152_after_chunked148_recovery_v12_20261009')
s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v7_20261009')
s=s.replace('actual149152_recovery_after_actual148_chunked_main_v11_20261009','actual149152_recovery_after_actual148_chunked_main_v12_20261009')
s=s.replace('actual149152_after_chunked148_hidden_launches_v11_20261009','actual149152_after_chunked148_hidden_launches_v12_20261009')
s=s.replace('actual149152_recovery_waiting_dispatch_launch_v11_20261009','actual149152_recovery_waiting_dispatch_launch_v12_20261009')
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
create(A/'actual149152_final_gate_preparation_v12_20261009.json',{'status':'prepared_actual_remote_reconciliation_gate_only','input_sha256':{str(p):sha(p) for p in (old,new,Path(__file__))},'scientific_cases_unchanged':True})
print(new)
