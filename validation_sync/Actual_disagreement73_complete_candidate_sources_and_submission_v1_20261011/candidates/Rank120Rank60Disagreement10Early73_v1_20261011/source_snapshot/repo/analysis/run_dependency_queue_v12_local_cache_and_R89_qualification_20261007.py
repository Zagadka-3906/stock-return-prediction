"""Retain all32 original routes; qualify alternate R89 and use tested parent cache for R90."""
from pathlib import Path
import inspect
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha


def source_namespace(plan):
    import run_dependency_queue_v3_20261006 as previous
    source = A / 'run_dependency_queue_v10_20261006.py'
    assert sha(source) == plan['original_controller_source_sha256']
    text = source.read_text(encoding='utf-8')
    patches = {
        '    if number in (66, 81):': '    if number in (66, 81, 89):',
        '        import qualified_round_recovery_evidence_v3_20261006 as qualification':
            '        import qualified_round_recovery_evidence_v4_20261007 as qualification',
        "else 'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py'":
            "else 'run_classifier_consensus_round90_with_precise_gate_and_parent_cache_20261007.py' if job['round']==90 else 'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py'",
        '    run.update(dependency_queue_plan=str(plan_path),':
            "    run.update(name=job['name'], recovery_driver_sha256=previous.sha(A / 'run_reboot_recovery_attempt_20261006.py'), dependency_queue_plan=str(plan_path),",
    }
    effective = text
    for before, after in patches.items():
        assert effective.count(before) == 1, before
        effective = effective.replace(before, after)
    restored = effective
    for before, after in reversed(list(patches.items())):
        assert restored.count(after) == 1
        restored = restored.replace(after, before)
    assert restored == text
    namespace = {'__file__': str(source), '__name__': 'actual_all_original_routes_local_cache_v12'}
    exec(compile(effective, str(source), 'exec'), namespace)
    original_ready = namespace['ready']
    def serialized_ready(job, jobs):
        if job['gate'].get('quality_slot'):
            for path in plan['complete_ranking_registration_serialization_markers']:
                if not previous.marker(path, ['passed']):
                    return False
        return original_ready(job, jobs)
    namespace['ready'] = serialized_ready
    return namespace, effective, patches


def main():
    import run_dependency_queue_v3_20261006 as previous
    plan = read(Path(sys.argv[1]))
    proof = read(A / 'dependency_queue_v12_local_cache_routes_preflight_20261007/verification.json')
    assert proof['status'] == 'passed_original32_routes_and_R90_only_dispatch_and_strict89_qualification_source_controls'
    main_source = inspect.getsource(previous.main)
    before = "    state_path = plan_path.parent / 'state.json'"
    assert main_source.count(before) == 1
    main_source = main_source.replace(before, "    state_path = Path(plan['shared_original_state_path'])")
    exec(compile(main_source, str(A / 'run_dependency_queue_v12_shared_state_main_20261007.py'), 'exec'), vars(previous))
    namespace, _, _ = source_namespace(plan)
    namespace['main']()


if __name__ == '__main__':
    main()
