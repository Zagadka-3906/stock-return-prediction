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
    from collect_full_lossless_round134_qa45_20261007 import collect
    sync = helpers.sync
    full_payload, full = collect(134, 45, 40)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v45_20261007/round134/qa/interaction_result.json'",
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
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round134/full_report_reconstructed_for_publication.json.gz'
    manifest, payload = namespace['snapshot'](134)
    assert manifest['scored_records'] == full['scored_records'] == 40
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round134')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    ready = read(A / 'nonflag_ReverseBayesFine40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json')
    extra = [Path(__file__), A / 'nonflag_ReverseBayesFine40_round134_source_preparation_v1_20261007.json',
        A / 'prepare_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py',
        A / 'run_nonflag_ReverseBayesFine40_round134_full_registration_v1_20261007.py',
        A / 'nonflag_ReverseBayesFine40_round134_source_admission_v1_20261007.json',
        A / 'prepare_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py',
        A / 'seal_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py',
        A / 'predict_nonflag_residual_ReverseBayesFine_complete_scheme_20261007.py',
        A / 'nonflag_residual_ReverseBayesFine_compatible_parent_20261007.py',
        A / 'nonflag_ReverseBayesFine40_plan_20261007.json',
        A / 'nonflag_residual_ReverseBayesFine37_transform_preflight_20261007/verification.json',
        A / 'nonflag_ReverseBayesFine40_round134_source_admission_v1_20261007.json',
        A / 'local_118_119_publication_contract_v5_actual_hidden_launches_20261007.json',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py', A / 'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',
        A / 'quantile_HGB_bank20_github_v5_20261007/receipt.json',
        A / 'nonflag_ReverseBayesFine40_scores_github_v1_20261007/receipt.json',
        ROOT / 'candidates/optimization_20261003_r134/registry_alias_verification.json',
        Path(ready['source_candidate']) / 'manifest.json']
    for folder in (A / 'nonflag_ReverseBayesFine40_selected_release_v1_20261007', Path(ready['source_release']),
        A / 'nonflag_ReverseBayesFine40_official_comparison_v1_20261007',
        A / 'nonflag_residual_ReverseBayesFine37_transform_preflight_20261007'):
        extra += list(folder.glob('*.json'))
    extra += [p for p in (A / 'nonflag_residual_EmpiricalBayes64_bank10_20261007').rglob('*.json') if not p.name.startswith('independent_linear_state_')]
    for name in ('cpu_conditional_residual_hgb_native_bank20', 'nonflag_ReverseBayesFine40_official_comparison_v1',
        'cpu_conditional_residual_hgb20_bank_evidence_publication', 'nonflag_ReverseBayesFine40_scores_main_publication_v1',
        'nonflag_ReverseBayesFine40_selected_candidate_preparation_v1', 'nonflag_ReverseBayesFine40_selected_candidate_sealing_v1'):
        service = A / 'service_owned_workflows_20261006' / name
        extra += list(service.glob('*.json')) + list(service.glob('*.log'))
    extra += [A / 'nonflag_ReverseBayesFine40_actual_source_paths_before_registration_20261007.json', A / 'weighted_HGB340_actual_source_paths_before_registration_20261007.json']
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
        actual_complete_QA_version=45, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate=ready['source_candidate'],
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix / 'README.md').as_posix()] += (
        '\n本轮40项完整官方比较：112、132、133合格锚点，两组反向贝叶斯残差及等权集成各12幅度，以及消融。'
        '实际10年度成熟模型，教师106；替换已有非涨停HGB，保留完整涨停分支和2020输出。'
        '37项5635800行CDF与111冷前缀核对；官方八指标选优后冻结，选中新方案执行原生重载、独立线性解码、两次完整重放及冷80。'
        '完整榜六视图和45秒QA45保留，全部源码参数核对。仅main，未读取真实测试标签。有限网格不证明优化穷尽。\n').encode('utf8')
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
        '登记第134轮40项反向贝叶斯残差幅度加密完整验证并发布完整榜与QA45', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round134_receipt.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 134, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 40,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 45, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_official_pilot_records_registered': 40,
        'new_quality_scores_by_registration': 0,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round134'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
