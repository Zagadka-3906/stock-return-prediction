"""Waves77–80: decouple membership ranker, refine fusion and TopK finishing."""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round11 as previous
from optimize_training_round11 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,read,dump,sha,log,weights_from_name
from optimize_training_round6 import source_raw,source_model
OUT=ROOT/'analysis/optimization_20261003_r12'
PREVIOUS=ROOT/'analysis/optimization_20261003_r11'
RANKERS=PREVIOUS/'rankers'
EXPECTED=.449041870533273
WAVES=(77,78,79,80)
FIELDS=previous.FIELDS+('membership_ensemble_name','membership_slow_weight','recipe')
COARSE_WEIGHTS=(.75,.55,.60,.65,.70,.80,.85,.90,1.)
FINE_OFFSETS=(-.025,0.,.025)
MEMBERSHIP_NAMES=tuple(previous.ENSEMBLES)
MEMBERSHIP_SLOW=(0.,.125,.24,.375,.5)
EARLY90=(.15,.20,.25,.30,.35)
ALPHAS=(.875,.90,.925,.95)
AUXILIARY=(.20,.25,.30)
BONUSES=(.20,.30,.40)
TOP_SLOW=(.18,.24,.30)
REST_SLOW=(.15,.20,.25)
OUTPUT_FUSION_OFFSETS=(-.0125,0.,.0125)
RETENTIONS=(.9835,.984,.9845,.985,.9855)
SHIFTS=(.055,.075,.095,.115,.135)


def baseline():
    prior=read(PREVIOUS/'selection.json')['winner']
    return {**{k:deepcopy(prior[k]) for k in previous.FIELDS+('recipe',)},
            'membership_signal':'independent','membership_ensemble_name':prior['top_ensemble_name'],
            'membership_slow_weight':prior['top_slow_weight']}


def configuration(row):return {k:deepcopy(row[k]) for k in FIELDS}


def signature(row):return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))


def best(rows):
    def order(r):
        names={r[k] for k in ('top_ensemble_name','ensemble_name','membership_ensemble_name')}
        members=set().union(*(set(weights_from_name(n)) for n in names))
        return (-r['connected_final_score'],len(members),len(names),r['add_priority_weight']+r['drop_priority_weight'],signature(r))
    return min(rows,key=order)


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


