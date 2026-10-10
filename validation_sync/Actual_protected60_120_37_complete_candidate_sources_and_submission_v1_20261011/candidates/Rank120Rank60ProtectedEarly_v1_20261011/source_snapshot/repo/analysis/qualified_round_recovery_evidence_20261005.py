"""Require the actual closed R66 recovery scope without replacing its failed proof."""
from pathlib import Path
import hashlib
import json

from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence as original

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def complete_round_evidence(number):
    if number != 66:
        return original(number)
    result = ROOT / 'results/optimization_20261003_r66.json'
    folder = ROOT / 'analysis/optimization_20261003_r66'
    scoped = folder / 'provenance_scope_execution_recovery_v3_20261005.json'
    frozen = folder / 'recovery_frozen_execution_v3_20261005.json'
    if not all(p.exists() for p in (result, scoped, frozen)):
        return None
    report, scope, control = read(result), read(scoped), read(frozen)
    if report.get('status') != 'complete' or scope.get('status') != 'passed':
        return None
    required = ('scope_started', 'recovery_execution', 'original_failed_scope_retained',
                'all_original_and_recovery_inputs_fully_rehashed_andmatched', 'all_sha_bindings_restored')
    if not all(scope.get(key) is True for key in required) or scope.get('failed') is not False:
        return None
    failed_path = folder / 'provenance_scope_execution.json'
    failed = read(failed_path)
    if failed.get('status') != 'failed' or not failed.get('failure', '').startswith('FileNotFoundError:'):
        return None
    if 'optimization_20261003_r66' not in failed['failure']:
        return None
    if control.get('original_frozen_protocol_not_changed') is not True:
        return None
    protocol_path = folder / 'protocol.json'
    if sha(protocol_path) != scope['original_protocol_sha256'] or sha(protocol_path) != control['original_protocol_sha256']:
        return None
    bindings = control['input_sha256']
    if bindings.get(str(failed_path.resolve())) != sha(failed_path):
        return None
    for source, expected in read(protocol_path)['input_sha256'].items():
        if bindings.get(source) != expected:
            return None
    for source, expected in bindings.items():
        if sha(source) != expected:
            return None
    for key in ('component_audit', 'calibrated_written_csv', 'method_causal_checks', 'prediction'):
        if report.get(key, {}).get('status') != 'passed':
            return None
    candidate = Path(report['candidate_submission']).parent / 'verification.json'
    official = folder / 'calibrated_csv_official.json'
    if not candidate.exists() or not official.exists():
        return None
    prediction, metrics = read(candidate), read(official)
    if prediction.get('status') != 'passed' or metrics.get('status') != 'passed':
        return None
    if (prediction.get('rows'), prediction.get('days'), prediction.get('codes')) != (1599600, 344, 4650):
        return None
    if metrics['metrics'] != report['winner']['metrics']:
        return None
    if report['scored_records'] != read(protocol_path)['expected_scored_records']:
        return None
    if prediction.get('test_labels_read') is not False or metrics.get('test_labels_read') is not False:
        return None
    if sha(Path(report['candidate_submission'])) != prediction['csv_sha256']:
        return None
    paths = (result, scoped, frozen, failed_path, protocol_path, candidate, official)
    return {'round': 66, 'status': 'complete_declared_round',
            'score': metrics['metrics']['final_score'], 'scored_records': report['scored_records'],
            'candidate_csv_sha256': prediction['csv_sha256'], 'actual_recovery_scope_required': True,
            'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in paths}}
