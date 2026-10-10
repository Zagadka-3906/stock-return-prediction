"""Execute driver bindings, copied-source sealing and actual saved classifier dispatch."""
from pathlib import Path
from types import SimpleNamespace
import ast
import hashlib
import importlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'ready_classifier_reference_execution_preflight_20261005'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    from predict_ready_classifier_reference_scheme_20261005 import copy_sources, source_names
    import train_streaming_rank_classifier_bank_v3_20261005 as bank
    annual = A / 'streaming_classifier_actual_annual_completion_audit_20261005/verification.json'
    assert bank.read(annual)['actual_annual_fits'] == 20
    sources = [Path(__file__), A / 'ready_classifier_reference_complete_plan_20261005.json',
        A / 'ready_classifier_reference_generator_preflight_20261005/verification.json', annual,
        A / 'streaming_rank_classifier_direct_router_preflight_20261005/verification.json',
        bank.OUT / 'oof_audit.json', bank.OUT / 'training_execution_scope.json']
    sources += list(dict.fromkeys(A / name for n in (85, 86) for name in source_names(n)))
    sources += [bank.OUT / name / f'{prefix}_2020.{suffix}' for name in bank.CONFIGS
        for prefix, suffix in (('model', 'joblib'), ('info', 'json'))]
    bindings = {str(path): sha(path) for path in sources}
    for path in sources:
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    OUT.mkdir()
    create(OUT / 'frozen_before_controls.json', {'source_sha256': bindings,
        'actual_unqualified_parent_baseline_not_called': True, 'test_labels_read': False})
    tree = ast.parse((A / 'run_ready_classifier_reference_round_20261005.py').read_text(encoding='utf-8'))
    body = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'main').body
    nodes = [node for node in body if isinstance(node, ast.Assign) and (
        any(isinstance(t, ast.Name) and t.id in ('module', 'release') for t in node.targets)
        or any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Attribute) and t.value.attr == 'modules' for t in node.targets))]
    assert len(nodes) == 4
    actual = ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[]))
    cases = []
    for number in (85, 86):
        env = {'number': number, 'sys': sys, 'importlib': importlib}
        exec(compile(actual, str(A / 'run_ready_classifier_reference_round_20261005.py'), 'exec'), env)
        module, release = env['module'], env['release']
        assert module.PREVIOUS_NUMBER == number - 1
        assert sys.modules[f'optimize_training_round{number}'] is module
        assert sys.modules[f'finalize_training_round{number}'] is release
        assert release.PREVIOUS == module.PREVIOUS and issubclass(release.ReleaseContext, module.Context)
        assert release.select.__code__.co_filename.endswith('explicit_parent_release_engine_v2_20261005.py')
        assert module.execute.__code__.co_filename.endswith('ready_classifier_reference_search_engine_20261005.py')
        assert len(module.MODELS) == 4 and all(cfg['kind'] == 'streaming_rank_classifier' for cfg in module.trainer.CONFIGS.values())
        assert module.previous.__file__.endswith(f'optimize_training_round{number-1}_v2.py')
        ns = SimpleNamespace(ROOT=ROOT, NUMBER=number)
        candidate = OUT / f'candidate{number}'
        copy_sources(ns, candidate)
        expected = {name: sha(A / name) for name in source_names(number)}
        assert {name: sha(candidate / name) for name in expected} == expected
        for prefix in ('optimize_training_round', 'finalize_training_round'):
            (candidate / f'{prefix}{number}.py').write_bytes((A / f'{prefix}{number}.py').read_bytes())
        copy_sources(ns, candidate)
        for prefix in ('optimize_training_round', 'finalize_training_round'):
            assert sha(candidate / f'{prefix}{number}.py') == sha(A / f'{prefix}{number}_v2.py')
        for parent in (81, 82, 83, 84):
            assert sha(candidate / f'optimize_training_round{parent}.py') == sha(A / f'optimize_training_round{parent}_v2.py')
        before = {p.name: sha(p) for p in candidate.glob('*.py')}
        copy_sources(ns, candidate)
        assert before == {p.name: sha(p) for p in candidate.glob('*.py')}
        create(candidate / 'manifest.json', {'status': 'sealed_source_control'})
        try:
            copy_sources(ns, candidate)
        except AssertionError:
            pass
        else:
            raise AssertionError('Sealed candidate was edited')
        assert before == {p.name: sha(p) for p in candidate.glob('*.py')}
        cases.append({'round': number, 'explicit_parent_round': number-1,
            'actual_driver_binding_statements_executed': 4,
            'all4_existing_full_annual_classifier_configurations': True,
            'previous_factory_actual_V2_selected': True,
            'all_candidate_sources_and_effective_canonical_aliases_SHA_checked': True,
            'source_copy_idempotence_and_sealed_write_rejection': True})
    import numpy as np
    import streaming_rank_classifier_future_codec_adapter_20261005 as adapter
    import fourier_tuning_model_sources_20261004 as legacy
    original = legacy.predict_arrays
    restore = adapter.install()
    route_checks = []
    try:
        assert legacy.predict_arrays.__code__.co_filename.endswith('streaming_rank_classifier_future_codec_adapter_20261005.py')
        for name in bank.CONFIGS:
            source = bank.OUT / name / 'model_2020.joblib'
            copied = OUT / f'copied_{name}_model2020.joblib'
            shutil.copyfile(source, copied)
            assert sha(source) == sha(copied)
            bundle = bank.core.load_bundle(copied)
            x = np.random.default_rng(20261005).standard_normal((131, 63)).astype(np.float32)
            x[1, 0], x[2, 1], x[3, 2] = np.nan, np.inf, -np.inf
            direct = bank.core.predict_arrays(bundle, x)
            hooked = legacy.predict_arrays(bundle, x)
            assert np.array_equal(direct, hooked) and np.isfinite(hooked).all()
            for size in (1, 80, 130):
                assert np.array_equal(hooked[:size], legacy.predict_arrays(bundle, x[:size]))
            route_checks.append({'model': name, 'real_full2020_model_sha256': sha(source),
                'actual_copied_model131_rows_and1_80_130_prefix_bit_identical': True,
                'feature_values_are_synthetic_dispatch_controls_not_full_future': True})
            assert copied.resolve().is_relative_to(OUT.resolve())
            copied.unlink()
    finally:
        restore()
    assert legacy.predict_arrays is original
    for path, digest in bindings.items():
        assert sha(path) == digest, path
    value = {'status': 'passed', 'source_sha256': bindings, 'controls': cases,
        'actual_saved_full_annual_classifier_dispatch_checks': route_checks,
        'actual_native_dispatch_install_and_restore_checked': True,
        'actual20_annual_fits_independently_verified': True,
        'all4_actual_final_fits_full_future_reload_and_cold80_still_required_before_quality': True,
        'R84_and_R85_actual_qualification_required_before_quality': True,
        'actual_parent_baseline_full_reproduction_and_complete_future_controls_still_pending': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', value)
    print(json.dumps({'status': 'passed_actual_classifier_driver_sources_and_saved_model_dispatch_controls',
        'rounds': [85, 86], 'actual_full_annual_models_dispatched': 4}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
