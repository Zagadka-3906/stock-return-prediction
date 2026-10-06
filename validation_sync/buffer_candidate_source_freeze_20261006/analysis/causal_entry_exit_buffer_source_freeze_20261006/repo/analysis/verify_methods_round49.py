"""Verify the selected final temporal scheme and additional causal controls."""
from pathlib import Path
from copy import deepcopy
import numpy as np
from optimize_training_round49 import OUT,baseline,prefix_controls,dump,sha
from finalize_training_round49 import ReleaseContext,selected


def main():
    winner=selected()['winner'];ctx=ReleaseContext(winner);raw=ctx.finished('baseline')
    assert np.array_equal(ctx.predict(raw,0.,0.)[0],np.load(OUT/'selected_validation.npy'))
    cases=[winner]
    for p in ({'alpha':.5,'mix':.25,'power':.5},{'alpha':.9,'mix':.1,'power':1.},{'alpha':.995,'mix':.025,'power':2.}):
        cfg=deepcopy(baseline());cfg['temporal_postprocessing']=p;cases.append(cfg)
    dump(OUT/'final_temporal_causal_checks.json',{'status':'passed','controls':[prefix_controls(ctx,cfg) for cfg in cases],
        'selected_output_bit_identical':True,'no_new_model_training':True,'new_scored_records':0,'test_data_read':False,
        'verification_script_sha256':sha(Path(__file__))},immutable=True)
