"""Fresh full model/codec inference of the sealed selected buffer candidate."""
from pathlib import Path
from types import SimpleNamespace
import argparse
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read, sha, create


def main(output):
    import psutil
    assert psutil.virtual_memory().available >= 8 * 2**30
    candidate = ROOT / 'candidates/causal_entry_exit_buffer_20261006'
    release = A / 'causal_entry_exit_buffer_release_20261006'
    manifest = read(candidate / 'manifest.json')
    assert manifest['status'] == 'passed'
    for relative, item in manifest['files'].items():
        assert sha(candidate / relative) == item['sha256'], relative
    from seal_buffer_candidate_source_package_20261006 import checked_sources
    checked_sources()
    import numpy as np
    import optimize_training_round85_v2 as parent
    import whole_scheme_future_runtime_20261004 as runtime
    from causal_entry_exit_buffer_v2_20261006 import transform
    from predict_ready_classifier_reference_scheme_20261005 import predict
    output = Path(output).resolve()
    assert output.drive.upper() in ('D:', 'E:') and not output.exists()
    # Explicitly require a new output directory: the original predictor's
    # existing-verification shortcut must never count as fresh inference.
    output.mkdir(parents=True)
    namespace = SimpleNamespace(**vars(parent))
    namespace.OUT = release
    selection = read(candidate / 'selection.json')
    original_predict, original_copy = runtime.FutureContext.predict, runtime.copy_models

    def selected_predict(context, *args, **kwargs):
        values, stats = original_predict(context, *args, **kwargs)
        margin = context._whole_graph['entry_exit_buffer']['margin']
        assert margin == 0.
        result = transform(values, context.dates, context.flags, context.codes, margin)
        assert np.array_equal(result, values)
        return result, {**stats, 'entry_exit_buffer': {'margin': margin, 'labels_used': False}}

    def model_copy(native, roots, destination):
        # Use the selected candidate's actual verified model bytes rather than
        # relying on historical source paths surviving model-cache cleanup.
        stored = read(candidate / 'verification.json')['models']
        rebound_native, rebound_roots = {}, {}
        for key, info in {**roots, **{'whole_'+k: v for k, v in native.items()}}.items():
            actual = {**info, 'path': str(candidate / Path(stored[key]['path']).name)}
            assert sha(actual['path']) == info['sha256'] == stored[key]['sha256']
            if key.startswith('whole_'):
                rebound_native[key[6:]] = actual
            else:
                rebound_roots[key] = actual
        return original_copy(rebound_native, rebound_roots, destination)

    runtime.FutureContext.predict, runtime.copy_models = selected_predict, model_copy
    try:
        predict(namespace, selection, candidate_path=output, mapping_path=release / 'future_return_mapping.json')
        result = read(output / 'verification.json')
        assert result['status'] == 'passed' and result['model_reload_bit_identical']
        assert result['cold80_day_prefix_bit_identical'] and result['pipeline_replay_bit_identical']
        assert sha(output / 'submission.csv') == read(candidate / 'verification.json')['csv_sha256']
        create(output / 'buffer_replay_verification.json', {'status': 'passed_fresh_full1599600_buffer_candidate_model_inference',
            'source_candidate': str(candidate), 'source_manifest_sha256': sha(candidate / 'manifest.json'),
            'new_output_directory_not_cached_final_prediction': True,
            'actual_saved_model_and_independent_codec_controls': result['actual_model_reload_controls'],
            'actual_cold80_controls': result['actual80_day_prefix_model_controls'],
            'csv_sha256': sha(output / 'submission.csv'), 'new_model_fits': 0, 'test_labels_read': False})
    finally:
        runtime.FutureContext.predict, runtime.copy_models = original_predict, original_copy


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    main(parser.parse_args().out)
