"""Waves127–130: augment complete output roles, including a standalone foundation."""
from copy import deepcopy
import itertools
import json
import os
from pathlib import Path
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round24 as previous
import pairwise_model_sources_20261003 as trainer
from optimize_training_round24 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r25'
PREVIOUS=ROOT/'analysis/optimization_20261003_r24'
FOUNDATION=PREVIOUS
WAVES=(127,128,129,130)
FIELDS=previous.FIELDS+('final_augmentation','final_limit_delta')
MODELS=tuple(trainer.CONFIGS)
NEW_MODELS=tuple(trainer.NEW_CONFIGS)
ROLES=('membership','top','rest')
WEIGHTS=(.005,.025,.075,.2)


def baseline():
    return {**previous.configuration(read(PREVIOUS/'selection.json')['winner']),
            'final_augmentation':{r:{'model':'none','weight':0.} for r in ROLES},'final_limit_delta':0.}


def expected():return read(PREVIOUS/'selection.json')['winner']['connected_final_score']
def configuration(row):return {k:deepcopy(row[k]) for k in FIELDS}
def signature(row):return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))


def best(rows):
    def key(row):
        used=[v for v in row['final_augmentation'].values() if v['weight']>0]
        return (-row['connected_final_score'],len({v['model'] for v in used}),len(used),abs(row['final_limit_delta']),signature(row))
    return min(rows,key=key)


