"""Publish measured local acceleration and strict unfinished-grid repair evidence on main."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert read(p / 'service_execution.json')['status'] == 'passed', name
    return p


def main():
    closed('compact_MLP44_full111_route_evidence_main_publication')
    proof_path = A / 'round90_previous_run_input_precheck_20261007.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed_actual_all255_original_unstarted90_run_inputs_match'
    assert proof['checked_count'] == 255 and not proof['mismatches']
    out = A / 'single_host_checkpoint_and_round90_pins_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), proof_path, Path(proof['previous_run']),
        A / 'single_host_actual_progress_checkpoint_20261007_0348.json',
        A / 'compact_MLP44_full111_route_evidence_github_20261007/receipt.json',
        A / 'classifier_consensus124_scoring_snapshot_github_20261007/receipt.json']
    pins = {**proof['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(out / 'frozen_before_main_publication.json', {'input_sha256': pins, 'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held, retries = [], []
    restore = install()
    sync = helpers.sync
    old_git = sync.git

    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return old_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(t in str(error).lower() for t in ('tls', 'ssl', 'connection', 'timed out', 'unable to access')):
                    raise
                retries.append({'command': args[0], 'attempt': attempt + 1, 'error': str(error)[:1000]})
                if attempt == 2:
                    raise
                time.sleep(2)

    sync.git = retry_git
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        with LockedReadHashCache(pins) as scope:
            prefix = Path('validation_sync/single_host_checkpoint_and_round90_pins_20261007')
            payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
            files = {}
            for p in dict.fromkeys([*sources, out / 'frozen_before_main_publication.json']):
                data = p.read_bytes()
                assert not sync.SECRET.search(data), p
                raw_sha = hashlib.sha256(data).hexdigest()
                target = (prefix / p.relative_to(ROOT)).as_posix()
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
                    target += '.gz'
                payload[target] = data
                files[p.relative_to(ROOT).as_posix()] = {'published_path': target, 'original_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            manifest = {'status': 'actual255_original_unstarted90_run_input_hashes_and_single_host_progress_checkpoint',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'actual_original_round90_inputs_checked': 255,
                'actual_original_round90_input_mismatches': 0,
                'original_round90_protocol_absent_at_input_check': not proof['original90_scientific_protocol_exists'],
                'new_scientific_launches_by_input_check': 0, 'new_quality_scores_by_publication': 0,
                'goal_complete_or_resource_direction_exhaustion_not_claimed': True,
                'remote_workers_dispatched': 0, 'scientific_workers_stopped_or_restarted': 0,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机阶段检查点与未启动第90轮原输入核对\n\n'
                '第90轮原运行包255个输入逐个实际SHA256核对，无缺失、无不一致。检查时该轮尚未生成科学protocol。'
                '此核对不代替之后实际启动前的冻结与全过程检查，没有新拟合、评分或科学启动。\n\n'
                '记录当前本机强身份进程、原32条任务及19条余项、完整124项评分阶段、既有合格最高分，'
                '以及新16/32网络的20拟合44评分完整111流程等待状态。所有原科学与GPU进程保留。'
                'R89候选与完整榜/main尚未最终闭合，不能将评分阶段或源预检称为完成总目标。\n\n'
                '仅main，初末所有封存输入Windows只读共享锁及全量重哈希，本机D/E存储，未读真实测试标签。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存本机阶段检查点与未启动第90轮原255个输入真实哈希核对', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit, 'at_local': sync.now(),
                'branch': 'main', 'raw_git_blobs_verified': len(hashes), 'new_quality_scores': 0,
                'all_source_inputs_initial_and_final_read_locked_full_rehash': True,
                'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
            print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    finally:
        sync.git = old_git
        for p in reversed(held):
            if p.is_running():
                p.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})
        create(out / 'transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
