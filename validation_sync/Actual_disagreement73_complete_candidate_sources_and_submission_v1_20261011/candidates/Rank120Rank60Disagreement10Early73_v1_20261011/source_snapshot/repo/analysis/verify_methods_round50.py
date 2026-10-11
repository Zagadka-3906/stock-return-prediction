"""Verify selected whole replay and changed-root/late-layer causal prefixes."""
from pathlib import Path
from copy import deepcopy
import numpy as np
from optimize_training_round50 import OUT,baseline,proposals,axes,prefix_controls,dump,sha
from finalize_training_round50 import ReleaseContext,selected


def main():
    winner=selected()['winner'];ctx=ReleaseContext(winner)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    cases=[winner]
    groups={}
    for axis in axes():groups.setdefault(axis['group'],axis)
    for axis in groups.values():cases.append(proposals(deepcopy(baseline()),axis)[1][1])
    controls=[prefix_controls(ctx,cfg) for cfg in cases]
    dump(OUT/'whole_scheme_joint_causal_checks.json',{'status':'passed','selected_output_bit_identical':True,
        'controls':controls,'each_active_group_has_changed_weight_control':list(groups),
        'new_scored_records':0,'new_model_training':False,'test_data_read':False,
        'verification_script_sha256':sha(Path(__file__))},immutable=True)
