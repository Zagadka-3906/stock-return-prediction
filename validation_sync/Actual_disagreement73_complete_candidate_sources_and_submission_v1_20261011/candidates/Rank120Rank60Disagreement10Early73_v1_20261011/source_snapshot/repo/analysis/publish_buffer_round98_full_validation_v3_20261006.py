"""Publish the complete immutable round98 board, every original score, and QA."""
from pathlib import Path
import hashlib
import gzip
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    # The caller holds only the exactly owned idle main publisher. Scientific
    # children continue running, and every publication uses main exclusively.
    import collect_full_lossless_round_publication_20261006 as collector
    collector_source = Path(collector.__file__)
    collector_text = collector_source.read_text(encoding='utf-8')
    before = "publication = read(display / 'runtime_publication.json')"
    assert collector_text.count(before) == 1
    collector_text = collector_text.replace(before, "publication = read(display / 'runtime_publication_completeness_v2_20261006.json')")
    before = "'complete_rankings_lossless.html', 'runtime_publication.json',"
    assert collector_text.count(before) == 1
    collector_text = collector_text.replace(before, "'complete_rankings_lossless.html', 'runtime_publication_completeness_v2_20261006.json',")
    collector_namespace = dict(collector.__dict__)
    exec(compile(collector_text, str(collector_source), 'exec'), collector_namespace)
    collect = collector_namespace['collect']
    sync = helpers.sync
    full_payload, full = collect(98, 9, 16)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        "copy(candidate / 'manifest.json', relative / 'candidate_manifest.json')": "copy(COMPLETE_CANDIDATE_MANIFEST, relative / 'candidate_manifest.json')",
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v9_20261006/round98/qa/interaction_result.json'",
        'assert sha(board_path.read_bytes()) == board_sha':
            'assert sha(gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())) == board_sha'}
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    namespace = dict(sync.__dict__, __name__='actual_buffer98_complete_immutable_publication')
    exec(compile(text, str(source), 'exec'), namespace)
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round98/full_report_reconstructed_for_publication.json.gz'
    namespace['COMPLETE_CANDIDATE_MANIFEST'] = A / 'optimization_20261003_r98/candidate_complete_manifest_20261006.json'
    manifest, payload = namespace['snapshot'](98)
    assert manifest['scored_records'] == full['scored_records'] == 16
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round98')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    extra = [
        *list((A / 'causal_entry_exit_buffer_release_20261006').glob('*.json')),
        *list((A / 'causal_entry_exit_buffer_official_pilot_20261006').glob('case*_official.json')),
        A / 'causal_entry_exit_buffer_official_pilot_20261006/frozen_before_actual_official_scores.json',
        A / 'causal_entry_exit_buffer_official_pilot_20261006/verification.json',
        A / 'buffer_round98_ranking_source_preparation_20261006.json',
        A / 'causal_entry_exit_buffer_source_freeze_20261006/manifest.json',
        ROOT / 'candidates/optimization_20261003_r98/registry_alias_verification.json',
        ROOT / 'candidates/causal_entry_exit_buffer_20261006/manifest.json']
    extra += list((A / 'causal_entry_exit_buffer_official_pilot_20261006/identical_official_scores').glob('*.json'))
    extra += list((A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_round98_full_registration').glob('*.json'))
    extra += [A / 'optimization_20261003_r98/full_registration_failure.json', A / 'github_validation_sync_main_20261005/round98_receipt.json', Path(__file__),
        A / 'optimization_20261003_r98/candidate_complete_manifest_20261006.json',
        A / 'optimization_20261003_r98/publication_recovery_execution_v2_20261006.json',
        A / 'optimization_20261003_r98/frozen_before_full_publication_recovery_20261006.json',
        A / 'optimization_20261003_r98/actual_idle_publisher_full_recovery_20261006.json',
        A / 'optimization_20261003_r98/actual_hidden_full_publication_recovery_children_20261006.json',
        ROOT / 'candidates/optimization_20261003_r98/manifest.json',
        A / 'lossless_ranking_display_qa_v8_20261006/round98/verification.json',
        *(A / 'service_owned_workflows_20261006/buffer_round98_full_publication_recovery').glob('*.json')]
    for path in extra:
        data = path.read_bytes()
        assert not sync.SECRET.search(data), path
        raw_sha = hashlib.sha256(data).hexdigest()
        raw_bytes = len(data)
        target = (prefix / 'original_execution_evidence' / path.relative_to(ROOT)).as_posix()
        if len(data) >= 5 * 1024**2:
            data = gzip.compress(data, compresslevel=6, mtime=0)
            assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
            target += '.gz'
        assert len(data) < 5 * 1024**2, path
        payload[target] = data
        manifest['local_input_source_sha256'][path.relative_to(ROOT).as_posix()] = raw_sha
        manifest['exported_files'][target] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'original_bytes': raw_bytes, 'original_sha256': raw_sha, 'lossless_original_bytes_preserved': True}
    attributes = (prefix / '.gitattributes').as_posix()
    payload[attributes] = b'* -text\n'
    manifest['exported_files'][attributes] = {'bytes': 8, 'sha256': hashlib.sha256(payload[attributes]).hexdigest()}
    manifest.update(immutable_all_values_lossless_display_and_complete_original_QA_published=True,
        actual_complete_QA_version=9, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate='candidates/causal_entry_exit_buffer_20261006',
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix / 'README.md').as_posix()] += (
        '\n本轮是既有16项官方评分的正式登记：评分和方案冻结时间沿用原记录，'
        '全部1599600行预测、实际模型/独立编解码器及80日前缀复核在原命名候选目录实际完成，'
        '第98轮目录使用经SHA核验的相同文件硬链接，并不声称为新增推理。'
        '完整榜、全部原始六视图检查及封存来源已实际重建和验证。\n').encode('utf-8')
    previous = sync.git('rev-parse', 'HEAD')
    helpers.verify_main(previous)
    assert not sync.git('status', '--porcelain')
    for target, data in payload.items():
        sync.atomic(sync.WORKTREE / target, data)
    filenames = sorted(payload)
    for offset in range(0, len(filenames), 50):
        sync.git('add', '-f', '--', *filenames[offset:offset+50])
    staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
    assert staged and staged <= set(payload)
    sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
        '登记第98轮16项实际后处理验证并发布完整榜与全量QA', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round98_complete_inventory_receipt_20261006.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 98, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 16,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 9, 'original_official_pilot_records_registered': 16,
        'new_quality_scores_by_registration': 0, 'initial_publication_failure_preserved': True,
        'full_immutable_ranking_and_all_original_QA_preserved': True,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round98'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
