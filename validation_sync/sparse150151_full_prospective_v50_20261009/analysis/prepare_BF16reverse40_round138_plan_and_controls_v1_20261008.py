"""Freeze the previously uncovered neural reverse direction and queue real full controls after137."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    import numpy as np
    import BF16_reverse_complete_parent_rank_CDF_v1_20261008 as codec
    plan_path=A/'BF16reverse40_round138_plan_v1_20261008.json'
    plan={'status':'frozen40_reverse_BF16_complete_parent_cases_before_any_new_reverse_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':138,'model_name':'reverse_valid_rank_MLP16384_BF16_micro8192_32epochs',
        'native_recipe':'own_mature_BF16_micro8192_weighted_accum_v1_20261008',
        'actual_annual_bank':'E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008',
        'qualified_anchor_rounds':[135,136,137],'roles':['all_valid','nonflag_valid','flag_valid'],
        'weights':[.0025,.005,.01,.025,.05,.075,.1,.2,.35,.5,.75,1.],
        'expected_scored_records':40,'expected_transform_controls':37,'expected_cold_controls':111,
        'rank_universe':'all_current_raw_forecasts','first2020_active':True,'signal_sign_on_valid_rows':-1.,
        'invalid_signal_bits_preserved':True,'stage_graph_key':'BF16_reverse_complete_parent_rank_CDF',
        'new_stage_position':'after_complete_qualified_parent_all_signed_Bayes_BF16_CrossFamily_and_Huber_branches',
        'transform':'inverseCDF_parent((1-weight)*parent_day_rank_over_N+weight*valid_reversed_neural_day_rank_over_N)',
        'invalid_and_declared_unselected_parent_raw_values_preserved':True,'zero_weight_is_exact_whole_parent_identity':True,
        'additional_model_fits_by_this_comparison':0,'physical_models_counted_by_unique_native_model_sha256_union':True,
        'exact_parent_frozen_only_after137_official_candidate_QA48_and_main':True,
        'whole_native_independent_replay_and_sources_required_before_scoring':True,
        'select_by_actual_official_continuous_S_all8_metrics_no_extra_quality_gates':True,
        'actual_official_scores':0,'selection_bias_uncorrected':True,'test_labels_read':False,'global_exhaustion_claimed':False}
    create(plan_path,plan)
    synthetic=A/'BF16_reverse_rank_CDF_synthetic_preflight_v1_20261008';assert not synthetic.exists();synthetic.mkdir()
    rng=np.random.default_rng(2026100838);dates=np.repeat(np.array([20200102,20251230,20260102],dtype=np.int32),4650)
    parent=np.round(rng.normal(size=len(dates)),2).astype(np.float64);neural=np.round(rng.normal(size=len(dates)),2).astype(np.float64)
    valid=rng.random(len(dates))>.17;flags=(rng.random(len(dates))>.85).astype(np.int8)
    parent[~valid]=-1e6;neural[~valid]=-1e6;neural[0]=-0.;neural[1]=0.
    paths=[Path(__file__),Path(codec.__file__),A/'BF16_complete_parent_rank_CDF_v1_20261008.py',plan_path]
    pins={str(p):sha(p) for p in paths};create(synthetic/'frozen_before_actual_controls.json',{
        'input_sha256':pins,'synthetic_dates_not_actual_future_X':True,'actual_quality_scores':0,'new_fits':0,'test_labels_read':False})
    signal=codec.reversed_signal(neural,valid)
    assert np.array_equal(signal[~valid].view('u8'),neural[~valid].view('u8'))
    assert np.array_equal(signal[valid].view('u8'),(-neural[valid]).view('u8'))
    prepared=codec.prepare(parent,neural,dates,flags,valid);records=[]
    for role in codec.ROLES:
        for weight in (0.,*plan['weights']):
            value=codec.apply_prepared(parent,flags,valid,role,weight,prepared)
            other=codec.pandas_oracle(parent,neural,dates,flags,valid,role,weight)
            assert np.array_equal(value.view('u8'),other.view('u8'))
            cohort=codec.selected(flags,valid,role)
            assert np.array_equal(value[~cohort].view('u8'),parent[~cohort].view('u8'))
            for days in (1,2):
                n=days*4650;prefix=codec.transform(parent[:n],neural[:n],dates[:n],flags[:n],valid[:n],role,weight)
                assert np.array_equal(prefix.view('u8'),value[:n].view('u8'))
            if weight==0.:assert np.array_equal(value.view('u8'),parent.view('u8'))
            else:assert np.any(value[dates<20210101]!=parent[dates<20210101])
            records.append({'role':role,'weight':weight,'Pandas_CDF_and_two_whole_day_prefix_bits_exact':True,
                'invalid_signal_and_parent_and_unselected_bits_preserved':True})
    for p,d in pins.items():assert sha(p)==d,p
    create(synthetic/'verification.json',{'status':'passed_actual39_reverse_BF16_synthetic_CDF_and78_day_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,
        'actual_cases':39,'actual_day_controls':78,'actual_quality_scores':0,'new_fits':0,
        'actual_future_X_and_Y_read':False,'synthetic_controls_do_not_qualify_actual_future_candidate':True})
    source=A/'verify_BF16_rank_CDF_full37_v1_20261008.py';text=source.read_text(encoding='utf8')
    mapping={'BF16_rank_CDF_full37_preflight_v1_20261008':'BF16_reverse_rank_CDF_full37_preflight_v1_20261008',
        'nonflag_ReverseBayesFine40_round134_full_registration_v1':'Huber52_round137_full_registration_v3_20261008',
        'BF16_complete_parent_rank_CDF_v1_20261008':'BF16_reverse_complete_parent_rank_CDF_v1_20261008',
        'BF16wide40_round135_plan_v1_20261008':'BF16reverse40_round138_plan_v1_20261008',
        'BF16_rank_CDF_synthetic_preflight_v1_20261008':'BF16_reverse_rank_CDF_synthetic_preflight_v1_20261008',
        'passed_actual18_synthetic_BF16_rank_CDF_roles_and36_day_prefixes':'passed_actual39_reverse_BF16_synthetic_CDF_and78_day_controls',
        'actual_BF16_rank_CDF_full37_location_v1_20261008':'actual_BF16_reverse_rank_CDF_full37_location_v1_20261008',
        'passed_actual37_full5635800_BF16_rank_CDF_independent_and111_cold_controls':'passed_actual37_full5635800_reverse_BF16_CDF_independent_and111_cold_controls'}
    for before,after in mapping.items():text=text.replace(before,after)
    needle="parent = min(parents, key=lambda number: (-metrics[number]['final_score'], number))";assert text.count(needle)==1
    text=text.replace(needle,"parent = min(parents, key=lambda number: (-metrics[number]['final_score'],len(read(ROOT/f'candidates/optimization_20261003_r{number}/verification.json')['models']),number))")
    driver=A/'verify_BF16_reverse_rank_CDF_full37_v1_20261008.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),source,driver,plan_path,synthetic/'verification.json',Path(codec.__file__)]}
    row=start('BF16_reverse_rank_CDF_actual_full37_controls_v1_20261008',driver.name,[],pins)
    create(A/'actual_BF16reverse40_plan_and_full37_hidden_launch_v1_20261008.json',{
        'status':'frozen40_reverse_cases_actual39_synthetic_and78_day_controls_then_queued_full37_after137',
        'identity':row,'input_sha256':pins,'new_fits':0,'actual_quality_scores':0,'test_labels_read':False,
        'round138_complete_source_admission_native_hooks_scoring_candidate_QA49_main_still_required':True})
    print('Reverse-BF16 plan40 frozen;39 synthetic/78 day controls passed; full37/111 queued after qualified137.',flush=True)


if __name__=='__main__':main()
