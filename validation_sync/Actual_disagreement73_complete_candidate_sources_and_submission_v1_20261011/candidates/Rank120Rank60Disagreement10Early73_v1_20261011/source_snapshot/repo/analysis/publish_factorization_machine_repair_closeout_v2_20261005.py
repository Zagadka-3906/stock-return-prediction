"""Publish complete repaired FM evidence and unchanged official gain attribution."""
from pathlib import Path
import hashlib
import gzip
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher
from publish_main_closeout_v2_20261005 import names, blob_hashes

sync = watcher.sync
PREFIX = Path('validation_sync/factorization_machine_repair_closeout_20261005')
OUT = ROOT / 'analysis/factorization_machine_repair_closeout_20261005'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'receipt.json').exists()
    folders = ('factorization_machine_trained_interaction_audit_20261005',
        'factorization_machine_direct_router_preflight_v2_20261005',
        'factorization_machine_search_generator_preflight_v4_20261005',
        'factorization_machine_v4_workflow_handoff_20261005',
        'factorization_machine_future_qa_v2_20261005', 'round65_limit_up_gain_audit_v3_20261005')
    proofs = {folder: sync.read(ROOT / 'analysis' / folder / 'verification.json') for folder in folders}
    for value in proofs.values():
        assert value['status'].startswith('passed')
        for key in ('input_sha256', 'source_sha256', 'artifact_sha256'):
            for source, expected in value.get(key, {}).items():
                assert sha(source) == expected, source
    future = proofs['factorization_machine_future_qa_v2_20261005']
    assert future['actual_fulltraining_fits'] == 6 and future['new_fulltraining_fits_this_execution'] == 5
    assert sum(r['fit_artifact_existed_before_this_execution'] for r in future['checks']) == 1
    assert future['all6_models_fullfuture_reload_and_cold80_controls_passed']
    resources = sync.read(ROOT / 'analysis/factorization_machine_future_qa_v2_20261005/resource_summary.json')
    assert resources['status'] == 'passed' and not resources['actual_resources']['observation_errors']
    assert sha(ROOT / 'analysis/factorization_machine_future_qa_v2_20261005/actual_resource_samples.jsonl') == resources['actual_resources']['sample_file_sha256']
    manifests = {}
    for stage in ('annual', 'future'):
        receipt = sync.read(sync.OUT / f'factorization_machine_completed_{stage}_receipt.json')
        prefix = f'validation_sync/factorization_machine_completed_{stage}_20261005'
        raw = sync.subprocess.check_output(['git', 'show', f"{receipt['commit']}:{prefix}/manifest.json"], cwd=ROOT)
        manifest = json.loads(raw)
        expected = {v['published_path']: v['published_sha256'] for v in manifest['source_files'].values()}
        assert blob_hashes(receipt['commit'], expected) == expected
        manifests[stage] = {'commit': receipt['commit'], 'git_blob_sha256_verified_count': len(expected)}
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    parent = observer.parent()
    assert parent is not None and str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in parent.cmdline()
    native_run = sync.read(ROOT / 'analysis/factorization_machine_native_github_run_v2_20261005.json')
    assert not psutil.pid_exists(native_run['pid'])
    assert sync.read(ROOT / 'analysis/factorization_machine_native_github_state_v2_20261005.json')['status'] == 'completed_native_evidence_publication'
    suspended = []
    try:
        for process in (observer, parent):
            process.suspend()
            suspended.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        pending = names('ls-files', '--modified') | names('ls-files', '--others', '--exclude-standard')
        evidence = set()
        for folder in (*folders, 'factorization_machine_future_qa_20261005',
                       'round65_limit_up_gain_audit_20261005', 'round65_limit_up_gain_audit_v2_20261005'):
            evidence.update(p for p in (ROOT / 'analysis' / folder).glob('*.json') if p.is_file())
        evidence.update(ROOT / 'analysis/run_logs' / name for name in (
            'factorization_machine_full_future_20261005.stderr.log',
            'round65_limit_up_gain_audit_20261005.stderr.log',
            'round65_limit_up_gain_audit_v2_20261005.stderr.log',
            'round65_limit_up_gain_audit_v2_repaired_20261005.stderr.log'))
        selected = {ROOT / name for name in pending} | evidence
        raw_dirty = sync.subprocess.check_output(['git','ls-files','--modified','-z'],cwd=sync.WORKTREE) + sync.subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=sync.WORKTREE)
        dirty = {p.decode('utf-8') for p in raw_dirty.split(b'\0') if p}
        allowed = {p.relative_to(ROOT).as_posix() for p in selected}
        assert all(name in allowed or name.startswith(PREFIX.as_posix() + '/') for name in dirty), dirty - allowed
        paths, captures = [], {}
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for source in sorted(selected):
            assert source.is_file() and source.suffix in ('.py', '.json', '.md', '.log', '.png')
            data = source.read_bytes()
            assert not sync.SECRET.search(data)
            original_sha = hashlib.sha256(data).hexdigest()
            if source.suffix == '.json':
                json.loads(data.decode('utf-8-sig'))
            relative = source.relative_to(ROOT)
            destination = PREFIX / relative if source in evidence else relative
            if len(data) >= 5 * 1024**2:
                assert source.suffix == '.json' and relative.parts[0] == 'results'
                destination = PREFIX / (relative.as_posix() + '.gz')
                data = gzip.compress(data, compresslevel=6, mtime=0)
                assert hashlib.sha256(gzip.decompress(data)).hexdigest() == original_sha
            assert len(data) < 90 * 1024**2
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            captures[relative.as_posix()] = {'published_path': destination.as_posix(),
                'sha256': hashlib.sha256(data).hexdigest(), 'source_sha256': original_sha, 'bytes': len(data),
                'runtime_snapshot': source not in evidence and source.suffix == '.json' and (
                    'state' in source.stem or 'resume' in source.stem or
                    source.stem.startswith(('optimization_boundary', 'optimization_fit_cost', 'next_experiment')))}
        manifest = {'status': 'passed_complete_repaired_native_scopes_and_independent_full_gain_attribution',
            'at_local': sync.now(), 'previous_main': head, 'files': captures,
            'actual_complete_annual_fits': 30, 'actual_complete_final_fit_artifacts': 6,
            'new_final_fits_in_repaired_execution': 5, 'previous_final_fit_reused': 1,
            'actual30_complete_models_independent_pair_formula_passed': True,
            'actual30_direct_router_controls_passed': True,
            'native_publication_git_blobs_verified': manifests,
            'original_failure_preserved': "KeyError: 'hidden'",
            'failure_is_router_error_not_physical_capacity_exhaustion': True,
            'actual_official_FM_quality_rounds73_74_still_pending': True,
            'actual_predecessors72_73_required': True, 'planned_scores': {'73': 124, '74': 138},
            'R65_gain_verified_with_all5635800_original_training_validation_rows': True,
            'R65_complete_method_causal_scope_passed': True, 'completed_connected_ranking_records': 9604,
            'only_publication_branch': 'main', 'live_scientific_jobs_untouched': True,
            'new_quality_scores_by_this_publication': 0, 'test_labels_read': False,
            'global_resource_exhaustion_established': False}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json', sync.encoded(manifest))
        document = ('# 因子分解机完整训练与推理修复记录\n\n'
            '六种原始63特征配置的30次完整年度拟合、6个成熟最终模型及全量1,599,600条未来推理检查均完成。'
            '30个真实完整训练模型通过独立预处理和显式特征对交互公式检查，二阶交互均实际生效。\n\n'
            '原分发器误用了模型类型名称，导致最终推理进入MLP路径并报hidden缺失；失败源、协议和资源证据保留。'
            '新分发器直接检查6个完整FM和24个既有模型，通过预测和前缀位级一致性；不依靠旧codec挂钩掩盖分发错误。'
            '复用此前已经训练的一个最终模型，新执行仅补齐其余5次最终拟合；训练配置和参数均未更改。\n\n'
            '第73/74轮等待任务已切换到v4，124/138项完整评分及真实前序方案要求保留，尚未产生这两轮官方分数。'
            '第65轮增益在全部5,635,800条原始训练验证记录上复核：非涨停排序和每个Top组成员相同，全部增益来自IC。'
            '官方标签保持原始精度；float32特征表标签不替代官方评分标签。归因检查原失败记录亦保留。\n\n'
            '所有验证仍直接同步main。第65轮因果验证、候选预测及9,604条完整榜均已通过，第66轮已启动。运行状态只是提交时快照，后续方案评分继续执行；'
            '反复使用既有验证年份的选模偏差未校正，未读取实际测试标签，未宣告方法或物理资源耗尽。'
            '模型、原始数据和预测留在本地D/E盘。\n')
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md', document.encode('utf-8'))
        paths.extend(((PREFIX / 'manifest.json').as_posix(), (PREFIX / 'README.md').as_posix()))
        for source, item in captures.items():
            if not item['runtime_snapshot']:
                assert sha(ROOT / source) == item['source_sha256'], source
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '完成因子分解机30折与6最终模型，修复直接分发并复核完整验证增益', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {v['published_path']: v['sha256'] for v in captures.values()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_only_main_and_all_selected_git_blob_sha256',
                   'at_local': sync.now(), 'commit': commit, 'files': len(paths),
                   'actual30_annual6_final_and_all_future_controls_complete': True,
                   'new_quality_scores': 0,
                   'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(OUT / 'receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
