"""Publish genuine CPU controls, live GPU evidence and the owned deferred job on main."""
from pathlib import Path
import hashlib
import json
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import watch_validations_main_v2_20261005 as watcher
from publish_main_closeout_v2_20261005 import names, blob_hashes

sync = watcher.sync
PREFIX = Path('validation_sync/memory_efficient_mlp_controls_20261005')
OUT = A / 'memory_efficient_mlp_controls_github_20261005'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert not (OUT / 'receipt.json').exists()
    folders = ('memory_efficient_mlp_preflight_20261005', 'neural16384_actual_shared_memory_observation_20261005',
        'memory_efficient_mlp_gpu_recovery_v2_20261005')
    for folder in folders:
        proof = sync.read(A / folder / 'verification.json')
        assert proof['status'].startswith('passed')
        for source, expected in proof['source_sha256'].items():
            assert sha(source) == expected, source
    cpu = sync.read(A / folders[0] / 'verification.json')
    assert cpu['actual_small_control_fits'] == 11 and cpu['actual_full_annual_fits'] == 0
    followup = sync.read(A / folders[2] / 'verification.json')
    job = followup['job']
    process = psutil.Process(job['pid'])
    assert job['script'] in process.cmdline() and not Path(job['stderr']).read_text(encoding='utf-8')
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    parent = observer.parent()
    assert str(A / 'watch_validations_main_v3_20261005.py') in parent.cmdline()
    paused = []
    try:
        for p in (observer, parent):
            p.suspend()
            paused.append(p)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        selected = {ROOT / name for name in names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')}
        selected.add(Path(__file__))
        evidence = set()
        for folder in folders:
            evidence.update((A / folder).glob('*.json'))
        evidence.update(A / f'run_logs/memory_efficient_mlp_gpu_controls_20261005.{stream}.log' for stream in ('stdout', 'stderr'))
        evidence.add(A / 'main_candidate_source_closeout_v6_20261005/receipt.json')
        selected |= evidence
        captures, targets = {}, {}
        for source in sorted(selected):
            assert source.is_file() and source.suffix in ('.py', '.json', '.log'), source
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), source
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            name = destination.as_posix()
            targets[name] = data
            captures[relative.as_posix()] = {'published_path': name, 'sha256': hashlib.sha256(data).hexdigest(),
                'bytes': len(data), 'runtime_snapshot': source not in evidence and source.suffix == '.json' and (
                    'state' in source.stem or 'resume' in source.stem or 'optimization_boundary' in source.stem
                    or 'cost_evidence' in source.stem or 'directions' in source.stem)}
        baseline = cpu['saved_tensor_controls'][0]['CPU_actual_peak_unique_autograd_saved_nonparameter_bytes']
        reductions = {row['mode']: 1 - row['CPU_actual_peak_unique_autograd_saved_nonparameter_bytes'] / baseline for row in cpu['saved_tensor_controls']}
        manifest = {'status': 'actual_CPU_controls_and_owned_deferred_full_width_GPU_measurements_published',
            'at_local': sync.now(), 'files': captures, 'actual_small_CPU_fit_count': 11,
            'actual_gradient_and_update_controls': len(cpu['gradient_controls']),
            'CPU_peak_saved_autograd_nonparameter_tensor_reductions': reductions,
            'saved_tensor_reductions_are_not_GPU_runtime_peak_reductions': True,
            'checkpoint_32epoch_mature512_width_CPU_weights_bit_identical_to_original': True,
            'microbatch_32epoch_CPU_max_weight_difference': max(row['max_32epoch_state_abs_difference_from_original'] for row in cpu['mature_pilots']),
            'actual_owned16384_training_reached_logged_epoch': 4,
            'Windows_reported_owned_GPU_shared_usage_bytes': 4848615424,
            'terminal_GPU_waiter_registry_error_retained_before_any_fit': True,
            'actual_registry_verified_GPU_waiter_owned_live_at_publication': job['pid'],
            'original_native_GPU_work_untouched': True,
            'full32epoch15_annual3_final_and_official_quality_sources_still_pending': True,
            'actual_new_full_annual_fits': 0, 'actual_new16384_GPU_fits': 0, 'new_quality_scores': 0,
            'latest_qualified_round': 66, 'qualified_ranking_records': 9822, 'only_publication_branch': 'main',
            'test_labels_read': False, 'global_resource_exhaustion_established': False}
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded(manifest)
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 16384宽度训练的内存优化对照\n\n'
            '原32轮大模型训练已记录第4轮完成。独立核验实际进程身份、CPU计算时间推进和Windows进程GPU内存计数：'
            '两次约30秒间隔观察均报告4,848,615,424字节共享GPU内存；这不是OOM或硬件极限证明。\n\n'
            '新增梯度累积、激活重算和两者结合，保留有效批大小及AdamW更新频率。'
            'MSE与Huber各三种实现通过不等长尾批的实际float64梯度及更新检查。'
            '原实现、基准包装及三种新实现共完成11次真实成熟样本CPU控制训练；四个包装模型均完成4096条、512宽度、32轮，'
            '重载及80条记录前缀一致，三个新实现的未来标签污染检查通过。激活重算权重与原实现逐位一致，'
            '梯度累积及组合权重最大差约1.19e-7，需要独立官方评分。\n\n'
            'CPU中自动求导保存的非参数张量峰值分别减少75%、97.64%、99.41%；这仅度量该CPU控制里的保存张量，'
            '不能当成GPU总内存节省或16384完整拟合的证据。\n\n'
            '真实16384宽度GPU单批对照已排队，将等待原完整年度及最终GPU进程结束后执行。'
            '首次等待任务读错登记字段并在训练前终止，原代码、RUN和错误均保留；V2已通过实际进程登记和等待检查。'
            '三种新实现的15次完整年度训练、3次最终训练及完整官方方案评分仍待后续入口完成，不能以控制试验替代。'
            '完整榜仍9822条，最高分0.4510081068915626；未读取测试标签。\n\n'
            '参考实现语义：[PyTorch2.11激活重算](https://docs.pytorch.org/docs/2.11/checkpoint.html)、'
            '[有效批梯度累积](https://docs.pytorch.org/docs/2.11/notes/amp_examples.html#gradient-accumulation)、'
            '[Windows GPU内存计数](https://devblogs.microsoft.com/directx/gpus-in-the-task-manager/)。\n').encode('utf-8')
        for source, item in captures.items():
            if not item['runtime_snapshot']:
                assert sha(ROOT / source) == item['sha256'], source
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '验证三种MLP内存优化及真实共享显存，冻结后续GPU对照', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_only_main_verified_raw_CPU_controls_and_GPU_evidence',
            'commit': commit, 'at_local': sync.now(), 'files': len(targets),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}',
            'actual_small_CPU_control_fits': 11, 'new_official_quality_scores': 0}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for p in reversed(paused):
            if p.is_running():
                p.resume()


if __name__ == '__main__':
    main()
