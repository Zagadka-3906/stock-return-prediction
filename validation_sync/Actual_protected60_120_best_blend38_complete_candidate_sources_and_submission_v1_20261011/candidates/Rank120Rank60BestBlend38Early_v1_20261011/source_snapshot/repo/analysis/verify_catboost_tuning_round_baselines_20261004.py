"""New rounds preserve a real complete baseline and all prior shift components."""
from pathlib import Path
import sys
import time
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import optimize_training_round37 as role
import optimize_training_round38 as pure
from replay_complete_scheme_20261003 import empty_roles
from finalize_training_round18 import ReleaseContext,selected


def main():
    qa=ROOT/'analysis/catboost_tuning_round_baselines_qa_20261004';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    source=ROOT/'analysis/optimization_20261003_r18';record=selected()
    ctx=ReleaseContext(record['winner']);frozen=np.load(source/'selected_validation.npy')
    cfg={**deepcopy(record['winner']),'standalone':None,'standalone_replacement':False,
         'secondary_augmentation':empty_roles(),'final_augmentation':empty_roles(),'final_limit_delta':0.,
         'linear_augmentation':empty_roles(),'linear_limit_delta':0.,
         'regularization_augmentation':empty_roles(),'regularization_limit_delta':0.,
         'stacking_augmentation':empty_roles(),'stacking_limit_delta':0.,
         'neural_tuning_augmentation':empty_roles(),'neural_tuning_limit_delta':0.,
         'catboost_tuning_augmentation':empty_roles(),'catboost_tuning_limit_delta':0.}
    role_cfg=role.configuration(cfg)
    role.FOUNDATION=source;role.PREVIOUS=source;role.baseline=lambda:deepcopy(role_cfg)
    ctx.__class__=role.Context;ctx.configure(role_cfg)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),role_cfg['slow16_weight'],role_cfg['retention'],role_cfg['limit_up_delta'])
    assert np.array_equal(pred,frozen);role_proof=role.prefix_controls(ctx,role_cfg)
    # Observe the complete shift passed to the final constructor without scoring.
    shifted=deepcopy(role_cfg)
    for key,value in zip(('final_limit_delta','linear_limit_delta','regularization_limit_delta','stacking_limit_delta','neural_tuning_limit_delta'),(.01,-.02,.03,.04,.05)):shifted[key]=value
    role.baseline=lambda:deepcopy(shifted);ctx.configure(shifted)
    captured=[];finish=ctx.finish_output
    ctx.finish_output=lambda base,retention,delta:(captured.append(delta) or base,{})
    ctx.predict(ctx.donor(ctx.finished('baseline')),shifted['slow16_weight'],shifted['retention'],shifted['limit_up_delta'])
    expected=shifted['limit_up_delta']+shifted['final_limit_delta']+shifted['linear_limit_delta']+shifted['regularization_limit_delta']+shifted['stacking_limit_delta']+shifted['neural_tuning_limit_delta']
    assert captured==[expected]
    del ctx.finish_output
    role.baseline=lambda:deepcopy(role_cfg)
    pure_cfg=pure.configuration(cfg)
    pure.PREVIOUS=source;pure.baseline=lambda:deepcopy(pure_cfg)
    ctx.__class__=pure.Context;ctx.configure(pure_cfg)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),pure_cfg['slow16_weight'],pure_cfg['retention'],pure_cfg['limit_up_delta'])
    assert np.array_equal(pred,frozen);pure_proof=pure.prefix_controls(ctx,pure_cfg)
    pure.baseline=lambda:deepcopy(shifted)
    standalone=pure.standalone_cfg(next(iter(pure.MODELS)))
    for group in ('diverse_augmentation','secondary_augmentation','final_augmentation','linear_augmentation','regularization_augmentation','stacking_augmentation','neural_tuning_augmentation','catboost_tuning_augmentation'):
        assert all(spec['weight']==0 for spec in standalone[group].values()),group
    for key in ('final_limit_delta','linear_limit_delta','regularization_limit_delta','stacking_limit_delta','neural_tuning_limit_delta','catboost_tuning_limit_delta'):assert standalone[key]==0,key
    paths=[Path(__file__),ROOT/'analysis/optimize_training_round37.py',ROOT/'analysis/optimize_training_round38.py',
           ROOT/'analysis/catboost_tuning_rounds_prepared_20261004.json',source/'selected_validation.npy',source/'selection.json']
    role.dump(qa/'verification.json',{'status':'passed','validation_rows':len(frozen),
         'round37_zero_added_signal_bit_identical':True,'round38_previous_output_bit_identical':True,
         'controls':[role_proof,pure_proof],'all_six_foundation_limit_shift_components_forwarded':True,
         'standalone_clears_all_eight_augmentation_groups':True,'new_model_scores':0,'test_data_read':False,
         'input_sha256':{str(p.resolve()):role.sha(p) for p in paths},
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Neural tuning round full baselines, prefix checks, cumulative shifts and standalone isolation passed.',flush=True)


if __name__=='__main__':main()
