from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'monitor_reboot_optimization_v109_20261011.py';new=A/'monitor_reboot_optimization_v110_20261011.py';assert not new.exists();text=old.read_text(encoding='utf8').replace('v109','v110').replace('.109.tmp','.110.tmp').replace('handoff_v193','handoff_v195').replace('按用户要求11:00停止','按用户要求13:00停止').replace('actual_user_stop1100_reboot_guard_v2_20261011','actual_user_stop1300_guard_v1_20261011')
 names=['actual_stock_rank20class10_BCE_own6_full5_queue_v1_20261011','actual_stock_rank20class10_balanced_BCE_CPU_v1_20261011','StockRank20Class10Embedding_actual_mature_fixture_CPU_v1_20261011','actual_stock_rank20class10_embedding_small512_restart_v1_20261011','StockRank20Class10EmbeddingSmall512_independent_small_CPU_v1_20261011','actual_stock_rank20class10_embedding_small512_bank6_v1_20261011','StockRank20Class10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank20class10_native42_and_fast46_queue_v1_20261011','actual_stock_rank20class10_embedding_six_state_native42_v1_20261011','actual_stock_rank20class10_embedding_after175_fast17_screen_v1_20261011','actual_stock_rank20class10_embedding_after175_large_allocation29_screen_v1_20261011','actual_stock_rank20class10_embedding_eleven_parent_callbacks_CPU_v1_20261011','actual_1300_deadline_Top10BCE_CPU_sources_main_v1_20261011']
 text=text.replace(' while True:\n',' names+='+repr(names)+'\n while True:\n',1)
 insert="""  classbank=Path('E:/赛题五_本机临时/stock_rank20class10_embedding_small512_BF16_bank6_v1_20261011');classyears=[]
  for y in range(2020,2026):
   p=classbank/str(y)/'info.json'
   if p.exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model':classyears.append(y)
  classcounts={}
  for kind,count in [('high_impact17',17),('large_allocation29',29)]:
   folder=Path('E:/赛题五_本机临时')/f'StockRank20Class10EmbeddingSmall512_after175_{kind}_screen_v1_20261011';rows=[read(p) for p in folder.glob('case*_official.json')]
   classcounts[kind]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
"""
 needle="  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json');state=";assert text.count(needle)==1;text=text.replace(needle,insert+needle)
 text=text.replace("'rank20tail4_46_scores':tailcounts,","'rank20tail4_46_scores':tailcounts,'rank20class10_completed_annual_years':classyears,'rank20class10_46_scores':classcounts,")
 text=text.replace("  for kind,row in counts.items():","  lines.append(f'新Top10二元分类已完成年度：{classyears}；官方评分进度：{classcounts}。')\n  for kind,row in counts.items():")
 compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
 row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v109_20261011/native_launch.json');stack=None
 if owned(row):
  p=psutil.Process(row['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout;assert 'main (monitor_reboot_optimization_v109_20261011.py:' in stack
  retire(row,'Observer110 follows actual13:00 user deadline and new BCE classification own6/scoring46; science preserved')
 proof=A/'actual_observer110_deadline13_and_classification_sources_admission_v1_20261011.json';paths=[Path(__file__),old,new,A/'stock_rank20class10_BCE_own6_sources_admission_v1_20261011.json',A/'stock_rank20class10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json',A/'user_requested_stop1300_until_manual_continue_v1_20261011/deadline_extension_verification.json',A/'activate_user_requested_stop1300_v1_20261011.py',A/'user_requested_stop1300_v1_20261011.py',ROOT/'AGENTS.md']
 create(proof,{'status':'compiled_actual13_guard_and_fresh_BCE_direction_observer110_before_own6_completion','input_sha256':{str(p):sha(p) for p in paths},'retired_exact_idle_observer':row,'actual_idle_stack':stack,'new_fits':0,'new_scores':0,'deadline':'2026-10-11T13:00:00+08:00','old11_deadline_superseded':True,'test_labels_read':False})
 assert allowed();r=start_service('actual_fast_optimization_progress_reboot_v110_20261011',new.name,[],{str(new):sha(new),str(proof):sha(proof)});create(A/'actual_fast_optimization_progress_reboot_v110_20261011_activation.json',r)
 publisher=A/'publish_actual_1300_deadline_Top10BCE_CPU_sources_main_v1_20261011.py';assert not publisher.exists()
 body="""from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_stock_rank20class10_balanced_BCE_CPU_v1_20261011');closed('StockRank20Class10Embedding_actual_mature_fixture_CPU_v1_20261011');closed('actual_stock_rank20class10_embedding_eleven_parent_callbacks_CPU_v1_20261011')
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths=[Path(__file__),template,ROOT/'AGENTS.md',A/'activate_user_requested_stop1300_v1_20261011.py',A/'user_requested_stop1300_v1_20261011.py',A/'user_requested_stop1300_until_manual_continue_v1_20261011/deadline_extension_verification.json',A/'user_requested_stop1300_until_manual_continue_v1_20261011/actual_schedule_activation.json',A/'user_requested_stop1300_until_manual_continue_v1_20261011/actual_1100_guard_retirement.json',A/'user_requested_stop1300_until_manual_continue_v1_20261011/schedule.json',A/'actual_observer110_deadline13_and_classification_sources_admission_v1_20261011.json']
 for pattern in ('*stock_rank20class10*20261011.py','*stock_rank20class10*20261011.json','*rank20class10*20261011.py','*rank20class10*20261011.json'):paths.extend(A.glob(pattern))
 for pp in [A/'stock_rank20class10_BCE_own6_sources_admission_v1_20261011.json',A/'stock_rank20class10_balanced_BCE_actual_CPU_controls_v1_20261011.json',A/'stock_rank20class10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json']:
  for name,d in read(pp)['input_sha256'].items():
   assert sha(name)==d,name
   if Path(name).suffix in ('.py','.json'):paths.append(Path(name))
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Actual_1300_deadline_Top10BCE_CPU_sources')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual13_deadline_and_Top10_mature20_binary_BCE_CPU6_fixture49153_callback11_passed_before_complete_own6_or_scores','deadline':'2026-10-11T13:00:00+08:00','old11_guard_exact_identity_retired':True,'actual_binary_loss_and_gradient_cases':6,'actual_mature_fixture_rows':49153,'actual_callback_checks':11,'own6_full5_official46_and_full195_not_completed':True,'new_fits_by_publication':0,'new_scores_by_publication':0,'test_labels_read':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\\n"+text[end:]
 driver=A/'publish_Actual_1300_deadline_Top10BCE_CPU_sources_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\\n');assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
"""
 compile(body,str(publisher),'exec');publisher.write_text(body,encoding='utf8',newline='\n')
 assert allowed();r=start_service('actual_1300_deadline_Top10BCE_CPU_sources_main_v1_20261011',publisher.name,[],{str(publisher):sha(publisher),str(proof):sha(proof)});create(A/'actual_1300_deadline_Top10BCE_CPU_sources_main_activation_v1_20261011.json',r)
 print({'observer110_actual13_deadline_and_new_BCE_CPU_main_queued':True},flush=True)
if __name__=='__main__':main()
