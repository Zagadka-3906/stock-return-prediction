"""Publish every actual37 official capsule after serialized full registration."""
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


def main():
    service = A / 'service_owned_workflows_20261006/conditional_flag_rank_official_comparison_v2'
    identity = read(service / 'native_launch.json')
    while owned(identity):
        time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    folder = A / 'conditional_flag_rank_official_comparison_v2_20261006'
    proof = read(folder / 'verification.json')
    assert proof['status'] == 'passed_actual37_conditional_flag_full_controls_and_original_official_scores'
    assert len(proof['records']) == proof['new_quality_score_records'] == 37
    # The round100 controller also holds the idle publisher while writing the
    # shared board/worktree. Wait for its natural terminal result, so two manual
    # holders can never enter the same worktree transaction concurrently.
    registration = A / 'service_owned_workflows_20261006/extended_cohort_round100_full_registration'
    registration_identity = read(registration / 'native_launch.json')
    while owned(registration_identity):
        time.sleep(30)
    assert (registration / 'service_execution.json').exists()
    out = A / 'conditional_flag_rank_official_comparison_github_20261006'
    assert not out.exists()
    out.mkdir()
    prefix = Path('validation_sync/conditional_flag_rank_official_comparison_20261006')
    sources = [Path(__file__), *(A / name for name in (
        'run_conditional_flag_rank_official_comparison_20261006.py',
        'run_conditional_flag_rank_official_comparison_v2_20261006.py',
        'conditional_flag_rank_transform_20261006.py',
        'conditional_flag_rank_codec_20261006.py',
        'cohort_rank_calibration_20261006.py')),
        *folder.rglob('*.json'), *service.glob('*.json'), *service.glob('*.log'),
        A / 'conditional_flag_rank_bank_v2_20261006/verification.json',
        A / 'conditional_flag_rank_native_bank_github_20261006/receipt.json']
    for record in proof['records']:
        capsule = Path(record['official_score_cache']['official_metrics_source'])
        assert hashlib.sha256(capsule.read_bytes()).hexdigest() == record['official_metric_capsule_sha256']
        assert read(capsule)['metrics'] == record['metrics']
        sources.append(capsule)
    sync = helpers.sync
    payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
    records = {}
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
        records[source.relative_to(ROOT).as_posix()] = {
            'published_path': target.as_posix(), 'original_sha256': raw_digest,
            'published_sha256': hashlib.sha256(data).hexdigest()}
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
        payload[(prefix / 'manifest.json').as_posix()] = sync.encoded({
            'status': proof['status'], 'at_local': sync.now(), 'files': records,
            'scored_records': 37, 'best': proof['best'],
            'actual_original_official_capsules_all_preserved': True,
            'all5_635_800_rows_final_past_return_mapped_output_scored': True,
            'actual_native_bank_fits': 18, 'native_fits_by_this_comparison': 0,
            'actual_common_curve_pair_fits': 4,
            'candidate_and_full_ranking_qualification_pending': True,
            'test_labels_read': False, 'previous_main': previous,
            'scientific_processes_suspended_or_restarted': 0,
            'idle_publisher_before_and_after_hold': idle, 'only_branch': 'main'})
        payload[(prefix / 'README.md').as_posix()] = (
            '# 涨停条件排名模型：37个实际完整官方比较\n\n'
            '以已合格第99轮完整方案为预定父方案：恒等锚点一项，'
            '7/15/31叶三个真实年度模型，各配2020年度固定斜率0.08/0.125/0.2、'
            '混合权重0.1/0.25/0.5/1，共37项。'
            '后续年度公共排名曲线仅使用各年度之前已成熟的训练OOF标签；'
            '第一年度专用模型仅使用2020年前成熟训练样本，固定斜率不拟合当年标签。\n\n'
            '逐项完成全部5635800行、1212日的非涨停排序与并列关系检查、'
            '80/260/975日冷前缀逐位核验，原官方脚本评分过去收益率映射后的完整CSV。'
            '恒等锚点全部8项指标精确复现父方案，所有非IC评分项逐项精确不变。'
            '保留全部原始分数、官方缓存胶囊、输入与预测数值哈希、选参协议和源码。'
            '不读取测试标签；当前仅发布实际比较，不提前宣称候选推理与完整榜资格。\n\n'
            '发表事务等待第100轮完整榜任务自然结束，保证共用工作树顺序写入。'
            '所有发表只使用main。\n').encode('utf-8')
        for target, data in payload.items():
            sync.atomic(sync.WORKTREE / target, data)
        names = sorted(payload)
        for start in range(0, len(names), 50):
            sync.git('add', '-f', '--', *names[start:start + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(names)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '保存37项涨停条件排名方案的完整原始官方评分与控制', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified',
            'commit': commit, 'at_local': sync.now(), 'branch': 'main',
            'raw_git_blobs_verified': len(hashes), 'scored_records': 37,
            'best_official_score': proof['best']['connected_final_score'],
            'candidate_and_full_ranking_qualification_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_specialist_comparison_publication',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
