"""Publish measured local acceleration and strict unfinished-grid repair evidence on main."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert read(p / 'service_execution.json')['status'] == 'passed', name
    return p


def main():
    closed('full_universe_HGB_preprocessing_memory_audit')
    closed('memory_bounded_numeric_preparation_preflight')
    closed('CPU_COMPACT_MLP44_round111_full_registration')
    closed('CPU_MLP44_round110_full_registration')
    proof = read(A / 'memory_bounded_numeric_preparation_preflight_20261007/verification.json')
    assert proof['status'] == 'passed_actual_historical372000_rows63_feature_preparation_bits_prefixes_and_allocation_controls'
    out = A / 'HGB_memory_and_numeric_preparation_controls_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[Path(p) for p in proof['input_sha256'] if Path(p).suffix.lower() in ('.py','.json','.md','.txt')]]
    for name in ('full_universe_HGB_preprocessing_memory_audit_20261007','memory_bounded_numeric_preparation_preflight_20261007'):
        sources += list((A/name).glob('*.json'))
    sources += [A/'audit_full_universe_HGB_preprocessing_memory_20261007.py']
    for name in ('full_universe_HGB_preprocessing_memory_audit','memory_bounded_numeric_preparation_preflight'):
        service=A/'service_owned_workflows_20261006'/name
        sources+=list(service.glob('*.json'))+list(service.glob('*.log'))
    resource=read(A/'full_universe_HGB_preprocessing_memory_audit_20261007/verification.json')
    pins = {**proof['input_sha256'], **resource['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(out / 'frozen_before_main_publication.json', {'input_sha256': pins, 'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held, retries = [], []
    restore = install()
    sync = helpers.sync
    old_git = sync.git

    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return old_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(t in str(error).lower() for t in ('tls', 'ssl', 'connection', 'timed out', 'unable to access')):
                    raise
                retries.append({'command': args[0], 'attempt': attempt + 1, 'error': str(error)[:1000]})
                if attempt == 2:
                    raise
                time.sleep(2)

    sync.git = retry_git
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        with LockedReadHashCache(pins) as scope:
            prefix = Path('validation_sync/HGB_memory_and_numeric_preparation_controls_20261007')
            payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
            files = {}
            for p in dict.fromkeys([*sources, out / 'frozen_before_main_publication.json']):
                data = p.read_bytes()
                assert not sync.SECRET.search(data), p
                raw_sha = hashlib.sha256(data).hexdigest()
                target = (prefix / p.relative_to(ROOT)).as_posix()
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
                    target += '.gz'
                payload[target] = data
                files[p.relative_to(ROOT).as_posix()] = {'published_path': target, 'original_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            manifest={'status':'published_actual_mature_training_counts_and_bit_identical_bounded_preparation_controls',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'verification_status':proof['status'],'actual_historical_rows':372000,'actual_features':63,
                'full_training_rows_final2025':6754006,'old_preparation_feature_storage_lower_bound_GiB':14.266395561397076,
                'new_native_fits':0,'new_official_scores':0,'scientific_workers_stopped_or_restarted':0,
                'not_adopted_in_frozen_or_live_HGB_training':True,
                'native24_fits_full6754006_preparation_or_observed_OOM_not_claimed':True,
                'no_data_prediction_arrays_or_model_weights_uploaded':True,
                'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            manifest['old_preparation_feature_storage_lower_bound_GiB']=max(r['prepare_simultaneous_feature_storage_lower_bound_GiB'] for r in resource['windows'])
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 全股票池HGB实际样本内存范围与分块预处理检查\n\n'
                '2020至2025六个成熟窗口逐一统计，最终2025训练6754006行。Float64原特征矩阵、原有预处理临时矩阵和保留的Polars数值表，'
                '在最终窗口预处理阶段合计至少约14.27GiB，尚不含键、标签、验证矩阵和其他进程。原门槛为12GiB。'
                '这是源码分配与实际行数推导；小矩阵C/F布局的NumPy内存分配也实测，未声称实际OOM或全局资源穷尽。\n\n'
                '8192行分块调用原预处理函数，保持原中位数、均值、标准差及计算顺序。'
                '372000行真实历史63特征的F64、C64、F32、非连续视图四种布局，分别两种相反顺序实测；'
                '输出float64位值、输入未修改、8192行跨块前缀及缺失、无穷、负零控制均通过。'
                '前缀计数是行数，不是交易日。\n\n'
                'F64布局旧实现额外tracemalloc峰值约536MiB，分块约191MiB；这些数字不含原输入、Polars表和其他进程。'
                '本记录尚未在已封存HGB24训练任务中采用新实现，没有新模型训练或选模评分。'
                '完整6754006行训练输入和24个原生模型验证仍须实际执行。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存HGB675万成熟样本内存范围及37万行分块预处理位值和分配检查', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit, 'at_local': sync.now(),
                'branch': 'main', 'raw_git_blobs_verified': len(hashes), 'new_quality_scores': 0,
                'all_source_inputs_initial_and_final_read_locked_full_rehash': True,
                'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
            print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    finally:
        sync.git = old_git
        for p in reversed(held):
            if p.is_running():
                p.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})
        create(out / 'transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
