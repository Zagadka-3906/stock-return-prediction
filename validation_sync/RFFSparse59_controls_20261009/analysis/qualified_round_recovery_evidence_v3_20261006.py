"""Require closed, fully source-locked R81 recovery while retaining prior gates."""
from pathlib import Path
import json

import psutil
import qualified_round_recovery_evidence_v2_20261005 as previous
from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha

ROOT = Path(__file__).resolve().parents[1]
_cache = None


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def complete_round_evidence(number):
    global _cache
    if number != 81:
        return previous.complete_round_evidence(number)
    folder = ROOT / 'analysis/optimization_20261003_r81'
    service = ROOT / 'analysis/service_owned_workflows_20261006/round81_publication_recovery_v2'
    result = ROOT / 'results/optimization_20261003_r81.json'
    scoped = folder / 'publication_recovery_execution_v2_20261006.json'
    frozen = folder / 'recovery_frozen_execution_v2_20261006.json'
    paths = (result, scoped, frozen, service / 'service_execution.json', service / 'native_launch.json')
    if not all(path.exists() for path in paths):
        return None
    report, scope, control = read(result), read(scoped), read(frozen)
    terminal, launch = read(paths[3]), read(paths[4])
    if report.get('status') != 'complete' or scope.get('status') != 'passed' or terminal.get('status') != 'passed':
        return None
    for pid, birth in ((launch['pid'], launch['owned_parent_creation_time']),
                       (launch['owned_worker_pid'], launch['owned_worker_creation_time'])):
        try:
            if abs(psutil.Process(pid).create_time() - birth) < 1e-5:
                return None
        except psutil.NoSuchProcess:
            pass
    required = (
        'original_failed_scope_retained',
        'all_original_frozen_inputs_fully_rehashed_andmatched',
        'all_selected_scientific_artifacts_andcandidate_bytes_rehashed_andmatched',
        'Windows_read_share_only_locks_held_during_actual_full_selected_replay_and_full_QA',
        'actual_selected5635800_row_replay_bit_identical',
        'actual_entire_original_ranking_QA_and_browser_lossless_codec_checks_passed',
        'final_full_rehash_before_read_lock_release_passed', 'all_read_handles_closed',
        'original45_second_browser_timeout_retained',
        'previous_directory_collision_failure_preserved',
        'QA_and_profile_output_paths_both_unique_for_actual_retry',
    )
    if not all(scope.get(key) is True for key in required):
        return None
    if any(scope.get(key) != 0 for key in ('new_model_fits', 'new_quality_scores')) or scope.get('test_labels_read') is not False:
        return None
    if not all(control.get(key) is True for key in ('original_frozen_protocol_not_changed',
            'original_failed_scope_retained', 'mutable_live_ranking_output_excluded_from_lifetime_scientific_bindings')):
        return None
    protocol_path, failed_path = folder / 'protocol.json', folder / 'provenance_scope_execution.json'
    protocol, failed = read(protocol_path), read(failed_path)
    if failed.get('status') != 'failed' or not failed.get('failure', '').startswith('TimeoutExpired:'):
        return None
    if 'chrome.exe' not in failed['failure'] or 'timed out after 45 seconds' not in failed['failure']:
        return None
    if scope.get('original_failure') != failed['failure']:
        return None
    collision = read(folder / 'publication_recovery_failure_20261006.json')
    if collision.get('status') != 'failed_preserved_actual_recovery' or not collision.get('failure', '').startswith('FileExistsError:'):
        return None
    if scope.get('input_sha256') != control['input_sha256']:
        return None
    bindings = dict(control['input_sha256'])
    if scope.get('original_frozen_input_files') != len(protocol['input_sha256']):
        return None
    if any(bindings.get(path) != digest for path, digest in protocol['input_sha256'].items()):
        return None
    if any(control['actual_QA_read_lock_input_sha256'].get(path) != digest for path, digest in bindings.items()):
        return None
    if str((ROOT / 'results/all_model_rankings_20261003.json').resolve()) in bindings:
        return None
    bindings.update(scope['immutable_recovery_evidence_sha256'])
    extra_paths = (*paths, protocol_path, failed_path, service / 'job_definition.json')
    for path in extra_paths:
        bindings.setdefault(str(path.resolve()), fresh_sha(path))
    if _cache is None:
        _cache = LockedReadHashCache(bindings).__enter__()
    if _cache.expected != bindings:
        return None
    sha = _cache.sha
    for path, digest in bindings.items():
        if sha(path) != digest:
            return None
    if any(sha(protocol_path) != obj['original_protocol_sha256'] or sha(failed_path) != obj['original_failed_scope_sha256'] for obj in (scope, control)):
        return None
    if any(report.get(key, {}).get('status') != 'passed' for key in ('component_audit', 'calibrated_written_csv', 'method_causal_checks', 'prediction')):
        return None
    candidate = Path(report['candidate_submission'])
    verification_path, official_path = candidate.parent / 'verification.json', folder / 'calibrated_csv_official.json'
    prediction, official = read(verification_path), read(official_path)
    if prediction.get('status') != 'passed' or official.get('status') != 'passed':
        return None
    if (prediction.get('rows'), prediction.get('days'), prediction.get('codes')) != (1599600, 344, 4650):
        return None
    if prediction.get('test_labels_read') is not False or official.get('test_labels_read') is not False:
        return None
    if sha(candidate) != prediction['csv_sha256'] or sha(folder / 'calibrated_validation.csv') != official['csv_sha256']:
        return None
    if official['metrics'] != report['winner']['metrics'] or report['scored_records'] != protocol['expected_scored_records'] or report['scored_records'] != 124:
        return None
    qa_path = ROOT / 'analysis/lossless_ranking_display_qa_v3_20261006/round81/verification.json'
    qa = read(qa_path)
    if qa.get('status') != 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks':
        return None
    if (qa['original_full_QA_result']['connected_records'], qa['original_full_QA_result']['new_round_records']) != (9946, 124):
        return None
    if scope.get('full_ranking_records') != 9946:
        return None
    evidence_paths = (*extra_paths, verification_path, official_path, qa_path)
    return {'round': 81, 'status': 'complete_declared_round',
        'score': official['metrics']['final_score'], 'scored_records': 124,
        'candidate_csv_sha256': prediction['csv_sha256'],
        'actual_recovery_scope_required': True, 'actual_source_locked_full_replay_and_QA_required': True,
        'both_original_failures_retained': True,
        'source_sha256': {str(path.relative_to(ROOT)): sha(path) for path in evidence_paths}}


def close():
    global _cache
    try:
        if _cache is not None:
            try:
                _cache.reverify()
            finally:
                _cache.close()
                _cache = None
    finally:
        previous.close()
