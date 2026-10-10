"""Freeze two complementary49-case cached ensemble searches, with sequential RAM-safe scoring."""
from pathlib import Path
import sys,importlib,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();source=A/'run_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011.py';base=source.read_text(encoding='utf8');prepared=[]
    configs=[('mixed_near_pure49','Rank5Rank20_after175_near_pure49_screen_v1_20261011','rank5_rank20_near_pure49_predeclared_plan_v1_20261011.json','actual_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011'),('mixed_long_window49','Rank20ShortLong_after175_mixed_window49_screen_v1_20261011','rank20_short_long_mixed_window49_predeclared_plan_v1_20261011.json','actual_rank5_rank20_after175_near_pure49_screen_v1_20261011')]
    for kind,outname,planname,dependency in configs:
        text=base.replace('StockRank5Rank20_after175_mixed_horizon49_screen_v2_20261011',outname)
        pointer='actual_'+outname+'_location.json'
        text=text.replace('actual_StockRank5Rank20_after175_mixed_horizon49_screen_location_v2_20261011.json',pointer)
        text=text.replace('rank5_rank20_mixed_horizon49_predeclared_plan_v1_20261011.json',planname)
        text=text.replace('    assert allowed()\n',"    assert allowed();closed("+repr(dependency)+")\n",1)
        text=text.replace('(.000078125,.00015625,.0003125,.000625,.00125,.0025,.005,.01)','(.0000390625,.000078125,.00015625,.0003125,.000625,.00125,.0025,.005)')
        if kind=='mixed_near_pure49':
            text=text.replace('for blend in (.25,.5,.75):','for blend in (.03125,.0625,.125):')
            filename='run_rank5_rank20_after175_near_pure49_screen_v1_20261011.py';service='actual_rank5_rank20_after175_near_pure49_screen_v1_20261011';horizons=[20,5];windows=[252,252]
        else:
            text=text.replace('for blend in (.25,.5,.75):','for blend in (.0625,.25,.5):')
            text=text.replace('stock_rank5_embedding','stock_rank20long_embedding').replace('StockRank5Embedding','StockRank20LongEmbedding').replace('rank5_weight','long504_weight')
            text=text.replace("right['configuration']['label_horizon_trading_days']==5","right['configuration']['label_horizon_trading_days']==20")
            text=text.replace("right['configuration']['target']=='y_rank_5mean'","right['configuration']['target']=='y_rank_20mean'")
            text=text.replace("left['configuration']['training_calendar_window']==right['configuration']['training_calendar_window']==252","left['configuration']['training_calendar_window']==252 and right['configuration']['training_calendar_window']==504")
            text=text.replace('stock_rank5_rank20_mixed_label_horizon_ID16_cross120_recent252_e64','stock_rank20_short_long_mixed_window_ID16_cross120_252_504_e64')
            text=text.replace('actual_mixed_rank5_rank20_49_TRAIN_only_official_scoring','actual_mixed_rank20_252_504_49_TRAIN_only_official_scoring').replace('passed49_mixed_rank5_rank20_TRAIN_only_CDF_both_signs_official_comparisons','passed49_mixed_rank20_252_504_TRAIN_only_CDF_both_signs_official_comparisons')
            filename='run_rank20_short_long_after175_mixed_window49_screen_v1_20261011.py';service='actual_rank20_short_long_after175_mixed_window49_screen_v1_20261011';horizons=[20,20];windows=[252,504]
        driver=save(filename,text);module=importlib.import_module(driver.stem);cases=module.cases();assert len(cases)==49
        plan=A/planname;create(plan,{'status':'predeclared49_cached_two_model_complement_before_any_new_scores','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'kind':kind,'input_sha256':{str(Path(__file__)):sha(__file__),str(source):sha(source),str(driver):sha(driver)},'cases':cases,'label_horizons':horizons,'training_windows':windows,'training_populations_equal_not_claimed':True,'actual_service':service,'output':str(module.OUT),'location_pointer':str(A/pointer),'sequential_dependency':dependency,'expected_records':49,'expected_full_controls':48,'expected_prefix_controls':144,'new_native_fits':0,'new_scores_before_declaration':0,'future_X_read':False,'test_labels_read':False,'selection_bias_uncorrected':True,'adaptive_TRAIN_search_not_blind_evaluation':True,'future_candidate_qualification_pending':True})
        assert allowed();row=start_service(service,driver.name,[],{str(driver):sha(driver),str(plan):sha(plan)});create(A/(service+'_activation.json'),row);prepared.append({'service':service,'plan':str(plan),'driver':str(driver),'location_pointer':str(A/pointer),'output':str(module.OUT)})
    create(A/'cached_mixed_near_pure_and_long_window49_admission_v1_20261011.json',{'status':'frozen_two49_case_cached_ensemble_screens_sequentially_dispatched','input_sha256':{str(Path(__file__)):sha(__file__),str(source):sha(source),**{str(Path(r['plan'])):sha(r['plan']) for r in prepared},**{str(Path(r['driver'])):sha(r['driver']) for r in prepared}},'screens':prepared,'new_fits':0,'expected_additional_official_scores':98,'actual_scores_not_claimed_complete':True})
    print({'new_declared_cached_cases':98,'sequential_RAM_threshold_GiB':11.5,'new_model_fits':0},flush=True)
if __name__=='__main__':main()
