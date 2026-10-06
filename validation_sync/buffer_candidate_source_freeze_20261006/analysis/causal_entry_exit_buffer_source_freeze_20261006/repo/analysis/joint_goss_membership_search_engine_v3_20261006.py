"""Prespecified whole-graph role/standalone searches with isolated official pools."""
from copy import deepcopy
from pathlib import Path
import importlib
import itertools
import json
import os
import time
from gradient_sampling_scheme_runtime_20261005 import (
    bank,empty_roles,append_role_layer as original_append_role_layer,standalone_graph as original_standalone_graph,AdaptiveGraphContext,
    all_paths,prepare_raw,native_sources)
from whole_scheme_replay_runtime_20261004 import prefix_controls as graph_controls,raw_sources
from optimize_training_round50 import root_model_sources,state_mapping_path

import joint_goss_membership_retention_grid_v2_20261006 as grid

ROOT=bank.ROOT
ROLES=('membership','top','rest')
WEIGHTS=(.005,.025,.075,.2)
RETENTIONS=(0.,.97,.98,.984,.99)
ALPHAS=(.8,.9,.95)
AUXILIARY=(0.,.25)


def append_role_layer(graph):
    return original_append_role_layer(graph,number=95)


def standalone_graph(graph,name,postprocessing,retention=.98,delta=.075):
    return original_standalone_graph(graph,name,postprocessing,retention,delta,number=96)


