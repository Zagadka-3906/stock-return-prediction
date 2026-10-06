"""Preserve the interrupted main6 gzip and rerun the unchanged exact serializer."""
from pathlib import Path
import ast
import gzip
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import pair, stack

OUT = A / 'interrupted_round95_lossless_snapshot_recovery_20261006'


def main():
    assert not OUT.exists()
    OUT.mkdir()
    display = (A / 'lossless_ranking_display_v2_20261006/round95').resolve()
    snapshot = display / 'full_report_reconstructed_for_publication.json.gz'
    interrupted = display / 'full_report_reconstructed_for_publication.interrupted_main6_20261006.json.gz'
    verification = display / 'full_report_publication_snapshot_verification.json'
    report = ROOT / 'results/all_model_rankings_20261003.json'
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    assert owned(publisher)
    original = A / 'immutable_lossless_ranking_snapshot_20261006.py'
    proof = read(display / 'verification.json')
    assert sha(report) == proof['original_report_sha256']
    assert snapshot.exists() and not verification.exists() and not interrupted.exists()
    assert snapshot.resolve().is_relative_to(display) and interrupted.resolve().parent == display
    sources = [Path(__file__), original, display / 'verification.json', report,
        A / 'watch_validations_main_v7_20261006.py']
    pins = {str(path): sha(path) for path in sources}
    create(OUT / 'frozen_before_actual_recovery.json', {
        'input_sha256': pins, 'publisher': publisher, 'orphan_snapshot_sha256': sha(snapshot),
        'original_full_report_sha256': proof['original_report_sha256'],
        'scientific_sources_and_all10570_records_unchanged': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    parent, worker = pair(publisher)
    tree = ast.parse((A / 'watch_validations_main_v7_20261006.py').read_text(encoding='utf-8'))
    sleeps = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute) and node.func.attr == 'sleep'
        and len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and node.args[0].value == 45]
    assert len(sleeps) == 1
    needle = f'    main (watch_validations_main_v7_20261006.py:{sleeps[0]})'
    suspended = []
    try:
        while True:
            assert owned(publisher)
            before = stack(worker.pid)
            if needle not in before or worker.children():
                time.sleep(1)
                continue
            worker.suspend(); suspended.append(worker)
            parent.suspend(); suspended.append(parent)
            after = stack(worker.pid)
            if needle in after and not worker.children(): break
            for process in reversed(suspended): process.resume()
            suspended = []
            time.sleep(1)
        create(OUT / 'actual_publisher_idle_boundary.json', {
            'status': 'passed_original_publisher_idle_before_and_after_hold',
            'before': before, 'after': after, 'scientific_workers_held': 0})
        try:
            with gzip.open(snapshot, 'rb') as stream: hashlib.file_digest(stream, 'sha256')
        except EOFError as error:
            create(OUT / 'actual_interrupted_gzip_diagnosis.json', {
                'status': 'confirmed_gzip_missing_end_of_stream_marker',
                'error': str(error), 'orphan_sha256': sha(snapshot),
                'previous_main6_retirement_did_not_check_its_in_process_serializer_stack': True})
        else: raise AssertionError('Expected a genuinely interrupted gzip, not a verified file')
        snapshot.rename(interrupted)
        assert sha(interrupted) == read(OUT / 'frozen_before_actual_recovery.json')['orphan_snapshot_sha256']
        from immutable_lossless_ranking_snapshot_20261006 import prepare
        restored = prepare(display)
        with gzip.open(restored, 'rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == proof['original_report_sha256']
        assert read(verification)['status'] == 'passed_exact_original_full_report_bytes_from_immutable_lossless_HTML'
        for path, digest in pins.items(): assert sha(path) == digest, path
        create(OUT / 'verification.json', {
            'status': 'passed_original_exact_full10570_report_serializer_after_preserving_interrupted_gzip',
            'input_sha256': pins, 'original_report_sha256': proof['original_report_sha256'],
            'restored_gzip_sha256': sha(restored), 'preserved_interrupted_file': str(interrupted),
            'original_serializer_executed_unchanged': True, 'all_original_full_QA_and_candidate_unchanged': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'scientific_workers_stopped_or_restarted': 0,
            'test_labels_read': False})
        print('passed_original_exact_full10570_report_serializer_after_preserving_interrupted_gzip', flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running(): process.resume()


if __name__ == '__main__':
    try: main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_interrupted_snapshot_recovery',
                'error': f'{type(exc).__name__}: {exc}'})
        raise
