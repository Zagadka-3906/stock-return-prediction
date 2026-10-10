"""Publish closed GOSS controls and verify raw scientific Git export bytes."""
from pathlib import Path
import gzip
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
PREFIX = Path('validation_sync/gradient_sampling_controls_20261005')
OUT = A / 'gradient_sampling_controls_github_20261005'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not (OUT / 'receipt.json').exists()
    folders = ('gradient_sampling_preflight_20261005', 'gradient_sampling_direct_router_preflight_20261005',
        'gradient_sampling_search_generator_preflight_20261005', 'gradient_sampling_followups_20261005',
        'gradient_sampling_observer_integration_preflight_v12_20261005',
        'factorization_machine_release_dispatch_preflight_v5_20261005',
        'factorization_machine_release_dispatch_handoff_v5_20261005')
    for folder in folders:
        proof = sync.read(A / folder / 'verification.json')
        assert proof['status'].startswith('passed')
        for field in ('source_sha256', 'input_sha256'):
            for source, expected in proof.get(field, {}).items():
                assert sha(source) == expected, source
    followup = sync.read(A / 'gradient_sampling_followups_20261005/verification.json')
    for job in (followup['native'], followup['future'], *followup['quality_rounds'], followup['monitor']):
        assert job['script'] in psutil.Process(job['pid']).cmdline()
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    audit = sync.read(A / 'validation_export_raw_bytes_audit_20261005/pre_repair.json')
    assert not audit['unresolved']
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
        assert head == audit['original_commit']
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        paths, repaired = [], {}
        # This stays in the publisher worktree; future automatic rounds inherit it.
        sync.atomic(sync.WORKTREE / 'validation_sync/.gitattributes', b'* -text\n')
        paths.append('validation_sync/.gitattributes')
        for item in audit['reconstructable_only_CRLF']:
            name = item['path']
            data = sync.subprocess.check_output(['git', 'show', f'{head}:{name}'], cwd=ROOT)
            assert hashlib.sha256(data).hexdigest() == item['current_sha256']
            original = data.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
            assert hashlib.sha256(original).hexdigest() == item['target_sha256']
            assert len(original) == item['expected_bytes']
            sync.atomic(sync.WORKTREE / name, original)
            paths.append(name)
            repaired[name] = item['target_sha256']
        selected = {ROOT / name for name in names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')}
        selected.add(ROOT / '后续选模标准.md')
        evidence = {A / 'validation_export_raw_bytes_audit_20261005/pre_repair.json'}
        for folder in folders:
            evidence.update((A / folder).glob('*.json'))
        evidence.update(A / f'run_logs/actual_optimization_monitor_v{n}_20261005.stderr.log' for n in (10, 11))
        evidence.add(A / 'optimization_20261003_r66/provenance_scope_execution_recovery_v3_20261005.json')
        selected |= evidence
        captures = {}
        for source in sorted(selected):
            assert source.is_file()
            assert source.suffix in ('.py', '.json', '.md', '.png', '.log') or source.name == '.gitattributes', source
            data = source.read_bytes()
            assert not sync.SECRET.search(data)
            original_sha = hashlib.sha256(data).hexdigest()
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            if len(data) >= 5 * 1024**2:
                assert source.suffix == '.json' and relative.parts[0] == 'results'
                destination = PREFIX / (relative.as_posix() + '.gz')
                data = gzip.compress(data, compresslevel=6, mtime=0)
                assert hashlib.sha256(gzip.decompress(data)).hexdigest() == original_sha
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            captures[relative.as_posix()] = {'published_path': destination.as_posix(),
                'sha256': hashlib.sha256(data).hexdigest(), 'source_sha256': original_sha, 'bytes': len(data),
                'runtime_snapshot': source not in evidence and source.suffix == '.json' and (
                    'state' in source.stem or 'resume' in source.stem or 'optimization_boundary' in source.stem
                    or 'cost_evidence' in source.stem or 'directions' in source.stem)}
        manifest = {'status': 'closed_controls_and_raw_validation_export_byte_repair',
            'at_local': sync.now(), 'files': captures, 'raw_export_repairs': repaired,
            'original_scientific_sources_and_scores_unchanged': True,
            'all7_automatic_round_export_manifests_checked': True, 'round_artifacts_checked': audit['checked'],
            'six_actual4096_row48_round_GOSS_pilots_passed': True,
            'six_pilot_and30_inherited_native_direct_and_codec_routes_passed': True,
            'actual124_138_138_schema_generator_controls_passed': True,
            'actual30_annual300_round_GOSS_fits_not_yet_completed': True,
            'actual6_GOSS_final_fits_and262_official_scores_still_pending': True,
            'FM73_74_actual_release_dispatch_corrected_without_editing_frozen_sources': True,
            'only_publication_branch': 'main', 'latest_qualified_round': 66, 'qualified_ranking_records': 9822,
            'test_labels_read': False, 'new_quality_scores_by_publication': 0,
            'global_resource_exhaustion_established': False}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md', (
            '# GOSS 梯度采样与发布检查\n\n'
            '原始63特征、同样的成熟训练窗口和300轮预算；六个新配置仅改变GOSS采样率和秩/收益目标。'
            '六个4096条成熟样本48轮模型、未来标签污染、独立叶公式、重载和前缀检查已通过。'
            '六个新试验模型与30个既有完整模型通过直接分发和完整codec检查。\n\n'
            '第75/76轮124/138项完整方案网格的生成检查通过，尚未进行这两轮官方评分。'
            '30次完整年度训练和6次最终训练会先等待当前16384宽度模型的年度及最终训练阶段结束。'
            '14GiB预留是调度规则；未宣告物理资源耗尽。第73/74轮实际最终化入口已改正，原文件保留。\n\n'
            '第66轮218项评分、候选和因果检查、恢复全量来源复核已完成，完整榜9822条。'
            '自动上传的第60至66轮中87个JSON仅发生CRLF到LF转换；本提交恢复与各原清单完全一致的字节，'
            '没有改变评分或科学源文件。验证目录设置-text，后续自动导出保留原始字节。'
            '原选模标准文件同样保留原始字节。\n\n'
            '未读取测试标签；多次选模偏差未校正；数据、权重、预测及临时文件继续存放D/E。\n').encode('utf-8'))
        paths.extend(((PREFIX / 'manifest.json').as_posix(), (PREFIX / 'README.md').as_posix()))
        for source, item in captures.items():
            if not item['runtime_snapshot']:
                assert sha(ROOT / source) == item['source_sha256'], source
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '验证GOSS新采样方案，修复FM发布入口并保留验证原始字节', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {**repaired, **{item['published_path']: item['sha256'] for item in captures.values()}}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_only_main_raw_git_blobs_and_all_closed_controls',
            'commit': commit, 'at_local': sync.now(), 'files': len(paths), 'repaired_raw_round_artifacts': len(repaired),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}',
            'new_quality_scores': 0}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(paused):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
