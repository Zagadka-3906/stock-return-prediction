"""Preserve failed generator sources and create distinct corrected quality versions."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        if isinstance(value, str):
            compile(value, str(path), 'exec') if path.suffix == '.py' else None
            stream.write(value)
        else:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


def version(text):
    text = re.sub(r'(ready_classifier_consensus_reference_(?:search_engine|round|scheme|generators|execution|complete_plan|generator_preflight|execution_preflight|quality_run))_20261006',
                  r'\1_v2_20261006', text)
    text = text.replace('run_ready_classifier_consensus_reference_round_20261006', 'run_ready_classifier_consensus_reference_round_v2_20261006')
    text = text.replace('predict_ready_classifier_consensus_reference_scheme_20261006', 'predict_ready_classifier_consensus_reference_scheme_v2_20261006')
    text = text.replace('check_ready_classifier_consensus_reference_scheme_20261006', 'check_ready_classifier_consensus_reference_scheme_v2_20261006')
    return text


def main():
    failed = A / 'ready_classifier_consensus_reference_generator_preflight_20261006/frozen_before_generator_controls.json'
    assert failed.exists() and not (failed.parent / 'verification.json').exists()
    frozen = json.loads(failed.read_text(encoding='utf-8'))['source_sha256']
    assert all(sha(path) == digest for path, digest in frozen.items())
    outputs = {}
    engine = version((A / 'ready_classifier_consensus_reference_search_engine_20261006.py').read_text(encoding='utf-8'))
    for old in range(346, 353):
        engine = engine.replace(f'wave{old}', f'wave{old+7}')
    engine = engine.replace("previous=importlib.import_module(f'optimize_training_round{parent_number}_v2')",
        "previous=importlib.import_module(f'optimize_training_round{parent_number}_v3' if parent_number==89 else f'optimize_training_round{parent_number}_v2')")
    for name in ('optimize_training_round', 'finalize_training_round', 'run_training_round'):
        engine = engine.replace(f'{name}{{number}}_v2', f'{name}{{number}}_v3')
    engine = engine.replace('explicit_parent_release_engine_v2_20261005.py', 'explicit_parent_release_engine_v3_20261006.py')
    outputs['ready_classifier_consensus_reference_search_engine_v2_20261006.py'] = engine
    driver = version((A / 'run_ready_classifier_consensus_reference_round_20261006.py').read_text(encoding='utf-8'))
    for name in ('optimize_training_round', 'finalize_training_round'):
        driver = driver.replace(f'{name}{{number}}_v2', f'{name}{{number}}_v3')
    outputs['run_ready_classifier_consensus_reference_round_v2_20261006.py'] = driver
    check = version((A / 'check_ready_classifier_consensus_reference_scheme_20261006.py').read_text(encoding='utf-8'))
    outputs['check_ready_classifier_consensus_reference_scheme_v2_20261006.py'] = check
    predictor = version((A / 'predict_ready_classifier_consensus_reference_scheme_20261006.py').read_text(encoding='utf-8'))
    for name in ('optimize_training_round89', 'finalize_training_round89'):
        predictor = predictor.replace(name + '_v2.py', name + '_v3.py')
    for name in ('optimize_training_round', 'finalize_training_round', 'run_training_round'):
        predictor = predictor.replace(f'{name}{{number}}_v2', f'{name}{{number}}_v3')
    predictor = predictor.replace("'ready_classifier_consensus_reference_search_engine_v2_20261006.py',",
        "'ready_classifier_consensus_reference_search_engine_v2_20261006.py',\n        'explicit_parent_release_engine_v3_20261006.py',")
    predictor = predictor.replace("name.endswith('_v2.py')", "name.endswith(('_v2.py', '_v3.py'))")
    predictor = predictor.replace("name.replace('_v2.py', '.py')", "name.replace('_v2.py', '.py').replace('_v3.py', '.py')")
    outputs['predict_ready_classifier_consensus_reference_scheme_v2_20261006.py'] = predictor
    release = (A / 'explicit_parent_release_engine_v2_20261005.py').read_text(encoding='utf-8')
    release = release.replace('optimize_training_round{number}_v2', 'optimize_training_round{number}_v3')
    release = release.replace('finalize_training_round{number}_v2', 'finalize_training_round{number}_v3')
    outputs['explicit_parent_release_engine_v3_20261006.py'] = release
    generator = version((A / 'verify_ready_classifier_consensus_reference_generators_20261006.py').read_text(encoding='utf-8'))
    generator = generator.replace('optimize_training_round{number}_v2', 'optimize_training_round{number}_v3')
    generator = generator.replace("('_v2')", "('_v3')")
    generator = generator.replace("('_v2_pipeline')", "('_v3_pipeline')")
    generator = generator.replace("('optimize_training_round', '_v2')", "('optimize_training_round', '_v3')")
    generator = generator.replace("('finalize_training_round', '_v2')", "('finalize_training_round', '_v3')")
    generator = generator.replace("('run_training_round', '_v2_pipeline')", "('run_training_round', '_v3_pipeline')")
    outputs['verify_ready_classifier_consensus_reference_generators_v2_20261006.py'] = generator
    execution = version((A / 'verify_ready_classifier_consensus_reference_execution_20261006.py').read_text(encoding='utf-8'))
    execution = execution.replace("f'optimize_training_round{parent}_v2.py'", "f'optimize_training_round{parent}_{\"v3\" if parent>=89 else \"v2\"}.py'")
    execution = execution.replace('explicit_parent_release_engine_v2_20261005.py', 'explicit_parent_release_engine_v3_20261006.py')
    outputs['verify_ready_classifier_consensus_reference_execution_v2_20261006.py'] = execution
    for number in (89, 90):
        outputs[f'optimize_training_round{number}_v3.py'] = (
            f'import sys\nimport optimize_training_round{number-1}_{"v3" if number==90 else "v2"}\n'
            'from ready_classifier_consensus_reference_search_engine_v2_20261006 import install\n'
            f'install({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\n')
        outputs[f'finalize_training_round{number}_v3.py'] = (
            'from explicit_parent_release_engine_v3_20261006 import install\n'
            f'install({number},globals())\n')
        outputs[f'run_training_round{number}_v3_pipeline.py'] = (
            'from run_ready_classifier_consensus_reference_round_v2_20261006 import main\n'
            f'if __name__ == "__main__":main({number})\n')
    for name, text in outputs.items():
        create(A / name, text)
    plan = json.loads((A / 'ready_classifier_consensus_reference_complete_plan_20261006.json').read_text(encoding='utf-8'))
    create(A / 'ready_classifier_consensus_reference_complete_plan_v2_20261006.json', {
        **plan, 'previous_failed_generator_inputs_preserved': True,
        'same_fixed6_composites_and262_record_grid': True,
        'quality_source_files_generated': list(outputs),
        'old_generator_freeze_sha256': sha(failed), 'corrected_wave_result_file_references': True})
    assert all(sha(path) == digest for path, digest in frozen.items())
    create(A / 'classifier_consensus_quality_version_repair_20261006.json', {
        'status': 'distinct_corrected_versions_before_controls',
        'original_failed_source_sha256': frozen, 'failed_generator_freeze_sha256': sha(failed),
        'generated_sha256': {name: sha(A / name) for name in outputs},
        'original_sources_unchanged': True, 'new_quality_scores': 0,
        'new_native_fits': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'preserved_failed_attempt_and_created_corrected_versions',
                      'new_source_files': len(outputs)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
