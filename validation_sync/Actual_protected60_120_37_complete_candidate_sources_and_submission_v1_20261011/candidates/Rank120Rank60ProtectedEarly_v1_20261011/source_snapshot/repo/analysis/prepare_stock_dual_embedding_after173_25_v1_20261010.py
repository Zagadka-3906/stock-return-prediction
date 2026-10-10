"""Predeclare complementary return/rank embedding consensus without extra fitting."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    source=A/'run_Dual120Consensus_after169_high_impact193_screen_v3_20261010.py';text=source.read_text(encoding='utf8')
    begin=text.index('def cases():');end=text.index('\ndef main():',begin)
    casecode="""def cases():
    rows=[{'kind':'anchor173','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'mean_weight':None}]
    for mixture in (.25,.5,.75):
        for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
            for weight in (.004,.016,.064,.25):rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':1.,'protect_fraction':.15,'mean_weight':mixture})
    assert len(rows)==25;return rows

"""
    text=text[:begin]+casecode+text[end:]
    begin=text.index("    closed('Cross120170_complete132_family_v5_20261010')");end=text.index('    import numpy as np,polars as pl,psutil',begin)
    gate="""    closed('StockEmbedding173_complete36_family_v3_20261010')
    closed('actual_stock_rank_embedding_after170_fast17_screen_v1_20261010')
    closed('actual_stock_rank_embedding_after170_completion_main_v55_20261010')
    closed('actual_stock_embedding_six_state_native42_v2_20261010')
    closed('actual_stock_rank_embedding_six_state_native42_v1_20261010')
    release=read(A/'github_validation_sync_main_20261005/round173_receipt.json')
    assert release['status']=='pushed_and_remote_head_verified' and release['scored_records']==36
"""
    text=text[:begin]+gate+text[end:]
    replacements={
      'neural_BF16_medium2048_cross120recent252rank5huber050_seed09_e64_bank6_v1_20261009':'stock_rank_embedding_small512_BF16_bank6_v1_20261010',
      'neural_BF16_medium2048_cross120recent252forward5huber050_seed09_e64_bank6_v1_20261009':'stock_embedding_small512_BF16_bank6_v1_20261010',
      'actual_BF16Cross120Recent252Rank5Huber050174_full5_independent_location_v1_20261009':'actual_StockRankEmbeddingSmall512_full5_independent_location_v1_20261009',
      'actual_BF16Cross120Recent252Rank5Huber050174_native42_calendar_location_v1_20261009':'actual_stock_rank_embedding_six_state_native42_location_v1_20261010',
      'actual_BF16Cross120Recent252Forward5Huber050173_full5_independent_location_v1_20261009':'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009',
      'actual_BF16Cross120Recent252Forward5Huber050173_native42_calendar_location_v1_20261009':'actual_stock_embedding_six_state_native42_location_v1_20261010',
      'Dual120Consensus_after169_high_impact193_screen_v1_20261010':'StockDualEmbedding_after173_high_impact25_screen_v1_20261010',
      'optimization_20261003_r169':'optimization_20261003_r173',
      'dual120mean5rank5_daily_rank_consensus':'stock_return1d_rank1d_embedding_daily_rank_consensus',
      'complete_parent169':'complete_parent173',
      "'parent_round':169":"'parent_round':173",
      "'kind']=='anchor169'":"'kind']=='anchor173'",
      "'expected_cases':193":"'expected_cases':25",
      "'new_quality_score_records':193":"'new_quality_score_records':25",
      "'actual_nonidentity_full_controls':192":"'actual_nonidentity_full_controls':24",
      "'actual_nonidentity_prefix_controls':576":"'actual_nonidentity_prefix_controls':72",
      'frozen_new193_dual120_rank_consensus':'frozen_new25_stock_return_and_rank_embedding_consensus',
      'actual_new_dual120_consensus193':'actual_new_stock_dual_embedding25',
      'passed193_actual_two_own120_banks_rank_consensus_cumulative169':'passed25_actual_two_stock_embedding_banks_rank_consensus_cumulative173',
    }
    for old,new in replacements.items():text=text.replace(old,new)
    dest=A/'run_stock_dual_embedding_after173_high_impact25_screen_v1_20261010.py';assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
    cases=__import__(dest.stem).cases();assert len(cases)==25 and cases[0]['kind']=='anchor173'
    assert "if c['kind']=='anchor173'" in text
    create(A/'stock_dual_embedding_after173_predeclared25_plan_v1_20261010.json',{'status':'predeclared25_before_any_stock_rank_embedding_quality_scores','cases':cases,'mean_weight_is_return_embedding_weight':True,'rank_weight_is_one_minus_mean_weight':True,'highest_complete_qualified_parent_round':173,'extra_training_fits':0,'physical_leaves_added_at_most':2,'expected_official_scores':25,'actual_nonidentity_full_controls_required':24,'actual_nonidentity_cold_controls_required':72,'all_peer_ranks_same_day_only':True,'future_X_read':False,'test_labels_read':False,'new_quality_scores':0,'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,dest,A/'dual_target_daily_rank_consensus_v1_20261010.py']}})
    row=start_service('actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010',dest.name,[],{str(dest):sha(dest)})
    create(A/'actual_stock_dual_embedding_after173_high_impact25_activation_v1_20261010.json',row)
    print({'actual_return_rank_ensemble25_queue':'started','new_fits':0,'new_scores':0},flush=True)
if __name__=='__main__':main()
