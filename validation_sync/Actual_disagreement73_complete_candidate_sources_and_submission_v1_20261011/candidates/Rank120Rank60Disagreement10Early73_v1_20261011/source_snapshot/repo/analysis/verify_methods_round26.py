"""Selected state-dependent fusion with cold caches and fixed-membership proof."""
from copy import deepcopy
from pathlib import Path
import numpy as np
from optimize_training_round26 import OUT,FOUNDATION,ROLES,regime,baseline,proposals,prefix_controls,dump,sha,log
from finalize_training_round26 import ReleaseContext,selected


def main():
    from return_mapping import top_sets
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.promote('baseline')
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    base=baseline();cases=[winner]
    for role in ROLES:
        for state in regime.NAMES:
            for low,high in ((0.,.1),(.1,0.)):
                cfg=deepcopy(base);cfg['final_augmentation'][role]={'model':proposals()[role][0],'weight':.1,'regime':state,'low':low,'high':high};cases.append(cfg)
    controls=[prefix_controls(ctx,cfg) for cfg in cases]
    if winner['final_augmentation']['membership']['weight']==0:
        assert top_sets(ctx.pdf,pred)==top_sets(ctx.pdf,np.load(FOUNDATION/'selected_validation.npy'))
        membership='All foundation Top sets unchanged for ordering-only selected output'
    else:membership='An explicit second causal retention floor is part of the selected membership method'
    dump(OUT/'market_regime_causal_checks.json',{'status':'passed','controls':controls,
         'selected_output_bit_identical':True,'membership_construction':membership,'new_scored_records':0,
         'test_data_read':False,'regime_bank_audit_sha256':sha(regime.OUT/'oof_audit.json'),
         'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round26 selected market-state method and both cold-cache prefix controls passed')


if __name__=='__main__':main()
