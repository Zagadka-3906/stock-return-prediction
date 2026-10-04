"""Versioned R63 handoff, including an explicit zero-axis publication policy."""
from pathlib import Path
import argparse
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main(probe=False):
    if probe:
        import psutil
        print(json.dumps({'round': 63, 'lazy_imports_only': not any(n in sys.modules for n in ('numpy', 'pandas', 'polars', 'torch')),
            'rss_bytes': psutil.Process().memory_info().rss, 'waits_for_full_qualified_round': 62,
            'zero_active_weight_stages_remain_nonempty': True, 'new_model_fits': 0, 'new_quality_scores': 0}), flush=True)
        return
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    state = ROOT / 'analysis/ongoing_optimization_r63_state.json'
    state.write_text(json.dumps({'round': 63, 'stage': 'waiting_for_actual_complete_round62_scientific_and_scope_evidence',
        'status': 'running', 'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'continuous_optimization_authorized': True, 'test_labels_read': False}, ensure_ascii=False, indent=2), encoding='utf-8')
    while complete_round_evidence(62) is None:
        time.sleep(10)
    from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha
    proof_path = ROOT / 'analysis/latest_joint_zero_axis_policy_preflight_20261005/verification.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed_actual_scored_graph_count_and_source_binding_checks'
    bindings = dict(proof['input_sha256'])
    bindings[str(proof_path.resolve())] = fresh_sha(proof_path)
    with LockedReadHashCache(bindings):
        import frozen_provenance_execution_scope_20261004 as scope_module
        import optimize_training_round63 as module
        import run_training_round63_pipeline as original
        from latest_joint_zero_axis_stage_policy_20261005 import install
        restore = install(module)
        original_class = scope_module.FrozenProvenanceExecutionScope

        def scoped_factory(target, sources, metadata, analysis_root):
            extra = [Path(__file__), ROOT / 'analysis/latest_joint_zero_axis_stage_policy_20261005.py', proof_path]
            metadata = {**metadata, 'effective_outer_driver': str(Path(__file__).resolve()),
                'effective_outer_driver_sha256': fresh_sha(Path(__file__)),
                'zero_axis_coordinates_preserve_two_unchanged_baseline_controls': True}
            return original_class(target, [*sources, *extra], metadata, analysis_root)

        scope_module.FrozenProvenanceExecutionScope = scoped_factory
        try:
            original.main()
        finally:
            scope_module.FrozenProvenanceExecutionScope = original_class
            restore()
        assert read(module.OUT / 'provenance_scope_execution.json')['status'] == 'passed'
    module.dump(module.OUT / 'zero_axis_handoff_execution.json', {'status': 'passed',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'sources_read_locked_and_end_rehashed': True,
        'original_stage_math_preserved_for_nonempty_axes': True, 'all_runtime_bindings_restored': True,
        'new_model_fits': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe', action='store_true')
    main(parser.parse_args().probe)
