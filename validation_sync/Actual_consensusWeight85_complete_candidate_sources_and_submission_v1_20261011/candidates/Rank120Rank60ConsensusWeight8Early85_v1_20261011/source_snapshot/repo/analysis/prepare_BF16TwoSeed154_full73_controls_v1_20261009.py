"""Run73 independent synthetic ensemble mixes and queue73 complete historical checks after real fits."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import numpy as np,pandas as pd
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    proposal=A/'BF16TwoSeed79_round154_proposal_v1_20261009.json';plan=read(proposal)
    cases=plan['scientific_cases'];assert len(cases)==73
    rng=np.random.default_rng(20261010154);n=30*31
    dates=np.repeat(np.arange(20200102,20200132),31)
    parent=np.round(rng.normal(size=n),2).astype(np.float64);valid=rng.uniform(size=n)>.11;flags=rng.uniform(size=n)<.13
    left=np.round(rng.normal(size=n),2).astype(np.float64);right=np.round(rng.normal(size=n),2).astype(np.float64)
    left[~valid]=right[~valid]=parent[~valid]=-1e6
    raw=(left+right)*.5;oracle_mean=((pd.Series(left)+pd.Series(right))/2.).to_numpy()
    assert np.array_equal(raw.view('u8'),oracle_mean.view('u8'))
    def exact(a,b):assert a.dtype==b.dtype==np.float64 and np.array_equal(a.view('u8'),b.view('u8'))
    records=[]
    for i,c in enumerate(cases):
        out=codec.transform(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign'])
        independent=codec.pandas_oracle(parent,raw,dates,flags,valid,c['role'],c['weight'],c['sign']);exact(out,independent)
        mask=codec.selected(flags,valid,c['role']);exact(out[~mask],parent[~mask])
        if not c['weight']:exact(out,parent)
        cold=[]
        for days in (5,12,26):
            count=days*31;mean_prefix=(left[:count]+right[:count])*.5
            prefix=codec.transform(parent[:count],mean_prefix,dates[:count],flags[:count],valid[:count],c['role'],c['weight'],c['sign'])
            independent_prefix=codec.pandas_oracle(parent[:count],mean_prefix,dates[:count],flags[:count],valid[:count],c['role'],c['weight'],c['sign'])
            exact(prefix,out[:count]);exact(independent_prefix,out[:count]);cold.append({'days':days,'rows':count,'bits_exact':True})
        records.append({'case':i,'configuration':c,'full_Pandas_bits_exact':True,'cold_controls':cold,'unselected_bits_exact':True})
    original=A/'verify_BF16Medium153_full73_training_v1_20261009.py';target=A/'verify_BF16TwoSeed154_full73_training_v1_20261009.py'
    syn=A/'BF16TwoSeed79_synthetic73_cold219_v1_20261009.json'
    pins={str(p):sha(p) for p in (Path(__file__),proposal,Path(codec.__file__),A/'BF16_complete_parent_rank_CDF_v1_20261008.py',original)}
    create(syn,{'status':'passed_actual73_synthetic_two_seed_equal_mean_signed_rank_mixes_and219_prefixes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_cases':73,'actual_cold_cases':219,
        'rows':n,'fixture_days':30,'fixture_codes':31,'records':records,'new_quality_scores':0,'actual_annual_fits_not_claimed':True,'test_labels_read':False})
    mathplan=A/'BF16TwoSeed79_round154_math_plan_v1_20261009.json'
    create(mathplan,{'status':'fixed_projection_of_original_two_seed154_proposal_for_training_math_controls',
        'input_sha256':{str(proposal):sha(proposal),str(syn):sha(syn)},'fixed_scientific_stage_base_round':148,
        'expected_full_cases':73,'new_cases':cases,'expected_quality_cases':79,'quality_anchor_rounds':plan['quality_anchor_rounds'],
        'official_scores':0,'test_labels_read':False})
    source=original.read_text(encoding='utf8').replace('BF16Medium153','BF16TwoSeed154').replace('medium153','two_seed154')
    source=source.replace('BF16TwoSeed154_complete_parent_rank_CDF_v1_20261009','BF16Medium153_complete_parent_rank_CDF_v1_20261009')
    source=source.replace("closed('BF16TwoSeed154_independent_full5_GPU_controls_v1_20261009')","closed('BF16TwoSeed154_equal_mean_full5_controls_v1_20261009')")
    source=source.replace('BF16Medium78_round153_proposal_v1_20261009.json','BF16TwoSeed79_round154_math_plan_v1_20261009.json')
    source=source.replace('actual_BF16TwoSeed154_full5_independent_location_v1_20261009.json','actual_BF16TwoSeed154_equal_mean_full5_location_v1_20261009.json')
    source=source.replace('BF16Medium78_synthetic73_cold219_v1_20261009.json','BF16TwoSeed79_synthetic73_cold219_v1_20261009.json')
    compile(source,str(target),'exec')
    with target.open('x',encoding='utf8') as f:f.write(source)
    meta=A/'BF16TwoSeed154_full73_controls_preparation_v1_20261009.json'
    create(meta,{'status':'passed73_synthetic_and219_prefixes_and_prepared_complete_historical_controls_after_real_mean',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),proposal,syn,mathplan,original,target)},
        'expected_full_historical_rows':5635800,'expected_full_cases':73,'expected_cold_cases':219,'actual_full_historical_controls_not_yet_claimed':True,
        'quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('BF16TwoSeed154_actual_full73_training_v1_20261009',target.name,[],{str(meta):sha(meta),str(target):sha(target)})
    create(A/'BF16TwoSeed154_full73_hidden_launch_v1_20261009.json',row);print({'synthetic':73,'cold':219,'queued_full_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
