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
    from collect_full_lossless_round206_qa117_v1_20261011 import collect
    sync = helpers.sync
    full_payload, full = collect(206, 117, 35)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v117_20261010/round206/qa/interaction_result.json'",
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
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round206/full_report_reconstructed_for_publication.json.gz'
    manifest, payload = namespace['snapshot'](206)
    assert manifest['scored_records'] == full['scored_records'] == 35
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round206')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    ready = read(A / 'StockRank60Window504DirectEmbedding206_selected_release_v1_20261011/selected_candidate_ready_for_registration.json')
    from prepare_StockRank60Window504Direct206_complete35_pipeline_v1_20261011 import source_paths
    extra=source_paths()+[ROOT/'candidates/optimization_20261003_r206/registry_alias_verification.json',Path(ready['source_candidate'])/'manifest.json']
    for folder in (A/'StockRank60Window504DirectEmbedding206_selected_release_v1_20261011',Path(ready['source_release']),Path('E:/赛题五_本机临时/stock_rank60window504_direct_embedding35_selected_native14_v1_20261011')):
        extra += list(folder.glob('*.json'))
    for name in ('Frontier133_selected_native_stage_v2_20261010','StockRank60Window504DirectEmbedding206_selected_candidate_preparation_v1_20261011','StockRank60Window504DirectEmbedding206_selected_candidate_sealing_v1_20261011'):
        folder=A/'service_owned_workflows_20261006'/name
        extra+=list(folder.glob('*.json'))+list(folder.glob('*.log'))
    for family in read(A/'stock_rank60window504_direct_embedding_complete35_after205_selection_plan_v1_20261011.json')['families']:
        choices=[Path(family['output'])] if family.get('output') else [Path('E:/赛题五_本机临时')/(family['name']+'_screen_v1_'+date) for date in ('20261010','20261011')]
        existing=[p for p in choices if (p/'verification.json').is_file()]
        assert len(existing)==1,(family,choices)
        folder=existing[0];assert family.get('records',len(read(folder/'verification.json')['records']))==len(read(folder/'verification.json')['records'])
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
        actual_complete_QA_version=117, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate=ready['source_candidate'],
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix/'README.md').as_posix()] += ('\n第206轮：股票身份嵌入与二十日平均收益的截面排名Huber目标，六年度近期252日且标签严格完整成熟的样本独立64轮训练；17项小权重及保护融合、29项大权重及全有效股票融合，与完整175及205两个锚点共35条TRAIN官方记录统一选择。44项全量Pandas控制、132个因果前缀；最高官方S优先和物理模型SHA去重。胜出新方案六状态14原生、14冷启动、7拟合前拒绝检查，冻结后两次1599600行完整独立推理及cold80；锚点如实复用。完整榜18372条、六视图QA117及GitHub main；未使用测试标签。\n').encode('utf8')

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
        '登记第206轮133项保护头部排序方案与完整榜QA117', timeout=206)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=206)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round206_receipt.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 206, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 35,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 117, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_official_pilot_records_registered': 35,
        'new_quality_scores_by_registration': 0,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round206'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