def install(number,namespace):
    assert number == 97
    parent_number=95
    previous=importlib.import_module('optimize_training_round95_v3')
    class Bindings:pass
    ns=Bindings();ns.__dict__=namespace
    namespace.update(ROOT=ROOT,OUT=ROOT/f'analysis/optimization_20261003_r{number}',
        PREVIOUS=ROOT/f'analysis/optimization_20261003_r{parent_number}',previous=previous,trainer=bank,
        MODELS=tuple(bank.CONFIGS),NEW_MODELS=tuple(bank.CONFIGS),
        GRAPH_FIELD='gradient_sampling_joint_membership_scheme_graph',
        WAVES=(378,379,380),
        NUMBER=number,PREVIOUS_NUMBER=parent_number,ROLES=ROLES,WEIGHTS=WEIGHTS,RETENTIONS=RETENTIONS,
        read=bank.read,dump=bank.dump,sha=bank.sha,log=bank.log,
        root_model_sources=root_model_sources,state_mapping_path=state_mapping_path,
        future_native_sources=native_sources)
    for key in ('HERE','YEARS','KEYS','BASE_POST','ARCHIVE','RANKERS','weights_from_name'):
        namespace[key]=getattr(previous,key)
    namespace['FIELDS']=previous.FIELDS+(namespace['GRAPH_FIELD'],)
    def graph(cfg):return cfg[ns.GRAPH_FIELD]
    def configuration(row):return {key:deepcopy(row[key]) for key in ns.FIELDS}
    def baseline():
        winner=ns.read(ns.PREVIOUS/'selection.json')['winner'];cfg=previous.configuration(winner)
        origin=winner[previous.GRAPH_FIELD]
        cfg[ns.GRAPH_FIELD]=deepcopy(origin)
        return cfg
    def expected():return ns.read(ns.PREVIOUS/'selection.json')['winner']['connected_final_score']
    def signature(cfg):return json.dumps(configuration(cfg),sort_keys=True,separators=(',',':'))
    def best(rows):
        def model_cost(name):
            cfg=bank.all_configs.get(name,{})
            return len(cfg['members']) if cfg.get('kind') in ('neural_ensemble','linear_leaf_ensemble') else 1
        def complexity(row):
            g=graph(row);root=g['root'];cfg=root['configuration']
            count=model_cost(cfg['standalone']['model']) if cfg.get('standalone') else 5
            return count+sum(model_cost(spec['model']) for node in g['layers'] for spec in node['specs'].values() if spec['weight']>0)
        return min(rows,key=lambda row:(-row['connected_final_score'],complexity(row),signature(row)))
    def node(cfg):return next(item for item in graph(cfg)['layers'] if item['round']==95)
    def pure(cfg):return False
    def standalone_cfg(name,alpha=.9,aux=.25,bonus=.3):
        cfg=ns.baseline();cfg[ns.GRAPH_FIELD]=standalone_graph(graph(cfg),name,
            dict(ns.BASE_POST,alpha=alpha,weight=aux,bonus=bonus));return cfg
    def native(cfg):return native_sources(graph(cfg))
    class Context(AdaptiveGraphContext):
        def __init__(self,fixture=None,scoring=None,paths=None):
            cfg=fixture if fixture is not None else ns.baseline()
            scoring=Path(scoring) if scoring is not None else ns.OUT/'scoring_validation_only'
            scoring.mkdir(exist_ok=True)
            for name in ('测试集_X.csv','测试集_Y.csv'):
                if not (scoring/name).exists():os.link(ns.PREVIOUS/'scoring_validation_only'/name,scoring/name)
            super().__init__(graph(cfg),scoring=scoring,paths=paths or all_paths(graph(cfg),ns.OUT))
            self.configure(cfg)
        def configure(self,cfg):
            if ns.GRAPH_FIELD in cfg:
                self._basis_cfg=configuration(cfg);cfg={'whole_scheme_graph':graph(cfg)}
            return super().configure(cfg)
    def verify():
        protocol=ns.read(ns.OUT/'protocol.json')
        for path,digest in protocol['input_sha256'].items():assert ns.sha(path)==digest,path
        return protocol
    def freeze():
        if (ns.OUT/'protocol.json').exists():verify();return
        from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
        assert complete_round_evidence(parent_number) is not None
        ns.OUT.mkdir(exist_ok=True);cfg=ns.baseline()
        proof=ROOT/'analysis/gradient_sampling_preflight_20261005/verification.json'
        assert ns.read(proof)['status']=='passed_actual_gradient_sampling_maturity_native_reload_and_prefix_controls'
        gates=[bank.OUT/'oof_audit.json',ROOT/'analysis/gradient_sampling_future_qa_20261005/verification.json',
            ROOT/'analysis/joint_goss_membership_generator_preflight_v3_20261006/verification.json',ROOT/'analysis/gradient_sampling_direct_router_preflight_20261005/verification.json',ROOT/'analysis/gradient_sampling_memmap_native_promotion_20261006/verification.json',ROOT/'analysis/ready_goss_reference_execution_preflight_v2_20261006/verification.json']
        for path in gates:assert ns.read(path)['status']=='passed',path
        sources=[ROOT/'analysis/gradient_sampling_memmap_complete_bank_v3_github_20261006/receipt.json',Path(__file__),ROOT/'analysis/gradient_sampling_scheme_runtime_20261005.py',
            ROOT/'analysis/joint_goss_membership_release_engine_v3_20261006.py',ROOT/'analysis/predict_joint_goss_membership_scheme_v3_20261006.py',
            ROOT/'analysis/check_joint_goss_membership_scheme_v3_20261006.py',ROOT/f'analysis/optimize_training_round{number}_v3.py',
            ROOT/f'analysis/finalize_training_round{number}_v3.py',ROOT/f'analysis/run_training_round{number}_v3_pipeline.py',
            ROOT/'analysis/run_nystrom_ridge_round_pipeline_20261004.py',
            ROOT/'analysis/whole_scheme_replay_runtime_20261004.py',ROOT/'analysis/whole_scheme_future_runtime_20261004.py',
            ROOT/'analysis/role_layer_replay_20261004.py',ROOT/'analysis/nystrom_ridge_model_sources_20261004.py',
            ROOT/'analysis/parallel_candidate_scoring_one_20261005.py',ROOT/'analysis/finalize_training_round7.py',
            ROOT/'analysis/finalize_optimization.py',ROOT/'analysis/score_calibrated_candidates_20261003.py',
            ROOT/'analysis/nystrom_ridge_complete_output_search_plan_20261004.json',
            ROOT/'analysis/verify_nystrom_ridge_search_generators_20261004.py',
            ROOT/'analysis/gradient_sampling_model_sources_20261005.py',
            ROOT/'analysis/agreement_gated_weights_20261005.py',
            ROOT/'analysis/nystrom_future_codec_adapter_20261005.py',ROOT/'analysis/gradient_sampling_future_codec_adapter_20261005.py',ROOT/'analysis/linear_leaf_ensemble_future_codec_adapter_20261005.py',ROOT/'analysis/linear_leaf_future_codec_adapter_20261005.py',ROOT/'analysis/predict_gradient_sampling_scheme_codec_20261005.py',
            ROOT/'analysis/run_joint_goss_membership_round_v3_20261006.py',
            ROOT/'analysis/verify_joint_goss_membership_generators_v3_20261006.py',
            ROOT/'analysis/joint_membership_retention_scope_20261006/planned_round97_v4.json',
            bank.OUT/'protocol.json',ROOT/'后续选模标准.md',ROOT/'active_release.json',state_mapping_path(),
            ns.PREVIOUS/'protocol.json',ns.PREVIOUS/'selection.json',ns.PREVIOUS/'selected_validation.npy',
            ROOT/f'candidates/optimization_20261003_r{parent_number}/verification.json',
            ROOT/f'candidates/optimization_20261003_r{parent_number}/manifest.json',proof,*gates]
        sources += [ROOT/'analysis/joint_goss_membership_retention_grid_v2_20261006.py',ns.PREVIOUS/'wave371_results.json',ROOT/'analysis/joint_membership_retention_scope_20261006/verification.json']
        sources += [Path(path) for path in ns.read(ns.PREVIOUS/'protocol.json')['input_sha256']]
        sources += [Path(path) for path in ns.read(bank.OUT/'protocol.json')['input_sha256']]
        sources += list(bank.OUT.glob('*/info_202[0-4].json'))+list(bank.OUT.glob('*/model_202[0-4].joblib'))+list(bank.OUT.glob('*/raw_202[0-4].parquet'))
        sources += [Path(bank.native.__file__),bank.native.SOURCE]
        native_universe=native(cfg)
        for name in bank.CONFIGS:
            g=standalone_graph(graph(cfg),name,dict(ns.BASE_POST,alpha=.9,weight=.25,bonus=.3))
            native_universe.update(native_sources(g))
        roots=root_model_sources(graph(cfg));sources += [Path(info['path']) for info in {**native_universe,**roots}.values()]
        for values in raw_sources(graph(cfg)).values():sources.extend(path for path in values if path.exists())
        ns.dump(ns.OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'explicit_parent_round':parent_number,'independent_comparison_branch':True,'starting_configuration':cfg,'baseline_score':ns.expected(),'expected_scored_records':151,
            'wave_arm_counts':[73,24,54],
            'model_names':ns.MODELS,'new_model_training':False,'new_fold_models_trained':0,
            'previous_gradient_sampling_bank_actual_annual_fits':30,'new_native_model_configurations':0,'existing_native_configurations_reused':6,'same_validation':'5635800 rows;1212 continuous days;2020–2024 expanding mature-label OOF',
            'role_grid':{'roles':ROLES,'membership_weights':grid.WEIGHTS,'first_retentions':grid.RETENTIONS,'final_retentions':grid.FINAL_RETENTIONS,'additional_shifts':grid.DELTAS,'all_local_membership_anchors_positive':True},
            'refinement_target':'Existing GOSS layer95 through new authoritative graph field; historical95 field unchanged',
            'historical_graph_parameters_preserved':True,'new_role_before_frozen_final_temporal_transform':True,'inherited_agreement_gates_replayed_in_validation_andfuture':True,'actual_component_checks_before_quality_required':True,
            'parent_root_and_all_other_role_layers_preserved':True,
            'each_adaptive_coordinate_anchor_frozen_before_scoring':True,
            'parallel_candidate_execution':{'workers':1,'ordered_commits':True,'private_official_scoring':True},
            'future_native_model_sources':native_universe,'future_root_model_sources':roots,
            'selection_rule':'Highest actual official continuous complete-output S; exact ties prefer fewer active model branches',
            'current_parameter_authority':ns.GRAPH_FIELD,'test_labels_read':False,'test_future_prices_used_to_select':False,
            'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
            'global_resource_exhaustion_established':False,
            'input_sha256':{str(path.resolve()):ns.sha(path) for path in dict.fromkeys(sources)}},immutable=True)
    def prefix_controls(ctx,cfg,counts=(80,260,975)):
        return graph_controls(ctx,graph(cfg),counts)
    def build():
        import numpy as np
        verify()
        if (ns.OUT/'component_audit.json').exists():
            for path,digest in ns.read(ns.OUT/'component_audit.json')['output_sha256'].items():assert ns.sha(path)==digest,path
            return
        paths=prepare_raw(ns.OUT);ctx=Context();cfg=ns.baseline()
        pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.);assert np.array_equal(pred,np.load(ns.PREVIOUS/'selected_validation.npy'))
        assert ctx.score(pred)==ns.read(ns.PREVIOUS/'selection.json')['winner']['metrics']
        controls=[prefix_controls(ctx,cfg)]
        for name in ns.MODELS:
            for role in ROLES:
                case=deepcopy(cfg)
                node(case)['specs']['membership']={'model':name,'weight':.005}
                node(case)['specs'][role]={'model':name,'weight':.025}
                node(case)['retention']=.995
                controls.append({'model':name,'role':role,**prefix_controls(ctx,case,counts=(80,260))})
        from predict_joint_goss_membership_scheme_v3_20261006 import predict
        record={'winner':{**cfg,'connected_final_score':None},'frozen_sha256':{'active_release.json':ns.sha(ROOT/'active_release.json')}}
        predict(ns,record,candidate_path=ns.OUT/'baseline_future_control',mapping_path=ns.PREVIOUS/'future_return_mapping.json')
        assert ns.sha(ns.OUT/'baseline_future_control/submission.csv')==ns.sha(ROOT/f'candidates/optimization_20261003_r{parent_number}/submission.csv')
        changed=deepcopy(cfg)
        node(changed)['specs']['membership']={'model':ns.MODELS[0],'weight':.025}
        node(changed)['retention']=.998
        record={'winner':{**changed,'connected_final_score':None},'frozen_sha256':{'active_release.json':ns.sha(ROOT/'active_release.json')}}
        predict(ns,record,candidate_path=ns.OUT/'changed_future_control',mapping_path=ns.PREVIOUS/'future_return_mapping.json')
        ns.dump(ns.OUT/'component_audit.json',{'status':'passed','actual_previous_complete_validation_bit_identical':True,
            'all8_previous_official_metrics_exact':True,'actual_previous_future_csv_byte_identical':True,
            'all6_new_native_models_cold_prefix_andpoisoning_controls':controls,'models_trained':0,'test_labels_read':False,
            'actual_changed_complete_future_CSV_andcold80_controls_passed':True,
            'output_sha256':{str(path.resolve()):ns.sha(path) for path in paths.values()}},immutable=True)
    def evaluate(ctx,cfg):
        assert previous.configuration(cfg)==previous.configuration(ns.baseline())
        ctx._whole_signal_cache.clear();ctx._whole_regime_cache.clear();ctx.configure(cfg)
        pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.);metrics=ctx.score(pred)
        parent=ns.read(ns.PREVIOUS/'selection.json')['winner']
        ns.log(f'Round{number} matched GOSS complete graph:{metrics["final_score"]:.9f}')
        extra={key:deepcopy(parent[key]) for key in ('ensemble_weights','top_ensemble_weights','membership_ensemble_weights','role_ensembles_split')}
        if pure(cfg):
            members={graph(cfg)['root']['configuration']['standalone']['model']:1.}
            extra.update(ensemble_weights=members,top_ensemble_weights=members,membership_ensemble_weights=members,role_ensembles_split=False)
        return {**configuration(cfg),'donor':'baseline',**extra,'fold_local_pruning_repaired':True,'pruned_member_excluded':True,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats,
            'official_score_cache':deepcopy(ctx.last_official_score_cache),'causal_return_mapping':deepcopy(ctx.last_candidate_return_mapping)}
    def execute(wave,arms,finish=True):
        from parallel_candidate_scoring_one_20261005 import evaluate_many
        path=ns.OUT/f'wave{wave}_results.json';payload=ns.read(path) if path.exists() else {'status':'running','results':{}}
        missing=[(key,cfg) for key,cfg in arms if key not in payload['results']]
        for key,row in evaluate_many(ns.__name__,missing,ns.OUT):payload['results'][key]=row;ns.dump(path,payload)
        if finish:payload['status']='complete';ns.dump(path,payload)
        return payload
    def prior_best(waves):return best([row for wave in waves for row in ns.read(ns.OUT/f'wave{wave}_results.json')['results'].values()])
    def independent():
        ns.verify();ns.build()
        ns.execute(ns.WAVES[0],grid.initial_arms(ns))
    namespace.update(graph=graph,configuration=configuration,baseline=baseline,expected=expected,signature=signature,best=best,
        node=node,pure=pure,standalone_cfg=standalone_cfg,native_sources=native,Context=Context,verify=verify,freeze=freeze,
        prefix_controls=prefix_controls,build=build,evaluate=evaluate,execute=execute,prior_best=prior_best,independent=independent)
    install_joint_refinement(ns)


