"""Waves261–265: joint weights, per-layer retention and final temporal refinement."""
from copy import deepcopy
from pathlib import Path
import itertools
import json
import os
import sys
import time
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[variable]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round62 as previous
from optimize_training_round62 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
from latest_graph_joint_axes_20261005 import active_axes,with_weight,retention_axes,expected_records
from whole_scheme_replay_runtime_20261004 import ValidationContext,raw_sources,prefix_controls as runtime_controls
from whole_scheme_future_runtime_20261004 import resolve_native_sources,candidate_models
OUT=ROOT/'analysis/optimization_20261003_r63'
PREVIOUS=ROOT/'analysis/optimization_20261003_r62'
GRAPH_FIELD='latest_joint_scheme_graph'
NUMBER=63
future_native_sources=resolve_native_sources
WAVES=(261,262,263,264,265)
FIELDS=previous.FIELDS+('latest_joint_scheme_graph',)
MODELS=NEW_MODELS=()
RETENTIONS=(0.,.97,.98,.984,.99)


def baseline():
    cfg=previous.configuration(read(PREVIOUS/'selection.json')['winner'])
    graph=deepcopy(cfg['nystrom_ridge_standalone_scheme_graph'])
    graph['active_weight_axes']=active_axes(graph)
    return {**cfg,'latest_joint_scheme_graph':graph}
def expected():return read(PREVIOUS/'selection.json')['winner']['connected_final_score']
def configuration(row):return {key:deepcopy(row[key]) for key in FIELDS}
def signature(row):return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))
def best(rows):
    def complexity(row):
        graph=row['latest_joint_scheme_graph'];active=sum(spec['weight']>0 for node in graph['layers'] for spec in node['specs'].values())
        root=graph['root']['configuration']
        if graph['root']['kind']=='complete_r30':active+=sum(v['weight']>0 for g in ('diverse_augmentation','secondary_augmentation','final_augmentation','linear_augmentation') for v in root[g].values())
        return active
    return min(rows,key=lambda row:(-row['connected_final_score'],complexity(row),signature(row)))
def axes():return read(OUT/'protocol.json')['weight_axes']


class Context(ValidationContext):
    def __init__(self):
        scoring=OUT/'scoring_validation_only';scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,scoring/name)
        super().__init__(baseline()['latest_joint_scheme_graph'],scoring=scoring)
    def configure(self,cfg):
        super().configure({'whole_scheme_graph':cfg.get(GRAPH_FIELD,cfg.get('whole_scheme_graph'))})


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol
def root_model_sources(graph):
    root=graph['root'];models=candidate_models(ROOT/f'candidates/optimization_20261003_r{root["round"]}')
    if root['kind']=='standalone' or root['configuration'].get('standalone'):return {}
    names=[f'seed{component["seed"]}_f{component["fraction"]:.3f}_r{component["rounds"]}' for component in root['configuration']['recipe']['components']]
    return {name:models[name] for name in names}