class Context(previous.Context):
    def __init__(self):
        super().__init__();self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())

    def configure(self,cfg):
        super().configure(cfg)
        self.final_augmentation=deepcopy(cfg.get('final_augmentation',{r:{'model':'none','weight':0.} for r in ROLES}))
        self.final_limit_delta=cfg.get('final_limit_delta',0.)
        self._foundation_configuration=previous.configuration({**cfg,'standalone':cfg.get('standalone')}) if 'standalone' in cfg else None
        if not hasattr(self,'_final_cache'):self._final_cache={}

    def finished(self,name,recipe=None):
        import numpy as np
        return np.load(FOUNDATION/'promote_baseline.npy')[:len(self.dates)]

    def weights_for(self,spec):return spec['weight']

    def signal(self,name):
        import numpy as np
        from optimize_wave15 import daily_ranks
        if name not in self._final_cache or len(self._final_cache[name])<len(self.dates):
            raw=np.load(OUT/f'raw/{name}.npy',mmap_mode='r')[:len(self.dates)]
            self._final_cache[name]=daily_ranks(raw,self.valid,self.dates)
        return self._final_cache[name][:len(self.dates)]

    def finish_output(self,base,retention,original_delta):
        import numpy as np
        from optimize_wave13 import build_ab
        from optimize_wave15 import daily_ranks
        active=any(spec['weight']>0 for spec in self.final_augmentation.values())
        if not active:
            pred=base.copy()
            if self.final_limit_delta:pred[self.flags==1]+=self.final_limit_delta
            return pred,{'extra_role_augmentation':False,'additional_limit_shift':self.final_limit_delta}
        unshifted=base.copy();unshifted[self.flags==1]-=original_delta
        ranks=daily_ranks(unshifted,self.valid,self.dates)
        def blend(role):
            spec=self.final_augmentation[role]
            if spec['weight']==0:return unshifted
            weight=self.weights_for(spec);other=self.signal(spec['model']);valid=(ranks>-9)&(other>-9)
            values=np.full(len(base),-10.);weighted=(1-weight)*ranks+weight*other
            assert np.isfinite(weighted).all() and np.all(np.asarray(weight)>=0) and np.all(np.asarray(weight)<=1)
            values[valid]=weighted[valid]+1e-9*self.tie_key[valid]
            return values
        donor,a,b=(blend(role) for role in ROLES)
        # Fixed membership gets zero extra retention; a changed donor gets its own causal floor.
        second_retention=retention if self.final_augmentation['membership']['weight']>0 else 0.
        pred,stats=build_ab(donor,a,b,self.dates,self.flags,self.codes,self.n_codes,second_retention)
        pred[self.flags==1]+=original_delta
        if self.final_limit_delta:pred[self.flags==1]+=self.final_limit_delta
        return pred,{'extra_role_augmentation':True,'second_retention':second_retention,'construction':stats,
                    'additional_limit_shift':self.final_limit_delta}

    def predict(self,donor,weight,retention,delta=0.):
        base,original=super().predict(donor,weight,retention,delta)
        pred,extra=self.finish_output(base,retention,delta)
        return pred,{'foundation':original,'final_augmentation':extra}


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round24 import selected
    selected();trainer.verify()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round25.py',ROOT/'analysis/verify_methods_round25.py',
             ROOT/'analysis/run_training_round25_pipeline.py',ROOT/'analysis/predict_final_roles_round25.py',
             ROOT/'analysis/preflight_final_roles_round25.py',ROOT/'analysis/final_roles_round25_preflight/verification.json',
             Path(trainer.__file__),ROOT/'analysis/train_pairwise_bank_20261003.py',trainer.OUT/'protocol.json',trainer.OUT/'oof_audit.json',
             ROOT/'analysis/score_calibrated_candidates_20261003.py',ROOT/'后续选模标准.md',ROOT/'active_release.json',
             PREVIOUS/'selection.json',PREVIOUS/'protocol.json',PREVIOUS/'standalone_causal_checks.json',
             PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
             ROOT/'candidates/optimization_20261003_r24/verification.json',ROOT/'candidates/optimization_20261003_r24/manifest.json',ROOT/'candidates/optimization_20261003_r24/rank_prediction.npy']
    sources += [ROOT/'analysis/official_validation_csv_parse_cache_20261003.py',
                ROOT/'analysis/validation_parse_cache_qa_20261003/verification.json',
                ROOT/'analysis/verify_validation_parse_cache_20261003.py',
                ROOT/'analysis/validation_parse_cache_full_oof_qa_20261003/verification.json',
                ROOT/'analysis/verify_prospective_score_wrappers_20261003.py',
                ROOT/'analysis/prospective_score_wrappers_qa_20261003/verification.json']
    sources += [ROOT/'analysis/cross_round_official_score_reuse_20261003.py',
                ROOT/'analysis/verify_cross_round_official_reuse_20261003.py',
                ROOT/'analysis/cross_round_official_reuse_qa_20261003/verification.json',
                ROOT/'analysis/verify_mapped_cross_round_reuse_20261003.py',
                ROOT/'analysis/mapped_cross_round_reuse_qa_20261003/verification.json']
    sources += [ROOT/'analysis/parallel_candidate_scoring_20261004.py',
                ROOT/'analysis/parallel_scoring_qa_context_20261004.py',
                ROOT/'analysis/verify_parallel_candidate_scoring_20261004.py',
                ROOT/'analysis/parallel_candidate_scoring_qa_20261004/verification.json']
    sources += [ROOT/'analysis/parallel_candidate_scoring_four_20261004.py',
                ROOT/'analysis/parallel_scoring_four_qa_context_20261004.py',
                ROOT/'analysis/verify_parallel_candidate_scoring_four_20261004.py',
                ROOT/'analysis/parallel_candidate_scoring_four_qa_20261004/verification.json',
                ROOT/'analysis/verify_official_parallel_capacity_20261004.py',
                ROOT/'analysis/official_parallel_capacity_qa_20261004/verification.json',
                ROOT/'analysis/prospective_parallel_four_adoption_20261004/verification.json']
    sources.extend(Path(p) for p in read(PREVIOUS/'protocol.json')['input_sha256'])
    for name in MODELS:
        for year in YEARS:
            sources.extend(trainer.source_dir(name)/f'{kind}_{year}.{suffix}' for kind,suffix in (('model','joblib'),('raw','parquet'),('info','json')))
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'baseline_score':expected(),
         'starting_configuration':baseline(),'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'wave127':{'models':MODELS,'roles':ROLES,'weights':WEIGHTS,'baseline_records':1},
         'wave128':{'independent_role_winner_on_off_combinations':8},
         'wave129':{'six_weights_each_role':'zero,half,anchor,double,anchor+0.0125,anchor+0.025','clip':(0.,.8)},
         'wave130':{'additional_limit_shift':(-.04,-.02,0.,.02,.04)},
         'parallel_candidate_execution':{'workers':4,'commit_order':'declared arm order','adaptive_stage_barriers_preserved':True,'private_actual_csv_and_official_capsules':True},
         'expected_scored_records':452,'new_model_training':True,'new_fold_models_trained':20,
         'complete_output_foundation_round':24,'inherited_fields_fixed':previous.FIELDS,
         'method':'Apply a separate signal to complete-output membership, Top ordering or rest ordering. Each is a current-day rank fusion. Ordering-only changes keep the foundation Top set unchanged; membership changes get an explicit second causal retention floor. This works with both standalone and hybrid foundations.',
         'official_candidate_scoring':'Every scoring record uses its own prior-mature-label return mapping and actual emitted CSV.',
         'selection_rule':'highest official connected composite; exact ties prefer fewer extra models/roles and smaller extra shift',
         'test_labels_read':False,'test_future_prices_used_to_select':False,'pruned_member_excluded':True,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round25 complete-output role augmentation protocol frozen')


