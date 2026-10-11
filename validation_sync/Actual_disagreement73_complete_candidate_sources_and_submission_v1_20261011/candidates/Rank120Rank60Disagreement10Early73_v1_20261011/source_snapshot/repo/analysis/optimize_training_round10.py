"""Waves68–70: independent priorities for retention additions and removals."""
from __future__ import annotations
import argparse
import itertools
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round9 as previous
from optimize_training_round9 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r10'
PREVIOUS=ROOT/'analysis/optimization_20261003_r9'
RANKERS=ROOT/'analysis/optimization_20261003_r8/rankers'
EXPECTED=.44882887216021156
WAVES=(68,69,70)
PRIORITY_WEIGHTS=(.025,.1,.25,.5,1.)
FINE_OFFSETS=(-.05,0.,.05)
RETENTIONS=(.9835,.984,.9845,.985,.9855)
SHIFTS=(.055,.075,.095,.115,.135)


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round9 import selected
    winner=selected()['winner']
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/retention_priority_round10.py',ROOT/'analysis/finalize_training_round10.py',
             ROOT/'后续选模标准.md',ROOT/'evaluate.py',ROOT/'active_release.json',
             ROOT/'analysis/optimize_training_round9.py',ROOT/'analysis/finalize_training_round9.py',
             ROOT/'analysis/optimize_training_round8.py',ROOT/'analysis/optimize_training_round7.py',
             ROOT/'analysis/finalize_training_round7.py',ROOT/'analysis/finalize_optimization.py',
             HERE/'optimize_wave13.py',HERE/'optimize_wave15.py',HERE/'combined_fold_frame.parquet',
             PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
             PREVIOUS/'component_audit.json',ROOT/'candidates/optimization_20261003_r9/verification.json']
    sources += [RANKERS/f'{winner[key]}.npy' for key in ('ensemble_name','top_ensemble_name')]
    sources += [PREVIOUS/f'raw/source_topk_{year}.json' for year in YEARS]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':EXPECTED,'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'starting_winner':winner,'priority_signal':'Current-day percentile rank of the learned Top orderer.',
         'coarse_grid':{'modes':['add_only','drop_only','both'],'weights':PRIORITY_WEIGHTS,'baseline':True},
         'fine_grid':'Cartesian clipped +/-0.05 and unchanged addition/removal weights around the coarse winner.',
         'fine_offsets':FINE_OFFSETS,'retentions':RETENTIONS,'shifts':SHIFTS,
         'fixed_membership':'Unconstrained donor Top decile stays fixed; only choices during retention swaps change.',
         'priority_blend':'(1-weight)*daily donor rank + weight*daily Top orderer rank; weight zero uses original donor.',
         'causality':'Only current predictions, stock codes, limit-up flags and previously selected codes enter membership.',
         'selection_rule':'highest official connected composite; exact ties prefer lower total priority weight',
         'expected_scored_records':35,'new_model_training':False,'pruned_member_excluded':True,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round10 retention-priority protocol frozen')


class Context(previous.Context):
    def __init__(self):
        super().__init__()
        self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        winner=read(PREVIOUS/'selection.json')['winner']
        self.roles(winner['top_ensemble_name'],winner['ensemble_name'])
        self.top_slow_weight=winner['top_slow_weight']
        self.add_priority_weight=self.drop_priority_weight=0.

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline'
        if recipe is not None:assert recipe==read(PREVIOUS/'selection.json')['winner']['recipe']
        return np.load(PREVIOUS/'promote_baseline.npy')

    def predict(self,donor,weight,retention,delta=0.):
        import numpy as np
        import pandas as pd
        from optimize_wave15 import weighted_rank_blend
        from retention_priority_round10 import build_priority
        n=len(self.dates)
        def ordering(values,ranks,w):
            blend=weighted_rank_blend([values,self.slow],[1-w,w],ranks,self.valid,self.dates,('w5a','slow'))
            return np.where(blend>-9,blend+1e-9*self.tie_key,blend)+1e-9*self.tie_key
        a=ordering(self.top_values[:n],{'w5a':self.top_ranks[:n],'slow':self.ranks['slow']},self.top_slow_weight)
        b=ordering(self.w5a,self.ranks,weight)
        if self.add_priority_weight or self.drop_priority_weight:
            # Recompute on the supplied dates, including in independent causal-prefix replay.
            donor_rank=pd.Series(donor).groupby(self.dates).rank(method='average',pct=True).to_numpy()
            top_rank=pd.Series(a).groupby(self.dates).rank(method='average',pct=True).to_numpy()
            def priority(w):return donor if w==0 else (1-w)*donor_rank+w*top_rank
            adds=priority(self.add_priority_weight);drops=priority(self.drop_priority_weight)
        else:adds=drops=donor
        pred,stats=build_priority(donor,a,b,self.dates,self.flags,self.codes,self.n_codes,retention,adds,drops)
        pred[self.flags==1]+=delta
        return pred,stats


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();winner=read(PREVIOUS/'selection.json')['winner']
    donor=ctx.donor(ctx.finished('baseline'))
    pred,stats=ctx.predict(donor,winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    for year in YEARS:dump(OUT/f'raw/source_topk_{year}.json',read(PREVIOUS/f'raw/source_topk_{year}.json'),immutable=True)
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_prediction_bit_identical':True,
         'baseline_construction':stats,'test_data_read':False,'new_model_training':False,
         'pruned_member_excluded':True,'constraints_asserted_every_day':True},immutable=True)
    log('Round10 zero-priority baseline rebuilt bit identically')


