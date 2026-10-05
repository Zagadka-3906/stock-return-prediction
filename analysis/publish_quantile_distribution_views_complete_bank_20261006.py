"""Publish all30 virtual annual and6 full future distribution views and pending quality scope."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'quantile_distribution_views_bank_20261006'
FUTURE = A / 'quantile_distribution_views_future_qa_20261006'
SERVICE = A / 'service_owned_workflows_20261006/quantile_distribution_views_full_workflow'
OUT = A / 'quantile_distribution_views_bank_github_20261006'
PREFIX = Path('validation_sync/quantile_distribution_views_bank_20261006')


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
    while not (SERVICE / 'service_execution.json').exists():
        if (SERVICE / 'native_launch.json').exists():
            assert owned(sync.read(SERVICE / 'native_launch.json')), 'Actual controls are missing without a terminal record.'
        time.sleep(10)
    terminal = sync.read(SERVICE / 'service_execution.json')
    row = sync.read(SERVICE / 'native_launch.json')
    while owned(row):
        time.sleep(.2)
    if terminal['status'] == 'passed':
        proof = sync.read(FUTURE / 'verification.json')
        audit = sync.read(SOURCE / 'oof_audit.json')
        assert proof['status'] == audit['status'] == 'passed'
        assert audit['actual_virtual_annual_outputs'] == 30 and audit['actual_virtual_final_artifacts'] == 6
        assert proof['actual_full_future_views'] == 6 and proof['actual_native_fits'] == 0
        assert len(proof['checks']) == 6 and audit['new_quality_scores'] == proof['new_quality_scores'] == 0
        scope = sync.read(SOURCE / 'execution_scope.json')
        assert scope['status'] == 'passed' and scope['all_scientific_sources_fully_rehashed_unchanged']
        assert audit['new_model_fits'] == scope['new_model_fits'] == 0
        for filename, digest in scope['input_sha256'].items():
            assert sha(Path(filename)) == digest
        for check in proof['checks']:
            assert (check['rows'], check['days'], check['codes']) == (1599600, 344, 4650)
            assert check['actual_whole_future_selfcontained_independent_codec_bit_identical']
            assert check['actual_cold80_reload372000_rows_bit_identical']
            assert sha(SOURCE / check['model'] / 'model_2025.joblib') == check['model_sha256']
            assert sha(FUTURE / (check['model'] + '_raw.parquet')) == check['raw_sha256']

    else:
        assert (SOURCE / 'execution_scope.json').exists() or terminal.get('failure')
    sources = [Path(__file__), *A.glob('*quantile_distribution_views*20261006.py'),
        *A.glob('*quantile_distribution_views*20261006.json'),
        A / 'build_lossless_ranking_display_v4_20261006.py',
        A / 'verify_lossless_ranking_display_v6_20261006.py',
        A / 'lossless_ranking_runtime_adapter_v3_20261006.py',
        *[A / f'{prefix}{n}{suffix}.py' for n in (93, 94)
          for prefix,suffix in (('optimize_training_round','_v3'),('finalize_training_round','_v3'),('run_training_round','_v3_pipeline'))]]
    sources += sorted(SOURCE.rglob('*.json')) + sorted(SOURCE.glob('*.jsonl'))
    sources += sorted(SOURCE.glob('*/raw_202*.parquet'))
    sources += sorted(FUTURE.glob('*.json')) + sorted(FUTURE.glob('*.parquet'))
    sources += sorted(SERVICE.glob('*.json')) + sorted(SERVICE.glob('*.log'))
    sources += sorted((A / 'quantile_distribution_views_quality_queue_20261006').glob('*.json'))
    for name in ('quantile_distribution_views_full_workflow', 'quantile_distribution_views_quality_queue',
                 'quantile_distribution_views_preflight', 'quantile_distribution_views_preflight_publication'):
        folder = A / 'service_owned_workflows_20261006' / name
        sources += sorted(folder.glob('*.json'))
    for name in ('quantile_distribution_views_preflight_20261006', 'quantile_distribution_views_quality_generator_preflight_v2_20261006'):
        sources += sorted((A / name).glob('*.json'))

    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(50):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': terminal['status'], 'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual30_annual6_future_fixed_view_status': terminal['status'],
            'original198_and_new262_official_scores_full_scheme_causality_ranking_and_adoption_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 六种分位数分布组合：完整五年输出及全部未来X推理\n\n'
            '六种固定组合完成30份年度样本外输出，每种均覆盖5635800行、1212日、4650股票，'
            '逐年度核对原生300轮父模型、完全成熟的同一训练矩阵和标签、精确键及372000行冷启动前缀。'
            '另完成六种完整1599600行、344日未来X的独立自包含推理、重载和80日前缀检查。\n\n'
            '组合逐行排序三个原生收益分位数，比较区间中点、负区间宽度、上尾反向值，'
            '以及中位数减0.25、0.5、1倍区间宽度。没有新原生拟合、拟合权重、测试答案或未来价格标签。'
            '15个年度和3个最终原生收益模型全部复用；30加6是虚拟输出或组合文件数量。\n\n'
            '原有198条分位数完整评分保留；新增93/94轮124/138条全五年方案评分队列，'
            '在前序92/93轮完全合格后执行。完整收益率映射CSV官方总分、冻结、因果、候选和完整榜尚待完成。'
            '源码、精确输出和所有验证记录同步main，尚未证明整体优化或资源边界。\n'
        ).encode('utf-8')

        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '完成六种分位数组合30年度输出和全部未来X原生重载并保留262条评分队列', timeout=180)
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
