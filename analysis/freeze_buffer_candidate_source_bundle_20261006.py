"""Freeze repository Python sources before the already scheduled actual inference."""
from pathlib import Path
import importlib.metadata
import json
import platform
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned

OUT = A / 'causal_entry_exit_buffer_source_freeze_20261006'
CANDIDATE = ROOT / 'candidates/causal_entry_exit_buffer_20261006'
RELEASE = A / 'causal_entry_exit_buffer_release_20261006'


def sources():
    # Include the full local Python roots rather than guessing dependencies of
    # dynamic model codecs, historical recipe modules, or deserialized classes.
    return sorted(set(ROOT.glob('*.py')) | set(A.glob('*.py')) |
        set((A / 'connected_validation_20261002').glob('*.py')) |
        set((ROOT / 'src').rglob('*.py')) | set((ROOT / 'experiments').rglob('*.py')))


def main():
    assert not OUT.exists() and not CANDIDATE.exists() and not RELEASE.exists()
    waiter = read(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_candidate_waiter/native_launch.json')
    assert owned(waiter), 'The original inference admission waiter must still be owned and live'
    assert read(A / 'causal_entry_exit_buffer_candidate_waiter_20261006/state.json')['status'] == 'waiting_for_candidate_memory_admission'
    OUT.mkdir()
    pins = {str(p.resolve()): sha(p) for p in sources()}
    create(OUT / 'frozen_before_source_copy.json', {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': pins, 'candidate_inference_not_started': True,
        'existing_waiter_identity': waiter, 'no_scientific_process_suspended': True})
    files = {}
    for path, digest in pins.items():
        source = Path(path)
        relative = source.relative_to(ROOT)
        target = OUT / 'repo' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(target) == sha(source) == digest
        files[relative.as_posix()] = {'sha256': digest, 'bytes': target.stat().st_size,
            'original_source': path}
    assert not CANDIDATE.exists() and not RELEASE.exists(), 'A pre-inference freeze may not be backdated'
    for path, digest in pins.items():
        assert sha(path) == digest, path
    versions = {}
    for name in ('numpy', 'pandas', 'polars', 'lightgbm', 'xgboost', 'scipy', 'joblib', 'torch', 'scikit-learn'):
        versions[name] = importlib.metadata.version(name)
    create(OUT / 'manifest.json', {'status': 'passed_pre_inference_local_Python_source_snapshot',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'files': files,
        'python': platform.python_version(), 'library_versions': versions,
        'local_source_roots': ['root/*.py', 'analysis/*.py', 'analysis/connected_validation_20261002/*.py',
            'src/**/*.py', 'experiments/**/*.py'],
        'source_snapshot_is_not_a_new_model_fit_or_score': True,
        'actual_saved_model_inference_and_full_ranking_pending': True, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_pre_inference_source_freeze', 'source_files': len(files),
        'source_bytes': sum(v['bytes'] for v in files.values())}), flush=True)


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_source_freeze',
                'error': f'{type(error).__name__}: {error}'})
        raise
