"""Matched uncovered widths: actual private-fitter parity."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
OUT=ROOT/'analysis/neural_width_preflight_20261004'

def normalized(c):
    c=dict(c)
    if c.get('rank_training_offset')==-.5:c.pop('rank_training_offset')
    return c

def main():
    import numpy as np
    import train_neural_width_bank_20261004 as bank
    import train_neural_regularization_bank_20261003 as control
    import neural_interaction_model_sources_20261004 as existing
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    baseline=control.CONFIGS['rank512_drop000_e32'];assert baseline==bank.COMMON
    assert bank.engine is not control.engine
    assert bank.engine.fit_arrays.__code__.co_code==control.engine.fit_arrays.__code__.co_code
    assert bank.engine.predict_arrays.__code__.co_code==control.engine.predict_arrays.__code__.co_code
    original_out,original_configs=control.engine.OUT,dict(control.engine.CONFIGS)
    changes={name:{k:v for k,v in cfg.items() if v!=baseline[k]} for name,cfg in bank.CONFIGS.items()}
    assert list(changes.values())==[{'hidden':[w,w//2,w//4]} for w in (1024,2048,4096,8192)]
    assert all(not [name for name,c in existing.CONFIGS.items() if normalized(c)==normalized(cfg)] for cfg in bank.CONFIGS.values())
    sources=[Path(__file__),Path(bank.__file__),bank.SOURCE,Path(control.__file__),
        ROOT/'results/optimization_20261003_r31.json',ROOT/'results/optimization_20261003_r35.json',Path(existing.__file__)]
    hashes={str(p.resolve()):bank.sha(p) for p in sources}
    bank.dump(OUT/'frozen_before_controls.json',{'status':'frozen_before_implementation_checks',
        'input_sha256':hashes,'configurations':bank.CONFIGS,'changes_from_control':changes,
        'existing_configuration_inventory':existing.CONFIGS,
        'no_identical_existing_configuration_after_target_offset_normalization':True,
        'training_validation_motivation_rounds':[31,35],'new_quality_scores':0,'test_labels_read':False},immutable=True)
    rng=np.random.default_rng(20261004);x=rng.standard_normal((1024,63)).astype(np.float32)
    x[::31,3]=np.nan;y=np.linspace(-.5,.5,len(x),dtype=np.float32)
    checks=[]
    for name,cfg in bank.CONFIGS.items():
        small={**cfg,'epochs':1};a=control.engine.fit_arrays(x,y,small);b=bank.engine.fit_arrays(x,y,small)
        assert np.array_equal(a['mean'],b['mean']) and np.array_equal(a['scale'],b['scale'])
        assert all(np.array_equal(a['state'][k].numpy(),b['state'][k].numpy()) for k in a['state'])
        full=bank.engine.predict_arrays(b,x);assert np.array_equal(full,control.engine.predict_arrays(a,x))
        for n in (1,80,1023):assert np.array_equal(full[:n],bank.engine.predict_arrays(b,x[:n]))
        checks.append({'model':name,'actual_one_epoch1024_row_preprocessing_weights_andpredictions_bit_identical':True,
            'fixed_padded_prediction_prefix_bit_identical':True})
    assert control.engine.OUT==original_out and control.engine.CONFIGS==original_configs
    for p,d in hashes.items():assert bank.sha(Path(p))==d,p
    bank.dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_private_fitter_controls':checks,'changes_from_control':changes,
        'original_trainer_globals_unchanged':True,'input_sha256':hashes,'new_quality_scores':0,'test_labels_read':False,
        'scope':'Four prespecified width extensions; original seed, data, target andoptimizer settings. Actual annual maturity/replay, full-model future controls andcomplete official output scores still required.'},immutable=True)
    print('All4 uncovered neural width fitter controls passed',flush=True)

if __name__=='__main__':main()
