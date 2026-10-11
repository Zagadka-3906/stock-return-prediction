from pathlib import Path
import sys,re
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import recover_actual149152_after_chunked148_v10_20261009 as previous
old=Path(previous.__file__);new=A/'recover_actual149152_after_chunked148_v11_20261009.py'
names={old.name:new.name,
 'actual149152_after_chunked148_recovery_v10_20261009.json':'actual149152_after_chunked148_recovery_v11_20261009.json',
 'AdaptiveJointCrossHuber242_round148_full_registration_v5_20261009':'AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009',
 'actual149152_recovery_after_actual148_chunked_main_v10_20261009':'actual149152_recovery_after_actual148_chunked_main_v11_20261009',
 'actual149152_after_chunked148_hidden_launches_v10_20261009.json':'actual149152_after_chunked148_hidden_launches_v11_20261009.json',
 'actual149152_recovery_waiting_dispatch_launch_v10_20261009.json':'actual149152_recovery_waiting_dispatch_launch_v11_20261009.json',
 'complete_hidden_launches_v9_20261009':'complete_hidden_launches_v11_20261009',
 'PureRFFHuber149_complete_chronological_dispatch_v9_20261009':'PureRFFHuber149_complete_chronological_dispatch_v11_20261009'}
for n in [*previous.BASE.values(),*previous.CORE.values()]:
 m=re.search(r'_v(\d+)_20261009.py$',n);assert m,n
 names[n]=n[:m.start()]+f'_v{int(m[1])+1}_20261009.py'
for n in ['verify_PureRFFHuber20_year2023_native_supplement_v3_20261009.py','verify_Pure149_all25_annual_native_coverage_v3_20261009.py','verify_SparseAfter14860_native_historical_calendar_v3_20261009.py','verify_SparseAfter14825_full_historical_controls_v3_20261009.py']:
 names[n]=n.replace('_v3_','_v4_')
names['publish_actual149_all5_and152_historical_main_v54_20261009.py']='publish_actual149_all5_and152_historical_main_v55_20261009.py'
for stem in ['actual149_all5_and152_historical_main_v54','actual149_all5_and152_historical_v54','actual149_all5_and152_historical_main_publication_v54']:
 names[stem]=stem.replace('v54','v55')
s=old.read_text(encoding='utf8')
pattern=re.compile('|'.join(re.escape(k) for k in sorted(names,key=len,reverse=True)))
s=pattern.sub(lambda m:names[m[0]],s)
# Process-local transport settings are inherited by hidden descendants. TLS stays enabled.
settings="""import os
count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
 os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
os.environ['GIT_CONFIG_COUNT']=str(count+2)
"""
s=s.replace('from run_dependency_queue_v3_20261006 import read,sha,create,owned\n','from run_dependency_queue_v3_20261006 import read,sha,create,owned\n'+settings,1)
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
create(A/'actual149152_resume_preparation_v11_20261009.json',{'status':'prepared_new_gate_and_process_local_verified_TLS_transport_only','input_sha256':{str(p):sha(p) for p in (old,new,Path(__file__))},'scientific_case_parameters_changed':False,'old_failed_jobs_preserved':True,'TLS_verification_enabled':True})
print(new)
