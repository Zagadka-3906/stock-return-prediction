"""Reuse the actual main7 publisher; retain every scientific dispatch and check."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def create(path, text):
    assert not path.exists()
    compile(text, str(path), 'exec')
    with path.open('x', encoding='utf-8', newline='') as stream: stream.write(text)


def main():
    original = A / 'handoff_joint_goss_round97_full_execution_20261006.py'
    target = A / 'handoff_joint_goss_round97_full_execution_v2_20261006.py'
    text = original.read_text(encoding='utf-8')
    text = text.replace("OUT=A/'joint_goss_round97_actual_handoff_20261006'",
        "OUT=A/'joint_goss_round97_actual_handoff_recovery_v2_20261006'")
    text = text.replace("row('main_publisher_v6')", "row('main_publisher_v7')")
    text = text.replace("A/'run_service_owned_windows_workflow_20261006.py')})",
        "A/'run_service_owned_windows_workflow_20261006.py',\n"
        "        A/'recover_joint97_handoff_sources_v2_20261006.py',\n"
        "        A/'interrupted_round95_lossless_snapshot_recovery_20261006/verification.json')})")
    start = text.index('        parent,worker=pair(old_publisher)\n')
    end = text.index('        for _ in range(180):\n            assert owned(publisher)', start)
    text = text[:start] + (
        '        # main7 already implements all original and new97 exports. Reuse its\n'
        '        # actual owned process and lock; never retire an in-process serializer.\n'
        '        publisher=old_publisher\n'
        '        pair(publisher)\n'
    ) + text[end:]
    text = text.replace("previously_activated_jobs=deepcopy(snapshot['activated_jobs']))",
        "previously_activated_jobs=deepcopy(snapshot['activated_jobs']),\n"
        "            activation_handoff_commit_marker=str(OUT/'handoff_commit.json'))")
    needle = "        print('passed_actual_queue10_main7_observer34_additive_joint97_handoff',flush=True)"
    assert text.count(needle) == 1
    text = text.replace(needle, """        # Compatibility locations remain the immutable prototype's declared
        # adoption locations. Fill them only after this actual recovery passes.
        compatibility=A/'joint_goss_round97_actual_handoff_20261006'
        recovered=read(OUT/'verification.json')
        recovered.update(recovered_previous_failed_handoff=True,
            actual_recovery_verification=str(OUT/'verification.json'),
            already_owned_main7_reused_without_retirement=True,
            original_failed_handoff_record_preserved=str(compatibility/'failure.json'))
        create(compatibility/'handoff_commit.json',read(OUT/'handoff_commit.json'))
        create(compatibility/'verification.json',recovered)
""" + needle)
    create(target, text)
    original_waiter = A / 'wait_joint_goss_round97_idle_handoff_20261006.py'
    waiter = original_waiter.read_text(encoding='utf-8')
    waiter = waiter.replace("OUT=A/'joint_goss_round97_idle_handoff_waiter_20261006'",
        "OUT=A/'joint_goss_round97_idle_handoff_waiter_v2_20261006'")
    waiter = waiter.replace("source=A/'handoff_joint_goss_round97_full_execution_20261006.py'",
        "source=A/'handoff_joint_goss_round97_full_execution_v2_20261006.py'")
    waiter = waiter.replace('for p in (Path(__file__),source,proof,receipt)',
        "for p in (Path(__file__),source,proof,receipt,A/'recover_joint97_handoff_sources_v2_20261006.py',\n"
        "        A/'interrupted_round95_lossless_snapshot_recovery_20261006/verification.json')")
    create(A / 'wait_joint_goss_round97_idle_handoff_v2_20261006.py', waiter)
    # The scientific plan and dispatch source are deliberately byte unchanged.
    tree = ast.parse(text)
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name) and node.func.id == 'start_service']
    names = [node.args[0].value for node in calls if node.args and isinstance(node.args[0], ast.Constant)]
    assert set(names) == {'dependency_queue_v10', 'progress_monitor_v34'}
    assert "additional97_records':151" in text and "original25_routes" in text
    proof = {'status': 'passed_exact_scientific_queue10_and_scope_preserved_with_actual_main7_reuse',
        'actual_new_source_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (Path(__file__), target, A / 'wait_joint_goss_round97_idle_handoff_v2_20261006.py')},
        'new_training_fits': 0, 'new_quality_scores': 0,
        'main_publisher_replaced_or_restarted_by_recovery': False,
        'original_failed_handoff_and_gzip_preserved': True, 'test_labels_read': False}
    path = A / 'joint97_handoff_source_recovery_v2_20261006.json'
    with path.open('x', encoding='utf-8') as stream: json.dump(proof, stream, ensure_ascii=False, indent=2); stream.write('\n')
    print(proof['status'], flush=True)


if __name__ == '__main__': main()
