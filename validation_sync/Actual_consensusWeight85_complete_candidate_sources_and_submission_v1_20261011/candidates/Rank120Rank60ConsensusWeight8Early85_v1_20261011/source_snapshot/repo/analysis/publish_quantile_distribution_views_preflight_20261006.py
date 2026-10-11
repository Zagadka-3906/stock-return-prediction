"""Publish actual current service-owned full-fit GPU resource observations."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'quantile_distribution_views_preflight_20261006'
SERVICE = A / 'service_owned_workflows_20261006/quantile_distribution_views_preflight'
OUT = A / 'quantile_distribution_views_preflight_github_20261006'
PREFIX = Path('validation_sync/quantile_distribution_views_preflight_20261006')


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
        proof = sync.read(SOURCE / 'verification.json')
        assert proof['status'] == 'passed_actual_six_distribution_views_native_cold80_independent_codec_and_math_controls'
        assert proof['actual_native_views_checked'] == 6 and len(proof['checks']) == 6
        assert proof['pilot_weights_written_to_disk'] == proof['new_model_fits'] == proof['new_quality_scores'] == 0
        assert proof['test_labels_read'] is False
        for filename, digest in proof['input_sha256'].items():
            assert sha(Path(filename)) == digest
        for check in proof['checks']:
            assert (check['rows'], check['days'], check['codes']) == (372000, 80, 4650)
            assert check['actual_native_primary_vs_independent_codec_cold80_bit_identical']
            assert check['actual32768row_crossing_constant_and_future_head_poison_controls_passed']

    else:
        assert (SOURCE / 'failure.json').exists()
    sources = [Path(__file__), *A.glob('*quantile_distribution_views*20261006.py'),
        *A.glob('*quantile_distribution_views*20261006.json'),
        *[A / f'{prefix}{n}{suffix}.py' for n in (93, 94) for prefix,suffix in (('optimize_training_round','_v3'),('finalize_training_round','_v3'),('run_training_round','_v3_pipeline'))]]
    sources += sorted((A / 'quantile_distribution_views_quality_generator_preflight_v2_20261006').glob('*.json'))
    sources += sorted(SOURCE.glob('*.json')) + sorted(SOURCE.glob('*.log'))
    sources += sorted(SERVICE.glob('*.json')) + sorted(SERVICE.glob('*.log'))
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
            'actual_six_native_cold80_component_control_status': terminal['status'],
            'all_original_native_fit_andquality_scopes_preserved': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 六种固定分位数分布组合的原生推理预检查\n\n'
            '先逐行排序10%、50%、90%三个收益分位数预测，然后固定比较区间中点、负区间宽度、'
            '上尾反向值，以及中位数减0.25、0.5、1倍区间宽度。全部公式和系数在推理前固定，'
            '没有使用测试答案、未来价格重建标签或未来表现选择方案。\n\n'
            '六种组合均完成真实80天372000行的独立原生推理与内存序列化重载，'
            '核对三个原生300轮模型与完全成熟的训练元数据；另检查32768行交叉分位数、'
            '常数及未来行扰动。无效价格行在反向与排序后统一恢复原有哨兵值。'
            '试验模型权重只在内存缓冲中序列化，没有新增原生拟合或官方分数。\n\n'
            '搜索生成器核对93轮124条、94轮138条以及独立主模型胜出的另一分支。'
            '生成器使用合成排序值，不是实际官方成绩。原有198条评分完整保留；'
            '另有262条完整五年收益映射CSV的官方评分、冻结、因果、候选、完整榜与main发布待完成。\n'
        ).encode('utf-8')

        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '验证六种分位数组合真实80天原生重载和262条搜索分支，保留原有198条方案', timeout=180)
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
