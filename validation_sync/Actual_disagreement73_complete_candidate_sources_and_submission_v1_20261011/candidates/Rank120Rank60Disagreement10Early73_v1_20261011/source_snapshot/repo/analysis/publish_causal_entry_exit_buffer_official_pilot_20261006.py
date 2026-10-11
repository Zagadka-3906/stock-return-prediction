"""Publish all actual mapped-output pilot scores; keep release qualification pending."""
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

OUT = A / 'causal_entry_exit_buffer_official_pilot_github_20261006'
PREFIX = Path('validation_sync/causal_entry_exit_buffer_official_pilot_20261006')


def main():
    pilot = A / 'causal_entry_exit_buffer_official_pilot_20261006'
    proof = read(pilot / 'verification.json')
    assert proof['status'] == 'completed_actual16_training_official_scores_full_submission_release_pending'
    assert len(proof['records']) == 16 and proof['new_quality_score_records'] == 16
    assert proof['candidate_inference_and_full_ranking_qualification_pending']
    for path, digest in proof['input_sha256'].items(): assert sha(path) == digest, path
    for row in proof['records']:
        capsule = Path(row['official_score_cache']['official_metrics_source'])
        assert sha(capsule) == row['official_metric_capsule_sha256']
        assert read(capsule)['metrics'] == row['metrics']
    assert proof['best']['margin'] == 0. and proof['score_gain_over_frozen_parent'] == 0.
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), A / 'score_causal_entry_exit_buffer_official_pilot_20261006.py',
        A / 'causal_entry_exit_buffer_v2_20261006.py',
        *pilot.glob('*.json'), *pilot.glob('identical_official_scores/*.json'),
        *(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_official_pilot').glob('*.json')]
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
    identity = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    assert owned(identity)
    root, worker = helpers.owned_pair(identity['pid'], Path(identity['script']), identity['script_args'])
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
            'status': proof['status'], 'previous_main': previous, 'at_local': sync.now(), 'files': files,
            'actual_scored_pilot_records': 16, 'new_native_fits': 0,
            'full_candidate_and_completed_board_qualification_pending': True,
            'only_publication_branch': 'main'})
        targets[(PREFIX / 'scores.csv').as_posix()] = (
            'margin,official_final_score,ic_mean,annual_excess,mean_turnover\n' +
            ''.join(','.join(str(value) for value in (row['margin'], row['connected_final_score'],
                row['metrics']['ic_mean'], row['metrics']['annual_excess'], row['metrics']['mean_turnover']))+'\n'
                for row in sorted(proof['records'], key=lambda row: (-row['connected_final_score'], row['margin'])))
        ).encode('utf-8')
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 完整方案后成员缓冲：16项实际官方训练验证比较\n\n'
            '0—1范围16个预先固定参数，全部按相同5635800行、1212日、4650股票、2020—2024'
            '连续向前验证比较。每项先使用成熟的过去OOF标签收益映射，再由未改动的官方评分脚本'
            '比较最终CSV；等价输入仅在CSV、训练OOF别名、脚本与运行库指纹完全相同时复用官方分数。'
            '各项8指标、映射成熟边界、CSV与评分指纹、源码和实际资源记录随附。无测试标签，无新训练。\n\n'
            '最高分0.4510081068915626仍是零缓冲原方案；0.00025—0.004等价，复杂度并列规则保留零参数。'
            '强缓冲1.0将换手降至0.015150958342132297，但年化超额收益降至0.28844670470238853，'
            '总分0.42800594370453654；换手下降不等于官方总分提高，本方向尚未带来提升。\n\n'
            '这是实际全量官方评分试验，已完成16项；完整方案冻结、候选推理复核、正式完整榜资格'
            '登记仍待后续完成。目前完整资格榜10570条不因这份试验记录提前增长，既有第96轮等任务继续。'
            '只存源文件、记录和分数，不上传训练评分CSV或大模型副本。所有上传仅main。\n'
        ).encode('utf-8')
        for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50): sync.git('add', '-f', '--', *selected[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '记录16项成熟收益映射后的官方成员缓冲比较及不采用结果', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual16_official_buffer_pilot_records_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(hashes),
            'actual_scored_pilot_records': 16, 'full_release_qualification_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
        print(json.dumps(read(OUT / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_official_buffer_pilot_publication',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running(): process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__': main()
