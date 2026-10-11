from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'publish_actual149_all5_and152_historical_main_v56_20261009.py';new=A/'publish_actual_prospective_and_delivery_main_v57_20261009.py'
s=old.read_text(encoding='utf8').replace('actual149_all5_and152_historical_main_v56','actual_prospective_and_delivery_main_v57').replace('actual149_all5_and152_historical_v56','actual_prospective_and_delivery_v57')
s=s.replace('actual149152_historical_safe_publication_v56','actual_prospective_and_delivery_safe_publication_v57')
marker=" for p in A.glob('*round148*20261009.py'):sources.append(p)";assert marker in s
addition=""" for pattern in ('*publication_safe*20261009.py','*publication_safe*20261009.json','*safe_pipeline*20261009.py','*safe_pipeline*20261009.json'):
  sources.extend(p for p in A.glob(pattern) if p.is_file())
 for name in ('actual_optimization_checkpoint_v53_20261009.json','audit_actual_optimization_resources_v53_20261009.py',
  'latest_actual_optimization_progress_pointer_v54_20261009.json','SparseAfter148152_actual_prospective_scope_v3_20261009.json'):
  sources.append(A/name)
 for row in read(A/'actual_sparse150152_publication_safe_hidden_launches_v16_20261009.json').values():
  f=Path(row['script_args'][0]).parent
  sources.extend(f/p for p in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
  if (f/'service_execution.json').exists():sources.extend(f/p for p in ('service_execution.json','stdout.log','stderr.log'))
 delivery=read(A/'actual_optimization_checkpoint_v53_20261009.json')['delivered_submission']
 sources.append(Path(delivery['output'])/'submission_manifest.json')
"""
s=s.replace(marker,addition+marker)
needle="'actual152_official_scores':0,'actual152_future_X_read':False,";assert needle in s
s=s.replace(needle,"'actual152_official_scores':0,'actual152_future_X_read':False,'actual152_prospective_sources':32,'actual152_prospective_graph_controls':200,'actual148_delivered_submission_verified':True,")
s=s.replace("'同步149全五年度100原生及152在完整148上稀疏修正25历史75因果验证'","'同步152完整32路径200方案图验证、150至152安全发布接收流程和148交付核验'")
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
pins={str(p):sha(p) for p in (old,new,Path(__file__),A/'SparseAfter148152_actual_prospective_scope_v3_20261009.json',A/'sparse150152_publication_safe_receivers_v16_20261009.json')}
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('actual_prospective_and_delivery_main_publication_v57_20261009',new.name,[],pins)
create(A/'actual_prospective_and_delivery_main_hidden_launch_v57_20261009.json',row);print(row['owned_worker_pid'],flush=True)
