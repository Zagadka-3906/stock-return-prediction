"""Publish actual residual bank or49 comparison evidence with serialized main writes."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def wait_closed(service):
    identity = read(service / 'native_launch.json')
    while owned(identity):
        time.sleep(30)
    return read(service / 'service_execution.json')


def main(phase):
    assert phase in ('bank', 'scores')
    bank = A / 'conditional_flag_residual_bank_20261006'
    folder = bank if phase == 'bank' else A / 'conditional_flag_residual_official_comparison_20261006'
    service = A / 'service_owned_workflows_20261006' / (
        'conditional_flag_residual_native_bank' if phase == 'bank' else 'conditional_flag_residual_official_comparison')
    assert wait_closed(service)['status'] == 'passed'
    proof = read(folder / 'verification.json')
    expected = ('passed_actual20_past_OOF_conditional_residual_native_models_and_independent_codec' if phase == 'bank'
        else 'passed_actual49_conditional_residual_native_and_ensemble_full_official_comparisons')
    assert proof['status'] == expected
    if phase == 'bank':
        assert proof['actual_native_fits'] == len(proof['actual_models']) == 20
    else:
        assert proof['new_quality_score_records'] == len(proof['records']) == 49
    # Complete the previous manual worktree holder before admitting another.
    wait_closed(A / 'service_owned_workflows_20261006/conditional_flag_round101_full_registration_v2')
    if phase == 'scores':
        assert wait_closed(A / 'service_owned_workflows_20261006/conditional_residual_bank_evidence_publication')['status'] == 'passed'
    out = A / f'conditional_residual_{phase}_github_20261006'
    assert not out.exists()
    out.mkdir()
    prefix = Path(f'validation_sync/conditional_residual_{phase}_20261006')
    sources = [Path(__file__), *(A / name for name in (
        'train_conditional_flag_residual_bank_20261006.py',
        'conditional_flag_residual_transform_20261006.py',
        'run_conditional_flag_residual_official_comparison_20261006.py',
        'conditional_flag_rank_codec_20261006.py', 'cohort_rank_calibration_v2_20261006.py')),
        *service.glob('*.json'), *service.glob('*.log')]
    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]
    if phase == 'scores':
        sources += list(folder.rglob('*.json'))
        for record in proof['records']:
            capsule = Path(record['official_score_cache']['official_metrics_source'])
            assert hashlib.sha256(capsule.read_bytes()).hexdigest() == record['official_metric_capsule_sha256']
            assert read(capsule)['metrics'] == record['metrics']
            sources.append(capsule)
    sync = helpers.sync
    payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data), source
        raw_digest = hashlib.sha256(data).hexdigest()
        target = prefix / source.relative_to(ROOT)
        if len(data) >= 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_digest
            target = Path(target.as_posix() + '.gz')
        payload[target.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': target.as_posix(),
            'original_sha256': raw_digest, 'published_sha256': hashlib.sha256(data).hexdigest()}
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    held = []
    restore = install()
    try:
        parent, worker, idle = suspended_idle(publisher,
            '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        manifest = {'status': proof['status'], 'phase': phase, 'at_local': sync.now(), 'files': files,
            'actual_native_model_fits': 20, 'new_native_fits_by_comparison': 0,
            'scored_records': 0 if phase == 'bank' else 49,
            'actual_diagnostic_mature_parent_curve_refits': 5,
            'first2020_and_nonflagged_predictions_identity': True,
            'models_predictions_and_training_data_not_uploaded': True,
            'candidate_and_complete_ranking_qualification_pending': True,
            'previous_main': previous, 'only_branch': 'main', 'test_labels_read': False,
            'idle_publisher_before_and_after_hold': idle, 'scientific_processes_suspended_or_restarted': 0}
        if phase == 'scores':
            manifest['best_actual_official_record'] = proof['best']
        payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
        payload[(prefix / 'README.md').as_posix()] = (
            '# 条件排名残差模型：实际核验与官方比较\n\n'
            '父方案是已完整合格第100轮。三个模型使用63个提供字段的因果特征及'
            '完整第95轮年度OOF预测的每日百分位；另有只使用该百分位的一维对照。'
            '目标为历史完整有限标签池的真实收益排名减去当前训练窗口拟合的涨停组曲线。'
            '每个模型完成2021—2024四个年度模型及2025最终模型，共20次真实CPU拟合，'
            '预定最多64轮；实际棵树数逐项记录，不以验证早停选择模型。'
            '2020因缺乏此前完整方案OOF而保持父方案，所有非涨停原始预测逐位不变。\n\n'
            '五个训练窗口的成熟曲线独立复现父方案已保存曲线，'
            '各验证年度标签污染不影响当年训练曲线。每个原生模型、重载模型和'
            '独立树遍历的实际预测逐位相等，年度80/260/975日前缀检查全部保留。\n\n'
            '49项质量比较为四个原生残差、三个特征模型的等权平均及全部四个模型的等权平均，'
            '分别测试0.01/0.025/0.05/0.1/0.25/0.5/0.75/1，加一个父方案锚点。'
            '比较最终过去收益率映射后的完整5635800行CSV，使用原官方脚本；'
            '全年连接处不重置换手，无额外单指标或显著性淘汰条件。\n\n'
            f'本目录阶段为{phase}：bank是已完成的训练和推理核验，不产生质量分数；'
            'scores是49项自然结束后的全部实际官方分数和原始胶囊。'
            '候选完整推理、方案封存与完整榜仍另行完成；不提前声称优化方向耗尽。'
            '所有阶段只发布main，并保留全部原始记录、哈希和源码，不上传模型权重。\n').encode('utf-8')
        for name, data in payload.items():
            sync.atomic(sync.WORKTREE / name, data)
        names = sorted(payload)
        for start in range(0, len(names), 50):
            sync.git('add', '-f', '--', *names[start:start + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(names)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'保存条件排名残差模型的完整实际{phase}核验记录', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'phase': phase,
            'at_local': sync.now(), 'commit': commit, 'branch': 'main', 'actual_native_model_fits': 20,
            'scored_records': manifest['scored_records'], 'raw_git_blobs_verified': len(hashes),
            'candidate_and_complete_ranking_qualification_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_residual_phase_publication',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main(sys.argv[1])
