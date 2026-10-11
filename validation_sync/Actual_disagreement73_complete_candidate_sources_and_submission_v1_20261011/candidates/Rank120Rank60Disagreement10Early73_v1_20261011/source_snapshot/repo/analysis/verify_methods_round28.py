"""Rebuild selected output and all standalone causal postprocessing controls."""
import numpy as np
from optimize_training_round28 import OUT,MODELS,baseline,standalone_cfg,prefix_controls,dump,log
from finalize_training_round28 import ReleaseContext,selected


def main():
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.promote('baseline')
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    controls=[prefix_controls(ctx,winner)]
    controls.extend(prefix_controls(ctx,standalone_cfg(name),counts=(80,260)) for name in MODELS)
    dump(OUT/'standalone_causal_checks.json',{'status':'passed','selected_output_bit_identical':True,
         'controls':controls,'new_model_training':False,'test_data_read':False,'new_scored_records':0},immutable=True)
    log('Round28 standalone prediction, poisoned labels and fully rebuilt date prefixes passed')


if __name__=='__main__':main()