def state_mapping_path():return ROOT/'analysis/market_regime_bank_20261003/future_mapping_2025.json'
def freeze():
    if (OUT/'protocol.json').exists():verify();return
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    assert complete_round_evidence(62) is not None
    OUT.mkdir(exist_ok=True)
    graph=baseline()['latest_joint_scheme_graph']
    plan=ROOT/'analysis/latest_graph_joint_search_plan_20261005.json'
    preflight=ROOT/'analysis/latest_graph_joint_round63_source_preflight_20261005/verification.json'
    prepared=read(preflight)
    assert prepared['status']=='passed_pre_execution_source_and_lazy_dispatch_checks'
    for path,digest in prepared['input_sha256'].items():assert sha(path)==digest,path
    sources=[Path(__file__),ROOT/'analysis/latest_graph_joint_axes_20261005.py',
        ROOT/'analysis/finalize_training_round63.py',ROOT/'analysis/predict_latest_joint_scheme_20261005.py',
        ROOT/'analysis/check_latest_joint_scheme_20261005.py',ROOT/'analysis/run_training_round63_pipeline.py',
        ROOT/'analysis/prepare_latest_graph_joint_round63_sources_20261005.py',plan,preflight,
        ROOT/'analysis/latest_graph_joint_axes_scope_audit_20261005/verification.json',
        ROOT/'analysis/whole_scheme_replay_runtime_20261004.py',ROOT/'analysis/whole_scheme_future_runtime_20261004.py',
        ROOT/'analysis/nystrom_ridge_release_engine_20261004.py',ROOT/'analysis/predict_nystrom_ridge_scheme_20261004.py',
        ROOT/'analysis/parallel_candidate_scoring_four_20261004.py',ROOT/'analysis/publish_training_round.py',
        ROOT/'analysis/build_all_model_rankings_20261003.py',ROOT/'analysis/verify_all_model_rankings_20261003.py',
        ROOT/'后续选模标准.md',ROOT/'active_release.json',state_mapping_path(),
        PREVIOUS/'selection.json',PREVIOUS/'protocol.json',PREVIOUS/'selected_validation.npy',
        PREVIOUS/'provenance_scope_execution.json',
        ROOT/'results/optimization_20261003_r62.json',ROOT/'candidates/optimization_20261003_r62/verification.json',
        ROOT/'candidates/optimization_20261003_r62/manifest.json']
    sources += [Path(path) for path in read(PREVIOUS/'protocol.json')['input_sha256']]
    for paths in raw_sources(graph).values():sources.extend(paths)
    native=resolve_native_sources(graph);roots=root_model_sources(graph)
    sources += [Path(info['path']) for info in {**native,**roots}.values()]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'baseline_score':expected(),'starting_configuration':baseline(),
        'weight_axes':active_axes(graph),'retention_axes':retention_axes(graph),
        'expected_scored_records':expected_records(graph),
        'records_formula':'1+18*actual_weight_axes+5*actual_retention_axes+20',
        'waves':list(WAVES),'new_model_training':False,'new_fold_models_trained':0,
        'same_validation':'5635800 rows;1212 continuous days;2020–2024 expanding mature-label OOF',
        'method':'Current complete graph joint weights, both coordinate orders, historical retention, final temporal processing.',
        'axes_recomputed_from_actual_r62_effective_branches':True,
        'cached_earlier_active_weight_axes_not_used_as_authority':True,
        'weight_values':'zero,half,anchor,double,anchor+0.0125,anchor+0.025; clipped[0,0.8]',
        'retention_values':RETENTIONS,'each_adaptive_anchor_frozen_before_its_candidate_scores':True,
        'fixed_model_names_and_other_hyperparameters':True,
        'parallel_candidate_execution':{'workers':4,'ordered_commits':True,'private_official_scoring':True},
        'future_native_model_sources':native,'future_root_model_sources':roots,
        'current_parameter_authority':GRAPH_FIELD,
        'selection_rule':'highest actual complete official connected score; exact ties prefer fewer active model branches',
        'test_labels_read':False,'test_future_prices_used_to_select':False,
        'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'global_resource_exhaustion_established':False,
        'input_sha256':{str(path.resolve()):sha(path) for path in dict.fromkeys(sources)}},immutable=True)

def prefix_controls(ctx,cfg,counts=(80,260,975)):return runtime_controls(ctx,cfg['latest_joint_scheme_graph'],counts)
def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();cfg=baseline();pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    metrics=ctx.score(pred);assert metrics==read(PREVIOUS/'selection.json')['winner']['metrics']
    controls=prefix_controls(ctx,cfg)
    from predict_latest_joint_scheme_20261005 import predict
    record={'winner':{**cfg,'connected_final_score':None},'frozen_sha256':{'active_release.json':sha(ROOT/'active_release.json')}}
    predict(record,candidate_path=OUT/'baseline_future_control',mapping_path=PREVIOUS/'future_return_mapping.json')
    previous_candidate=ROOT/'candidates/optimization_20261003_r62'
    assert sha(OUT/'baseline_future_control/submission.csv')==sha(previous_candidate/'submission.csv')
    dump(OUT/'component_audit.json',{'status':'passed','latest_selected_R62_validation_bit_identical':True,
        'all_eight_official_baseline_metrics_exact':True,'actual_frozen_model_future_csv_byte_identical':True,
        'controls':controls,'models_trained':0,'new_quality_scores':0,'test_labels_read':False,
        'future_control_verification_sha256':sha(OUT/'baseline_future_control/verification.json')},immutable=True)
def evaluate(ctx,cfg):
    assert previous.configuration(cfg)==previous.configuration(baseline())
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.);metrics=ctx.score(pred)
    foundation=read(PREVIOUS/'selection.json')['winner'];log(f'Round63 latest-graph joint candidate:{metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline',**{key:deepcopy(foundation[key]) for key in ('ensemble_weights','top_ensemble_weights','membership_ensemble_weights','role_ensembles_split')},
        'fold_local_pruning_repaired':True,'pruned_member_excluded':True,'connected_final_score':metrics['final_score'],
        'metrics':metrics,'construction':stats,'official_score_cache':deepcopy(ctx.last_official_score_cache),
        'causal_return_mapping':deepcopy(ctx.last_candidate_return_mapping)}
