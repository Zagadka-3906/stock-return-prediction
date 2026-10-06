"""Seal actual inference outputs together with their pre-inference source snapshot."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create

FREEZE = A / 'causal_entry_exit_buffer_source_freeze_20261006'
RELEASE = A / 'causal_entry_exit_buffer_release_20261006'
CANDIDATE = ROOT / 'candidates/causal_entry_exit_buffer_20261006'


def checked_sources():
    record = read(FREEZE / 'manifest.json')
    assert record['status'] == 'passed_pre_inference_local_Python_source_snapshot'
    assert not record['test_labels_read']
    for relative, info in record['files'].items():
        assert sha(ROOT / relative) == sha(FREEZE / 'repo' / relative) == info['sha256'], relative
    for name in ('freeze_and_infer_causal_entry_exit_buffer_20261006.py',
        'causal_entry_exit_buffer_v2_20261006.py', 'seal_buffer_candidate_source_package_20261006.py',
        'replay_sealed_buffer_candidate_20261006.py'):
        assert f'analysis/{name}' in record['files'], name
    return record


def prerequisites():
    sources = checked_sources()
    release = read(RELEASE / 'verification.json')
    candidate = read(CANDIDATE / 'verification.json')
    before = read(RELEASE / 'frozen_before_actual_candidate_inference.json')
    selection = read(CANDIDATE / 'selection.json')
    assert release['status'] == 'passed_actual_frozen_zero_buffer_full_candidate_saved_model_reload_and_cold80'
    assert candidate['status'] == 'passed' and not candidate['test_labels_read']
    assert (candidate['rows'], candidate['days'], candidate['codes']) == (1599600, 344, 4650)
    assert sources['at_local'] <= selection['frozen_at_local'], 'The source snapshot must precede inference'
    assert sha(RELEASE / 'selection.json') == before['selection_sha256']
    assert read(RELEASE / 'selection.json') == selection
    assert candidate['model_reload_bit_identical'] and candidate['cold80_day_prefix_bit_identical']
    assert candidate['pipeline_replay_bit_identical'] and candidate['csv_replay_byte_identical']
    assert candidate['old_delivery_pointer_unchanged']
    assert release['actual_model_reload_controls'] == candidate['actual_model_reload_controls']
    assert release['actual_cold80_model_controls'] == candidate['actual80_day_prefix_model_controls']
    assert sha(CANDIDATE / 'submission.csv') == release['csv_sha256'] == candidate['csv_sha256']
    for key, info in candidate['models'].items():
        path = Path(info['path']).resolve()
        assert path.is_relative_to(CANDIDATE.resolve()), key
        assert sha(path) == info['sha256'], key
    assert len(release['actual_model_storage']) == len(candidate['models'])
    return sources, release, candidate


def main():
    assert not (CANDIDATE / 'manifest.json').exists(), 'Never edit an already sealed candidate'
    sources, release, prediction = prerequisites()
    # The snapshot contains every local Python source in the declared inference
    # roots, including the actual hook that adds the selected buffer.
    for relative, info in sources['files'].items():
        original = FREEZE / 'repo' / relative
        target = CANDIDATE / 'source_snapshot' / 'repo' / relative
        assert target.resolve().is_relative_to(CANDIDATE.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(original, target)
        assert os.path.samefile(original, target) and sha(target) == info['sha256']
    evidence = [FREEZE / 'manifest.json', FREEZE / 'frozen_before_source_copy.json',
        RELEASE / 'frozen_before_actual_candidate_inference.json', RELEASE / 'verification.json',
        A / 'causal_entry_exit_buffer_official_pilot_20261006/verification.json',
        A / 'causal_entry_exit_buffer_full_controls_v3_20261006/verification.json']
    for path in evidence:
        target = CANDIDATE / 'evidence' / path.relative_to(A)
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(path, target)
        assert sha(target) == sha(path)
    create(CANDIDATE / 'source_package_verification.json', {
        'status': 'passed_actual_inference_outputs_and_pre_inference_local_source_package',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'source_files': len(sources['files']), 'source_snapshot_manifest_sha256': sha(FREEZE / 'manifest.json'),
        'actual_candidate_verification_sha256': sha(CANDIDATE / 'verification.json'),
        'csv_sha256': release['csv_sha256'], 'actual_saved_model_reload_and_cold80_references_preserved': True,
        'all_models_sources_and_final_outputs_hash_verified': True,
        'zero_buffer_actual_training_and_future_identity_selected_by_official_scores': True,
        'full_ranking_registration_and_QA_pending': True, 'new_model_fits': 0, 'new_quality_scores': 0,
        'test_labels_read': False})
    create(CANDIDATE / 'manifest.json', {'status': 'passed', 'files': {
        p.relative_to(CANDIDATE).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
        for p in sorted(CANDIDATE.rglob('*')) if p.is_file() and p != CANDIDATE / 'manifest.json'}})
    # Nested source manifests are evidence and must themselves be covered.
    manifest = read(CANDIDATE / 'manifest.json')
    for p in CANDIDATE.rglob('manifest.json'):
        if p == CANDIDATE / 'manifest.json':
            continue
        relative = p.relative_to(CANDIDATE).as_posix()
        assert manifest['files'][relative]['sha256'] == sha(p), relative
    assert len(manifest['files']) == sum(p.is_file() for p in CANDIDATE.rglob('*')) - 1
    for relative, info in manifest['files'].items():
        assert sha(CANDIDATE / relative) == info['sha256'], relative
    create(RELEASE / 'source_package_verification.json', {'status': 'passed_sealed_actual_buffer_candidate',
        'candidate': str(CANDIDATE), 'manifest_sha256': sha(CANDIDATE / 'manifest.json'),
        'source_package_verification_sha256': sha(CANDIDATE / 'source_package_verification.json'),
        'manifest_files': len(manifest['files']), 'full_ranking_and_main_publication_pending': True,
        'test_labels_read': False})
    print(json.dumps(read(RELEASE / 'source_package_verification.json')), flush=True)


if __name__ == '__main__':
    main()
