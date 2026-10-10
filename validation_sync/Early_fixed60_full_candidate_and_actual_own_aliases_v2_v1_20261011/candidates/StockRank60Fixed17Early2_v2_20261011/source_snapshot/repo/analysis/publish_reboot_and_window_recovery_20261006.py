"""Publish reboot recovery and verified console fix while keeping fits running."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import watch_validations_main_v2_20261005 as watcher
from finalize_main_branch_consolidation_20261005 import owned_pair, verify_main
from publish_main_closeout_v2_20261005 import blob_hashes

sync = watcher.sync
RECOVERY = A / 'system_reboot_workflow_recovery_20261006'
OUT = A / 'reboot_and_window_recovery_github_20261006'
PREFIX = Path('validation_sync/reboot_and_window_recovery_20261006')


def main():
    assert not (OUT / 'receipt.json').exists()
    OUT.mkdir(exist_ok=True)
    rows = sync.read(RECOVERY / 'verification.json')['jobs']
    by_name = {row['name']: row for row in rows}
    by_name['gradient_sampling_native'] = sync.read(RECOVERY / 'gradient_sampling_native_v2/launch.json')
    ownership = {}
    for name, row in by_name.items():
        worker = psutil.Process(row['owned_worker_pid'])
        assert worker.create_time() == row['owned_worker_creation_time']
        assert worker.cmdline()[-len(row['script_args']):] == row['script_args']
        ownership[name] = {'pid': worker.pid, 'verified_live': True,
                           'creation_time': worker.create_time()}
    pairs = []
    for name in ('main_publisher', 'progress_monitor'):
        row = by_name[name]
        pair = owned_pair(row['pid'], Path(row['script']), row['script_args'])
        assert pair[1].pid == row['owned_worker_pid']
        pairs.append(pair)
    suspended = []
    try:
        for _ in range(20):
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
            time.sleep(.2)
        else:
            raise RuntimeError('A publication or observer child is still active.')
        previous = sync.git('rev-parse', 'HEAD')
        verify_main(previous)
        assert not sync.git('status', '--porcelain')
        sources = [Path(__file__), *(A / name for name in (
            'run_reboot_recovery_attempt_20261006.py', 'launch_reboot_workflow_recovery_20261006.py',
            'windows_hidden_process_launch_20261006.py', 'hide_recovery_terminal_windows_20261006.py',
            'complete_recovery_window_fix_20261006.py', 'repair_reboot_gradient_sampling_launch_20261006.py',
            'audit_streaming_classifier_signal_complementarity_20261005.py'))]
        for folder in (RECOVERY, A / 'recovery_terminal_window_fix_20261006',
                       A / 'streaming_classifier_signal_complementarity_20261005'):
            sources.extend(folder.rglob('*.json'))
        sources.append(A / 'resumed_rounds_reboot_20261006.json')
        targets, files = {}, {}
        for source in dict.fromkeys(sources):
            data = source.read_bytes()
            assert not sync.SECRET.search(data)
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
            raw_digest = sync.sha(data)
            if len(data) > 5 * 1024**2:
                data = gzip.compress(data, mtime=0)
                destination = Path(destination.as_posix() + '.gz')
            targets[destination.as_posix()] = data
            files[source.relative_to(ROOT).as_posix()] = {
                'published_path': destination.as_posix(), 'raw_sha256': raw_digest,
                'published_sha256': sync.sha(data)}
        fix = sync.read(A / 'recovery_terminal_window_fix_20261006/verified_hidden_launch.json')
        assert fix['hidden_terminal_windows'] == 32 and fix['actual_virtual_environment_child_console_handle'] == 0
        targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'verified_reboot_recovery_current33_owned_jobs_and_actual_consoleless_launch',
            'at_local': sync.now(), 'previous_main': previous, 'files': files,
            'current_owned_jobs': ownership, 'required_rounds_retained': list(range(67, 89)),
            'original_resource_samples_and_failed_attempts_retained': True,
            'window_fix': fix, 'only_publication_branch': 'main',
            'pending_quality_not_claimed_complete': True, 'model_fits_not_stopped_or_restarted_by_publication': True,
            'test_labels_read': False, 'new_quality_scores_by_publication': 0})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 系统重启后恢复与终端窗口修复\n\n'
            '系统于2026-10-05 23:56重启，原任务句柄已失效。核验并复用五份完整年度模型'
            '（四份流式回归、一份16384宽网络）及R81已保存71条评分；未保存的部分训练重新完整运行。'
            '原67—80及81—88的全部待验证任务保留，恢复后的33个工作进程已逐一核验身份。\n\n'
            '原启动将CREATE_NO_WINDOW与DETACHED_PROCESS混用，使隐藏设置失效。'
            '32个确认属于本项目的终端窗口已隐藏，未关闭训练进程。'
            '新的启动函数使用CREATE_NO_WINDOW、SW_HIDE和DEVNULL输入，'
            '已实际启动原虚拟环境Python子进程，确认控制台句柄为0。\n\n'
            'GOSS首次恢复因缺少原TMP/TEMP/TMPDIR环境失败，错误与原执行记录保留；'
            '新尝试恢复原冻结路径并使用无窗口方式启动。'
            '原源码、模型参数、冻结协议及中断前资源日志保持不变。'
            '分类输出互补性为完整训练期诊断，未据此声称任何新模型已通过官方完整质量验证。'
            '未完成的训练、评分、候选因果检查及推理仍是待办，目标尚未完成。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '恢复重启后的完整验证任务，修复后台终端窗口启动方式', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_reboot_and_console_fix_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blob_sha256_verified': len(expected),
            'current_jobs_positively_verified_before_publication': len(ownership),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with (OUT / 'receipt.json').open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
