"""Check actual robust drivers, source copies and saved small native typed dispatch."""
from pathlib import Path
from types import SimpleNamespace
import ast
import hashlib
import importlib
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'ready_robust_reference_execution_preflight_20261005'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    assert not OUT.exists()
    from predict_ready_robust_reference_scheme_20261005 import copy_sources, source_names
    import train_streaming_robust_regression_bank_20261005 as bank
    import streaming_robust_regression_model_sources_20261005 as router
    preflight = A / 'streaming_robust_regression_preflight_20261005'
    proof = bank.read(preflight / 'verification.json')
    assert proof['actual_small32pass_fits'] == 16 and proof['actual_full_annual_fits'] == 0
    sources = [Path(__file__), A / 'ready_robust_reference_complete_plan_20261005.json',
        A / 'ready_robust_reference_generator_preflight_20261005/verification.json', preflight / 'verification.json',
        Path(router.__file__), A / 'streaming_robust_regression_future_codec_adapter_20261005.py',
        A / 'streaming_rank_classifier_direct_router_preflight_20261005/verification.json']
    sources += list(dict.fromkeys(A / name for number in (87, 88) for name in source_names(number)))
    sources += [preflight / f'{name}_4096row32pass.joblib' for name in bank.CONFIGS]
    bindings = {str(path): sha(path) for path in sources}
    OUT.mkdir()
    create(OUT / 'frozen_before_controls.json', {'source_sha256': bindings,
        'only_actual_saved4096row_models_used_for_dispatch_not_full_fit_qualification': True,
        'actual_unqualified_parent_baseline_not_called': True, 'test_labels_read': False})
    tree = ast.parse((A / 'run_ready_robust_reference_round_20261005.py').read_text(encoding='utf-8'))
    body = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main').body
    nodes = [n for n in body if isinstance(n, ast.Assign) and (
        any(isinstance(t, ast.Name) and t.id in ('module', 'release') for t in n.targets)
        or any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Attribute)
               and t.value.attr == 'modules' for t in n.targets))]
    assert len(nodes) == 4
    actual = ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[]))
    cases = []
    for number in (87, 88):
        env = {'number': number, 'sys': sys, 'importlib': importlib}
        exec(compile(actual, str(A / 'run_ready_robust_reference_round_20261005.py'), 'exec'), env)
        module, release = env['module'], env['release']
        assert module.PREVIOUS_NUMBER == number - 1
        assert sys.modules[f'optimize_training_round{number}'] is module
        assert sys.modules[f'finalize_training_round{number}'] is release
        assert release.PREVIOUS == module.PREVIOUS and issubclass(release.ReleaseContext, module.Context)
        assert release.select.__code__.co_filename.endswith('explicit_parent_release_engine_v2_20261005.py')
        assert module.execute.__code__.co_filename.endswith('ready_robust_reference_search_engine_20261005.py')
        assert len(module.MODELS) == 4
        assert all(cfg['kind'] == 'streaming_robust_regression' for cfg in module.trainer.CONFIGS.values())
        candidate = OUT / f'candidate{number}'
        ns = SimpleNamespace(ROOT=ROOT, NUMBER=number)
        copy_sources(ns, candidate)
        before = {p.name: sha(p) for p in candidate.glob('*.py')}
        for name in source_names(number):
            assert sha(candidate / name) == sha(A / name), name
        for parent in (81, 82, 83, 84, 85, 86, number):
            assert sha(candidate / f'optimize_training_round{parent}.py') == sha(A / f'optimize_training_round{parent}_v2.py')
        copy_sources(ns, candidate)
        assert before == {p.name: sha(p) for p in candidate.glob('*.py')}
        create(candidate / 'manifest.json', {'status': 'sealed_source_control'})
        try:
            copy_sources(ns, candidate)
        except AssertionError:
            pass
        else:
            raise AssertionError('A sealed candidate was edited.')
        cases.append({'round': number, 'explicit_parent_round': number - 1,
            'actual_driver_binding_statements_executed': 4,
            'candidate_source_and_canonical_alias_SHA_verified': True,
            'copy_idempotence_and_sealed_write_rejection': True})
    assert router.CONFIGS == {**router.previous.CONFIGS, **bank.CONFIGS}
    for name in router.previous.CONFIGS:
        assert router.source_dir(name) == router.previous.source_dir(name)
    import fourier_tuning_model_sources_20261004 as legacy
    from streaming_robust_regression_future_codec_adapter_20261005 import install
    original, checks = legacy.predict_arrays, []
    restore = install()
    try:
        x = np.random.default_rng(20261005).normal(size=(131, 63)).astype(np.float32)
        x[1, 0], x[2, 1], x[3, 2] = np.nan, np.inf, -np.inf
        for name in bank.CONFIGS:
            source = preflight / f'{name}_4096row32pass.joblib'
            bundle = bank.core.load_bundle(source)
            direct = bank.core.predict_arrays(bundle, x)
            assert np.array_equal(direct, router.predict_arrays(bundle, x))
            assert np.array_equal(direct, legacy.predict_arrays(bundle, x))
            for size in (1, 80, 130):
                assert np.array_equal(direct[:size], legacy.predict_arrays(bundle, x[:size]))
            checks.append({'model': name, 'saved_actual4096row_model_sha256': sha(source),
                'direct_and_future_codec131_rows_and_prefixes_bit_identical': True})
        inherited = A / 'streaming_rank_classification_preflight_v3_20261005'
        for name in router.previous.NEW_CONFIGS:
            bundle = bank.core.load_bundle(inherited / f'{name}_4096row32epoch.joblib')
            assert np.array_equal(router.previous.predict_arrays(bundle, x), router.predict_arrays(bundle, x))
            assert np.array_equal(router.previous.predict_arrays(bundle, x), legacy.predict_arrays(bundle, x))
    finally:
        restore()
    assert legacy.predict_arrays is original
    assert all(sha(path) == digest for path, digest in bindings.items())
    route = {'status': 'passed', 'source_sha256': bindings, 'controls': checks,
        'all_inherited_configurations_and_source_paths_preserved': len(router.previous.CONFIGS),
        'all4_inherited_classifier_native_routes_bit_identical': True,
        'actual_install_and_restore_checked': True, 'new_quality_scores': 0, 'test_labels_read': False}
    create(A / 'streaming_robust_regression_direct_router_preflight_20261005/verification.json', route)
    create(OUT / 'verification.json', {'status': 'passed', 'source_sha256': bindings, 'controls': cases,
        'actual_saved_small_native_dispatch_controls': checks,
        'all20_fullannual4_final_fits_and_fullfuture_QA_still_required_before_quality': True,
        'actual_qualified_R86_and_R87_required_before_quality': True,
        'new_full_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_actual_robust_drivers_copies_sealing_and_native_dispatch',
                      'rounds': [87, 88], 'full_fits_by_controls': 0}), flush=True)


if __name__ == '__main__':
    main()
