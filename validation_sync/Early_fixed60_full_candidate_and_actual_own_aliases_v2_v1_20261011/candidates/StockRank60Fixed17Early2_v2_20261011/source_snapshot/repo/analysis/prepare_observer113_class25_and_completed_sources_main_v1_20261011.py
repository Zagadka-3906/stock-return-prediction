from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();old=A/'monitor_reboot_optimization_v112_20261011.py';new=A/'monitor_reboot_optimization_v113_20261011.py';assert not new.exists();s=old.read_text(encoding='utf8').replace('v112','v113').replace('.112.tmp','.113.tmp').replace('handoff_v200','handoff_v205')
 names=['actual_stock_rank20class25_BCE_own6_full5_queue_v1_20261011','actual_stock_rank20class25_balanced_BCE_CPU_v1_20261011','StockRank20Class25Embedding_actual_mature_fixture_CPU_v1_20261011','actual_stock_rank20class25_embedding_small512_restart_v1_20261011','StockRank20Class25EmbeddingSmall512_independent_small_CPU_v1_20261011','actual_stock_rank20class25_embedding_small512_bank6_v1_20261011','StockRank20Class25EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank20class25_native42_and_fast46_queue_v1_20261011','actual_stock_rank20class25_embedding_six_state_native42_v1_20261011','actual_stock_rank20class25_embedding_after175_fast17_screen_v1_20261011','actual_stock_rank20class25_embedding_after175_large_allocation29_screen_v1_20261011','actual_stock_rank20class25_embedding_eleven_parent_callbacks_CPU_v1_20261011','actual_stock_rank20class25_objective_stages_main_v1_20261011','actual_stock_rank20class25_CPU6_sources_main_v1_20261011','actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011','actual_class10_after183_completed17_main_v1_20261011']
 s=s.replace(' while True:\n',' names+='+repr(names)+'\n while True:\n',1)
 insert="""  class25bank=Path('E:/赛题五_本机临时/stock_rank20class25_embedding_small512_BF16_bank6_v1_20261011');class25years=[]
  for y in range(2020,2026):
   p=class25bank/str(y)/'info.json'
   if p.exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model':class25years.append(y)
  class25counts={}
  for kind,count in [('high_impact17',17),('large_allocation29',29)]:
   folder=Path('E:/赛题五_本机临时')/f'StockRank20Class25EmbeddingSmall512_after175_{kind}_screen_v1_20261011';rows=[read(p) for p in folder.glob('case*_official.json')]
   class25counts[kind]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  extra17folder=Path('E:/赛题五_本机临时/StockRank20Class10EmbeddingSmall512_after183_high_impact17_screen_v1_20261011');extra17rows=[read(p) for p in extra17folder.glob('case*_official.json')]
  class10after183={'completed':len(extra17rows),'expected':17,'best_S':max((r['connected_final_score'] for r in extra17rows),default=None),'qualification_pending':True}
"""
 needle="  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json');state=";assert s.count(needle)==1;s=s.replace(needle,insert+needle)
 s=s.replace("'rank20class10_46_scores':classcounts,","'rank20class10_46_scores':classcounts,'rank20class25_completed_annual_years':class25years,'rank20class25_46_scores':class25counts,'class10_after183_17':class10after183,")
 s=s.replace('  for kind,row in counts.items():',"  lines.append(f'Top25分类已完成年度：{class25years}；实际评分：{class25counts}。Top10与最佳183融合：{class10after183}。')\n  for kind,row in counts.items():")
 compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 row=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v112_20261011/native_launch.json');assert owned(row);p=psutil.Process(row['owned_worker_pid']);assert not p.children();r=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30);assert r.returncode==0 and 'main (monitor_reboot_optimization_v112_20261011.py:' in r.stdout;retire(row,'Observer113 follows actual newTop25 CPU6 and own6 plus latest183 Top10 screen17; science preserved')
 paths=[Path(__file__),old,new,A/'stock_rank20class25_BCE_own6_sources_admission_v1_20261011.json',A/'stock_rank20class25_balanced_BCE_actual_CPU_controls_v1_20261011.json',A/'stock_rank20class25_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json',A/'stock_rank20class10_latest_qualified183_predeclared17_sources_v1_20261011.json'];proof=A/'actual_observer113_class25_sources_admission_v1_20261011.json';create(proof,{'status':'compiled_actual_top25_CPU6_fixture49153_callback11_and_latest183_screen17_observer113','input_sha256':{str(p):sha(p) for p in paths},'retired_exact_idle_observer':row,'actual_idle_stack':r.stdout,'new_fits':0,'new_scores':0,'full_completion_claimed':False})
 assert allowed();r=start_service('actual_fast_optimization_progress_reboot_v113_20261011',new.name,[],{str(new):sha(new),str(proof):sha(proof)});create(A/'actual_fast_optimization_progress_reboot_v113_20261011_activation.json',r)
 oldstage=A/'run_stock_rank20class10_objective_actual_stages_main_v1_20261011.py';stage=A/'run_stock_rank20class25_objective_actual_stages_main_v1_20261011.py';assert not stage.exists();s=oldstage.read_text(encoding='utf8').replace('stock_rank20class10','stock_rank20class25').replace('StockRank20Class10','StockRank20Class25').replace('stockrank20class10','stockrank20class25').replace('top10_balanced','top25_balanced');compile(s,str(stage),'exec');stage.write_text(s,encoding='utf8',newline='\n')
 assert allowed();r=start_service('actual_stock_rank20class25_objective_stages_main_v1_20261011',stage.name,[],{str(stage):sha(stage),str(proof):sha(proof)});create(A/'actual_stock_rank20class25_objective_stages_main_activation_v1_20261011.json',r)
 publisher=A/'run_publish_stock_rank20class25_CPU6_sources_main_v1_20261011.py';assert allowed();r=start_service('actual_stock_rank20class25_CPU6_sources_main_v1_20261011',publisher.name,[],{str(publisher):sha(publisher),str(proof):sha(proof)});create(A/'actual_stock_rank20class25_CPU6_sources_main_activation_v1_20261011.json',r)
 print({'actual_observer113_and_Top25_CPU_and_stage_main_queued':True},flush=True)
if __name__=='__main__':main()
