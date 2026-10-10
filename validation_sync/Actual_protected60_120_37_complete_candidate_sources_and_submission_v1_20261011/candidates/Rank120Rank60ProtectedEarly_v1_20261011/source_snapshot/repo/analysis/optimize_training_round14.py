"""Waves85–88: audited neural/ExtraTrees augmentation of three separate roles."""
from __future__ import annotations
import argparse
from copy import deepcopy
import itertools
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round13 as previous
import train_diverse_backbones_20261003 as trainer
from optimize_training_round13 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r14'
PREVIOUS=ROOT/'analysis/optimization_20261003_r13'
WAVES=(85,86,87,88)
FIELDS=previous.FIELDS+('diverse_augmentation',)
ROLES=('membership','top','rest')
MODELS=tuple(trainer.CONFIGS)
WEIGHTS=(.05,.15,.30,.50)


def baseline():
    old=read(PREVIOUS/'selection.json')['winner']
    return {**previous.configuration(old),'diverse_augmentation':{role:{'model':'none','weight':0.} for role in ROLES}}


def expected():return read(PREVIOUS/'selection.json')['winner']['connected_final_score']


def configuration(row):return {k:deepcopy(row[k]) for k in FIELDS}


def signature(row):
    import json
    return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))


def best(rows):
    def key(row):
        active=[v for v in row['diverse_augmentation'].values() if v['weight']>0]
        return (-row['connected_final_score'],len({v['model'] for v in active}),len(active),signature(row))
    return min(rows,key=key)


class Context(previous.Context):
    def __init__(self):
        super().__init__();self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())

    def configure(self,cfg):
        super().configure(cfg)
        self.diverse_augmentation=deepcopy(cfg.get('diverse_augmentation',{r:{'model':'none','weight':0.} for r in ROLES}))
        if not hasattr(self,'_diverse_cache'):self._diverse_cache={}

    def augment(self,base,role):
        import numpy as np
        from optimize_wave15 import daily_ranks
        spec=self.diverse_augmentation[role];weight=spec['weight']
        if weight==0:return base
        assert 0<weight<=1 and spec['model'] in MODELS
        name=spec['model']
        if name not in self._diverse_cache:
            values=np.load(OUT/f'rankers/{name}.npy');self._diverse_cache[name]=(values,daily_ranks(values,self.valid,self.dates))
        n=len(self.dates);other=self._diverse_cache[name][1][:n];current=daily_ranks(base,self.valid,self.dates)
        keep=(other>-9)&(current>-9);out=np.full(n,-10.)
        out[keep]=(1-weight)*current[keep]+weight*other[keep]
        return np.where(out>-9,out+1e-9*self.tie_key,out)+1e-9*self.tie_key

    def orderers(self,weight):
        a,b=super().orderers(weight)
        return self.augment(a,'top'),self.augment(b,'rest')

    def membership_orderer(self):return self.augment(super().membership_orderer(),'membership')

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline' and (recipe is None or recipe==baseline()['recipe'])
        return np.load(PREVIOUS/'promote_baseline.npy')


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round13 import selected
    selected();trainer.verify();assert read(trainer.OUT/'oof_audit.json')['status']=='passed'
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round14.py',ROOT/'analysis/verify_methods_round14.py',ROOT/'analysis/run_training_round14_pipeline.py',
             Path(trainer.__file__),trainer.OUT/'protocol.json',trainer.OUT/'oof_audit.json',
             ROOT/'后续选模标准.md',ROOT/'evaluate.py',ROOT/'active_release.json',
             PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
             PREVIOUS/'nonlinear_memory_causal_checks.json',ROOT/'candidates/optimization_20261003_r13/verification.json',
             ROOT/'analysis/optimize_training_round13.py',ROOT/'analysis/finalize_training_round13.py',
             ROOT/'analysis/optimize_training_round12.py',ROOT/'analysis/optimize_training_round11.py',
             ROOT/'analysis/retention_priority_round10.py',HERE/'optimize_wave15.py',HERE/'optimize_wave18.py']
    for name in MODELS:
        for year in YEARS:
            sources.extend(trainer.OUT/name/f'{kind}_{year}.{suffix}' for kind,suffix in (('model','joblib'),('raw','parquet'),('info','json')))
            sources.append(trainer.OUT/f'boundary_control_{name}_{year}.json')
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'baseline_score':expected(),
         'starting_configuration':baseline(),'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'wave85':{'models':MODELS,'roles':ROLES,'weights':WEIGHTS,'baseline_records':1},
         'wave86':{'independent_role_winner_combinations':8},
         'wave87':{'per_role_weight_offsets':(-.10,-.05,0.,.05,.10),'zero_control_each_role':True,'clip':(0.,.8)},
         'wave88':{'memory':(0.,.0125,.025,.0375,.05),'fusion':(.725,.75,.775),
                   'top_slow':(.22,.24,.26),'rest_slow':(.23,.25,.27),'limit_shifts':(.055,.075,.095)},
         'expected_scored_records':83,'new_model_training':True,'new_fold_models_trained':15,
         'training_pipeline':str(trainer.OUT/'protocol.json'),'method':'Three independently augmented membership/Top/rest orderers; combine independent role winners, then refine.',
         'selection_rule':'highest official connected composite; exact ties prefer fewer active new models and augmented roles',
         'test_labels_read':False,'test_future_prices_used_to_select':False,'pruned_member_excluded':True,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round14 new MLP/ExtraTrees role-augmentation protocol frozen')


