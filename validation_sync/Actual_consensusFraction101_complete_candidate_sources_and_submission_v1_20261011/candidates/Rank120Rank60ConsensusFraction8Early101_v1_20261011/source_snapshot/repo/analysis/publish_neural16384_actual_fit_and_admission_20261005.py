"""Publish actual full-fit and admission recovery evidence directly to main."""
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
from finalize_main_branch_consolidation_20261005 import owned_pair, verify_main

sync = watcher.sync
PREFIX = Path('validation_sync/neural16384_actual_fit_and_admission_20261005')
OUT = A / 'neural16384_actual_fit_and_admission_github_20261005'


def main():
    assert not (OUT / 'receipt.json').exists()
    folders = ('neural16384_idle_memory_admission_20261005', 'owned_waiter_memory_reclaim_20261005',
               'operational_observer_memory_reclaim_20261005',
               'pending_round_dispatch_and_wide_fit_20261005', 'neural16384_idle_admission_watch_20261005')
    evidence = set()
    for folder in folders:
        proof = sync.read(A / folder / 'verification.json')
        assert proof['status'].startswith('passed')
        for filename, value in proof.get('input_sha256', proof.get('source_sha256', {})).items():
            assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == value, filename
        evidence.update((A / folder).glob('*.json'))
    wide = sync.read(A / 'pending_round_dispatch_and_wide_fit_20261005/actual_completed_2020_fit.json')
    assert wide['actual_new_completed_annual_fits'] == 1 and wide['actual_fit_record']['completed_epochs'] == 32
    dispatch = sync.read(A / 'pending_round_dispatch_and_wide_fit_20261005/dispatch_controls.json')
    assert len(dispatch['controls']) == 12 and dispatch['planned_scored_records'] == 1380
    recovered = sync.read(A / 'operational_observer_memory_reclaim_20261005/verification.json')
    assert recovered['next_year_execution_started'] and recovered['reserve14GiB_not_changed']
    watch = sync.read(A / 'neural16384_idle_admission_watch_20261005/verification.json')
    watch_process = psutil.Process(watch['pid'])
    assert watch['script'] in watch_process.cmdline()
    assert not Path(watch['stderr']).read_bytes()
    trainer = psutil.Process(32148)
    assert str(A / 'run_neural16384_full_bank_20261005.py') in trainer.cmdline()
    stdout = A / 'run_logs/neural16384_annual_recovery_qualified_20261005.stdout.log'
    assert 'fold2021: fitting 2,594,048 mature rows' in stdout.read_text(encoding='utf-8')
    bank = A / 'neural16384_full_bank_20261005'
    for path in (bank / 'protocol.json', bank / 'rank16384_drop000_seed07_e32/info_2020.json',
                 bank / 'prefix_control_rank16384_drop000_seed07_e32_2020.json',
                 bank / 'boundary_control_rank16384_drop000_seed07_e32_2020.json',
                 bank / 'boundary_control_rank16384_drop000_seed07_e32_2021.json'):
        evidence.add(path)
    publisher = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    parent, child = owned_pair(publisher.parent().pid, A / 'watch_validations_main_v3_20261005.py')
    assert child.pid == publisher.pid
    suspended = []
    try:
        for process in (child, parent):
            process.suspend()
            suspended.append(process)
        assert all(p.pid == child.pid or p.name().lower() == 'conhost.exe'
                   for p in parent.children(recursive=True)), 'Publisher currently owns an active command.'
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        verify_main(head)
        selected = {ROOT / name for name in names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')}
        selected.add(Path(__file__))
        selected |= evidence
        captures, targets = {}, {}
        for source in sorted(selected):
            assert source.is_file() and source.suffix in ('.py', '.json'), source
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), source
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            targets[destination.as_posix()] = data
            captures[relative.as_posix()] = {'published_path': destination.as_posix(),
                'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                'runtime_snapshot': source not in evidence and source.suffix == '.json' and (
                    'state' in source.stem or 'resume' in source.stem or 'cost_evidence' in source.stem
                    or 'boundary_evidence' in source.stem or 'directions' in source.stem)}
        manifest = {'status': 'verified_actual_first_full_wide_annual_fit_and_live_next_year_recovery',
            'at_local': sync.now(), 'files': captures, 'actual_completed_wide_annual_fits': 1,
            'actual_completed_2020_training_rows': 1694259, 'actual_started_2021_training_rows': 2594048,
            'actual_original_parameters': 168894465, 'original_epochs': 32, 'original_effective_batch': 32768,
            'remaining_full_annual_fits': 4, 'required_full_final_fits_still_pending': 1,
            'original14GiB_reserve_not_changed': True, 'native_process_not_restarted': True,
            'one_native18_waiters2_observers_working_set_reclaim_attempts_preserved': True,
            'actual12_queued_release_dispatch_checks_passed': True, 'planned_official_records67_to78': 1380,
            'latest_qualified_round': 66, 'completed_board_records': 9822,
            'completed_best_score': .4510081068915626, 'test_labels_read': False,
            'new_quality_scores': 0, 'only_publication_branch': 'main',
            'global_resource_exhaustion_established': False}
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded(manifest)
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 16384宽度首个完整年度拟合与真实等待恢复\n\n'
            '2020年度实际169万行、63特征、168,894,465参数、32轮及1664次原生AdamW更新已完成。'
            '原始模型与预测文件SHA256、成熟窗口和原512控制的输入矩阵/目标/键、实际模型重载、'
            '冷80日372,000行前缀及未来标签污染控制均已核验。该证据只覆盖首年；其余4年及1个最终模型仍须完成。\n\n'
            '原进程在16:52保存后等待原14GiB主机可用内存门槛。针对这个已完成年度的空闲进程、'
            '18个已核验等待进程及2个空闲观察器依次调用Windows K32EmptyWorkingSet。'
            '前两次尝试未立即启动下一年，其完整证据保留；第三次后，原进程于20:05开始2021年度259万行训练。'
            '没有终止或重启训练，也没有改变32轮、有效批32768、种子、预处理、标签成熟窗口或14GiB预留规则。'
            'API说明见[微软文档](https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-emptyworkingset)。\n\n'
            '守护入口的实际当前训练保护检查通过：训练中不执行回收；只在完整年度及冷前缀检查完成、'
            '下一年尚未执行、30秒CPU观察符合空闲条件时尝试回收一次，保留逐次记录。'
            '该操作是内存调度恢复，不代表物理资源上限或优化得分。\n\n'
            '第67至78轮12个真实入口的规范导入、输出目录、前驱轮次、选模/校准及ReleaseContext闭包检查通过，'
            '冻结的1380条官方评分仍待实际原生模型和完整前驱资格。没有调用新评分或读取测试标签。'
            '当前合格完整榜仍为9822条，最高分0.4510081068915626；全局优化边界尚未证明。\n').encode('utf-8')
        for name, item in captures.items():
            if not item['runtime_snapshot'] and not name.endswith('/state.json'):
                assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == item['sha256'], name
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '核验首个16384宽度完整年度拟合，恢复原进程下一年训练并守护内存调度', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_only_main_actual_full_fit_and_native_continuation_verified',
                   'at_local': sync.now(), 'commit': commit, 'files': len(targets),
                   'verified_raw_git_blob_sha256_count': len(expected), 'new_quality_scores': 0,
                   'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
