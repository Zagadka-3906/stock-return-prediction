"""Publish actual full postprocessor controls and their preserved failure to main."""
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

OUT = A / 'causal_entry_exit_buffer_controls_github_20261006'
PREFIX = Path('validation_sync/causal_entry_exit_buffer_controls_20261006')


def main():
    controls2 = A / 'causal_entry_exit_buffer_full_controls_v2_20261006'
    controls3 = A / 'causal_entry_exit_buffer_full_controls_v3_20261006'
    prior, proof = read(controls2 / 'verification.json'), read(controls3 / 'verification.json')
    expected = 'passed_full5635800_row_entry_exit_buffer_causal_and_zero_identity_controls'
    assert prior['status'] == proof['status'] == expected
    for value in (prior, proof):
        for path, digest in value['input_sha256'].items(): assert sha(path) == digest, path
    assert len(prior['actual_all11_margin_controls']) == 11
    assert len(proof['actual_all16_margin_controls']) == 16
    for first, second in zip(prior['actual_all11_margin_controls'], proof['actual_all16_margin_controls']):
        assert first == second, first['margin']
    assert proof['runtime_adopted'] is False and proof['new_quality_scores'] == 0
    assert not OUT.exists()
    OUT.mkdir()
    # Avoid racing the independently verified controller handoff's main push.
    handoff_row = read(A / 'service_owned_workflows_20261006/joint_goss_round97_idle_handoff_waiter/native_launch.json')
    while owned(handoff_row): time.sleep(1)
    sources = [Path(__file__), A / 'causal_entry_exit_buffer_20261006.py',
        A / 'causal_entry_exit_buffer_v2_20261006.py',
        A / 'verify_causal_entry_exit_buffer_full_controls_20261006.py',
        A / 'verify_causal_entry_exit_buffer_full_controls_v2_20261006.py',
        A / 'verify_causal_entry_exit_buffer_full_controls_v3_20261006.py',
        A / 'recover_causal_entry_exit_buffer_controls_v2_20261006.py',
        A / 'expand_causal_entry_exit_buffer_controls_v3_20261006.py',
        *controls2.glob('*.json'), *controls3.glob('*.json'),
        *(A / 'causal_entry_exit_buffer_full_controls_20261006').glob('*.json')]
    sync = helpers.sync
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for path in dict.fromkeys(sources):
        data = path.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), path
        target = path.relative_to(ROOT) if path.parent == A and path.suffix == '.py' else PREFIX / path.relative_to(ROOT)
        targets[target.as_posix()] = data
        files[path.relative_to(ROOT).as_posix()] = {
            'published_path': target.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    rows = [read(A / f'service_owned_workflows_20261006/{name}/native_launch.json')
        for name in ('main_publisher_v7', 'main_publisher_v6')
        if (A / f'service_owned_workflows_20261006/{name}/native_launch.json').exists()]
    row = next(value for value in rows if owned(value))
    root, worker = helpers.owned_pair(row['pid'], Path(row['script']), row['script_args'])
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
        else: raise RuntimeError('Main publisher still owns an active publication')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': expected, 'previous_main': previous, 'at_local': sync.now(), 'files': files,
            'first11_wider_margin_controls_exactly_equal_previous_controls': True,
            'full_controls_only_not_official_selection_scores': True, 'new_quality_scores': 0,
            'runtime_adopted': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 当前完整方案后的成员缓冲变体：实际全量因果控制\n\n'
            '已有模型后处理使用历史Top奖励；本变体是在第85轮冻结完整输出之后追加的组合，'
            '按当日非涨停股票的横截面排序给昨日成员加入选缓冲，只改变成员分组；'
            '组内继续原输出排序，每日非涨停预测值仅重新分配，涨停值逐位保留。'
            '不是把通用留存奖励概念宣称为未尝试的新模型。\n\n'
            '真实5635800行、1212日、4650股票，16个预先固定的0—1缓冲参数：'
            '逐位零参数等价、每天值分布与涨停值保留、独立冷80/260/975日前缀、'
            '更改未来分数及涨停标记不影响前260日、实际输出换手与内部状态一致，全部通过。'
            '初次控制错误要求每个正参数必须改变成员，失败保留；改为保存等价参数证据。'
            '扩展版本前11项与前版本完整结果逐项相同。\n\n'
            '0.00025—0.004与父输出相同；0.1的换手诊断约0.032298，1.0约0.015151。'
            '这不是官方综合分：尚需成熟收益映射、八项官方指标、完整方案冻结、'
            '实际候选推理与完整榜资格检查。不得只凭换手下降选用。'
            '父路径退出诊断也不是全局换手下界或资源边界。\n\n'
            '新增训练0、新增选模分数0、未采用、未读测试标签。数据中没有读取训练标签列；'
            '未输出或保留新的大模型/预测副本，只保留源文件、控制记录和数值SHA。所有记录仅main。\n'
        ).encode('utf-8')
        for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50): sync.git('add', '-f', '--', *selected[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验完整输出后16组成员缓冲的全量因果性并保留无效参数与失败证据', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {
            'status': 'pushed_actual16_full_causal_buffer_controls_and_preserved_failure_main_only',
            'commit': commit, 'at_local': sync.now(), 'raw_git_blobs_verified': len(hashes),
            'new_quality_scores': 0, 'runtime_adopted': False,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
        print(json.dumps(read(OUT / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_full_buffer_control_publication',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running(): process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__': main()
