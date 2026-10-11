"""Freeze a dropout-only contrast and queue six own fits after current GPU consumers."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    names=['neural_BF16_medium2048_seed09_e64_native_v1_20261009.py',
        'verify_neural_BF16_medium2048_seed09_restart_v1_20261009.py',
        'train_neural_BF16_medium2048_seed09_e64_bank6_v1_20261009.py',
        'neural_BF16_medium2048_seed09_independent_forward_v1_20261009.py']
    sources=[Path(__file__),ROOT/'后续选模标准.md'];targets=[]
    for name in names:
        original=A/name;target=A/name.replace('seed09','drop05_seed09')
        source=original.read_text(encoding='utf8');s=source.replace('seed09','drop05_seed09')
        if name.startswith('neural_') and '_native_' in name:
            assert s.count("'dropout': 0.")==1;s=s.replace("'dropout': 0.","'dropout': .05")
        if name.startswith('train_'):
            needle='    import joblib\n';assert s.count(needle)==1
            gate="""    # Preserve sole-GPU chronological resource ownership until all155 inference ends.
    predecessor=A/'service_owned_workflows_20261006/BF16Seed10_80_round155_full_registration_v1_20261009'
    while not (predecessor/'native_launch.json').exists() or owned(read(predecessor/'native_launch.json')):time.sleep(15)
    assert read(predecessor/'service_execution.json')['status']=='passed'
"""
            s=s.replace(needle,gate+needle)
        compile(s,str(target),'exec')
        with target.open('x',encoding='utf8') as f:f.write(s)
        sources.extend((original,target));targets.append(target)
    tree=ast.parse(targets[0].read_text(encoding='utf8'))
    cfg=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CONFIG' for t in n.targets)))
    oldpath=A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json';old=read(oldpath)['configuration'];sources.append(oldpath)
    assert cfg['dropout']==.05 and cfg['seed']==20261009 and cfg['epochs']==64
    assert {k:v for k,v in cfg.items() if k not in ('dropout','recipe')}=={k:v for k,v in old.items() if k not in ('dropout','recipe')}
    declaration=A/'neural_BF16_medium2048_drop05_seed09_e64_frontier_v1_20261009.json'
    create(declaration,{'status':'frozen_dropout_only_contrast_before_new_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'configuration':cfg,'comparison_configuration':old,'only_scientific_training_change':'dropout0_to0.05',
        'annual_years':list(range(2020,2026)),'all_six_own_fits_required':True,'old_weights_not_reused':True,
        'training_gpu_waits_actual_complete155_to_avoid_gpu_competition':True,
        'fixed_epochs_no_validation_early_stopping':True,'training_labels_only':True,'future_X_read':False,
        'test_labels_read':False,'new_quality_scores':0,'potential_future_round':156})
    weights=[.0005,.001,.002,.004,.008,.016,.032,.064,.125,.25,.5,1.]
    cases=[{'sign':1,'role':'all_valid','weight':0.}]
    cases.extend({'model':'rank_MLP2048_BF16_drop05_seed09_e64','sign':sign,'role':role,'weight':w}
        for sign in (1,-1) for role in ('all_valid','nonflag_valid','flag_valid') for w in weights)
    assert len(cases)==73
    proposal=A/'BF16Drop05_81_round156_proposal_v1_20261009.json'
    create(proposal,{'status':'frozen_dropout_contrast73_cases_and8_anchors_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(declaration):sha(declaration)},
        'configuration':cfg,'actual_scheme_base_round':148,'quality_anchor_rounds':list(range(148,156)),
        'new_cases':cases,'expected_quality_cases':81,'required_validation':'2020_to2024_complete_continuous_official_S',
        'transformation':'valid_only_signed_daily_rank_CDF_after_complete148_unselected_bits_preserved',
        'first2020_active':True,'full73_cold219_native42_independent_controls_required_before_quality':True,
        'actual_complete155_required_before_scoring':True,'actual_quality_scores':0,'future_X_read':False,
        'test_labels_read':False,'resource_or_global_search_exhaustion_claimed':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*targets,declaration,proposal]}
    rows={'control':start('actual_BF16_medium2048_drop05_seed09_restart_control_v1_20261009',targets[1].name,[],pins),
        'annual':start('actual_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009',targets[2].name,[],pins)}
    create(A/'neural_BF16_medium2048_drop05_seed09_e64_hidden_launches_v1_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
