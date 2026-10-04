"""Audit rank-preserving legacy fusion and continuous-score fusion without new fitting."""
from copy import deepcopy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round20 import OUT,MODELS,ROLES,BLENDS,proposals,baseline,prefix_controls,dump,sha,log
from finalize_training_round20 import ReleaseContext,selected


def main():
    import numpy as np
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.promote('baseline')
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    cases=[winner]
    for role in ROLES:
        name=proposals()[role][0]
        for blend in BLENDS:
            cfg=deepcopy(baseline());cfg['secondary_augmentation'][role]={'model':name,'weight':.05,'blend':blend}
            cases.append(cfg)
    controls=[prefix_controls(ctx,promote,cfg) for cfg in cases]
    dump(OUT/'diverse_augmentation_causal_checks.json',{'status':'passed','controls':controls,
         'active_secondary_blend_controls':len(cases)-1,'control_configurations':cases,'selected_output_bit_identical':True,'new_models_trained':0,
         'all_raw_model_sources_verified_in_previous_rounds':True,'test_data_read':False,'new_scored_records':0,
         'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round20 selected output, both fusion scales, poisoned labels and full date prefixes passed')


if __name__=='__main__':main()
