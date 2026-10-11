"""Observe current verified service identities; never dispatch scientific work."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,psutil,re
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
 routes37=read(A/'actual_latest183_parent196198_routes37_v1_20261011.json');aliases={**data['service_aliases'],**routes37['service_aliases']}
 aliases['actual_stock_rank60_native42_and_fast46_queue_v1_20261011']='actual_stock_rank60_native42_and_fast46_queue_v2_20261011'
 routes38=read(A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json');routes40=read(A/'actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json')
 aliases.update(routes38['service_aliases']);aliases.update(routes40['service_alias_updates'])
 aliases['actual_stock_rank120_own6_full5_native42_direct33_queue_v1_20261011']='actual_stock_rank120_own6_full5_native42_direct33_queue_v2_20261011'
 aliases['recovery15_StockRank20Seed10Embedding186_round186_full_registration_v1_20261010']='actual186_registered_QA_main_resume39_v1_20261011'
 for proof_name in ['actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json','actual_scratch_only_and_sealing_sources42_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases43_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases44_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json']:
  proof=read(A/proof_name);aliases.update(proof['service_alias_updates']);names += [n for n,d in proof['tasks']]
 aliases['actual186_registered_QA_main_resume39_v1_20261011']='actual186_complete_parent_bridge41_v1_20261011'
 aliases['actual186_complete_parent_bridge40_v1_20261011']='actual186_complete_parent_bridge41_v1_20261011'
 aliases['actual_StockRank60Fixed17Early2_selected_candidate_sealing_v2_20261011']='actual_StockRank60Fixed17Early2_selected_candidate_sealing_v3_20261011'
 aliases['actual_early_fixed60_complete_candidate_and_own_aliases_main_v1_20261011']='actual_early_fixed60_complete_candidate_and_own_aliases_main_v2_20261011'
 aliases['actual_rank120_rank60_after183_protected37_screen_v1_20261011']='actual_rank120_rank60_after183_protected37_screen_v2_20261011'
 names += ['actual_rank120_rank60_after183_protected37_screen_v2_20261011','actual_stock_rank60_after183_protected_fraction38_screen_v1_20261011']
 for n in list(aliases):
  if 'Rank20TwoSeed187_round187_full_registration' in n:aliases[n]='actual187_registered_QA_main_resume45_v1_20261011'
 names += ['actual187_registered_QA_main_resume45_v1_20261011','actual_rank120_rank60_protected_twelve_callbacks_CPU_v1_20261011','actual_rank120_rank60_protected37_early_normalization_v1_20261011','actual_rank120_rank60_protected37_early_selected_native14_v1_20261011','Rank120Rank60ProtectedEarly_selected_candidate_preparation_v1_20261011','Rank120Rank60ProtectedEarly_selected_candidate_sealing_v1_20261011','actual_protected60_120_37_candidate_and_tuple45_sources_main_v1_20261011','actual_protected60_120_37_complete_candidate_main_v1_20261011','actual_rank60_seed10_own6_and_two_seed37_predeclared_sources_main_v1_20261011','actual_rank60_seed10_pure33_and_two_seed37_completed70_main_v1_20261011']
 p46=read(A/'actual_fraction38_gate_only_routes46_admission_v1_20261011.json');aliases.update(p46['service_alias_updates']);names += [n for n,d in p46['tasks']]
 for filename in ['actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json','actual_failed_future202_206_routes49_admission_v1_20261011.json','actual_current_publication_paths_and_prospective50_admission_v1_20261011.json']:
  latest=read(A/filename);aliases.update(latest['service_alias_updates']);names += [n for n,d in latest['tasks']]
 aliases['actual187_registered_QA_main_resume45_v1_20261011']='actual187_completed_QA_publication_only_resume47_v1_20261011'
 names += ['actual187_completed_QA_publication_only_resume47_v1_20261011','actual_current50_and_publication47_sources_main_v1_20261011']
 for filename in ['actual_current_publication_paths_and_prospective53_admission_v1_20261011.json','actual_verified_current55_publication_runtime_admission_v1_20261011.json','actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json']:
  latest=read(A/filename);aliases.update(latest['service_alias_updates']);names += [n for n,d in latest['tasks']]
 aliases['actual187_completed_QA_publication_only_resume47_v1_20261011']='actual187_complete_QA_main_finally_bridge57_v2_20261011'
 aliases['actual_rank120_rank60_protected37_completed_main_v1_20261011']='actual_rank120_rank60_protected37_completed_main_v2_20261011'
 names += ['actual187_complete_QA_main_finally_bridge57_v2_20261011','actual_rank120_rank60_protected37_completed_main_v2_20261011','actual_current58_and_completed187_bridge57_sources_main_v1_20261011','actual_verified_early37_alternate_submission_delivery_v1_20261011']
 names += ['actual_rank120_rank60_best_blend_fraction38_early_normalization_v1_20261011', 'actual_rank120_rank60_best_blend_fraction38_early_selected_native14_v1_20261011', 'Rank120Rank60BestBlend38Early_selected_candidate_preparation_v1_20261011', 'Rank120Rank60BestBlend38Early_selected_candidate_sealing_v1_20261011', 'actual_protected60_120_best_blend38_complete_candidate_main_v1_20261011', 'actual_verified_best_blend38_alternate_submission_delivery_v1_20261011', 'actual_rank60medium2048_own6_native42_direct33_queue_v2_20261011', 'actual_rank60medium_twelve_parent183_callbacks_CPU_v2_20261011', 'StockRank60MediumEmbedding_actual_mature_fixture_CPU_v2_20261011', 'actual_stock_rank60medium_embedding_medium2048_restart_v1_20261011', 'StockRank60MediumEmbeddingMedium2048_independent_small_CPU_v1_20261011', 'actual_stock_rank60medium_embedding_medium2048_bank6_v1_20261011', 'StockRank60MediumEmbeddingMedium2048_independent_full5_GPU_controls_v1_20261011', 'actual_stock_rank60medium_embedding_six_state_native42_v1_20261011', 'actual_stock_rank60medium_embedding_after183_direct_allocation33_v1_20261011', 'actual_rank60medium2048_pure33_completed_main_v1_20261011']
 raw59=read(A/'actual_raw_science_completed183_current59_admission_v1_20261011.json');aliases.update(raw59['service_alias_updates']);names += [n for n,d in raw59['tasks']]
 next60=read(A/'actual_future202_206_current60_raw59_admission_v1_20261011.json');aliases.update(next60['service_alias_updates']);names += [n for n,d in next60['tasks']]
 names += ['actual_rank120_rank60_bestblend40_after206_normalization_v1_20261011', 'actual_rank120_rank60_bestblend40_selected_native14_v1_20261011', 'Rank120Rank60BestBlend207_complete40_family_v1_20261011']
 names += ['actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011', 'actual_stock_rank60medium_best33_native14_v2_20261011', 'actual_StockRank60MediumBest33Early_selected_candidate_preparation_v2_20261011', 'actual_StockRank60MediumBest33Early_selected_candidate_sealing_v3_20261011', 'actual_rank60medium2048_best33_complete_candidate_main_v1_20261011', 'actual_verified_rank60medium2048_best33_alternate_delivery_v1_20261011', 'actual_medium2048_best33_candidate_predeclared_sources_main_v1_20261011']
 def current(n):
  canonical=re.sub(r'^recovery\d+_','',n)
  if n not in aliases and canonical in aliases:n=canonical
  seen=set()
  while n in aliases and aliases[n]!=n:
   assert n not in seen;seen.add(n);n=aliases[n]
  return n
 names += [n for n,d in routes37['tasks']]
 names += ['actual_stock_rank20class10_twelve_parent183_callbacks_CPU_v2_20261011','actual_rank60_rank20_twelve_parent183_callbacks_CPU_v1_20261011','actual_rank60_rank20_after183_mixed49_screen_v1_20261011','actual_183_parent37_and_mixed60_49_sources_main_v1_20261011']
 names+=['actual184_registered_QA_main_complete_parent_bridge30_v1_20261011','recovery35_StockTopPairEmbedding48_selected_native14_v8_20261010','main_publisher_reboot_v12_20261011','actual_user_stop1300_guard_v1_20261011','actual_shared_publication_board_loader_controls_v1_20261011','actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011','actual_class10_after183_completed17_main_v1_20261011']
 for tag,title in [('rank20class10','Rank20Class10'),('rank20class25','Rank20Class25'),('rank60','Rank60')]:
  names += [f'actual_stock_{tag}_embedding_small512_restart_v1_20261011',f'Stock{title}Embedding_actual_mature_fixture_CPU_v1_20261011',f'Stock{title}EmbeddingSmall512_independent_small_CPU_v1_20261011',f'actual_stock_{tag}_embedding_small512_bank6_v1_20261011',f'Stock{title}EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011',f'actual_stock_{tag}_embedding_six_state_native42_v1_20261011',f'actual_stock_{tag}_embedding_after175_fast17_screen_v1_20261011',f'actual_stock_{tag}_embedding_after175_large_allocation29_screen_v1_20261011',f'actual_stock_{tag}_embedding_eleven_parent_callbacks_CPU_v1_20261011',f'actual_stock_{tag}_native42_and_fast46_queue_v1_20261011',f'actual_stock_{tag}_objective_stages_main_v1_20261011']
 names += ['actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011','actual_recent252_rank60_mature_population_CPU_v2_20261011','actual_rank60_first_mature_boundary_and_gaps_CPU_v1_20261011','actual_stock_rank20class25_BCE_own6_full5_queue_v1_20261011','actual_stock_rank20class10_objective_stages_main_v2_20261011','actual_rank60_shared_runtime36_CPU_sources_main_v1_20261011']
 names += ['recovery31_StockPairRankEmbedding184_complete48_family_v9_20261010','actual_stock_rank60_complete198_factory_v1_20261011','actual_stock_rank60_embedding48_after197_normalization_queue_v1_20261011','StockRank60Embedding48_selected_native14_v1_20261011','StockRank60Embedding198_complete48_family_v1_20261011','actual_rank60_official46_main_receipt_alias_v1_20261011']
 names += ['actual_rank60_rank20_mixed51_after198_normalization_v1_20261011', 'actual_rank60_rank20_mixed51_selected_native14_v1_20261011', 'Rank60Rank20Mixed199_complete51_family_v4_20261011', 'actual_complete199_sources_main_v1_20261011', 'actual_rank60_rank20_after183_completed49_main_v1_20261011', 'actual_new_closed_main_browser_compression_v3_20261011', 'actual_fast_dispatch_sources_main_v1_20261011']
 names += ['actual_stock_rank60_embedding_after183_direct_allocation33_v1_20261011', 'actual_rank60_after183_completed33_main_v1_20261011', 'actual_rank60_direct33_predeclared_CPU_sources_main_v1_20261011', 'actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011', 'StockRank60DirectEmbedding35_selected_native14_v6_20261011', 'StockRank60DirectEmbedding200_complete35_family_v6_20261011', 'actual_complete200_actual_v6_sources_main_v1_20261011']
 names += ['actual_stock_rank120_own6_full5_native42_direct33_queue_v1_20261011', 'StockRank120Embedding_actual_mature_fixture_CPU_v1_20261011', 'StockRank120EmbeddingSmall512_independent_small_CPU_v1_20261011', 'actual_stock_rank120_embedding_small512_restart_v1_20261011', 'actual_stock_rank120_embedding_small512_bank6_v1_20261011', 'StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011', 'actual_stock_rank120_embedding_six_state_native42_v1_20261011', 'actual_stock_rank120_embedding_after183_direct_allocation33_v1_20261011', 'actual_rank120_after183_completed33_main_v1_20261011', 'actual_rank120_actual31_CPU_sources_main_v1_20261011']
 names += [n for n,d in routes40['tasks']]
 names += ['actual186_registered_QA_main_resume39_v1_20261011', 'actual186_complete_parent_bridge40_v1_20261011', 'actual_stock_rank120_objective_stages_main_v1_20261011']
 names += ['actual_stock_rank120_direct_embedding35_after200_normalization_queue_v7_20261011', 'StockRank120DirectEmbedding35_selected_native14_v7_20261011', 'StockRank120DirectEmbedding201_complete35_family_v7_20261011', 'actual_StockRank60Fixed17Early2_selected_candidate_preparation_v2_20261011', 'actual_StockRank60Fixed17Early2_selected_candidate_sealing_v2_20261011', 'actual_early_fixed60_complete_candidate_and_own_aliases_main_v1_20261011', 'actual_shared_report_controls_and_fixed60_case17_main_v3_20261011', 'actual_stock_rank60_fixed_leading_case17_native14_v2_20261011', 'actual_shared_live_ranking_report180_reader_controls_v1_20261011', 'actual_shared_live_ranking_report_scope_controls_v1_20261011']
 names += ['actual_stock_rank60seed10_embedding_small512_restart_v1_20261011','StockRank60Seed10EmbeddingSmall512_independent_small_CPU_v1_20261011','actual_stock_rank60seed10_embedding_small512_bank6_v1_20261011','StockRank60Seed10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank60seed10_embedding_six_state_native42_v1_20261011','actual_stock_rank60seed10_embedding_after183_direct_allocation33_v1_20261011','actual_rank60_two_seed_after183_protected37_screen_v1_20261011','actual_protected37_fraction38_completed75_main_v1_20261011','actual_report_reader15_current44_and_protected37_fraction38_sources_main_v1_20261011']
 names += ['actual_recent504_rank60_mature_population_CPU_v1_20261011', 'actual_stock_rank60window504_embedding_small512_restart_v1_20261011', 'StockRank60Window504EmbeddingSmall512_independent_small_CPU_v1_20261011', 'actual_stock_rank60window504_embedding_small512_bank6_v1_20261011', 'StockRank60Window504EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011', 'actual_stock_rank60window504_embedding_six_state_native42_v1_20261011', 'actual_stock_rank60window504_embedding_after183_direct_allocation33_v1_20261011', 'actual_rank60_window504_own6_predeclared_sources_main_v1_20261011', 'actual_rank60_window504_pure33_completed_main_v1_20261011']
 names += ['actual_complete202_205_prospective_sources_main_v1_20261011', 'actual_near_protected39_after189_normalization_v1_20261011', 'actual_near_protected39_selected_native14_v1_20261011', 'actual_rank120_rank60_protected37_completed_main_v1_20261011', 'actual_rank120_rank60_protected39_after202_normalization_v1_20261011', 'actual_rank120_rank60_protected39_selected_native14_v1_20261011', 'actual_rank60_seed10_pure33_completed_main_v1_20261011', 'actual_rank60_two_seed_protected37_completed_main_v1_20261011', 'actual_rank60_two_seed_protected39_after204_normalization_v2_20261011', 'actual_rank60_two_seed_protected39_selected_native14_v2_20261011', 'actual_rank60_window504_pure33_completed_main_v1_20261011', 'actual_stock_rank60seed10_direct_embedding35_after203_normalization_queue_v1_20261011', 'actual_stock_rank60_fraction_embedding40_after201_normalization_queue_v1_20261011', 'actual_stock_rank60_fraction_embedding40_after201_normalization_queue_v2_20261011', 'Rank120Rank60Protected203_complete39_family_v1_20261011', 'Rank60TwoSeedProtected205_complete39_family_v2_20261011', 'recovery14_actual_near_protected39_after189_normalization_v1_20261011', 'recovery14_actual_near_protected39_selected_native14_v1_20261011', 'recovery15_actual_near_protected39_after189_normalization_v1_20261011', 'recovery15_actual_near_protected39_selected_native14_v1_20261011', 'recovery16_actual_near_protected39_after189_normalization_v1_20261011', 'recovery16_actual_near_protected39_selected_native14_v1_20261011', 'recovery19_actual_near_protected39_after189_normalization_v1_20261011', 'recovery19_actual_near_protected39_selected_native14_v1_20261011', 'recovery21_actual_near_protected39_after189_normalization_v1_20261011', 'recovery21_actual_near_protected39_selected_native14_v1_20261011', 'recovery24_actual_near_protected39_after189_normalization_v1_20261011', 'recovery24_actual_near_protected39_selected_native14_v1_20261011', 'recovery31_actual_near_protected39_after189_normalization_v1_20261011', 'recovery31_actual_near_protected39_selected_native14_v1_20261011', 'recovery35_actual_near_protected39_after189_normalization_v1_20261011', 'recovery35_actual_near_protected39_selected_native14_v1_20261011', 'recovery36_actual_near_protected39_after189_normalization_v1_20261011', 'recovery36_actual_near_protected39_selected_native14_v1_20261011', 'recovery40_actual_near_protected39_after189_normalization_v1_20261011', 'recovery40_actual_near_protected39_selected_native14_v1_20261011', 'recovery41_actual_near_protected39_after189_normalization_v1_20261011', 'recovery41_actual_near_protected39_selected_native14_v1_20261011', 'recovery42_actual_near_protected39_after189_normalization_v1_20261011', 'recovery42_actual_near_protected39_selected_native14_v1_20261011', 'recovery43_actual_near_protected39_after189_normalization_v1_20261011', 'recovery43_actual_near_protected39_selected_native14_v1_20261011', 'recovery44_actual_near_protected39_after189_normalization_v1_20261011', 'recovery44_actual_near_protected39_selected_native14_v1_20261011', 'recovery45_actual_near_protected39_after189_normalization_v1_20261011', 'recovery45_actual_near_protected39_selected_native14_v1_20261011', 'StockRank60FractionEmbedding202_complete40_family_v1_20261011', 'StockRank60FractionEmbedding202_complete40_family_v2_20261011', 'StockRank60Seed10DirectEmbedding204_complete35_family_v1_20261011']
 names += ['actual_fraction38_completed_namespace_bridge_v1_20261011','actual_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011','actual_rank120_rank60_best_blend_fraction38_completed_main_v1_20261011','actual_best_blend38_and_prospective_gate46_sources_main_v1_20261011','actual_complete206_prospective_sources_main_v1_20261011']
 while True:
  c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');now=datetime.now(timezone(timedelta(hours=8)))
  dynamic=[]
  for number in range(185,207):
   for folder in A.glob(f'*{number}*complete_family*'):
    if folder.is_dir():
     for p in folder.glob('*_launch.json'):
      r=read(p)
      if 'name' in r:dynamic.append(r['name'])
  services={n:status(n) for n in dict.fromkeys(current(n) for n in names+dynamic)};rounds={};science={}
  for n in range(183,208):
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
  mixed=Path('E:/赛题五_本机临时/StockRank60Rank20_after183_higher_allocation49_screen_v1_20261011');mixedrows=[read(p) for p in mixed.glob('case*_official.json')]
  science['rank60_rank20_after183_mixed49']={'completed':len(mixedrows),'expected':49,'best_S':max((r['connected_final_score'] for r in mixedrows),default=None),'qualification_pending':True}
  direct=Path('E:/赛题五_本机临时/StockRank60EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011');directrows=[read(p) for p in direct.glob('case*_official.json')]
  science['rank60_pure_after183_direct33']={'completed':len(directrows),'expected':33,'best_S':max((r['connected_final_score'] for r in directrows),default=None),'qualification_pending':True}
  b120=Path('E:/赛题五_本机临时/stock_rank120_embedding_small512_BF16_bank6_v1_20261011');y120=[]
  for y in range(2020,2026):
   p=b120/str(y)/'info.json'
   if p.exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model':y120.append(y)
  f120=Path('E:/赛题五_本机临时/StockRank120EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011');r120=[read(p) for p in f120.glob('case*_official.json')]
  science['rank120_pure_after183_direct33']={'completed_annual_years':y120,'completed':len(r120),'expected':33,'best_S':max((r['connected_final_score'] for r in r120),default=None),'qualification_pending':True}
  for tag,folder,count in [('rank120_rank60_protected37','StockRank120Rank60_after183_protected37_screen_v1_20261011',37),('rank60_fraction_refinement38','StockRank60EmbeddingSmall512_after183_protected_fraction38_screen_v1_20261011',38)]:
   d=Path('E:/赛题五_本机临时')/folder;rows=[read(p) for p in d.glob('case*_official.json')]
   science[tag]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  seedbank=Path('E:/赛题五_本机临时/stock_rank60seed10_embedding_small512_BF16_bank6_v1_20261011')
  seedyears=[year for year in range(2020,2026) if (seedbank/str(year)/'info.json').exists()]
  science['rank60_seed10_own_bank']={'completed_annual_years':seedyears,'expected_models':6,'actual_stage':read(seedbank/'actual_stage.json') if (seedbank/'actual_stage.json').exists() else None}
  for tag,folder,count in [('rank60_seed10_pure33','StockRank60Seed10EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011',33),('rank60_two_seed_protected37','StockRank60TwoSeed_after183_protected37_screen_v1_20261011',37)]:
   directory=Path('E:/赛题五_本机临时')/folder;rows=[read(p) for p in directory.glob('case*_official.json')]
   science[tag]={'completed':len(rows),'expected':count,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  early=A/'StockRank60Fixed17Early2_selected_release_v2_20261011'
  stage={}
  for filename in ['selected_case_before_future_features.json','calibrated_csv_official.json','inference_ready.json','selected_candidate_ready_for_registration.json']:
   p=early/filename
   if p.exists():
    obj=read(p);stage[filename]={'status':obj.get('status'),'S':obj.get('selected_official_score',obj.get('metrics',{}).get('final_score',obj.get('best',{}).get('connected_final_score'))),'new_inference_claimed':obj.get('new_inference_claimed'),'actual_saved_native_models':obj.get('actual_saved_native_models'),'sealed_candidate_complete':obj.get('sealed_candidate_complete')}
  science['rank60_fixed17_early_full_candidate']={'stages':stage,'full_connected_board_and_release_qualification_pending':True}
  main_receipt=A/'Early_fixed60_full_candidate_and_actual_own_aliases_v2_main_receipt_v1_20261011.json'
  science['rank60_fixed17_early_full_candidate']['actual_main_receipt']=read(main_receipt) if main_receipt.exists() else None
  release=A/'Rank120Rank60ProtectedEarly_selected_release_v1_20261011';stages={}
  for filename in ['selected_case_before_future_features.json','calibrated_csv_official.json','inference_ready.json','selected_candidate_ready_for_registration.json']:
   path=release/filename
   if path.exists():
    value=read(path);stages[filename]={'status':value.get('status'),'S':value.get('metrics',{}).get('final_score',value.get('best',{}).get('connected_final_score')),'new_inference_claimed':value.get('new_inference_claimed'),'actual_saved_native_models':value.get('actual_saved_native_models'),'sealed_candidate_complete':value.get('sealed_candidate_complete')}
  science['rank60_rank120_all37_early_full_candidate']={'stages':stages,'full_board_pending':True}
  widebank=Path('E:/赛题五_本机临时/stock_rank60window504_embedding_small512_BF16_bank6_v1_20261011')
  wideyears=[year for year in range(2020,2026) if (widebank/str(year)/'info.json').exists()]
  science['rank60_window504_own_bank']={'completed_annual_years':wideyears,'expected_models':6,'actual_stage':read(widebank/'actual_stage.json') if (widebank/'actual_stage.json').exists() else None,'training_calendar_origins':504}
  folder=Path('E:/赛题五_本机临时/StockRank60Window504EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011');rows=[read(p) for p in folder.glob('case*_official.json')]
  science['rank60_window504_pure33']={'completed':len(rows),'expected':33,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  folder=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011');rows=[read(p) for p in folder.glob('case*_official.json')]
  science['rank120_rank60_best_blend_fraction38']={'completed':len(rows),'expected':38,'best_S':max((r['connected_final_score'] for r in rows),default=None),'qualification_pending':True}
  def score_values(value):
   if isinstance(value,dict):
    if value.get('best_S') is not None:yield value['best_S']
    for child in value.values():yield from score_values(child)
  pending_highest=max([.4514130257498636,*score_values(science)])
  alternate=A/'alternate_verified_early37_submission_delivery_v1_20261011.json'
  science['early37_alternate_submission_delivery']={'actual':read(alternate) if alternate.exists() else None,'full_connected_board_pending':True}
  alternate38=A/'alternate_verified_best_blend38_submission_delivery_v1_20261011.json'
  science['best_blend38_alternate_submission_delivery']={'actual':read(alternate38) if alternate38.exists() else None,'full_connected_board_pending':True}
  mb=Path('E:/赛题五_本机临时/stock_rank60medium_embedding_medium2048_BF16_bank6_v1_20261011')
  mf=Path('E:/赛题五_本机临时/StockRank60MediumEmbeddingMedium2048_after183_direct_allocation33_screen_v1_20261011')
  mr=[read(p) for p in mf.glob('case*_official.json')]
  science['rank60medium2048_own6_and_pure33']={'completed_annual_years':[y for y in range(2020,2026) if (mb/str(y)/'info.json').exists()],'expected_models':6,'completed_scores':len(mr),'expected_scores':33,'best_S':max((r['connected_final_score'] for r in mr),default=None),'qualification_pending':True}
  gain=A/'rank60medium2048_best33_gain_decision_v1_20261011.json'
  science['rank60medium2048_actual_gain_decision']={'actual':read(gain) if gain.exists() else None,'actual_full_candidate_not_yet_claimed':not (A/'alternate_verified_rank60medium2048_best33_submission_delivery_v1_20261011.json').exists()}
  pending_highest=max([.4514130257498636,*score_values(science)])
  delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')
  state={'at_local':now.isoformat(),'stop_at_local':c['stop_at_local'],'science':science,'services':services,'rounds':rounds,'latest_fully_qualified_delivery':delivery,'pending_cached_highest_S':pending_highest,'pending_cached_highest_submission_qualified':delivery['official_score']>=pending_highest,'available_memory_bytes':psutil.virtual_memory().available,'D_free_bytes':psutil.disk_usage('D:/').free,'E_free_bytes':psutil.disk_usage('E:/').free,'goal_exhaustion_proven':False}
  write(A/'optimization_live_progress_v134_20261011.json',state);write(A/'actual_optimization_fast_runtime_handoff_v267_20261011.json',state)
  lines=[f'更新时间：{now.isoformat()}；用户截止13:00。',f'已完全核验交付：第{delivery["selected_round"]}轮，S={delivery["official_score"]}。更高缓存分数尚待提交核验。']
  lines += [f'{tag}：{row}' for tag,row in science.items()]
  for n,row in rounds.items():lines.append(f'第{n}轮：'+('main '+row['receipt']['commit'] if row['receipt'] else '未完成main发布'))
  for n,row in services.items():
   if row['status']=='failed':lines.append(f'当前实际失败：{n}；{row["terminal"]["failure"]}')
  for name in ['optimization_live_progress_v134_20261011.md','optimization_live_progress_current_20261010.md']:
   p=A/name;q=p.with_name(p.name+'.134.tmp');q.write_text('\n\n'.join(lines)+'\n',encoding='utf8');q.replace(p)
  if now>=datetime.fromisoformat(c['stop_at_local']) or c['status']!='optimization_active_after_explicit_manual_resume':return
  time.sleep(20)
if __name__=='__main__':main()
