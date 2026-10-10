"""Check real pending release closures and the first actual complete wide annual fit."""
from pathlib import Path
import datetime
import hashlib
import importlib
import json
import math
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'pending_round_dispatch_and_wide_fit_20261005'
sys.path[:0] = [str(ROOT), str(A)]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def closure(function):
    return [cell.cell_contents for cell in function.__closure__ or ()]


def save(name, value):
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    assert not OUT.exists()
    OUT.mkdir()
    sources = {Path(__file__), A / 'resumed_rounds_nystrom_locked_20261004.json'}
    jobs = [row for row in read(A / 'resumed_rounds_nystrom_locked_20261004.json') if row['round'] >= 67]
    assert {row['round'] for row in jobs} == set(range(67, 79))
    import publish_training_round as publication
    sources.add(Path(publication.__file__))
    controls = []
    frozen_sources_verified = {}
    for job in sorted(jobs, key=lambda row: row['round']):
        number = job['round']
        process = psutil.Process(job['pid'])
        command = process.cmdline()
        assert job['script'] in command
        assert command[-len(job['script_args']):] == job['script_args']
        assert not (ROOT / f'results/optimization_20261003_r{number}.json').exists()
        assert not Path(job['stderr']).read_bytes()
        run_path = Path(job['script_args'][1])
        sources.add(run_path)
        for filename, digest in read(run_path)['input_sha256'].items():
            path = Path(filename)
            if path.suffix == '.py':
                assert sha(path) == digest, filename
                frozen_sources_verified[str(path)] = digest
                sources.add(path)
        if number in (73, 74):
            from run_factorization_machine_round_v6_20261005 import bind_round_modules
            experiment, release = bind_round_modules(number)
        else:
            suffix = '_v2' if number <= 72 else ''
            experiment = importlib.import_module(f'optimize_training_round{number}{suffix}')
            sys.modules[f'optimize_training_round{number}'] = experiment
            release = importlib.import_module(f'finalize_training_round{number}')
        assert publication.importlib.import_module(f'optimize_training_round{number}') is experiment
        assert publication.importlib.import_module(f'finalize_training_round{number}') is release
        assert release.OUT == experiment.OUT == A / f'optimization_20261003_r{number}'
        assert experiment.PREVIOUS == A / f'optimization_20261003_r{number-1}'
        assert experiment.NUMBER == number
        for name in ('selected', 'select', 'calibrate'):
            assert experiment in closure(getattr(release, name)), (number, name)
        assert release.ReleaseContext.__bases__ == (experiment.Context,)
        assert release.selected in closure(release.ReleaseContext.__init__)
        sources.update((Path(experiment.__file__), Path(release.__file__)))
        controls.append({'round': number, 'owned_live_root': process.pid,
            'actual_optimizer_module': experiment.__name__, 'actual_release_module': release.__name__,
            'canonical_publication_import_identity': True,
            'correct_round_outputs_and_complete_previous_round': True,
            'actual_selected_select_calibrate_and_ReleaseContext_closures_correct': True,
            'waves': experiment.WAVES, 'planned_scored_records': job['expected_scored_records'],
            'scoring_and_future_inference_not_called_by_this_control': True})
    save('dispatch_controls.json', {'status': 'passed_all12_actual_pending_canonical_release_closures',
                                    'controls': controls, 'planned_scored_records': sum(row['planned_scored_records'] for row in controls),
                                    'frozen_actual_source_bindings_checked': frozen_sources_verified,
                                    'new_quality_scores': 0, 'test_labels_read': False})
    bank = A / 'neural16384_full_bank_20261005'
    name = 'rank16384_drop000_seed07_e32'
    info_path = bank / name / 'info_2020.json'
    info = read(info_path)
    baseline_path = A / 'neural_regularization_bank_20261003/rank512_drop000_e32/info_2020.json'
    baseline = read(baseline_path)
    for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end',
                'features', 'training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256'):
        assert info['training_meta'][key] == baseline['training_meta'][key], key
    measurement_path = bank / 'actual_native_fit_measurements.jsonl'
    measurement_lines = measurement_path.read_bytes().splitlines()
    complete = [json.loads(line) for line in measurement_lines
                if json.loads(line).get('context', {}).get('year') == 2020
                and json.loads(line).get('requested_epochs') == 32]
    assert len(complete) == 1
    actual = complete[0]
    assert actual['status'] == 'completed_original_requested_epochs'
    assert actual['completed_epochs'] == len(actual['training_losses']) == 32
    assert actual['configuration'] == info['configuration']
    assert actual['parameter_count'] == 168894465
    assert actual['actual_training_rows'] == info['training_meta']['rows'] == 1694259
    assert actual['actual_feature_count'] == len(info['training_meta']['features']) == 63
    assert actual['planned_native_optimizer_steps'] == math.ceil(1694259 / 32768) * 32 == 1664
    assert info['model_reload_bit_identical'] and info['test_data_read'] is False
    model_path = bank / name / 'model_2020.joblib'
    raw_path = bank / name / 'raw_2020.parquet'
    assert sha(model_path) == info['model_sha256']
    assert sha(raw_path) == info['prediction_sha256']
    prefix_path = bank / f'prefix_control_{name}_2020.json'
    boundary_path = bank / f'boundary_control_{name}_2020.json'
    assert read(prefix_path)['actual_saved_model_cold80_day_prefix_bit_identical']
    assert read(boundary_path)['boundary_future_label_poisoning_bit_identical']
    sources.update((info_path, baseline_path, prefix_path, boundary_path, bank / 'protocol.json'))
    save('actual_completed_2020_fit.json', {
        'status': 'passed_actual_complete32_epoch_fit_and_original_saved_controls',
        'training_info': info, 'actual_fit_record': actual,
        'actual_model_sha256': info['model_sha256'], 'actual_prediction_sha256': info['prediction_sha256'],
        'actual_cold80_day_prefix_rows': read(prefix_path)['rows'],
        'matched512_training_matrices_targets_keys_and_maturity_exact': True,
        'actual_new_completed_annual_fits': 1, 'remaining_complete_annual_fits': 4,
        'complete_final_training_and_official_quality_still_pending': True,
        'no_independent_prediction_or_scoring_run_by_this_hash_and_binding_audit': True,
        'partial_fit_evidence_is_not_full5year_native_qualification': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    save('verification.json', {'status': 'passed12_real_release_dispatches_and_actual_first_full_wide_annual_fit',
        'at_local': datetime.datetime.now().isoformat(), 'dispatch_control_count': len(controls),
        'frozen_py_source_bindings_checked': len(frozen_sources_verified),
        'actual_new_completed_annual_fits': 1, 'five_year_wide_model_still_incomplete': True,
        'input_sha256': {str(path): sha(path) for path in sorted(sources)},
        'test_labels_read': False, 'new_quality_scores': 0})
    print('Passed 12 real release dispatches and the actual first 32-epoch wide annual fit.', flush=True)


if __name__ == '__main__':
    main()
