"""Publish actual rank execution adoption, full scoring controls, and all preserved unsuccessful controls."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'exact_rank_cache_dependency_handoff_20261006'
OUT = A / 'exact_rank_cache_dependency_handoff_github_20261006'
PREFIX = Path('validation_sync/exact_rank_cache_dependency_handoff_20261006')


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
    assert proof['status'] == 'passed_actual_queue5_controller_handoff_original_full_grids_and_live_workers_preserved'
    assert owned(proof['actual_new_controller']) and not owned(proof['old_controller'])
    for filename, digest in proof['input_sha256'].items():
        assert sha(Path(filename)) == digest
    terminal = {'status': 'passed'}
    sources = [Path(__file__), *[A / name for name in (
        'exact_daily_rank_memoization_20261006.py', 'exact_rank_cache_official_worker_adapter_20261006.py',
        'verify_exact_rank_cache_actual_scoring_adapter_20261006.py',
        'verify_exact_rank_cache_actual_scoring_adapter_v2_20261006.py',
        'verify_exact_rank_cache_queue_routes_20261006.py',
        'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py',
        'run_dependency_queue_v5_20261006.py', 'handoff_dependencies_to_exact_rank_cache_v5_20261006.py')]]
    for name in ('exact_rank_cache_actual_scoring_adapter_20261006',
                 'exact_rank_cache_actual_scoring_adapter_v2_20261006',
                 'exact_rank_cache_queue_routes_20261006',
                 'exact_rank_cache_dependency_handoff_20261006'):
        folder = A / name
        for pattern in ('*.json', '*.jsonl', '*.txt', '*.log'):
            sources += sorted(folder.rglob(pattern))
    folder = A / 'service_owned_workflows_20261006/dependency_queue_v5'
    sources += sorted(folder.glob('*.json')) + sorted(folder.glob('*.log'))
    sources += [A / 'service_owned_dependency_queue_v4_20261006/queue_plan_v5.json',
                A / 'service_owned_dependency_queue_v4_20261006/state.json']
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(ROOT)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(300):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(1.)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': terminal['status'], 'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_controller_wiring_control_status': terminal['status'],
            'actual_original_scoring_adapter_and_shared_queue_handoff_verified': True,
            'failed_overly_strict_cache_count_control_preserved': True,
            'exact_rank_cache_execution_armed_for84_to90': True,
            'original_four_worker67_to80_and198_plus262_plans_preserved': True,
            'original198_and_additional262_official_quality_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 真实评分工作进程的排名复用接入与原队列交接\n\n'
            '在原单评分器的Windows spawn、原Context初始化和原evaluate_many/_evaluate路径中，'
            '对已冻结R65完整方案执行冷、热两次真实候选评分调用。'
            '每次核对所有5635800行Float64位、原评分CSV字节和全部8项官方指标，全部一致。'
            '仅复用字节匹配的原官方评分胶囊；控制明确禁止额外调用官方评价器，实际新增质量记录0。\n\n'
            '冷调用75.5877秒包含初始化，热调用19.9205秒不包含初始化，不能把这个比值当作公平的端到端加速率。'
            '此前配对的完整预测计算为原41.4796秒、1GiB热12.3414秒；这也不保证其他方案或训练、评分、发布全流程同样加速。'
            '实际原评分流程保留根节点部分缓存，热调用15组排名全部命中且新增失配0，'
            '所以旧控制要求23次命中的断言过严。失败源码、失败记录、两次原官方胶囊事件及诊断均完整保留。\n\n'
            '全部23份原排队轮次的实际驱动、参数及传递源码SHA经过只读锁核验。'
            '第89、90轮原记录直接指向v3驱动且参数为空；旧控制器按包装记录解包会失败。'
            '新路由保持这两轮原v3驱动及空参数，只补齐资格检查和执行来源包装。\n\n'
            '新控制器仅给尚未启动或冻结的84—90轮接入已核验的1GiB排名复用，'
            '67—80轮原四进程执行保持原样，避免凭单进程核验证据增加四份缓存内存。'
            '23份原排队轮次和所有原生训练、官方评分网格均保留；原91/92共198及93/94共262方案及独立发布器不变。'
            '控制器继续写原共享state和registry，兼容91/92原等待器。\n\n'
            '新控制器首先禁止激活任务，实际核对无窗口身份、原激活记录和所有运行进程后，'
            '仅退出旧控制器的两个精确PID；第83轮、宽网络、观察器和所有独立发布器继续运行。'
            '写入交接提交记录后新控制器才允许按原依赖条件启动后续任务。'
            '实际交接检查通过，可见终端窗口0；尚未将待启动84—90轮宣称为完成。\n\n'
            '本次新增模型训练0、质量记录0，不读取测试标签，不写重复模型，项目和临时文件使用D/E。'
            '全部成功与失败记录均只提交main；优化目标和资源边界检查仍未完成。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '接入84至90轮精确排名复用并核验真实评分路径与全部原队列参数', timeout=180)
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
