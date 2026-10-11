from pathlib import Path
import sys,time,json,subprocess,shutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import psutil
processes={p.pid:p for p in psutil.process_iter()};rows=[]
for folder in (A/'service_owned_workflows_20261006').iterdir():
 p=folder/'native_launch.json'
 if not p.is_file():continue
 try:
  row=read(p);worker=processes.get(row.get('owned_worker_pid'))
  if worker is None or abs(worker.create_time()-row['owned_worker_creation_time'])>.1:continue
  terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
  rows.append({'service':folder.name,'worker_pid':worker.pid,'rss_GiB':worker.memory_info().rss/2**30,'cpu_seconds':sum(worker.cpu_times()[:2]),'terminal_record':terminal,'driver':row.get('original_driver'),'process_status':worker.status()})
 except (psutil.Error,KeyError,json.JSONDecodeError):continue
gpu=None;exe=shutil.which('nvidia-smi')
if exe:
 result=subprocess.run([exe,'--query-gpu=name,utilization.gpu,memory.used,memory.total','--format=csv,noheader,nounits'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
 gpu={'exit_code':result.returncode,'snapshot':result.stdout.strip()}
progress=read(A/'optimization_live_progress_v54_20261009.json');delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')
assert delivery['selected_round']==148 and delivery['csv_sha256']==sha(Path(delivery['output'])/'submission.csv')
checkpoint={'status':'actual148_fully_qualified_and149152_historical_and_publication_recovered','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
 'goal_status':'active','deadline_local':'2026-10-10T23:59:00+08:00','best_fully_qualified':progress['best_fully_qualified'],'delivered_submission':delivery,
 'actual_owned_services':rows,'gpu_snapshot':gpu,'available_memory_GiB':psutil.virtual_memory().available/2**30,'free_storage_GiB':{d:psutil.disk_usage(d+':/').free/2**30 for d in ('D','E')},
 'actual149_all5_state_native_proof':read(A/'Pure149_all25_annual_native_coverage_v1_20261009.json')['status'],
 'actual152_25full75prefix60native':True,'actual152_32sources200graphs':True,'actual152_official_scores':0,
 'verified_publication_lossless_chunking_and_index_guards':str(A/'lossless_chunked_safe_main_runtime_v1_20261009.json'),
 'recovery_publication148_main':read(A/'github_validation_sync_main_20261005/round148_receipt.json')['commit'],
 'actual149152_historical_main_receipt':read(A/'actual149_all5_and152_historical_main_v56_receipt_20261009.json'),
 'optimization_exhaustion_proven':False,'global_semantic_uniqueness_not_claimed':True,'test_labels_read':False,'competition_upload_performed':False}
create(A/'actual_optimization_checkpoint_v53_20261009.json',checkpoint)
print(json.dumps({'gpu':gpu,'available_memory_GiB':checkpoint['available_memory_GiB'],'services':[{k:r[k] for k in ('service','worker_pid','rss_GiB')} for r in rows]},ensure_ascii=False),flush=True)