def prefix_controls(ctx,cfg,counts=(80,260,975)):
    from copy import copy
    import numpy as np
    import polars as pl
    ctx.configure(cfg);promote=ctx.finished('baseline');pred,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    poisoned=copy(ctx);poisoned.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    poisoned.label_free=ctx.label_free.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    replay,_=poisoned.predict(poisoned.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);assert np.array_equal(pred,replay)
    proofs=[];dates=np.unique(ctx.dates)
    for count in counts:
        last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={k:v[:n] for k,v in ctx.ranks.items()};prefix._final_cache={}
        replay,_=prefix.predict(prefix.donor(promote[:n]),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        assert np.array_equal(pred[:n],replay),(cfg['final_augmentation'],last)
        proofs.append({'days':count,'through_date':last,'bit_identical':True,'cold_extra_signal_cache':True})
    return {'final_augmentation':cfg['final_augmentation'],'label_poisoning_bit_identical':True,'future_append_prefix_invariance':proofs}


def build():
    import numpy as np
    import polars as pl
    verify()
    if (OUT/'component_audit.json').exists():
        for path,digest in read(OUT/'component_audit.json')['output_sha256'].items():assert sha(path)==digest,path
        return
    ctx=Context();folder=OUT/'raw';folder.mkdir(exist_ok=True)
    for name in MODELS:
        parts=[]
        for year in YEARS:
            source=trainer.source_dir(name);info=read(source/f'info_{year}.json');path=source/f'raw_{year}.parquet'
            assert sha(path)==info['prediction_sha256'] and info['model_reload_bit_identical']
            meta=info['training_meta'];assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']<year*10000+101
            frame=ctx.label_free.filter(pl.col('trade_date')//10000==year);raw=pl.read_parquet(path)
            assert raw.select(KEYS).equals(frame.select(KEYS));parts.append(raw['pred_raw'].to_numpy())
        np.save(folder/f'{name}.npy',np.concatenate(parts))
    base=baseline();ctx.configure(base);pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),base['slow16_weight'],base['retention'],base['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    controls=[]
    for name,role in itertools.product(NEW_MODELS,ROLES):
        cfg=deepcopy(base);cfg['final_augmentation'][role]={'model':name,'weight':.075};controls.append(prefix_controls(ctx,cfg,counts=(80,260)))
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_output_bit_identical':True,
         'active_method_prefix_and_poisoning_controls':controls,'models_trained':20,'test_data_read':False,
         'output_sha256':{str(p):sha(p) for p in sorted(folder.glob('*.npy'))}},immutable=True)
    log('Round25 complete-output baseline and new role controls passed')


