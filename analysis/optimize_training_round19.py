"""Waves105–108: CatBoost rank/return and depth variants under both role-fusion scales."""
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
import optimize_training_round18 as previous
import catboost_model_sources_20261003 as trainer
from optimize_training_round13 import prefix_controls
from optimize_training_round18 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r19'
PREVIOUS=ROOT/'analysis/optimization_20261003_r18'
WAVES=(105,106,107,108)
FIELDS=previous.FIELDS
ROLES=('membership','top','rest')
MODELS=tuple(trainer.CONFIGS)
NEW_MODELS=tuple(trainer.NEW_CONFIGS)
WEIGHTS=(.005,.025,.05,.15,.30,.50)
BLENDS=('rank','score')


def baseline():
    old=read(PREVIOUS/'selection.json')['winner']
    cfg=previous.configuration(old)
    for spec in cfg['diverse_augmentation'].values():spec.setdefault('blend','rank')
    return cfg


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
        if name not in self._diverse_cache or len(self._diverse_cache[name][1])<len(self.dates):
            values=np.load(trainer.ranker_source(name,OUT))[:len(self.dates)]
            self._diverse_cache[name]=(values,daily_ranks(values,self.valid,self.dates))
        other=self._diverse_cache[name][1][:len(self.dates)]
        if spec.get('blend','rank')=='rank':
            current=daily_ranks(base,self.valid,self.dates);keep=(other>-9)&(current>-9);out=np.full(len(base),-10.)
            out[keep]=(1-weight)*current[keep]+weight*other[keep]
            return np.where(out>-9,out+1e-9*self.tie_key,out)+1e-9*self.tie_key
        assert spec['blend']=='score';keep=(other>-9)&(base>-9);out=np.full(len(base),-10.)
        out[keep]=(1-weight)*base[keep]+weight*other[keep]+weight*1e-9*self.tie_key[keep]
        return out

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline' and (recipe is None or recipe==baseline()['recipe'])
        return np.load(PREVIOUS/'promote_baseline.npy')


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round18 import selected
    selected();trainer.verify();assert read(trainer.OUT/'oof_audit.json')['status']=='passed'
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/identical_official_score_cache_20261003.py',ROOT/'analysis/official_score_cache_qa_20261003/verification.json',ROOT/'analysis/finalize_training_round19.py',ROOT/'analysis/verify_methods_round19.py',ROOT/'analysis/run_training_round19_pipeline.py',
             Path(trainer.__file__),ROOT/'analysis/train_catboost_bank_20261003.py',ROOT/'analysis/objective_model_sources_20261003.py',ROOT/'analysis/train_objective_bank_20261003.py',ROOT/'analysis/cross_section_model_sources_20261003.py',ROOT/'analysis/train_cross_section_bank_20261003.py',ROOT/'analysis/train_neural_bank_20261003.py',ROOT/'analysis/train_diverse_backbones_20261003.py',ROOT/'analysis/diverse_model_sources_20261003.py',trainer.OUT/'protocol.json',trainer.OUT/'oof_audit.json',
             ROOT/'后续选模标准.md',ROOT/'evaluate.py',ROOT/'active_release.json',
             PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
             PREVIOUS/'diverse_augmentation_causal_checks.json',ROOT/'candidates/optimization_20261003_r18/verification.json',
             ROOT/'analysis/optimize_training_round18.py',ROOT/'analysis/finalize_training_round18.py',
             ROOT/'analysis/optimize_training_round12.py',ROOT/'analysis/optimize_training_round11.py',
             ROOT/'analysis/retention_priority_round10.py',HERE/'optimize_wave15.py',HERE/'optimize_wave18.py']
    sources += [path for number in (14,15,16,17) for path in (ROOT/f'analysis/optimization_20261003_r{number}/rankers').glob('*.npy')]
    for name in NEW_MODELS:
        for year in YEARS:
            sources.extend(trainer.OUT/name/f'{kind}_{year}.{suffix}' for kind,suffix in (('model','joblib'),('raw','parquet'),('info','json')))
            sources.append(trainer.OUT/f'boundary_control_{name}_{year}.json')
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'baseline_score':expected(),
         'starting_configuration':baseline(),'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'wave105':{'models':NEW_MODELS,'roles':ROLES,'weights':WEIGHTS,'blends':BLENDS,'baseline_records':1},
         'wave106':{'baseline_rank_score_role_combinations':27},
         'wave107':{'six_weights_each_role':'zero,half,anchor,double,anchor+0.0125,anchor+0.025','clip':(0.,.8)},
         'wave108':{'memory':(0.,.0125,.025,.0375,.05),'fusion':(.725,.75,.775),
                   'top_slow':(.22,.24,.26),'rest_slow':(.23,.25,.27),'limit_shifts':(.055,.075,.095)},
         'official_score_reuse':'Only byte-identical output CSVs with identical validation CSVs, official code and runtime versions; retain each requested scoring record.',
         'expected_scored_records':174,'new_model_training':True,'new_fold_models_trained':15,
         'training_pipeline':str(trainer.OUT/'protocol.json'),'method':'Compare three new CatBoost targets/depths in rank and continuous-score fusion, three independent roles, then three-way combinations and fine weights. GPU refits are not bit-deterministic; frozen serial inference is verified.',
         'selection_rule':'highest official connected composite; exact ties prefer fewer active new models and augmented roles',
         'test_labels_read':False,'test_future_prices_used_to_select':False,'pruned_member_excluded':True,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round19 CatBoost targets/depths and both fusion scales protocol frozen')


