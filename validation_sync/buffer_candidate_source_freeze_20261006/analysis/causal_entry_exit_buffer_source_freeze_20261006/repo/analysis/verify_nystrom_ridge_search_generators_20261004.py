"""Execute actual generators with synthetic ties andin-memory scoring adapters."""
from pathlib import Path
from copy import deepcopy
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT)]
import optimize_training_round60 as parent
import optimize_training_round61 as roles
import optimize_training_round62 as pure
from nystrom_ridge_scheme_runtime_20261004 import append_role_layer
from additive_basis_scheme_runtime_20261004 import append_role_layer as earlier_role_layer
from no_dropout_seed_scheme_runtime_20261004 import append_role_layer as prior_role_layer
from neural_interaction_scheme_runtime_20261004 import append_role_layer as preceding_interaction_layer
from neural_width_scheme_runtime_20261004 import append_role_layer as preceding_width_layer
from portfolio_surrogate_scheme_runtime_20261004 import append_role_layer as preceding_portfolio_layer
from verify_whole_scheme_runtime_20261004 import root_graph
OUT=ROOT/'analysis/nystrom_ridge_search_generator_preflight_20261004'


def main():
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    old=roles.read(ROOT/'analysis/optimization_20261003_r29/selection.json')['winner']
    base=deepcopy(old);graph=root_graph(old);graph['temporal_postprocessing']={'alpha':1.,'mix':0.,'power':1.}
    for key in parent.FIELDS:
        if key.endswith('_augmentation'):base.setdefault(key,{role:{'model':'none','weight':0.} for role in roles.ROLES})
        elif key.endswith('_limit_delta'):base.setdefault(key,0.)
    base.setdefault('temporal_postprocessing',deepcopy(graph['temporal_postprocessing']));base['whole_scheme_graph']=graph
    base['basis_role_scheme_graph']=earlier_role_layer(graph)
    base['basis_standalone_scheme_graph']=deepcopy(base['basis_role_scheme_graph'])
    base['no_dropout_role_scheme_graph']=prior_role_layer(base['basis_standalone_scheme_graph'])
    base['no_dropout_standalone_scheme_graph']=deepcopy(base['no_dropout_role_scheme_graph'])
    base['neural_interaction_role_scheme_graph']=preceding_interaction_layer(base['no_dropout_standalone_scheme_graph'])
    base['neural_interaction_standalone_scheme_graph']=deepcopy(base['neural_interaction_role_scheme_graph'])
    base['neural_width_role_scheme_graph']=preceding_width_layer(base['neural_interaction_standalone_scheme_graph'])
    base['neural_width_standalone_scheme_graph']=deepcopy(base['neural_width_role_scheme_graph'])
    base['portfolio_surrogate_role_scheme_graph']=preceding_portfolio_layer(base['neural_width_standalone_scheme_graph'])
    base['portfolio_surrogate_standalone_scheme_graph']=deepcopy(base['portfolio_surrogate_role_scheme_graph'])
    fixture={**parent.configuration(base),'nystrom_ridge_role_scheme_graph':append_role_layer(base['portfolio_surrogate_standalone_scheme_graph'])}
    fixture52={**deepcopy(fixture),'nystrom_ridge_standalone_scheme_graph':deepcopy(fixture['nystrom_ridge_role_scheme_graph'])}
    sources=[Path(__file__),ROOT/'analysis/nystrom_ridge_search_engine_20261004.py',
        ROOT/'analysis/nystrom_ridge_scheme_runtime_20261004.py',ROOT/'analysis/optimize_training_round61.py',
        ROOT/'analysis/optimize_training_round62.py',ROOT/'analysis/run_nystrom_ridge_round_pipeline_20261004.py',
        ROOT/'analysis/optimization_20261003_r29/selection.json']
    inputs={str(p.resolve()):roles.sha(p) for p in sources}
    roles.dump(OUT/'frozen_before_controls.json',{'input_sha256':inputs,
        'scope':'Generator control only; synthetic0 tie scores, in-memory result capsules, noofficial scoring, models orinference.'},immutable=True)
    summaries=[]
    for module,start,expected in ((roles,fixture,[49,8,18,25]),(pure,fixture52,[25,56,17])):
        module.OUT=OUT/f'memory_only_r{module.NUMBER}';module.baseline=lambda cfg=deepcopy(start):deepcopy(cfg)
        original_read=module.read;memory={};events=[]
        def read(path):return deepcopy(memory[str(path)]) if str(path) in memory else original_read(path)
        def dump(path,value,*args,**kwargs):
            if kwargs.get('immutable'):assert str(path) not in memory
            memory[str(path)]=deepcopy(value);events.append({'event':'anchor_saved','path':Path(path).name})
        def execute(wave,arms,finish=True):
            path=module.OUT/f'wave{wave}_results.json';payload=read(path) if str(path) in memory else {'status':'running','results':{}}
            arms=list(arms);assert len({key for key,cfg in arms})==len(arms)
            for key,cfg in arms:
                assert module.previous.configuration(cfg)==module.previous.configuration(start)
                g=module.graph(cfg);assert g['temporal_postprocessing']==graph['temporal_postprocessing']
                if module.NUMBER==61:
                    assert g['root']==start[module.GRAPH_FIELD]['root']
                    assert g['layers'][:-1]==start[module.GRAPH_FIELD]['layers'][:-1]
                    for spec in module.node(cfg)['specs'].values():assert 0<=spec['weight']<=.8
                elif module.pure(cfg):
                    assert g['layers']==[] and g['root']['configuration']['standalone']['model'] in module.MODELS
                if key not in payload['results']:
                    payload['results'][key]={**module.configuration(cfg),'connected_final_score':0.,
                        'synthetic_tie_generator_control_only':True}
            if finish:payload['status']='complete'
            memory[str(path)]=deepcopy(payload);events.append({'event':'scoring_adapter_called','wave':wave,'arms':len(arms)})
            return deepcopy(payload)
        module.read=read;module.dump=dump;module.verify=lambda:None;module.build=lambda:None;module.execute=execute
        module.independent()
        if module.NUMBER==61:module.combinations();module.refine_weights()
        else:module.model_refinement()
        module.refinement()
        actual=[len(memory[str(module.OUT/f'wave{wave}_results.json')]['results']) for wave in module.WAVES]
        assert actual==expected,(module.NUMBER,actual,expected)
        assert all(memory[str(module.OUT/f'wave{wave}_results.json')]['status']=='complete' for wave in module.WAVES)
        if module.NUMBER==61:
            for role in module.ROLES:
                path=f'weight_{role}_protocol.json';saved=next(i for i,e in enumerate(events) if e.get('path')==path)
                assert events[saved+1]['event']=='scoring_adapter_called' and events[saved+1]['wave']==256
        else:
            for name in module.MODELS:
                path=f'model_retention_{name}_protocol.json';saved=next(i for i,e in enumerate(events) if e.get('path')==path)
                assert events[saved+1]['event']=='scoring_adapter_called' and events[saved+1]['wave']==259
        summaries.append({'round':module.NUMBER,'actual_generated_records_per_wave':actual,
            'total':sum(actual),'actual_generator_functions_executed':True,
            'predecessor_configurations_andfinal_temporal_parameters_unchanged':True,
            'each_adaptive_anchor_saved_before_next_scoring_batch':True,'synthetic_scores_only_notquality_evidence':True})
    for path,digest in inputs.items():assert roles.sha(path)==digest,path
    # Use the original writer; mutated adapters exist only in this checker process.
    from train_nystrom_ridge_bank_20261004 import dump as real_dump
    real_dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_generator_controls':summaries,'input_sha256':inputs,
        'new_quality_scores':0,'official_scoring_calls':0,'test_data_read':False,
        'scope':'Actual generators andadaptive control flow under synthetic exact ties. Numerical forecasts, metrics, calibration andfuture inference require the separate actual-data preflight.'},immutable=True)
    print('Actual no-dropout generators verified:100 role and98 standalone records',flush=True)


if __name__=='__main__':main()
