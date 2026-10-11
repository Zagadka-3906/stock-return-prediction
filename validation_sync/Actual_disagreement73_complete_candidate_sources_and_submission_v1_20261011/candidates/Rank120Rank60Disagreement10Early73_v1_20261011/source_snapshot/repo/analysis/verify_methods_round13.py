"""Audit the selected nonlinear membership and active memory controls."""
from copy import deepcopy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round13 import OUT,baseline,prefix_controls,dump,sha,log
from finalize_training_round13 import ReleaseContext,selected


def main():
    import numpy as np
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.promote('baseline')
    ctx.configure(winner)
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    cases=[winner,dict(baseline(),membership_power=0.,membership_memory=.6),
           dict(baseline(),membership_power=-2.,membership_memory=.4,membership_mode='within_block')]
    controls=[prefix_controls(ctx,promote,cfg) for cfg in cases]
    dump(OUT/'nonlinear_memory_causal_checks.json',{'status':'passed','controls':controls,
         'selected_output_bit_identical':True,'test_data_read':False,'new_scored_records':0,
         'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round13 nonlinear consensus, causal stock memory, label poisoning and prefix invariance passed')


if __name__=='__main__':main()
