"""Refine the measured negative-CDF transition using existing mature two-horizon banks."""
from pathlib import Path
from datetime import datetime
import importlib,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
PLAN='rank5_rank20_near_refined25_predeclared_plan_v1_20261011.json'
DRIVER='run_rank5_rank20_after175_near_refined25_screen_v1_20261011.py'
FOLDER='Rank5Rank20_after175_near_refined25_screen_v1_20261011'
SERVICE='actual_rank5_rank20_after175_near_refined25_screen_v1_20261011'

def main():
    assert allowed()
    precursor=Path('E:/赛题五_本机临时/Rank5Rank20_after175_near_pure49_screen_v1_20261011/verification.json')
    measured=read(precursor);assert len(measured['records'])==49
    assert measured['best']['connected_final_score']==0.4514130257498636
    source=A/'run_rank5_rank20_after175_near_pure49_screen_v1_20261011.py'
    text=source.read_text(encoding='utf8');first=text.index('def cases():');last=text.index('\ndef main():')
    replacement="""def cases():
    rows=[{'kind':'anchor175','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'rank5_weight':None}]
    for blend in (.03125,.0625,.125):
        for weight in (.00021875,.00025,.00028125,.00034375,.000375,.0004375,.0005,.0005625):
            rows.append({'kind':'CDF','role':'nonflag_valid','weight':weight,'sign':-1.,'protect_fraction':None,'rank5_weight':blend})
    assert len(rows)==25;return rows

"""
    text=text[:first]+replacement+text[last:]
    text=text.replace('Rank5Rank20_after175_near_pure49_screen_v1_20261011',FOLDER)
    text=text.replace('rank5_rank20_near_pure49_predeclared_plan_v1_20261011.json',PLAN)
    text=text.replace("closed('actual_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011')","closed('actual_rank5_rank20_after175_near_protected37_screen_v1_20261011')")
    text=text.replace("'expected_cases':49","'expected_cases':25").replace("'new_quality_score_records':49","'new_quality_score_records':25")
    text=text.replace("'actual_nonidentity_full_controls':48","'actual_nonidentity_full_controls':24").replace("'actual_nonidentity_prefix_controls':144","'actual_nonidentity_prefix_controls':72")
    text=text.replace('frozen49_own_stock_embedding_return1d_after175_hypotheses','frozen25_own_stock_embedding_return1d_after175_hypotheses')
    text=text.replace('passed49_mixed_rank5_rank20_TRAIN_only_CDF_both_signs_official_comparisons','passed25_near_refined_negative_CDF_TRAIN_only_official_comparisons')
    text=text.replace('actual_mixed_rank5_rank20_49_TRAIN_only_official_scoring','actual_near_refined25_TRAIN_only_official_scoring')
    driver=A/DRIVER;assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    cases=importlib.import_module(Path(DRIVER).stem).cases();assert len(cases)==25
    old={tuple(sorted(r['configuration'].items())) for r in measured['records']}
    assert all(tuple(sorted(c.items())) not in old for c in cases[1:])
    stage=A/'rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011.py'
    pins={str(p):sha(p) for p in [Path(__file__),source,driver,precursor,stage,A/'three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011.json']}
    create(A/PLAN,{'status':'predeclared25_adaptive_TRAIN_only_negative_CDF_transition_refinement_before_new_scores',
           'at_local':datetime.now().isoformat(),'input_sha256':pins,'cases':cases,'actual_service':SERVICE,
           'output':str(Path('E:/赛题五_本机临时')/FOLDER),
           'native_stage_module':stage.stem,'stage_kind':'rank5_rank20_mixed_raw_average',
           'expected_records':25,'expected_nonidentity_full_controls':24,'expected_nonidentity_prefix_controls':72,
           'label_horizons':[20,5],'training_windows':[252,252],'training_populations_equal_not_claimed':True,
           'new_native_fits':0,'new_quality_scores_before_declaration':0,'test_labels_read':False,
           'future_X_read':False,'selection_bias_uncorrected':True,'adaptive_TRAIN_search_not_blind':True,
           'complete191_factory_not_yet_created':True,'preceding_full189_highest_candidate_remains_prioritized':True})
    assert allowed();row=start_service(SERVICE,DRIVER,[],{**pins,str(A/PLAN):sha(A/PLAN)})
    create(A/(SERVICE+'_activation.json'),row)
    create(A/'near_refined25_sources_and_dispatch_admission_v1_20261011.json',{'status':'compiled25_cached_two_horizon_TRAIN_scores_queued_after_protected37',
           'input_sha256':{**pins,str(A/PLAN):sha(A/PLAN)},'actual_service_identity':row,'new_native_fits':0,
           'actual_scoring_not_claimed_complete':True,'future_selected_native_and_candidate_pending':True,'test_labels_read':False})
    print({'new_refinement_cases':25,'worker':row['owned_worker_pid'],'new_native_fits':0},flush=True)

if __name__=='__main__':main()