def execute(wave,arms,finish=True):
    from parallel_candidate_scoring_four_20261004 import evaluate_many
    path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    missing=[(key,cfg) for key,cfg in arms if key not in payload['results']]
    for key,row in evaluate_many('optimize_training_round63',missing,OUT):payload['results'][key]=row;dump(path,payload)
    if finish:payload['status']='complete';dump(path,payload)
    return payload
def prior_best(waves):return best([row for wave in waves for row in read(OUT/f'wave{wave}_results.json')['results'].values()])
def weight_at(graph,axis):
    if axis['round']==30:return graph['root']['configuration'][axis['group']][axis['role']]['weight']
    return next(node for node in graph['layers'] if node['round']==axis['round'])['specs'][axis['role']]['weight']
def proposals(cfg,axis):
    anchor=weight_at(cfg['latest_joint_scheme_graph'],axis);values=(0.,anchor*.5,anchor,min(.8,anchor*2),min(.8,anchor+.0125),min(.8,anchor+.025))
    arms=[]
    for index,value in enumerate(values):
        proposal=deepcopy(cfg);proposal['latest_joint_scheme_graph']=with_weight(proposal['latest_joint_scheme_graph'],axis,value,axes())
        arms.append((f'r{axis["round"]}_{axis["group"]}_{axis["role"]}_{index}_w{value:g}',proposal))
    return arms
def independent():
    verify();build();cfg=baseline();arms=[('baseline',cfg)]
    for axis in axes():arms.extend(proposals(cfg,axis))
    execute(261,arms)
def coordinate_pass(wave,earlier,order):
    verify();winner=prior_best(earlier)
    for axis in order:
        path=OUT/f'coordinate_{wave}_r{axis["round"]}_{axis["group"]}_{axis["role"]}.json'
        if path.exists():anchor=read(path)['anchor']
        else:
            anchor=configuration(winner);dump(path,{'anchor':anchor,'axis':axis},immutable=True)
        payload=execute(wave,proposals(anchor,axis),False)
        winner=best([winner]+list(payload['results'].values()))
    execute(wave,[])
def forward():coordinate_pass(262,(261,),axes())
def reverse():coordinate_pass(263,(261,262),list(reversed(axes())))
def retention_refinement():
    verify();winner=prior_best((261,262,263))
    for axis in read(OUT/'protocol.json')['retention_axes']:
        path=OUT/f'retention_r{axis["round"]}_protocol.json'
        if path.exists():anchor=read(path)['anchor']
        else:anchor=configuration(winner);dump(path,{'anchor':anchor,'axis':axis,'values':RETENTIONS},immutable=True)
        arms=[]
        for value in RETENTIONS:
            cfg=deepcopy(anchor);graph=cfg['latest_joint_scheme_graph']
            target=graph['root']['configuration'] if axis['kind']=='root' else next(node for node in graph['layers'] if node['round']==axis['round'])
            target['retention']=value;arms.append((f'r{axis["round"]}_retention{value:g}',cfg))
        payload=execute(264,arms,False);winner=best([winner]+list(payload['results'].values()))
    execute(264,[])
def temporal_refinement():
    verify();winner=prior_best((261,262,263,264));base=configuration(winner);p=base['latest_joint_scheme_graph']['temporal_postprocessing']
    anchor=p if p['mix']>0 and (p['alpha']!=1. or p['power']!=1.) else {'alpha':.995,'mix':.025,'power':1.}
    dump(OUT/'temporal_refinement_protocol.json',{'anchor':anchor,'winner_before_refinement':winner},immutable=True)
    arms=[]
    for index,(offset,mix) in enumerate(itertools.product((-.025,-.005,0.,.005,.025),(0.,anchor['mix']*.5,anchor['mix'],min(1.,anchor['mix']*2)))):
        cfg=deepcopy(base);cfg['latest_joint_scheme_graph']['temporal_postprocessing']={**anchor,'alpha':min(1.,max(.001,anchor['alpha']+offset)),'mix':mix}
        arms.append((f'temporal{index}_da{offset:g}_mix{mix:g}',cfg))
    execute(265,arms)
