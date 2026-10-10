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
    closed('cpu_compact_conditional_residual_mlp_codec_preflight')
    folder = A / 'cpu_compact_conditional_residual_mlp_codec_preflight_20261007'
    proof = read(folder / 'verification.json')
    assert proof['status'] == 'passed_actual_four_historical_CPU_MLP_codec_controls'
    assert proof['actual_diagnostic_fits'] == len(proof['records']) == 4
    assert proof['actual_selection_model_fits'] == proof['actual_official_scores'] == 0
    out = A / 'compact_MLP_codec_preflight_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), *[A / n for n in (
        'cpu_compact_conditional_residual_mlp_bank20_plan_20261007.json',
        'cpu_compact_conditional_residual_mlp_bank20_admission_20261007.json',
        'verify_cpu_compact_conditional_residual_mlp_codec_preflight_20261007.py',
        'train_cpu_compact_conditional_residual_mlp_bank20_20261007.py',
        'run_compact_conditional_residual_mlp44_official_comparison_20261007.py',
        'publish_cpu_compact_conditional_residual_mlp20_evidence_20261007.py',
        'cpu_conditional_residual_mlp_codec_20261007.py',
        'conditional_residual_mlp_CDF_transform_20261007.py')]]
    sources += [folder / 'verification.json', folder / 'frozen_before_actual_controls.json']
    service = A / 'service_owned_workflows_20261006/cpu_compact_conditional_residual_mlp_codec_preflight'
    sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    for name in ('cpu_compact_conditional_residual_mlp_native_bank20',
        'cpu_compact_conditional_residual_mlp20_bank_evidence_publication',
        'compact_conditional_residual_mlp44_official_comparison',
        'cpu_compact_conditional_residual_mlp20_scores_evidence_publication'):
        service = A / 'service_owned_workflows_20261006' / name
        sources += [service / n for n in ('job_definition.json', 'verified_hidden_launch.json', 'native_launch.json')]
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
            prefix = Path('validation_sync/compact_MLP_codec_preflight_20261007')
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
            manifest = {'status': 'actual_four_compact_CPU_MLP_historical_codec_diagnostics_and_predeclared20_44_grid',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'actual_diagnostic_model_fits': 4, 'actual_new_selection_model_fits': 0,
                'actual_official_quality_scores': 0, 'prospective_native_fit_count': 20,
                'prospective_official_comparison_count': 44,
                'four_hidden_architectures': [[16], [32], [16], [32]], 'activation_order': ['relu', 'relu', 'tanh', 'tanh'],
                'actual_saved_native_independent_NumPy_and0_1_79_256_511_601_prefix_bits_exact': True,
                'native_training_waits_actual_R90_R110_and_alternating_benchmark_closure': True,
                'future_candidate_and_full111_registration_still_to_prepare_not_claimed_complete': True,
                'scientific_workers_stopped_or_restarted': 0, 'remote_workers_dispatched': 0,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 16与32宽度CPU条件残差网络诊断与后续网格\n\n'
                '四个新宽度配置：16/32单隐藏层各采用ReLU或tanh。此前已训练64及128_64，本记录不把MLP家族宣称为从未覆盖。'
                '四个历史512行、2epoch诊断实际完成，601行保存重载、独立NumPy解码及0/1/79/256/511/601行前缀逐位一致。\n\n'
                '四个诊断不参与选模，正式模型与官方分数均为0。正式网格为20次成熟窗口拟合、44项最终映射CSV官方比较；'
                '训练必须等当前R90/R110与排序缓存重复测速自然闭合，评分串行检查RAM和原队列写者。'
                '未来获胜候选和完整第111轮流程仍需准备，本预检不冒充完整方案验证。\n\n'
                '仅训练集，固定106教师、共同2020—2024向前验证、首年无此前成熟OOF为恒等；24epoch无验证早停。'
                '仅官方综合分选优，训练验证多次选择偏差未校正。科学GPU进程保留，D/E本机存储，GitHub仅main。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存四个16与32宽度CPU网络历史重载解码真实诊断和20拟合44比较预定网格', timeout=180)
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
