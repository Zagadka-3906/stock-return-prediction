from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write
def status(n):
 f=A/'service_owned_workflows_20261006'/n
 terminal=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None
 identity=read(f/'native_launch.json') if (f/'native_launch.json').exists() else None
 return {'status':terminal['status'] if terminal else 'running' if identity and owned(identity) else 'not_started_or_not_owned','terminal':terminal,'identity':identity}
def main():
 r15=read(A/'actual183_inner_completion_recovery_routes_v15_20261011.json');r16=read(A/'cached149_39_27_exact_wrapper_recovery_routes_v16_20261011.json')
 names=['actual_rank10_rank20_after175_higher_allocation49_screen_v1_20261011','actual_rank10_rank20_higher49_completed_official_main_v1_20261011','actual_higher_potential95_routes15_16_sources_main_v1_20261011',*[n for n,d in r15['remaining_tasks'][:-11]],*[n for n,d in r16['remaining_tasks']],*[n for n in r15['service_aliases'].values() if n.startswith('recovery15_') and ('183' in n or '184' in n)],'actual_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011','actual_stock_rank10_embedding_small512_restart_v1_20261011','StockRank10EmbeddingSmall512_independent_small_CPU_v1_20261011','actual_stock_rank10_embedding_small512_bank6_v1_20261011','StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank10_embedding_six_state_native42_v1_20261011','actual_stock_rank10_embedding_after175_fast17_screen_v1_20261011','actual_stock_rank10_embedding_after175_large_allocation29_screen_v1_20261011','actual_stock_rank10_objective_stages_main_v3_20261011','actual_rank10_official46_main_receipt_alias_v1_20261011','actual_stock_rank10_embedding48_after191_normalization_queue_v1_20261011','StockRank10Embedding48_selected_native14_v1_20261011','StockRank10Embedding192_complete48_family_v1_20261011','main_publisher_reboot_v12_20261011','actual_user_stop1100_reboot_guard_v2_20261011']
 names+=['Rank10Rank20Higher193_complete51_family_v4_20261011', 'actual_rank10_rank20_higher51_after192_normalization_v1_20261011', 'actual_rank10_rank20_higher51_selected_native14_v1_20261011', 'actual_rank10_rank20_mixed_selected_native14_v1_20261011', 'actual_Rank10_full5_native42_Higher193_Tail4_CPU6_sources_main_v1_20261011', 'actual_stock_rank20tail4_embedding_small512_restart_v2_20261011', 'StockRank20Tail4EmbeddingSmall512_independent_small_CPU_v1_20261011', 'actual_stock_rank20tail4_embedding_small512_bank6_v1_20261011', 'StockRank20Tail4EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011', 'actual_stock_rank20tail4_own_training_and_full5_queue_v3_20261011', 'actual_stock_rank20tail4_embedding_six_state_native42_v1_20261011', 'actual_stock_rank20tail4_embedding_after175_fast17_screen_v1_20261011', 'actual_stock_rank20tail4_embedding_after175_large_allocation29_screen_v1_20261011', 'actual_stock_rank20tail4_objective_stages_main_v2_20261011', 'actual_stock_rank20tail4_embedding_eleven_parent_callbacks_CPU_v1_20261011', 'actual_stock_rank20tail4_embedding48_after193_normalization_queue_v1_20261011', 'StockRank20Tail4Embedding48_selected_native14_v1_20261011', 'StockRank20Tail4Embedding194_complete48_family_v1_20261011', 'actual_rank20tail4_official46_main_receipt_alias_v1_20261011']
 while True:
  control=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');now=datetime.now(timezone(timedelta(hours=8)))
  services={n:status(n) for n in dict.fromkeys(names)};rounds={}
  for n in range(182,195):
   p=A/f'github_validation_sync_main_20261005/round{n}_receipt.json';q=A/f'optimization_20261003_r{n}/full_registration_execution.json'
   rounds[str(n)]={'receipt':read(p) if p.exists() else None,'full_registration':read(q) if q.exists() else None}
  bank=Path('E:/赛题五_本机临时/stock_rank10_embedding_small512_BF16_bank6_v1_20261011');years=[]
  for y in range(2020,2026):
   p=bank/str(y)/'info.json'
   if p.exists():
    info=read(p)
    if info['status']=='passed_actual_complete_mature_BF16_micro_annual_model':years.append(y)
  counts={}
  for kind,count in [('high_impact17',17),('large_allocation29',29)]:
   folder=Path('E:/赛题五_本机临时')/f'StockRank10EmbeddingSmall512_after175_{kind}_screen_v1_20261011';files=list(folder.glob('case*_official.json'))
   rows=[read(p) for p in files];counts[kind]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  mixedfolder=Path('E:/赛题五_本机临时/StockRank10Rank20_after175_higher_allocation49_screen_v1_20261011');mixedrows=[read(p) for p in mixedfolder.glob('case*_official.json')]
  counts['rank10_rank20_higher49']={'completed':len(mixedrows),'expected':49,'best_S':max((r['connected_final_score'] for r in mixedrows),default=None),'qualification_pending':True}
  tailbank=Path('E:/赛题五_本机临时/stock_rank20tail4_embedding_small512_BF16_bank6_v1_20261011');taily=[]
  for y in range(2020,2026):
   p=tailbank/str(y)/'info.json'
   if p.exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model':taily.append(y)
  tailcounts={}
  for kind,count in [('high_impact17',17),('large_allocation29',29)]:
   folder=Path('E:/赛题五_本机临时')/f'StockRank20Tail4EmbeddingSmall512_after175_{kind}_screen_v1_20261011';rows=[read(p) for p in folder.glob('case*_official.json')]
   tailcounts[kind]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json');state={'at_local':now.isoformat(),'stop_at_local':control['stop_at_local'],'actual_completed_cached_score_cases':209,'actual_rank10_completed_annual_years':years,'rank10_46_scores':counts,'rank20tail4_completed_annual_years':taily,'rank20tail4_46_scores':tailcounts,'rounds':rounds,'services':services,'latest_fully_qualified_delivery':delivery,'pending_cached_highest_S':.4514130257498636,'pending_cached_highest_submission_qualified':delivery['official_score']>=.4514130257498636,'available_memory_bytes':psutil.virtual_memory().available,'D_free_bytes':psutil.disk_usage('D:/').free,'E_free_bytes':psutil.disk_usage('E:/').free,'goal_exhaustion_proven':False}
  write(A/'optimization_live_progress_v107_20261011.json',state);write(A/'actual_optimization_fast_runtime_handoff_v191_20261011.json',state)
  lines=[f'更新时间：{now.isoformat()}；按用户要求11:00停止。','当前优先真实十日成熟平均收益排序目标的独立六年度模型；209项已有评分全部复用。',f'十日模型已完成年度：{years}；待完成的年度训练、评分和提交资格均不记为通过。']
  lines.append(f'加权二十日模型已完成年度：{taily}；实际评分进度：{tailcounts}。')
  for kind,row in counts.items():lines.append(f"十日{kind}：{row['completed']}/{row['expected']}，目前TRAIN最高S={row['best_S']}。")
  for n,row in rounds.items():lines.append(f"第{n}轮完整登记：{row['full_registration']['status'] if row['full_registration'] else '待完成'}；main：{row['receipt']['commit'] if row['receipt'] else '待完成'}。")
  for n,row in services.items():
   if row['status']=='failed':lines.append(f"实际失败需修复：{n}；{row['terminal']['failure']}")
  for name in ['optimization_live_progress_v107_20261011.md','optimization_live_progress_current_20261010.md']:
   p=A/name;q=p.with_name(p.name+'.107.tmp');q.write_text('\n\n'.join(lines)+'\n',encoding='utf8');q.replace(p)
  if now>=datetime.fromisoformat(control['stop_at_local']) or control['status']!='optimization_active_after_explicit_manual_resume':return
  time.sleep(20)
if __name__=='__main__':main()