class Context(previous.Context):
    def __init__(self):
        super().__init__()
        self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())

    def configure(self,cfg):
        import numpy as np
        from optimize_wave15 import daily_ranks
        super().configure(cfg)
        name=cfg.get('membership_ensemble_name',cfg['top_ensemble_name'])
        if name not in self._role_cache:
            values=np.load(RANKERS/f'{name}.npy')
            self._role_cache[name]=(values,daily_ranks(values,self.valid,self.dates))
        self.membership_values,self.membership_ranks=self._role_cache[name]
        self.membership_ensemble_name=name;self.membership_slow_weight=cfg.get('membership_slow_weight',cfg['top_slow_weight'])

    def membership_orderer(self):
        import numpy as np
        from optimize_wave15 import weighted_rank_blend
        if self.membership_ensemble_name==self.top_ensemble_name and self.membership_slow_weight==self.top_slow_weight:
            return self.orderers(self.rest_slow_weight)[0]
        n=len(self.dates);w=self.membership_slow_weight
        ranks={'w5a':self.membership_ranks[:n],'slow':self.ranks['slow']}
        blend=weighted_rank_blend([self.membership_values[:n],self.slow],[1-w,w],ranks,self.valid,self.dates,('w5a','slow'))
        return np.where(blend>-9,blend+1e-9*self.tie_key,blend)+1e-9*self.tie_key

    def donor(self,promote,rerank_weight=None):
        import numpy as np
        from optimize_wave15 import daily_ranks
        from optimize_wave18 import lift
        from analysis.topset_hybrid_20261002.fold_validation import top_sets
        weight=self.rerank_weight if rerank_weight is None else rerank_weight
        assert 0<=weight<=1
        if weight==0:return super().donor(promote,0.)
        signal=self.membership_orderer()
        ranks_slow=daily_ranks(self.slow_finished,self.valid,self.dates);ranks_signal=daily_ranks(signal,self.valid,self.dates)
        usable=(ranks_slow>-9)&(ranks_signal>-9);reranker=np.full(len(promote),-10.)
        reranker[usable]=(1-weight)*ranks_slow[usable]+weight*ranks_signal[usable]
        promoted=np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*self.tie_key,promote)
        if self.membership_mode=='within_block':
            mask,stats=top_sets(self.pdf,promoted);assert stats['boundary_tie_days']==0
            local=mask&usable
            local_slow=daily_ranks(self.slow_finished,local,self.dates);local_signal=daily_ranks(signal,local,self.dates)
            reranker[local]=(1-weight)*local_slow[local]+weight*local_signal[local]
        else:assert self.membership_mode=='global'
        reranker=np.where(reranker>-9,reranker+1e-9*self.tie_key,reranker)
        return lift(promoted,reranker,self.pdf)[0]

    def rebuild_recipe(self,recipe,frame=None):
        import numpy as np
        import polars as pl
        from optimize_wave15 import daily_ranks
        from optimize_wave6 import make_prediction_param
        from src.scoring import Panel
        label_free=self.label_free if frame is None else frame
        parts=[]
        for year in YEARS:
            fold=label_free.filter(pl.col('trade_date')//10000==year)
            if not len(fold):continue
            valid=fold['price_valid'].to_numpy();dates=fold['trade_date'].to_numpy();raws=[]
            for component in recipe['components']:
                cached=pl.read_parquet(source_raw(component['seed'],component['rounds'],year))
                cached=cached.filter(pl.col('trade_date')<=int(dates.max()))
                assert cached.select(KEYS).equals(fold.select(KEYS))
                raws.append((component['weight'],cached['pred_raw'].to_numpy()))
            mixed=sum(w*daily_ranks(raw,valid,dates) for w,raw in raws);mixed[~valid]=-10.
            parts.append(make_prediction_param(Panel.from_frame(fold.with_columns(pl.Series('pred_raw',mixed))),
                         fold['aux_raw'].to_numpy(),**recipe['postprocessing']))
        return np.concatenate(parts)

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline';recipe=recipe or baseline()['recipe']
        key=hashlib.sha256(json.dumps(recipe,sort_keys=True).encode()).hexdigest()[:20]
        path=OUT/f'promote/{key}.npy'
        if path.exists():return np.load(path)
        pred=self.rebuild_recipe(recipe);path.parent.mkdir(exist_ok=True);np.save(path,pred);return np.load(path)


def freeze():
    from finalize_training_round11 import selected
    selected()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round12.py',ROOT/'后续选模标准.md',ROOT/'evaluate.py',
             ROOT/'active_release.json',ROOT/'analysis/optimize_training_round11.py',ROOT/'analysis/finalize_training_round11.py',
             ROOT/'analysis/optimize_training_round8.py',ROOT/'analysis/optimize_training_round7.py',
             ROOT/'analysis/finalize_training_round7.py',ROOT/'analysis/finalize_optimization.py',
             ROOT/'analysis/retention_priority_round10.py',HERE/'optimize_wave6.py',HERE/'optimize_wave15.py',
             HERE/'optimize_wave18.py',HERE/'combined_fold_frame.parquet',PREVIOUS/'selection.json',
             PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',PREVIOUS/'component_audit.json',
             ROOT/'candidates/optimization_20261003_r11/verification.json']
    sources += [RANKERS/f'{name}.npy' for name in MEMBERSHIP_NAMES]
    for year in YEARS:
        sources += [PREVIOUS/f'raw/source_topk_{year}.json',source_model(2026,year)]
        for rounds in (90,180):sources += [source_raw(2026,rounds,year),source_raw(2026,rounds,year).with_suffix('.json')]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'baseline_score':EXPECTED,
         'starting_configuration':baseline(),'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'wave77':{'fusion_weights':COARSE_WEIGHTS,'fine_offsets':FINE_OFFSETS,'fine_clipped_to_unit_interval':True},
         'wave78':{'independent_membership_ensembles':MEMBERSHIP_NAMES,'membership_slow_weights':MEMBERSHIP_SLOW},
         'wave79':{'early90_weights':EARLY90,'alphas':ALPHAS,'auxiliary_weights':AUXILIARY,'bonuses':BONUSES},
         'wave80':{'top_slow_weights':TOP_SLOW,'rest_slow_weights':REST_SLOW,'fusion_offsets':OUTPUT_FUSION_OFFSETS,
                   'retentions':RETENTIONS,'limit_up_shifts':SHIFTS},
         'adaptive_rule':'Freeze each next-axis grid around the highest official score observed before that axis.',
         'membership_decoupled_from_return_ordering':True,'expected_scored_records':70,
         'selection_rule':'highest official connected composite; exact ties prefer fewer model families and role ensembles',
         'new_model_training':False,'pruned_member_excluded':True,'all_validation_years_previously_viewed':True,
         'selection_bias_uncorrected':True,'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round12 independent-membership protocol frozen')


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();cfg=baseline();promote=ctx.finished('baseline',cfg['recipe'])
    assert np.array_equal(promote,np.load(PREVIOUS/'promote_baseline.npy'))
    pred,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    for year in YEARS:dump(OUT/f'raw/source_topk_{year}.json',read(PREVIOUS/f'raw/source_topk_{year}.json'),immutable=True)
    dump(OUT/'component_audit.json',{'status':'passed','baseline_promote_rebuilt_bit_identical':True,
         'baseline_independent_membership_complete_output_bit_identical':True,
         'source_rankers':{name:sha(RANKERS/f'{name}.npy') for name in MEMBERSHIP_NAMES},
         'test_data_read':False,'new_model_training':False,'pruned_member_excluded':True},immutable=True)
    log('Round12 TopK rebuild and independent-membership baseline controls passed')


