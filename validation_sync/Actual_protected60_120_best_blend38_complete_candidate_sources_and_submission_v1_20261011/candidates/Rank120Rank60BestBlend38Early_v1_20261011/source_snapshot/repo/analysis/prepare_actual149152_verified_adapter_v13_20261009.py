from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'recover_actual149152_after_chunked148_v12_20261009.py';new=A/'recover_actual149152_after_chunked148_v13_20261009.py'
s=old.read_text(encoding='utf8').replace('recover_actual149152_after_chunked148_v12_20261009','recover_actual149152_after_chunked148_v13_20261009')
s=s.replace('from recover_actual149152_after_chunked148_v10_20261009 import execute','from recover_actual149152_after_chunked148_v13_20261009 import execute')
for stem in ('actual149152_after_chunked148_recovery','actual149152_recovery_after_actual148_chunked_main','actual149152_after_chunked148_hidden_launches','actual149152_recovery_waiting_dispatch_launch'):
 s=s.replace(stem+'_v12_20261009',stem+'_v13_20261009')
assert 'from recover_actual149152_after_chunked148_v10_20261009 import execute' not in s
assert 'from recover_actual149152_after_chunked148_v13_20261009 import execute' in s
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
create(A/'actual149152_verified_adapter_preparation_v13_20261009.json',{'status':'verified_own_current_adapter_import_before_launch','input_sha256':{str(p):sha(p) for p in (old,new,Path(__file__))},'scientific_parameters_changed':False})
print(new)
