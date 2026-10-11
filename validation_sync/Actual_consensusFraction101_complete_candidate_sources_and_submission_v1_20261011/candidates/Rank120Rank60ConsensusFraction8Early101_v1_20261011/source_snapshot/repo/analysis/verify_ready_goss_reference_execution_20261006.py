"""Execute the FM drivers and verify their actual canonical and copied sources."""
from pathlib import Path
from types import SimpleNamespace
import ast
import hashlib
import importlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
OUT=A/'ready_goss_reference_execution_preflight_20261006'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    from predict_ready_goss_reference_scheme_20261006 import copy_sources,source_names
    sources=[Path(__file__),A/'ready_goss_reference_complete_plan_20261006.json',
        A/'ready_goss_reference_generator_preflight_20261006/verification.json',
        A/'gradient_sampling_direct_router_preflight_20261005/verification.json',
        A/'gradient_sampling_future_qa_20261005/verification.json',
        A/'gradient_sampling_scheme_runtime_20261005.py',A/'gradient_sampling_model_sources_20261005.py',
        A/'predict_gradient_sampling_scheme_codec_20261005.py',A/'gradient_sampling_future_codec_adapter_20261005.py']
    sources += list(dict.fromkeys(A/name for n in (95,96) for name in source_names(n)))
    bindings={str(path):sha(path) for path in sources}
    for path in sources:
        if path.suffix=='.py':compile(path.read_text(encoding='utf-8'),str(path),'exec')
    OUT.mkdir()
    create(OUT/'frozen_before_controls.json',{'source_sha256':bindings,'test_labels_read':False,
        'factory_and_driver_only_actual_unqualified_parent_baseline_not_called':True})
    tree=ast.parse((A/'run_ready_goss_reference_round_20261006.py').read_text(encoding='utf-8'))
    body=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='main').body
    nodes=[node for node in body if isinstance(node,ast.Assign) and (
        any(isinstance(t,ast.Name) and t.id in ('module','release') for t in node.targets)
        or any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Attribute) and t.value.attr=='modules' for t in node.targets))]
    assert len(nodes)==4
    actual=ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]))
    cases=[]
    for number in (95,96):
        env={'number':number,'sys':sys,'importlib':importlib}
        exec(compile(actual,str(A/'run_ready_goss_reference_round_20261006.py'),'exec'),env)
        module,release=env['module'],env['release']
        assert module.PREVIOUS_NUMBER==(84 if number==95 else 95)
        assert sys.modules[f'optimize_training_round{number}'] is module
        assert sys.modules[f'finalize_training_round{number}'] is release
        assert release.PREVIOUS==module.PREVIOUS and issubclass(release.ReleaseContext,module.Context)
        assert release.select.__code__.co_filename.endswith('explicit_parent_release_engine_v2_20261005.py')
        assert module.execute.__code__.co_filename.endswith('ready_goss_reference_search_engine_20261006.py')
        assert len(module.MODELS)==6 and all(cfg['kind']=='lightgbm_gradient_sampling' for cfg in module.trainer.CONFIGS.values())
        assert module.previous.__file__.endswith(f'optimize_training_round{84 if number==95 else 95}_v2.py')
        ns=SimpleNamespace(ROOT=ROOT,NUMBER=number)
        candidate=OUT/f'candidate{number}'
        copy_sources(ns,candidate)
        expected={name:sha(A/name) for name in source_names(number)}
        assert {name:sha(candidate/name) for name in expected}==expected
        for prefix in ('optimize_training_round','finalize_training_round'):
            (candidate/f'{prefix}{number}.py').write_bytes((A/f'{prefix}{number}.py').read_bytes())
        copy_sources(ns,candidate)
        for prefix in ('optimize_training_round','finalize_training_round'):
            assert sha(candidate/f'{prefix}{number}.py')==sha(A/f'{prefix}{number}_v2.py')
        assert sha(candidate/'optimize_training_round84.py')==sha(A/'optimize_training_round84_v2.py')
        before={p.name:sha(p) for p in candidate.glob('*.py')}
        copy_sources(ns,candidate)
        assert before=={p.name:sha(p) for p in candidate.glob('*.py')}
        create(candidate/'manifest.json',{'status':'sealed_source_control'})
        try:copy_sources(ns,candidate)
        except AssertionError:pass
        else:raise AssertionError('Sealed candidate was edited')
        assert before=={p.name:sha(p) for p in candidate.glob('*.py')}
        cases.append({'round':number,'explicit_parent_round':84 if number==95 else 95,'actual_driver_binding_statements_executed':4,
            'native_kind':'lightgbm_gradient_sampling','actual6_existing_full_model_configurations':True,
            'previous_factory_actual_V2_selected':True,'all_candidate_sources_and_effective_canonical_aliases_SHA_checked':True,
            'legacy_copy_recovery_idempotence_and_sealed_write_rejection':True})
    import gradient_sampling_future_codec_adapter_20261005 as adapter
    import fourier_tuning_model_sources_20261004 as legacy
    original=legacy.predict_arrays
    restore=adapter.install()
    try:
        assert legacy.predict_arrays.__code__.co_filename.endswith('gradient_sampling_future_codec_adapter_20261005.py')
    finally:restore()
    assert legacy.predict_arrays is original
    for path,digest in bindings.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed','source_sha256':bindings,'controls':cases,
        'actual_GOSS_native_dispatch_install_and_restore_checked':True,
        'existing_actual_full_native_future_and_direct_router_controls_required':True,
        'R84_and_R95_actual_qualification_required_before_quality':True,
        'actual_parent_baseline_full_reproduction_and_complete_future_controls_still_pending':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'status':'passed_actual_GOSS_driver_source_and_dispatch_controls','controls':cases},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
