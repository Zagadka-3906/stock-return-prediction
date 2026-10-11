"""Check causality of the new rule even though selection kept the zero-weight baseline."""
from copy import copy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from finalize_training_round10 import ReleaseContext,selected
from optimize_training_round10 import OUT,dump,sha,log


def main():
    import numpy as np
    import polars as pl
    record=selected();winner=record['winner'];ctx=ReleaseContext(winner)
    ctx.add_priority_weight=.05;ctx.drop_priority_weight=.5
    promote=ctx.finished('baseline');donor=ctx.donor(promote)
    prediction,stats=ctx.predict(donor,winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    poisoned=copy(ctx)
    poisoned.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    poisoned.label_free=ctx.label_free.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    replay,_=poisoned.predict(poisoned.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(prediction,replay),'Label poisoning affected membership/output'
    prefixes=[];dates=np.unique(ctx.dates)
    for count in (80,260,975):
        last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'))
        prefix=copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):
            setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={key:value[:n] for key,value in ctx.ranks.items()}
        result,_=prefix.predict(prefix.donor(promote[:n]),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
        assert np.array_equal(prediction[:n],result),last
        prefixes.append({'days':count,'through_date':last,'bit_identical':True})
    assert not np.array_equal(prediction,np.load(OUT/'selected_validation.npy')),'Nonzero control was inactive'
    dump(OUT/'nonzero_priority_causal_checks.json',{'status':'passed','add_priority_weight':.05,'drop_priority_weight':.5,
         'nonzero_control_changes_prediction':True,'label_poisoning_bit_identical':True,
         'future_append_prefix_invariance':prefixes,'construction':stats,'test_data_read':False,
         'new_scored_records':0,'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round10 nonzero priority label poisoning and all three causal prefixes passed')


if __name__=='__main__':main()
