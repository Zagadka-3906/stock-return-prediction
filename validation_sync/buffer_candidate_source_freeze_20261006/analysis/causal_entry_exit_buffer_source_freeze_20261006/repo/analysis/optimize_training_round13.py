"""Waves81–84: nonlinear membership consensus and causal stock-level memory."""
from __future__ import annotations
import argparse
from copy import deepcopy,copy
import itertools
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round12 as previous
from optimize_training_round12 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r13'
PREVIOUS=ROOT/'analysis/optimization_20261003_r12'
EXPECTED=.44913731266032064
WAVES=(81,82,83,84)
FIELDS=previous.FIELDS+('membership_power','membership_memory')
POWERS=(-4.,-2.,-1.,0.,.5,1.,2.,4.,8.)
MEMORIES=(0.,.2,.4,.6,.75,.85,.925)
FUSIONS=(.70,.725,.75,.775,.80)


def baseline():
    old=read(PREVIOUS/'selection.json')['winner']
    return {**previous.configuration(old),'membership_power':1.,'membership_memory':0.}


def configuration(row):return {k:deepcopy(row[k]) for k in FIELDS}


def signature(row):
    import json
    return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))


def best(rows):
    return min(rows,key=lambda r:(-r['connected_final_score'],r['membership_memory']!=0.,r['membership_power']!=1.,signature(r)))


def power_consensus(a,b,weight,power):
    import numpy as np
    assert 0<=weight<=1 and np.all(a>0) and np.all(b>0)
    if power==1:return (1-weight)*a+weight*b
    if power==0:return np.exp((1-weight)*np.log(a)+weight*np.log(b))
    return ((1-weight)*a**power+weight*b**power)**(1/power)


def stock_memory(values,dates,codes,n_codes,rho):
    import numpy as np
    assert 0<=rho<1
    if rho==0:return values
    result=values.copy();state=np.full(n_codes,np.nan)
    _,starts=np.unique(dates,return_index=True);ends=np.append(starts[1:],len(dates))
    for start,end in zip(starts,ends):
        rows=np.arange(start,end);rows=rows[values[start:end]>-9]
        stock=codes[rows];prior=state[stock];seen=np.isfinite(prior)
        fresh=values[rows].copy();fresh[seen]=(1-rho)*fresh[seen]+rho*prior[seen]
        result[rows]=fresh;state[stock]=fresh
    assert np.isfinite(result).all()
    return result


