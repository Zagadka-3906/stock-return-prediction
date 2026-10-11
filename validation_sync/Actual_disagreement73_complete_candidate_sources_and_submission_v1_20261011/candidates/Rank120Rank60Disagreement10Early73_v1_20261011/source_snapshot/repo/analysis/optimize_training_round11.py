"""Waves71–76: four independent optimization methods, combinations and refinement."""
from __future__ import annotations
import argparse
from copy import deepcopy
import itertools
import json
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round10 as previous
from optimize_training_round10 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,read,dump,sha,log
from optimize_training_round8 import weights_name,weights_from_name
from optimize_training_round7 import member_paths
OUT=ROOT/'analysis/optimization_20261003_r11'
PREVIOUS=ROOT/'analysis/optimization_20261003_r10'
RANKERS=OUT/'rankers'
OLD_RANKERS=ROOT/'analysis/optimization_20261003_r8/rankers'
EXPECTED=.44882887216021156
WAVES=(71,72,73,74,75,76)
MEMBERS=('lgb','xgb','two','gru')
TOP_BASE={'lgb':1.,'xgb':1.,'gru':1.}
REST_BASE={'lgb':1.,'xgb':1.,'two':1.,'gru':2.25}
TOP_NAMES=[];REST_NAMES=[];ENSEMBLES={}
for base,names in ((TOP_BASE,TOP_NAMES),(REST_BASE,REST_NAMES)):
    ENSEMBLES[weights_name(base)]=base
    for member in base:
        for delta in (-.25,.25):
            weights=dict(base);weights[member]+=delta
            name=weights_name(weights);ENSEMBLES[name]=weights;names.append(name)
TOP_SLOW=(.18,.24,.30)
REST_SLOW=(.15,.20,.25)
PRIORITY_SIGNALS=('rest','slow','slow_finished')
PRIORITY_WEIGHTS=(.05,.5)
MEMBERSHIP_SIGNALS=('top','rest')
MEMBERSHIP_MODES=('global','within_block')
MEMBERSHIP_WEIGHTS=(.05,.25,.75)
RETENTIONS=(.9835,.984,.9845,.985,.9855)
SHIFTS=(.055,.075,.095,.115,.135)
FIELDS=('top_ensemble_name','ensemble_name','top_slow_weight','slow16_weight','priority_signal',
        'add_priority_weight','drop_priority_weight','membership_signal','membership_mode',
        'membership_w5a_weight','retention','limit_up_delta')
METHOD_FIELDS=(FIELDS[:2],FIELDS[2:4],FIELDS[4:7],FIELDS[7:10])


def baseline():
    prior=read(PREVIOUS/'selection.json')['winner']
    return {**{k:prior[k] for k in FIELDS if k in prior},'priority_signal':'top','membership_signal':'top'}


def signature(cfg):return tuple(cfg[k] for k in FIELDS)


def best(rows):
    return min(rows,key=lambda r:(-r['connected_final_score'],r['add_priority_weight']+r['drop_priority_weight']+
               r['membership_w5a_weight'],len(set(r['ensemble_weights'])|set(r['top_ensemble_weights'])),signature(r)))


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round10 import selected
    selected()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round11.py',ROOT/'后续选模标准.md',
             ROOT/'evaluate.py',ROOT/'active_release.json',ROOT/'analysis/optimize_training_round10.py',
             ROOT/'analysis/finalize_training_round10.py',ROOT/'analysis/retention_priority_round10.py',
             ROOT/'analysis/optimize_training_round9.py',ROOT/'analysis/optimize_training_round8.py',
             ROOT/'analysis/optimize_training_round7.py',ROOT/'analysis/finalize_training_round7.py',
             ROOT/'analysis/finalize_optimization.py',ROOT/'experiments/final_sweep_wave3.py',
             HERE/'optimize_wave6.py',HERE/'optimize_wave13.py',HERE/'optimize_wave15.py',HERE/'optimize_wave18.py',
             HERE/'combined_fold_frame.parquet',HERE/'connected_pred_peer67_slow16.npy',
             HERE/'pp_a0_b0_top_only_w0.25_rl1_tcw1.npy',PREVIOUS/'selection.json',
             PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
             ROOT/'candidates/optimization_20261003_r10/verification.json']
    for year in YEARS:
        sources += [member_paths(year)[m] for m in MEMBERS]+[PREVIOUS/f'raw/source_topk_{year}.json']
    sources += [OLD_RANKERS/f'{weights_name(w)}.npy' for w in (TOP_BASE,REST_BASE)]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':EXPECTED,'starting_configuration':baseline(),
         'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'methods':{'wave71_role_weights':{'ensembles':ENSEMBLES,'top_names':TOP_NAMES,'rest_names':REST_NAMES,
                                         'joint':'Combine independent Top/rest winners if distinct from an already scored configuration.'},
                    'wave72_ordering':{'top_slow':TOP_SLOW,'rest_slow':REST_SLOW},
                    'wave73_retention_priorities':{'signals':PRIORITY_SIGNALS,'weights':PRIORITY_WEIGHTS,
                                                  'modes':['add_only','drop_only','both']},
                    'wave74_membership_fusion':{'signals':MEMBERSHIP_SIGNALS,'modes':MEMBERSHIP_MODES,
                                               'weights':MEMBERSHIP_WEIGHTS}},
         'independent_comparison':'Each method starts from the same R10 winner. Baselines are rerun as controls.',
         'wave75_combinations':'Unique Cartesian on/off combinations of the four independent method winners; baseline included.',
         'wave76_refinement':{'retentions':RETENTIONS,'shifts':SHIFTS},
         'selection_rule':'highest official connected composite; exact ties prefer simpler priorities and membership fusion',
         'new_model_training':False,'pruned_member_excluded':True,'all_validation_years_previously_viewed':True,
         'selection_bias_uncorrected':True,'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round11 four-method search protocol frozen')


