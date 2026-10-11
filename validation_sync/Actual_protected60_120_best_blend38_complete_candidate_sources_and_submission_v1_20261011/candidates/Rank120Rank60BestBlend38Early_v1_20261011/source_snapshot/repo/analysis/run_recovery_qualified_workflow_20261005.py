"""Execute unchanged queued drivers with explicit recovered-R66 provenance."""
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
    assert run['original_driver'] == str(driver)
    assert run['original_arguments'] == arguments
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, digest in run['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    import qualified_round_recovery_evidence_v2_20261005 as qualification
    import refresh_optimization_boundary_evidence_20261004 as base
    base.complete_round_evidence = qualification.complete_round_evidence
    import standalone_root_source_adapter_20261005 as adapter
    import optimize_training_round50 as root_sources
    restore_sources = adapter.install(root_sources)
    import frozen_provenance_execution_scope_20261004 as provenance
    original_scope = provenance.FrozenProvenanceExecutionScope
    additions = [Path(__file__).resolve(), run_path,
        A / 'qualified_round_recovery_evidence_20261005.py',
        A / 'qualified_round_recovery_evidence_v2_20261005.py',
        A / 'standalone_root_source_adapter_20261005.py',
        A / 'standalone_root_source_adapter_preflight_20261005/verification.json']

    def extended_scope(module, extra_sources, driver_metadata, analysis_root):
        extra_sources = list(dict.fromkeys([*extra_sources, *additions]))
        metadata = {**driver_metadata, 'effective_recovery_launcher': str(Path(__file__).resolve()),
            'recovery_launcher_run': str(run_path),
            'actual_R66_recovery_scope_required': True,
            'standalone_empty_root_resolved_before_candidate_lookup': True,
            'original_frozen_scientific_sources_unchanged': True}
        return original_scope(module, extra_sources, metadata, analysis_root)

    provenance.FrozenProvenanceExecutionScope = extended_scope
    sys.argv = [str(driver), *arguments]
    print(json.dumps({'status': 'recovery_qualification_bridge_installed',
        'original_driver': str(driver), 'run': str(run_path),
        'only_publication_branch': 'main', 'new_quality_scores_by_bridge': 0,
        'test_labels_read': False}, ensure_ascii=False), flush=True)
    try:
        runpy.run_path(str(driver), run_name='__main__')
    finally:
        provenance.FrozenProvenanceExecutionScope = original_scope
        restore_sources()
        qualification.close()


if __name__ == '__main__':
    main()
