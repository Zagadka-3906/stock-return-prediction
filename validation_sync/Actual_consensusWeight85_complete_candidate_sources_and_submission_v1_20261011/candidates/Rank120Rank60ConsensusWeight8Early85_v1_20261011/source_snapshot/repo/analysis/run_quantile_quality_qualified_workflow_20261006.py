"""Run prospective full grids with strict recovered predecessors and hidden children."""
from pathlib import Path
import json
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    driver, run_path, *arguments = sys.argv[1:]
    driver, run_path = Path(driver).resolve(), Path(run_path).resolve()
    run = json.loads(run_path.read_text(encoding='utf-8-sig'))
    number = run['round']
    assert number in (91, 92)
    assert run['original_driver'] == str(driver) and run['original_arguments'] == arguments
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, digest in run['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    import qualified_round_recovery_evidence_v3_20261006 as qualification
    import refresh_optimization_boundary_evidence_20261004 as base
    old_gate = base.complete_round_evidence
    base.complete_round_evidence = qualification.complete_round_evidence
    import standalone_root_source_adapter_20261005 as adapter
    import optimize_training_round50 as root_sources
    restore_sources = adapter.install(root_sources)
    from hidden_windows_child_creation_20261006 import install as hide_children
    restore_children = hide_children()
    from lossless_ranking_runtime_adapter_v2_20261006 import install as lossless
    restore_ranking = lossless(number)
    import frozen_provenance_execution_scope_20261004 as provenance
    original_scope = provenance.FrozenProvenanceExecutionScope
    additions = [Path(__file__).resolve(), run_path, *[A / filename for filename in (
        'qualified_round_recovery_evidence_20261005.py',
        'qualified_round_recovery_evidence_v2_20261005.py',
        'qualified_round_recovery_evidence_v3_20261006.py',
        'standalone_root_source_adapter_20261005.py',
        'standalone_root_source_adapter_preflight_20261005/verification.json',
        'hidden_windows_child_creation_20261006.py',
        'lossless_ranking_runtime_adapter_v2_20261006.py',
        'build_lossless_ranking_display_20261006.py',
        'build_lossless_ranking_display_v3_20261006.py',
        'verify_lossless_ranking_display_20261006.py',
        'verify_lossless_ranking_display_v5_20261006.py')]]

    def extended_scope(module, extra_sources, driver_metadata, analysis_root):
        extra_sources = list(dict.fromkeys([*extra_sources, *additions]))
        metadata = {**driver_metadata, 'effective_recovery_launcher': str(Path(__file__).resolve()),
            'recovery_launcher_run': str(run_path), 'actual_R66_and_R81_recoveries_required_where_referenced': True,
            'standalone_empty_root_resolved_before_candidate_lookup': True,
            'lossless_full_ranking_and_complete_actual_browser_QA_required': True,
            'all_child_processes_explicitly_hidden_including_multiprocessing': True,
            'original_frozen_scientific_sources_unchanged': True}
        return original_scope(module, extra_sources, metadata, analysis_root)

    provenance.FrozenProvenanceExecutionScope = extended_scope
    sys.argv = [str(driver), *arguments]
    print(json.dumps({'status': 'strict_recovery_lossless_ranking_and_hidden_child_bridge_installed',
        'round': number, 'original_driver': str(driver), 'run': str(run_path),
        'only_publication_branch': 'main', 'new_quality_scores_by_bridge': 0,
        'test_labels_read': False}, ensure_ascii=False), flush=True)
    try:
        runpy.run_path(str(driver), run_name='__main__')
    finally:
        provenance.FrozenProvenanceExecutionScope = original_scope
        restore_ranking()
        restore_sources()
        base.complete_round_evidence = old_gate
        try:
            qualification.close()
        finally:
            events = restore_children()
            with (run_path.parent / 'hidden_child_process_launches.json').open('x', encoding='utf-8') as stream:
                json.dump({'actual_child_creations': events, 'all_creation_flags_restored': True},
                    stream, ensure_ascii=False, indent=2)
                stream.write('\n')


if __name__ == '__main__':
    main()
