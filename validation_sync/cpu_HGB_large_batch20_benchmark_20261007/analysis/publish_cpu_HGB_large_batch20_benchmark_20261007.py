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
    closed('cpu_HGB_large_batch20_inference_benchmark')
    proof = read(A / 'cpu_HGB_large_batch20_benchmark_20261007/verification.json')
    assert proof['status'] == 'passed_actual20_saved_HGB_two_alternating_inference_repeats_all_bits_and_prefix_controls'
    out = A / 'cpu_HGB_large_batch20_benchmark_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), A/'benchmark_cpu_HGB_large_batch20_20261007.py',
        A/'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',A/'cpu_conditional_residual_hgb_codec_20261007.py',
        A/'cpu_conditional_residual_mlp_codec_20261007.py',A/'cpu_HGB_large_batch20_benchmark_admission_20261007.json',
        A/'cpu_conditional_residual_hgb20_bank_github_20261007/receipt.json']
    sources += list((A/'cpu_HGB_large_batch20_benchmark_20261007').glob('*.json'))
    service=A/'service_owned_workflows_20261006/cpu_HGB_large_batch20_inference_benchmark'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    bank=A/'cpu_conditional_residual_hgb_bank20_20261007'
    sources += [bank/item['name']/f"info_{item['year']}.json" for item in read(bank/'verification.json')['actual_models']]
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
            prefix = Path('validation_sync/cpu_HGB_large_batch20_benchmark_20261007')
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
            manifest = {'status': 'actual20_saved_HGB_two_alternating_native_and_independent_decoder_benchmark',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'remote_workers_dispatched':0,'actual_saved_native_models_tested':20,
                'two_alternating_repeats_model_count':40,'aggregate_seconds_per_repeat':proof['aggregate_seconds_per_repeat'],
                'median_aggregate_seconds':proof['median_aggregate_seconds'],
                'native_phase_speedup':proof['native_phase_speedup'],
                'independent_decoder_phase_speedup':proof['independent_decoder_phase_speedup'],
                'full_future_or_whole_goal_speedup_not_claimed':True,
                'new_fits':0,'new_model_selection_scores_by_this_publication':0,
                'selected_future_wrapper_adoption_not_claimed':True,
                'original_GPU_scientist_not_suspended_stopped_or_restarted': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 20个已训练HGB模型的推理批次交替测速\n\n'
                '仅使用训练期数据和已封存的20个原生模型，四条路径分别是原生256行、原生8192行、独立NumPy解码256行和独立解码8192行。'
                '两个重复的执行顺序相反，线程数均为4；全部输出按uint64逐位比较，并核验原年度OOF数组和各模型前缀。\n\n'
                '模型、预处理、树加法顺序和评分数学不变。记录各自推理阶段的中位耗时及倍数；不声称1599600行未来推理或整个目标的提速。'
                '第112轮已封存的候选推理封装尚未切换，本记录仅验证新执行实现。没有新拟合、选模评分或测试标签读取。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存20个HGB模型原生与独立解码扩大推理批次的两次交替测速与逐位核验', timeout=180)
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
