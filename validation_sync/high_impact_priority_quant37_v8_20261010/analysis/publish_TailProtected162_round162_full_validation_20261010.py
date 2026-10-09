"""Publish the complete immutable round116 board, every original score, and QA."""
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
    from collect_full_lossless_round162_qa73_20261010 import collect
    sync = helpers.sync
    full_payload, full = collect(162, 73, 76)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v73_20261010/round162/qa/interaction_result.json'",
        'assert sha(board_path.read_bytes()) == board_sha':
            'assert sha(gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())) == board_sha'}
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    old_guard = "        assert len(data) < 5 * 1024**2, f'Unexpected large review artifact: {source}'"
    assert text.count(old_guard) == 1
    text = text.replace(old_guard, "        raw_digest = sha(data)\n        if len(data) >= 5 * 1024**2:\n            data = gzip.compress(data, mtime=0)\n            destination = Path(str(destination) + '.gz')\n            assert sha(gzip.decompress(data)) == raw_digest")
    old_binding = "bindings[str(source.relative_to(ROOT)).replace('\\\\', '/')] = sha(data)"
    assert text.count(old_binding) == 1
    text = text.replace(old_binding, old_binding.replace('sha(data)', 'raw_digest'))
    namespace = dict(sync.__dict__, __name__='actual_simplex_residual106_complete_immutable_publication')
    exec(compile(text, str(source), 'exec'), namespace)
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round162/full_report_reconstructed_for_publication.json.gz'
    manifest, payload = namespace['snapshot'](162)
    assert manifest['scored_records'] == full['scored_records'] == 76
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round162')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    ready = read(A / 'TailProtected162_selected_release_v1_20261010/selected_candidate_ready_for_registration.json')
    from prepare_protected162_full_registry_sources_v1_20261010 import source_paths
    extra=source_paths()+[ROOT/'candidates/optimization_20261003_r162/registry_alias_verification.json',Path(ready['source_candidate'])/'manifest.json']
    for folder in (A/'TailProtected162_selected_release_v1_20261010',Path(ready['source_release']),Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010')):
        extra += list(folder.glob('*.json'))
    for name in ('TailProtected162_selected_native14_v1_20261010','TailProtected162_selected_candidate_preparation_v1_20261010','TailProtected162_selected_candidate_sealing_v1_20261010'):
        folder=A/'service_owned_workflows_20261006'/name
        extra+=list(folder.glob('*.json'))+list(folder.glob('*.log'))
    for family in ('protected_upper_tail_screen_v1_20261010','protected_official_top_screen_v2_20261010'):
        folder=Path('E:/赛题五_本机临时')/family
        extra+=list(folder.glob('*.json'))
        for row in read(folder/'verification.json')['records']:extra.append(Path(row['official_score_cache']['official_metrics_source']))
    for path in extra:
        data = path.read_bytes()
        assert not sync.SECRET.search(data), path
        target = (prefix / 'original_execution_evidence' / (path.relative_to(ROOT) if path.is_relative_to(ROOT) else Path('external_metadata')/(sha(path)+'_'+path.name))).as_posix()
        raw_sha, raw_size = hashlib.sha256(data).hexdigest(), len(data)
        if len(data) >= 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
            target += '.gz'
        payload[target] = data
        manifest['local_input_source_sha256'][(path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path))] = raw_sha
        manifest['exported_files'][target] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'original_sha256': raw_sha, 'original_bytes': raw_size, 'lossless_original_bytes_preserved': True}
    attributes = (prefix / '.gitattributes').as_posix()
    payload[attributes] = b'* -text\n'
    manifest['exported_files'][attributes] = {'bytes': 8, 'sha256': hashlib.sha256(payload[attributes]).hexdigest()}
    manifest.update(immutable_all_values_lossless_display_and_complete_original_QA_published=True,
        actual_complete_QA_version=73, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate=ready['source_candidate'],
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix/'README.md').as_posix()] += ('\n第162轮：完整157之后两类保护头部的排序置换方案；74项已实际训练内评分及两个合格锚点，共76项。仅选中方案执行完整候选推理。保留原始37+37冻结计划、逐项官方分数和36+36完整、108+108截断控制，以及选中方案原生14、冷14和7项成熟截止拒绝控制。完整榜原六视图QA73与main；不读取测试标签，不声称穷尽。\n').encode('utf8')
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
        '登记第162轮76项保护头部排序方案与完整榜QA73', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round162_receipt.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 162, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 76,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 73, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_official_pilot_records_registered': 76,
        'new_quality_scores_by_registration': 0,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round162'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
