"""Publish remaining sources and genuine validation records to main alone."""
from pathlib import Path
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import watch_validations_main_v2_20261005 as watcher
from publish_main_closeout_v2_20261005 import blob_hashes, names
from finalize_main_branch_consolidation_20261005 import owned_pair, verify_main

sync = watcher.sync
PREFIX = Path('validation_sync/main_only_pending_sources_20261005')
OUT = A / 'main_only_pending_sources_20261005'


def observer_pairs():
    launch = sync.read(sync.OUT / 'launch_v3.json')['publisher']
    publisher = owned_pair(launch['pid'], Path(launch['script']), launch['script_args'])
    assert publisher[1].pid == sync.read(sync.OUT / 'owner.lock')['pid']
    launch = sync.read(A / 'actual_optimization_monitor_launch_v13_20261005.json')
    monitor = owned_pair(launch['pid'], Path(launch['script']), launch['script_args'])
    return publisher, monitor


def main():
    assert not (OUT / 'receipt.json').exists(), 'Publication already completed.'
    preflight = sync.read(A / 'streaming_rank_classification_preflight_v2_20261005/verification.json')
    assert preflight['status'].startswith('passed') and preflight['actual_small32epoch_fits'] == 16
    bank = A / 'streaming_rank_classification_bank_v2_20261005'
    failed = sync.read(bank / 'training_execution_scope.json')
    assert failed['status'] == 'failed' and failed['failure'] == 'ValueError: sort array is read-only'
    launches = sync.read(A / 'streaming_rank_classifier_followups_20261005/verification.json')
    for role in ('native', 'future'):
        launch = launches[role]
        for pid in (launch['pid'], launch['owned_worker_pid']):
            assert not psutil.pid_exists(pid), 'Capture terminal attempts after their handles have closed.'
    for record in (preflight, sync.read(A / 'streaming_rank_classifier_bank_run_20261005.json'),
                   sync.read(A / 'streaming_rank_classifier_future_run_20261005.json')):
        for filename, expected in record['input_sha256'].items():
            source = Path(filename)
            if source.suffix in ('.py', '.json', '.md'):
                assert hashlib.sha256(source.read_bytes()).hexdigest() == expected, filename
    assert not list(bank.glob('*/info_*.json')), 'Failed attempt cannot be counted as qualified full fits.'

    evidence = set()
    for folder in ('streaming_rank_classification_preflight_20261005',
                   'streaming_rank_classification_preflight_v2_20261005',
                   'streaming_rank_classifier_label_recovery_v2_20261005',
                   'streaming_rank_classifier_followups_20261005',
                   'streaming_rank_classification_bank_v2_20261005'):
        evidence.update(p for p in (A / folder).rglob('*')
                        if p.is_file() and p.suffix in ('.json', '.jsonl', '.md', '.py'))
    for role in ('native', 'future'):
        evidence.update(Path(launches[role][stream]) for stream in ('stdout', 'stderr'))
    evidence.add(A / 'neural16384_actual_fit_and_admission_github_20261005/receipt.json')

    pairs = observer_pairs()
    suspended = []
    try:
        for attempt in range(12):
            for parent, child in pairs:
                for process in (child, parent):
                    process.suspend()
                    suspended.append(process)
            busy = [p for parent, child in pairs for p in parent.children(recursive=True)
                    if p.pid != child.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(1)
        else:
            raise RuntimeError('Owned publisher remains busy; preserve its commands.')

        assert not sync.git('status', '--porcelain'), 'Publishing worktree must be clean.'
        previous = sync.git('rev-parse', 'HEAD')
        assert sync.git('rev-parse', 'HEAD', cwd=ROOT) == previous
        old_heads = verify_main(previous)
        selected = names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')
        tracked = names('ls-files')
        for folder in ('analysis', 'experiments', 'src', 'tests', 'config'):
            selected.update(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*.py')
                            if '__pycache__' not in p.parts and p.relative_to(ROOT).as_posix() not in tracked)
        selected.add(Path(__file__).relative_to(ROOT).as_posix())
        sources = {ROOT / name for name in selected} | evidence
        targets, captures = {}, {}
        for source in sorted(sources):
            assert source.is_file() and source.suffix in ('.py', '.json', '.jsonl', '.log', '.md', '.toml', '.yaml', '.yml')
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), source
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            elif source.suffix == '.jsonl':
                for line in data.decode('utf-8-sig').splitlines():
                    if line.strip():
                        json.loads(line)
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            targets[destination.as_posix()] = data
            captures[relative.as_posix()] = {'published_path': destination.as_posix(),
                'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                'runtime_snapshot': source not in evidence and source.suffix == '.json' and (
                    'state' in source.stem or 'resume' in source.stem or
                    source.stem.startswith(('optimization_boundary', 'optimization_fit_cost', 'next_experiment')))}
        manifest = {'status': 'captured_remaining_sources_and_actual_validation_records_for_main',
            'at_local': sync.now(), 'authorization': '调整GitHub分支，把所有东西都合并提交到主分支main，不要其他分支',
            'previous_main': previous, 'files': captures,
            'historical_branch_heads_verified_ancestors': old_heads,
            'local_branches': ['main'], 'remote_branches': ['main'], 'default_branch': 'main',
            'future_validation_push_target': 'refs/heads/main',
            'publisher_worktree_detached_HEAD': True,
            'small_classifier32epoch_control_fits_passed': 16,
            'actual_full_classifier_attempt_status': failed['status'],
            'actual_full_classifier_failure': failed['failure'],
            'qualified_full_classifier_annual_fits': 0, 'qualified_full_classifier_final_fits': 0,
            'original_failed_sources_and_launches_retained': True,
            'training_processes_not_suspended_or_stopped': True,
            'runtime_files_are_submission_time_snapshots': True,
            'raw_data_weights_predictions_remain_local_D_or_E': True,
            'test_labels_read': False, 'new_quality_scores': 0}
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded(manifest)
        targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# main 分支代码与验证记录补齐\n\n'
            '全部历史分支提交已包含在 main；本地、GitHub 及默认分支均只保留 main。'
            '本次补齐尚未提交的模型代码、冻结运行清单、真实验证证据及运行状态快照。'
            '后续完成验证继续直接提交 main，同步目录使用分离 HEAD。\n\n'
            '四种流式分类配置的16次小样本32轮拟合及成熟窗口、未来污染、原生权重、重载和前缀检查通过。'
            '首次完整2020年训练实际执行了32轮，但随后在只读数组原地排序时失败，尚无合格完整年度模型。'
            '原始失败、修复前后源码、冻结证据、实际完整训练与后续退出日志全部保留。'
            '这些记录不表示完整年度验证、候选推理或官方评分已经完成。\n\n'
            '提交保留各文件原始字节并逐文件核验 SHA256；原始数据、权重与预测仍存 D/E 盘。'
            '其他训练任务继续运行。\n').encode('utf-8')
        for name, record in captures.items():
            if not record['runtime_snapshot']:
                assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == record['sha256'], name
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '将剩余模型源码及全部本轮验证证据提交main，核验历史合并与唯一分支', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        assert not sync.git('status', '--porcelain', cwd=ROOT)
        assert not sync.git('status', '--porcelain')
        receipt = {'status': 'pushed_all_pending_sources_and_validation_records_verified_main_only',
            'at_local': sync.now(), 'commit': commit, 'changed_files': len(staged),
            'raw_git_blob_sha256_verified': len(expected),
            'local_branches': ['main'], 'remote_branches': ['main'], 'default_branch': 'main',
            'historical_branch_commits_preserved': old_heads,
            'source_worktree_clean_at_snapshot': True,
            'future_validation_push_target': 'refs/heads/main',
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}'}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
