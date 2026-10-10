"""Freeze and launch the missing93/94 full publication path with no visible console."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from collect_full_lossless_round_publication_20261006 import read, sha
from handoff_distribution_views_progress_monitor_20261006 import create
from run_dependency_queue_v3_20261006 import owned
from launch_service_owned_workflow_with_pwsh_20261006 import launch


def main():
    preflight_path = A / 'distribution_views_full_publication_collector_preflight_20261006/verification.json'
    preflight = read(preflight_path)
    assert preflight['status'] == 'passed_actual_full138_record_round82_collector_and_committed_blob_match'
    assert preflight['actual_raw_git_blobs_matching'] == 10
    for source, digest in preflight['input_sha256'].items():
        assert sha(source) == digest
    main_service = A / 'service_owned_workflows_20261006/main_publisher_v5'
    main_definition = read(main_service / 'job_definition.json')
    assert owned(read(main_service / 'native_launch.json'))
    for name in ('quantile_tree_quality_queue_v2', 'quantile_distribution_views_quality_queue'):
        assert owned(read(A / f'service_owned_workflows_20261006/{name}/native_launch.json'))
    original = read(A / 'quantile_tree_quality_queue_v2_20261006/plan.json')
    new = read(A / 'quantile_distribution_views_quality_queue_20261006/plan.json')
    assert original['expected_full_records'] == [100, 98] and new['quality_records'] == [124, 138]
    pins = dict(main_definition['input_sha256'])
    sources = [Path(__file__).resolve(), preflight_path, *[A / name for name in (
        'collect_full_lossless_round_publication_20261006.py',
        'distribution_views_lossless_publication_adapter_20261006.py',
        'verify_distribution_views_full_publication_collector_20261006.py',
        'run_distribution_views_full_ranking_publisher_20261006.py',
        'immutable_lossless_ranking_snapshot_20261006.py',
        'verified_round_main_publication_20261006.py',
        'publish_classifier_consensus_workflows_20261006.py',
        'sync_validated_rounds_main_20261005.py',
        'build_lossless_ranking_display_v2_20261006.py',
        'publish_main_closeout_v2_20261005.py',
        'finalize_main_branch_consolidation_20261005.py',
        'watch_validations_main_v2_20261005.py',
        'qualified_round_recovery_evidence_20261005.py',
        'qualified_round_recovery_evidence_v2_20261005.py',
        'qualified_round_recovery_evidence_v3_20261006.py',
        'hidden_windows_child_creation_20261006.py',
        'atomic_optimization_observer_writes_20261005.py',
        'quantile_tree_quality_queue_v2_20261006/plan.json',
        'quantile_distribution_views_quality_queue_20261006/plan.json')]]
    pins.update({str(path.resolve()): sha(path) for path in sources})
    for plan in (original, new):
        for source, digest in plan['input_sha256'].items():
            assert sha(source) == digest
    for source, digest in pins.items():
        assert sha(source) == digest
        if Path(source).suffix == '.py':
            compile(Path(source).read_text(encoding='utf-8-sig'), source, 'exec')
    service = A / 'service_owned_workflows_20261006/distribution_views_full_ranking_publisher'
    assert not service.exists() and not (A / 'distribution_views_full_ranking_publisher_20261006').exists()
    service.mkdir()
    run_path = service / 'publisher_run.json'
    create(run_path, {'status': 'frozen_before_actual93_94_full_publication_wait',
        'required_rounds': [93, 94], 'expected_records': [124, 138], 'input_sha256': pins,
        'original198_and_new262_scientific_plans_preserved': True,
        'main5_preserved_and_temporarily_suspended_only_while_idle': True,
        'primary_export_or_complete_supplement_both_preserve_all_full_values_and_QA': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    definition_path = service / 'job_definition.json'
    create(definition_path, {'name': 'distribution_views_full_ranking_publisher',
        'driver': str(A / 'run_distribution_views_full_ranking_publisher_20261006.py'),
        'arguments': [str(run_path)], 'scratch': str(ROOT / 'tmp/service_owned_distribution_views_full_ranking_publisher'),
        'input_sha256': {**pins, str(run_path): sha(run_path)},
        'bootstrap_sha256': sha(A / 'run_service_owned_windows_workflow_20261006.py'),
        'command_line': subprocess.list2cmdline([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
            str(A / 'run_service_owned_windows_workflow_20261006.py'), str(definition_path)])})
    result = launch(definition_path, Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'))
    create(service / 'verified_hidden_launch.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
