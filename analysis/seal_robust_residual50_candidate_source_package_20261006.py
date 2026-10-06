"""Seal actual cohort inference with complete pre-inference sources and evidence."""
from pathlib import Path
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
FREEZE = A / 'robust_residual50_source_freeze_20261006'
RELEASE = A / 'robust_residual50_release_20261006'
CANDIDATE = ROOT / 'candidates/robust_residual50_20261006'


def checked_sources():
    record = read(FREEZE / 'manifest.json')
    assert record['status'] == 'passed_pre_inference_local_Python_source_snapshot'
    assert not record['test_labels_read']
    for relative, info in record['files'].items():
        assert sha(ROOT / relative) == sha(FREEZE / 'repo' / relative) == info['sha256'], relative
    for name in ('freeze_and_infer_robust_residual50_candidate_20261006.py',
                 'conditional_flag_residual_extrapolation_transform_20261006.py', 'predict_robust_residual50_native_scheme_20261006.py',
                 'seal_robust_residual50_candidate_source_package_20261006.py',
                 'conditional_flag_rank_codec_20261006.py', 'conditional_identity_regression_tree_codec_20261006.py'):
        assert f'analysis/{name}' in record['files'], name
    return record


def main():
    assert not (CANDIDATE / 'manifest.json').exists()
    service = A / 'service_owned_workflows_20261006/robust_residual50_candidate_inference'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'passed'
    sources = checked_sources()
    release = read(RELEASE / 'verification.json')
    prediction = read(CANDIDATE / 'verification.json')
    before = read(RELEASE / 'frozen_before_actual_candidate_inference.json')
    selection = read(CANDIDATE / 'selection.json')
    assert release['status'] == 'passed_frozen_conditional_residual_full_saved_model_candidate_and_independent_decoder_and_cold80'
    assert prediction['status'] == 'passed' and not prediction['test_labels_read']
    assert (prediction['rows'], prediction['days'], prediction['codes']) == (1599600, 344, 4650)
    assert sources['at_local'] <= selection['frozen_at_local']
    assert sha(RELEASE / 'selection.json') == before['selection_sha256']
    assert selection == read(RELEASE / 'selection.json')
    for key in ('model_reload_bit_identical', 'cold80_day_prefix_bit_identical',
                'pipeline_replay_bit_identical', 'csv_replay_byte_identical', 'old_delivery_pointer_unchanged'):
        assert prediction[key], key
    assert release['actual_model_reload_controls'] == prediction['actual_model_reload_controls']
    assert release['actual_cold80_model_controls'] == prediction['actual80_day_prefix_model_controls']
    assert sha(CANDIDATE / 'submission.csv') == prediction['csv_sha256'] == release['csv_sha256']
    curve = read(CANDIDATE / 'cohort_curve_replay_verification.json')
    assert curve['status'] == 'passed_actual_curve_reload_and_independent_full_and_cold80_future_decoder'
    assert sha(CANDIDATE / 'cohort_curve.json') == before['parent_curve_sha256']
    assert sha(CANDIDATE / 'cohort_curve.json') == prediction['whole_scheme_graph']['cohort_rank_calibration']['future_curve_model']['sha256']
    assert len(prediction['models']) == len(prediction['actual_model_reload_controls']) == len(prediction['actual80_day_prefix_model_controls']) == 13 + len(selection['native_component_names'])
    assert read(CANDIDATE / 'conditional_residual_native_replay_verification.json')['status'] == 'passed_actual_saved_parent13_and_selected_residual_heads_full_independent_decoder_and_cold80'
    for key, info in prediction['models'].items():
        assert Path(info['path']).resolve().is_relative_to(CANDIDATE.resolve()), key
        assert sha(info['path']) == info['sha256'], key
    assert len(release['actual_native_model_storage']) == len(prediction['models'])
    for relative, info in sources['files'].items():
        original = FREEZE / 'repo' / relative
        target = CANDIDATE / 'source_snapshot/repo' / relative
        assert target.resolve().is_relative_to(CANDIDATE.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(original, target)
        assert sha(target) == info['sha256']
    evidence = [FREEZE / 'manifest.json', FREEZE / 'frozen_before_source_copy.json',
                RELEASE / 'frozen_before_actual_candidate_inference.json', RELEASE / 'verification.json',
                RELEASE / 'causal_validation.json', RELEASE / 'calibrated_csv_official.json',
                A / 'robust_conditional_residual_comparison50_v2_20261006/verification.json',
                A / 'conditional_flag_residual_bank_20261006/verification.json',
                A / 'conditional_residual128_256_bank40_20261006/verification.json',
                A / 'robust_conditional_residual_bank20_v2_20261006/verification.json',
                A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',
                service / 'service_execution.json', service / 'native_launch.json']
    for path in evidence:
        target = CANDIDATE / 'evidence' / path.relative_to(A)
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(path, target)
        assert sha(target) == sha(path)
    create(CANDIDATE / 'source_package_verification.json', {
        'status': 'passed_actual_inference_outputs_and_pre_inference_local_source_package',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source_files': len(sources['files']),
        'source_snapshot_manifest_sha256': sha(FREEZE / 'manifest.json'),
        'actual_candidate_verification_sha256': sha(CANDIDATE / 'verification.json'),
        'csv_sha256': release['csv_sha256'],
        'actual_native_codec_curve_reload_cold80_and_full_CSV_replay_preserved': True,
        'all_models_sources_final_outputs_hash_verified': True,
        'selected_by_actual_full50_original_official_scores': True,
        'full_ranking_registration_and_QA_pending': True, 'new_quality_scores': 0, 'test_labels_read': False})
    create(CANDIDATE / 'manifest.json', {'status': 'passed', 'files': {
        p.relative_to(CANDIDATE).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
        for p in sorted(CANDIDATE.rglob('*')) if p.is_file() and p != CANDIDATE / 'manifest.json'}})
    manifest = read(CANDIDATE / 'manifest.json')
    assert len(manifest['files']) == sum(p.is_file() for p in CANDIDATE.rglob('*')) - 1
    for relative, info in manifest['files'].items():
        assert sha(CANDIDATE / relative) == info['sha256'], relative
    create(RELEASE / 'source_package_verification.json', {
        'status': 'passed_sealed_actual_conditional_residual_candidate', 'candidate': str(CANDIDATE),
        'manifest_sha256': sha(CANDIDATE / 'manifest.json'),
        'manifest_files': len(manifest['files']), 'full_ranking_and_main_publication_pending': True,
        'test_labels_read': False})
    print(json.dumps(read(RELEASE / 'source_package_verification.json')), flush=True)


if __name__ == '__main__':
    main()
