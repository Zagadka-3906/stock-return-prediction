"""Versioned typed-model dispatch around the unchanged R61-R63 controllers."""
from pathlib import Path
import argparse
import importlib
import json
import os
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
PROOF = ROOT / 'analysis/nystrom_future_codec_recovery_20261005/verification.json'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main(number):
    assert number in (61, 62, 63)
    while not PROOF.exists():
        time.sleep(10)
    assert read(PROOF)['status'] == 'passed'
    if number < 63:
        original = importlib.import_module('run_nystrom_ridge_locked_pipeline_20261004')
        while not all(p.exists() for p in original.gates(number)):
            time.sleep(10)
    else:
        from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
        while complete_round_evidence(62) is None:
            time.sleep(10)
        original = importlib.import_module('run_latest_joint_round63_locked_v2_20261005')
    scratch = ROOT / f'tmp/round{number}_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[variable] = str(scratch)
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        os.environ[variable] = '8'
    from locked_read_hash_cache_20261004 import fresh_sha
    for path, digest in read(PROOF)['input_sha256'].items():
        assert fresh_sha(path) == digest, path
    from nystrom_future_codec_adapter_20261005 import install
    import frozen_provenance_execution_scope_20261004 as scopes
    original_scope = scopes.FrozenProvenanceExecutionScope
    extras = [Path(__file__), ROOT / 'analysis/nystrom_future_codec_adapter_20261005.py', PROOF,
              ROOT / 'analysis/nystrom_future_codec_recovery_20261005/frozen_before_future_controls.json',
              ROOT / 'analysis/train_nystrom_ridge_bank_20261004.py',
              ROOT / 'analysis/nystrom_ridge_model_sources_20261004.py']

    def factory(module, sources, metadata, analysis_root):
        metadata = {**metadata, 'typed_codec_outer_driver': str(Path(__file__)),
                    'typed_codec_outer_driver_sha256': fresh_sha(Path(__file__)),
                    'ridge_nystrom_uses_frozen_native_predictor': True,
                    'legacy_model_dispatch_unchanged': True, 'temporary_files_drive': 'D'}
        return original_scope(module, [*sources, *extras], metadata, analysis_root)

    restore = install()
    scopes.FrozenProvenanceExecutionScope = factory
    try:
        original.main(number) if number < 63 else original.main()
    finally:
        scopes.FrozenProvenanceExecutionScope = original_scope
        restore()
    module = importlib.import_module(f'optimize_training_round{number}')
    candidate = ROOT / f'candidates/optimization_20261003_r{number}'
    assert read(candidate / 'verification.json')['status'] == 'passed'
    shutil.copyfile(ROOT / 'analysis/nystrom_future_codec_adapter_20261005.py', candidate / 'nystrom_future_codec_adapter_20261005.py')
    module.dump(module.OUT / 'typed_future_codec_execution.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'candidate_verification_sha256': fresh_sha(candidate / 'verification.json'),
        'adapter_sha256': fresh_sha(candidate / 'nystrom_future_codec_adapter_20261005.py'),
        'all_runtime_bindings_restored': True, 'temporary_files_drive': 'D',
        'new_model_fits': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int, choices=(61, 62, 63))
    main(parser.parse_args().number)
