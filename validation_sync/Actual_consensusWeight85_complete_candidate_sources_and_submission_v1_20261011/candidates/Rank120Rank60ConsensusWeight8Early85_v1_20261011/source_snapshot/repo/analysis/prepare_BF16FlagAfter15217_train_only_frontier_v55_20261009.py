"""Freeze the uncovered joint sparse152/flag-neural direction before any own quality scores."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import numpy as np
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    parent=A/'optimization_20261003_r152';assert read(parent/'full_registration_execution.json')['status']=='passed'
    seed=Path(read(A/'actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009.json')['output'])
    bankproof=seed/'verification.json';assert read(bankproof)['actual_native_fits']==6
    paths=[Path(__file__),A/'verify_BF16FlagAfter15217_full_training_v1_20261009.py',
        parent/'full_registration_execution.json',parent/'protocol.json',parent/'selection.json',parent/'selected_validation.npy',
        parent/'calibrated_csv_official.json',A/'github_validation_sync_main_20261005/round152_receipt.json',
        ROOT/'candidates/optimization_20261003_r152/verification.json',bankproof,Path(codec.__file__),A/'BF16_complete_parent_rank_CDF_v1_20261008.py',ROOT/'后续选模标准.md']
    for y in range(2020,2026):
        p=seed/str(y)/'info.json';info=read(p);assert info['year']==y
        assert info['training_meta']['last']<info['training_meta']['cutoff_exclusive']<y*10000+101
        assert info['training_meta']['last_label_end']<=info['training_meta']['cutoff_exclusive']
        assert sha(seed/str(y)/'model.joblib')==info['model_sha256'];paths.extend((p,seed/str(y)/'model.joblib'))
    cases=[{'role':'flag_valid','weight':0.,'sign':1.}]
    weights=[.001,.002,.003,.004,.006,.008,.012,.016]
    cases.extend({'role':'flag_valid','weight':w,'sign':s} for s in (1.,-1.) for w in weights)
    assert len(cases)==17
    parent_models=read(ROOT/'candidates/optimization_20261003_r152/verification.json')['models']
    final=read(seed/'2025/info.json')['model_sha256'];assert final not in {m['sha256'] for m in parent_models.values()}
    pins={str(p):sha(p) for p in paths}
    proposal=A/'BF16FlagAfter15217_train_only_proposal_v1_20261009.json'
    create(proposal,{'status':'frozen_uncovered_flag_neural_after_complete152_before_own_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'potential_future_round':157,'fixed_scientific_stage_base_round':152,
        'new_direction':'combine_current_sparse_nonflag152_with_existing_seed09_flag_only_neural_postprocessor',
        'new_cases':cases,'expected_full_cases':17,'expected_cold_cases':51,'model_name':'rank_MLP2048_BF16_seed09_e64',
        'native_bank':str(seed),'existing_own_mature_annual_fits_reused':6,'new_fits':0,
        'rank_universe':'all_current_raw_forecasts','only_flag_valid_rows_may_change':True,
        'selection':'official_continuous_S_then_unique_final_model_SHA_count_then_abs_weight_then_case',
        'new_nonzero_final_model_count':len({m['sha256'] for m in parent_models.values()})+1,
        'all_training_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'full_candidate_replays_future_freeze_complete_ranking_QA_and_main_still_required':True,
        'input_sha256':pins,'test_labels_read':False,'actual_future_X_read':False,'new_quality_scores':0})
    rng=np.random.default_rng(20261009);dates=np.repeat([20200102,20200103,20200106],94)
    p=rng.normal(size=len(dates));raw=rng.normal(size=len(dates));flags=rng.integers(0,2,len(dates));valid=rng.random(len(dates))>.1
    p[~valid]=-1e6;raw[~valid]=-1e6;records=[]
    for i,c in enumerate(cases):
        value=codec.transform(p,raw,dates,flags,valid,c['role'],c['weight'],c['sign'])
        oracle=codec.pandas_oracle(p,raw,dates,flags,valid,c['role'],c['weight'],c['sign'])
        assert np.array_equal(value.view('u8'),oracle.view('u8'))
        mask=codec.selected(flags,valid,c['role']);assert np.array_equal(value[~mask].view('u8'),p[~mask].view('u8'))
        for n in (94,188,282):
            prefix=codec.transform(p[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign'])
            assert np.array_equal(prefix.view('u8'),value[:n].view('u8'))
        records.append({'case':i,'independent_Pandas_and3_cold_prefixes_bits_exact':True})
    create(A/'BF16FlagAfter15217_synthetic17_cold51_v1_20261009.json',{'status':'passed_synthetic17_flag_only_and51_prefix_controls_not_full_training',
        'input_sha256':{**pins,str(proposal):sha(proposal)},'records':records,'actual_cases':17,'actual_cold_cases':51,'fixture_rows':282,'new_quality_scores':0,'actual_future_X_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    driver=A/'verify_BF16FlagAfter15217_full_training_v1_20261009.py'
    row=start('BF16FlagAfter15217_actual_full_training_controls_v1_20261009',driver.name,[],{str(proposal):sha(proposal),str(driver):sha(driver)})
    create(A/'BF16FlagAfter15217_full_controls_launch_v55_20261009.json',{'launch':row,'GPU_fits_not_stopped_or_restarted':True,
        'waits_actual_dropout156_six_fits_before_full_CPU_controls':True,'official_scores_not_yet_started':True})
    print({'synthetic_cases':17,'synthetic_prefixes':51,'actual_full_controller':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