class Context(previous.Context):
    def __init__(self):
        super().__init__()
        self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())

    def roles(self,top,rest):
        import numpy as np
        from optimize_wave15 import daily_ranks
        for name in dict.fromkeys((top,rest)):
            if name not in self._role_cache:
                path=RANKERS/f'{name}.npy'
                if not path.exists():path=OLD_RANKERS/f'{name}.npy'
                values=np.load(path)
                self._role_cache[name]=(values,daily_ranks(values,self.valid,self.dates))
        self.ensemble_name=self.rest_ensemble_name=rest;self.top_ensemble_name=top
        self.w5a,rank_rest=self._role_cache[rest];self.top_values,self.top_ranks=self._role_cache[top]
        self.ranks={'w5a':rank_rest,'slow':self.ranks['slow']}

    def configure(self,cfg):
        self.roles(cfg['top_ensemble_name'],cfg['ensemble_name'])
        self.top_slow_weight=cfg['top_slow_weight'];self.rest_slow_weight=cfg['slow16_weight']
        self.add_priority_weight=cfg['add_priority_weight'];self.drop_priority_weight=cfg['drop_priority_weight']
        self.priority_signal=cfg['priority_signal'];self.membership_signal=cfg['membership_signal']
        self.membership_mode=cfg['membership_mode'];self.rerank_weight=cfg['membership_w5a_weight']

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline'
        if recipe is not None:assert recipe==read(PREVIOUS/'selection.json')['winner']['recipe']
        return np.load(PREVIOUS/'promote_baseline.npy')

    def orderers(self,weight):
        import numpy as np
        from optimize_wave15 import weighted_rank_blend
        n=len(self.dates)
        def ordering(values,ranks,w):
            blend=weighted_rank_blend([values,self.slow],[1-w,w],ranks,self.valid,self.dates,('w5a','slow'))
            return np.where(blend>-9,blend+1e-9*self.tie_key,blend)+1e-9*self.tie_key
        a=ordering(self.top_values[:n],{'w5a':self.top_ranks[:n],'slow':self.ranks['slow']},self.top_slow_weight)
        return a,ordering(self.w5a,self.ranks,weight)

    def donor(self,promote,rerank_weight=None):
        import numpy as np
        from optimize_wave15 import daily_ranks
        from optimize_wave18 import lift
        from analysis.topset_hybrid_20261002.fold_validation import top_sets
        weight=self.rerank_weight if rerank_weight is None else rerank_weight
        assert 0<=weight<=1
        if weight==0:return super().donor(promote,0.)
        a,b=self.orderers(self.rest_slow_weight);signal=a if self.membership_signal=='top' else b
        ranks_slow=daily_ranks(self.slow_finished,self.valid,self.dates)
        ranks_signal=daily_ranks(signal,self.valid,self.dates)
        usable=(ranks_slow>-9)&(ranks_signal>-9)
        reranker=np.full(len(promote),-10.)
        reranker[usable]=(1-weight)*ranks_slow[usable]+weight*ranks_signal[usable]
        promoted=np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*self.tie_key,promote)
        if self.membership_mode=='within_block':
            mask,stats=top_sets(self.pdf,promoted);assert stats['boundary_tie_days']==0
            local=mask&usable
            local_slow=daily_ranks(self.slow_finished,local,self.dates)
            local_signal=daily_ranks(signal,local,self.dates)
            reranker[local]=(1-weight)*local_slow[local]+weight*local_signal[local]
        else:assert self.membership_mode=='global'
        reranker=np.where(reranker>-9,reranker+1e-9*self.tie_key,reranker)
        return lift(promoted,reranker,self.pdf)[0]

    def predict(self,donor,weight,retention,delta=0.):
        import numpy as np
        import pandas as pd
        from retention_priority_round10 import build_priority
        a,b=self.orderers(weight)
        if self.add_priority_weight or self.drop_priority_weight:
            signal={'top':a,'rest':b,'slow':self.slow,'slow_finished':self.slow_finished}[self.priority_signal]
            donor_rank=pd.Series(donor).groupby(self.dates).rank(method='average',pct=True).to_numpy()
            signal_rank=pd.Series(signal).groupby(self.dates).rank(method='average',pct=True).to_numpy()
            def priority(w):return donor if w==0 else (1-w)*donor_rank+w*signal_rank
            adds=priority(self.add_priority_weight);drops=priority(self.drop_priority_weight)
        else:adds=drops=donor
        pred,stats=build_priority(donor,a,b,self.dates,self.flags,self.codes,self.n_codes,retention,adds,drops)
        pred[self.flags==1]+=delta
        return pred,stats


