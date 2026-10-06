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
    closed('classifier_consensus124_official_scoring_snapshot')
    folder = A / 'classifier_consensus124_official_scoring_snapshot_20261007'
    proof = read(folder / 'verification.json')
    assert proof['status'] == 'passed_actual124_completed_official_capsules_all8_bits_not_candidate_or_full_QA_qualification'
    assert proof['actual_completed_scoring_records'] == len(proof['records']) == 124
    out = A / 'classifier_consensus124_scoring_snapshot_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[Path(p) for p in proof['input_sha256']],
        folder / 'verification.json', folder / 'frozen_before_actual_scoring_snapshot.json']
    service = A / 'service_owned_workflows_20261006/classifier_consensus124_official_scoring_snapshot'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
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
            prefix = Path('validation_sync/classifier_consensus124_scoring_snapshot_20261007')
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
            manifest = {'status': 'actual124_completed_R89_official_scoring_capsules_not_candidate_or_full_QA_closure',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'actual_completed_official_records': 124, 'actual_wave_counts': [73, 8, 18, 25],
                'all_original8_metric_bits_verified_against_raw_official_capsules': True,
                'actual_date_index_official_evaluations': proof['actual_original_official_date_index_executions'],
                'actual_original_official_capsule_cache_hits': proof['actual_original_official_capsule_cache_hits'],
                'highest_completed_grid_score': proof['highest_completed_grid_score'],
                'qualified106_score': proof['qualified106_score'], 'grid_improves_qualified106': proof['grid_improves_qualified106'],
                'scientific_candidate_future_and_full_QA_main_closure_not_claimed_by_snapshot': True,
                'actual_new_official_scores_by_snapshot': 0, 'scientific_workers_stopped_or_restarted': 0,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 第89轮124项完整连续官方评分阶段快照\n\n'
                '353—356组73/8/18/25项均真实complete，共124项，所有8项指标逐位对照原官方指标文件通过。'
                '最高综合分0.4510531893859833，低于已完整合格106方案的0.45110171046668335。\n\n'
                '92次实际官方执行使用1212个日期索引，32项复用完全相同预测的原官方缓存；评分源码与公式未改。'
                '完整参数图和逐项记录附于原始组JSON，较大文件gzip无损保存并核对原SHA。\n\n'
                '这是评分阶段，尚不代表R89候选推理、封存、完整榜QA4与main流程闭合。'
                '科学进程仍在后续候选阶段，没有停止、暂停或重启。快照没有新增模型拟合或重复选模评分；只本机D/E及main，未读真实测试标签。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存第89轮124项真实完整官方评分记录及92次日期索引和32项相同预测缓存证据', timeout=180)
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
