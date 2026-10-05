"""Keep the numerical predictor and package the actual execution entrypoints."""
from pathlib import Path
import hashlib
import json
from predict_factorization_machine_scheme_v4_20261005 import predict as numerical_predict


def copy_actual_sources(ns, candidate):
    candidate = Path(candidate).resolve()
    assert candidate.drive.upper() in ('D:', 'E:')
    assert not (candidate / 'manifest.json').exists(), 'Published candidate is immutable.'
    number = ns.NUMBER
    assert number in (73, 74)
    analysis = ns.ROOT / 'analysis'
    candidate.mkdir(parents=True, exist_ok=True)
    sources = {
        f'optimize_training_round{number}.py': f'optimize_training_round{number}_v4.py',
        f'finalize_training_round{number}.py': f'finalize_training_round{number}_v6.py',
        f'finalize_training_round{number}_v6.py': f'finalize_training_round{number}_v6.py',
        f'run_training_round{number}_v6_pipeline.py': f'run_training_round{number}_v6_pipeline.py',
        'run_factorization_machine_round_v6_20261005.py': 'run_factorization_machine_round_v6_20261005.py',
        Path(__file__).name: Path(__file__).name,
    }
    records = {}
    for destination, source_name in sources.items():
        source = analysis / source_name
        data = source.read_bytes()
        target = candidate / destination
        if target.exists() and target.read_bytes() != data:
            # The inherited predictor copied these historical canonical files.
            # Preserve their bytes explicitly before making the runnable alias current.
            assert destination in (f'optimize_training_round{number}.py', f'finalize_training_round{number}.py')
            old = target.read_bytes()
            assert old == (analysis / destination).read_bytes(), destination
            historical = candidate / 'legacy_review_sources' / destination
            historical.parent.mkdir(exist_ok=True)
            if historical.exists():
                assert historical.read_bytes() == old
            else:
                with historical.open('xb') as stream:
                    stream.write(old)
            target.write_bytes(data)
        elif not target.exists():
            with target.open('xb') as stream:
                stream.write(data)
        assert target.read_bytes() == data
        records[destination] = {'actual_project_source': str(source),
            'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
    record = {'status': 'passed_actual_execution_sources_copied', 'round': number,
        'source_files': records, 'actual_pipeline': f'run_training_round{number}_v6_pipeline.py',
        'actual_driver': 'run_factorization_machine_round_v6_20261005.py',
        'actual_release': f'finalize_training_round{number}_v6.py',
        'actual_experiment': f'optimize_training_round{number}_v4.py',
        'canonical_aliases_use_actual_modules': True,
        'numerical_prediction_delegate': 'predict_factorization_machine_scheme_v4_20261005.py',
        'unchanged_native_models_and_forecast_math': True,
        'reproduction_requires_project_data_and_dependencies': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    encoded = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    path = candidate / 'candidate_source_execution.json'
    if path.exists():
        assert path.read_bytes() == encoded
    else:
        with path.open('xb') as stream:
            stream.write(encoded)
    return record


def predict(ns, record, candidate_path=None, mapping_path=None):
    candidate = Path(candidate_path) if candidate_path is not None else ns.ROOT / f'candidates/optimization_20261003_r{ns.NUMBER}'
    assert not (candidate / 'manifest.json').exists(), 'Published candidate is immutable.'
    numerical_predict(ns, record, candidate_path=candidate, mapping_path=mapping_path)
    copy_actual_sources(ns, candidate)
