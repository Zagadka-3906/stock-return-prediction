"""Freeze the actual pilot winner and replay its selected graph from saved models."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A), str(A / 'connected_validation_20261002')]
from run_dependency_queue_v3_20261006 import read, sha, create

OUT = A / 'causal_entry_exit_buffer_release_20261006'
CANDIDATE = ROOT / 'candidates/causal_entry_exit_buffer_20261006'


def main():
    import psutil
    assert psutil.virtual_memory().available >= 8 * 2**30
    assert not OUT.exists() and not CANDIDATE.exists()
    OUT.mkdir()
    import numpy as np
    import optimize_training_round85_v2 as parent
    from causal_entry_exit_buffer_v2_20261006 import transform
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    import whole_scheme_future_runtime_20261004 as runtime
    from predict_ready_classifier_reference_scheme_20261005 import predict
    pilot_path = A / 'causal_entry_exit_buffer_official_pilot_20261006/verification.json'
    pilot = read(pilot_path)
    assert pilot['status'] == 'completed_actual16_training_official_scores_full_submission_release_pending'
    best = max(pilot['records'], key=lambda row: (row['connected_final_score'], -row['margin']))
    # This actually measured grid selected the unmodified parent by the declared tie rule.
    assert best['margin'] == 0. and pilot['score_gain_over_frozen_parent'] == 0.
    parent_selection = read(parent.OUT / 'selection.json')
    parent_candidate = ROOT / 'candidates/optimization_20261003_r85'
    prior = read(parent_candidate / 'verification.json')
    assert prior['status'] == 'passed' and parent_selection['winner']['metrics'] == best['metrics']
    sources = [Path(__file__), A / 'causal_entry_exit_buffer_v2_20261006.py', pilot_path,
        parent.OUT / 'selection.json', parent.OUT / 'protocol.json',
        parent.OUT / 'future_return_mapping.json', parent_candidate / 'verification.json',
        A / 'whole_scheme_future_runtime_20261004.py',
        A / 'predict_ready_classifier_reference_scheme_20261005.py',
        A / 'predict_nystrom_ridge_scheme_20261004.py']
    pins = {**pilot['input_sha256'], **{str(path): sha(path) for path in sources}}
    graph_field = parent.GRAPH_FIELD
    selection = deepcopy(parent_selection)
    selection.update(status='frozen_before_test_prediction',
        frozen_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        actual_source_pilot=str(pilot_path), actual_pilot_records=16,
        chosen_postprocessor={'kind': 'causal_entry_exit_buffer_v2', 'margin': 0.},
        selection_rule='Highest original official continuous mapped-output score; exact ties prefer zero buffer',
        score_gain=0., test_labels_read=False,
        candidate_model_storage='Hardlinks to byte-verified existing models where possible, no new fits')
    selection['winner'][graph_field]['entry_exit_buffer'] = {'margin': best['margin'],
        'implementation': 'causal_entry_exit_buffer_v2_20261006.py', 'position': 'after_complete_graph'}
    selection['frozen_sha256'].update({str(Path(path).relative_to(ROOT).as_posix()): digest
        for path, digest in pins.items() if Path(path).is_relative_to(ROOT)})
    create(OUT / 'selection.json', selection)
    os.link(parent.OUT / 'protocol.json', OUT / 'protocol.json')
    os.link(parent.OUT / 'future_return_mapping.json', OUT / 'future_return_mapping.json')
    create(OUT / 'frozen_before_actual_candidate_inference.json', {
        'status': 'frozen_full_parent_graph_and_actual_zero_buffer_before_future_inference',
        'input_sha256': pins, 'selected_margin': best['margin'], 'actual_pilot_records': 16,
        'official_score': best['connected_final_score'], 'selection_sha256': sha(OUT / 'selection.json'),
        'no_future_features_or_labels_used_to_select_margin': True,
        'actual_saved_model_reload_and_full_cold80_controls_required': True,
        'new_model_fits': 0, 'test_labels_read': False})
    namespace = SimpleNamespace(**vars(parent))
    namespace.OUT = OUT
    original_predict = runtime.FutureContext.predict
    original_copy = runtime.copy_models
    events = []

    def buffered_predict(context, *args, **kwargs):
        values, stats = original_predict(context, *args, **kwargs)
        margin = context._whole_graph['entry_exit_buffer']['margin']
        output = transform(values, context.dates, context.flags, context.codes, margin)
        assert np.array_equal(output, values), 'Actual selected zero buffer must be a full-vector identity'
        return output, {**stats, 'entry_exit_buffer': {'margin': margin, 'actual_rows': len(output),
            'actual_complete_vector_bit_identical': True, 'labels_used': False}}

    def linked_models(native_sources, root_sources, destination):
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        copied = {}
        for key, info in {**root_sources, **{'whole_'+name: value for name, value in native_sources.items()}}.items():
            source = Path(info['path']).resolve()
            target = (destination / source.name).resolve()
            assert target.is_relative_to(CANDIDATE.resolve()) and sha(source) == info['sha256']
            mode = 'existing_identical'
            if not target.exists():
                if source.drive.upper() == target.drive.upper():
                    os.link(source, target)
                    mode = 'hardlink'
                else:
                    import shutil
                    shutil.copyfile(source, target)
                    mode = 'necessary_cross_volume_copy'
            assert sha(target) == info['sha256']
            if mode == 'hardlink': assert os.path.samefile(source, target)
            copied[key] = {**deepcopy(info), 'path': str(target), 'whole_graph_source': str(source)}
            events.append({'key': key, 'source': str(source), 'target': str(target),
                'sha256': info['sha256'], 'storage': mode, 'actual_model_bytes_verified': True})
        return copied

    runtime.FutureContext.predict = buffered_predict
    runtime.copy_models = linked_models
    try:
        with LockedReadHashCache(pins):
            predict(namespace, selection, candidate_path=CANDIDATE,
                mapping_path=OUT / 'future_return_mapping.json')
            candidate = read(CANDIDATE / 'verification.json')
            assert candidate['status'] == 'passed'
            assert (candidate['rows'], candidate['days'], candidate['codes']) == (1599600, 344, 4650)
            assert candidate['csv_sha256'] == prior['csv_sha256'] == sha(CANDIDATE / 'submission.csv')
            assert np.array_equal(np.load(CANDIDATE / 'rank_prediction.npy', mmap_mode='r'),
                np.load(parent_candidate / 'rank_prediction.npy', mmap_mode='r'))
            assert candidate['model_reload_bit_identical'] and candidate['cold80_day_prefix_bit_identical']
            create(OUT / 'verification.json', {
                'status': 'passed_actual_frozen_zero_buffer_full_candidate_saved_model_reload_and_cold80',
                'input_sha256': pins, 'actual_pilot_records': 16, 'selected_margin': 0.,
                'selected_official_score': best['connected_final_score'], 'score_gain': 0.,
                'candidate': str(CANDIDATE), 'csv_sha256': candidate['csv_sha256'],
                'rows': 1599600, 'days': 344, 'stocks': 4650,
                'actual_model_reload_controls': candidate['actual_model_reload_controls'],
                'actual_cold80_model_controls': candidate['actual80_day_prefix_model_controls'],
                'pipeline_replay_and_original_parent_csv_byte_identical': True,
                'actual_model_storage': events, 'new_model_fits': 0, 'test_labels_read': False,
                'formal_full_ranking_and_complete_source_manifest_qualification_pending': True})
            print('passed_actual_frozen_zero_buffer_full_candidate_saved_model_reload_and_cold80', flush=True)
    finally:
        runtime.FutureContext.predict = original_predict
        runtime.copy_models = original_copy


if __name__ == '__main__':
    try: main()
    except BaseException as exc:
        if OUT.exists() and not (OUT / 'failure.json').exists():
            create(OUT / 'failure.json', {'status': 'failed_preserved_frozen_buffer_candidate_inference',
                'error': f'{type(exc).__name__}: {exc}'})
        raise