def evaluate(ctx,cfg):
    ctx.configure(cfg);promote=ctx.finished('baseline',cfg['recipe'])
    pred,stats=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);metrics=ctx.score(pred)
    log(f'Round12 {signature(cfg)}: {metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline','ensemble_weights':weights_from_name(cfg['ensemble_name']),
            'top_ensemble_weights':weights_from_name(cfg['top_ensemble_name']),
            'membership_ensemble_weights':weights_from_name(cfg['membership_ensemble_name']),
            'role_ensembles_split':cfg['top_ensemble_name']!=cfg['ensemble_name'],
            'fold_local_pruning_repaired':True,'pruned_member_excluded':True,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def execute(wave,arms,ctx=None,finish=True):
    ctx=ctx or Context();path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    for key,cfg in arms:
        if key not in payload['results']:
            payload['results'][key]=evaluate(ctx,cfg);dump(path,payload)
            if signature(cfg)==signature(baseline()):assert abs(payload['results'][key]['connected_final_score']-EXPECTED)<1e-12
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def prior_best(waves):
    rows=[]
    for wave in waves:
        payload=read(OUT/f'wave{wave}_results.json');assert payload['status']=='complete';rows+=list(payload['results'].values())
    return best(rows)


def fusion():
    verify();build();ctx=Context();base=baseline()
    payload=execute(77,[(f'fusion{w:g}',dict(base,membership_w5a_weight=w)) for w in COARSE_WEIGHTS],ctx,finish=False)
    winner=best(payload['results'].values());base=configuration(winner)
    weights=[min(1.,max(0.,winner['membership_w5a_weight']+offset)) for offset in FINE_OFFSETS]
    dump(OUT/'fusion_fine_protocol.json',{'coarse_winner':winner,'fine_weights':weights},immutable=True)
    execute(77,[(f'fine{i}_fusion{w:g}',dict(base,membership_w5a_weight=w)) for i,w in enumerate(weights)],ctx)


def membership_ranker():
    verify();winner=prior_best((77,));base=configuration(winner)
    dump(OUT/'membership_ranker_protocol.json',{'winner_before_ranker':winner,'ensembles':MEMBERSHIP_NAMES,
         'membership_slow_weights':MEMBERSHIP_SLOW},immutable=True)
    ctx=Context();payload=execute(78,[(name,dict(base,membership_ensemble_name=name)) for name in MEMBERSHIP_NAMES],ctx,finish=False)
    winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(78,[(f'membership_slow{w:g}',dict(base,membership_slow_weight=w)) for w in MEMBERSHIP_SLOW],ctx)


def donor_recipe():
    verify();winner=prior_best((77,78));base=configuration(winner)
    dump(OUT/'donor_recipe_protocol.json',{'winner_before_recipe':winner,'early90':EARLY90,'alphas':ALPHAS,
         'auxiliary_weights':AUXILIARY,'bonuses':BONUSES},immutable=True)
    ctx=Context()
    for axis,values in (('early90',EARLY90),('alpha',ALPHAS),('weight',AUXILIARY),('bonus',BONUSES)):
        arms=[]
        for value in values:
            cfg=deepcopy(base)
            if axis=='early90':cfg['recipe']['components'][0]['weight']=value;cfg['recipe']['components'][1]['weight']=1-value
            else:cfg['recipe']['postprocessing'][axis]=value
            arms.append((f'{axis}{value:g}',cfg))
        payload=execute(79,arms,ctx,finish=False)
        winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(79,[],ctx)


def refinement():
    import itertools
    verify();winner=prior_best((77,78,79));base=configuration(winner)
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner,'top_slow':TOP_SLOW,'rest_slow':REST_SLOW,
         'fusion_offsets':OUTPUT_FUSION_OFFSETS,'retentions':RETENTIONS,'shifts':SHIFTS},immutable=True)
    ctx=Context()
    payload=execute(80,[(f'top{t:g}_rest{r:g}',dict(base,top_slow_weight=t,slow16_weight=r))
                       for t,r in itertools.product(TOP_SLOW,REST_SLOW)],ctx,finish=False)
    winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    weights=[min(1.,max(0.,winner['membership_w5a_weight']+offset)) for offset in OUTPUT_FUSION_OFFSETS]
    for label,key,values in (('fusion','membership_w5a_weight',weights),('retention','retention',RETENTIONS),('shift','limit_up_delta',SHIFTS)):
        payload=execute(80,[(f'{label}{i}_{v:g}',dict(base,**{key:v})) for i,v in enumerate(values)],ctx,finish=False)
        winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(80,[],ctx)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','fusion','membership_ranker','donor_recipe','refinement','all'))
    stage=parser.parse_args().stage
    for name in (('freeze','build','fusion','membership_ranker','donor_recipe','refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
