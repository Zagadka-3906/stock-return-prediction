"""Waves159–161: compare complete standalone outputs of all six mature past-OOF learned stacking backbones."""
from __future__ import annotations
from copy import deepcopy
import itertools
import json
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round33 as previous
import stacking_model_sources_20261004 as trainer
from optimize_training_round33 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r34'
PREVIOUS=ROOT/'analysis/optimization_20261003_r33'
WAVES=(159,160,161)
FIELDS=previous.FIELDS
MODELS=tuple(trainer.NEW_CONFIGS)
NEW_MODELS=()
ALPHAS=(.8,.9,.95)
AUXILIARY=(0.,.25)


def baseline():return {**previous.configuration(read(PREVIOUS/'selection.json')['winner']),'standalone_replacement':False}
def expected():return read(PREVIOUS/'selection.json')['winner']['connected_final_score']
def configuration(row):return {k:deepcopy(row[k]) for k in FIELDS}
def signature(row):return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))


def best(rows):
    def complexity(row):
        if row['standalone']:
            name=row['standalone']['model'];return len(trainer.CONFIGS[name].get('members',[name]))
        return 5+len({v['model'] for group in ('diverse_augmentation','secondary_augmentation') for v in row[group].values() if v['weight']>0})
    return min(rows,key=lambda row:(-row['connected_final_score'],complexity(row),signature(row)))


def standalone_cfg(name,alpha=.9,aux=.25,bonus=.3):
    cfg=baseline();cfg['standalone']={'model':name,'postprocessing':dict(BASE_POST,alpha=alpha,weight=aux,bonus=bonus)}
    cfg['diverse_augmentation']={r:{'model':'none','weight':0.,'blend':'score'} for r in ('membership','top','rest')}
    cfg['secondary_augmentation']=deepcopy(cfg['diverse_augmentation'])
    cfg['standalone_replacement']=True;cfg['final_augmentation']={r:{'model':'none','weight':0.} for r in ('membership','top','rest')};cfg['final_limit_delta']=0.
    cfg['linear_augmentation']=deepcopy(cfg['final_augmentation']);cfg['linear_limit_delta']=0.
    cfg['regularization_augmentation']=deepcopy(cfg['final_augmentation']);cfg['regularization_limit_delta']=0.
    cfg['stacking_augmentation']=deepcopy(cfg['final_augmentation']);cfg['stacking_limit_delta']=0.
    return cfg


