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
    closed('numpy_daily_ranks_full_parent_graph_preflight_v2')
    closed('CPU_MLP44_round110_full_registration')
    proof = read(A / 'numpy_daily_ranks_full_parent_graph_preflight_v2_20261007/verification.json')
    assert proof['status'] == 'passed_actual_R88_parent5635800_numpy_daily_ranks_and_cold80_260_975_bits'
    out = A / 'numpy_daily_ranks_full_parent_controls_v2_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), A / 'exact_numpy_daily_ranks_20261007.py',
        A / 'verify_numpy_daily_ranks_full_parent_graph_v2_20261007.py',
        A / 'exact_numpy_daily_ranks_benchmark_20261007/verification.json']
    sources += list((A / 'numpy_daily_ranks_full_parent_graph_preflight_v2_20261007').glob('*.json'))
    service=A/'service_owned_workflows_20261006/numpy_daily_ranks_full_parent_graph_preflight_v2'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    pins = {**proof['input_sha256'], **{str(p): sha(p) for p in sources}}
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
            prefix = Path('validation_sync/numpy_daily_ranks_full_parent_controls_20261007')
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
            manifest = {'status':'published_actual_numpy_daily_ranks_full_R88_parent_graph_controls',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'verification_status':proof['status'],'actual_full_parent_rows':5635800,
                'actual_original_full_and_two_numpy_full_controls':3,'actual_cold_prefixes':[80,260,975],
                'new_native_fits':0,'new_official_scores':0,'scientific_workers_stopped_or_restarted':0,
                'full_future_graph_all8_official_metrics_and_whole_goal_speedup_not_claimed':True,
                'no_data_prediction_arrays_or_model_weights_uploaded':True,
                'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# NumPy按日排名完整R88父方案图实际检查\n\n'
                '原父方案图完整5635800行回放，以及NumPy排名的两次完整回放，均逐位等于已冻结的R88验证预测。'
                '另外清空根模型和层缓存，以80、260、975天冷前缀验证逐位相同。原排名函数绑定在结束时恢复。\n\n'
                '本控制等待第114轮实际验证、main及闭合后执行，未停止任何既有科学进程。'
                '没有新模型训练或选模评分。计时仅作为检查耗时，不能解释为公平的整图或全任务加速倍率。'
                '本控制未覆盖完整测试期推理和八项官方评分；未采用到已冻结方案。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存NumPy每日排名完整父模型图及三个冷前缀的实际位值等价证据', timeout=180)
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