def build():
    import numpy as np
    import polars as pl
    from src.scoring import Panel
    from optimize_wave6 import make_prediction_param
    verify()
    if (OUT/'component_audit.json').exists():
        for path,digest in read(OUT/'component_audit.json')['output_sha256'].items():assert sha(path)==digest,path
        return
    ctx=Context();folder=OUT/'rankers';folder.mkdir(exist_ok=True);parts={name:[] for name in MODELS}
    for year in YEARS:
        frame=ctx.label_free.filter(pl.col('trade_date')//10000==year)
        for name in MODELS:
            source=trainer.OUT/name/f'raw_{year}.parquet';info=read(trainer.OUT/name/f'info_{year}.json')
            assert sha(source)==info['prediction_sha256'] and info['model_reload_bit_identical']
            meta=info['training_meta'];assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']<year*10000+101
            raw=pl.read_parquet(source);assert raw.select(KEYS).equals(frame.select(KEYS))
            parts[name].append(make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw['pred_raw']))),
                 frame['aux_raw'].to_numpy(),**dict(BASE_POST,alpha=0,bonus=0)))
    for name,arrays in parts.items():np.save(folder/f'{name}.npy',np.concatenate(arrays))
    base=baseline();ctx.configure(base);pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),base['slow16_weight'],base['retention'],base['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    controls=[]
    for role,name in zip(ROLES,MODELS):
        cfg=deepcopy(base);cfg['diverse_augmentation'][role]={'model':name,'weight':.15}
        controls.append(previous.prefix_controls(ctx,ctx.finished('baseline'),cfg,counts=(80,260)))
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_output_bit_identical':True,
         'active_augmentation_prefix_and_poisoning_controls':controls,'models_trained':15,'test_data_read':False,
         'output_sha256':{str(p):sha(p) for p in sorted(folder.glob('*.npy'))}},immutable=True)
    log('Round14 baseline, new role rankers and active-method causal controls passed')


def evaluate(ctx,cfg):
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);metrics=ctx.score(pred)
    log(f'Round14 augmentation={cfg["diverse_augmentation"]}: {metrics["final_score"]:.9f}')
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
            if signature(cfg)==signature(baseline()):assert abs(row['connected_final_score']-expected())<1e-12
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def prior_best(waves):return best([r for w in waves for r in read(OUT/f'wave{w}_results.json')['results'].values()])


def independent():
    verify();build();base=baseline();arms=[('baseline',base)]
    for role,name,weight in itertools.product(ROLES,MODELS,WEIGHTS):
        cfg=deepcopy(base);cfg['diverse_augmentation'][role]={'model':name,'weight':weight}
        arms.append((f'{role}_{name}_w{weight:g}',cfg))
    execute(85,arms)


def combinations():
    verify();base=baseline();rows=read(OUT/'wave85_results.json')['results'];winners={}
    for role in ROLES:
        winners[role]=best(row for row in rows.values() if row['diverse_augmentation'][role]['weight']>0)
    dump(OUT/'combination_protocol.json',{'independent_role_winners':winners},immutable=True)
    arms=[]
    for switches in itertools.product((0,1),repeat=3):
        cfg=deepcopy(base)
        for role,on in zip(ROLES,switches):
            if on:cfg['diverse_augmentation'][role]=deepcopy(winners[role]['diverse_augmentation'][role])
        arms.append(('on_'+''.join(map(str,switches)),cfg))
    execute(86,arms)


def refine_weights():
    verify();winner=prior_best((85,86));base=configuration(winner);ctx=Context()
    role_winners=read(OUT/'combination_protocol.json')['independent_role_winners']
    dump(OUT/'weight_refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    for role in ROLES:
        spec=base['diverse_augmentation'][role];name=spec['model'] if spec['weight']>0 else role_winners[role]['diverse_augmentation'][role]['model']
        values=[0.]+[min(.8,max(0.,spec['weight']+d)) for d in (-.10,-.05,0.,.05,.10)]
        dump(OUT/f'weight_refinement_{role}_protocol.json',{'anchor':base,'model':name,'weights':values},immutable=True)
        arms=[]
        for index,weight in enumerate(values):
            cfg=deepcopy(base);cfg['diverse_augmentation'][role]={'model':name if weight>0 else 'none','weight':weight}
            arms.append((f'{role}_{index}_w{weight:g}',cfg))
        payload=execute(87,arms,ctx,False);winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(87,[],ctx)


def refinement():
    verify();winner=prior_best((85,86,87));base=configuration(winner);ctx=Context()
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    for label,key,values in (('memory','membership_memory',(0.,.0125,.025,.0375,.05)),('fusion','membership_w5a_weight',(.725,.75,.775))):
        payload=execute(88,[(f'{label}{v:g}',dict(base,**{key:v})) for v in values],ctx,False)
        winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    payload=execute(88,[(f'top{t:g}_rest{r:g}',dict(base,top_slow_weight=t,slow16_weight=r))
                       for t,r in itertools.product((.22,.24,.26),(.23,.25,.27))],ctx,False)
    winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(88,[(f'shift{v:g}',dict(base,limit_up_delta=v)) for v in (.055,.075,.095)],ctx)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','independent','combinations','refine_weights','refinement','all'));stage=parser.parse_args().stage
    for name in (('freeze','build','independent','combinations','refine_weights','refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
