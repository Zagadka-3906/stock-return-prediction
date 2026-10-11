"""Publish every pending reviewable source and the closed recovery controls on main."""
from pathlib import Path
import hashlib
import json
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import watch_validations_main_v2_20261005 as watcher
from publish_main_closeout_v2_20261005 import names, blob_hashes

sync = watcher.sync
PREFIX = Path('validation_sync/recovery_qualified_workflows_20261005')
OUT = A / 'recovery_qualified_workflow_github_20261005'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'receipt.json').exists()
    folders = ('standalone_root_source_adapter_preflight_20261005',
        'recovery_qualification_bridge_preflight_20261005',
        'recovery_qualified_workflow_handoff_20261005')
    for folder in folders:
        proof = sync.read(A / folder / 'verification.json')
        assert proof['status'].startswith('passed')
        for key in ('input_sha256', 'source_sha256'):
            for source, expected in proof.get(key, {}).items():
                assert sha(source) == expected, source
    run = sync.read(A / 'github_validation_sync_main_20261005/run_v3.json')
    for source, expected in run['input_sha256'].items():
        assert sha(source) == expected, source
    native_receipt = sync.read(A / 'github_validation_sync_main_20261005/launch_v3.json')
    assert native_receipt['status'].startswith('passed')
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    parent = observer.parent()
    assert parent is not None and parent.pid == native_receipt['publisher']['pid']
    assert str(A / 'watch_validations_main_v3_20261005.py') in parent.cmdline()
    paused = []
    try:
        for process in (observer, parent):
            process.suspend()
            paused.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        for previous in ('8a8fa5702acdd5ada0e53df97640e919c9970f16', '49477a6a8834c68a5d9990887129ac26279a519d'):
            sync.git('merge-base', '--is-ancestor', previous, head)
        pending = names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')
        selected = {ROOT / name for name in pending}
        evidence = set()
        for folder in folders:
            evidence.update(p for p in (A / folder).glob('*.json') if p.is_file())
        evidence.update(A / 'optimization_20261003_r66' / name for name in (
            'protocol.json', 'provenance_scope_execution.json',
            'recovery_frozen_execution_v3_20261005.json'))
        evidence.update(A / 'github_validation_sync_main_20261005' / name for name in ('run_v3.json', 'launch_v3.json'))
        evidence.add(A / 'run_logs/round66_nystrom_tuning_v2_20261005.stderr.log')
        selected |= evidence
        paths, captures = [], {}
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for source in sorted(selected):
            assert source.is_file()
            assert source.suffix in ('.py', '.json', '.md', '.log', '.png') or source.name == '.gitignore', source
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), source
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            captures[relative.as_posix()] = {'published_path': destination.as_posix(),
                'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                'runtime_snapshot': source not in evidence and source.suffix == '.json' and (
                    'state' in source.stem or 'resume' in source.stem or 'optimization_boundary' in source.stem)}
        recovery = sync.read(A / 'round66_root_source_recovery_launch_20261005.json')
        assert recovery['script'] in psutil.Process(recovery['pid']).cmdline()
        original_failed = sync.read(A / 'optimization_20261003_r66/provenance_scope_execution.json')
        assert original_failed['status'] == 'failed'
        manifest = {'status': 'closed_source_controls_and_live_recovery_sources_published',
            'at_local': sync.now(), 'previous_main': head, 'files': captures,
            'all_old_branch_history_reachable_from_main': True, 'only_publication_branch': 'main',
            'actual_R66_recovery_still_running': True, 'actual_R66_scientific_job_untouched': recovery,
            'R66_complete_scientific_scope_not_claimed': True,
            'downstream_jobs_require_actual_passed_recovery_scope': True,
            'automatic_R66_export_includes_failed_original_and_passed_recovery': True,
            'original_failed_scope_and_frozen_protocol_preserved': True,
            'planned_R66_official_records': 218, 'latest_qualified_round': 65,
            'qualified_ranking_records': 9604, 'new_quality_scores_by_publication': 0,
            'test_labels_read': False, 'global_resource_exhaustion_established': False,
            'large_assets': 'Raw data, model weights, predictions and live scratch remain on D/E.'}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
        document = ('# 仅 main 与第66轮恢复衔接\n\n'
            '本地和 GitHub 仅保留 main，原分支历史均可从 main 到达；后续完成的每轮验证继续直接提交 main。\n\n'
            '第66轮原来源解析在独立方案生成前读取当前轮尚不存在的候选文件，原失败协议保留。'
            '新来源适配保持既有模型来源字典不变，十种独立核模型通过实际模型来源检查。'
            '恢复执行已通过方案构建，正在按原218项网格继续评分，尚未宣告该轮完成。\n\n'
            '已完成的第65轮方案和未完成的第66轮拒绝检查均通过。'
            '第67至74轮、宽度模型训练、进度观察与自动提交已接入严格的恢复资格检查。'
            '自动导出第66轮时将同时保留原失败证明、实际恢复冻结来源和通过的恢复执行证明。'
            '所有训练参数、官方评分函数、前序方案资格和完整因果检查要求保持原样。\n\n'
            '此提交新增官方评分数为0；第66轮的实际评分继续在独立进程执行。'
            '验证反复选模偏差未校正，未读取测试标签，未证明可行方法或物理资源已耗尽。'
            '数据、权重、预测和临时文件保存在D/E盘。\n')
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md', document.encode('utf-8'))
        paths.extend(((PREFIX / 'manifest.json').as_posix(), (PREFIX / 'README.md').as_posix()))
        for source, item in captures.items():
            if not item['runtime_snapshot']:
                assert sha(ROOT / source) == item['sha256'], source
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '统一 main 并同步第66轮来源恢复、严格资格与后续自动提交', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {item['published_path']: item['sha256'] for item in captures.values()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_only_main_and_all_selected_git_blob_sha256',
            'at_local': sync.now(), 'commit': commit, 'files': len(paths),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}',
            'all_historical_branch_tips_are_ancestors': True, 'new_quality_scores': 0}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(paused):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
