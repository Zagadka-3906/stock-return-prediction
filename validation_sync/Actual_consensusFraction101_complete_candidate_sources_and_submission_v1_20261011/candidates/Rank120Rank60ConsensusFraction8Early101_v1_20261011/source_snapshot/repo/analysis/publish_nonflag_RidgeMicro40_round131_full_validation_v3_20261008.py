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
    from collect_full_lossless_round131_qa42_20261007 import collect
    sync = helpers.sync
    full_payload, full = collect(131, 42, 40)
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / 'analysis/lossless_ranking_display_qa_v42_20261007/round131/qa/interaction_result.json'",
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
    namespace['PUBLICATION_FULL_REPORT'] = A / 'lossless_ranking_display_v2_20261006/round131/full_report_reconstructed_for_publication.json.gz'
    manifest, payload = namespace['snapshot'](131)
    assert manifest['scored_records'] == full['scored_records'] == 40
    assert manifest['connected_records'] == full['connected_records']
    assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
    payload.update(full_payload)
    manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
    manifest['exported_files'].update(full['exported_files'])
    prefix = Path('validation_sync/round131')
    # Retain the actual inference/cold-model controls and the original pilot
    # freeze rather than presenting the registry alias as fresh inference.
    ready = read(A / 'nonflag_RidgeMicro40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json')
    extra = [Path(__file__), A / 'nonflag_RidgeMicro40_round131_source_preparation_v1_20261007.json',
        A / 'prepare_nonflag_RidgeMicro40_round131_sources_v1_20261007.py',
        A / 'run_nonflag_RidgeMicro40_round131_full_registration_v1_20261007.py',
        A / 'nonflag_RidgeMicro40_round131_source_admission_v1_20261007.json',
        A / 'prepare_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',
        A / 'seal_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',
        A / 'predict_nonflag_residual_RidgeMicro_complete_scheme_20261007.py',
        A / 'nonflag_residual_RidgeMicro_compatible_parent_20261007.py',
        A / 'nonflag_RidgeMicro40_plan_20261007.json',
        A / 'nonflag_residual_RidgeMicro37_transform_preflight_20261007/verification.json',
        A / 'nonflag_RidgeMicro40_round131_source_admission_v1_20261007.json',
        A / 'local_118_119_publication_contract_v5_actual_hidden_launches_20261007.json',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py', A / 'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',
        A / 'quantile_HGB_bank20_github_v5_20261007/receipt.json',
        A / 'nonflag_RidgeMicro40_scores_github_v1_20261007/receipt.json',
        ROOT / 'candidates/optimization_20261003_r131/registry_alias_verification.json',
        Path(ready['source_candidate']) / 'manifest.json']
    for folder in (A / 'nonflag_RidgeMicro40_selected_release_v1_20261007', Path(ready['source_release']),
        A / 'nonflag_RidgeMicro40_official_comparison_v1_20261007',
        A / 'nonflag_residual_RidgeMicro37_transform_preflight_20261007'):
        extra += list(folder.glob('*.json'))
    extra += [p for p in (A / 'nonflag_residual_Ridge_bank10_20261007').rglob('*.json') if not p.name.startswith('independent_linear_state_')]
    for name in ('cpu_conditional_residual_hgb_native_bank20', 'nonflag_RidgeMicro40_official_comparison_v1',
        'cpu_conditional_residual_hgb20_bank_evidence_publication', 'nonflag_RidgeMicro40_scores_main_publication_v1',
        'nonflag_RidgeMicro40_selected_candidate_preparation_v1', 'nonflag_RidgeMicro40_selected_candidate_sealing_v1'):
        service = A / 'service_owned_workflows_20261006' / name
        extra += list(service.glob('*.json')) + list(service.glob('*.log'))
    extra += [A / 'nonflag_RidgeMicro40_actual_source_paths_before_registration_20261007.json', A / 'weighted_HGB340_actual_source_paths_before_registration_20261007.json']
    extra += [A/'prepare_actual_manual_resume_and_round131_publication_v3_20261008.py',A/'publish_nonflag_RidgeMicro40_round131_full_validation_20261007.py',A/'run_round131_preserved_QA42_main_recovery_v3_20261008.py',A/'actual_manual_resume_after_shutdown_20261008.json',A/'actual_next_morning_main_transport_handoff_20261007.json',A/'actual_night_manual_handoff_API_v2_20261007/receipt.json',A/'shutdown_ready_stop_until_manual_continue_20261007/disk_recovery_manifest.json',A/'optimization_20261003_r131/full_registration_failure.json',A/'optimization_20261003_r131/provenance_scope_execution.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/job_definition.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/launch_result.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/native_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/service_execution.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/verified_hidden_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/stderr.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/stdout.log']
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
        actual_complete_QA_version=42, registration_of_existing_official_pilot=True,
        actual_inference_source_candidate=ready['source_candidate'],
        original_selected_freeze_timestamp_preserved=True, new_quality_scores_by_registration=0)
    payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
    payload[(prefix / 'README.md').as_posix()] += '\n本轮实际40项完整官方比较：112、129、130三个合格锚点，两组非涨停残差Ridge及等权集成各12个幅度（36项），加一个消融。复用既有10个年度成熟Ridge模型，教师为106；37项5635800行全量变换和111项冷前缀核对通过。胜出l025残差权重0.002075，S=0.45111337697678194，较原最佳提高约7.28e-9。选中新方案已执行17个原生模型重载、独立解码、两次完整未来特征重放和冷80检查。完整榜13498条，原始六视图和45秒QA42完整保留。本次恢复昨晚失败的上传并核对全部冻结文件，不重复计入评分、拟合或推理。旧模板数量和轮次文字另作历史证据保留，不能替代本轮实际40项记录。仅main，未读取真实测试标签；不声称优化穷尽。\n'.encode('utf8')
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
        '补完第131轮40项Ridge验证完整榜与QA42并保留上传失败历史', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    assert helpers.blob_hashes(commit, hashes) == hashes
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    helpers.verify_main(commit)
    helpers.watcher.advance_source_index(commit)
    receipt = A / 'github_validation_sync_main_20261005/round131_receipt.json'
    create(receipt, {'status': 'pushed_and_remote_head_verified', 'round': 131, 'at_local': sync.now(),
        'commit': commit, 'branch': 'main', 'remote': sync.REMOTE,
        'official_score': manifest['metrics']['final_score'], 'scored_records': 40,
        'connected_records': manifest['connected_records'], 'raw_git_blobs_verified': len(hashes),
        'actual_full_QA_version': 42, 'full_immutable_ranking_and_all_original_QA_preserved': True, 'original_official_pilot_records_registered': 40,
        'new_quality_scores_by_registration': 0,
        'scheme_url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/round131'})
    print(json.dumps(read(receipt), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
