"""Automatically publish closed native training/future evidence on main only."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def publish(stage):
    assert stage in ('annual', 'future')
    receipt_path = sync.OUT / f'factorization_machine_completed_{stage}_receipt.json'
    if receipt_path.exists():
        return sync.read(receipt_path)
    bank = Path(sync.read(ROOT / 'analysis/factorization_machine_storage_20261005.json')['output_directory'])
    files = {Path(__file__), ROOT / 'analysis/factorization_machine_native_github_run_v2_20261005.json'}
    checks = []
    if stage == 'annual':
        audit = sync.read(bank / 'oof_audit.json')
        execution = sync.read(bank / 'training_execution_scope.json')
        assert audit['status'] == execution['status'] == 'passed' and audit['actual_annual_fits'] == 30
        files |= {p for p in bank.glob('*.json') if p.is_file()}
        infos = list(bank.glob('*/info_202[0-4].json'))
        assert len(infos) == 30
        for source in infos:
            info = sync.read(source)
            assert info['status'] == 'passed' and info['new_model_fits'] == 1 and info['completed_training_epochs']==32
            assert sha(source.parent / f"model_{info['year']}.joblib") == info['model_sha256']
            assert sha(source.parent / f"raw_{info['year']}.parquet") == info['prediction_sha256']
            assert sync.read(bank / f"prefix_control_{info['model']}_{info['year']}.json")['status'] == 'passed'
            assert sync.read(bank / f"boundary_control_{info['model']}_{info['year']}.json")['status'] == 'passed'
            checks.append({'model': info['model'], 'year': info['year'], 'info_sha256': sha(source),
                'model_sha256': info['model_sha256'], 'raw_sha256': info['prediction_sha256']})
        files |= set(infos)
        resources = ROOT / 'analysis/factorization_machine_annual_resource_observer_20261005'
        observed = sync.read(resources / 'resource_summary.json')
        assert observed['status'] == 'completed_owned_process_observation'
        assert sha(resources / 'actual_resource_samples.jsonl') == observed['resource_evidence']['sample_file_sha256']
        files |= {resources / 'resource_summary.json', resources / 'actual_resource_samples.jsonl'}
    else:
        qa = ROOT / 'analysis/factorization_machine_future_qa_v2_20261005'
        audit = sync.read(qa / 'verification.json')
        assert audit['status'] == 'passed' and audit['actual_fulltraining_fits'] == 6
        assert audit['all6_models_fullfuture_reload_and_cold80_controls_passed']
        resource = sync.read(qa / 'resource_summary.json')
        assert resource['status'] == 'passed'
        assert sha(qa / 'actual_resource_samples.jsonl') == resource['actual_resources']['sample_file_sha256']
        for row in audit['checks']:
            name = row['model']
            source = bank / name / 'info_2025.json'
            info = sync.read(source)
            assert info['status'] == 'passed' and info['new_model_fits'] == 1
            assert info['completed_training_epochs']==32 and info['training_meta'] == row['mature_training']
            assert sha(source.parent / 'model_2025.joblib') == sha(qa / f'{name}.joblib') == info['model_sha256'] == row['model_sha256']
            assert sha(qa / f'{name}_raw.parquet') == row['raw_sha256']
            assert row['actual_full1599600_row_reload_bit_identical'] and row['actual_cold80_day_prefix_bit_identical']
            checks.append({'model': name, 'info_sha256': sha(source),
                'model_sha256': row['model_sha256'], 'raw_sha256': row['raw_sha256']})
            files.add(source)
        assert len(checks) == 6
        files |= {p for p in qa.glob('*') if p.suffix in ('.json', '.jsonl')}
    prefix = Path(f'validation_sync/factorization_machine_completed_{stage}_20261005')
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    assert str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent = observer.parent()
    assert parent is not None and parent.cmdline()[1:] == observer.cmdline()[1:]
    suspended = []
    try:
        for process in (observer, parent):
            process.suspend()
            suspended.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True)), 'Main publisher currently busy.'
        paths, bindings = [], {}
        existing = sync.WORKTREE / prefix / 'manifest.json'
        if not existing.exists():
            assert not sync.git('status', '--porcelain')
            head = sync.git('rev-parse', 'HEAD')
            assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
            sync.atomic(sync.WORKTREE / prefix / '.gitattributes', b'* -text\n')
            paths.append((prefix / '.gitattributes').as_posix())
            for source in sorted(files):
                relative = source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('authorized_E_bank') / source.relative_to(bank)
                destination = relative if source == Path(__file__) else prefix / relative
                data = source.read_bytes()
                assert not sync.SECRET.search(data)
                original_sha = hashlib.sha256(data).hexdigest()
                if len(data) >= 5 * 1024**2:
                    assert source.suffix == '.jsonl'
                    destination = Path(destination.as_posix() + '.gz')
                    data = gzip.compress(data, compresslevel=6, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == original_sha
                assert len(data) < 90 * 1024**2
                sync.atomic(sync.WORKTREE / destination, data)
                paths.append(destination.as_posix())
                bindings[str(source)] = {'original_sha256': original_sha,
                    'published_sha256': hashlib.sha256(data).hexdigest(), 'published_path': destination.as_posix()}
            manifest = {'status': 'passed_actual_closed_native_training_or_fullfuture_scope',
                'at_local': sync.now(), 'stage': stage, 'source_files': bindings, 'checks': checks,
                'actual_annual_fits': 30 if stage == 'annual' else None,
                'actual_mature_final_fits':6 if stage=='future' else None,'epochs_each_complete_fit':32,'training_device':'cpu',
                'whole_scheme_official_rounds73_74_remain_separate_required_work': True,
                'native_models_and_raw_predictions_retained_local_D_or_E': True,
                'only_publication_branch': 'main', 'new_quality_scores': 0, 'test_labels_read': False}
            sync.atomic(existing, sync.encoded(manifest))
            paths.append((prefix / 'manifest.json').as_posix())
            for source, value in bindings.items():
                assert sha(source) == value['original_sha256'], source
            for offset in range(0, len(paths), 50):
                sync.git('add', '--', *paths[offset:offset + 50])
            changed = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
            assert changed and changed <= set(paths)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                '核验因子分解机全部30个完整年度模型' if stage == 'annual' else '核验因子分解机6个成熟最终模型和全部未来预测', timeout=180)
        else:
            manifest = sync.read(existing)
            assert manifest['stage'] == stage
            assert not sync.git('status', '--porcelain'), 'Existing native commit needs review before retry.'
            for source, value in manifest['source_files'].items():
                assert sha(source) == value['original_sha256'], source
        commit = sync.git('rev-parse', 'HEAD')
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        result = {'status': 'pushed_verified_only_main', 'at_local': sync.now(), 'stage': stage,
            'commit': commit, 'actual_verified_model_count': len(checks), 'new_quality_scores': 0,
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{prefix.as_posix()}'}
        sync.atomic(receipt_path, sync.encoded(result))
        return result
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


def main():
    run_path = ROOT / 'analysis/factorization_machine_native_github_run_v2_20261005.json'
    deadline = time.monotonic() + 60
    while not run_path.exists():
        assert time.monotonic() < deadline
        time.sleep(.1)
    run = sync.read(run_path)
    for source, value in run['input_sha256'].items():
        assert sha(source) == value, source
    bank = Path(sync.read(ROOT / 'analysis/factorization_machine_storage_20261005.json')['output_directory'])
    while True:
        state = {'at_local': sync.now(), 'status': 'waiting_for_actual_closed_native_scopes',
                 'only_branch': 'main', 'pid': psutil.Process().pid}
        try:
            for stage, ready in (
                ('annual', (bank / 'oof_audit.json').exists() and (bank / 'training_execution_scope.json').exists()
                           and (ROOT / 'analysis/factorization_machine_annual_resource_observer_20261005/resource_summary.json').exists()),
                ('future', (ROOT / 'analysis/factorization_machine_future_qa_v2_20261005/verification.json').exists())):
                if ready:
                    state[stage] = publish(stage)
            if all((sync.OUT / f'factorization_machine_completed_{stage}_receipt.json').exists() for stage in ('annual', 'future')):
                state['status'] = 'completed_native_evidence_publication'
        except Exception as error:
            state.update(status='native_publication_retry_pending', error=f'{type(error).__name__}: {error}')
        sync.atomic(ROOT / 'analysis/factorization_machine_native_github_state_v2_20261005.json', sync.encoded(state))
        if state['status'] == 'completed_native_evidence_publication':
            print(json.dumps(state, ensure_ascii=False), flush=True)
            return
        time.sleep(15)


if __name__ == '__main__':
    main()
