"""Observe current verified service identities; never dispatch scientific work."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write

def status(name):
 d=A/'service_owned_workflows_20261006'/name
 t=read(d/'service_execution.json') if (d/'service_execution.json').exists() else None
 i=read(d/'native_launch.json') if (d/'native_launch.json').exists() else None
 return {'status':t['status'] if t else 'running' if i and owned(i) else 'not_started_or_not_owned','terminal':t,'identity':i}

def main():
 data=read(A/'unified_completed_parent_shared_publication36_routes_v1_20261011.json')
 names=[n for n,_ in data['remaining_tasks']]
 names+=['actual184_registered_QA_main_complete_parent_bridge30_v1_20261011','recovery35_StockTopPairEmbedding48_selected_native14_v8_20261010','main_publisher_reboot_v12_20261011','actual_user_stop1300_guard_v1_20261011','actual_shared_publication_board_loader_controls_v1_20261011','actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011','actual_class10_after183_completed17_main_v1_20261011']
 for tag,title in [('rank20class10','Rank20Class10'),('rank20class25','Rank20Class25'),('rank60','Rank60')]:
  names += [f'actual_stock_{tag}_embedding_small512_restart_v1_20261011',f'Stock{title}Embedding_actual_mature_fixture_CPU_v1_20261011',f'Stock{title}EmbeddingSmall512_independent_small_CPU_v1_20261011',f'actual_stock_{tag}_embedding_small512_bank6_v1_20261011',f'Stock{title}EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011',f'actual_stock_{tag}_embedding_six_state_native42_v1_20261011',f'actual_stock_{tag}_embedding_after175_fast17_screen_v1_20261011',f'actual_stock_{tag}_embedding_after175_large_allocation29_screen_v1_20261011',f'actual_stock_{tag}_embedding_eleven_parent_callbacks_CPU_v1_20261011',f'actual_stock_{tag}_native42_and_fast46_queue_v1_20261011',f'actual_stock_{tag}_objective_stages_main_v1_20261011']
 names += ['actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011','actual_recent252_rank60_mature_population_CPU_v2_20261011','actual_rank60_first_mature_boundary_and_gaps_CPU_v1_20261011','actual_stock_rank20class25_BCE_own6_full5_queue_v1_20261011','actual_stock_rank20class10_objective_stages_main_v2_20261011','actual_rank60_shared_runtime36_CPU_sources_main_v1_20261011']
 while True:
  c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');now=datetime.now(timezone(timedelta(hours=8)))
  services={n:status(n) for n in dict.fromkeys(names)};rounds={};science={}
  for n in range(183,199):
   p=A/f'github_validation_sync_main_20261005/round{n}_receipt.json';q=A/f'optimization_20261003_r{n}/full_registration_execution.json'
   rounds[str(n)]={'receipt':read(p) if p.exists() else None,'full_registration':read(q) if q.exists() else None}
  for tag,title in [('rank20class10','Rank20Class10'),('rank20class25','Rank20Class25'),('rank60','Rank60')]:
   bank=Path('E:/赛题五_本机临时')/f'stock_{tag}_embedding_small512_BF16_bank6_v1_20261011';years=[];counts={}
   for y in range(2020,2026):
    p=bank/str(y)/'info.json'
    if p.exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model':years.append(y)
   for kind,count in [('high_impact17',17),('large_allocation29',29)]:
    folder=Path('E:/赛题五_本机临时')/f'Stock{title}EmbeddingSmall512_after175_{kind}_screen_v1_20261011';rows=[read(p) for p in folder.glob('case*_official.json')]
    counts[kind]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
   science[tag]={'completed_annual_years':years,'official_scores':counts}
  folder=Path('E:/赛题五_本机临时/StockRank20Class10EmbeddingSmall512_after183_high_impact17_screen_v1_20261011');rows=[read(p) for p in folder.glob('case*_official.json')]
  science['class10_after183']={'completed':len(rows),'expected':17,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')
  state={'at_local':now.isoformat(),'stop_at_local':c['stop_at_local'],'science':science,'services':services,'rounds':rounds,'latest_fully_qualified_delivery':delivery,'pending_cached_highest_S':.4514130257498636,'pending_cached_highest_submission_qualified':delivery['official_score']>=.4514130257498636,'available_memory_bytes':psutil.virtual_memory().available,'D_free_bytes':psutil.disk_usage('D:/').free,'E_free_bytes':psutil.disk_usage('E:/').free,'goal_exhaustion_proven':False}
  write(A/'optimization_live_progress_v115_20261011.json',state);write(A/'actual_optimization_fast_runtime_handoff_v216_20261011.json',state)
  lines=[f'更新时间：{now.isoformat()}；用户截止13:00。',f'已完全核验交付：第{delivery["selected_round"]}轮，S={delivery["official_score"]}。更高缓存分数尚待提交核验。']
  lines += [f'{tag}：{row}' for tag,row in science.items()]
  for n,row in rounds.items():lines.append(f'第{n}轮：'+('main '+row['receipt']['commit'] if row['receipt'] else '未完成main发布'))
  for n,row in services.items():
   if row['status']=='failed':lines.append(f'当前实际失败：{n}；{row["terminal"]["failure"]}')
  for name in ['optimization_live_progress_v115_20261011.md','optimization_live_progress_current_20261010.md']:
   p=A/name;q=p.with_name(p.name+'.115.tmp');q.write_text('\n\n'.join(lines)+'\n',encoding='utf8');q.replace(p)
  if now>=datetime.fromisoformat(c['stop_at_local']) or c['status']!='optimization_active_after_explicit_manual_resume':return
  time.sleep(20)
if __name__=='__main__':main()
