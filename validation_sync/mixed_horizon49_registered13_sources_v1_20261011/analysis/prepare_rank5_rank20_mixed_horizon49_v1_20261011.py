"""Predeclare a new mixed-label-horizon ensemble of two completed independent model banks."""
from pathlib import Path
import sys,importlib,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();source=A/'run_rank20_two_seed_after175_complement49_screen_v1_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('StockRank20TwoSeed_after175_complement49_screen_v1_20261010','StockRank5Rank20_after175_mixed_horizon49_screen_v1_20261011')
    text=text.replace('stock_rank20seed10','stock_rank5').replace('StockRank20Seed10','StockRank5')
    text=text.replace('rank20_two_seed_complement49_predeclared_plan_v1_20261010.json','rank5_rank20_mixed_horizon49_predeclared_plan_v1_20261011.json')
    text=text.replace('actual_StockRank20TwoSeed_after175_complement49_screen_location_v1_20261010.json','actual_StockRank5Rank20_after175_mixed_horizon49_screen_location_v1_20261011.json')
    text=text.replace('second_seed_weight','rank5_weight').replace('stock_rank20_two_seed_ID16_cross120_recent252_e64','stock_rank5_rank20_mixed_label_horizon_ID16_cross120_recent252_e64')
    text=text.replace("for role in ('nonflag_valid','all_valid'):","for role in ('nonflag_valid',):")
    text=text.replace('(.00015625,.0003125,.000625,.00125)', '(.000078125,.00015625,.0003125,.000625,.00125,.0025,.005,.01)')
    start=text.index('    for year in range(2020,2026):');end=text.index('    pins={str(p):sha(p) for p in paths}',start)
    replacement="""    for year in range(2020,2026):
        left=read(oldbank/str(year)/'info.json');right=read(bank/str(year)/'info.json')
        assert left['configuration']['seed']==right['configuration']['seed']==20261009
        assert left['configuration']['label_horizon_trading_days']==20
        assert right['configuration']['label_horizon_trading_days']==5
        assert left['configuration']['target']=='y_rank_20mean' and right['configuration']['target']=='y_rank_5mean'
        assert left['configuration']['training_calendar_window']==right['configuration']['training_calendar_window']==252
        assert left['model_sha256']!=right['model_sha256']
        # Each horizon is independently matured. Their training matrices/populations are intentionally different.
        paths += [oldbank/str(year)/'info.json',bank/str(year)/'info.json']
"""
    text=text[:start]+replacement+text[end:]
    text=text.replace('actual_new_own_stock_embedding_rank20_two_seed49_training_only_official_scoring','actual_mixed_rank5_rank20_49_TRAIN_only_official_scoring')
    text=text.replace('passed49_own_stock_embedding_one_day_return_after175_TRAIN_only_CDF_tiny_weights_and_protected_tail_official_comparisons','passed49_mixed_rank5_rank20_TRAIN_only_CDF_both_signs_official_comparisons')
    driver=A/'run_rank5_rank20_after175_mixed_horizon49_screen_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    module=importlib.import_module(driver.stem);cases=module.cases();assert len(cases)==49 and all('rank5_weight' in c for c in cases)
    plan=A/'rank5_rank20_mixed_horizon49_predeclared_plan_v1_20261011.json'
    create(plan,{'status':'predeclared49_mixed_independently_matured_rank5_and_rank20_label_horizons_before_score','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'cases':cases,'input_sha256':{str(source):sha(source),str(driver):sha(driver),str(Path(__file__)):sha(__file__)},'label_horizons':[20,5],'training_populations_equal_not_claimed':True,'physical_signal_models':2,'parent_round':175,'new_fits':0,'new_scores_before_declaration':0,'future_X_read':False,'test_labels_read':False,'full_candidate_qualification_pending':True})
    assert allowed();row=start_service('actual_rank5_rank20_after175_mixed_horizon49_screen_v1_20261011',driver.name,[],{str(plan):sha(plan),str(driver):sha(driver)});create(A/'actual_rank5_rank20_mixed_horizon49_activation_v1_20261011.json',row)
    print({'new_mixed_horizon_cases':49,'new_model_fits':0,'actual_service_pid':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
