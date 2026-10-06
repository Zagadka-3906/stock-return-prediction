"""Exercise actual publication imports, closure identity and candidate source bytes."""
from pathlib import Path
import hashlib
import importlib
import json
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    from run_factorization_machine_round_v6_20261005 import bind_round_modules
    from predict_factorization_machine_scheme_v5_20261005 import copy_actual_sources, numerical_predict
    from predict_factorization_machine_scheme_v4_20261005 import predict as existing_predict
    assert numerical_predict is existing_predict
    import publish_training_round as publication
    out = A / 'factorization_machine_candidate_source_preflight_v6_20261005'
    assert not out.exists()
    out.mkdir()
    controls = []
    sources = {Path(__file__), A / 'prepare_factorization_candidate_sources_v6_20261005.py',
        A / 'predict_factorization_machine_scheme_v5_20261005.py',
        A / 'predict_factorization_machine_scheme_v4_20261005.py',
        A / 'run_factorization_machine_round_v5_20261005.py',
        A / 'run_factorization_machine_round_v6_20261005.py',
        A / 'publish_training_round.py', A / 'nystrom_ridge_release_engine_20261004.py'}
    for number in (73, 74):
        experiment, release = bind_round_modules(number)
        assert publication.importlib.import_module(f'optimize_training_round{number}') is experiment
        assert publication.importlib.import_module(f'finalize_training_round{number}') is release
        assert release.OUT == experiment.OUT == A / f'optimization_20261003_r{number}'
        for name in ('selected', 'select', 'calibrate'):
            assert experiment in [cell.cell_contents for cell in getattr(release, name).__closure__]
        assert release.ReleaseContext.__bases__ == (experiment.Context,)
        assert release.selected in [cell.cell_contents for cell in release.ReleaseContext.__init__.__closure__]
        candidate = out / f'packaged_source_control_r{number}'
        candidate.mkdir()
        # Reproduce precisely the historical copies made by the numeric delegate.
        for stem in ('optimize_training_round', 'finalize_training_round'):
            name = f'{stem}{number}.py'
            (candidate / name).write_bytes((A / name).read_bytes())
            sources.add(A / name)
        ns = SimpleNamespace(ROOT=ROOT, NUMBER=number)
        record = copy_actual_sources(ns, candidate)
        assert copy_actual_sources(ns, candidate) == record
        for destination, item in record['source_files'].items():
            assert sha(candidate / destination) == item['sha256'] == sha(item['actual_project_source'])
            sources.add(Path(item['actual_project_source']))
        assert (candidate / 'legacy_review_sources' / f'finalize_training_round{number}.py').read_bytes() == (A / f'finalize_training_round{number}.py').read_bytes()
        saved = {p.relative_to(candidate).as_posix(): sha(p) for p in candidate.rglob('*') if p.is_file()}
        (candidate / 'manifest.json').write_text('{}', encoding='utf-8')
        try:
            copy_actual_sources(ns, candidate)
        except AssertionError as error:
            assert 'immutable' in str(error)
        else:
            raise AssertionError('A sealed candidate must reject source changes.')
        assert all(sha(candidate / name) == digest for name, digest in saved.items())
        controls.append({'round': number, 'actual_publication_canonical_import_identity': True,
            'actual_release_output_and_closures_correct': True, 'actual_copied_source_sha256': saved,
            'idempotent_before_publication': True, 'sealed_candidate_rejected_without_changes': True,
            'inherited_numeric_predictor_function_identity': True, 'forecast_inference_not_run_by_this_control': True})
    generator = json.loads((A / 'factorization_machine_search_generator_preflight_v4_20261005/verification.json').read_text(encoding='utf-8'))
    assert [row['generated_records'] for row in generator['controls']] == [124, 138, 138]
    for path, expected in generator['source_sha256'].items():
        assert sha(path) == expected
    sources.add(A / 'factorization_machine_search_generator_preflight_v4_20261005/verification.json')
    with (out / 'verification.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_actual_publication_import_and_candidate_source_controls',
            'controls': controls, 'source_sha256': {str(p): sha(p) for p in sorted(sources)},
            'planned_official_records_unchanged': {'73': 124, '74': 138},
            'original_frozen_sources_preserved': True, 'new_model_fits': 0,
            'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print('FM73/74 actual publication imports and candidate source controls passed', flush=True)


if __name__ == '__main__':
    main()
