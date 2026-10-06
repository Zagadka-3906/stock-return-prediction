"""Publish real candidate admission/wait and the verified rejected-CSV cleanup."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

OUT = A / 'buffer_candidate_admission_cleanup_github_20261006'
PREFIX = Path('validation_sync/buffer_candidate_admission_cleanup_20261006')


def main():
    cleanup = A / 'rejected_buffer_pilot_csv_cleanup_20261006.json'
    proof = read(cleanup)
    assert proof['status'] == 'passed_removed_only_published_rejected_private_buffer_prediction_csv'
    assert not Path(proof['removed_path']).exists()
    for path, digest in proof['input_sha256'].items(): assert sha(path) == digest, path
    failed = read(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_frozen_inference/service_execution.json')
    assert failed['status'] == 'failed' and failed['failure'] == 'AssertionError: '
    waiter = read(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_candidate_waiter/native_launch.json')
    assert owned(waiter)
    assert waiter['actual_native_console_handle'] == 0 and not waiter['independent_launch_root_in_any_job']
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), A / 'freeze_and_infer_causal_entry_exit_buffer_20261006.py',
        A / 'wait_causal_entry_exit_buffer_candidate_20261006.py',
        A / 'cleanup_rejected_buffer_pilot_prediction_csv_20261006.py', cleanup,
        *(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_frozen_inference').glob('*.json'),
        *(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_candidate_waiter').glob('*.json'),
        *(A / 'causal_entry_exit_buffer_candidate_waiter_20261006').glob('*.json')]
    sync = helpers.sync
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for path in dict.fromkeys(sources):
        data = path.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), path
        target = path.relative_to(ROOT) if path.parent == A and path.suffix == '.py' else PREFIX / path.relative_to(ROOT)
        targets[target.as_posix()] = data
        files[path.relative_to(ROOT).as_posix()] = {'published_path': target.as_posix(),
            'raw_sha256': hashlib.sha256(data).hexdigest()}
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    assert owned(publisher)
    root, worker = helpers.owned_pair(publisher['pid'], Path(publisher['script']), publisher['script_args'])
    suspended = []
    restore = install()
    try:
        for _ in range(180):
            for process in (worker, root): process.suspend(); suspended.append(process)
            busy = [p for p in root.children(recursive=True)
                if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy: break
            for process in reversed(suspended): process.resume()
            suspended = []
            time.sleep(1)
        else: raise RuntimeError('Main7 owns an active publication')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual_candidate_wait_and_rejected_private_csv_cleanup_verified',
            'previous_main': previous, 'at_local': sync.now(), 'files': files,
            'removed_rejected_private_CSV_bytes': proof['removed_bytes'],
            'candidate_full_inference_and_final_board_qualification_pending': True,
            'new_quality_scores': 0, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 成员缓冲候选推理的实际内存等待与弃用预测副本清理\n\n'
            '16项正式官方评分已单独上传，最高仍为零缓冲原方案。首次候选程序在8GiB可用内存'
            '准入处退出，未创建推理输出。失败记录保留；新的实际无窗口独立后台程序要求连续'
            '两次9GiB安全样本后执行完全相同的原程序，并仅允许没有任何科学输出时的原准入'
            '断言重新等待，其他失败均保留。8/9GiB是保护规则，不是全局物理边界。'
            '候选源码要求先冻结完整图，再实际从已验证模型字节重载、完整1599600行、344日、'
            '4650股票及冷80日前缀核验，模型同盘使用校验后的硬链接减少重复存储。'
            '目前这里只证明等待程序实际启动，不证明推理或正式完整榜登记已完成。\n\n'
            '最强缓冲1.0的弃用私有预测CSV经官方胶囊的完整CSV SHA核验，确认独立文件且'
            '不是任何冻结输入、16项分数已上main后删除，回收222022443字节。只删除这一条'
            '明确记录的文件；原模型、父候选、训练评分输入及第96轮不动，分数、源码、'
            '映射边界、数据及CSV指纹全部保留。所有项目文件仍在D/E盘；未读测试标签。\n'
        ).encode('utf-8')
        for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50): sync.git('add', '-f', '--', *selected[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '记录候选推理实际内存等待并清理已发布弃用预测CSV副本', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_buffer_candidate_wait_and_rejected_CSV_cleanup_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(hashes),
            'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
        print(json.dumps(read(OUT / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_candidate_admission_cleanup_publication',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running(): process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__': main()
