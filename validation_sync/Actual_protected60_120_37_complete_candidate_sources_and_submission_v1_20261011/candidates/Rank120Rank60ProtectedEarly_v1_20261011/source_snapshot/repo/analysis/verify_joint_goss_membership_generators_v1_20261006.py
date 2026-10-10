"""Exercise new search coverage and the actual retention branch; no quality scores."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import hashlib
import importlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
OUT=A/'joint_goss_membership_generator_preflight_v1_20261006'

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def create(p,v):
    with Path(p).open('x',encoding='utf-8') as f:
        json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')

def source_paths():
    from predict_joint_goss_membership_scheme_v1_20261006 import source_names
    names=(*source_names(97),'optimize_training_round97.py','finalize_training_round97.py',
        'run_training_round97_pipeline.py','verify_joint_goss_membership_generators_v1_20261006.py',
        'run_joint_goss_quality_qualified_workflow_v1_20261006.py',
        'run_joint_goss_quality_with_exact_rank_cache_v1_20261006.py',
        'lossless_ranking_runtime_adapter_v5_20261006.py','build_lossless_ranking_display_v6_20261006.py',
        'verify_lossless_ranking_display_v7_20261006.py','joint_goss_lossless_publication_adapter_v1_20261006.py',
        'watch_validations_main_v7_20261006.py','role_layer_replay_20261004.py',
        'joint_membership_retention_scope_20261006/planned_round97_v2.json',
        'optimization_20261003_r84/selection.json','optimization_20261003_r95/protocol.json')
    return [A/name for name in dict.fromkeys(names)]+[ROOT/'后续选模标准.md']

def main():
    assert not OUT.exists();OUT.mkdir()
    paths=source_paths();bindings={str(p):sha(p) for p in paths}
    for p in paths:
        if p.suffix=='.py':compile(p.read_text(encoding='utf-8'),str(p),'exec')
    create(OUT/'frozen_before_controls.json',{'status':'frozen_before_generator_and_actual_retention_branch_controls',
        'input_sha256':bindings,'private_synthetic_ordering_is_not_quality':True,
        'R95_final_selection_not_yet_available_no_public_fake_selection_written':True,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
    ns=importlib.import_module('optimize_training_round97_v1')
    seed=ns.previous.baseline()
    assert ns.previous.node(seed)['round']==95
    saved={key:getattr(ns,key) for key in ('read','dump','verify','build','execute','OUT')}
    controls=[]
    for scenario in ('baseline_zero_wins','positive_model_wins','inherited_positive_baseline_wins'):
        parent=deepcopy(seed)
        if scenario=='inherited_positive_baseline_wins':
            for role in ns.ROLES:ns.previous.node(parent)['specs'][role]={'model':ns.MODELS[0],'weight':.025}
        predecessor={'winner':parent}
        parent_rows={}
        for role in ('top','rest'):
            cfg=deepcopy(parent);ns.previous.node(cfg)['specs'][role]={'model':ns.MODELS[1],'weight':.075}
            parent_rows[role]={**cfg,'connected_final_score':.1}
        memory={};protocols={};counts={};generated={}
        ns.OUT=OUT/scenario
        def read(p):
            p=Path(p)
            if p==ns.PREVIOUS/'selection.json':return deepcopy(predecessor)
            if p==ns.PREVIOUS/'wave371_results.json':return {'status':'complete','results':deepcopy(parent_rows),'private_control_fixture':True}
            if p.name in memory:return deepcopy(memory[p.name])
            return saved['read'](p)
        def execute(wave,arms,finish=True):
            payload=memory.setdefault(f'wave{wave}_results.json',{'status':'running','results':{}})
            generated[wave]=deepcopy(arms)
            for key,cfg in arms:
                assert key not in payload['results']
                assert ns.previous.configuration(cfg)==parent
                g=ns.graph(cfg);origin=ns.previous.graph(parent)
                assert g['root']==origin['root']
                assert len(g['layers'])==len(origin['layers'])
                assert [n for n in g['layers'] if n['round']!=95]==[n for n in origin['layers'] if n['round']!=95]
                assert cfg[ns.previous.GRAPH_FIELD]==origin
                if key=='baseline':score=.2 if scenario=='positive_model_wins' else .9
                else:score=.8 if scenario=='positive_model_wins' else .4
                payload['results'][key]={**ns.configuration(cfg),'connected_final_score':score}
                counts[wave]=counts.get(wave,0)+1
            if finish:payload['status']='complete'
            return deepcopy(payload)
        ns.read=read;ns.execute=execute;ns.verify=lambda:None;ns.build=lambda:None
        ns.dump=lambda path,data,**kwargs:protocols.setdefault(Path(path).name,deepcopy(data))
        try:
            ns.independent();ns.combinations();ns.refinement()
            assert [counts[w] for w in ns.WAVES]==[73,24,54]
            assert sum(counts.values())==151
            for wave,arms in generated.items():
                for key,cfg in arms:
                    if key!='baseline':assert ns.node(cfg)['specs']['membership']['weight']>0
                    if wave==379:
                        for role in ('top','rest'):
                            enabled=f'{role}1' in key
                            assert (ns.node(cfg)['specs'][role]['weight']>0)==enabled
            assert len({ns.signature(cfg) for key,cfg in generated[378] if key!='baseline'})==72
            final_models={ns.node(cfg)['specs']['membership']['model'] for key,cfg in generated[380]}
            assert final_models==set(ns.MODELS)
            for model in ns.MODELS:
                pairs={(ns.node(cfg)['retention'],ns.node(cfg)['additional_delta']) for key,cfg in generated[380] if ns.node(cfg)['specs']['membership']['model']==model}
                assert len(pairs)==9
            controls.append({'scenario':scenario,'counts_per_wave':counts,'generated_records':151,
                'positive_membership_for_each_of6_local_anchors':True,
                'disabled_top_rest_cleared_even_when_positive_parent_baseline_wins':True,
                'historical_graph_field_root_and_other_layers_unchanged':True,
                'ordering_values_are_private_synthetic_fixtures_not_official_scores':True})
        finally:
            for key,value in saved.items():setattr(ns,key,value)
    import numpy as np
    from role_layer_replay_20261004 import finish_layer
    size=4650
    base=np.concatenate([np.arange(size,dtype=float),np.arange(size,dtype=float)[::-1]])
    ctx=SimpleNamespace(flags=np.zeros(2*size,dtype=np.int8),valid=np.ones(2*size,dtype=bool),
        dates=np.repeat(np.array([20200102,20200103]),size),codes=np.tile(np.arange(size),2),
        n_codes=size,tie_key=np.tile(np.arange(size),2),
        weights_for=lambda spec:spec['weight'],signal=lambda name:np.tile(np.linspace(.001,.999,size),2))
    zero={role:{'model':'none','weight':0.} for role in ns.ROLES}
    zlo,_=finish_layer(ctx,base,zero,.984,0.,0.)
    zhi,_=finish_layer(ctx,base,zero,.998,0.,0.)
    assert np.array_equal(zlo,base) and np.array_equal(zhi,base)
    positive=deepcopy(zero);positive['membership']={'model':'private_fixture_signal','weight':.025}
    lo,ls=finish_layer(ctx,base,positive,.984,0.,0.)
    hi,hs=finish_layer(ctx,base,positive,.998,0.,0.)
    assert ls['second_retention']==.984 and hs['second_retention']==.998
    assert not np.array_equal(lo,hi)
    actual={'actual_shared_finish_layer_executed':True,'stocks_per_day':size,'days':2,
        'zero_membership_retention_is_noop_confirmed':True,'positive_membership_retention_changes_actual_output':True,
        'low_second_retention':ls['second_retention'],'high_second_retention':hs['second_retention'],
        'low_swaps':ls['construction']['swaps'],'high_swaps':hs['construction']['swaps'],
        'fixture_predictions_are_not_official_quality_and_not_submissions':True}
    for p,digest in bindings.items():assert sha(p)==digest,p
    proof={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':bindings,'controls':controls,'actual_retention_branch_control':actual,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False,
        'actual_parent_replay_full151_quality_full_candidate_causal_and_browser_QA_still_required':True}
    create(OUT/'verification.json',proof)
    print(json.dumps({'status':'passed','controls':controls,'actual_retention_branch_control':actual},ensure_ascii=False),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_generator_control','error':f'{type(exc).__name__}: {exc}'})
        raise
