"""Prepare the entire156 scientific validation route before own fits or quality."""
from pathlib import Path
import sys,time,ast,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_BF16Seed10_155_scientific_frontier_v1_20261009 import route as previous_route

def route(s):
    s=previous_route(s)
    s=s.replace('actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009','actual_BF16Drop05_156_full5_independent_location_v1_20261009')
    s=s.replace('BF16TwoSeed154_seed10_independent_full5_GPU_controls_v1_20261009','BF16Drop05_156_independent_full5_GPU_controls_v1_20261009')
    s=s.replace('BF16Seed10_155','BF16Drop05_156').replace('BF16Seed10_80','BF16Drop05_81')
    s=s.replace('seed10_155','drop05_156').replace('seed10','drop05_seed09')
    s=s.replace('SEED10_AFTER_COMPLETE148','DROP05_AFTER_COMPLETE148')
    s=s.replace('BF16Drop05_81_round155_proposal_v1_20261009','BF16Drop05_81_round156_proposal_v2_20261009')
    return s

def main():
    import numpy as np
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    native=A/'neural_BF16_medium2048_drop05_seed09_e64_native_v1_20261009.py'
    tree=ast.parse(native.read_text(encoding='utf8'))
    cfg=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in n.targets)))
    initial=A/'BF16Drop05_81_round156_proposal_v1_20261009.json';frozen=read(initial)
    assert cfg==frozen['configuration'] and cfg['dropout']==.05
    pairs=[('BF16Seed10_155_complete_parent_native_stage_v1_20261009.py','BF16Drop05_156_complete_parent_native_stage_v1_20261009.py'),
        ('predict_BF16Seed10_155_complete_parent_scheme_v1_20261009.py','predict_BF16Drop05_156_complete_parent_scheme_v1_20261009.py'),
        ('verify_BF16Seed10_155_predictor_ABI_v1_20261009.py','verify_BF16Drop05_156_predictor_ABI_v1_20261009.py'),
        ('verify_BF16Seed10_155_native42_calendar_v1_20261009.py','verify_BF16Drop05_156_native42_calendar_v1_20261009.py'),
        ('verify_BF16Seed10_155_full73_training_v2_20261009.py','verify_BF16Drop05_156_full73_training_v1_20261009.py'),
        ('verify_BF16Medium153_independent_small_CPU_v1_20261009.py','verify_BF16Drop05_156_independent_small_CPU_v1_20261009.py'),
        ('verify_BF16Medium153_full5_independent_GPU_v1_20261009.py','verify_BF16Drop05_156_full5_independent_GPU_v1_20261009.py')]
    sources=[Path(__file__),initial,native,A/'neural_BF16_medium2048_drop05_seed09_independent_forward_v1_20261009.py',
        A/'neural_BF16_medium2048_drop05_seed09_e64_frontier_v1_20261009.json',Path(codec.__file__),
        A/'BF16_complete_parent_rank_CDF_v1_20261008.py',ROOT/'后续选模标准.md']
    for old,new in pairs:
        src,dst=A/old,A/new;s=route(src.read_text(encoding='utf8'))
        if 'full73_training' in new:s=s.replace('BF16Drop05_156_full73_training_v2_20261009','BF16Drop05_156_full73_training_v1_20261009')
        if 'full5_independent_GPU' in new:
            # The previous reusable route refers to seed10's existing audit. Here
            # this bank must execute its own independent audit and own small proof.
            s=s.replace('BF16Drop05_156_full5_independent_controls','BF16Drop05_156_full5_independent_controls')
        compile(s,str(dst),'exec')
        with dst.open('x',encoding='utf8') as f:f.write(s)
        sources.extend((src,dst))
    cases=[{k:c[k] for k in ('role','weight','sign')} for c in frozen['new_cases']]
    assert len(cases)==73
    proposal=A/'BF16Drop05_81_round156_proposal_v2_20261009.json'
    create(proposal,{'status':'frozen_complete_dropout156_science_with_initial_grid_exact',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':156,'after_round':155,
        'fixed_scientific_stage_base_round':148,'anchor_rounds':list(range(148,156)),
        'configuration':cfg,'native_bank':'E:/赛题五_本机临时/neural_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009',
        'native_fit_years':list(range(2020,2026)),'new_cases':cases,'expected_full_cases':73,
        'expected_cold_cases':219,'expected_official_cases':81,'first2020_active':True,
        'rank_universe':'all_current_raw_forecasts','graph_key':'BF16_medium2048_drop05_seed09_complete_parent_rank_CDF',
        'model_name':'rank_MLP2048_BF16_drop05_seed09_e64','initial_configuration_and_grid_exact':True,
        'all_six_own_mature_fits_required_not_old_weights':True,
        'quality_selection':'continuous_official_S_then_actual_unique_model_SHA_count_then_abs_weight_then_case',
        'input_sha256':{str(p):sha(p) for p in sources},'actual_future_X_read':False,'test_labels_read':False,
        'new_quality_scores':0,'all_training_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'optimization_exhaustion_proven':False})
    rng=np.random.default_rng(15620261009);dates=np.repeat(np.array([20200102,20210104,20230103,20241230,20250102,20260102]),47)
    parent=np.round(rng.normal(size=len(dates)),1).astype(np.float64);parent[0]=-0.
    flags=rng.integers(0,2,len(dates));valid=rng.random(len(dates))>.2
    raw=np.round(rng.normal(size=len(dates)),2).astype(np.float64);raw[~valid]=-1e6
    def exact(a,b):assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))
    records=[]
    for i,c in enumerate(cases):
        out=codec.transform(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign'])
        exact(out,codec.pandas_oracle(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign']))
        keep=~codec.selected(flags,valid,c['role']);exact(out[keep],parent[keep])
        for n in (94,188,235):exact(codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],c['role'],c['weight'],c['sign']),out[:n])
        changed=parent.copy();changed[dates>=20250101]=rng.normal(size=(dates>=20250101).sum())
        other=codec.transform(changed,raw,dates,flags,valid,c['role'],c['weight'],c['sign']);exact(other[dates<20250101],out[dates<20250101])
        if not c['weight']:exact(out,parent)
        records.append({'case':i,'configuration':c,'Pandas_bits_exact':True,'cold_prefixes':[94,188,235],
            'future_parent_perturbation_preserves_past':True,'unselected_and_invalid_bits_exact':True,
            'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(out)).cast('B')).hexdigest()})
    synthetic=A/'BF16Drop05_81_synthetic73_cold219_v1_20261009.json'
    create(synthetic,{'status':'passed73_synthetic_signed_CDF219_prefixes_before_actual_dropout156_controls',
        'input_sha256':{str(p):sha(p) for p in [*sources,proposal]},'records':records,'actual_cases':73,
        'actual_cold_cases':219,'actual_full5635800_controls_still_required':True,'new_quality_scores':0,
        'actual_future_X_read':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={}
    for name,driver in [('BF16Drop05_156_independent_small_CPU_v1_20261009','verify_BF16Drop05_156_independent_small_CPU_v1_20261009.py'),
        ('BF16Drop05_156_independent_full5_GPU_controls_v1_20261009','verify_BF16Drop05_156_full5_independent_GPU_v1_20261009.py'),
        ('BF16Drop05_156_actual_native42_calendar_v1_20261009','verify_BF16Drop05_156_native42_calendar_v1_20261009.py'),
        ('BF16Drop05_156_actual_full73_training_v1_20261009','verify_BF16Drop05_156_full73_training_v1_20261009.py')]:
        launches[name]=start(name,driver,[],{str(proposal):sha(proposal),str(synthetic):sha(synthetic),str(A/driver):sha(A/driver)})
    create(A/'BF16Drop05_156_scientific_controls_hidden_launches_v1_20261009.json',{'launches':launches,
        'actual_own_six_annual_fits_still_required':True,'new_quality_scores':0,'test_labels_read':False})
    print({'synthetic':73,'prefixes':219,'prospective_official_cases':81,'waiting_scientific_workers':{n:r['owned_worker_pid'] for n,r in launches.items()}},flush=True)
if __name__=='__main__':main()
