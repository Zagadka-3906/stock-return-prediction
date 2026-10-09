from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'publish_actual149_all5_and152_historical_main_v55_20261009.py';new=A/'publish_actual149_all5_and152_historical_main_v56_20261009.py'
s=old.read_text(encoding='utf8').replace('SparseAfter14825_full_historical_controls_v1_20261009','SparseAfter14825_full_historical_controls_v2_20261009')
s=s.replace('actual149_all5_and152_historical_main_v55','actual149_all5_and152_historical_main_v56').replace('actual149_all5_and152_historical_v55','actual149_all5_and152_historical_v56')
s=s.replace('sources=[Path(__file__),',"sources=[Path(__file__),A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.json',A/'Pure149_chunked_publication_receiver_runtime_v15_20261009.py',A/'Pure149_chunked_publication_receiver_runtime_v15_20261009.json',",1)
s=s.replace("if __name__=='__main__':main()","""if __name__=='__main__':
 import os
 count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
 for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
  os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
 os.environ['GIT_CONFIG_COUNT']=str(count+2)
 from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
 with safe(Path('E:/赛题五_本机临时/actual149152_historical_safe_publication_v56_20261009')):main()
""")
needle=" for n in jobs:\n  f=A/'service_owned_workflows_20261006'/n;"
assert needle in s
extra=""" for p in A.glob('*round148*20261009.py'):sources.append(p)
 for p in A.glob('*round148*20261009.json'):sources.append(p)
 for p in A.glob('*actual149152*20261009.py'):sources.append(p)
 for p in A.glob('*actual149152*20261009.json'):sources.append(p)
 for version in range(2,9):
  f=A/'service_owned_workflows_20261006'/f'AdaptiveJointCrossHuber242_round148_full_registration_v{version}_20261009'
  if f.is_dir():sources.extend(p for p in f.iterdir() if p.suffix in ('.json','.log'))
"""
s=s.replace(needle,extra+needle)
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
pins={str(p):sha(p) for p in (old,new,Path(__file__),A/'lossless_chunked_safe_main_runtime_v1_20261009.py')}
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('actual149_all5_and152_historical_main_publication_v56_20261009',new.name,[],pins)
create(A/'actual149152_historical_main_hidden_launch_v56_20261009.json',row);print(row['owned_worker_pid'])
