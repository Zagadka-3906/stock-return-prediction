"""Waves145–147: jointly revisit active layers by recomputing the complete scheme."""
from copy import deepcopy
from pathlib import Path
import json
import os
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round29 as previous
import linear_model_sources_with_inputs_20261004 as trainer
import build_scheme_replay_bank_20261003 as bank
from replay_complete_scheme_20261003 import Context as ReplayContext,prefix_controls
from optimize_training_round29 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r30'
PREVIOUS=ROOT/'analysis/optimization_20261003_r29'
FORMAL=ROOT/'deliveries/connected_topk0175_20261003'
WAVES=(145,146,147)
FIELDS=previous.FIELDS
MODELS=tuple(trainer.CONFIGS)
NEW_MODELS=()
GROUPS=('diverse_augmentation','secondary_augmentation','final_augmentation','linear_augmentation')


def baseline():return previous.configuration(read(PREVIOUS/'selection.json')['winner'])
def expected():return read(PREVIOUS/'selection.json')['winner']['connected_final_score']
def configuration(row):return {key:deepcopy(row[key]) for key in FIELDS}
def signature(row):return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))


def best(rows):
    def key(row):
        active=[spec for group in GROUPS for spec in row[group].values() if spec['weight']>0]
        return (-row['connected_final_score'],len({spec['model'] for spec in active}),len(active),signature(row))
    return min(rows,key=key)


def axes(cfg):
    return [(group,role) for group in GROUPS for role,spec in cfg[group].items()
            if spec['weight']>0 and (not cfg['standalone'] or group not in GROUPS[:2])]


def scalar_axes(cfg):
    if cfg['standalone']:
        return [('standalone.alpha','alpha',(-.025,0.,.025)),
                ('standalone.bonus','bonus',(-.05,0.,.05)),
                ('standalone.aux','weight',(-.125,0.,.125))]
    return [(key,None,(-.025,0.,.025)) for key in ('top_slow_weight','slow16_weight',
            'membership_slow_weight','membership_w5a_weight','membership_memory')]+[
            ('membership_power',None,(0.,.5,1.,2.))]


def expected_records(cfg):
    return 1+12*len(axes(cfg))+sum(len(values) for _,_,values in scalar_axes(cfg))+5+3+5+5


class Context(ReplayContext):
    replay_folder=bank.OUT
    def __init__(self):
        super().__init__();self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round29 import selected
    selected();trainer.verify();bank.verify();audit=read(bank.OUT/'oof_audit.json');assert audit['status']=='passed'
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/causal_model_loading_20261004.py',ROOT/'analysis/linear_model_sources_with_inputs_20261004.py',ROOT/'analysis/verify_current_day_input_loading_20261004.py',ROOT/'analysis/current_day_input_loading_qa_20261004/verification.json',ROOT/'analysis/replay_complete_scheme_20261003.py',Path(bank.__file__),
         bank.OUT/'protocol.json',bank.OUT/'oof_audit.json',ROOT/'analysis/preflight_complete_scheme_replay_20261003.py',
         ROOT/'analysis/complete_scheme_replay_preflight_20261003/verification.json',
         ROOT/'analysis/finalize_training_round30.py',ROOT/'analysis/verify_methods_round30.py',
         ROOT/'analysis/predict_complete_scheme_round30.py',ROOT/'analysis/run_training_round30_pipeline.py',
         PREVIOUS/'selection.json',PREVIOUS/'protocol.json',PREVIOUS/'selected_validation.npy',
         PREVIOUS/'promote_baseline.npy',PREVIOUS/'linear_role_causal_checks.json',
         ROOT/'candidates/optimization_20261003_r29/verification.json']
    sources += [ROOT/'analysis/verify_complete_future_replay_20261003.py',
                ROOT/'analysis/complete_scheme_future_replay_qa_20261003/verification.json',
                ROOT/'analysis/verify_complete_future_branches_v2_20261003.py',
                ROOT/'analysis/complete_scheme_future_branches_qa_v2_20261003/verification.json',
                ROOT/'analysis/optimization_20261003_r18/promote_baseline.npy',
                FORMAL/'generation_inputs.parquet',FORMAL/'train_test.json',
                ARCHIVE/'releases/pooled_rms25/backbone_raw.parquet',
                ARCHIVE/'releases/ensemble4/T2f_xgboost_test_raw.parquet',
                ARCHIVE/'releases/ensemble4/W2c_two_day_test_raw.parquet',
                ARCHIVE/'releases/ensemble4/W2d_pruned_test_raw.parquet',HERE/'w5a_test/gru_raw_test.npy']
    sources += [ROOT/'analysis/cross_round_official_score_reuse_20261003.py',
                ROOT/'analysis/verify_cross_round_official_reuse_20261003.py',
                ROOT/'analysis/cross_round_official_reuse_qa_20261003/verification.json',
                ROOT/'analysis/verify_mapped_cross_round_reuse_20261003.py',
                ROOT/'analysis/mapped_cross_round_reuse_qa_20261003/verification.json']
    sources += [ROOT/'analysis/parallel_candidate_scoring_20261004.py',
                ROOT/'analysis/parallel_scoring_qa_context_20261004.py',
                ROOT/'analysis/verify_parallel_candidate_scoring_20261004.py',
                ROOT/'analysis/parallel_candidate_scoring_qa_20261004/verification.json']
    sources.extend(Path(info['path']) for info in read(ROOT/'candidates/optimization_20261003_r29/verification.json')['models'].values())
    sources.extend(Path(path) for path in read(PREVIOUS/'protocol.json')['input_sha256'])
    sources.extend(Path(path) for path in read(bank.OUT/'protocol.json')['input_sha256'])
    sources.extend(Path(path) for path in audit['output_sha256'])
    cfg=baseline()
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':expected(),'starting_configuration':cfg,'same_validation':'2020–2024 annual forward OOF;1212 continuous days;5635800 rows',
         'active_weight_axes':axes(cfg),'scalar_axes':scalar_axes(cfg),
         'weight_values':'zero, half, anchor, double, anchor+0.0125, anchor+0.025; clipped to [0,0.8]',
         'search':'Independent active-weight arms, then one coordinate pass with each anchor frozen before scoring; scalar and complete output refinement follow.',
         'parallel_candidate_execution':{'workers':2,'commit_order':'declared arm order','adaptive_stage_barriers_preserved':True,'private_actual_csv_and_official_capsules':True},
         'expected_scored_records':expected_records(cfg),'new_model_training':False,'new_fold_models_trained':0,
         'method':'Recompute the standalone or original hybrid foundation, both initial model additions, complete-output role addition including causal regime weights, and final linear addition. No frozen output foundation is used to hide changes to earlier layers.',
         'recipe_fixed':True,'model_names_fixed':True,'test_labels_read':False,
         'test_future_prices_used_to_select':False,'pruned_member_excluded':True,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'input_sha256':{str(path.resolve()):sha(path) for path in dict.fromkeys(sources)}},immutable=True)


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();cfg=baseline();promote=ctx.finished('baseline')
    pred,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    controls=prefix_controls(ctx,cfg)
    dump(OUT/'component_audit.json',{'status':'passed','complete_previous_output_recomputed_bit_identically':True,
         'controls':controls,'models_trained':0,'test_data_read':False,'output_sha256':{}},immutable=True)