def build():
    import numpy as np
    import polars as pl
    from experiments.final_sweep_wave3 import ensemble_raw
    from optimize_wave6 import make_prediction_param
    from src.scoring import Panel
    verify()
    if (OUT/'component_audit.json').exists():
        for path,digest in read(OUT/'component_audit.json')['output_sha256'].items():assert sha(path)==digest,path
        return
    ctx=Context();RANKERS.mkdir(exist_ok=True)
    pending={name:[] for name in ENSEMBLES if not (RANKERS/f'{name}.npy').exists()}
    for year in YEARS:
        frame=ctx.label_free.filter(pl.col('trade_date')//10000==year);panel=Panel.from_frame(frame);arrays={}
        for member in MEMBERS:
            raw=pl.read_parquet(member_paths(year)[member]).sort('trade_date','ts_code')
            assert raw.select(KEYS).with_columns(pl.col('trade_date').cast(pl.Int32)).equals(frame.select(KEYS))
            column='gru_raw' if member=='gru' and year<2022 else 'pred_raw'
            arrays[member]=raw[column].to_numpy().astype(np.float64)
        for name in pending:
            weights=ENSEMBLES[name];assert 'pruned' not in weights and all(w>0 for w in weights.values())
            mixed=ensemble_raw(panel,weights,arrays)
            pending[name].append(make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',mixed))),
                                 frame['aux_raw'].to_numpy(),**dict(BASE_POST,alpha=0,bonus=0)))
        dump(OUT/f'raw/source_topk_{year}.json',read(PREVIOUS/f'raw/source_topk_{year}.json'),immutable=True)
        log(f'Round11 {year}: {len(pending)} role-weight rankers rebuilt from frozen OOF members')
    for name,parts in pending.items():np.save(RANKERS/f'{name}.npy',np.concatenate(parts))
    for weights in (TOP_BASE,REST_BASE):
        name=weights_name(weights);assert np.array_equal(np.load(RANKERS/f'{name}.npy'),np.load(OLD_RANKERS/f'{name}.npy'))
    # Clear the bootstrap fallback cache so controls consume newly reconstructed rankers.
    ctx._role_cache={};ctx.configure(baseline())
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),.20,.984,.075)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    dump(OUT/'component_audit.json',{'status':'passed','baseline_role_rankers_bit_identical':True,
         'baseline_complete_prediction_bit_identical':True,'new_model_training':False,'test_data_read':False,
         'pruned_member_excluded':True,'output_sha256':{str(p):sha(p) for p in sorted(RANKERS.glob('*.npy'))}},immutable=True)
    log('Round11 rebuilt role-ranker and complete-output controls passed')


