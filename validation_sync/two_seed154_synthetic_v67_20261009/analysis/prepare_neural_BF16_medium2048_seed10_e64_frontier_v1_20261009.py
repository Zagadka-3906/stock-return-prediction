"""Declare a second independent seed and fixed equal-weight two-seed ensemble before quality."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    names=['neural_BF16_medium2048_seed09_e64_native_v1_20261009.py',
        'verify_neural_BF16_medium2048_seed09_restart_v1_20261009.py',
        'train_neural_BF16_medium2048_seed09_e64_bank6_v1_20261009.py',
        'neural_BF16_medium2048_seed09_independent_forward_v1_20261009.py']
    inputs=[Path(__file__)];targets=[]
    for name in names:
        original=A/name;target=A/name.replace('seed09','seed10');source=original.read_text(encoding='utf8')
        s=source.replace('seed09','seed10')
        if name.startswith('neural_') and '_native_' in name:
            needle="'seed': 20261009";assert s.count(needle)==1;s=s.replace(needle,"'seed': 20261010")
        compile(s,str(target),'exec')
        with target.open('x',encoding='utf8') as f:f.write(s)
        targets.append(target);inputs.extend((original,target))
    tree=ast.parse(targets[0].read_text(encoding='utf8'))
    cfg=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in n.targets)))
    assert cfg['seed']==20261010 and cfg['hidden']==[2048,1024,512] and cfg['epochs']==64 and cfg['learning_rate']==.0005
    old=read(A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json')['configuration']
    assert {k:v for k,v in cfg.items() if k not in ('seed','recipe')}=={k:v for k,v in old.items() if k not in ('seed','recipe')}
    inputs.append(A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json')
    declaration=A/'neural_BF16_medium2048_seed10_e64_frontier_v1_20261009.json'
    create(declaration,{'status':'declared_independent_seed10_six_mature_fits_before_any_154_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'configuration':cfg,
        'annual_years':[2020,2021,2022,2023,2024,2025],'old_seed09_weights_not_reused':True,
        'training_labels_only':True,'future_X_read':False,'test_labels_read':False,'new_quality_scores':0,
        'actual_new_native_fits_not_yet_claimed':True,'fixed_epochs_no_early_stopping':True,'potential_future_round':154})
    proposal=A/'BF16TwoSeed79_round154_proposal_v1_20261009.json'
    weights=[.0005,.001,.002,.004,.008,.016,.032,.064,.125,.25,.5,1.]
    cases=[{'model':'fixed_equal_seed09_seed10_mean','sign':sign,'role':role,'weight':w} for sign in (1,-1) for role in ('all_valid','nonflag_valid','flag_valid') for w in weights]
    cases.append({'model':'zero_two_seed_residual_identity','sign':1,'role':'all_valid','weight':0.})
    assert len(cases)==73
    create(proposal,{'status':'frozen_two_seed_ensemble_grid_before_153_and154_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(declaration):sha(declaration)},
        'actual_scheme_base_round':148,'quality_anchor_rounds':[148,149,150,151,152,153],
        'seed_values':[20261009,20261010],'raw_ensemble_arithmetic':'(seed09_float64 + seed10_float64) * 0.5; invalid rows stay -1e6',
        'transformation':'daily rank CDF of valid-only signed ensemble after complete148; unselected parent bits preserved',
        'first2020_active':True,'scientific_cases':cases,'expected_quality_cases':79,
        'actual_12_saved_annual_states_native_independent_full_and_cold_controls_required':True,
        'actual_153_full_registration_required_before_scoring':True,'actual_quality_scores':0,
        'future_X_read':False,'test_labels_read':False,'resource_or_global_search_exhaustion_claimed':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*targets,declaration,proposal]}
    rows={'control':start('actual_BF16_medium2048_seed10_restart_control_v1_20261009',targets[1].name,[],pins),
        'annual':start('actual_BF16_medium2048_seed10_e64_bank6_v1_20261009',targets[2].name,[],pins)}
    create(A/'neural_BF16_medium2048_seed10_e64_hidden_launches_v1_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)

if __name__=='__main__':main()
