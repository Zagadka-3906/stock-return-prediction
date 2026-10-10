"""Publish actual controller wiring and observed complete native scope progress on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'distribution_views_full_ranking_publication_wiring_20261006'
OUT = A / 'distribution_views_full_ranking_publication_wiring_github_20261006'
PREFIX = Path('validation_sync/distribution_views_full_ranking_publication_wiring_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not OUT.exists()
    OUT.mkdir()
    proof = sync.read(SOURCE / 'verification.json')
    assert proof['status'] == 'passed_actual_owned_publisher_and_preserved_scientific_queue_wiring'
    assert owned(proof['actual_publication_worker'])
    for filename, digest in proof['publication_source_sha256'].items():
        assert sha(Path(filename)) == digest
    for row in proof['actual_other_worker_identities'].values():
        assert owned(row)
    terminal = {'status': 'passed'}
    sources = [Path(__file__), *[A / name for name in (
        'collect_full_lossless_round_publication_20261006.py',
        'distribution_views_lossless_publication_adapter_20261006.py',
        'verify_distribution_views_full_publication_collector_20261006.py',
        'run_distribution_views_full_ranking_publisher_20261006.py',
        'prepare_distribution_views_full_ranking_publisher_20261006.py',
        'verify_distribution_views_full_ranking_publisher_20261006.py')]]
    sources += sorted(SOURCE.glob('*.json'))
    for name in ('distribution_views_full_publication_collector_preflight_20261006',
                 'distribution_views_full_ranking_publisher_20261006'):
        sources += sorted((A / name).glob('*.json'))
    folder = A / 'service_owned_workflows_20261006/distribution_views_full_ranking_publisher'
    sources += sorted(folder.glob('*.json')) + sorted(folder.glob('*.log'))
    for name in ('quantile_tree_quality_queue_v2_20261006', 'quantile_distribution_views_quality_queue_20261006'):
        sources += sorted((A / name).glob('*.json'))
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(50):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': terminal['status'], 'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_controller_wiring_control_status': terminal['status'],
            'actual_full_round82_collector_and_live93_94_publisher_wiring_verified': True,
            'original198_and_additional262_official_quality_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 第93、94轮完整交互榜与全部检查证据的发布接入\n\n'
            '原main发布器对67—92轮包含完整无损交互榜，对93、94轮原先会回退到精简导出。'
            '新增独立无窗口发布器为93、94轮接入全部原始JSON值、完整交互HTML、原始字节重构gzip、'
            '完整科学与浏览器检查、原始截图及SHA256。它不修改原科学程序或已冻结参数。\n\n'
            '接入在实际第82轮的138条方案、10084条完整榜记录上通过收集核验，'
            '十份完整原始文件逐一与已提交Git原始blob一致。新路径要求93、94轮各自完整评分、'
            '冻结、因果、候选和完整QA_v6实际通过，才执行发布。'
            '本次不把第82轮证据当成未来93、94轮已经通过的证明。\n\n'
            '发布器与原main5通过精确PID、创建时间、命令身份协调，仅在原发布器空闲时暂时挂起。'
            '先完成者可以直接执行完整发布；若原发布器已完成基础导出，则补齐同一轮的完整证据和清单。'
            '每次检查原始Git字节后推送main并核对远端和源索引；原有198及新增262评分方案保持不变。'
            '启动身份、无窗口方式和当前等待真实第93轮合格的状态已经核对。'
            '两轮实际评分和最终完整发布仍待完成；没有新增模型、官方分数或资源耗尽结论。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '接入第93和94轮完整无损榜与全部检查证据发布并核验原始Git字节', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'control_status': terminal['status'],
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected), 'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt', 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'actual_CreateProcess_calls': restore()})


if __name__ == '__main__':
    main()
