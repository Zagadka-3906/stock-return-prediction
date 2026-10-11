"""Fresh complete cohort inference from the sealed candidate's actual model bytes."""
from pathlib import Path
from types import SimpleNamespace
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read, sha, create


def main(output):
    import psutil
    assert psutil.virtual_memory().available >= 8 * 2**30
    candidate = ROOT / 'candidates/cohort_rank_calibration_20261006'
    release = A / 'cohort_rank_calibration_release_20261006'
    manifest = read(candidate / 'manifest.json')
    assert manifest['status'] == 'passed'
    for relative, item in manifest['files'].items():
        assert sha(candidate / relative) == item['sha256'], relative
    from seal_cohort_candidate_source_package_20261006 import checked_sources
    checked_sources()
    import optimize_training_round95_v3 as parent
    from predict_cohort_calibrated_scheme_20261006 import predict
    output = Path(output).resolve()
    assert output.drive.upper() in ('D:', 'E:') and not output.exists()
    ns = SimpleNamespace(**vars(parent))
    ns.OUT = release
    ns.GRAPH_FIELD = 'cohort_rank_calibration_scheme_graph'
    original = read(candidate / 'verification.json')
    ns.cohort_saved_models = original['models']
    for key, info in ns.cohort_saved_models.items():
        assert Path(info['path']).resolve().is_relative_to(candidate.resolve()), key
        assert sha(info['path']) == info['sha256'], key
    selection = read(candidate / 'selection.json')
    result, _ = predict(ns, selection, output, candidate / 'cohort_curve.json',
                        candidate / 'return_mapping.json')
    assert result['status'] == 'passed' and result['model_reload_bit_identical']
    assert result['cold80_day_prefix_bit_identical'] and result['pipeline_replay_bit_identical']
    assert sha(output / 'submission.csv') == original['csv_sha256']
    create(output / 'sealed_cohort_replay_verification.json', {
        'status': 'passed_fresh_full1599600_cohort_saved_model_inference',
        'source_candidate': str(candidate), 'source_manifest_sha256': sha(candidate / 'manifest.json'),
        'new_output_directory_not_cached_prediction': True,
        'actual_saved_models_and_independent_codecs': result['actual_model_reload_controls'],
        'actual_cold80_controls': result['actual80_day_prefix_model_controls'],
        'csv_sha256': result['csv_sha256'], 'new_model_fits': 0, 'test_labels_read': False})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    main(parser.parse_args().out)
