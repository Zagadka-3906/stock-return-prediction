"""Publish the complete immutable round115 board, every original score, and QA."""
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
    from collect_full_lossless_round115_qa26_20261007 import collect
    sync = helpers.sync
    full_payload, full = collect(115, 26, 66)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v26_20261007/round115/qa/interaction_result.json'",
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
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round115/full_report_reconstructed_for_publication.json.gz'
    manifest, payload = namespace['snapshot'](115)
    assert manifest['scored_records'] == full['scored_records'] == 66
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round115')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    ready = read(A / 'protected_upper_pool_HGB66_selected_release_20261007/selected_candidate_ready_for_registration.json')
    extra = [Path(__file__), A / 'protected_upper_pool_HGB66_round115_source_preparation_20261007.json',
        A / 'prepare_protected_upper_pool_HGB66_round115_sources_20261007.py',
        A / 'run_protected_upper_pool_HGB66_round115_full_registration_20261007.py',
        A / 'protected_upper_pool_HGB66_candidate_source_admission_20261007.json',
        A / 'prepare_protected_upper_pool_HGB66_selected_candidate_20261007.py',
        A / 'seal_protected_upper_pool_HGB66_selected_candidate_20261007.py',
        A / 'predict_protected_upper_pool_CPU_HGB_scheme_20261007.py',
        A / 'protected_upper_pool_HGB_CDF_transform_20261007.py',
        A / 'protected_upper_pool_HGB_CDF_plan_20261007.json',
        A / 'protected_upper_pool_HGB_CDF_preflight_20261007/verification.json',
        A / 'protected_upper_pool_HGB66_scoring_admission_20261007.json',
        A / 'protected_upper_pool_HGB66_candidate_actual_launch_20261007.json',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py', A / 'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',
        A / 'cpu_full_universe_HGB24_bank_recovery_v2_github_20261007/receipt.json',
        A / 'protected_upper_pool_HGB66_scores_v2_github_20261007/receipt.json',
        ROOT / 'candidates/optimization_20261003_r115/registry_alias_verification.json',
        Path(ready['source_candidate']) / 'manifest.json']
    for folder in (A / 'protected_upper_pool_HGB66_selected_release_20261007', Path(ready['source_release']),
        A / 'protected_upper_pool_HGB66_official_comparison_v2_20261007',
        A / 'protected_upper_pool_HGB_selected_hook_preflight_20261007'):
        extra += list(folder.glob('*.json'))
    extra += [p for p in (A / 'cpu_full_universe_HGB_bank24_recovery_v2_20261007').rglob('*.json') if not p.name.startswith('independent_hist_tree_state_')]
    for name in ('cpu_full_universe_HGB_native_bank24_v2', 'protected_upper_pool_HGB66_official_comparison_v2',
        'cpu_full_universe_HGB24_bank_evidence_publication_v2', 'protected_upper_pool_HGB66_scores_main_publication_v3',
        'protected_upper_pool_HGB66_selected_candidate_preparation', 'protected_upper_pool_HGB66_selected_candidate_sealing'):
        service = A / 'service_owned_workflows_20261006' / name
        extra += list(service.glob('*.json')) + list(service.glob('*.log'))
    for path in extra:
        data = path.read_bytes()
        assert not sync.SECRET.search(data), path
        target = (prefix / 'original_execution_evidence' / path.relative_to(ROOT)).as_posix()
        raw_sha, raw_size = hashlib.sha256(data).hexdigest(), len(data)
        if len(data) >= 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
            target += '.gz'
        payload[target] = data
        manifest['local_input_source_sha256'][path.relative_to(ROOT).as_posix()] = raw_sha
        manifest['exported_files'][target] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'original_sha256': raw_sha, 'original_bytes': raw_size, 'lossless_original_bytes_preserved': True}
    attributes = (prefix / '.gitattributes').as_posix()
    payload[attributes] = b'* -text\n'
    manifest['exported_files'][attributes] = {'bytes': 8, 'sha256': hashlib.sha256(payload[attributes]).hexdigest()}
    manifest.update(immutable_all_values_lossless_display_and_complete_original_QA_published=True,
        actual_complete_QA_version=26, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate=ready['source_candidate'],
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix / 'README.md').as_posix()] += (
        '\n本轮登记66项原始完整官方评分：112至114三个合格锚点和63项低分区HGB排序/CDF方案。'
        '父方案在本轮评分前按三者完整官方总分确定，完全同分取最早者。'
        '只在当前非涨停、价格有效、预测可用股票的严格低分子池重排，整个边界并列组保留。'
        '只按完整官方总分选择，不设Top、最差年份或显著性淘汰条件。'
        '已有24个完整HGB模型复用；若产生新方案，实际冻结后完成完整1599600行、原生模型/独立解码、两次重放、CSV及冷80日检查。'
        '若选中已有锚点，则逐位预测、全部8项指标、完整方案和封存字节核对后复用，0新推理。'
        '具体路径和原冻结时间见selected_candidate_ready_for_registration.json。'
        '完整榜六视图与45秒浏览器检查均保留，只main，未读真实测试标签。\n').encode('utf-8')
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
        '登记第115轮66项低分区CPU HGB排序与CDF融合验证并发布完整榜与全量QA', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round115_receipt.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 115, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 66,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 26, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_official_pilot_records_registered': 66,
        'new_quality_scores_by_registration': 0,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round115'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