def build():
    import numpy as np
    import polars as pl
    from src.scoring import Panel
    from optimize_wave6 import make_prediction_param
    verify()
    if (OUT/'component_audit.json').exists():
        for path,digest in read(OUT/'component_audit.json')['output_sha256'].items():assert sha(path)==digest,path
        return
    ctx=Context();folder=OUT/'rankers';folder.mkdir(exist_ok=True);parts={name:[] for name in NEW_MODELS}
    for year in YEARS:
        frame=ctx.label_free.filter(pl.col('trade_date')//10000==year)
        for name in NEW_MODELS:
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
    for role,name in zip(ROLES,NEW_MODELS):
        for blend in BLENDS:
            cfg=deepcopy(base);cfg['diverse_augmentation'][role]={'model':name,'weight':.025,'blend':blend}
            controls.append(prefix_controls(ctx,ctx.finished('baseline'),cfg,counts=(80,260)))
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_output_bit_identical':True,
         'active_augmentation_prefix_and_poisoning_controls':controls,'models_trained':15,'test_data_read':False,
         'output_sha256':{str(p):sha(p) for p in sorted(folder.glob('*.npy'))}},immutable=True)
    log('Round19 baseline, new role rankers and active-method causal controls passed')


def evaluate(ctx,cfg):
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);metrics=ctx.score(pred)
    log(f'Round19 augmentation={cfg["diverse_augmentation"]}: {metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline','ensemble_weights':weights_from_name(cfg['ensemble_name']),
            'top_ensemble_weights':weights_from_name(cfg['top_ensemble_name']),
            'membership_ensemble_weights':weights_from_name(cfg['membership_ensemble_name']),
            'role_ensembles_split':cfg['top_ensemble_name']!=cfg['ensemble_name'],'fold_local_pruning_repaired':True,
            'pruned_member_excluded':True,'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats,'official_score_cache':deepcopy(ctx.last_official_score_cache)}


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
    for role,name,blend,weight in itertools.product(ROLES,NEW_MODELS,BLENDS,WEIGHTS):
        cfg=deepcopy(base);cfg['diverse_augmentation'][role]={'model':name,'weight':weight,'blend':blend}
        arms.append((f'{role}_{blend}_{name}_w{weight:g}',cfg))
    execute(105,arms)


def combinations():
    verify();base=baseline();rows=read(OUT/'wave105_results.json')['results'];winners={}
    for role in ROLES:
        winners[role]={blend:best(row for key,row in rows.items() if key.startswith(role+'_'+blend+'_')) for blend in BLENDS}
    dump(OUT/'combination_protocol.json',{'independent_role_winners':winners},immutable=True)
    arms=[]
    for switches in itertools.product(('baseline',)+BLENDS,repeat=3):
        cfg=deepcopy(base)
        for role,choice in zip(ROLES,switches):
            if choice!='baseline':cfg['diverse_augmentation'][role]=deepcopy(winners[role][choice]['diverse_augmentation'][role])
        arms.append(('choices_'+'_'.join(switches),cfg))
    execute(106,arms)


def refine_weights():
    verify();winner=prior_best((105,106));base=configuration(winner);ctx=Context()
    role_winners=read(OUT/'combination_protocol.json')['independent_role_winners']
    dump(OUT/'weight_refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    for role in ROLES:
        spec=base['diverse_augmentation'][role]
        if spec['weight']==0:spec=best(role_winners[role].values())['diverse_augmentation'][role]
        name=spec['model'];blend=spec.get('blend','rank');anchor=base['diverse_augmentation'][role]['weight']
        values=[0.,max(0.,anchor*.5),anchor,min(.8,anchor*2),min(.8,anchor+.0125),min(.8,anchor+.025)]
        dump(OUT/f'weight_refinement_{role}_protocol.json',{'anchor':base,'model':name,'blend':blend,'weights':values},immutable=True)
        arms=[]
        for index,weight in enumerate(values):
            cfg=deepcopy(base);cfg['diverse_augmentation'][role]={'model':name if weight>0 else 'none','weight':weight,'blend':blend}
            arms.append((f'{role}_{index}_{blend}_w{weight:g}',cfg))
        payload=execute(107,arms,ctx,False);winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(107,[],ctx)


def refinement():
    verify();winner=prior_best((105,106,107));base=configuration(winner);ctx=Context()
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    for label,key,values in (('memory','membership_memory',(0.,.0125,.025,.0375,.05)),('fusion','membership_w5a_weight',(.725,.75,.775))):
        payload=execute(108,[(f'{label}{v:g}',dict(base,**{key:v})) for v in values],ctx,False)
        winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    payload=execute(108,[(f'top{t:g}_rest{r:g}',dict(base,top_slow_weight=t,slow16_weight=r))
                       for t,r in itertools.product((.22,.24,.26),(.23,.25,.27))],ctx,False)
    winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(108,[(f'shift{v:g}',dict(base,limit_up_delta=v)) for v in (.055,.075,.095)],ctx)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','independent','combinations','refine_weights','refinement','all'));stage=parser.parse_args().stage
    for name in (('freeze','build','independent','combinations','refine_weights','refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
