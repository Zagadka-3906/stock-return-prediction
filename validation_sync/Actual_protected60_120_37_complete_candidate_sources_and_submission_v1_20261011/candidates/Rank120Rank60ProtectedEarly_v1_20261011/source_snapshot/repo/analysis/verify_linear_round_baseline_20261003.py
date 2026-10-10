"""Check prospective baseline replay against a complete frozen R18 output."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
from copy import deepcopy
import optimize_training_round28 as round28
import optimize_training_round29 as round29
from finalize_training_round18 import ReleaseContext,selected


def main():
    folder=ROOT/'analysis/linear_round_baseline_qa_20261003';folder.mkdir(exist_ok=True)
    assert not (folder/'verification.json').exists()
    record=selected();source=ROOT/'analysis/optimization_20261003_r18'
    ctx=ReleaseContext(record['winner']);frozen=np.load(source/'selected_validation.npy')
    empty={role:{'model':'none','weight':0.,'blend':'score'} for role in ('membership','top','rest')}
    base={**deepcopy(record['winner']),'secondary_augmentation':deepcopy(empty),
          'standalone':None,'standalone_replacement':False,
          'final_augmentation':{role:{'model':'none','weight':0.} for role in empty},'final_limit_delta':0.}
    cfg28=round28.configuration(base)
    round28.PREVIOUS=source;round28.baseline=lambda:deepcopy(cfg28)
    ctx.__class__=round28.Context;ctx.configure(cfg28)
    p28,_=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg28['slow16_weight'],cfg28['retention'],cfg28['limit_up_delta'])
    assert np.array_equal(p28,frozen)
    proof28=round28.prefix_controls(ctx,cfg28)
    cfg29={**cfg28,'linear_augmentation':{role:{'model':'none','weight':0.} for role in empty},'linear_limit_delta':0.}
    round29.FOUNDATION=source;round29.PREVIOUS=source;round29.baseline=lambda:deepcopy(cfg29)
    ctx.__class__=round29.Context;ctx.configure(cfg29)
    p29,_=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg29['slow16_weight'],cfg29['retention'],cfg29['limit_up_delta'])
    assert np.array_equal(p29,frozen)
    proof29=round29.prefix_controls(ctx,cfg29)
    round29.dump(folder/'verification.json',{'status':'passed','complete_frozen_baseline_round':18,
         'full_validation_rows':len(frozen),'round28_complete_baseline_bit_identical':True,
         'round29_zero_added_signal_bit_identical':True,'prefix_and_label_poisoning_controls':[proof28,proof29],
         'test_data_read':False,'new_official_scores':0,
         'source_sha256':{str(p.resolve()):round29.sha(p) for p in (
             Path(__file__),ROOT/'analysis/optimize_training_round28.py',ROOT/'analysis/optimize_training_round29.py',
             source/'selected_validation.npy',source/'selection.json')},
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Both prospective complete baselines and fresh prefixes passed.',flush=True)


if __name__=='__main__':main()
