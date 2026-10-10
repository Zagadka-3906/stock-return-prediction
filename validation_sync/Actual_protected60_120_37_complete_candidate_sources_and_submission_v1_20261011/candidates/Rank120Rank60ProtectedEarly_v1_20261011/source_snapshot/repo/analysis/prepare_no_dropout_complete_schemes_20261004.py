"""Generate isolated R53/R54 adapters without modifying frozen R51/R52 sources."""
from pathlib import Path
import hashlib
import json
import re
import time

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'analysis'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def translate(source):
    text = source.read_text(encoding='utf-8-sig')
    text = text.replace('additive_basis', 'no_dropout_seed')
    text = text.replace('basis_role_scheme_graph', 'no_dropout_role_scheme_graph')
    text = text.replace('basis_standalone_scheme_graph', 'no_dropout_standalone_scheme_graph')
    text = text.replace('round51', 'round53').replace('round52', 'round54')
    text = re.sub(r'\b51\b', '53', text)
    text = re.sub(r'\b52\b', '54', text)
    for old, new in ((219, 226), (220, 227), (221, 228), (222, 229), (223, 230), (224, 231), (225, 232)):
        text = text.replace(str(old), str(new))
    text = text.replace('196', '148').replace('258', '178')
    text = text.replace('[145,8,18,25]', '[97,8,18,25]').replace('[73,168,17]', '[49,112,17]')
    return text


def main():
    pairs = (
        ('additive_basis_scheme_runtime_20261004.py', 'no_dropout_seed_scheme_runtime_20261004.py'),
        ('additive_basis_search_engine_20261004.py', 'no_dropout_seed_search_engine_20261004.py'),
        ('additive_basis_release_engine_20261004.py', 'no_dropout_seed_release_engine_20261004.py'),
        ('predict_additive_basis_scheme_20261004.py', 'predict_no_dropout_seed_scheme_20261004.py'),
        ('check_additive_basis_scheme_20261004.py', 'check_no_dropout_seed_scheme_20261004.py'),
        ('run_additive_basis_round_pipeline_20261004.py', 'run_no_dropout_seed_round_pipeline_20261004.py'),
        ('optimize_training_round51.py', 'optimize_training_round53.py'),
        ('optimize_training_round52.py', 'optimize_training_round54.py'),
        ('finalize_training_round51.py', 'finalize_training_round53.py'),
        ('finalize_training_round52.py', 'finalize_training_round54.py'),
        ('run_training_round51_pipeline.py', 'run_training_round53_pipeline.py'),
        ('run_training_round52_pipeline.py', 'run_training_round54_pipeline.py'))
    sources = {}
    for original, new in pairs:
        source, target = HERE / original, HERE / new
        assert not target.exists(), target
        target.write_text(translate(source), encoding='utf-8', newline='\n')
        sources[str(source.resolve())] = sha(source)
    # This generated stage is followed by model-family-specific edits andactual controls.
    record = {'status': 'isolated_adapters_generated_awaiting_family_specific_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'original_source_sha256': sources,
        'original_frozen_sources_unchanged': True, 'new_quality_scores': 0, 'test_labels_read': False}
    with (HERE / 'no_dropout_seed_adapter_generation_20261004.json').open('x', encoding='utf-8') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    print('Twelve isolated R53/R54 adapter sources generated; existing sources unchanged')


if __name__ == '__main__':
    main()