def install_joint_refinement(ns):
    def combinations():
        first=ns.read(ns.OUT/f'wave{ns.WAVES[0]}_results.json')
        assert first['status']=='complete'
        prior=ns.read(ns.PREVIOUS/'wave371_results.json')
        assert prior['status']=='complete'
        top_rest={}
        for role in ('top','rest'):
            candidates=[r for r in prior['results'].values() if ns.previous.node(r)['specs'][role]['weight']>0]
            top_rest[role]=deepcopy(ns.previous.node(ns.previous.best(candidates))['specs'][role])
        rows=list(first['results'].values())
        anchors={name:grid.local_positive_anchor(ns,rows,name) for name in ns.MODELS}
        ns.dump(ns.OUT/'combination_protocol.json',{'model_local_positive_membership_anchors':anchors,'top_rest_from_completed_R95_wave371':top_rest},immutable=True)
        ns.execute(ns.WAVES[1],grid.combination_arms(ns,rows,top_rest))
    def refinement():
        rows=[]
        for wave in ns.WAVES[:2]:
            payload=ns.read(ns.OUT/f'wave{wave}_results.json');assert payload['status']=='complete'
            rows.extend(payload['results'].values())
        anchors={name:grid.local_positive_anchor(ns,rows,name) for name in ns.MODELS}
        ns.dump(ns.OUT/'refinement_protocol.json',{'model_local_positive_membership_anchors':anchors,'retentions':grid.FINAL_RETENTIONS,'additional_deltas':grid.DELTAS},immutable=True)
        ns.execute(ns.WAVES[2],grid.final_arms(ns,rows))
    ns.__dict__.update(combinations=combinations,refinement=refinement)
