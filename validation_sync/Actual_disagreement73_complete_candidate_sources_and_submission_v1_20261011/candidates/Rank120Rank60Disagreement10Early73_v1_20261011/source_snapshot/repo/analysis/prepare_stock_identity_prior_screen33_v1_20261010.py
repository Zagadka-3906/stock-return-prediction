"""Freeze33 cheap identity-prior combinations before inspecting any official result."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    s=(A/'run_TopWeighted_after163_high_impact65_screen_v1_20261010.py').read_text(encoding='utf8')
    begin=s.index('def cases():');end=s.index('\ndef main():',begin)
    cases='''def cases():
    rows=[{'kind':'anchor163','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for role in ('nonflag_valid','all_valid'):
        for sign in (1.,-1.):
            for weight in (.004,.064,.25,1.):rows.append({'kind':'CDF','role':role,'weight':weight,'sign':sign,'protect_fraction':None})
    for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
        for fraction in (.25,.35):
            for sign in (1.,-1.):
                for weight in (.016,.064):rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':fraction})
    assert len(rows)==33;return rows
'''
    s=s[:begin]+cases+s[end:]
    begin=s.index("    for name in ('actual_BF16_");end=s.index('    import numpy',begin)
    s=s[:begin]+"    for name in ('actual_stock_identity_excess_prior_bank6_v1_20261010','actual_TopWeighted_after163_high_impact65_screen_v1_20261010','ReusedNN165Quality19_round165_full_registration_v1_20261009'):closed(name)\n"+s[end:]
    begin=s.index("    bank=Path('E:");end=s.index('    pins={',begin)
    replacement='''    bank=Path('E:/赛题五_本机临时/stock_identity_excess_prior_bank6_v1_20261010');full=bank
    pointer=A/'actual_stock_identity_excess_prior_bank6_location_v1_20261010.json'
    proof=read(bank/'verification.json');assert proof['actual_native_fits']==6 and proof['rows_days_stocks']==[5635800,1212,4650]
    assert proof['actual_full_independent_OOF_cases']==5 and proof['actual_cold_prefix_cases']==15
    paths=[Path(__file__),ROOT/'后续选模标准.md',pointer,bank/'verification.json',bank/'combined_raw.parquet',A/'stock_identity_excess_return_prior_native_v1_20261010.py',A/'stock_identity_excess_prior_actual_CPU_controls_v1_20261010.json',A/'optimization_20261003_r163/selected_validation.npy',A/'optimization_20261003_r163/calibrated_csv_official.json',A/'connected_validation_20261002/combined_fold_frame.parquet',Path(cdf.__file__),Path(valid_tail.__file__),Path(top_tail.__file__),A/'protected_upper_tail_rank_permutation_controls_v1_20261010.json',A/'protected_official_top_rank_permutation_controls_v2_20261010.json']
'''
    s=s[:begin]+replacement+s[end:]
    s=s.replace('TopWeighted_after163_high_impact65','stock_identity_prior_after163_screen33').replace("'recipe':'topweightedhuber010'","'recipe':'stock_identity_excess_prior756_lambda252'")
    s=s.replace('new_Huber65_cumulative163_hypotheses_after_own6_full5_native42_qualification','new_stock_identity33_cumulative163_hypotheses_after_own6_actual_full5_lookup_controls')
    s=s.replace('actual_new_Huber65_training_only_official_scoring','actual_stock_identity33_training_only_official_scoring')
    s=s.replace("'expected_cases':65","'expected_cases':33").replace("'new_quality_score_records':65","'new_quality_score_records':33").replace("'actual_nonidentity_full_controls':64","'actual_nonidentity_full_controls':32").replace("'actual_nonidentity_prefix_controls':192","'actual_nonidentity_prefix_controls':96").replace('passed65_actual_qualified_new_Huber_cumulative163_and_protected_tail_training_only_official_comparisons','passed33_actual_stock_identity_mature6_full5_cumulative163_training_only_official_comparisons')
    target=A/'run_stock_identity_prior_after163_screen33_v1_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    create(A/'stock_identity_prior_screen33_frozen_intent_v1_20261010.json',{'status':'compiled_frozen_plan_no_scores','parent_round':163,'physical_model':'stock_identity_excess_prior756_lambda252','actual_expected_cases':33,'actual_expected_nonidentity_full_checks':32,'actual_expected_prefix_checks':96,'future_X_read':False,'test_labels_read':False,'not_submission_qualified':True,'driver_sha256':sha(target),'waits_complete_Top65_and165_before_CPU_scoring':True})
    row=start_service('actual_stock_identity_prior_after163_screen33_v1_20261010',target.name,[],{str(target):sha(target),str(Path(__file__)):sha(Path(__file__))})
    create(A/'stock_identity_prior_screen33_actual_hidden_launch_v1_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
