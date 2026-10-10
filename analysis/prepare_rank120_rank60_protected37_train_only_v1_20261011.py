"""Admit new long-horizon protected blends; reuse actual own models, never Test Y."""
from pathlib import Path
import sys,ast,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
PROOF=A/'rank120_rank60_after183_protected37_predeclared_sources_admission_v1_20261011.json'

def main():
 assert allowed()
 template=A/'run_rank60_rank20_after183_mixed49_screen_v1_20261011.py'
 original=template.read_text(encoding='utf8');tree=ast.parse(original)
 case=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cases')
 lines=original.splitlines();new_cases="""def cases():
    rows=[{'kind':'anchor183','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'rank120_weight':None}]
    for blend in (.125,.5,.875):
        for sign in (-1.,1.):
            for weight in (.004,.016,.064,.25,.5,1.):
                rows.append({'kind':'valid_pool_protection_v1','role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':.15,'rank120_weight':blend})
    assert len(rows)==37;return rows
"""
 source='\n'.join(lines[:case.lineno-1])+ '\n'+new_cases+'\n'+'\n'.join(lines[case.end_lineno:])+'\n'
 # Preserve the horizon-neutral mixing oracle; rename bank/pointer identifiers only.
 source=source.replace('StockRank60Rank20','NEW_DUAL_TITLE')
 source=source.replace('stock_rank60','stock_rank120').replace('StockRank60','StockRank120')
 source=source.replace('stock_rank20','stock_rank60').replace('StockRank20','StockRank60')
 source=source.replace('NEW_DUAL_TITLE','StockRank120Rank60')
 source=source.replace('rank60_weight','rank120_weight').replace('raw60','raw120')
 source=source.replace('actual_StockRank60EmbeddingSmall512_full5_independent_location_v1_20261009','actual_StockRank60EmbeddingSmall512_full5_independent_location_v1_20261011')
 source=source.replace('stock_rank60_embedding_small512_BF16_bank6_v1_20261010','stock_rank60_embedding_small512_BF16_bank6_v1_20261011')
 source=source.replace('actual_stock_rank60_embedding_six_state_native42_location_v1_20261010','actual_stock_rank60_embedding_six_state_native42_location_v1_20261011')
 source=source.replace("left['configuration']['label_horizon_trading_days']==20","left['configuration']['label_horizon_trading_days']==60")
 source=source.replace("right['configuration']['label_horizon_trading_days']==60","right['configuration']['label_horizon_trading_days']==120")
 source=source.replace("left['configuration']['target']=='y_rank_20mean' and right['configuration']['target']=='y_rank_60mean'","left['configuration']['target']=='y_rank_60mean' and right['configuration']['target']=='y_rank_120mean'")
 begin=source.index('    assert allowed()\n',source.index('def main():'))
 end=source.index("    release=read(A/'github_validation_sync_main_20261005/round183_receipt.json')",begin)
 gates="""    assert allowed()
    closed('actual_rank60_rank20_after183_mixed49_screen_v1_20261011')
    closed('actual_stock_rank120_embedding_after183_direct_allocation33_v1_20261011')
    closed('actual_stock_rank120_embedding_six_state_native42_v1_20261011')
    closed('actual_stock_rank60_embedding_six_state_native42_v1_20261011')
    closed('actual_stock_rank120_embedding_small512_bank6_v1_20261011')
    closed('StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
"""
 source=source[:begin]+gates+source[end:]
 source=source.replace('StockRank120Rank60_after183_higher_allocation49_screen_v1_20261011','StockRank120Rank60_after183_protected37_screen_v1_20261011')
 source=source.replace('rank60_rank20_after183_mixed49_predeclared_sources_admission_v1_20261011.json',PROOF.name)
 source=source.replace('stock_rank120_rank20_mixed_label_horizon_ID16_cross120_recent252_e64','stock_rank120_rank60_mixed_label_horizon_ID16_cross120_recent252_e64')
 source=source.replace('actual_mixed_rank60_rank20_49_TRAIN_only_official_scoring','actual_mixed_rank120_rank60_37_TRAIN_only_official_scoring')
 source=source.replace('passed49_mixed_rank60_rank20_TRAIN_only_CDF_both_signs_official_comparisons','passed37_mixed_rank120_rank60_TRAIN_only_protected_both_signs_official_comparisons')
 source=source.replace('actual_StockRank120Rank60_after183_mixed_horizon49_screen_location_v2_20261011','actual_StockRank120Rank60_after183_protected37_screen_location_v1_20261011')
 source=re.sub(r'(?<!\d)49(?!\d)','37',source)
 source=source.replace("'actual_nonidentity_full_controls':48","'actual_nonidentity_full_controls':36").replace("'actual_nonidentity_prefix_controls':144","'actual_nonidentity_prefix_controls':108")
 source=source.replace('frozen49_own_stock_embedding_return1d_after183_hypotheses','frozen37_two_mature_stock_embedding_horizons_protected_after183_hypotheses')
 source=source.replace("'own_new_loss_bank_training_complete':True","'both_actual_mature_horizon_banks_training_complete':True")
 driver=A/'run_rank120_rank60_after183_protected37_screen_v1_20261011.py'
 ast.parse(source);assert not driver.exists() and not PROOF.exists()
 assert 'label_horizon_trading_days\']==20' not in source and 'StockRank20EmbeddingSmall512_full5' not in source
 assert "'rank120_weight':blend" in source and "right['configuration']['target']=='y_rank_120mean'" in source
 assert 'rank20_two_seed_raw_signal_v1_20261010 as mixing' in source
 assert 'actual_full_scalar_bits_exact' in source and 'full_independent_Pandas_exact' in source
 assert '(80,260,975)' in source and 'assert_invariants(parent,value,dates,flags,valid' in source
 assert "'actual_nonidentity_full_controls':36" in source and "'actual_nonidentity_prefix_controls':108" in source
 driver.write_text(source,encoding='utf8')
 namespace={'__name__':'admission_cases_only'}
 case_node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='cases')
 exec(compile(ast.fix_missing_locations(ast.Module(body=[case_node],type_ignores=[])),'<37 predeclared TRAIN cases>','exec'),namespace)
 cases=namespace['cases']();assert len(cases)==37 and len({repr(r) for r in cases})==37
 paths=[Path(__file__),template,driver,A/'rank20_two_seed_raw_signal_v1_20261010.py',A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json',A/'actual_rank60_120_direct_own_pointer_aliases_v2_20261011.json']
 for horizon in [60,120]:
  pointer=A/f'actual_StockRank{horizon}EmbeddingSmall512_full5_independent_location_v1_20261011.json'
  full=Path(read(pointer)['output']);assert read(full/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
  paths += [pointer,full/'verification.json']
 create(PROOF,{'status':'compiled37_predeclared_new60_120_protected_blends_before_controls_or_scores',
  'input_sha256':{str(p):sha(p) for p in paths},'cases':cases,'parent_round':183,
  'distinct_horizons':[60,120],'fresh_native_fits':0,'new_scores_not_yet_claimed':True,
  'actual_full_scalar_and_Pandas_and108_prefix_controls_required':True,
  'two_prior_score_streams_must_complete_before_dispatch':True,
  'future_X_read':False,'test_labels_read':False,'new_candidate_native_and_full_inference_pending':True})
 from start_fast_completed_owned_service_v1_20261011 import start_service
 assert allowed()
 print(start_service('actual_rank120_rank60_after183_protected37_screen_v1_20261011',driver.name,[],{str(driver):sha(driver),str(PROOF):sha(PROOF)}),flush=True)

if __name__=='__main__':main()
