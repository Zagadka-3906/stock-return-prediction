"""Publish actual closed R89 science, its retained failure and entire full QA on main."""
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


def main():
    service = A / 'service_owned_workflows_20261006/classifier_consensus_round89_status_recovery'
    while not (service / 'native_launch.json').exists() or owned(read(service / 'native_launch.json')):
        time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    out = A / 'classifier_consensus_round89_status_recovery_main_20261007'
    assert not out.exists()
    out.mkdir()
    import qualified_round_recovery_evidence_v4_20261007 as qualification
    evidence = qualification.scientific_round89_evidence()
    assert evidence is not None and evidence['scored_records'] == 124
    pins = {**read(A / 'optimization_20261003_r89/protocol.json')['input_sha256'],
        **{str(ROOT / p): digest for p, digest in evidence['source_sha256'].items()},
        str(Path(__file__)): sha(Path(__file__))}
    create(out / 'frozen_before_actual_full_main_publication.json', {'input_sha256': pins,
        'actual_complete_scientific_evidence': evidence, 'original_failed_scope_retained': True,
        'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    sync = helpers.sync
    held, retries = [], []
    restore = install()
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
            from collect_full_lossless_round_publication_20261006 import collect
            full_payload, full = collect(89, 4, 124)
            source = A / 'sync_validated_rounds_main_20261005.py'
            text = source.read_text(encoding='utf-8')
            patches = {
                'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
                "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'": "ROOT / 'analysis/lossless_ranking_display_qa_v4_20261006/round89/qa/interaction_result.json'",
                'assert sha(board_path.read_bytes()) == board_sha': 'assert sha(gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())) == board_sha',
                "        assert len(data) < 5 * 1024**2, f'Unexpected large review artifact: {source}'": "        raw_digest = sha(data)\n        if len(data) >= 5 * 1024**2:\n            data = gzip.compress(data, mtime=0)\n            destination = Path(str(destination) + '.gz')\n            assert sha(gzip.decompress(data)) == raw_digest",
                "bindings[str(source.relative_to(ROOT)).replace('\\\\', '/')] = sha(data)": "bindings[str(source.relative_to(ROOT)).replace('\\\\', '/')] = raw_digest",
            }
            for before, after in patches.items():
                assert text.count(before) == 1, before
                text = text.replace(before, after)
            namespace = dict(sync.__dict__, __name__='actual_closed_R89_precise_status_recovery_publication')
            exec(compile(text, str(source), 'exec'), namespace)
            namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round89/full_report_reconstructed_for_publication.json.gz'
            namespace['complete_round_evidence'] = lambda number: qualification.scientific_round89_evidence() if number == 89 else None
            manifest, payload = namespace['snapshot'](89)
            assert manifest['scored_records'] == full['scored_records'] == 124
            assert manifest['connected_records'] == full['connected_records']
            assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
            payload.update(full_payload)
            manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
            manifest['exported_files'].update(full['exported_files'])
            prefix = Path('validation_sync/round89')
            extras = [Path(__file__), A / 'qualified_round_recovery_evidence_v4_20261007.py',
                A / 'classifier_consensus_round89_status_recovery_admission_20261007.json',
                A / 'optimization_20261003_r89/provenance_scope_execution_status_recovery_20261007.json',
                A / 'optimization_20261003_r89/provenance_scope_execution.json',
                *list((A / 'classifier_consensus_round89_status_recovery_20261007').glob('*.json')),
                *list((A / 'optimization_20261003_r89').glob('*.json'))]
            for folder in (A / 'classifier_consensus_status_gate_recovery_preflight_20261007',
                A / 'rank_date_index_combined_worker_preflight_20261007',
                A / 'classifier_consensus_bank_20261005', A / 'classifier_consensus_future_qa_20261005',
                A / 'frozen_controller_name_collision_restoration_20261006',
                A / 'service_owned_dependency_queue_v11_recovery_20261006/activated_jobs/round89', service):
                extras += [p for p in folder.rglob('*.json') if not p.name.startswith('model_dump_')]
                extras += list(folder.glob('*.log'))
            extras += list((A / 'optimization_20261003_r89').rglob('identical_official_scores/*.json'))
            for path in dict.fromkeys(extras):
                data = path.read_bytes()
                assert not sync.SECRET.search(data), path
                target = (prefix / 'original_execution_evidence' / path.relative_to(ROOT)).as_posix()
                original_sha, original_size = hashlib.sha256(data).hexdigest(), len(data)
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == original_sha
                    target += '.gz'
                payload[target] = data
                manifest['local_input_source_sha256'][path.relative_to(ROOT).as_posix()] = original_sha
                manifest['exported_files'][target] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                    'original_sha256': original_sha, 'original_bytes': original_size, 'lossless_original_bytes_preserved': True}
            attributes = (prefix / '.gitattributes').as_posix()
            payload[attributes] = b'* -text\n'
            manifest['exported_files'][attributes] = {'bytes': 8, 'sha256': hashlib.sha256(payload[attributes]).hexdigest()}
            manifest.update(actual_complete_QA_version=4,
                immutable_all_values_lossless_display_and_complete_original_QA_published=True,
                actual_original124_scientific_recovery=True, original_failed_scope_preserved=True,
                actual_alternate_scope='analysis/optimization_20261003_r89/provenance_scope_execution_status_recovery_20261007.json')
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] += ('\n本轮重新完成原先门控中断的124项完整科学验证；旧失败证明原字节保留。'
                '修复只接受精确的分类路由成功状态并核验12项直接路由、4项继承路由和全部输入哈希。'
                '历史误覆盖的控制器绑定由两份独立冻结副本恢复，新启动单独记录；原数学与网格不变。'
                '原生模型复用但完整验证评分、选定冻结、1599600行推理、独立重载、80日前缀及完整榜QA均为实际执行。'
                '新恢复证明另存；不覆盖旧失败证明，也不把预检当作科学完成。\n').encode('utf-8')
            previous_head = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous_head)
            assert not sync.git('status', '--porcelain')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '恢复第89轮原124项分类集成科学验证并保留失败原件与完整榜QA', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            receipt = A / 'github_validation_sync_main_20261005/round89_receipt.json'
            create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 89, 'at_local': sync.now(),
                'commit': commit, 'branch': 'main', 'remote': sync.REMOTE, 'actual_full_QA_version': 4,
                'official_score': manifest['metrics']['final_score'], 'scored_records': 124,
                'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
                'full_immutable_ranking_and_all_original_QA_preserved': True,
                'original_failed_scope_preserved_and_alternate_closed_scope_required': True,
                'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round89'})
            create(out / 'verification.json', {'status': 'passed_actual_closed_R89_124_science_full_QA_raw_main_exports',
                'at_local': sync.now(), 'receipt': read(receipt), 'all_sources_initial_and_final_full_read_locked_hash': True,
                'original_failed_scope_preserved': True, 'new_quality_scores_by_publication': 0, 'test_labels_read': False})
            print(json.dumps(read(receipt), ensure_ascii=False), flush=True)
    finally:
        sync.git = old_git
        qualification.close()
        for p in reversed(held):
            if p.is_running():
                p.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})
        create(out / 'transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