def evaluate(ctx,cfg):
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    metrics=ctx.score(pred)
    log(f'Round11 {json.dumps(cfg,ensure_ascii=False,separators=(",",":"))}: {metrics["final_score"]:.9f}')
    return {**cfg,'donor':'baseline','recipe':read(PREVIOUS/'selection.json')['winner']['recipe'],
            'ensemble_weights':weights_from_name(cfg['ensemble_name']),
            'top_ensemble_weights':weights_from_name(cfg['top_ensemble_name']),
            'role_ensembles_split':cfg['top_ensemble_name']!=cfg['ensemble_name'],
            'fold_local_pruning_repaired':True,'pruned_member_excluded':True,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def execute(wave,arms,ctx=None,finish=True):
    ctx=ctx or Context();path=OUT/f'wave{wave}_results.json'
    payload=read(path) if path.exists() else {'status':'running','results':{}}
    for key,cfg in arms:
        if key not in payload['results']:
            payload['results'][key]=evaluate(ctx,cfg);dump(path,payload)
            if signature(cfg)==signature(baseline()):assert abs(payload['results'][key]['connected_final_score']-EXPECTED)<1e-12
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def role_weights():
    verify();build();base=baseline();arms=[('baseline',base)]
    for key,names in (('top_ensemble_name',TOP_NAMES),('ensemble_name',REST_NAMES)):
        for name in names:arms.append((f'{key}_{name}',dict(base,**{key:name})))
    ctx=Context();payload=execute(71,arms,ctx,finish=False)
    top=best(v for v in payload['results'].values() if v['ensemble_name']==base['ensemble_name'])
    rest=best(v for v in payload['results'].values() if v['top_ensemble_name']==base['top_ensemble_name'])
    joint=dict(base,top_ensemble_name=top['top_ensemble_name'],ensemble_name=rest['ensemble_name'])
    dump(OUT/'role_joint_protocol.json',{'independent_top':top,'independent_rest':rest,'joint':joint},immutable=True)
    extra=[] if signature(joint) in {signature(v) for v in payload['results'].values()} else [('joint_role_winners',joint)]
    execute(71,extra,ctx)


def ordering():
    verify();base=baseline()
    arms=[(f'top{t:g}_rest{r:g}',dict(base,top_slow_weight=t,slow16_weight=r)) for t,r in itertools.product(TOP_SLOW,REST_SLOW)]
    execute(72,arms)


def priorities():
    verify();base=baseline();arms=[('baseline',base)]
    for signal,w in itertools.product(PRIORITY_SIGNALS,PRIORITY_WEIGHTS):
        for mode,a,d in (('add',w,0.),('drop',0.,w),('both',w,w)):
            arms.append((f'{signal}_{mode}{w:g}',dict(base,priority_signal=signal,add_priority_weight=a,drop_priority_weight=d)))
    execute(73,arms)


def membership():
    verify();base=baseline();arms=[('baseline',base)]
    for signal,mode,w in itertools.product(MEMBERSHIP_SIGNALS,MEMBERSHIP_MODES,MEMBERSHIP_WEIGHTS):
        arms.append((f'{signal}_{mode}_weight{w:g}',dict(base,membership_signal=signal,membership_mode=mode,membership_w5a_weight=w)))
    execute(74,arms)


def combinations():
    verify();winners=[]
    for wave in (71,72,73,74):
        payload=read(OUT/f'wave{wave}_results.json');assert payload['status']=='complete';winners.append(best(payload['results'].values()))
    arms=[];seen=set()
    for switches in itertools.product((0,1),repeat=4):
        cfg=baseline()
        for enabled,fields,winner in zip(switches,METHOD_FIELDS,winners):
            if enabled:cfg.update({key:winner[key] for key in fields})
        if signature(cfg) not in seen:seen.add(signature(cfg));arms.append(('methods'+''.join(map(str,switches)),cfg))
    dump(OUT/'combination_protocol.json',{'method_winners':winners,'unique_arms':arms,'deduplication':'exact configuration'},immutable=True)
    execute(75,arms)


def refinement():
    verify();rows=[]
    for wave in (71,72,73,74,75):
        payload=read(OUT/f'wave{wave}_results.json');assert payload['status']=='complete';rows+=list(payload['results'].values())
    winner=best(rows);base={key:winner[key] for key in FIELDS}
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner,'retentions':RETENTIONS,'shifts':SHIFTS},immutable=True)
    ctx=Context();payload=execute(76,[(f'retention{r:g}',dict(base,retention=r)) for r in RETENTIONS],ctx,finish=False)
    winner=best(rows+list(payload['results'].values()));base={key:winner[key] for key in FIELDS}
    execute(76,[(f'limit_shift{s:g}',dict(base,limit_up_delta=s)) for s in SHIFTS],ctx)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','role_weights','ordering','priorities','membership','combinations','refinement','all'))
    stage=parser.parse_args().stage
    for name in (('freeze','build','role_weights','ordering','priorities','membership','combinations','refinement') if stage=='all' else (stage,)):
        globals()[name]()


if __name__=='__main__':main()
