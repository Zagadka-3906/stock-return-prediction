"""Publish complete two-year saved-output diversity evidence without extra quality gates."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'quantile_native_output_diversity_20261006'
SERVICE = A / 'service_owned_workflows_20261006/quantile_native_output_diversity'
OUT = A / 'quantile_native_output_diversity_github_20261006'
PREFIX = Path('validation_sync/quantile_native_output_diversity_20261006')


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
        assert proof['status'] == 'passed_actual_two_complete_annual_native_output_diversity_checks'
        assert proof['years'] == [2020, 2021] and proof['total_rows_each_model'] == 2259900
        assert proof['actual_new_native_models_checked'] == 8
        assert proof['actual_new_model_fits'] == proof['new_quality_scores'] == 0
        assert not proof['labels_loaded'] and proof['diagnostics_do_not_change_any_required_grid_or_adoption_gate']
        for filename, digest in proof['input_sha256'].items():
            assert sha(Path(filename)) == digest
        for year in proof['years']:
            yearly = sync.read(SOURCE / f'diagnostic_{year}.json')
            assert yearly['full_saved_prediction_rows'] == 1129950
            assert yearly['complete_annual_days'] == 243 and yearly['codes'] == 4650
            assert len(yearly['pairs']) == 28 and yearly['all_saved_keys_bit_identical']
    else:
        assert (SOURCE / 'failure.json').exists()
    sources = [Path(__file__), A / 'verify_quantile_native_output_diversity_20261006.py']
    sources += sorted(SOURCE.glob('*.json')) + sorted(SOURCE.glob('*.jsonl'))
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
            'actual_two_complete_annual_prediction_diagnostic_status': terminal['status'],
            'all20_annual_fits_and198_official_scores_and_native_bank_promotion_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 两个完整年度的原生输出互补性诊断\n\n'
            '2020和2021各1129950行、243日、4650股票，八个模型完整样本外输出键逐位对齐，'
            '核对原始文件、训练矩阵、目标、键和标签成熟元数据，以及八个新原生模型的实际300轮。'
            '四种分位数目标与既有两种平方损失树和两种岭回归逐日比较原生排序与有效价格行的前10%集合，'
            '共两年56组比较，没有读取标签，没有新增拟合或官方分数。\n\n'
            '四种目标确实产生不同输出。收益率10%分位数与既有收益率平方损失树的原生前10%重合率为'
            '2020年13.48%、2021年8.68%；90%分位数与既有排名树的日均Spearman为-0.328和-0.398。'
            '这些是预测差异证据，不构成收益优势。中位数与两侧尾部可进一步作为位置、跨度及风险惩罚的对照方向。\n\n'
            '诊断的前10%仅针对价格有效行，用固定人数和股票顺序处理并列，未加载涨停和标签；'
            '不是官方指标或换手率。原有20个年度模型及198条完整五年方案评分全部保留，'
            '最终采用仍以官方完整收益映射CSV总分决定。没有新增门槛或全局资源边界结论。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核对八个模型完整两年原生输出差异并保留全部56组诊断记录', timeout=180)
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
