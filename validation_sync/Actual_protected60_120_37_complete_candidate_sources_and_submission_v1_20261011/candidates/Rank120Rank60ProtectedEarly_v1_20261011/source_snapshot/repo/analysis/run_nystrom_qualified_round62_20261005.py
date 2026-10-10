"""Require full predecessor scope closure before the original typed R62 handoff."""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    from locked_read_hash_cache_20261004 import fresh_sha
    state = ROOT / 'analysis/ongoing_optimization_r62_state.json'
    state.write_text(json.dumps({'round': 62, 'stage': 'waiting_for_full_qualified_round61_scientific_and_scope_evidence',
        'status': 'running', 'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'continuous_optimization_authorized': True, 'test_labels_read': False}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    while complete_round_evidence(61) is None:
        time.sleep(10)
    evidence = complete_round_evidence(61)
    assert evidence is not None
    proof_path = ROOT / 'analysis/nystrom_round62_qualified_handoff_20261005/predecessor_qualified_before_freeze.json'
    with proof_path.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_full_qualified_predecessor',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'previous_round': evidence,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    import frozen_provenance_execution_scope_20261004 as scopes
    import run_nystrom_codec_locked_pipeline_20261005 as original
    original_scope = scopes.FrozenProvenanceExecutionScope

    def factory(module, sources, metadata, analysis_root):
        metadata = {**metadata, 'fully_qualified_predecessor_required': 61,
            'qualified_predecessor_outer_driver': str(Path(__file__)),
            'qualified_predecessor_outer_driver_sha256': fresh_sha(Path(__file__))}
        extra = [Path(__file__), proof_path,
                 ROOT / 'analysis/refresh_optimization_boundary_evidence_20261004.py',
                 ROOT / 'analysis/optimization_20261003_r61/provenance_scope_execution.json']
        return original_scope(module, [*sources, *extra], metadata, analysis_root)

    scopes.FrozenProvenanceExecutionScope = factory
    try:
        original.main(62)
    finally:
        scopes.FrozenProvenanceExecutionScope = original_scope


if __name__ == '__main__':
    main()
