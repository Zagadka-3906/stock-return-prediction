"""Replay active priority/fusion rules with poisoned labels and truncated dates."""
from copy import copy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from finalize_training_round11 import ReleaseContext,selected
from optimize_training_round11 import OUT,dump,sha,log


def main():
    import numpy as np
    import polars as pl
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.finished('baseline');checks=[]
    for signal,member_signal,mode in (('slow_finished','top','within_block'),('rest','rest','global')):
        cfg=dict(winner,priority_signal=signal,add_priority_weight=.05,drop_priority_weight=.5,
                 membership_signal=member_signal,membership_mode=mode,membership_w5a_weight=.25)
        ctx.configure(cfg)
        prediction,stats=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        poison=copy(ctx)
        poison.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
        poison.label_free=ctx.label_free.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
        replay,_=poison.predict(poison.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        assert np.array_equal(prediction,replay),'Label poisoning changed prediction'
        prefixes=[];dates=np.unique(ctx.dates)
        for count in (80,260,975):
            last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
            for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):
                setattr(prefix,name,getattr(ctx,name)[:n])
            prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={key:value[:n] for key,value in ctx.ranks.items()}
            values,_=prefix.predict(prefix.donor(promote[:n]),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
            assert np.array_equal(prediction[:n],values),last
            prefixes.append({'days':count,'through_date':last,'bit_identical':True})
        assert not np.array_equal(prediction,np.load(OUT/'selected_validation.npy')),'Active control was ineffective'
        checks.append({'priority_signal':signal,'membership_signal':member_signal,'membership_mode':mode,
                       'add_priority_weight':.05,'drop_priority_weight':.5,'membership_weight':.25,
                       'label_poisoning_bit_identical':True,'active_control_changes_prediction':True,
                       'future_append_prefix_invariance':prefixes,'construction':stats})
    dump(OUT/'nonzero_method_causal_checks.json',{'status':'passed','controls':checks,'test_data_read':False,
         'new_scored_records':0,'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round11 both membership modes, active priorities, label poisoning and causal prefixes passed')


if __name__=='__main__':main()
