"""Verify selected recomputation, poisoned labels and freshly computed prefixes."""
import numpy as np
from optimize_training_round30 import OUT,prefix_controls,dump,log
from finalize_training_round30 import ReleaseContext,selected

def main():
    winner=selected()['winner'];ctx=ReleaseContext(winner)
    promote=ctx.finished('baseline');pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    controls=prefix_controls(ctx,winner)
    dump(OUT/'complete_scheme_causal_checks.json',{'status':'passed','selected_output_bit_identical':True,
         'controls':controls,'new_model_training':False,'test_data_read':False,'new_scored_records':0},immutable=True)
    log('Round30 complete reconstruction, poisoned labels and cold prefixes passed')

if __name__=='__main__':main()
