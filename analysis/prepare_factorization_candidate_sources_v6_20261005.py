"""Version the pending FM execution and candidate packaging without changing grids."""
from pathlib import Path
import hashlib
import json

A = Path(__file__).resolve().parent


def create(path, text):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)


def main():
    source = (A / 'run_factorization_machine_round_v5_20261005.py').read_text(encoding='utf-8')
    source = source.replace('factorization_machine_quality_run_v5_', 'factorization_machine_quality_run_v6_')
    source = source.replace('predict_factorization_machine_scheme_v4_', 'predict_factorization_machine_scheme_v5_')
    source = source.replace('finalize_training_round{number}_v5.py', 'finalize_training_round{number}_v6.py')
    old = "    module = importlib.import_module(f'optimize_training_round{number}_v4')\n    sys.modules[f'optimize_training_round{number}'] = module\n    release = importlib.import_module(f'finalize_training_round{number}_v5')\n    assert release.OUT == module.OUT\n"
    assert source.count(old) == 1
    source = source.replace(old, '    module, release = bind_round_modules(number)\n')
    helper = "\ndef bind_round_modules(number):\n    assert number in (73, 74)\n    module = importlib.import_module(f'optimize_training_round{number}_v4')\n    sys.modules[f'optimize_training_round{number}'] = module\n    release = importlib.import_module(f'finalize_training_round{number}_v6')\n    assert release.OUT == module.OUT\n    sys.modules[f'finalize_training_round{number}'] = release\n    return module, release\n\n"
    source = source.replace('\ndef main(number):', helper + '\ndef main(number):')
    needle = "        ROOT / 'analysis/factorization_machine_release_dispatch_preflight_v5_20261005/verification.json',"
    assert source.count(needle) == 1
    source = source.replace(needle, needle + "\n        ROOT / 'analysis/predict_factorization_machine_scheme_v5_20261005.py',\n        ROOT / 'analysis/factorization_machine_candidate_source_preflight_v6_20261005/verification.json',")
    needle = '        result = publish(number,'
    assert source.count(needle) == 1
    source = source.replace(needle, "        assert importlib.import_module(f'optimize_training_round{number}') is module\n        assert importlib.import_module(f'finalize_training_round{number}') is release\n" + needle)
    paths = [A / 'run_factorization_machine_round_v6_20261005.py']
    create(paths[0], source)
    for number in (73, 74):
        release = (A / f'finalize_training_round{number}_v5.py').read_text(encoding='utf-8')
        release = release.replace('actual round', 'actual round').replace('predict_factorization_machine_scheme_v4_', 'predict_factorization_machine_scheme_v5_')
        path = A / f'finalize_training_round{number}_v6.py'
        create(path, release)
        paths.append(path)
        path = A / f'run_training_round{number}_v6_pipeline.py'
        create(path, f'from run_factorization_machine_round_v6_20261005 import main\nif __name__ == "__main__": main({number})\n')
        paths.append(path)
    create(A / 'factorization_machine_candidate_source_generation_v6_20261005.json', json.dumps({
        'status': 'generated_before_actual_candidate_source_controls',
        'files': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
        'planned_records': {'73': 124, '74': 138}, 'native_models_and_grids_unchanged': True,
        'original_frozen_sources_preserved': True, 'test_labels_read': False}, ensure_ascii=False, indent=2))
    print('Generated actual canonical release binding and FM candidate entrypoints v6', flush=True)


if __name__ == '__main__':
    main()