class Context(previous.Context):
    def __init__(self):
        super().__init__();self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())

    def configure(self,cfg):
        super().configure(cfg)
        self.membership_power=cfg.get('membership_power',1.);self.membership_memory=cfg.get('membership_memory',0.)

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline' and (recipe is None or recipe==baseline()['recipe'])
        return np.load(PREVIOUS/'promote_baseline.npy')

    def donor(self,promote,rerank_weight=None):
        import numpy as np
        from optimize_wave15 import daily_ranks
        from optimize_wave18 import lift
        from analysis.topset_hybrid_20261002.fold_validation import top_sets
        if self.membership_power==1. and self.membership_memory==0.:return super().donor(promote,rerank_weight)
        weight=self.rerank_weight if rerank_weight is None else rerank_weight
        if weight==0:return super().donor(promote,0.)
        signal=self.membership_orderer();a=daily_ranks(self.slow_finished,self.valid,self.dates)
        b=daily_ranks(signal,self.valid,self.dates);valid=(a>-9)&(b>-9)
        reranker=np.full(len(promote),-10.);reranker[valid]=power_consensus(a[valid],b[valid],weight,self.membership_power)
        promoted=np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*self.tie_key,promote)
        if self.membership_mode=='within_block':
            mask,stats=top_sets(self.pdf,promoted);assert stats['boundary_tie_days']==0
            local=mask&valid;la=daily_ranks(self.slow_finished,local,self.dates);lb=daily_ranks(signal,local,self.dates)
            reranker[local]=power_consensus(la[local],lb[local],weight,self.membership_power)
        else:assert self.membership_mode=='global'
        reranker=stock_memory(reranker,self.dates,self.codes,self.n_codes,self.membership_memory)
        reranker=np.where(reranker>-9,reranker+1e-9*self.tie_key,reranker)
        return lift(promoted,reranker,self.pdf)[0]


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round12 import selected
    selected()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round13.py',ROOT/'analysis/verify_methods_round13.py',
             ROOT/'后续选模标准.md',ROOT/'evaluate.py',ROOT/'active_release.json',PREVIOUS/'selection.json',
             PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',PREVIOUS/'component_audit.json',
             PREVIOUS/'independent_membership_causal_checks.json',ROOT/'candidates/optimization_20261003_r12/verification.json',
             ROOT/'analysis/optimize_training_round12.py',ROOT/'analysis/finalize_training_round12.py',
             ROOT/'analysis/optimize_training_round11.py',ROOT/'analysis/retention_priority_round10.py',
             HERE/'optimize_wave15.py',HERE/'optimize_wave18.py']
    sources += [RANKERS/f'{name}.npy' for name in previous.MEMBERSHIP_NAMES]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'baseline_score':EXPECTED,
         'starting_configuration':baseline(),'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'wave81':{'independent_power_consensus':POWERS,'fine_offsets':(-.25,0.,.25)},
         'wave82':{'independent_causal_memory':MEMORIES,'fine_offsets':(-.05,0.,.05),'fine_clip':(0.,.98)},
         'wave83':{'method_winner_on_off_combinations':4,'power_offsets':(-.125,0.,.125),
                   'memory_offsets':(-.025,0.,.025),'fusions':FUSIONS},
         'wave84':{'membership_slow':(.20,.24,.28),'top_slow':(.22,.24,.26),'rest_slow':(.23,.25,.27),
                   'limit_shifts':(.055,.075,.095)},
         'expected_scored_records':52,'causal_memory':'Only previously seen predictions of the same stock; missing ranks skip updates; cold start at first usable rank.',
         'independent_methods':'Each of wave81 and wave82 starts from R12; later grids follow highest official score.',
         'selection_rule':'highest official connected composite; exact ties prefer zero memory and arithmetic fusion',
         'new_model_training':False,'pruned_member_excluded':True,'test_labels_read':False,
         'test_future_prices_used_to_select':False,'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round13 nonlinear consensus and causal memory protocol frozen')


def prefix_controls(ctx,promote,cfg,counts=(80,260,975)):
    import numpy as np
    import polars as pl
    ctx.configure(cfg);pred,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    poisoned=copy(ctx);poisoned.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    poisoned.label_free=ctx.label_free.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    replay,_=poisoned.predict(poisoned.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    assert np.array_equal(pred,replay)
    proofs=[];dates=np.unique(ctx.dates)
    for count in counts:
        last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={k:v[:n] for k,v in ctx.ranks.items()}
        replay,_=prefix.predict(prefix.donor(promote[:n]),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        assert np.array_equal(pred[:n],replay),(cfg['membership_power'],cfg['membership_memory'],last)
        proofs.append({'days':count,'through_date':last,'bit_identical':True})
    return {'membership_power':cfg['membership_power'],'membership_memory':cfg['membership_memory'],
            'membership_mode':cfg['membership_mode'],'label_poisoning_bit_identical':True,'future_append_prefix_invariance':proofs}


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();cfg=baseline();promote=ctx.finished('baseline',cfg['recipe'])
    pred,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    controls=[prefix_controls(ctx,promote,dict(cfg,membership_power=p,membership_memory=rho),counts=(80,260))
              for p,rho in ((0.,.6),(-2.,.4))]
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_output_bit_identical':True,
         'active_method_prefix_and_poisoning_controls':controls,'test_data_read':False,'new_model_training':False},immutable=True)
    log('Round13 bit-identical baseline, nonlinear and causal-memory controls passed')