class Context(previous.Context):
    def __init__(self):
        super().__init__();self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())

    def configure(self,cfg):
        super().configure(cfg);self.standalone=deepcopy(cfg.get('standalone'));self.standalone_replacement=cfg.get('standalone_replacement',False);self._current_cfg=deepcopy(cfg)

    def finished(self,name,recipe=None):
        import numpy as np
        import polars as pl
        from src.scoring import Panel
        from optimize_wave6 import make_prediction_param
        assert name=='baseline'
        if not self.standalone_replacement:return np.load(PREVIOUS/'promote_baseline.npy')[:len(self.dates)]
        frame=self.label_free.head(len(self.dates));source=OUT
        raw=np.load(source/f'raw/{self.standalone["model"]}.npy',mmap_mode='r')[:len(frame)]
        return make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw))),
                                     frame['aux_raw'].to_numpy(),**self.standalone['postprocessing'])

    def donor(self,promote,rerank_weight=None):
        return promote

    def predict(self,donor,weight,retention,delta=0.):
        import numpy as np
        from optimize_wave13 import build_ab
        if not self.standalone_replacement:
            assert configuration(self._current_cfg)==baseline()
            pred=np.load(PREVIOUS/'selected_validation.npy',mmap_mode='r')[:len(self.dates)].copy()
            return pred,deepcopy(read(PREVIOUS/'selection.json')['winner']['construction'])
        ordered=np.where(donor>-9,donor+1e-9*self.tie_key,donor)
        pred,stats=build_ab(ordered,ordered,ordered,self.dates,self.flags,self.codes,self.n_codes,retention)
        pred[self.flags==1]+=delta
        return pred,stats


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round33 import selected
    selected();trainer.verify()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round34.py',ROOT/'analysis/verify_methods_round34.py',
             ROOT/'analysis/run_training_round34_pipeline.py',ROOT/'analysis/predict_standalone_round34.py',
             ROOT/'analysis/reuse_candidate_round34.py',ROOT/'analysis/preflight_standalone_round34_v2.py',ROOT/'analysis/standalone_round34_preflight_v2/verification.json',
             Path(trainer.__file__),ROOT/'analysis/train_oof_stacking_bank_20261004.py',ROOT/'analysis/verify_oof_stacking_20261004_v2.py',ROOT/'analysis/oof_stacking_preflight_20261004_v2/verification.json',trainer.OUT/'protocol.json',trainer.OUT/'oof_audit.json',trainer.OUT/'input_routing_recovery_protocol.json',ROOT/'analysis/resume_stacking_input_routing_20261004.py',ROOT/'analysis/causal_model_loading_20261004.py',ROOT/'analysis/verify_current_day_input_loading_20261004.py',ROOT/'analysis/current_day_input_loading_qa_20261004/verification.json',
             ROOT/'analysis/score_calibrated_candidates_20261003.py',
             ROOT/'analysis/identical_official_score_cache_20261003.py',ROOT/'analysis/official_score_cache_qa_20261003/verification.json',
             ROOT/'后续选模标准.md',ROOT/'evaluate.py',ROOT/'src/scoring.py',ROOT/'active_release.json',
             HERE/'optimize_wave6.py',HERE/'optimize_wave13.py',HERE/'return_mapping.py',ROOT/'run.py',ROOT/'src/postprocessing.py',PREVIOUS/'selection.json',PREVIOUS/'protocol.json',
             PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',PREVIOUS/'stacking_role_causal_checks.json',
             ROOT/'analysis/train_diverse_backbones_20261003.py',
             ROOT/'analysis/neural_regularization_bank_20261003/oof_audit.json',
             ROOT/'candidates/optimization_20261003_r33/verification.json']
    sources += [ROOT/'analysis/official_validation_csv_parse_cache_20261003.py',
                ROOT/'analysis/validation_parse_cache_qa_20261003/verification.json',
                ROOT/'analysis/verify_validation_parse_cache_20261003.py',
                ROOT/'analysis/validation_parse_cache_full_oof_qa_20261003/verification.json',
                ROOT/'analysis/verify_prospective_score_wrappers_20261003.py',
                ROOT/'analysis/prospective_score_wrappers_qa_20261003/verification.json']
    sources += [ROOT/'analysis/verify_linear_round_baseline_20261003.py',
                ROOT/'analysis/linear_round_baseline_qa_20261003/verification.json']
    sources += [ROOT/'analysis/verify_stacking_round_baselines_20261004_v2.py',
                ROOT/'analysis/stacking_round_baselines_qa_20261004_v2/verification.json']
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
         'wave159':{'standalone_models':MODELS,'alphas':ALPHAS,'auxiliary':AUXILIARY,'bonus':.3,'baseline_records':1},
         'wave160':{'each_model_refined_independently':True,'alpha_offsets':(-.025,0.,.025),'bonuses':(0.,.15,.3),'each_model_retention':(0.,.97,.98,.984,.99)},
         'wave161':{'retention':(0.,.97,.98,.984,.99),'limit_shifts':(.055,.075,.095),
                    'auxiliary_offsets':(-.125,0.,.125),'alpha_offsets':(-.0125,0.,.0125),'bonus_offsets':(-.05,0.,.05)},
         'parallel_candidate_execution':{'workers':4,'commit_order':'declared arm order','adaptive_stage_barriers_preserved':True,'private_actual_csv_and_official_capsules':True},
         'expected_scored_records':138,'new_model_training':False,'new_fold_models_trained':0,
         'standalone_method':'Only the named model and common auxiliary signal supply predictions. Continuous causal smoothing and persistence, retention construction with all three roles using its own complete postprocessed output, and past-label return calibration. No previous membership donor or return-ordering model contributes.',
         'selection_rule':'highest official connected composite; exact ties prefer fewer models',
         'test_labels_read':False,'test_future_prices_used_to_select':False,'pruned_member_excluded':True,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round34 complete standalone model protocol frozen')


