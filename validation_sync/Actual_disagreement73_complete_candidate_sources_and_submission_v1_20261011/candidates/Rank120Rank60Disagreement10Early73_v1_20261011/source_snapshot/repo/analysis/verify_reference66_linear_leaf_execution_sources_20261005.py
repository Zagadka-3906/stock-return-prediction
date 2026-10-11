"""Execute real driver bindings, verify packaged sources, and audit queued-round gaps."""
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy
import ast
import hashlib
import importlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
OUT=A/'reference66_linear_leaf_execution_preflight_20261005'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(path,record):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(record,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    from qualified_round_inventory_20261005 import assess
    fixtures=[(n,{'winner':{'connected_final_score':float(n)}}) for n in range(22,67)]
    fixtures.append((81,{'winner':{'connected_final_score':65.}}))
    gaps=assess(fixtures,range(22,83),[*range(22,67),81,82])
    assert gaps['active_round']==67 and gaps['last_contiguous_registered_completed_round']==66
    assert gaps['pending_rounds']==[*range(67,81),82] and gaps['best_round']==66
    assert gaps['published_rounds_pending_scoped_completion']==[82]
    from predict_reference66_linear_leaf_scheme_v2_20261005 import copy_sources,source_names
    sources=[Path(__file__),A/'reference66_linear_leaf_complete_plan_20261005.json',
        A/'reference66_linear_leaf_generator_preflight_v2_20261005/verification.json',
        A/'qualified_round_inventory_20261005.py',A/'refresh_continuous_progress_v2_20261005.py',
        A/'monitor_actual_optimization_progress_v15_20261005.py',A/'refresh_optimization_boundary_evidence_v14_20261005.py']
    sources += list(dict.fromkeys(A/name for n in (81,82) for name in source_names(n)))
    bindings={str(path):sha(path) for path in sources}
    for path in sources:
        if path.suffix=='.py':compile(path.read_text(encoding='utf-8'),str(path),'exec')
    OUT.mkdir()
    create(OUT/'frozen_before_controls.json',{'source_sha256':bindings,'new_quality_scores':0,'test_labels_read':False})
    tree=ast.parse((A/'run_reference66_linear_leaf_round_v2_20261005.py').read_text(encoding='utf-8'))
    body=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='main').body
    assignments=[node for node in body if isinstance(node,ast.Assign) and (
        any(isinstance(t,ast.Name) and t.id in ('module','release') for t in node.targets)
        or any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Attribute) and t.value.attr=='modules' for t in node.targets))]
    assert len(assignments)==4
    actual=ast.fix_missing_locations(ast.Module(body=assignments,type_ignores=[]))
    cases=[]
    for number in (81,82):
        env={'number':number,'sys':sys,'importlib':importlib}
        exec(compile(actual,str(A/'run_reference66_linear_leaf_round_v2_20261005.py'),'exec'),env)
        module,release=env['module'],env['release']
        assert sys.modules[f'optimize_training_round{number}'] is module
        assert sys.modules[f'finalize_training_round{number}'] is release
        assert module.PREVIOUS_NUMBER==(66 if number==81 else 81)
        assert release.PREVIOUS==module.PREVIOUS and issubclass(release.ReleaseContext,module.Context)
        assert module.execute.__code__.co_filename.endswith('linear_leaf_reference66_search_engine_v2_20261005.py')
        assert release.select.__code__.co_filename.endswith('explicit_parent_release_engine_v2_20261005.py')
        if number==81:
            cfg=module.baseline();reference=module.read(module.PREVIOUS/'selection.json')['winner'][module.previous.GRAPH_FIELD]
            assert module.graph(cfg)['root']==reference['root'] and module.graph(cfg)['layers'][:-1]==reference['layers']
            assert module.node(cfg)['round']==81 and all(v['weight']==0 for v in module.node(cfg)['specs'].values())
            for name in module.MODELS:
                graph=module.graph(module.standalone_cfg(name))
                assert graph['root']['round']==82 and not graph['layers']
        candidate=OUT/f'candidate{number}'
        ns=SimpleNamespace(ROOT=ROOT,NUMBER=number)
        copy_sources(ns,candidate)
        expected={name:sha(A/name) for name in source_names(number)}
        assert {name:sha(candidate/name) for name in expected}==expected
        # Execute the source recovery actually used after the legacy codec copies
        # canonical names. No prediction or synthetic quality score is produced.
        for prefix in ('optimize_training_round','finalize_training_round'):
            (candidate/f'{prefix}{number}.py').write_bytes((A/f'{prefix}{number}.py').read_bytes())
        copy_sources(ns,candidate)
        for prefix in ('optimize_training_round','finalize_training_round'):
            assert sha(candidate/f'{prefix}{number}.py')==sha(A/f'{prefix}{number}_v2.py')
        before={p.name:sha(p) for p in candidate.glob('*.py')}
        copy_sources(ns,candidate)
        assert before=={p.name:sha(p) for p in candidate.glob('*.py')}
        create(candidate/'manifest.json',{'status':'sealed_for_mutation_control'})
        try:copy_sources(ns,candidate)
        except AssertionError:pass
        else:raise AssertionError('Sealed source overwrite accepted')
        assert before=={p.name:sha(p) for p in candidate.glob('*.py')}
        cases.append({'round':number,'explicit_parent_round':module.PREVIOUS_NUMBER,
            'actual_driver_binding_statements_executed':4,'candidate_sources_and_canonical_aliases_sha256_checked':True,
            'legacy_overwrite_recovery_and_idempotence_and_sealed_candidate_rejection':True})
    original=ast.parse((A/'parallel_candidate_scoring_four_20261004.py').read_text(encoding='utf-8'))
    single=ast.parse((A/'parallel_candidate_scoring_one_20261005.py').read_text(encoding='utf-8'))
    funcs=lambda tree:{n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
    assert funcs(original)==funcs(single)
    for path,digest in bindings.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed','source_sha256':bindings,'controls':cases,
        'single_worker_initializer_evaluate_many_and_shutdown_actual_AST_identical_to_existing_four_worker':True,
        'actual_gap_inventory_control':{k:v for k,v in gaps.items() if k!='best_result'},
        'old67_through80_not_inferred_complete_when81_is_complete':True,'best_score_selected_across_all_qualified_rounds':True,
        'full_5635800_validation_and1599600_future_controls_still_required':True,
        'all_generator_ordering_values_are_synthetic_not_official_scores':True,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'status':'passed_actual_driver_source_packaging_and_pending_gap_controls','controls':cases},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
