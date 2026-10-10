"""Check nonselected block reranking for future-append invariance, without scoring."""
from copy import copy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import numpy as np
import optimize_training_round7 as experiment
from optimize_training_round7 import OUT,PREVIOUS,read,dump,log


def main():
    experiment.verify()
    ctx=experiment.Context();ctx.install('four_no_pruning');ctx.membership_mode='block';ctx.rerank_weight=.025
    promote=np.load(OUT/'promote_baseline.npy')
    full,_=ctx.predict(ctx.donor(promote),.24,.9845,.095)
    proofs=[]
    for count in (80,260):
        last=np.unique(ctx.dates)[count-1];n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={key:value[:n] for key,value in ctx.ranks.items()}
        replay,_=prefix.predict(prefix.donor(promote[:n]),.24,.9845,.095)
        assert np.array_equal(replay,full[:n]),last
        proofs.append({'membership_mode':'block','membership_weight':.025,'through_date':int(last),'days':count,'bit_identical':True})
    dump(OUT/'block_prefix_controls.json',{'status':'passed','test_data_read':False,'future_append_controls':proofs},immutable=True)
    log('Both nonzero block-reranking prefix controls passed')


if __name__=='__main__':main()
