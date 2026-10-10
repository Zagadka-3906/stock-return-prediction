"""Version the idle waiter to verify publisher sleep before holding it."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import create, sha


def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def main():
    original = A / 'publish_bounded_root_full_controls_waiter_20261006.py'
    publisher = original.read_text(encoding='utf-8')
    begin = publisher.index('    root, worker = helpers.owned_pair(')
    end = publisher.index("        previous = sync.git('rev-parse', 'HEAD')", begin)
    publisher = publisher[:begin] + '''    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    suspended = []
    restore = install()
    try:
        assert identity['name'] == 'main_publisher_v7'
        root, worker, idle = suspended_idle(identity,
            '    main (watch_validations_main_v7_20261006.py:71)')
        suspended.extend((worker, root))
        create(out / 'actual_publisher_idle_before_and_after_hold.json', idle)
''' + publisher[end:]
    publisher = publisher.replace('bounded_root_full_controls_waiter_20261006',
                                  'bounded_root_full_controls_waiter_v2_20261006')
    publisher = publisher.replace('bounded_root_full_controls_{phase}_',
                                  'bounded_root_full_controls_v2_{phase}_')
    publisher = publisher.replace("*folder.glob('*.json')]", "*folder.glob('*.json'),\n        *(A / 'bounded_root_waiter_safe_publication_adoption_20261006').glob('*.json')]")
    waiter = (A / 'wait_bounded_root_full_controls_20261006.py').read_text(encoding='utf-8')
    waiter = waiter.replace('bounded_root_full_controls_waiter_20261006',
                            'bounded_root_full_controls_waiter_v2_20261006')
    waiter = replace_once(waiter,
        "        A / 'windows_hidden_process_launch_20261006.py')}",
        "        A / 'windows_hidden_process_launch_20261006.py',\n"
        "        A / 'prepare_root_waiter_safe_publication_v2_20261006.py',\n"
        "        A / 'launch_bounded_root_full_controls_waiter_v2_20261006.py',\n"
        "        A / 'bounded_root_waiter_safe_publication_preparation_20261006.json',\n"
        "        A / 'bounded_root_waiter_safe_publication_adoption_20261006/activation.json')}")
    waiter = replace_once(waiter, "    try: main()", "    while not (A / 'bounded_root_waiter_safe_publication_adoption_20261006/activation.json').exists():\n        time.sleep(.25)\n    try: main()")
    files = {
        A / 'publish_bounded_root_full_controls_waiter_v2_20261006.py': publisher,
        A / 'wait_bounded_root_full_controls_waiter_v2_20261006.py': waiter,
    }
    # The original file name starts with wait_bounded, not wait_bounded...waiter.
    files[A / 'wait_bounded_root_full_controls_v2_20261006.py'] = files.pop(
        A / 'wait_bounded_root_full_controls_waiter_v2_20261006.py')
    publisher_path = A / 'publish_bounded_root_full_controls_waiter_v2_20261006.py'
    files[publisher_path] = replace_once(files[publisher_path],
        "A / 'wait_bounded_root_full_controls_20261006.py'",
        "A / 'wait_bounded_root_full_controls_v2_20261006.py'")
    for path, source in files.items():
        compile(source, str(path), 'exec')
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(source)
    create(A / 'bounded_root_waiter_safe_publication_preparation_20261006.json', {
        'status': 'prepared_versioned_waiter_with_actual_publisher_sleep_gate',
        'original_sources': {str(p): sha(p) for p in (
            original, A / 'wait_bounded_root_full_controls_20261006.py',
            A / 'verify_bounded_root_replay_full_controls_20261006.py',
            A / 'bounded_root_replay_memoization_20261006.py')},
        'new_sources': {str(p): sha(p) for p in files},
        'full_scientific_control_harness_and_14GiB_admission_unchanged': True,
        'queue10_actual_handoff_still_required': True,
        'no_child_tree_alone_is_not_a_publisher_idle_proof': True,
        'new_quality_scores': 0, 'new_native_fits': 0,
        'runtime_adopted': False, 'test_labels_read': False})


if __name__ == '__main__':
    main()
