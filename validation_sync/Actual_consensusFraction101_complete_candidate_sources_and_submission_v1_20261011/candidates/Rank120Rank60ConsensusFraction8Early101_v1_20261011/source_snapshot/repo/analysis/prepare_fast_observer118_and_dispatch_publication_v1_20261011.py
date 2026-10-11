"""Track round199 and the faster real score scheduler; preserve scientific jobs."""
from pathlib import Path
import ast,sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 source=A/'monitor_verified_current_optimization_v117_20261011.py'
 text=source.read_text(encoding='utf8').replace('v117','v118').replace('v221','v223').replace('.117.tmp','.118.tmp').replace('range(185,199)','range(185,200)').replace('range(183,199)','range(183,200)')
 marker=' def current(n):'
 assert text.count(marker)==1
 text=text.replace(marker," aliases['actual_stock_rank60_native42_and_fast46_queue_v1_20261011']='actual_stock_rank60_native42_and_fast46_queue_v2_20261011'\n"+marker)
 extra=['actual_rank60_rank20_mixed51_after198_normalization_v1_20261011','actual_rank60_rank20_mixed51_selected_native14_v1_20261011','Rank60Rank20Mixed199_complete51_family_v4_20261011','actual_complete199_sources_main_v1_20261011','actual_rank60_rank20_after183_completed49_main_v1_20261011','actual_new_closed_main_browser_compression_v3_20261011','actual_fast_dispatch_sources_main_v1_20261011']
 assert text.count(' while True:')==1;text=text.replace(' while True:',' names += '+repr(extra)+'\n while True:')
 target=A/'monitor_verified_current_optimization_v118_20261011.py';ast.parse(text);assert not target.exists();target.write_text(text,encoding='utf8')
 f=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v117_20261011';row=read(f/'native_launch.json');assert owned(row)
 worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid'])
 assert not worker.children() and parent.create_time()==row['owned_parent_creation_time'] and parent.cmdline()[1:]==worker.cmdline()[1:]
 spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
 result=None
 for attempt in range(4):
  result=subprocess.run([str(spy),'dump','--pid',str(worker.pid)],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  if '(idle)' in result.stdout and 'main (monitor_verified_current_optimization_v117_20261011.py:' in result.stdout:break
  import time;time.sleep(1)
 assert '(idle)' in result.stdout and 'main (monitor_verified_current_optimization_v117_20261011.py:' in result.stdout
 proof={'status':'verified_idle_readonly_observer_replaced_for_199_and_actual_v2_score_scheduler','identity':row,'actual_stack':result.stdout,'scientific_jobs_terminated':0,'input_sha256':{str(source):sha(source),str(target):sha(target),str(Path(__file__)):sha(__file__)}}
 create(A/'fast_observer118_actual_admission_v1_20261011.json',proof)
 assert allowed() and owned(row) and not worker.children();worker.terminate();worker.wait(15);parent.terminate();parent.wait(15)
 create(f/'administrative_supersession_for_observer118_v1_20261011.json',proof)
 n=start_service('actual_fast_optimization_progress_reboot_v118_20261011',target.name,[],proof['input_sha256']);create(A/'fast_observer118_actual_activation_v1_20261011.json',n)
 paths=[Path(__file__),target,A/'fast_observer118_actual_admission_v1_20261011.json',A/'run_stock_rank60_native42_and_fast46_queue_v2_20261011.py',A/'admit_rank60_two_score_streams_v2_20261011.py',A/'rank60_two_score_streams_pre_retirement_v2_20261011.json',A/'actual_rank60_two_score_streams_v2_20261011_activation.json',A/'compress_new_completed_main_browser_profiles_v3_20261011.py']
 for name in ('actual_stock_rank60_native42_and_fast46_queue_v2_20261011','actual_stock_rank60_embedding_after175_fast17_screen_v1_20261011'):
  paths += [A/'service_owned_workflows_20261006'/name/p for p in ('job_definition.json','native_launch.json')]
 prefix='Fast_dispatch_actual_v2_observer118_sources'
 template=(A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py').read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources',prefix)
 lines=template.splitlines();i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'))
 lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 manifest={'status':'actual_childless_idle_scheduler_replaced_and_original_H60_fast17_score_driver_started','original_scientific_drivers_unchanged':True,'completed_native_cases':42,'completed_cold_cases':42,'score_completion_pending':True,'new_scores_or_fits_by_publication':0,'test_labels_read':False}
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s);lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','核验空闲调度器后并行启动原生60日评分；保留全部原检查并更新199进度监控',timeout=180)"
 p=A/'publish_frozen_fast_dispatch_v2_observer118_sources_v1_20261011.py';text='\n'.join(lines)+'\n';ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8')
 assert allowed();n=start_service('actual_fast_dispatch_sources_main_v1_20261011',p.name,[],{str(q):sha(q) for q in [p,*paths]});create(A/'actual_fast_dispatch_sources_main_activation_v1_20261011.json',n)
 print({'observer118_started':True,'actual_dispatch_proofs_publication_queued_main':True},flush=True)
if __name__=='__main__':main()
