"""Declare a distinct medium neural recipe before any quality evaluation; use E-only durable artifacts."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
native_old=A/'neural_BF16_micro8192_native_v1_20261008.py';native_new=A/'neural_BF16_medium2048_seed09_e64_native_v1_20261009.py'
s=native_old.read_text(encoding='utf8')
replacements={"'hidden': [16384, 8192, 4096]":"'hidden': [2048, 1024, 512]","'epochs': 32":"'epochs': 64","'learning_rate': .001":"'learning_rate': .0005","'seed': 20261007":"'seed': 20261009",'own_mature_BF16_micro8192_weighted_accum_v1_20261008':'own_mature_BF16_medium2048_seed09_e64_weighted_accum_v1_20261009'}
for k,v in replacements.items():assert s.count(k)==1,k;s=s.replace(k,v)
compile(s,str(native_new),'exec')
with native_new.open('x',encoding='utf8') as f:f.write(s)
control_old=A/'verify_neural_BF16_micro_restart_v1_20261008.py';control_new=A/'verify_neural_BF16_medium2048_seed09_restart_v1_20261009.py'
s=control_old.read_text(encoding='utf8').replace('neural_BF16_micro8192_native_v1_20261008','neural_BF16_medium2048_seed09_e64_native_v1_20261009')
s=s.replace('E:/赛题五_本机临时/GPU实测_20261008/BF16_micro_restart_v1','E:/赛题五_本机临时/GPU实测_20261009/BF16_medium2048_seed09_restart_v1')
s=s.replace('actual_BF16_micro_restart_location_20261008.json','actual_BF16_medium2048_seed09_restart_location_v1_20261009.json')
compile(s,str(control_new),'exec')
with control_new.open('x',encoding='utf8') as f:f.write(s)
train_old=A/'train_neural_BF16_micro8192_bank6_v2_20261008.py';train_new=A/'train_neural_BF16_medium2048_seed09_e64_bank6_v1_20261009.py'
s=train_old.read_text(encoding='utf8').replace('neural_BF16_micro8192_native_v1_20261008','neural_BF16_medium2048_seed09_e64_native_v1_20261009')
s=s.replace('neural_BF16_micro8192_bank6_v2_20261008','neural_BF16_medium2048_seed09_e64_bank6_v1_20261009')
s=s.replace('actual_BF16_micro8192_small32_wide2_restart_control_v1_20261008','actual_BF16_medium2048_seed09_restart_control_v1_20261009')
s=s.replace('actual_BF16_micro_restart_location_20261008.json','actual_BF16_medium2048_seed09_restart_location_v1_20261009.json')
s=s.replace('actual_BF16_micro8192_bank6_location_v2_20261008.json','actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009.json')
s=s.replace('32 fixed epochs','64 fixed epochs')
needle="    create(A / 'actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009.json', {'status': 'authorized_new_recipe_annual_bank_on_E',\n        'output': str(OUT), 'protocol_sha256': sha(OUT / 'protocol.json'), 'new_quality_scores': 0})"
assert s.count(needle)==1
s=s.replace(needle,"    location=A/'actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009.json'\n    descriptor={'status':'authorized_new_recipe_annual_bank_on_E','output':str(OUT),'protocol_sha256':sha(OUT/'protocol.json'),'new_quality_scores':0}\n    if location.exists():assert read(location)==descriptor\n    else:create(location,descriptor)")
compile(s,str(train_new),'exec')
with train_new.open('x',encoding='utf8') as f:f.write(s)
tree=ast.parse(native_new.read_text(encoding='utf8'));cfg=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in n.targets)))
assert cfg['hidden']==[2048,1024,512] and cfg['epochs']==64 and cfg['seed']==20261009 and cfg['learning_rate']==.0005
inputs=[Path(__file__),native_old,native_new,control_old,control_new,train_old,train_new,A/'train_neural_width_bank_20261004.py']
create(A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json',{'status':'declared_distinct_BF16_medium_recipe_before_quality_training_labels_only',
 'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'configuration':cfg,
 'old_2048_FP32_seed07_e32_and_BF16_16384_seed07_e32_preserved':True,'annual_years':[2020,2021,2022,2023,2024,2025],
 'complete_native_restart_controls_required_before_annual_training':True,'test_labels_read':False,'future_X_read':False,'new_quality_scores':0,
 'actual_six_annual_fits_not_yet_claimed':True,'potential_future_round':153,'resource_exhaustion_not_claimed':True})
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
pins={str(p):sha(p) for p in (native_new,control_new,train_new,A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json')}
rows={}
rows['control']=start('actual_BF16_medium2048_seed09_restart_control_v1_20261009',control_new.name,[],pins)
rows['annual']=start('actual_BF16_medium2048_seed09_e64_bank6_v1_20261009',train_new.name,[],pins)
create(A/'neural_BF16_medium2048_seed09_e64_hidden_launches_v1_20261009.json',rows)
print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
