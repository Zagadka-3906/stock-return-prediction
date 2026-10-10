"""Complete actual R81 publication checks under all original frozen read locks."""
from pathlib import Path
import gzip
import hashlib
import json
import shutil
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
FOLDER = A / 'optimization_20261003_r81'
FROZEN = FOLDER / 'recovery_frozen_execution_20261006.json'
SCOPE = FOLDER / 'publication_recovery_execution_20261006.json'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def stage(name):
    print(json.dumps({'round': 81, 'actual_recovery_stage': name,
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'new_quality_scores': 0}), flush=True)


def main():
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    assert not FROZEN.exists() and not SCOPE.exists()
    original_scope = FOLDER / 'provenance_scope_execution.json'
    failure = read(original_scope)
    assert failure['status'] == 'failed' and failure['failure'].startswith('TimeoutExpired:')
    assert 'chrome.exe' in failure['failure'] and 'timed out after 45 seconds' in failure['failure']
    previous = read(A / 'system_reboot_workflow_recovery_20261006/round81/launch.json')
    try:
        worker = psutil.Process(previous['owned_worker_pid'])
        assert abs(worker.create_time() - previous['owned_worker_creation_time']) > 1e-5
    except psutil.NoSuchProcess:
        pass
    result_path = ROOT / 'results/optimization_20261003_r81.json'
    result = read(result_path)
    protocol_path = FOLDER / 'protocol.json'
    protocol = read(protocol_path)
    assert result['status'] == 'complete' and result['scored_records'] == protocol['expected_scored_records'] == 124
    for key in ('component_audit', 'calibrated_written_csv', 'method_causal_checks', 'prediction'):
        assert result[key]['status'] == 'passed', key
    official = read(FOLDER / 'calibrated_csv_official.json')
    assert official['status'] == 'passed' and official['metrics'] == result['winner']['metrics']
    candidate = Path(result['candidate_submission'])
    verification = read(candidate.parent / 'verification.json')
    assert verification['status'] == 'passed' and not verification['test_labels_read']
    assert (verification['rows'], verification['days'], verification['codes']) == (1599600, 344, 4650)
    assert sha(candidate) == verification['csv_sha256']
    assert sha(FOLDER / 'calibrated_validation.csv') == official['csv_sha256']
    controls = read(FOLDER / 'linear_leaf_causal_checks.json')
    assert controls['status'] == 'passed' and len(controls['checks']) == 20
    assert all(row['label_poisoning_bit_identical'] and all(p['bit_identical'] for p in row['prefixes']) for row in controls['checks'])
    assert sum(len(row['prefixes']) for row in controls['checks']) == 42
    waves = [read(path) for path in sorted(FOLDER.glob('wave*_results.json'))]
    assert all(row['status'] == 'complete' for row in waves)
    assert sum(len(row['results']) for row in waves) == 124
    inputs = dict(protocol['input_sha256'])
    paths = [Path(__file__), protocol_path, original_scope, result_path,
        FOLDER / 'selection.json', FOLDER / 'selected_validation.npy',
        FOLDER / 'calibrated_validation.csv', FOLDER / 'calibrated_csv_official.json',
        FOLDER / 'causal_validation.json', FOLDER / 'linear_leaf_causal_checks.json',
        candidate.parent / 'manifest.json', candidate.parent / 'verification.json',
        A / 'verify_lossless_ranking_display_20261006.py', A / 'verify_lossless_ranking_display_v2_20261006.py',
        A / 'build_lossless_ranking_display_20261006.py', A / 'locked_read_hash_cache_20261004.py']
    paths += list(FOLDER.glob('wave*_results.json')) + list(FOLDER.glob('causal_mapping_*.json'))
    paths += [FOLDER / 'future_return_mapping.json']
    display = A / 'lossless_ranking_display_20261006/round81'
    paths += [display / name for name in ('frozen_before_encoding.json', 'verification.json', 'complete_rankings_lossless.html')]
    manifest = read(candidate.parent / 'manifest.json')
    for name, metadata in manifest['files'].items():
        path = candidate.parent / name
        assert sha(path) == metadata['sha256'], name
        paths.append(path)
    for path in dict.fromkeys(paths):
        key, digest = str(path.resolve()), sha(path)
        assert key not in inputs or inputs[key] == digest, key
        inputs[key] = digest
    # The live report is a publication output; snapshot it without pinning a
    # mutable display file in the future predecessor-qualification cache.
    report_path = ROOT / 'results/all_model_rankings_20261003.json'
    report = read(report_path)
    board_sources = {item['path']: item['sha256'] for item in report['source_manifest']}
    report_sha = sha(report_path)
    assert report_sha == read(display / 'verification.json')['original_report_sha256']
    locked_inputs = dict(inputs)
    for path, digest in board_sources.items():
        key = str(Path(path).resolve())
        assert key not in locked_inputs or locked_inputs[key] == digest, key
        locked_inputs[key] = digest
    locked_inputs[str(report_path.resolve())] = report_sha
    create(FROZEN, {'status': 'frozen_before_actual_full_source_locked_publication_recovery',
        'input_sha256': inputs, 'actual_QA_read_lock_input_sha256': locked_inputs,
        'original_protocol_sha256': sha(protocol_path), 'original_failed_scope_sha256': sha(original_scope),
        'original_frozen_protocol_not_changed': True, 'original_failed_scope_retained': True,
        'mutable_live_ranking_output_excluded_from_lifetime_scientific_bindings': True,
        'expected_actual_full_ranking_records': 9946, 'new_model_fits': 0, 'new_quality_scores': 0,
        'test_labels_read': False})
    stage('full_original_and_selected_inputs_hash_and_read_lock')
    cache = LockedReadHashCache(locked_inputs)
    error, selected_replay, qa = None, False, None
    snapshot = FOLDER / 'recovery_full_ranking_snapshot_20261006.json.gz'
    try:
        with cache:
            import qualified_round_recovery_evidence_v2_20261005 as qualified
            import refresh_optimization_boundary_evidence_20261004 as boundary
            boundary.complete_round_evidence = qualified.complete_round_evidence
            import standalone_root_source_adapter_20261005 as adapter
            import optimize_training_round50 as root_sources
            restore = adapter.install(root_sources)
            try:
                import optimize_training_round81_v2 as module
                sys.modules['optimize_training_round81'] = module
                import numpy as np
                stage('actual_selected_full5635800_row_output_replay')
                context = module.Context()
                context.configure(read(FOLDER / 'selection.json')['winner'])
                prediction = context.predict(context.donor(context.finished('baseline')), 0., 0.)[0]
                assert len(prediction) == 5635800 and np.array_equal(prediction, np.load(FOLDER / 'selected_validation.npy'))
                selected_replay = True
                del context, prediction
                __import__('gc').collect()
            finally:
                restore()
                qualified.close()
            stage('actual_entire_original_QA_under_full_original_frozen_locks')
            from verify_lossless_ranking_display_v2_20261006 import main as full_qa
            full_qa(81)
            qa_path = A / 'lossless_ranking_display_qa_v2_20261006/round81/verification.json'
            qa = read(qa_path)
            assert qa['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
            assert qa['original_full_QA_result']['connected_records'] == 9946
            assert qa['original_full_QA_result']['new_round_records'] == 124
            stage('immutable_full_ranking_snapshot_and_final_full_rehash')
            with report_path.open('rb') as source, snapshot.open('xb') as destination:
                with gzip.GzipFile(filename='', mode='wb', fileobj=destination, compresslevel=6, mtime=0) as compressed:
                    shutil.copyfileobj(source, compressed, length=8 * 1024**2)
            with gzip.open(snapshot, 'rb') as stream:
                assert hashlib.file_digest(stream, 'sha256').hexdigest() == report_sha
        evidence_paths = [snapshot, qa_path, qa_path.parent / 'qa/interaction_result.json',
            qa_path.parent / 'qa/ranking_report.png', qa_path.parent / 'frozen_before_actual_full_QA.json']
        evidence = {str(path.resolve()): sha(path) for path in evidence_paths}
        create(SCOPE, {'status': 'passed', 'round': 81, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'original_failure': failure['failure'], 'original_failed_scope_retained': True,
            'original_protocol_sha256': sha(protocol_path), 'original_failed_scope_sha256': sha(original_scope),
            'all_original_frozen_inputs_fully_rehashed_andmatched': True,
            'all_selected_scientific_artifacts_andcandidate_bytes_rehashed_andmatched': True,
            'Windows_read_share_only_locks_held_during_actual_full_selected_replay_and_full_QA': True,
            'actual_selected5635800_row_replay_bit_identical': selected_replay,
            'actual_entire_original_ranking_QA_and_browser_lossless_codec_checks_passed': True,
            'final_full_rehash_before_read_lock_release_passed': True, 'all_read_handles_closed': cache.closed,
            'original_frozen_input_files': len(protocol['input_sha256']),
            'input_sha256': inputs, 'immutable_recovery_evidence_sha256': evidence,
            'published_result_sha256': sha(result_path), 'candidate_verification_sha256': sha(candidate.parent / 'verification.json'),
            'official_written_CSV_verification_sha256': sha(FOLDER / 'calibrated_csv_official.json'),
            'full_ranking_snapshot': str(snapshot), 'full_ranking_snapshot_raw_sha256': report_sha,
            'full_ranking_records': 9946, 'original45_second_browser_timeout_retained': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
        stage('passed_actual_closed_publication_recovery')
    except BaseException as failure_error:
        error = f'{type(failure_error).__name__}: {failure_error}'
        create(FOLDER / 'publication_recovery_failure_20261006.json', {'status': 'failed_preserved_actual_recovery',
            'failure': error, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'original_failed_scope_retained': True})
        raise


if __name__ == '__main__':
    main()