def evaluate(ctx,cfg):
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline',cfg['recipe'])),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    metrics=ctx.score(pred)
    log(f'Round13 power={cfg["membership_power"]:g} memory={cfg["membership_memory"]:g} fusion={cfg["membership_w5a_weight"]:g} top/rest={cfg["top_slow_weight"]:g}/{cfg["slow16_weight"]:g}: {metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline','ensemble_weights':weights_from_name(cfg['ensemble_name']),
            'top_ensemble_weights':weights_from_name(cfg['top_ensemble_name']),
            'membership_ensemble_weights':weights_from_name(cfg['membership_ensemble_name']),
            'role_ensembles_split':cfg['top_ensemble_name']!=cfg['ensemble_name'],'fold_local_pruning_repaired':True,
            'pruned_member_excluded':True,'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def execute(wave,arms,ctx=None,finish=True):
    ctx=ctx or Context();path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    for key,cfg in arms:
        if key not in payload['results']:
            row=evaluate(ctx,cfg);payload['results'][key]=row;dump(path,payload)
            if signature(cfg)==signature(baseline()):assert abs(row['connected_final_score']-EXPECTED)<1e-12
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def prior_best(waves):return best([r for w in waves for r in read(OUT/f'wave{w}_results.json')['results'].values()])


def nonlinear():
    verify();build();ctx=Context();base=baseline()
    payload=execute(81,[(f'power{p:g}',dict(base,membership_power=p)) for p in POWERS],ctx,False)
    winner=best(payload['results'].values());base=configuration(winner)
    powers=[winner['membership_power']+d for d in (-.25,0.,.25)]
    dump(OUT/'nonlinear_fine_protocol.json',{'coarse_winner':winner,'powers':powers},immutable=True)
    execute(81,[(f'fine{i}_power{p:g}',dict(base,membership_power=p)) for i,p in enumerate(powers)],ctx)


def memory():
    verify();ctx=Context();base=baseline()
    payload=execute(82,[(f'memory{rho:g}',dict(base,membership_memory=rho)) for rho in MEMORIES],ctx,False)
    winner=best(payload['results'].values());base=configuration(winner)
    memories=[min(.98,max(0.,winner['membership_memory']+d)) for d in (-.05,0.,.05)]
    dump(OUT/'memory_fine_protocol.json',{'coarse_winner':winner,'memories':memories},immutable=True)
    execute(82,[(f'fine{i}_memory{rho:g}',dict(base,membership_memory=rho)) for i,rho in enumerate(memories)],ctx)


def combinations():
    verify();base=baseline();p=prior_best((81,));m=prior_best((82,));ctx=Context()
    dump(OUT/'combination_protocol.json',{'nonlinear_method_winner':p,'memory_method_winner':m},immutable=True)
    arms=[(f'power_on{a}_memory_on{b}',dict(base,membership_power=p['membership_power'] if a else 1.,
           membership_memory=m['membership_memory'] if b else 0.)) for a,b in itertools.product((0,1),repeat=2)]
    payload=execute(83,arms,ctx,False);winner=best([p,m]+list(payload['results'].values()));base=configuration(winner)
    for label,key,values in (('power','membership_power',[winner['membership_power']+d for d in (-.125,0.,.125)]),
            ('memory','membership_memory',[min(.98,max(0.,winner['membership_memory']+d)) for d in (-.025,0.,.025)]),
            ('fusion','membership_w5a_weight',FUSIONS)):
        payload=execute(83,[(f'{label}{i}_{v:g}',dict(base,**{key:v})) for i,v in enumerate(values)],ctx,False)
        winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(83,[],ctx)


def refinement():
    verify();winner=prior_best((81,82,83));base=configuration(winner);ctx=Context()
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    payload=execute(84,[(f'membership_slow{v:g}',dict(base,membership_slow_weight=v)) for v in (.20,.24,.28)],ctx,False)
    winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    payload=execute(84,[(f'top{t:g}_rest{r:g}',dict(base,top_slow_weight=t,slow16_weight=r))
                       for t,r in itertools.product((.22,.24,.26),(.23,.25,.27))],ctx,False)
    winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(84,[(f'shift{v:g}',dict(base,limit_up_delta=v)) for v in (.055,.075,.095)],ctx)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','nonlinear','memory','combinations','refinement','all'));stage=parser.parse_args().stage
    for name in (('freeze','build','nonlinear','memory','combinations','refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
