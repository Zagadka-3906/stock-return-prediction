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
    from collect_full_lossless_round117_qa28_20261007 import collect
    sync = helpers.sync
    full_payload, full = collect(117, 28, 340)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v28_20261007/round117/qa/interaction_result.json'",
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
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round117/full_report_reconstructed_for_publication.json.gz'
    manifest, payload = namespace['snapshot'](117)
    assert manifest['scored_records'] == full['scored_records'] == 340
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round117')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    ready = read(A / 'flagged_HGB_weighted_quarters340_selected_release_v4_20261007/selected_candidate_ready_for_registration.json')
    extra = [Path(__file__), A / 'weighted_HGB340_round117_source_preparation_v2_20261007.json',
        A / 'prepare_weighted_HGB340_round117_sources_v2_20261007.py',
        A / 'run_weighted_HGB340_round117_full_registration_v2_20261007.py',
        A / 'weighted_HGB340_round117_source_admission_v2_20261007.json',
        A / 'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007.py',
        A / 'seal_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007.py',
        A / 'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
        A / 'refine_flagged_HGB_compatible_parent_transform_20261007.py',
        A / 'flagged_HGB_weighted_quarters340_plan_20261007.json',
        A / 'flagged_HGB_weighted_quarters340_transform_preflight_20261007/verification.json',
        A / 'weighted_HGB340_round117_source_admission_v2_20261007.json',
        A / 'weighted_HGB340_complete_pipeline_actual_hidden_launches_20261007.json',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py', A / 'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',
        A / 'weighted_HGB_and_percentile_controls_github_20261007/receipt.json',
        A / 'flagged_HGB_weighted_quarters340_scores_github_20261007/receipt.json',
        ROOT / 'candidates/optimization_20261003_r117/registry_alias_verification.json',
        Path(ready['source_candidate']) / 'manifest.json']
    for folder in (A / 'flagged_HGB_weighted_quarters340_selected_release_v4_20261007', Path(ready['source_release']),
        A / 'flagged_HGB_weighted_quarters340_official_comparison_20261007',
        A / 'flagged_HGB_weighted_quarters340_transform_preflight_20261007'):
        extra += list(folder.glob('*.json'))
    extra += [p for p in (A / 'cpu_conditional_residual_hgb_bank20_20261007').rglob('*.json') if not p.name.startswith('independent_hist_tree_state_')]
    for name in ('cpu_conditional_residual_hgb_native_bank20', 'flagged_HGB_weighted_quarters340_official_comparison',
        'cpu_conditional_residual_hgb20_bank_evidence_publication', 'flagged_HGB_weighted_quarters340_scores_main_publication',
        'flagged_HGB_weighted_quarters340_selected_candidate_preparation_v4', 'flagged_HGB_weighted_quarters340_selected_candidate_sealing_v4'):
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
        actual_complete_QA_version=28, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate=ready['source_candidate'],
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix / 'README.md').as_posix()] += (
        '\n本轮登记340项完整官方比较：112、115、116三个合格锚点、28种预定非等权四份集成乘12权重，以及移除涨停HGB的消融。'
        '每个集成保留四个有序加法槽，原生模型只保存与推理2至3个唯一组件。'
        '复用20个既有年度模型，特征教师为106；全部5635800行与1011冷前缀控制不读取测试答案。'
        '以完整官方总分选优，冻结后推理；已有合格锚点按逐位输出、8指标、完整图和全部封存字节核对后复用。'
        '完整榜六视图、45秒浏览器QA28和全部源码参数审计保留；仅main。有限网格通过不等于优化穷尽。\n').encode('utf-8')
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
        '登记第117轮340项涨停HGB非等权集成与完整父方案组合验证并发布完整榜与全量QA', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round117_receipt.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 117, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 340,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 28, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_official_pilot_records_registered': 340,
        'new_quality_scores_by_registration': 0,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round117'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
