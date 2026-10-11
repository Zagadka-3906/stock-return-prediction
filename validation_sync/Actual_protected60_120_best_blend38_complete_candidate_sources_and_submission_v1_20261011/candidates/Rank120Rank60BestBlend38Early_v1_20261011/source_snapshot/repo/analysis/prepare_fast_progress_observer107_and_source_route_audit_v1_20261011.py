from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'monitor_reboot_optimization_v106_20261011.py';new=A/'monitor_reboot_optimization_v107_20261011.py';assert not new.exists()
 text=old.read_text(encoding='utf8').replace('v106','v107').replace('.106.tmp','.107.tmp').replace('handoff_v189','handoff_v191').replace('range(182,193)','range(182,195)')
 names=['Rank10Rank20Higher193_complete51_family_v4_20261011','actual_rank10_rank20_higher51_after192_normalization_v1_20261011','actual_rank10_rank20_higher51_selected_native14_v1_20261011','actual_rank10_rank20_mixed_selected_native14_v1_20261011','actual_Rank10_full5_native42_Higher193_Tail4_CPU6_sources_main_v1_20261011','actual_stock_rank20tail4_embedding_small512_restart_v2_20261011','StockRank20Tail4EmbeddingSmall512_independent_small_CPU_v1_20261011','actual_stock_rank20tail4_embedding_small512_bank6_v1_20261011','StockRank20Tail4EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank20tail4_own_training_and_full5_queue_v3_20261011','actual_stock_rank20tail4_embedding_six_state_native42_v1_20261011','actual_stock_rank20tail4_embedding_after175_fast17_screen_v1_20261011','actual_stock_rank20tail4_embedding_after175_large_allocation29_screen_v1_20261011','actual_stock_rank20tail4_objective_stages_main_v2_20261011','actual_stock_rank20tail4_embedding_eleven_parent_callbacks_CPU_v1_20261011','actual_stock_rank20tail4_embedding48_after193_normalization_queue_v1_20261011','StockRank20Tail4Embedding48_selected_native14_v1_20261011','StockRank20Tail4Embedding194_complete48_family_v1_20261011','actual_rank20tail4_official46_main_receipt_alias_v1_20261011']
 text=text.replace(' while True:\n', ' names+='+repr(names)+'\n while True:\n',1)
 needle="  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json');state="
 extra="""  tailbank=Path('E:/赛题五_本机临时/stock_rank20tail4_embedding_small512_BF16_bank6_v1_20261011');taily=[]
  for y in range(2020,2026):
   p=tailbank/str(y)/'info.json'
   if p.exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model':taily.append(y)
  tailcounts={}
  for kind,count in [('high_impact17',17),('large_allocation29',29)]:
   folder=Path('E:/赛题五_本机临时')/f'StockRank20Tail4EmbeddingSmall512_after175_{kind}_screen_v1_20261011';rows=[read(p) for p in folder.glob('case*_official.json')]
   tailcounts[kind]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
"""
 assert text.count(needle)==1;text=text.replace(needle,extra+needle)
 text=text.replace("'rank10_46_scores':counts,","'rank10_46_scores':counts,'rank20tail4_completed_annual_years':taily,'rank20tail4_46_scores':tailcounts,")
 text=text.replace("  for kind,row in counts.items():", "  lines.append(f'加权二十日模型已完成年度：{taily}；实际评分进度：{tailcounts}。')\n  for kind,row in counts.items():")
 compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
 row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v106_20261011/native_launch.json');stack=None
 if owned(row):
  p=psutil.Process(row['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout
  assert 'main (monitor_reboot_optimization_v106_20261011.py:' in stack,stack
  retire(row,'Observer107 includes actual weighted-loss annual6 and 46 scores, higher193 and full194, no scientific termination')
 proof=A/'fast_progress_observer107_source_route_audit_v1_20261011.json'
 create(proof,{'status':'compiled_observer107_tracks_real_new_tail4_and_higher193_and194','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,A/'stock_rank20tail4_embedding194_full_execution_sources_admission_v1_20261011.json']},'retired_exact_idle_observer':row,'actual_stack':stack,'known_pending_source_routing_issue':{'source':'normalize_completed_stock_rank10_embedding_complete48_after191_v1_20261011.py','legacy_folder_suffix':'screen_v1_20261010','actual_folder_suffix':'screen_v1_20261011','passed192_not_claimed':True},'new_fits':0,'new_scores':0})
 assert allowed();r=start_service('actual_fast_optimization_progress_reboot_v107_20261011',new.name,[],{str(new):sha(new),str(proof):sha(proof)});create(A/'actual_fast_optimization_progress_reboot_v107_20261011_activation.json',r)
 print({'observer107_actual_launched':True},flush=True)
if __name__=='__main__':main()