def evaluate(ctx,cfg):
    ctx.configure(cfg);promote=ctx.finished('baseline')
    pred,stats=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    metrics=ctx.score(pred);log(f'Round30 complete replay: {metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline','ensemble_weights':weights_from_name(cfg['ensemble_name']),
         'top_ensemble_weights':weights_from_name(cfg['top_ensemble_name']),
         'membership_ensemble_weights':weights_from_name(cfg['membership_ensemble_name']),
         'role_ensembles_split':cfg['top_ensemble_name']!=cfg['ensemble_name'],
         'fold_local_pruning_repaired':True,'pruned_member_excluded':True,
         'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats,
         'official_score_cache':deepcopy(ctx.last_official_score_cache),
         'causal_return_mapping':deepcopy(ctx.last_candidate_return_mapping)}


def execute(wave,arms,ctx=None,finish=True):
    from parallel_candidate_scoring_20261004 import evaluate_many
    path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    missing=[];seen=set(payload['results'])
    for key,cfg in arms:
        if key not in seen:missing.append((key,cfg));seen.add(key)
    configurations=dict(missing)
    for key,row in evaluate_many('optimize_training_round30',missing,OUT):
        payload['results'][key]=row;dump(path,payload)
        if signature(configurations[key])==signature(baseline()):assert row['connected_final_score']==expected()
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def prior_best(waves):return best([row for wave in waves for row in read(OUT/f'wave{wave}_results.json')['results'].values()])


def proposals(cfg,group,role):
    anchor=cfg[group][role]['weight'];values=(0.,anchor*.5,anchor,min(.8,anchor*2),min(.8,anchor+.0125),min(.8,anchor+.025))
    result=[]
    for index,value in enumerate(values):
        proposal=deepcopy(cfg);proposal[group][role]['weight']=value
        result.append((f'{group}_{role}_{index}_w{value:g}',proposal))
    return result


def independent():
    verify();build();cfg=baseline();arms=[('baseline',cfg)]
    for group,role in axes(cfg):arms.extend(proposals(cfg,group,role))
    execute(145,arms)


def coordinate():
    verify();ctx=Context();winner=prior_best((145,))
    for group,role in axes(baseline()):
        path=OUT/f'coordinate_{group}_{role}_protocol.json'
        if path.exists():anchor=read(path)['anchor']
        else:
            anchor=configuration(winner);dump(path,{'anchor':anchor,'axis':(group,role)},immutable=True)
        payload=execute(146,proposals(anchor,group,role),ctx,False)
        winner=best([winner]+list(payload['results'].values()))
    execute(146,[],ctx)


def refinement():
    verify();ctx=Context();winner=prior_best((145,146))
    searches=scalar_axes(baseline())+[
         ('retention',None,(0.,.97,.98,.984,.99)),('limit_up_delta',None,(.055,.075,.095)),
         ('final_limit_delta',None,(-.04,-.02,0.,.02,.04)),('linear_limit_delta',None,(-.04,-.02,0.,.02,.04))]
    for name,key,values in searches:
        path=OUT/f'output_{name}_protocol.json'
        if path.exists():anchor=read(path)['anchor']
        else:
            anchor=configuration(winner);dump(path,{'anchor':anchor,'axis':name,'values':values},immutable=True)
        arms=[]
        for index,value in enumerate(values):
            cfg=deepcopy(anchor)
            if key:
                post=cfg['standalone']['postprocessing'];bounds=(0.,.995) if key=='alpha' else (0.,1.) if key=='weight' else (0.,2.)
                post[key]=min(bounds[1],max(bounds[0],post[key]+value))
            elif name=='membership_power':cfg[name]=value
            elif name in ('retention','limit_up_delta','final_limit_delta','linear_limit_delta'):cfg[name]=value
            else:cfg[name]=min(.99,max(0.,cfg[name]+value))
            arms.append((f'{name}_{index}_{value:g}',cfg))
        payload=execute(147,arms,ctx,False);winner=best([winner]+list(payload['results'].values()))
    execute(147,[],ctx)
