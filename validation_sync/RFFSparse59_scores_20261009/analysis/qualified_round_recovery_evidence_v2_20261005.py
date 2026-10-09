"""Keep strict recovered-round checks and seal their immutable inputs while observing."""
from pathlib import Path
import qualified_round_recovery_evidence_20261005 as strict
from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha

_cache = None


def complete_round_evidence(number):
    global _cache
    if number != 66:
        return strict.complete_round_evidence(number)
    folder = strict.ROOT / 'analysis/optimization_20261003_r66'
    result = strict.ROOT / 'results/optimization_20261003_r66.json'
    scoped = folder / 'provenance_scope_execution_recovery_v3_20261005.json'
    frozen = folder / 'recovery_frozen_execution_v3_20261005.json'
    if not all(p.exists() for p in (result, scoped, frozen)):
        return None
    report = strict.read(result)
    if report.get('status') != 'complete' or strict.read(scoped).get('status') != 'passed':
        return None
    if _cache is None:
        expected = dict(strict.read(frozen)['input_sha256'])
        candidate = Path(report['candidate_submission'])
        paths = (result, scoped, frozen, folder / 'protocol.json',
                 folder / 'provenance_scope_execution.json', candidate,
                 candidate.parent / 'verification.json', folder / 'calibrated_csv_official.json')
        for path in paths:
            expected.setdefault(str(path.resolve()), fresh_sha(path))
        _cache = LockedReadHashCache(expected).__enter__()
    original_sha = strict.sha
    try:
        strict.sha = _cache.sha
        return strict.complete_round_evidence(number)
    finally:
        strict.sha = original_sha


def close():
    global _cache
    if _cache is not None:
        try:
            _cache.reverify()
        finally:
            _cache.close()
            _cache = None
