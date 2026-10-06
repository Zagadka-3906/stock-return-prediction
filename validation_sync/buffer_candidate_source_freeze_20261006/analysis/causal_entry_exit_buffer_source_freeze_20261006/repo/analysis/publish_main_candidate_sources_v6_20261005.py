"""Publish the verified pending-round repair and current main-only state."""
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
PREFIX = Path('validation_sync/main_candidate_source_closeout_v6_20261005')
OUT = A / 'main_candidate_source_closeout_v6_20261005'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert not (OUT / 'receipt.json').exists()
    proof_path = A / 'factorization_machine_candidate_source_preflight_v6_20261005/verification.json'
    proof = sync.read(proof_path)
    assert proof['status'].startswith('passed')
    for source, digest in proof['source_sha256'].items():
        assert sha(source) == digest, source
    handoff_folder = A / 'factorization_machine_candidate_source_handoff_v6_20261005'
    handoff = sync.read(handoff_folder / 'verification.json')
    assert handoff['status'].startswith('passed') and handoff['all_other_registry_jobs_unchanged']
    for job in handoff['jobs']:
        assert psutil.Process(job['pid']).cmdline()[-len(job['script_args']):] == job['script_args']
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    parent = observer.parent()
    assert str(A / 'watch_validations_main_v3_20261005.py') in parent.cmdline()
    paused = []
    try:
        for process in (observer, parent):
            process.suspend()
            paused.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('rev-parse', 'refs/heads/main', cwd=ROOT) == head
        assert sync.git('branch', '--show-current', cwd=ROOT) == 'main'
        assert sync.git('for-each-ref', '--format=%(refname)', 'refs/heads', cwd=ROOT).splitlines() == ['refs/heads/main']
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        assert sync.git('ls-remote', '--symref', 'origin', 'HEAD').splitlines()[0] == 'ref: refs/heads/main\tHEAD'
        historical_heads = ('8a8fa5702acdd5ada0e53df97640e919c9970f16', '49477a6a8834c68a5d9990887129ac26279a519d')
        for old in historical_heads:
            sync.git('merge-base', '--is-ancestor', old, head, cwd=ROOT)
        assert sync.git('config', '--get-all', 'remote.origin.fetch', cwd=ROOT) == '+refs/heads/main:refs/remotes/origin/main'
        assert sync.git('config', '--get-all', 'remote.origin.push', cwd=ROOT) == 'refs/heads/main:refs/heads/main'
        branch_proof = {'status': 'passed_only_main_and_all_old_heads_ancestors',
            'at_local': sync.now(), 'prepublication_main': head, 'verified_merged_historical_heads': list(historical_heads),
            'local_branches': ['main'], 'remote_branches': ['main'], 'GitHub_default_branch': 'main',
            'future_validation_publication_branch': 'main', 'other_worktree_detached': True}
        OUT.mkdir(exist_ok=True)
        branch_path = OUT / 'branch_verification.json'
        with branch_path.open('x', encoding='utf-8') as stream:
            json.dump(branch_proof, stream, ensure_ascii=False, indent=2)
        selected = {ROOT / name for name in names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')}
        selected.add(Path(__file__))
        evidence = {proof_path, branch_path}
        evidence.update(handoff_folder.glob('*.json'))
        evidence.update(A / 'validation_export_raw_bytes_audit_20261005' / name for name in ('post_repair.json', 'receipt.json'))
        evidence.add(A / 'gradient_sampling_controls_github_20261005/receipt.json')
        selected |= evidence
        captures = {}
        targets = {}
        for source in sorted(selected):
            assert source.is_file() and source.suffix in ('.py', '.json'), source
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), source
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            name = destination.as_posix()
            assert name not in targets
            targets[name] = data
            captures[relative.as_posix()] = {'published_path': name,
                'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                'runtime_snapshot': source not in evidence and source.suffix == '.json' and (
                    'state' in source.stem or 'resume' in source.stem or 'optimization_boundary' in source.stem
                    or 'cost_evidence' in source.stem or 'directions' in source.stem)}
        manifest = {'status': 'verified_main_only_pending_release_and_candidate_source_closeout',
            'at_local': sync.now(), 'files': captures, 'branch_verification': branch_proof,
            'latest_completed_round': 66, 'qualified_ranking_records': 9822,
            'FM73_74_actual_publication_imports_and_candidate_sources_passed': True,
            'unchanged_official_planned_records': {'73': 124, '74': 138},
            'source_packaging_controls_are_not_candidate_forecast_validation': True,
            'native_full_training_and_all_other_jobs_preserved': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'global_resource_exhaustion_established': False}
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded(manifest)
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# main 分支及待验证方案来源检查\n\n'
            '本地、远程、默认和后续自动上传分支均为 main。两个原分支最后提交均已在 main 历史中。'
            '历史验证保留在主分支；大型完整榜的原始字节已在无损压缩档案中核对。\n\n'
            '第73/74轮实际评分仍使用原V4实验模块，官方网格仍为124/138条。'
            '修正V6驱动将实际最终化模块同时绑定到报告入口，避免报告重新导入指向旧轮次的历史脚本。'
            '候选将复制实际V6最终化及驱动来源，并保存旧脚本供复核。'
            '实际报告导入、模块闭包、来源逐字节复制、重复复制一致和已发布候选拒绝修改的检查均通过。\n\n'
            '本次来源检查没有进行候选全量预测，没有新增训练或官方评分。'
            '第73/74轮只替换了尚未开始评分的两个等待进程；16384宽度32轮完整训练及其他任务继续运行。'
            '候选全量推理、官方评分和因果检查仍将在各轮实际执行时完成。'
            '运行状态是带时间的快照，会在训练推进后更新；临时文件和模型继续存放D/E。\n').encode('utf-8')
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
            '统一main来源记录并修复第73至74轮报告入口和候选脚本绑定', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        assert sync.git('for-each-ref', '--format=%(refname)', 'refs/heads', cwd=ROOT).splitlines() == ['refs/heads/main']
        receipt = {'status': 'pushed_verified_only_main_and_actual_source_bytes',
            'commit': commit, 'at_local': sync.now(), 'files': len(targets),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}',
            'historical_heads_merged': list(historical_heads), 'new_model_fits': 0, 'new_quality_scores': 0}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(paused):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
