"""Prespecified whole-graph role/standalone searches with isolated official pools."""
from copy import deepcopy
from pathlib import Path
import importlib
import itertools
import json
import os
import time
from linear_leaf_scheme_runtime_20261005 import (
    bank,empty_roles,append_role_layer as original_append_role_layer,standalone_graph as original_standalone_graph,AdaptiveGraphContext,
    all_paths,prepare_raw,native_sources)
from whole_scheme_replay_runtime_20261004 import prefix_controls as graph_controls,raw_sources
from optimize_training_round50 import root_model_sources,state_mapping_path

ROOT=bank.ROOT
ROLES=('membership','top','rest')
WEIGHTS=(.005,.025,.075,.2)
RETENTIONS=(0.,.97,.98,.984,.99)
ALPHAS=(.8,.9,.95)
AUXILIARY=(0.,.25)


def append_role_layer(graph):
    return original_append_role_layer(graph,number=81)


def standalone_graph(graph,name,postprocessing,retention=.98,delta=.075):
    return original_standalone_graph(graph,name,postprocessing,retention,delta,number=82)


def install(number,namespace):
    assert number in (81,82)
    parent_number=66 if number==81 else 81
    previous=importlib.import_module(f'optimize_training_round{parent_number}')
    class Bindings:pass
    ns=Bindings();ns.__dict__=namespace
    namespace.update(ROOT=ROOT,OUT=ROOT/f'analysis/optimization_20261003_r{number}',
        PREVIOUS=ROOT/f'analysis/optimization_20261003_r{parent_number}',previous=previous,trainer=bank,
        MODELS=tuple(bank.CONFIGS),NEW_MODELS=tuple(bank.CONFIGS) if number==81 else (),
        GRAPH_FIELD='linear_leaf_role_scheme_graph' if number==81 else 'linear_leaf_standalone_scheme_graph',
        WAVES=(325,326,327,328) if number==81 else (329,330,331),
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
        cfg[ns.GRAPH_FIELD]=append_role_layer(origin) if number==81 else deepcopy(origin)
        return cfg
    def expected():return ns.read(ns.PREVIOUS/'selection.json')['winner']['connected_final_score']
    def signature(cfg):return json.dumps(configuration(cfg),sort_keys=True,separators=(',',':'))
    def best(rows):
        def model_cost(name):
            cfg=bank.all_configs.get(name,{})
            return len(cfg['members']) if cfg.get('kind')=='neural_ensemble' else 1
        def complexity(row):
            g=graph(row);root=g['root'];cfg=root['configuration']
            count=model_cost(cfg['standalone']['model']) if cfg.get('standalone') else 5
            return count+sum(model_cost(spec['model']) for node in g['layers'] for spec in node['specs'].values() if spec['weight']>0)
        return min(rows,key=lambda row:(-row['connected_final_score'],complexity(row),signature(row)))
    def node(cfg):return next(item for item in graph(cfg)['layers'] if item['round']==81)
    def pure(cfg):return graph(cfg)['root']['kind']=='standalone' and graph(cfg)['root']['round']==82
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
        proof=ROOT/'analysis/linear_leaf_preflight_20261005/verification.json'
        assert ns.read(proof)['status']=='passed_actual_linear_leaf_maturity_native_reload_and_prefix_controls'
        gates=[bank.OUT/'oof_audit.json',ROOT/'analysis/linear_leaf_future_qa_20261005/verification.json',
            ROOT/'analysis/reference66_linear_leaf_generator_preflight_v2_20261005/verification.json']
        for path in gates:assert ns.read(path)['status']=='passed',path
        sources=[Path(__file__),ROOT/'analysis/linear_leaf_scheme_runtime_20261005.py',
            ROOT/'analysis/explicit_parent_release_engine_v2_20261005.py',ROOT/'analysis/predict_reference66_linear_leaf_scheme_v2_20261005.py',
            ROOT/'analysis/check_reference66_linear_leaf_scheme_v2_20261005.py',ROOT/f'analysis/optimize_training_round{number}_v2.py',
            ROOT/f'analysis/finalize_training_round{number}_v2.py',ROOT/f'analysis/run_training_round{number}_v2_pipeline.py',
            ROOT/'analysis/run_nystrom_ridge_round_pipeline_20261004.py',
            ROOT/'analysis/whole_scheme_replay_runtime_20261004.py',ROOT/'analysis/whole_scheme_future_runtime_20261004.py',
            ROOT/'analysis/role_layer_replay_20261004.py',ROOT/'analysis/nystrom_ridge_model_sources_20261004.py',
            ROOT/'analysis/parallel_candidate_scoring_one_20261005.py',ROOT/'analysis/finalize_training_round7.py',
            ROOT/'analysis/finalize_optimization.py',ROOT/'analysis/score_calibrated_candidates_20261003.py',
            ROOT/'analysis/nystrom_ridge_complete_output_search_plan_20261004.json',
            ROOT/'analysis/verify_nystrom_ridge_search_generators_20261004.py',
            ROOT/'analysis/linear_leaf_model_sources_20261005.py',
            ROOT/'analysis/agreement_gated_weights_20261005.py',
            ROOT/'analysis/nystrom_future_codec_adapter_20261005.py',ROOT/'analysis/linear_leaf_future_codec_adapter_20261005.py',
            ROOT/'analysis/run_reference66_linear_leaf_round_v2_20261005.py',
            ROOT/'analysis/verify_reference66_linear_leaf_generators_v2_20261005.py',
            ROOT/'analysis/reference66_linear_leaf_complete_plan_20261005.json',
            bank.OUT/'protocol.json',ROOT/'后续选模标准.md',ROOT/'active_release.json',state_mapping_path(),
            ns.PREVIOUS/'protocol.json',ns.PREVIOUS/'selection.json',ns.PREVIOUS/'selected_validation.npy',
            ROOT/f'candidates/optimization_20261003_r{parent_number}/verification.json',
            ROOT/f'candidates/optimization_20261003_r{parent_number}/manifest.json',proof,*gates]
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
            'explicit_parent_round':parent_number,'independent_comparison_branch':True,'starting_configuration':cfg,'baseline_score':ns.expected(),'expected_scored_records':124 if number==81 else 138,
            'wave_arm_counts':[73,8,18,25] if number==81 else [37,84,17],
            'model_names':ns.MODELS,'new_model_training':False,'new_fold_models_trained':0,
            'previous_linear_leaf_bank_actual_annual_fits':30,'new_native_model_configurations':6,'same_validation':'5635800 rows;1212 continuous days;2020–2024 expanding mature-label OOF',
            'role_grid':{'roles':ROLES,'weights':WEIGHTS,'new_layer_floor':.98,'refined_floors':RETENTIONS,'additional_shifts':(-.04,-.02,0.,.02,.04)},
            'standalone_grid':{'alphas':ALPHAS,'auxiliary':AUXILIARY,'bonus':.3,'model_alpha_offsets':(-.025,0.,.025),'model_bonus_values':(0.,.15,.3),'retentions':RETENTIONS},
            'historical_graph_parameters_preserved':True,'new_role_before_frozen_final_temporal_transform':True,'inherited_agreement_gates_replayed_in_validation_andfuture':True,'actual_component_checks_before_quality_required':True,
            'standalone_discards_predecessor_root_andall_role_layers':True,
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
            for role in ROLES if number==81 else ('standalone',):
                case=deepcopy(cfg)
                if number==81:node(case)['specs'][role]={'model':name,'weight':.025}
                else:case=standalone_cfg(name)
                controls.append({'model':name,'role':role,**prefix_controls(ctx,case,counts=(80,260))})
        from predict_reference66_linear_leaf_scheme_v2_20261005 import predict
        record={'winner':{**cfg,'connected_final_score':None},'frozen_sha256':{'active_release.json':ns.sha(ROOT/'active_release.json')}}
        predict(ns,record,candidate_path=ns.OUT/'baseline_future_control',mapping_path=ns.PREVIOUS/'future_return_mapping.json')
        assert ns.sha(ns.OUT/'baseline_future_control/submission.csv')==ns.sha(ROOT/f'candidates/optimization_20261003_r{parent_number}/submission.csv')
        changed=deepcopy(cfg)
        if number==81:node(changed)['specs']['rest']={'model':ns.MODELS[0],'weight':.025}
        else:changed=standalone_cfg(ns.MODELS[0])
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
        ns.log(f'Round{number} matched constant andlinear leaf complete graph:{metrics["final_score"]:.9f}')
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
        ns.verify();ns.build();base=ns.baseline();arms=[('baseline',base)]
        if number==81:
            for name,role,weight in itertools.product(ns.MODELS,ROLES,WEIGHTS):
                cfg=deepcopy(base);node(cfg)['specs'][role]={'model':name,'weight':weight};arms.append((f'{name}_{role}_w{weight:g}',cfg))
        else:arms.extend((f'{name}_a{a:g}_aux{w:g}',standalone_cfg(name,a,w)) for name,a,w in itertools.product(ns.MODELS,ALPHAS,AUXILIARY))
        ns.execute(ns.WAVES[0],arms)
    namespace.update(graph=graph,configuration=configuration,baseline=baseline,expected=expected,signature=signature,best=best,
        node=node,pure=pure,standalone_cfg=standalone_cfg,native_sources=native,Context=Context,verify=verify,freeze=freeze,
        prefix_controls=prefix_controls,build=build,evaluate=evaluate,execute=execute,prior_best=prior_best,independent=independent)
    install_refinement(ns,number)


def install_refinement(ns,number):
    def combinations():
        rows=ns.read(ns.OUT/'wave325_results.json')['results'];base=ns.baseline();winners={}
        for role in ROLES:
            candidates=[row for row in rows.values() if ns.node(row)['specs'][role]['weight']>0]
            winners[role]=deepcopy(ns.node(ns.best(candidates))['specs'][role])
        ns.dump(ns.OUT/'combination_protocol.json',{'prespecified_best_single_role_choices':winners},immutable=True)
        arms=[]
        for bits in itertools.product((0,1),repeat=3):
            cfg=deepcopy(base)
            for role,on in zip(ROLES,bits):
                if on:ns.node(cfg)['specs'][role]=deepcopy(winners[role])
            arms.append((''.join(map(str,bits)),cfg))
        ns.execute(326,arms)
    def refine_weights():
        winner=ns.prior_best((325,326))
        for role in ROLES:
            path=ns.OUT/f'weight_{role}_protocol.json'
            if path.exists():anchor=ns.read(path)['anchor']
            else:anchor=ns.configuration(winner);ns.dump(path,{'anchor':anchor},immutable=True)
            old=ns.node(anchor)['specs'][role];fallback=ns.node(ns.best(row for row in ns.read(ns.OUT/'wave325_results.json')['results'].values() if ns.node(row)['specs'][role]['weight']>0))['specs'][role]
            spec=old if old['weight']>0 else fallback;weight=spec['weight']
            values=(0.,weight*.5,weight,min(.8,weight*2),min(.8,weight+.0125),min(.8,weight+.025));arms=[]
            for index,value in enumerate(values):
                cfg=deepcopy(anchor);ns.node(cfg)['specs'][role]={'model':spec['model'],'weight':value};arms.append((f'{role}_{index}_w{value:g}',cfg))
            result=ns.execute(327,arms,False);winner=ns.best([winner,*result['results'].values()])
        ns.execute(327,[])
    def refinement():
        if number==81:
            winner=ns.prior_best((325,326,327));anchor=ns.configuration(winner)
            ns.dump(ns.OUT/'refinement_protocol.json',{'anchor':anchor,'winner':winner},immutable=True);arms=[]
            for retention,delta in itertools.product(RETENTIONS,(-.04,-.02,0.,.02,.04)):
                cfg=deepcopy(anchor);ns.node(cfg).update(retention=retention,additional_delta=delta);arms.append((f'r{retention:g}_d{delta:g}',cfg))
            ns.execute(328,arms);return
        winner=ns.prior_best((329,330));base=ns.configuration(winner)
        ns.dump(ns.OUT/'refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
        if not ns.pure(base):ns.execute(331,[(f'unchanged_baseline_{i}',deepcopy(base)) for i in range(17)]);return
        for key,values in (('retention',RETENTIONS),('limit_up_delta',(.055,.075,.095))):
            anchor=deepcopy(base);ns.dump(ns.OUT/f'final_{key}_protocol.json',{'anchor':anchor,'values':values},immutable=True);arms=[]
            for value in values:
                cfg=deepcopy(anchor);ns.graph(cfg)['root']['configuration'][key]=value;arms.append((f'{key}_{value:g}',cfg))
            payload=ns.execute(331,arms,False);winner=ns.best([winner,*payload['results'].values()]);base=ns.configuration(winner)
        for key,offsets in (('weight',(-.125,0.,.125)),('alpha',(-.0125,0.,.0125)),('bonus',(-.05,0.,.05))):
            anchor=deepcopy(base);ns.dump(ns.OUT/f'final_{key}_protocol.json',{'anchor':anchor,'offsets':offsets},immutable=True);value=ns.graph(anchor)['root']['configuration']['standalone']['postprocessing'][key];arms=[]
            for index,offset in enumerate(offsets):
                cfg=deepcopy(anchor);post=ns.graph(cfg)['root']['configuration']['standalone']['postprocessing'];post[key]=min(.995 if key=='alpha' else 1.,max(0.,value+offset));arms.append((f'{key}_{index}',cfg))
            payload=ns.execute(331,arms,False);winner=ns.best([winner,*payload['results'].values()]);base=ns.configuration(winner)
        ns.execute(331,[])
    def model_refinement():
        rows=ns.read(ns.OUT/'wave329_results.json')['results'];anchors={name:ns.configuration(ns.best(row for row in rows.values() if ns.pure(row) and ns.graph(row)['root']['configuration']['standalone']['model']==name)) for name in ns.MODELS}
        ns.dump(ns.OUT/'model_refinement_protocol.json',{'anchors':anchors,'retentions':RETENTIONS},immutable=True)
        for name,cfg in anchors.items():
            post=ns.graph(cfg)['root']['configuration']['standalone']['postprocessing'];arms=[]
            for offset,bonus in itertools.product((-.025,0.,.025),(0.,.15,.3)):
                candidate=deepcopy(cfg);ns.graph(candidate)['root']['configuration']['standalone']['postprocessing'].update(alpha=min(.995,max(0.,post['alpha']+offset)),bonus=bonus);arms.append((f'{name}_a{offset:g}_b{bonus:g}',candidate))
            payload=ns.execute(330,arms,False);path=ns.OUT/f'model_retention_{name}_protocol.json'
            if path.exists():local=ns.read(path)['anchor']
            else:
                local=ns.configuration(ns.best([ns.best(row for row in rows.values() if ns.pure(row) and ns.graph(row)['root']['configuration']['standalone']['model']==name),*[row for row in payload['results'].values() if ns.graph(row)['root']['configuration']['standalone']['model']==name]]))
                ns.dump(path,{'anchor':local,'values':RETENTIONS},immutable=True)
            arms=[]
            for value in RETENTIONS:
                candidate=deepcopy(local);ns.graph(candidate)['root']['configuration']['retention']=value;arms.append((f'{name}_retention{value:g}',candidate))
            ns.execute(330,arms,False)
        ns.execute(330,[])
    ns.__dict__.update(combinations=combinations,refine_weights=refine_weights,refinement=refinement,model_refinement=model_refinement)
