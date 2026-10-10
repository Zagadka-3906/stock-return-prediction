"""Combine the proven rank20 signal with qualified dual174; freeze61 before scoring."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    old=A/'run_stock_rank20_embedding_after173_fast17_screen_v1_20261010.py'
    new=A/'run_stock_rank20_embedding_after174_complement61_screen_v1_20261010.py'
    text=old.read_text(encoding='utf8').replace('StockEmbedding173_complete36_family_v3_20261010','StockRankDual174_verified_candidate_registration_recovery_v3_20261010').replace("release['scored_records']==36","release['scored_records']==44").replace('173','174').replace('high_impact17','high_impact61')
    start=text.index('def cases():');end=text.index('\ndef main():',start)
    cases='''def cases():
    rows=[{'kind':'anchor174','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for sign in (1.,-1.):
        for weight in (.00025,.001,.004,.016,.064):rows.append({'kind':'CDF','role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':None})
    for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
        for protection in (.1,.15,.2,.25,.35):
            for weight in (.004,.008,.016,.032,.064):rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':1.,'protect_fraction':protection})
    assert len(rows)==61;return rows

'''
    text=text[:start]+cases+text[end:]
    text=text.replace('frozen17_own_stock_embedding_return1d','frozen61_own_rank20_mean_after_qualified_dual174').replace('return1d17_training_only','rank20_mean61_training_only').replace("'expected_cases':17","'expected_cases':61").replace("'new_quality_score_records':17","'new_quality_score_records':61").replace("'actual_nonidentity_full_controls':16","'actual_nonidentity_full_controls':60").replace("'actual_nonidentity_prefix_controls':48","'actual_nonidentity_prefix_controls':180").replace('passed17_own_stock_embedding_one_day_return','passed61_own_rank20_mean_complement')
    assert not new.exists();compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    module=importlib.import_module(new.stem);plan=module.cases();assert len(plan)==61
    create(A/'rank20_after174_complement61_predeclared_plan_v1_20261010.json',{'status':'predeclared61_rank20_identity_complement_to_verified_dual174_before_new_scores','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,A/'github_validation_sync_main_20261005/round174_receipt.json']},'cases':plan,'parent_round':174,'reused_existing_six_own_models':True,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False,'new_quality_scores':0})
    assert allowed();name='actual_stock_rank20_embedding_after174_complement61_screen_v1_20261010'
    row=start_service(name,new.name,[],{str(new):sha(new)});create(A/(name+'_activation.json'),row)
    print({'new_TRAIN_cases':61,'new_fits':0,'parent_round':174,'actual_quality_pending':True},flush=True)
if __name__=='__main__':main()
