"""Require closed, fully locked124-case R89 recovery while preserving every older gate."""
from pathlib import Path
import json
import hashlib
import qualified_round_recovery_evidence_v3_20261006 as previous
from run_dependency_queue_v3_20261006 import owned
from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
_previous_gate = previous.complete_round_evidence
_cache = None


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def fresh(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def scientific_round89_evidence():
    global _cache
    folder = A / 'optimization_20261003_r89'
    service = A / 'service_owned_workflows_20261006/classifier_consensus_round89_status_recovery'
    recovery = A / 'classifier_consensus_round89_status_recovery_20261007'
    alternate = folder / 'provenance_scope_execution_status_recovery_20261007.json'
    frozen = recovery / 'frozen_before_actual_status_gate_recovery.json'
    verified = recovery / 'verification.json'
    result = ROOT / 'results/optimization_20261003_r89.json'
    if not all(p.exists() for p in (alternate, frozen, verified, result, service / 'native_launch.json', service / 'service_execution.json')):
        return None
    launch, terminal = read(service / 'native_launch.json'), read(service / 'service_execution.json')
    if owned(launch) or terminal['status'] != 'passed':
        return None
    scope, control, completed, report = read(alternate), read(frozen), read(verified), read(result)
    if scope['status'] != 'passed' or report['status'] != 'complete':
        return None
    required = ('scope_started', 'all_sha_bindings_restored', 'recovery_execution',
        'original_failed_scope_retained', 'precise_original_route_gate_required',
        'all_original124_declared_cases_retained', 'Windows_read_share_only_raw_handles_and_full_initial_final_hash')
    if not all(scope.get(k) is True for k in required) or scope.get('failed') is not False:
        return None
    if scope['actual_recovery_quality_records'] != 124 or scope['new_model_fits'] != 0:
        return None
    if completed['status'] != 'passed_actual_original124_science_candidate_full_QA_alternate_scope_recovery':
        return None
    if completed['actual_quality_score_records'] != 124 or completed['new_native_fits'] != 0:
        return None
    failed_path = folder / 'provenance_scope_execution.json'
    failed = read(failed_path)
    expected_failure = 'AssertionError: ' + str(A / 'classifier_consensus_direct_router_preflight_20261005/verification.json')
    if failed['status'] != 'failed' or failed['scope_started'] is not False or failed['failure'] != expected_failure:
        return None
    protocol_path = folder / 'protocol.json'
    protocol = read(protocol_path)
    if protocol['expected_scored_records'] != 124 or report['scored_records'] != 124:
        return None
    if scope['input_sha256'] != protocol['input_sha256']:
        return None
    bindings = dict(protocol['input_sha256'])
    if any(bindings.get(p) != digest for p, digest in control['input_sha256'].items()):
        return None
    candidate = Path(report['candidate_submission'])
    official_path = folder / 'calibrated_csv_official.json'
    prediction_path = candidate.parent / 'verification.json'
    manifest_path = candidate.parent / 'manifest.json'
    qa_path = A / 'lossless_ranking_display_qa_v4_20261006/round89/verification.json'
    if not all(p.exists() for p in (official_path, prediction_path, manifest_path, qa_path)):
        return None
    prediction, official, qa = read(prediction_path), read(official_path), read(qa_path)
    if (prediction.get('rows'), prediction.get('days'), prediction.get('codes')) != (1599600, 344, 4650):
        return None
    if prediction['status'] != 'passed' or official['status'] != 'passed' or official['metrics'] != report['winner']['metrics']:
        return None
    if prediction.get('test_labels_read') is not False or official.get('test_labels_read') is not False:
        return None
    if not all(prediction.get(k) is True for k in ('model_reload_bit_identical', 'pipeline_replay_bit_identical', 'csv_replay_byte_identical', 'csv_ranks_unchanged', 'cold80_day_prefix_bit_identical')):
        return None
    if qa['status'] != 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks' or qa['original_full_QA_result']['new_round_records'] != 124:
        return None
    if not all(qa.get(k) is True for k in ('all_original_provenance_candidate_manifest_sorting_and_six_view_checks_passed', 'all_original_exact_report_values_and_browser_lossless_nodes_verified', 'original45_second_render_timeout_retained', 'all_new_browser_profiles_under_D')):
        return None
    if any(report.get(k, {}).get('status') != 'passed' for k in ('component_audit', 'calibrated_written_csv', 'method_causal_checks', 'prediction')):
        return None
    evidence_paths = [Path(__file__), result, alternate, frozen, verified, protocol_path, failed_path,
        service / 'native_launch.json', service / 'service_execution.json', service / 'job_definition.json',
        official_path, prediction_path, manifest_path, qa_path]
    for path in evidence_paths:
        bindings.setdefault(str(path.resolve()), fresh(path))
    bindings[str(candidate.resolve())] = prediction['csv_sha256']
    bindings[str((folder / 'calibrated_validation.csv').resolve())] = official['csv_sha256']
    for relative, item in read(manifest_path)['files'].items():
        path = candidate.parent / relative
        assert path.resolve().is_relative_to(candidate.parent.resolve())
        bindings[str(path.resolve())] = item['sha256']
    if _cache is None:
        _cache = LockedReadHashCache(bindings).__enter__()
    if _cache.expected != bindings:
        return None
    if any(_cache.sha(path) != digest for path, digest in bindings.items()):
        return None
    if _cache.sha(failed_path) != control['original_failed_scope_sha256'] or _cache.sha(failed_path) != scope['original_failed_scope_sha256']:
        return None
    if _cache.sha(alternate) != completed['actual_recovery_scope_sha256']:
        return None
    return {'round': 89, 'status': 'complete_declared_round', 'score': official['metrics']['final_score'],
        'scored_records': 124, 'candidate_csv_sha256': prediction['csv_sha256'],
        'actual_closed_status_recovery_scope_required': True, 'original_failed_scope_retained': True,
        'actual_all_original124_grid_and_full_candidate_and_QA_required': True,
        'source_sha256': {str(p.relative_to(ROOT)): _cache.sha(p) for p in evidence_paths}}


def complete_round_evidence(number):
    if number != 89:
        return _previous_gate(number)
    evidence = scientific_round89_evidence()
    if evidence is None:
        return None
    receipt_path = A / 'github_validation_sync_main_20261005/round89_receipt.json'
    if not receipt_path.exists():
        return None
    receipt = read(receipt_path)
    if receipt.get('status') != 'pushed_and_remote_head_verified' or receipt.get('round') != 89 or receipt.get('actual_full_QA_version') != 4:
        return None
    if receipt.get('scored_records') != 124 or receipt.get('official_score') != evidence['score'] or not receipt.get('full_immutable_ranking_and_all_original_QA_preserved'):
        return None
    evidence['source_sha256'][str(receipt_path.relative_to(ROOT))] = fresh(receipt_path)
    evidence['actual_full_QA_main_receipt_required_for_next90'] = True
    return evidence


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
