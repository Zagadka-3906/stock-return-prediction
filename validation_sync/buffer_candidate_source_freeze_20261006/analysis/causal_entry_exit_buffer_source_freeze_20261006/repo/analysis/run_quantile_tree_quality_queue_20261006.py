"""Run full R91/R92 only after closed native work and publish each full validation."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_tree_quality_queue_20261006'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def state(**extra):
    value = {'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'pid': os.getpid(),
        'required_quality_rounds': [91, 92], 'expected_full_quality_records': 198,
        'existing_required_rounds_and_original_queue_preserved': True,
        'physical_resource_boundary_established': False, 'test_labels_read': False, **extra}
    path = OUT / 'state.json'
    temporary = path.with_suffix('.next')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def main():
    from run_dependency_queue_v3_20261006 import owned
    from windows_hidden_process_launch_20261006 import launch
    from hidden_windows_child_creation_20261006 import install
    restore = install()
    plan = read(OUT / 'plan.json')
    for source, digest in plan['input_sha256'].items():
        assert sha(source) == digest, source
    full_service = A / 'service_owned_workflows_20261006/quantile_tree_full_workflow'
    proof = A / 'quantile_tree_future_qa_20261006/verification.json'
    generator = A / 'quantile_tree_quality_generator_preflight_v2_20261006/verification.json'
    codec = A / 'quantile_tree_codec_preflight_20261006/verification.json'
    closed = []
    try:
        for number, parent, expected in ((91, 90, 100), (92, 91, 98)):
            while True:
                launch_row = read(full_service / 'native_launch.json')
                terminal = full_service / 'service_execution.json'
                ready = (proof.exists() and terminal.exists()
                    and read(proof).get('status') == read(terminal).get('status') == 'passed'
                    and not owned(launch_row))
                if ready:
                    import qualified_round_recovery_evidence_v3_20261006 as qualification
                    try:
                        if qualification.complete_round_evidence(parent) is not None:
                            break
                    finally:
                        qualification.close()
                state(stage='waiting_closed_full24_native_fits_and_qualified_predecessor',
                    round=number, explicit_parent_round=parent, completed_quality_rounds=closed,
                    native_full_workflow_owned_live=owned(launch_row),
                    actual_quality_records_completed=0)
                time.sleep(30)
            assert read(generator)['status'] == read(codec)['status'] == 'passed'
            assert read(proof)['actual_full_final_fits'] == 4
            storage = read(A / 'quantile_tree_storage_20261006.json')
            bank = Path(storage['output_directory'])
            assert read(bank / 'oof_audit.json')['actual_annual_fits'] == 20
            assert read(bank / 'training_execution_scope.json')['status'] == 'passed'
            publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
            assert owned(publisher), 'The independently owned complete main publisher must be live.'
            folder = OUT / f'round{number}'
            folder.mkdir()
            driver = A / f'run_training_round{number}_v3_pipeline.py'
            bridge = A / 'run_quantile_quality_qualified_workflow_20261006.py'
            run_path = folder / 'qualified_run.json'
            create(run_path, {'round': number, 'original_driver': str(driver), 'original_arguments': [],
                'input_sha256': {**plan['input_sha256'], str(OUT / 'plan.json'): sha(OUT / 'plan.json')},
                'full_original_grid_and_native_controls_required': True, 'new_quality_scores_by_launcher': 0})
            scratch = Path(storage['temporary_directory']) / f'round{number}'
            scratch.mkdir(parents=True)
            assert scratch.drive.upper() in ('D:', 'E:')
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
            for key in ('TMP', 'TEMP', 'TMPDIR'):
                environment[key] = str(scratch)
            with (folder / 'stdout.log').open('xb') as out, (folder / 'stderr.log').open('xb') as err:
                process = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8',
                    str(bridge), str(driver), str(run_path)], cwd=ROOT, env=environment, stdout=out, stderr=err)
            time.sleep(.5)
            assert process.poll() is None
            root = psutil.Process(process.pid)
            children = [p for p in root.children(recursive=True)
                if p.name().lower() == 'python.exe' and p.cmdline()[1:] == root.cmdline()[1:]]
            assert len(children) == 1
            row = {'round': number, 'pid': root.pid, 'owned_parent_creation_time': root.create_time(),
                'script': str(bridge), 'script_args': [str(driver), str(run_path)],
                'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time()}
            create(folder / 'native_launch.json', row)
            while process.poll() is None:
                state(stage='actual_full_continuous_official_scheme_validation', round=number,
                    explicit_parent_round=parent, current_quality_job=row,
                    current_quality_worker_owned_live=owned(row), completed_quality_rounds=closed,
                    required_current_round_records=expected)
                time.sleep(15)
            assert process.returncode == 0, (folder / 'stderr.log').read_text(encoding='utf-8')[-3000:]
            import qualified_round_recovery_evidence_v3_20261006 as qualification
            try:
                evidence = qualification.complete_round_evidence(number)
                assert evidence is not None and evidence['scored_records'] == expected
            finally:
                qualification.close()
            receipt = A / f'github_validation_sync_main_20261005/round{number}_receipt.json'
            while not receipt.exists():
                state(stage='waiting_full_round_main_publication', round=number,
                    actual_current_full_quality_records=expected, completed_quality_rounds=closed)
                time.sleep(15)
            published = read(receipt)
            assert published['status'] == 'pushed_and_remote_head_verified'
            assert published['branch'] == 'main' and published['scored_records'] == expected
            assert published['raw_git_blobs_verified'] > 0
            assert published['official_score'] == evidence['score']
            closed.append(number)
        state(stage='completed_full198_records_frozen_causal_candidates_rankings_and_main_publications',
            completed_quality_rounds=closed, actual_full_quality_records_completed=198,
            global_goal_complete=False)
    finally:
        create(OUT / 'actual_hidden_child_creations.json', {'events': restore()})


if __name__ == '__main__':
    main()