def best(rows):
    return min(rows,key=lambda r:(-r['connected_final_score'],r['add_priority_weight']+r['drop_priority_weight'],
                                 r['add_priority_weight'],r['drop_priority_weight']))


def evaluate(ctx,add,drop,retention=.984,shift=.075):
    ctx.add_priority_weight=add;ctx.drop_priority_weight=drop
    pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),.20,retention,shift)
    metrics=ctx.score(pred)
    log(f'Round10 add={add:g} drop={drop:g} retain={retention:g} shift={shift:g}: {metrics["final_score"]:.9f}')
    winner=read(PREVIOUS/'selection.json')['winner']
    return {**{key:value for key,value in winner.items() if key not in ('wave','arm','metrics','construction','connected_final_score')},
            'retention':retention,'limit_up_delta':shift,'retention_priority_signal':'top_orderer_daily_rank',
            'add_priority_weight':add,'drop_priority_weight':drop,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def coarse():
    verify();build();ctx=Context();path=OUT/'wave68_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    arms=[('baseline',0.,0.)]
    for w in PRIORITY_WEIGHTS:arms += [(f'add{w:g}',w,0.),(f'drop{w:g}',0.,w),(f'both{w:g}',w,w)]
    for key,add,drop in arms:
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,add,drop);dump(path,result)
            if key=='baseline':assert abs(result['results'][key]['connected_final_score']-EXPECTED)<1e-12
    result['status']='complete';dump(path,result)


def fine():
    verify();prior=read(OUT/'wave68_results.json');assert prior['status']=='complete'
    winner=best(prior['results'].values())
    pairs=[(min(1.,max(0.,winner['add_priority_weight']+a)),min(1.,max(0.,winner['drop_priority_weight']+d)))
           for a,d in itertools.product(FINE_OFFSETS,FINE_OFFSETS)]
    dump(OUT/'fine_protocol.json',{'winner_before_fine':winner,'pairs':pairs,'duplicates_retained':True},immutable=True)
    ctx=Context();path=OUT/'wave69_results.json';result=read(path) if path.exists() else {'status':'running','results':{}}
    for index,(add,drop) in enumerate(pairs):
        key=f'local{index}_add{add:g}_drop{drop:g}'
        if key not in result['results']:result['results'][key]=evaluate(ctx,add,drop);dump(path,result)
    result['status']='complete';dump(path,result)


def refinement():
    verify();rows=[]
    for wave in (68,69):
        prior=read(OUT/f'wave{wave}_results.json');assert prior['status']=='complete';rows+=list(prior['results'].values())
    winner=best(rows)
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner,'retentions':RETENTIONS,'shifts':SHIFTS},immutable=True)
    ctx=Context();path=OUT/'wave70_results.json';result=read(path) if path.exists() else {'status':'running','results':{}}
    for retention in RETENTIONS:
        key=f'retention{retention:g}'
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,winner['add_priority_weight'],winner['drop_priority_weight'],retention);dump(path,result)
    winner=best(rows+list(result['results'].values()))
    for shift in SHIFTS:
        key=f'limit_shift{shift:g}'
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,winner['add_priority_weight'],winner['drop_priority_weight'],winner['retention'],shift);dump(path,result)
    result['status']='complete';dump(path,result)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','coarse','fine','refinement','all'))
    stage=parser.parse_args().stage
    for name in (('freeze','build','coarse','fine','refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
