"""Retry the sealed full R81 recovery with unique QA and profile directories."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    source = A / 'recover_round81_ranking_publication_20261006.py'
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == 'e24eec461047303464bb265e9585cb75e67293ca7fa21903e36138270d579033'
    text = data.decode('utf-8')
    replacements = {
        'recovery_frozen_execution_20261006.json': ('recovery_frozen_execution_v2_20261006.json', 1),
        'publication_recovery_execution_20261006.json': ('publication_recovery_execution_v2_20261006.json', 1),
        'publication_recovery_failure_20261006.json': ('publication_recovery_failure_v2_20261006.json', 1),
        'recovery_full_ranking_snapshot_20261006.json.gz': ('recovery_full_ranking_snapshot_v2_20261006.json.gz', 1),
        'verify_lossless_ranking_display_v2_20261006': ('verify_lossless_ranking_display_v3_20261006', 2),
        'lossless_ranking_display_qa_v2_20261006': ('lossless_ranking_display_qa_v3_20261006', 1),
    }
    for before, (after, expected) in replacements.items():
        assert text.count(before) == expected, before
        text = text.replace(before, after)
    before = '    assert not FROZEN.exists() and not SCOPE.exists()'
    after = '''    prior = read(FOLDER / 'publication_recovery_failure_20261006.json')
    assert prior['status'] == 'failed_preserved_actual_recovery'
    assert prior['failure'].startswith('FileExistsError:') and 'ranking_display_qa_20261006' in prior['failure']
    old_service = read(A / 'service_owned_workflows_20261006/round81_publication_recovery/service_execution.json')
    assert old_service['status'] == 'failed' and old_service['failure'] == prior['failure']
    old_launch = read(A / 'service_owned_workflows_20261006/round81_publication_recovery/native_launch.json')
    for pid, birth in ((old_launch['pid'], old_launch['owned_parent_creation_time']),
                       (old_launch['owned_worker_pid'], old_launch['owned_worker_creation_time'])):
        try:
            assert abs(psutil.Process(pid).create_time() - birth) > 1e-5
        except psutil.NoSuchProcess:
            pass
    assert not FROZEN.exists() and not SCOPE.exists()'''
    assert text.count(before) == 1
    text = text.replace(before, after)
    before = '    for path in dict.fromkeys(paths):'
    after = '''    paths += [A / 'recover_round81_ranking_publication_20261006.py',
        A / 'verify_lossless_ranking_display_v2_20261006.py',
        FOLDER / 'recovery_frozen_execution_20261006.json',
        FOLDER / 'publication_recovery_failure_20261006.json',
        A / 'service_owned_workflows_20261006/round81_publication_recovery/job_definition.json',
        A / 'service_owned_workflows_20261006/round81_publication_recovery/native_launch.json',
        A / 'service_owned_workflows_20261006/round81_publication_recovery/service_execution.json']
    for path in dict.fromkeys(paths):'''
    assert text.count(before) == 1
    text = text.replace(before, after)
    before = "'test_labels_read': False}"
    after = "'test_labels_read': False, 'previous_directory_collision_failure_preserved': True, 'QA_and_profile_output_paths_both_unique_for_actual_retry': True}"
    assert text.count(before) == 2
    text = text.replace(before, after)
    namespace = {'__name__': 'actual_round81_publication_recovery_v2', '__file__': str(Path(__file__).resolve())}
    exec(compile(text, str(Path(__file__).resolve()), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
