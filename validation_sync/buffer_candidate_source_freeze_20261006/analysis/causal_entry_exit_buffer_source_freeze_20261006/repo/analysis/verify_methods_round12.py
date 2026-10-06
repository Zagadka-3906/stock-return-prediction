"""Rebuild TopK prefix signals and verify independent membership causality."""
from copy import copy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from finalize_training_round12 import ReleaseContext,selected
from optimize_training_round12 import OUT,dump,sha,log


def main():
    import numpy as np
    import polars as pl
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.promote('baseline')
    assert np.array_equal(promote,ctx.rebuild_recipe(winner['recipe']))
    cases=[winner,dict(winner,membership_ensemble_name='lgb0.75_xgb1_two0_gru1',
           membership_slow_weight=.125,membership_mode='within_block',membership_w5a_weight=.25,
           priority_signal='rest',add_priority_weight=.05,drop_priority_weight=.5)]
    checks=[]
    for index,cfg in enumerate(cases):
        ctx.configure(cfg)
        pred,stats=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        if index==0:assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
        poison=copy(ctx)
        poison.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
        poison.label_free=ctx.label_free.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
        poisoned_promote=poison.rebuild_recipe(cfg['recipe'])
        assert np.array_equal(promote,poisoned_promote)
        replay,_=poison.predict(poison.donor(poisoned_promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        assert np.array_equal(pred,replay),'Poisoned labels changed predictions'
        prefixes=[];dates=np.unique(ctx.dates)
        for count in (80,260,975):
            last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
            for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):
                setattr(prefix,name,getattr(ctx,name)[:n])
            prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={k:v[:n] for k,v in ctx.ranks.items()}
            prefix.frame=ctx.frame.head(n);prefix.label_free=ctx.label_free.head(n)
            rebuilt=prefix.rebuild_recipe(cfg['recipe'])
            assert np.array_equal(promote[:n],rebuilt),'Future suffix changed TopK finishing'
            replay,_=prefix.predict(prefix.donor(rebuilt),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
            assert np.array_equal(pred[:n],replay),last
            prefixes.append({'days':count,'through_date':last,'topk_rebuilt_bit_identical':True,'prediction_bit_identical':True})
        checks.append({'selected_scheme':index==0,'membership_ensemble_name':cfg['membership_ensemble_name'],
                       'membership_mode':cfg['membership_mode'],'label_poisoning_bit_identical':True,
                       'future_append_prefix_invariance':prefixes,'construction':stats})
    dump(OUT/'independent_membership_causal_checks.json',{'status':'passed','controls':checks,
         'selected_topk_rebuilt_bit_identical':True,'test_data_read':False,'new_scored_records':0,
         'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round12 independently rebuilt TopK prefixes, label poisoning and independent membership passed')


if __name__=='__main__':main()
