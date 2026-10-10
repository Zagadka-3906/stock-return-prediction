"""Keep one fresh observer and retire only proved idle obsolete progress readers; no scientific worker is touched."""
from pathlib import Path
import sys,time,json,re
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 old=A/'monitor_actual_chronological_optimization_progress_v36_20261008.py';s=old.read_text(encoding='utf8').replace('optimization_live_progress_v36','optimization_live_progress_v37')
 s=s.replace("'reduced_required_heads_cross_huber_both':[2,3,5]", "'reduced_required_heads_cross_huber_both':[2,3,5],'own25_saved_state_audit':status('PureRFFHuber25_existing_native_evidence_audit_v1_20261008')")
 s=s.replace('25个年度状态的子集核验、完整历史回放和128项评分接收流程仍待准备','25个年度状态已完成子集核验；真实历史回放和128项评分接收流程仍待准备')
 p=save('monitor_actual_chronological_optimization_progress_v37_20261008.py',s)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p),str(Path(__file__)):sha(__file__)}
 row=start('actual_chronological_optimization_progress_observer_v37_20261008',p.name,[],pins)
 create(A/'latest_actual_optimization_progress_pointer_v37_20261008.json',{'json':str(A/'optimization_live_progress_v37_20261008.json'),
  'markdown':str(A/'optimization_live_progress_v37_20261008.md'),'launch':row,'input_sha256':pins,'new_quality_scores':0})
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 import psutil,subprocess
 retired=[];skipped=[]
 pattern=re.compile(r'actual_chronological_optimization_progress_observer_v(\d+)_20261008$')
 for folder in (A/'service_owned_workflows_20261006').glob('actual_chronological_optimization_progress_observer_v*_20261008'):
  m=pattern.fullmatch(folder.name)
  if not m or int(m.group(1))>=37:continue
  n=int(m.group(1));launch=read(folder/'native_launch.json')
  if not owned(launch):continue
  process=psutil.Process(launch['owned_worker_pid'])
  if process.memory_info().rss>=256*2**20:skipped.append({'name':folder.name,'reason':'reader_not_small_idle_process'});continue
  driver='monitor_actual_chronological_optimization_progress_v'+str(n)+'_20261008.py'
  if not (A/driver).is_file():skipped.append({'name':folder.name,'reason':'unexpected_driver_identity'});continue
  diagnostic=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(process.pid)],capture_output=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
  stack=diagnostic.stdout.decode('utf8',errors='replace')
  if diagnostic.returncode or any(('    '+name+' (') in stack for name in ('snapshot','write','status','loads','read')):
   skipped.append({'name':folder.name,'reason':'reader_currently_active_or_stack_unavailable'});continue
  if ('    main ('+driver+':') not in stack:skipped.append({'name':folder.name,'reason':'not_at_owned_reader_idle_frame'});continue
  parent=worker=None
  try:
   parent,worker,proof=suspended_idle(launch,'    main ('+driver+':')
   rss=worker.memory_info().rss;worker.terminate();parent.terminate()
   _,alive=psutil.wait_procs([worker,parent],timeout=5);assert not alive and not owned(launch)
   retired.append({'name':folder.name,'launch':launch,'idle_stack':proof,'RSS_bytes':rss,'reason':'superseded_read_only_progress_observer'})
  finally:
   for proc in (worker,parent):
    if proc is not None and proc.is_running():proc.resume()
 create(A/'actual_obsolete_progress_readers_retired_v37_20261008.json',{'status':'kept_fresh37_and_retired_only_proved_idle_obsolete_project_progress_readers',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'retired':retired,'skipped':skipped,'new_observer':row,
  'fit_scoring_native_inference_candidate_or_publication_workers_stopped':0,'all_source_files_and_old_observer_logs_preserved':True,
  'latest_fully_qualified_delivery_maintainer_and_main_publisher_preserved':True,'new_quality_scores':0,'test_labels_read':False})
 print(json.dumps({'observer':row['owned_worker_pid'],'retired_old_readers':len(retired),'RSS_bytes_retired':sum(r['RSS_bytes'] for r in retired),'skipped':len(skipped)}),flush=True)
if __name__=='__main__':main()
