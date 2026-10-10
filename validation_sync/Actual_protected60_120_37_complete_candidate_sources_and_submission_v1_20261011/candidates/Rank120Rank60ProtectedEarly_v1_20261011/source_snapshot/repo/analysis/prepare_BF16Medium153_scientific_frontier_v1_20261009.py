"""Freeze72 medium-neural signed/cohort/weight cases and zero before quality or futureX."""
from pathlib import Path
import sys,hashlib,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))

def main():
    import numpy as np
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    native=A/'neural_BF16_medium2048_seed09_e64_native_v1_20261009.py'
    tree=ast.parse(native.read_text(encoding='utf8'))
    config=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in n.targets)))
    source=A/'neural_BF16_independent_forward_v1_20261008.py';decoder=A/'neural_BF16_medium2048_seed09_independent_forward_v1_20261009.py'
    s=source.read_text(encoding='utf8');old='own_mature_BF16_micro8192_weighted_accum_v1_20261008'
    assert s.count(old)==1
    s=s.replace(old,config['recipe']);assert s.replace(config['recipe'],old)==source.read_text(encoding='utf8')
    compile(s,str(decoder),'exec')
    with decoder.open('x',encoding='utf8') as f:f.write(s)
    cases=[{'role':'all_valid','weight':0.,'sign':1.}]
    cases.extend({'role':role,'weight':weight,'sign':sign} for sign in (1.,-1.) for role in codec.ROLES for weight in (.0005,.001,.002,.004,.008,.016,.032,.064,.125,.25,.5,1.))
    assert len(cases)==73
    rng=np.random.default_rng(15320261009)
    dates=np.repeat(np.array([20200102,20210104,20230103,20241230,20250102,20260102]),47)
    parent=np.round(rng.normal(size=len(dates)),1).astype(np.float64);parent[0]=-0.
    flags=rng.integers(0,2,len(dates));valid=rng.random(len(dates))>.2
    raw=np.round(rng.normal(size=len(dates)),2).astype(np.float64);raw[~valid]=-1e6
    records=[]
    for i,c in enumerate(cases):
        out=codec.transform(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign'])
        exact(out,codec.pandas_oracle(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign']))
        keep=~codec.selected(flags,valid,c['role']);exact(out[keep],parent[keep])
        cold=[]
        for n in (94,188,235):
            prefix=codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign']);exact(prefix,out[:n]);cold.append(n)
        poisoned=parent.copy();poisoned[dates>=20250101]=rng.normal(size=(dates>=20250101).sum())
        other=codec.transform(poisoned,raw,dates,flags,valid,c['role'],c['weight'],c['sign']);exact(other[dates<20250101],out[dates<20250101])
        if not c['weight']:exact(out,parent)
        records.append({'case':i,'configuration':c,'Pandas_bits_exact':True,'cold_prefixes':cold,
            'future_parent_perturbation_preserves_past':True,'declared_unselected_and_invalid_bits_preserved':True,
            'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(out)).cast('B')).hexdigest()})
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed09_e64_bank6_v1_20261009')
    front=A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json'
    inputs=[Path(__file__),Path(codec.__file__),A/'BF16_complete_parent_rank_CDF_v1_20261008.py',source,decoder,native,front,
        A/'optimization_20261003_r148/selection.json',A/'optimization_20261003_r148/full_registration_execution.json',ROOT/'后续选模标准.md']
    assert read(A/'optimization_20261003_r148/full_registration_execution.json')['status']=='passed'
    proposal=A/'BF16Medium78_round153_proposal_v1_20261009.json'
    pins={str(p):sha(p) for p in inputs}
    create(proposal,{'status':'frozen_new_medium_neural73_case_parent148_frontier_before_quality_and_futureX',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':153,'after_round':152,'fixed_scientific_stage_base_round':148,
        'anchor_rounds':[148,149,150,151,152],'configuration':config,'native_bank':str(bank),'native_fit_years':[2020,2021,2022,2023,2024,2025],
        'new_cases':cases,'expected_full_cases':73,'expected_cold_cases':219,'expected_official_cases':78,
        'first2020_active':True,'rank_universe':'all_current_raw_forecasts','new_direction':'own2048_BF16_seed09_64epoch_neural_signed_rank_mix_after_entire148_parent',
        'quality_selection':'highest_complete_connected2020_2024_official_S_then_physical_native_count_then_absolute_weight_then_case',
        'remaining_required':['complete_own6_annual_fits_with_mature_labels','independent_saved_tensor_forward_and_native_OOF_replay_for_all6_states',
            'full73_training_Pandas_and219_cold_controls','complete_registry_prospective_routes_for_all_comparison_parents','prior_complete_forecast_hash_audit',
            'official78_scoring_and_main_publication','full_scheme_freeze_before_futureX','selected_two_full_native_independent_CSV_and_cold80',
            'sealed_candidate_original_six_view_QA_and_complete_ranking_main'],
        'input_sha256':pins,'test_labels_read':False,'actual_future_X_read':False,'new_quality_scores':0,
        'actual_all6_states_and_native_replays_not_yet_claimed':True,'selection_bias_uncorrected':True,'optimization_exhaustion_proven':False})
    create(A/'BF16Medium78_synthetic73_cold219_v1_20261009.json',{'status':'passed_actual73_synthetic219_prefixes_and_independent_signed_Pandas_before_quality',
        'input_sha256':{**pins,str(proposal):sha(proposal)},'records':records,'actual_cases':73,'actual_cold_cases':219,
        'native_6_state_full_replay_and_real_training73_checks_still_required':True,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'quality_cases_proposed':78,'synthetic':73,'cold':219,'actual_quality_scores':0},flush=True)

if __name__=='__main__':main()
