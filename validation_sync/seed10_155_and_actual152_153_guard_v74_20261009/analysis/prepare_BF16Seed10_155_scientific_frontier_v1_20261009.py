"""Freeze an uncovered individual seed10 direction using its own already trained six mature models."""
from pathlib import Path
import sys,time,ast,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def route(s):
    s=s.replace('BF16Medium153_complete_parent_rank_CDF_v1_20261009','__SHARED_SIGNED_CDF__')
    s=s.replace('actual_BF16Medium153_full5_independent_location_v1_20261009','actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009')
    s=s.replace('BF16Medium153_independent_full5_GPU_controls_v1_20261009','BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009')
    s=s.replace('BF16Medium153','BF16Seed10_155').replace('BF16Medium78','BF16Seed10_80')
    s=s.replace('medium153','seed10_155').replace('seed09','seed10').replace('MEDIUM_AFTER_COMPLETE148','SEED10_AFTER_COMPLETE148')
    return s.replace('__SHARED_SIGNED_CDF__','BF16Medium153_complete_parent_rank_CDF_v1_20261009')
def main():
    import numpy as np
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    from neural_BF16_medium2048_seed10_e64_native_v1_20261009 import CONFIG
    bank=Path(read(A/'actual_BF16_medium2048_seed10_e64_bank6_location_v1_20261009.json')['output'])
    bankproof=bank/'verification.json';assert read(bankproof)['actual_native_fits']==6
    pointer=A/'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009.json'
    independent=Path(read(pointer)['output'])/'verification.json';assert sha(independent)==read(pointer)['verification_sha256']
    p=read(independent);assert p['rows_days_stocks']==[5635800,1212,4650] and len(p['records'])==5
    pairs=[('BF16Medium153_complete_parent_native_stage_v1_20261009.py','BF16Seed10_155_complete_parent_native_stage_v1_20261009.py'),
        ('predict_BF16Medium153_complete_parent_scheme_v1_20261009.py','predict_BF16Seed10_155_complete_parent_scheme_v1_20261009.py'),
        ('verify_BF16Medium153_native42_calendar_v1_20261009.py','verify_BF16Seed10_155_native42_calendar_v1_20261009.py'),
        ('verify_BF16Medium153_full73_training_v1_20261009.py','verify_BF16Seed10_155_full73_training_v1_20261009.py'),
        ('verify_BF16Medium153_predictor_ABI_v1_20261009.py','verify_BF16Seed10_155_predictor_ABI_v1_20261009.py')]
    inputs=[Path(__file__),bankproof,pointer,independent,A/'neural_BF16_medium2048_seed10_e64_native_v1_20261009.py',
        A/'neural_BF16_medium2048_seed10_independent_forward_v1_20261009.py',Path(codec.__file__),A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
        A/'optimization_20261003_r148/full_registration_execution.json',A/'optimization_20261003_r148/selection.json',
        A/'BF16TwoSeed79_round154_proposal_v1_20261009.json',ROOT/'后续选模标准.md']
    for old,new in pairs:
        src,dst=A/old,A/new;assert not dst.exists();text=route(src.read_text(encoding='utf8'));compile(text,str(dst),'exec');dst.write_text(text,encoding='utf8');inputs.extend((src,dst))
    assert CONFIG['seed']==20261010 and CONFIG['epochs']==64
    model_shas=[]
    for year in range(2020,2026):
        info=read(bank/str(year)/'info.json');assert info['year']==year and info['configuration']==CONFIG
        assert info['training_meta']['last']<info['training_meta']['cutoff_exclusive']<year*10000+101
        assert sha(bank/str(year)/'model.joblib')==info['model_sha256'];model_shas.append(info['model_sha256'])
        inputs.append(bank/str(year)/'info.json')
    parent_models=read(ROOT/'candidates/optimization_20261003_r148/verification.json')['models']
    assert model_shas[-1] not in {m['sha256'] for m in parent_models.values()}
    cases=[{'role':'all_valid','weight':0.,'sign':1.}]
    weights=(.0005,.001,.002,.004,.008,.016,.032,.064,.125,.25,.5,1.)
    cases.extend({'role':role,'weight':weight,'sign':sign} for sign in (1.,-1.) for role in codec.ROLES for weight in weights)
    assert len(cases)==73
    pins={str(p):sha(p) for p in inputs}
    proposal=A/'BF16Seed10_80_round155_proposal_v1_20261009.json'
    create(proposal,{'status':'frozen_individual_seed10_after_complete148_before155_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':155,'after_round':154,
        'fixed_scientific_stage_base_round':148,'anchor_rounds':list(range(148,155)),
        'configuration':CONFIG,'native_bank':str(bank),'native_fit_years':list(range(2020,2026)),
        'new_cases':cases,'expected_full_cases':73,'expected_cold_cases':219,'expected_official_cases':80,
        'first2020_active':True,'rank_universe':'all_current_raw_forecasts',
        'graph_key':'BF16_medium2048_seed10_complete_parent_rank_CDF','model_name':'rank_MLP2048_BF16_seed10_e64',
        'new_direction':'individual_seed10_saved_neural_output_after_entire148_not_the_equal_two_seed_mean',
        'existing_six_own_mature_seed10_fits_reused':True,'no_refit_or_seed09_weight_reuse':True,
        'all80_official_scores_freeze_full_candidate_replays_six_view_QA_and_main_still_required':True,
        'quality_selection':'continuous_official_S_then_actual_unique_model_SHA_count_then_abs_weight_then_case',
        'input_sha256':pins,'actual_future_X_read':False,'test_labels_read':False,'new_quality_scores':0,
        'all_training_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,'optimization_exhaustion_proven':False})
    rng=np.random.default_rng(15520261009);dates=np.repeat(np.array([20200102,20210104,20230103,20241230,20250102,20260102]),47)
    parent=np.round(rng.normal(size=len(dates)),1).astype(np.float64);parent[0]=-0.
    flags=rng.integers(0,2,len(dates));valid=rng.random(len(dates))>.2
    raw=np.round(rng.normal(size=len(dates)),2).astype(np.float64);raw[~valid]=-1e6
    def exact(a,b):assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))
    records=[]
    for index,c in enumerate(cases):
        out=codec.transform(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign'])
        exact(out,codec.pandas_oracle(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign']))
        keep=~codec.selected(flags,valid,c['role']);exact(out[keep],parent[keep])
        for n in (94,188,235):exact(codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign']),out[:n])
        changed=parent.copy();changed[dates>=20250101]=rng.normal(size=(dates>=20250101).sum())
        other=codec.transform(changed,raw,dates,flags,valid,c['role'],c['weight'],c['sign']);exact(other[dates<20250101],out[dates<20250101])
        if not c['weight']:exact(out,parent)
        records.append({'case':index,'configuration':c,'fixture_rows':282,'Pandas_bits_exact':True,'cold_prefixes':[94,188,235],
            'future_parent_perturbation_preserves_past':True,'invalid_and_unselected_parent_bits_preserved':True,
            'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(out)).cast('B')).hexdigest()})
    create(A/'BF16Seed10_80_synthetic73_cold219_v1_20261009.json',{
        'status':'passed73_synthetic_signed_CDF219_prefixes_before_actual_seed10_155_controls',
        'input_sha256':{**pins,str(proposal):sha(proposal)},'records':records,'actual_cases':73,'actual_cold_cases':219,
        'actual_native42_and_full73_on_real_training_still_required':True,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={}
    for name,driver in [('BF16Seed10_155_actual_native42_calendar_v1_20261009','verify_BF16Seed10_155_native42_calendar_v1_20261009.py'),
        ('BF16Seed10_155_actual_full73_training_v1_20261009','verify_BF16Seed10_155_full73_training_v1_20261009.py')]:
        launches[name]=start(name,driver,[],{str(proposal):sha(proposal),str(A/driver):sha(A/driver),str(A/'BF16Seed10_155_complete_parent_native_stage_v1_20261009.py'):sha(A/'BF16Seed10_155_complete_parent_native_stage_v1_20261009.py')})
    create(A/'BF16Seed10_155_scientific_controls_hidden_launches_v1_20261009.json',{'launches':launches,'new_training_fits':0,'new_quality_scores':0})
    print({'proposed_official_cases':80,'synthetic_cases':73,'synthetic_cold_cases':219,'own_saved_model_states':6,'real_control_workers':{n:r['owned_worker_pid'] for n,r in launches.items()}},flush=True)
if __name__=='__main__':main()