def evaluate(ctx,cfg):
    assert previous.configuration(cfg)==previous.configuration(baseline()),'Keep the complete foundation frozen during this role search'
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);metrics=ctx.score(pred)
    foundation=read(FOUNDATION/'selection.json')['winner']
    log(f'Round25 final_roles={cfg["final_augmentation"]} extra_shift={cfg["final_limit_delta"]}: {metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline',**{k:deepcopy(foundation[k]) for k in ('ensemble_weights','top_ensemble_weights','membership_ensemble_weights','role_ensembles_split')},
            'fold_local_pruning_repaired':True,'pruned_member_excluded':True,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats,
            'official_score_cache':deepcopy(ctx.last_official_score_cache),'causal_return_mapping':deepcopy(ctx.last_candidate_return_mapping)}


def execute(wave,arms,ctx=None,finish=True):
    from parallel_candidate_scoring_four_20261004 import evaluate_many
    path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    missing=[];seen=set(payload['results'])
    for key,cfg in arms:
        if key not in seen:missing.append((key,cfg));seen.add(key)
    configurations=dict(missing)
    for key,row in evaluate_many('optimize_training_round25',missing,OUT):
        payload['results'][key]=row;dump(path,payload)
        if signature(configurations[key])==signature(baseline()):assert abs(row['connected_final_score']-expected())<1e-12
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def prior_best(waves):return best([r for w in waves for r in read(OUT/f'wave{w}_results.json')['results'].values()])


def independent():
    verify();build();base=baseline();arms=[('baseline',base)]
    for role,name,weight in itertools.product(ROLES,MODELS,WEIGHTS):
        cfg=deepcopy(base);cfg['final_augmentation'][role]={'model':name,'weight':weight}
        arms.append((f'{role}_{name}_w{weight:g}',cfg))
    execute(127,arms)


def combinations():
    verify();base=baseline();rows=read(OUT/'wave127_results.json')['results'];winners={}
    for role in ROLES:winners[role]=best(row for key,row in rows.items() if key.startswith(role+'_'))
    dump(OUT/'combination_protocol.json',{'independent_role_winners':winners},immutable=True)
    arms=[]
    for switches in itertools.product((0,1),repeat=3):
        cfg=deepcopy(base)
        for role,on in zip(ROLES,switches):
            if on:cfg['final_augmentation'][role]=deepcopy(winners[role]['final_augmentation'][role])
        arms.append(('switches'+''.join(map(str,switches)),cfg))
    execute(128,arms)


def refine_weights():
    verify();winner=prior_best((127,128));base=configuration(winner);ctx=Context()
    role_winners=read(OUT/'combination_protocol.json')['independent_role_winners']
    dump(OUT/'weight_refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    for role in ROLES:
        spec=base['final_augmentation'][role]
        if spec['weight']==0:spec=role_winners[role]['final_augmentation'][role]
        name=spec['model'];anchor=base['final_augmentation'][role]['weight']
        values=[0.,max(0.,anchor*.5),anchor,min(.8,anchor*2),min(.8,anchor+.0125),min(.8,anchor+.025)]
        dump(OUT/f'weight_refinement_{role}_protocol.json',{'anchor':base,'model':name,'weights':values},immutable=True)
        arms=[]
        for index,weight in enumerate(values):
            cfg=deepcopy(base);cfg['final_augmentation'][role]={'model':name if weight>0 else 'none','weight':weight}
            arms.append((f'{role}_{index}_w{weight:g}',cfg))
        payload=execute(129,arms,ctx,False);winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(129,[],ctx)


def refinement():
    verify();winner=prior_best((127,128,129));base=configuration(winner)
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    execute(130,[(f'extra_shift{value:g}',dict(base,final_limit_delta=value)) for value in (-.04,-.02,0.,.02,.04)])


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','independent','combinations','refine_weights','refinement'))
    globals()[parser.parse_args().stage]()