def prefix_controls(ctx,cfg,counts=(80,260,975)):
    from copy import copy
    import numpy as np
    import polars as pl
    ctx.configure(cfg);promote=ctx.finished('baseline');pred,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    poisoned=copy(ctx);poisoned.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    poisoned.label_free=ctx.label_free.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    poisoned_promote=poisoned.finished('baseline')
    replay,_=poisoned.predict(poisoned.donor(poisoned_promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    assert np.array_equal(pred,replay)
    proofs=[];dates=np.unique(ctx.dates)
    for count in counts:
        last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={k:v[:n] for k,v in ctx.ranks.items()}
        fresh_promote=prefix.finished('baseline');assert np.array_equal(promote[:n],fresh_promote)
        replay,_=prefix.predict(prefix.donor(fresh_promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        assert np.array_equal(pred[:n],replay),(cfg['standalone'],last)
        proofs.append({'days':count,'through_date':last,'bit_identical':True,'postprocessing_recomputed_from_prefix':True})
    return {'standalone':cfg['standalone'],'label_poisoning_bit_identical':True,'future_append_prefix_invariance':proofs}


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
    controls=[prefix_controls(ctx,standalone_cfg(name),counts=(80,260)) for name in MODELS]
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_output_bit_identical':True,
         'standalone_prefix_and_poisoning_controls':controls,'models_trained':0,'test_data_read':False,
         'output_sha256':{str(p):sha(p) for p in sorted(folder.glob('*.npy'))}},immutable=True)
    log('Round34 all standalone postprocessing prefix and label-poisoning controls passed')


def evaluate(ctx,cfg):
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);metrics=ctx.score(pred)
    pure=cfg['standalone'];members={pure['model']:1.} if pure else weights_from_name(cfg['ensemble_name'])
    log(f'Round34 standalone={pure}: {metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline','ensemble_weights':members,
            'top_ensemble_weights':members if pure else weights_from_name(cfg['top_ensemble_name']),
            'membership_ensemble_weights':members if pure else weights_from_name(cfg['membership_ensemble_name']),
            'role_ensembles_split':False if pure else cfg['top_ensemble_name']!=cfg['ensemble_name'],
            'fold_local_pruning_repaired':True,'pruned_member_excluded':True,'complete_standalone_model':cfg['standalone_replacement'],
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats,
            'official_score_cache':deepcopy(ctx.last_official_score_cache),'causal_return_mapping':deepcopy(ctx.last_candidate_return_mapping)}


def execute(wave,arms,ctx=None,finish=True):
    from parallel_candidate_scoring_four_20261004 import evaluate_many
    path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    missing=[];seen=set(payload['results'])
    for key,cfg in arms:
        if key not in seen:missing.append((key,cfg));seen.add(key)
    configurations=dict(missing)
    for key,row in evaluate_many('optimize_training_round34',missing,OUT):
        payload['results'][key]=row;dump(path,payload)
        if signature(configurations[key])==signature(baseline()):assert abs(row['connected_final_score']-expected())<1e-12
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def prior_best(waves):return best([r for w in waves for r in read(OUT/f'wave{w}_results.json')['results'].values()])


def independent():
    verify();build();arms=[('baseline',baseline())]
    arms.extend((f'{name}_alpha{a:g}_aux{w:g}',standalone_cfg(name,a,w)) for name,a,w in itertools.product(MODELS,ALPHAS,AUXILIARY))
    execute(159,arms)


def model_refinement():
    verify();rows=read(OUT/'wave159_results.json')['results'];anchors={name:configuration(best(r for r in rows.values() if r['standalone'] and r['standalone']['model']==name)) for name in MODELS}
    dump(OUT/'model_refinement_protocol.json',{'independent_model_winners':anchors,'retentions':(0.,.97,.98,.984,.99)},immutable=True)
    ctx=Context()
    for name,cfg in anchors.items():
        anchor=cfg['standalone']['postprocessing'];arms=[]
        for offset,bonus in itertools.product((-.025,0.,.025),(0.,.15,.3)):
            proposal=deepcopy(cfg);proposal['standalone']['postprocessing'].update(alpha=min(.995,max(0.,anchor['alpha']+offset)),bonus=bonus)
            arms.append((f'{name}_offset{offset:g}_bonus{bonus:g}',proposal))
        payload=execute(160,arms,ctx,False)
        protocol=OUT/f'retention_refinement_{name}_protocol.json'
        if protocol.exists():local=read(protocol)['anchor']
        else:
            local=configuration(best([{**cfg,'connected_final_score':best(r for r in rows.values() if r['standalone'] and r['standalone']['model']==name)['connected_final_score']}]+[r for r in payload['results'].values() if r['standalone']['model']==name]))
            dump(protocol,{'anchor':local,'retentions':(0.,.97,.98,.984,.99)},immutable=True)
        execute(160,[(f'{name}_retention{value:g}',dict(local,retention=value)) for value in (0.,.97,.98,.984,.99)],ctx,False)
    execute(160,[],ctx)


def refinement():
    verify();winner=prior_best((159,160));base=configuration(winner);ctx=Context()
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    if not base['standalone_replacement']:
        execute(161,[(f'unchanged_baseline_{i}',deepcopy(base)) for i in range(17)],ctx);return
    for key,values in (('retention',(0.,.97,.98,.984,.99)),('limit_up_delta',(.055,.075,.095))):
        payload=execute(161,[(f'{key}{v:g}',dict(base,**{key:v})) for v in values],ctx,False)
        winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    for key,offsets in (('weight',(-.125,0.,.125)),('alpha',(-.0125,0.,.0125)),('bonus',(-.05,0.,.05))):
        # Standalone winners receive the declared three-axis refinement; the previous complete baseline remains fixed.
        post=base['standalone']['postprocessing'] if base['standalone'] else base['recipe']['postprocessing'];anchor=post[key]
        arms=[]
        for index,offset in enumerate(offsets):
            proposal=deepcopy(base);target=proposal['standalone']['postprocessing'] if proposal['standalone'] else proposal['recipe']['postprocessing']
            target[key]=min(.995 if key=='alpha' else 1.,max(0.,anchor+offset));arms.append((f'{key}{index}_{target[key]:g}',proposal))
        # Rebuilding a baseline TopK recipe belongs to its earlier search; here hold the complete previous baseline fixed.
        if not base['standalone']:arms=[(f'{key}{i}_baseline_unchanged',deepcopy(base)) for i in range(3)]
        payload=execute(161,arms,ctx,False);winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(161,[],ctx)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','independent','model_refinement','refinement'))
    globals()[parser.parse_args().stage]()
