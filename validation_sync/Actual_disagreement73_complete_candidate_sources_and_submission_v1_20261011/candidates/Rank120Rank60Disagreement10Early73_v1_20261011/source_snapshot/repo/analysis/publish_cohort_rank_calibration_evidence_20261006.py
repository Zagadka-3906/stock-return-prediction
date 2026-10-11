"""Publish complete cohort controls or official pilot without qualification claims."""
from pathlib import Path
import gzip
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers


def main(phase):
    assert phase in ('controls', 'pilot')
    control = A / 'cohort_rank_calibration_full_controls_20261006'
    pilot = A / 'cohort_rank_calibration_official_pilot_20261006'
    folder = control if phase == 'controls' else pilot
    proof = read(folder / 'verification.json')
    status = ('passed_full17_cohort_causal_prefix_and_nonflagged_order_controls' if phase == 'controls'
        else 'completed_actual17_cohort_original_official_scores_full_qualification_pending')
    assert proof['status'] == status
    service = A / ('service_owned_workflows_20261006/cohort_rank_calibration_controls' if phase == 'controls'
        else 'service_owned_workflows_20261006/cohort_rank_calibration_official_pilot')
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'passed'
    out = A / f'cohort_rank_calibration_{phase}_github_20261006'
    assert not out.exists()
    out.mkdir()
    prefix = Path(f'validation_sync/cohort_rank_calibration_{phase}_20261006')
    sources = [Path(__file__), A / 'cohort_rank_calibration_20261006.py',
        A / 'run_cohort_rank_calibration_controls_20261006.py',
        A / 'score_cohort_rank_calibration_pilot_20261006.py',
        *control.glob('*.json'), *service.glob('*.json'), *service.glob('*.log')]
    if phase == 'pilot':
        sources += [*pilot.rglob('*.json'), *pilot.glob('*.log')]
        for row in proof['records']:
            sources.append(Path(row['official_score_cache']['official_metrics_source']))
    sync = helpers.sync
    targets = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for p in dict.fromkeys(sources):
        data = p.read_bytes()
        assert not sync.SECRET.search(data), p
        raw_sha = hashlib.sha256(data).hexdigest()
        target = p.relative_to(ROOT) if p.parent == A and p.suffix == '.py' else prefix / p.relative_to(ROOT)
        if len(data) > 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            target = Path(target.as_posix() + '.gz')
        targets[target.as_posix()] = data
        files[p.relative_to(ROOT).as_posix()] = {'published_path': target.as_posix(),
            'raw_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
    identity = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    held = []
    restore = install()
    try:
        parent, process, idle = suspended_idle(identity,
            '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((process, parent))
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(prefix / 'manifest.json').as_posix()] = sync.encoded({
            'phase': phase, 'status': status, 'files': files, 'previous_main': previous,
            'at_local': sync.now(), 'idle_publisher_before_and_after_hold': idle,
            'all17_cases_still_require_frozen_selected_candidate_and_complete_ranking_qualification': True,
            'new_native_base_model_fits': 0, 'test_labels_read': False,
            'only_publication_branch': 'main'})
        targets[(prefix / 'README.md').as_posix()] = (
            '# 训练期成熟标签的涨停分组排名校准\n\n'
            '在原完整第95轮图之后，使用当前全股票池百分位与题面涨停标志；'
            '仅以各预测年度之前、原fold_cutoff之前已成熟的训练OOF标签拟合两组单调曲线。'
            '训练目标为历史每日有限标签池的平均收益排名，首次2020年度保持原预测。'
            '分箱32/128，涨停组每箱向公共曲线收缩的伪样本0/200，混合权重0.1/0.25/0.5/1，'
            '另加原方案权重0，共17项；实际16次年度曲线拟合，基础模型新增训练0。\n\n'
            '全部5635800行、1212日、4650股票的非涨停排序及并列关系保持一致；'
            '80/260/975日冷前缀、2020恒等、2024标签污染不影响各年度模型的检查通过。'
            'controls仅是因果及排序控制，不是官方分数；pilot以原官方脚本对17个过去收益率映射后'
            'CSV评分，逐项检验超额收益、绝对收益与换手是否完全一致，以及总分变化是否来自IC。'
            '任何拟合或选择不读取测试标签。\n\n'
            '即使试评分提高，仍须冻结完整方案、原模型重载及独立推理、全部测试记录、'
            '因果检查、完整榜及浏览器QA；这些完成前不计入合格完整榜。全部阶段、分数与失败记录'
            '只上传main，后台子进程隐藏窗口，数据与模型存储D/E盘。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for start in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[start:start + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'记录17项成熟训练涨停分组校准的完整{phase}', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(out / 'receipt.json', {'status': 'pushed_verified_cohort_calibration_evidence_main_only',
            'phase': phase, 'at_local': sync.now(), 'commit': commit,
            'raw_git_blobs_verified': len(hashes),
            'candidate_and_full_ranking_qualification_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as exc:
        create(out / 'failure.json', {'status': 'failed_preserved_cohort_evidence_publication',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main(sys.argv[1])
