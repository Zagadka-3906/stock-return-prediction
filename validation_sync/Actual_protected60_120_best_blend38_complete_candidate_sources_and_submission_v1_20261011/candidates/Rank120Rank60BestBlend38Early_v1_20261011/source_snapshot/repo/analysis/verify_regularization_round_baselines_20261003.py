"""Check both future regularization rounds against the actual frozen R18 output."""
from pathlib import Path
import sys
import time
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import optimize_training_round31 as round31
import optimize_training_round32 as round32
from replay_complete_scheme_20261003 import empty_roles
from finalize_training_round18 import ReleaseContext,selected


def main():
    qa=ROOT/'analysis/regularization_round_baselines_qa_20261003';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    source=ROOT/'analysis/optimization_20261003_r18';record=selected()
    ctx=ReleaseContext(record['winner']);frozen=np.load(source/'selected_validation.npy')
    cfg={**deepcopy(record['winner']),'standalone':None,'standalone_replacement':False,
         'secondary_augmentation':empty_roles(),'final_augmentation':empty_roles(),'final_limit_delta':0.,
         'linear_augmentation':empty_roles(),'linear_limit_delta':0.,
         'regularization_augmentation':empty_roles(),'regularization_limit_delta':0.}
    cfg31=round31.configuration(cfg)
    round31.FOUNDATION=source;round31.PREVIOUS=source;round31.baseline=lambda:deepcopy(cfg31)
    ctx.__class__=round31.Context;ctx.configure(cfg31)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg31['slow16_weight'],cfg31['retention'],cfg31['limit_up_delta'])
    assert np.array_equal(pred,frozen);proof31=round31.prefix_controls(ctx,cfg31)
    cfg32=round32.configuration(cfg)
    round32.PREVIOUS=source;round32.baseline=lambda:deepcopy(cfg32)
    ctx.__class__=round32.Context;ctx.configure(cfg32)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg32['slow16_weight'],cfg32['retention'],cfg32['limit_up_delta'])
    assert np.array_equal(pred,frozen);proof32=round32.prefix_controls(ctx,cfg32)
    round32.dump(qa/'verification.json',{'status':'passed','validation_rows':len(frozen),
         'full_round31_zero_added_signal_bit_identical':True,'round32_previous_output_bit_identical':True,
         'controls':[proof31,proof32],'new_model_scores':0,'test_data_read':False,
         'input_sha256':{str(path.resolve()):round32.sha(path) for path in (Path(__file__),
             ROOT/'analysis/optimize_training_round31.py',ROOT/'analysis/optimize_training_round32.py',
             source/'selected_validation.npy',source/'selection.json')},
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Both regularization round baselines and fresh prefixes passed.',flush=True)


if __name__=='__main__':main()
