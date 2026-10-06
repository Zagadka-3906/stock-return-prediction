"""Create correctly numbered FM finalizers without editing frozen v4 sources."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    template = A / 'run_factorization_machine_round_v4_20261005.py'
    driver = template.read_text(encoding='utf-8-sig')
    assert "release = importlib.import_module(f'finalize_training_round{number}')" in driver
    driver = driver.replace("release = importlib.import_module(f'finalize_training_round{number}')",
        "release = importlib.import_module(f'finalize_training_round{number}_v5')\n    assert release.OUT == module.OUT")
    driver = driver.replace('factorization_machine_quality_run_v4_20261005.json', 'factorization_machine_quality_run_v5_20261005.json')
    driver = driver.replace('scope = FrozenProvenanceExecutionScope(module, [Path(__file__), run,',
        "scope = FrozenProvenanceExecutionScope(module, [Path(__file__), run,\n        ROOT / f'analysis/finalize_training_round{number}_v5.py',\n        ROOT / 'analysis/factorization_machine_release_dispatch_preflight_v5_20261005/verification.json',")
    files = {A / 'run_factorization_machine_round_v5_20261005.py': driver}
    for number in (73, 74):
        files[A / f'finalize_training_round{number}_v5.py'] = f'''"""Finalize actual round{number}, preserving the complete FM graph authority."""
from nystrom_ridge_release_engine_20261004 import install
install({number}, globals())

def predict():
    import optimize_training_round{number} as experiment
    from predict_factorization_machine_scheme_v4_20261005 import predict as infer
    assert OUT == experiment.OUT
    assert read(OUT / 'causal_validation.json')['status'] == read(OUT / 'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment, selected())
'''
        files[A / f'run_training_round{number}_v5_pipeline.py'] = f'from run_factorization_machine_round_v5_20261005 import main\nif __name__ == "__main__": main({number})\n'
    for path, source in files.items():
        compile(source, str(path), 'exec')
        with path.open('x', encoding='utf-8', newline='') as stream:
            stream.write(source)
    with (A / 'factorization_machine_release_dispatch_repair_v5_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'new_correctly_numbered_release_sources_created',
            'original_v4_sources_unchanged': True,
            'template_sha256': hashlib.sha256(template.read_bytes()).hexdigest(),
            'generated_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
            'original_canonical_release73_74_dispatches71_72': True,
            'training_and_prediction_math_unchanged': True, 'new_quality_scores': 0}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
