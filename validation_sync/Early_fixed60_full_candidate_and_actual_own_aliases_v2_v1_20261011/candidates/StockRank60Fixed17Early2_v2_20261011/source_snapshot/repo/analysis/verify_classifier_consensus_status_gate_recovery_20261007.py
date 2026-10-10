"""Actual strict route-gate checks, negative controls and preservation of the failed R89 scope."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import ast
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from run_dependency_queue_v3_20261006 import read, create, sha
    import classifier_consensus_status_gate_recovery_runtime_20261007 as adapter
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out = A / 'classifier_consensus_status_gate_recovery_preflight_20261007'
    assert not out.exists()
    out.mkdir()
    failed_path = A / 'optimization_20261003_r89/provenance_scope_execution.json'
    failed = read(failed_path)
    assert failed['status'] == 'failed' and failed['scope_started'] is False
    assert not (failed_path.parent / 'protocol.json').exists()
    pins = {**read(adapter.PROOF)['input_sha256'], **{str(p): sha(p) for p in (Path(__file__), Path(adapter.__file__), adapter.SOURCE, adapter.PROOF, failed_path)}}
    create(out / 'frozen_before_actual_strict_gate_controls.json', {'input_sha256': pins,
        'original_failed_scope_sha256': sha(failed_path), 'original_route_proof_sha256': sha(adapter.PROOF),
        'no_original_proof_or_science_source_or_failed_scope_rewrite': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    with LockedReadHashCache(pins) as scope:
        ns = SimpleNamespace(read=read, sha=scope.sha)
        adapter.verify_gate(ns, adapter.PROOF)
        original, patched, effective = adapter.patched_namespace()
        ast.parse(effective)
        assert patched['WEIGHTS'] == original.WEIGHTS
        assert patched['RETENTIONS'] == original.RETENTIONS
        assert patched['ROLES'] == original.ROLES and patched['ALPHAS'] == original.ALPHAS
        assert patched['AUXILIARY'] == original.AUXILIARY
        negatives = []
        actual = read(adapter.PROOF)
        for name in ('status', 'missing_check', 'false_bit_control', 'wrong_input_sha', 'test_labels_read'):
            bad = deepcopy(actual)
            if name == 'status': bad['status'] = 'passed'
            elif name == 'missing_check': bad['checks'].pop()
            elif name == 'false_bit_control': bad['checks'][0]['direct_and_future_routes_bit_identical'] = False
            elif name == 'wrong_input_sha': bad['input_sha256'][next(iter(bad['input_sha256']))] = '0' * 64
            else: bad['test_labels_read'] = True
            try:
                adapter.verify_gate(SimpleNamespace(read=lambda p: bad, sha=scope.sha), adapter.PROOF)
            except AssertionError:
                negatives.append(name)
            else:
                raise AssertionError(name)
        assert len(negatives) == 5
        scope.reverify()
    create(out / 'verification.json', {'status': 'passed_actual_precise_completed_route_gate_and_negative_controls_original_sources_preserved',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'actual12_direct_2020_2025_and4_inherited_bit_proofs_checked': True,
        'all_actual_route_proof_inputs_full_initial_and_final_hash_read_locks': True,
        'negative_controls_rejected': negatives, 'original_failed_scope_sha256': sha(failed_path),
        'only_one_exact_gate_line_diff_reverse_restored': True, 'all_original_parameter_grids_unchanged': True,
        'original_expected_round89_124_and_round90_138_grids_retained': True,
        'original_failed_R89_scope_still_failed_and_preserved': True,
        'R89_scientific_retry_and_alternate_scope_qualification_not_yet_executed': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
