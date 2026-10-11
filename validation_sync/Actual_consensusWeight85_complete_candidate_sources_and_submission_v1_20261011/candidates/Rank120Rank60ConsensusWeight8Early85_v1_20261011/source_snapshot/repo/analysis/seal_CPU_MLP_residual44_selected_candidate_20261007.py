"""Seal only a closed actual selected inference, or confirm exact existing candidate reuse."""
from pathlib import Path
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def main():
    service = A / 'service_owned_workflows_20261006/CPU_MLP44_selected_candidate_preparation'
    while not (service / 'native_launch.json').exists() or owned(read(service / 'native_launch.json')):
        time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    release = A / 'CPU_MLP_residual44_selected_release_20261007'
    ready = read(release / 'inference_ready.json')
    candidate = Path(ready['source_candidate'])
    if not ready['new_inference_claimed']:
        assert ready['status'] == 'passed_exact_selected_anchor44_candidate_reuse'
        assert sha(candidate / 'manifest.json') == ready['manifest_sha256']
        for relative, info in read(candidate / 'manifest.json')['files'].items():
            assert sha(candidate / relative) == info['sha256']
        create(release / 'selected_candidate_ready_for_registration.json', {**ready,
            'status': 'passed_actual44_selected_candidate_full_graph_and_metrics_and_source_bytes',
            'source_manifest_sha256': sha(candidate / 'manifest.json'), 'sealed_candidate_complete': True})
        return
    assert ready['status'] == 'passed_actual_selected_new_CPU_MLP44_candidate_inference'
    assert not (candidate / 'manifest.json').exists()
    selection = read(candidate / 'selection.json')
    assert selection == read(release / 'selection.json')
    before = read(release / 'frozen_before_actual_candidate_inference.json')
    assert sha(release / 'selection.json') == before['selection_sha256']
    prediction = read(candidate / 'verification.json')
    assert prediction['status'] == 'passed' and prediction['test_labels_read'] is False
    for key in ('model_reload_bit_identical', 'pipeline_replay_bit_identical', 'csv_replay_byte_identical',
                'cold80_day_prefix_bit_identical', 'actual_CPU_MLP_saved_native_independent_decoder_and_CDF_replay'):
        assert prediction[key]
    assert sha(candidate / 'submission.csv') == prediction['csv_sha256']
    assert len(prediction['models']) == len(prediction['actual_model_reload_controls']) == len(prediction['actual80_day_prefix_model_controls']) == ready['actual_saved_native_models']
    assert read(candidate / 'CPU_MLP_residual_CDF_native_replay_verification.json')['status'] == 'passed_actual_parent15_and_selected_CPU_MLP_full_two_replays_independent_decoder_and_cold80'
    freeze = Path(ready['pre_inference_source_snapshot'])
    sources = read(freeze / 'manifest.json')
    assert sources['at_local'] <= selection['frozen_at_local']
    for relative, info in sources['files'].items():
        source = freeze / 'repo' / relative
        assert sha(ROOT / relative) == sha(source) == info['sha256']
        target = candidate / 'source_snapshot/repo' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
        assert sha(target) == info['sha256']
    for name, info in prediction['models'].items():
        assert Path(info['path']).resolve().is_relative_to(candidate.resolve())
        assert sha(info['path']) == info['sha256'], name
    evidence = [freeze / 'manifest.json', *[release / name for name in (
        'selected_case_before_future_features.json', 'frozen_before_actual_candidate_inference.json',
        'verification.json', 'causal_validation.json', 'calibrated_csv_official.json')],
        service / 'native_launch.json', service / 'service_execution.json',
        A / 'cpu_conditional_residual_mlp_bank20_20261007/verification.json',
        A / 'conditional_residual_mlp44_official_comparison_20261007/verification.json']
    for source in evidence:
        target = candidate / 'evidence' / source.relative_to(A)
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
        assert sha(target) == sha(source)
    create(candidate / 'source_package_verification.json', {'status': 'passed_actual_pre_inference_source_snapshot_and_CPU_MLP44_native_candidate',
        'actual_source_files': len(sources['files']), 'csv_sha256': prediction['csv_sha256'],
        'new_native_fits': 0, 'test_labels_read': False})
    create(candidate / 'manifest.json', {'status': 'passed', 'files': {
        path.relative_to(candidate).as_posix(): {'sha256': sha(path), 'bytes': path.stat().st_size}
        for path in sorted(candidate.rglob('*')) if path.is_file() and path != candidate / 'manifest.json'}})
    for relative, info in read(candidate / 'manifest.json')['files'].items():
        assert sha(candidate / relative) == info['sha256'], relative
    create(release / 'source_package_verification.json', {'status': 'passed_sealed_actual_conditional_residual_candidate',
        'candidate': str(candidate), 'manifest_sha256': sha(candidate / 'manifest.json'), 'test_labels_read': False})
    create(release / 'selected_candidate_ready_for_registration.json', {**ready,
        'status': 'passed_actual44_selected_candidate_full_graph_and_metrics_and_source_bytes',
        'source_manifest_sha256': sha(candidate / 'manifest.json'), 'sealed_candidate_complete': True})


if __name__ == '__main__':
    main()
