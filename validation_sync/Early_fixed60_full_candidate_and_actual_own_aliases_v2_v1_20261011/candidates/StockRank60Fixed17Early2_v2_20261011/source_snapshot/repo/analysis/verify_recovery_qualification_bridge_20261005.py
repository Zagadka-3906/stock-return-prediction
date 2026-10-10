"""Check actual unchanged qualification and the uncompleted recovery rejection."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    import refresh_optimization_boundary_evidence_20261004 as base
    import qualified_round_recovery_evidence_20261005 as strict
    import qualified_round_recovery_evidence_v2_20261005 as sealed
    baseline = base.complete_round_evidence(65)
    assert baseline is not None
    assert strict.complete_round_evidence(65) == sealed.complete_round_evidence(65) == baseline
    assert not (ROOT / 'results/optimization_20261003_r66.json').exists()
    assert strict.complete_round_evidence(66) is sealed.complete_round_evidence(66) is None
    assert sealed._cache is None
    failed = strict.read(A / 'optimization_20261003_r66/provenance_scope_execution.json')
    assert failed['status'] == 'failed' and 'FileNotFoundError' in failed['failure']
    sources = [Path(__file__), A / 'run_recovery_qualified_workflow_20261005.py',
        A / 'qualified_round_recovery_evidence_20261005.py',
        A / 'qualified_round_recovery_evidence_v2_20261005.py',
        A / 'standalone_root_source_adapter_20261005.py',
        A / 'standalone_root_source_adapter_preflight_20261005/verification.json']
    for source in sources:
        if source.suffix == '.py':
            compile(source.read_text(encoding='utf-8-sig'), str(source), 'exec')
    out = A / 'recovery_qualification_bridge_preflight_20261005/verification.json'
    out.parent.mkdir(exist_ok=True)
    with out.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_actual_R65_delegate_and_unfinished_R66_rejection',
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'qualified_R65_unchanged': True, 'unfinished_R66_rejected': True,
            'failed_original_R66_proof_retained': True,
            'full_recovery_scientific_gates_not_claimed_complete': True,
            'sealed_hash_cache_not_opened_for_unfinished_round': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False},
            stream, ensure_ascii=False, indent=2)
    print('passed actual R65 delegation and unfinished R66 rejection', flush=True)


if __name__ == '__main__':
    main()
