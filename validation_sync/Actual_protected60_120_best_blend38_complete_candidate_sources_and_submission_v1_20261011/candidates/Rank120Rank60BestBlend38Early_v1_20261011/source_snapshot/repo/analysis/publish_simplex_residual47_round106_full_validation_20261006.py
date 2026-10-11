"""Publish the complete immutable round106 board, every original score, and QA."""
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
    from collect_full_lossless_round_publication_20261006 import collect
    sync = helpers.sync
    full_payload, full = collect(106, 17, 47)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v17_20261006/round106/qa/interaction_result.json'",
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
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round106/full_report_reconstructed_for_publication.json.gz'
    manifest, payload = namespace['snapshot'](106)
    assert manifest['scored_records'] == full['scored_records'] == 47
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round106')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    extra = [
        *list((A / 'simplex_residual47_release_20261006').glob('*.json')),
        *list((A / 'residual_simplex47_official_comparison_20261006').glob('case*_official.json')),
        A / 'residual_simplex47_official_comparison_20261006/frozen_before_actual_controls_and_official_scores.json',
        A / 'residual_simplex47_official_comparison_20261006/verification.json',
        A / 'simplex_residual47_full_registration_preparation_20261006.json',
        A / 'simplex_residual47_source_freeze_20261006/manifest.json',
        ROOT / 'candidates/optimization_20261003_r106/registry_alias_verification.json',
        ROOT / 'candidates/simplex_residual47_20261006/manifest.json']
    extra += list((A / 'residual_simplex47_official_comparison_20261006/identical_official_scores').glob('*.json'))
    extra += list((A / 'conditional_residual128_256_bank40_20261006').glob('*.json'))
    extra += list((A / 'service_owned_workflows_20261006/simplex_residual47_candidate_inference').glob('*.json'))
    extra += list((A / 'conditional_residual128_256_bank40_20261006').glob('*/info_*.json'))
    extra += [A / 'conditional_flag_residual_bank_20261006/verification.json',
        A / 'simplex_residual47_candidate_workflow_preparation_20261006.json',
        A / 'simplex_residual47_workflow_admission_20261006/verification.json']
    extra += list((A / 'conditional_residual128_256_bank40_20261006').glob('*/original64_prefix_*_verification.json'))

    extra += [ROOT / 'candidates/simplex_residual47_20261006/conditional_residual_native_replay_verification.json',
        ROOT / 'candidates/simplex_residual47_20261006/cohort_curve_replay_verification.json']
    extra += [A / 'simplex_residual47_workflow_admission_20261006/frozen_before_launch.json', A / 'simplex_residual47_candidate_admission_20261006/actual_admission.json', A / 'admit_simplex_residual47_candidate_20261006.py', A / 'wait_and_seal_simplex_residual47_candidate_20261006.py']
    extra += list((A / 'service_owned_workflows_20261006/simplex_residual47_candidate_sealing').glob('*.json'))
    extra += list((A / 'simplex_residual47_workflow_admission_20261006').glob('*.json'))
    extra += list((A / 'residual_simplex47_official_comparison_20261006').glob('*_verification.json'))
    extra += [A / 'residual_simplex47_frozen_before_hidden_launch_20261006.json',
        A / 'residual_simplex47_hidden_admission_20261006.json',
        A / 'run_residual_simplex47_official_comparison_20261006.py',
        A / 'publish_residual_simplex47_scores_20261006.py',
        A / 'residual_simplex47_scores_github_20261006/receipt.json']
    for name in ('residual_simplex47_official_comparison', 'residual_simplex47_scores_evidence_publication'):
        service = A / 'service_owned_workflows_20261006' / name
        extra += list(service.glob('*.json'))
        extra += list(service.glob('*.log'))
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
        actual_complete_QA_version=17, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate='candidates/simplex_residual47_20261006',
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix / 'README.md').as_posix()] += (
        '\n本轮是既有47项官方评分的正式登记：评分和方案冻结时间沿用原记录，'
        '全部1599600行预测、实际模型/独立编解码器及80日前缀复核在原命名候选目录实际完成，'
        '第106轮目录使用经SHA核验的相同文件硬链接，并不声称为新增推理。'
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
        '登记第106轮47项四分之一步长凸残差集成验证并发布完整榜与全量QA', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round106_receipt.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 106, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 47,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 17, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_official_pilot_records_registered': 47,
        'new_quality_scores_by_registration': 0,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round106'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
