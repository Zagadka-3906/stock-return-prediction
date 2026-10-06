"""Execute actual driver bindings and copied embedded consensus dispatch."""
from pathlib import Path
from types import SimpleNamespace
import ast
import hashlib
import importlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'ready_classifier_consensus_reference_execution_preflight_v2_20261006'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    import numpy as np
    from predict_ready_classifier_consensus_reference_scheme_v2_20261006 import copy_sources, source_names
    import build_classifier_consensus_bank_20261005 as bank
    import classifier_consensus_model_sources_20261005 as router
    preflight = A / 'classifier_consensus_preflight_20261005'
    assert bank.read(preflight / 'verification.json')['actual12_saved_composite_controls'] == 12
    sources = [Path(__file__), A / 'ready_classifier_consensus_reference_complete_plan_v2_20261006.json',
        A / 'ready_classifier_consensus_reference_generator_preflight_v2_20261006/verification.json',
        preflight / 'verification.json', A / 'classifier_consensus_direct_router_preflight_20261005/verification.json']
    sources += list(dict.fromkeys(A / name for number in (89, 90) for name in source_names(number)))
    sources += [preflight / f'{name}_2020.joblib' for name in bank.CONFIGS]
    bindings = {str(path): sha(path) for path in sources}
    OUT.mkdir()
    create(OUT / 'frozen_before_controls.json', {'source_sha256': bindings,
        'actual_full32pass_parent_estimators_embedded_in_saved_composites': True,
        'prediction_controls_not_substitute_for_fullfuture_or_quality': True,
        'test_labels_read': False, 'new_native_fits': 0})
    driver = A / 'run_ready_classifier_consensus_reference_round_v2_20261006.py'
    body = next(n for n in ast.parse(driver.read_text(encoding='utf-8')).body
                if isinstance(n, ast.FunctionDef) and n.name == 'main').body
    nodes = [n for n in body if isinstance(n, ast.Assign) and (
        any(isinstance(t, ast.Name) and t.id in ('module', 'release') for t in n.targets)
        or any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Attribute)
               and t.value.attr == 'modules' for t in n.targets))]
    assert len(nodes) == 4
    actual = ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[]))
    controls = []
    for number in (89, 90):
        env = {'number': number, 'sys': sys, 'importlib': importlib}
        exec(compile(actual, str(driver), 'exec'), env)
        module, release = env['module'], env['release']
        assert module.PREVIOUS_NUMBER == number - 1
        assert sys.modules[f'optimize_training_round{number}'] is module
        assert sys.modules[f'finalize_training_round{number}'] is release
        assert release.PREVIOUS == module.PREVIOUS and issubclass(release.ReleaseContext, module.Context)
        assert len(module.MODELS) == 6
        assert module.WAVES == ((353, 354, 355, 356) if number == 89 else (357, 358, 359))
        candidate = OUT / f'candidate{number}'
        copy_sources(SimpleNamespace(ROOT=ROOT, NUMBER=number), candidate)
        before = {p.name: sha(p) for p in candidate.glob('*.py')}
        for name in source_names(number):
            assert sha(candidate / name) == sha(A / name)
        for parent in (*range(81, 90), number):
            assert sha(candidate / f'optimize_training_round{parent}.py') == sha(A / f'optimize_training_round{parent}_{"v3" if parent>=89 else "v2"}.py')
        copy_sources(SimpleNamespace(ROOT=ROOT, NUMBER=number), candidate)
        assert before == {p.name: sha(p) for p in candidate.glob('*.py')}
        create(candidate / 'manifest.json', {'status': 'sealed_source_control'})
        try:
            copy_sources(SimpleNamespace(ROOT=ROOT, NUMBER=number), candidate)
        except AssertionError:
            pass
        else:
            raise AssertionError('A sealed candidate was edited.')
        controls.append({'round': number, 'explicit_parent_round': number - 1,
            'actual_driver_binding_statements_executed': 4,
            'all_copied_sources_and_canonical_alias_sha_verified': True,
            'source_copy_idempotence_and_sealed_write_rejection': True})
    for name in router.previous.CONFIGS:
        assert router.source_dir(name) == router.previous.source_dir(name)
    import fourier_tuning_model_sources_20261004 as legacy
    from classifier_consensus_future_codec_adapter_20261005 import install
    original, route_checks = legacy.predict_arrays, []
    restore = install()
    try:
        x = np.random.default_rng(20261006).normal(size=(131, 63)).astype(np.float32)
        x[1, 0], x[2, 1], x[3, 2] = np.nan, np.inf, -np.inf
        for name in bank.CONFIGS:
            model = preflight / f'{name}_2020.joblib'
            bundle = bank.parent.core.load_bundle(model)
            direct = bank.predict_arrays(bundle, x)
            assert np.array_equal(direct, router.predict_arrays(bundle, x))
            assert np.array_equal(direct, legacy.predict_arrays(bundle, x))
            for size in (1, 80, 130):
                assert np.array_equal(direct[:size], legacy.predict_arrays(bundle, x[:size]))
            route_checks.append({'model': name, 'actual_saved_embedded_composite_sha256': sha(model),
                                 'actual_nonfinite_features_and_prefix_routes_bit_identical': True})
    finally:
        restore()
    assert legacy.predict_arrays is original
    assert all(sha(path) == digest for path, digest in bindings.items())
    create(OUT / 'verification.json', {'status': 'passed', 'source_sha256': bindings,
        'driver_controls': controls, 'actual_saved_composite_routes': route_checks,
        'all_inherited_configurations_and_paths_preserved': len(router.previous.CONFIGS),
        'actual_R88_R89_scoped_completion_and_fullfuture_required_before_quality': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_actual_consensus_quality_bindings_copies_and_dispatch',
                      'rounds': [89, 90]}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
