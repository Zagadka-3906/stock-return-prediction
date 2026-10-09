"""Publish full consensus construction and corrected pending quality to main."""
from pathlib import Path
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
from run_dependency_queue_20261006 import owned

sync = watcher.sync
HANDOFF = A / 'consensus_queue_and_monitor_handoff_v2_20261006'
OUT = A / 'classifier_consensus_workflows_github_20261006'
PREFIX = Path('validation_sync/classifier_consensus_workflows_20261006')


def main():
    assert not (OUT / 'receipt.json').exists()
    proof = sync.read(HANDOFF / 'verification.json')
    assert proof['status'] == 'passed_consensus_full_controls_registered_and_owned_lightweight_handoff'
    plan = sync.read(HANDOFF / 'queue_plan.json')
    state = sync.read(HANDOFF / 'state.json')
    jobs = {**plan['preserved_active_jobs'], **state['activated_jobs'], 'dependency_queue': proof['queue']}
    assert all(owned(row) for row in jobs.values())
    pairs = [owned_pair(jobs[name]['pid'], Path(jobs[name]['script']), jobs[name]['script_args'])
             for name in ('main_publisher', 'progress_monitor')]
    suspended = []
    OUT.mkdir(exist_ok=True)
    try:
        for _ in range(30):
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
            raise RuntimeError('An existing publication or observer child is still active.')
        previous = sync.git('rev-parse', 'HEAD')
        verify_main(previous)
        assert not sync.git('status', '--porcelain')
        sources = [Path(__file__), A / 'resumed_rounds_dependency_queue_v3_20261006.json',
            A / 'monitor_actual_optimization_progress_v19_20261006.py',
            A / 'run_dependency_queue_v3_20261006.py',
            A / 'explicit_parent_release_engine_v3_20261006.py']
        sources += list(A.glob('*classifier_consensus*20261005.py')) + list(A.glob('*classifier_consensus*20261006.py'))
        sources += [A / 'handoff_consensus_queue_and_monitor_20261006.py', A / 'handoff_consensus_queue_and_monitor_v2_20261006.py']
        for number in (89, 90):
            for version in ('v2', 'v3'):
                sources += [A / f'optimize_training_round{number}_{version}.py',
                            A / f'finalize_training_round{number}_{version}.py',
                            A / f'run_training_round{number}_{version}_pipeline.py']
        sources += list(A.glob('*classifier_consensus*20261005.json')) + list(A.glob('*classifier_consensus*20261006.json'))
        folders = [p for p in A.iterdir() if p.is_dir() and
            (p.name.startswith('classifier_consensus_') or p.name.startswith('ready_classifier_consensus_')
             or p.name.startswith('consensus_queue_and_monitor_handoff_')) and p != OUT]
        for folder in folders:
            sources.extend(folder.rglob('*.json'))
            sources.extend(folder.rglob('*.jsonl'))
        targets, files = {}, {}
        for source in dict.fromkeys(sources):
            data = source.read_bytes()
            assert not sync.SECRET.search(data)
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
            targets[destination.as_posix()] = data
            files[source.relative_to(ROOT).as_posix()] = {'published_path': destination.as_posix(), 'raw_sha256': sync.sha(data)}
        native = sync.read(A / 'classifier_consensus_bank_20261005/oof_audit.json')
        future = sync.read(A / 'classifier_consensus_future_qa_20261005/verification.json')
        assert native['actual_virtual_annual_outputs'] == 30 and future['actual_virtual_final_artifacts'] == 6
        assert future['all6_fullfuture_reload_and_cold80_controls_passed']
        targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual30_virtual_annual6_fullfuture_controls_and262_pending_quality_published',
            'at_local': sync.now(), 'previous_main': previous, 'files': files,
            'current_owned_jobs': {name: {'pid': row['owned_worker_pid'], 'creation_time': row['owned_worker_creation_time']}
                                   for name, row in jobs.items()},
            'actual_virtual_annual_outputs': 30, 'actual_virtual_final_artifacts': 6,
            'reused_native_classifier_annual_fits': 20, 'reused_native_classifier_final_fits': 4,
            'new_native_fits': 0, 'required_rounds_retained': list(range(67, 91)),
            'official_quality_records_still_pending_for_new_rounds': 262,
            'initial_failed_generator_sources_and_evidence_retained': True,
            'only_publication_branch': 'main', 'test_labels_read': False, 'new_quality_scores_by_publication': 0})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 六种分类集成的完整推理验证与后续评分\n\n'
            '固定比较二分类平均、多分类平均、二分类权重25%/50%/75%的混合、'
            '多分类反向映射平均。复用20份实际32遍年度模型和4份成熟最终模型，新增原生训练0次。'
            '已完成30份五年年度预测，各自通过实际前80天推理；'
            '六份最终集成都覆盖1,599,600行、344天、4,650只股票，'
            '实际保存重载、冷启动80天及固定行前缀检查全部通过。'
            '独立原分类器predict_proba核验最大误差2.22e-16。\n\n'
            '首次评分生成器预检发现旧wave346文件引用，失败输入与源码全部保留，'
            '通过独立v2搜索引擎/v3轮次源码修复。'
            '角色网格124条、独立主模型网格138条，合计262条官方评分尚待执行。'
            '生成器已实际覆盖保留父方案和选中独立方案两种分支；'
            '实际驱动绑定、完整祖先源码复制、封存写入拒绝及原生分派均已核验。\n\n'
            '原67—88轮全部保留，增加89—90轮，分别以完整合格88、89轮为前置。'
            '28个依赖任务由一个轻量无窗口队列维护。第81轮仍在实际评分，'
            '新版进度观察器展示其真实进度，同时保留最早待完成67轮。'
            '复合模型仅记为虚拟产物，原生训练次数没有重复计入。\n\n'
            '完整官方评分、收益映射、冻结方案、最终因果检查、候选推理和完整榜更新'
            '仍由各轮正式程序完成。当前最佳完整分数仍为0.4510081068915626，'
            '本同步没有把预检或原始推理冒充新的官方质量结果；未读取测试标签。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '完成六种分类集成的完整推理验证并登记89至90轮262条评分', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        assert all(owned(row) for row in jobs.values())
        receipt = {'status': 'pushed_verified_classifier_consensus_full_controls_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blob_sha256_verified': len(expected),
            'official_quality_records_still_pending': 262,
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
