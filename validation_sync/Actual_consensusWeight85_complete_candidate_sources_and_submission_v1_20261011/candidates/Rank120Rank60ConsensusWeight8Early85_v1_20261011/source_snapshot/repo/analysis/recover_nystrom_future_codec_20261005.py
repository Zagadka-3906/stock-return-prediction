"""Retain passed controls and complete two failed typed-model future cases."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import os
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'analysis'), str(ROOT), str(ROOT / 'analysis/connected_validation_20261002')]
OUT = ROOT / 'analysis/nystrom_ridge_complete_scheme_preflight_20261004'
RECOVERY = ROOT / 'analysis/nystrom_future_codec_recovery_20261005'
RUN = ROOT / 'analysis/nystrom_future_codec_recovery_run_20261005.json'
SOURCE = ROOT / 'analysis/optimization_20261003_r29'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    while not RUN.exists():
        time.sleep(1)
    job = read(RUN)
    assert job['source_sha256'] == sha(Path(__file__))
    for path, digest in job['input_sha256'].items():
        assert sha(path) == digest, path
    assert not (OUT / 'verification.json').exists()
    assert not any((ROOT / f'analysis/optimization_20261003_r{n}/protocol.json').exists() for n in (61, 62, 63))
    original = read(OUT / 'frozen_before_controls.json')
    inputs = dict(original['input_sha256'])
    for path, digest in inputs.items():
        assert sha(path) == digest, path
    parameters = OUT / 'parameter_andreplay_checks.json'
    values = read(parameters)
    assert values['status'] == 'passed' and values['new_quality_scores'] == 0
    assert len(values['new_role_cases']) == 4 and len(values['role_controls']) == 13 and len(values['standalone_controls']) == 4
    error = Path(job['original_failed_stderr'])
    assert "KeyError: 'hidden'" in error.read_text(encoding='utf-8')
    baselines = {}
    for label in ('role_baseline', 'standalone_baseline'):
        path = OUT / label / 'candidate/verification.json'
        value = read(path)
        assert value['status'] == 'passed' and value['validation_score'] is None
        assert (value['rows'], value['days'], value['codes']) == (1599600, 344, 4650)
        assert value['csv_replay_byte_identical'] and value['cold80_day_prefix_bit_identical'] and not value['test_labels_read']
        assert sha(path.parent / 'submission.csv') == value['csv_sha256'] == sha(ROOT / 'candidates/optimization_20261003_r29/submission.csv')
        baselines[label] = sha(path)
    calibration = OUT / 'prototype_r61/calibrated_csv_official.json'
    assert read(calibration)['status'] == 'passed'
    assert read(calibration)['metrics'] == read(SOURCE / 'selection.json')['winner']['metrics']
    partial = OUT / 'role_changed'
    retained = RECOVERY / 'retained_failed_role_changed'
    assert partial.resolve().is_relative_to(OUT.resolve())
    assert retained.resolve().is_relative_to(RECOVERY.resolve()) and not retained.exists()
    partial_files = {str(p.relative_to(partial)): sha(p) for p in partial.rglob('*') if p.is_file()}
    assert not (partial / 'candidate/verification.json').exists()
    additions = [Path(__file__), RUN, parameters, error, calibration,
                 ROOT / 'analysis/nystrom_future_codec_adapter_20261005.py',
                 ROOT / 'analysis/fourier_tuning_model_sources_20261004.py',
                 ROOT / 'analysis/nystrom_ridge_model_sources_20261004.py',
                 ROOT / 'analysis/train_nystrom_ridge_bank_20261004.py',
                 *[OUT / label / 'candidate/verification.json' for label in baselines]]
    inputs.update({str(p.resolve()): sha(p) for p in additions})
    create(RECOVERY / 'frozen_before_future_controls.json', {
        'status': 'frozen_before_remaining_actual_future_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': inputs,
        'original_failure': 'Legacy future runtime routed ridge_nystrom bundles into the MLP hidden-layer constructor.',
        'versioned_change': 'Typed dispatch to the unchanged frozen native Nyström predictor; legacy bundles retain the original dispatch.',
        'retained_failed_partial_destination': str(retained), 'retained_partial_file_sha256': partial_files,
        'successful_parameter_calibration_and_two_actual_baseline_controls_reused': baselines,
        'original_sources_models_parameters_and_official_scorer_unchanged': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    partial.rename(retained)
    for relative, digest in partial_files.items():
        assert sha(retained / relative) == digest
    print('Retained failed codec case; passed parameter, calibration and two baseline controls preserved.', flush=True)
    scratch = ROOT / 'tmp/nystrom_future_codec_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[variable] = str(scratch)
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        os.environ[variable] = '8'
    import psutil
    while psutil.virtual_memory().available < 8 * 2**30:
        time.sleep(10)
    import optimize_training_round60 as parent
    import optimize_training_round61 as roles
    import optimize_training_round62 as pure
    from nystrom_ridge_scheme_runtime_20261004 import append_role_layer, native_sources
    from predict_nystrom_ridge_scheme_20261004 import predict
    from whole_scheme_future_runtime_20261004 import candidate_models
    from verify_whole_scheme_runtime_20261004 import root_graph
    from additive_basis_scheme_runtime_20261004 import append_role_layer as basis
    from no_dropout_seed_scheme_runtime_20261004 import append_role_layer as prior
    from neural_interaction_scheme_runtime_20261004 import append_role_layer as interaction
    from neural_width_scheme_runtime_20261004 import append_role_layer as width
    from portfolio_surrogate_scheme_runtime_20261004 import append_role_layer as portfolio
    old = read(SOURCE / 'selection.json')['winner']
    origin = root_graph(old)
    origin['root']['configuration'] = deepcopy(old)
    origin['temporal_postprocessing'] = {'alpha': 1., 'mix': 0., 'power': 1.}
    base = deepcopy(old)
    for key in parent.FIELDS:
        if key.endswith('_augmentation'):
            base.setdefault(key, {role: {'model': 'none', 'weight': 0.} for role in roles.ROLES})
        elif key.endswith('_limit_delta'):
            base.setdefault(key, 0.)
    base.setdefault('temporal_postprocessing', deepcopy(origin['temporal_postprocessing']))
    base['whole_scheme_graph'] = origin
    graph = origin
    for field, append in (('basis', basis), ('no_dropout', prior), ('neural_interaction', interaction),
                          ('neural_width', width), ('portfolio_surrogate', portfolio)):
        graph = append(graph)
        base[field + '_role_scheme_graph'] = graph
        base[field + '_standalone_scheme_graph'] = deepcopy(graph)
    fixture = {**parent.configuration(base), 'nystrom_ridge_role_scheme_graph': append_role_layer(graph)}
    fixture62 = {**deepcopy(fixture), 'nystrom_ridge_standalone_scheme_graph': deepcopy(fixture['nystrom_ridge_role_scheme_graph'])}
    roots = candidate_models(ROOT / 'candidates/optimization_20261003_r29')
    names = [f"seed{item['seed']}_f{item['fraction']:.3f}_r{item['rounds']}" for item in origin['root']['configuration']['recipe']['components']]
    roots = {name: roots[name] for name in names}
    for module, cfg in ((roles, fixture), (pure, fixture62)):
        module.OUT = OUT / f'prototype_r{module.NUMBER}'
        module.PREVIOUS = SOURCE
        module.baseline = lambda value=deepcopy(cfg): deepcopy(value)
        module.future_native_sources = lambda g: native_sources(g, {30: ROOT / 'candidates/optimization_20261003_r29'})
        module.root_model_sources = lambda g: {} if g['root']['kind'] == 'standalone' else deepcopy(roots)
    assert roles.graph(fixture) == read(OUT / 'role_baseline/candidate/verification.json')['whole_scheme_graph']
    assert pure.graph(fixture62) == read(OUT / 'standalone_baseline/candidate/verification.json')['whole_scheme_graph']
    role_cfg = deepcopy(fixture)
    roles.node(role_cfg)['specs']['rest'] = {'model': 'rank_nystrom64_s1_l01', 'weight': .025}
    pure_cfg = pure.standalone_cfg('rank_nystrom128_s1_l01')
    from nystrom_future_codec_adapter_20261005 import install
    restore = install()
    completed = dict(baselines)
    try:
        for label, module, cfg in (('role_changed', roles, role_cfg), ('pure_changed', pure, pure_cfg)):
            destination = OUT / label
            destination.mkdir(exist_ok=True)
            module.OUT = destination
            g = module.graph(cfg)
            module.dump(destination / 'protocol.json', {
                'status': 'frozen_implementation_control', 'input_sha256': inputs,
                'future_native_model_sources': module.future_native_sources(g),
                'future_root_model_sources': module.root_model_sources(g),
                'versioned_codec_recovery': str(RECOVERY / 'frozen_before_future_controls.json'),
                'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
            record = {'winner': {**cfg, 'connected_final_score': None},
                      'frozen_sha256': {'active_release.json': sha(ROOT / 'active_release.json')}}
            predict(module, record, candidate_path=destination / 'candidate', mapping_path=SOURCE / 'future_return_mapping.json')
            path = destination / 'candidate/verification.json'
            value = read(path)
            assert value['status'] == 'passed' and value['validation_score'] is None
            assert (value['rows'], value['days'], value['codes']) == (1599600, 344, 4650)
            assert value['model_reload_bit_identical'] and value['csv_replay_byte_identical'] and value['cold80_day_prefix_bit_identical']
            assert sha(path.parent / 'submission.csv') == value['csv_sha256'] and not value['test_labels_read']
            shutil.copyfile(ROOT / 'analysis/nystrom_future_codec_adapter_20261005.py', path.parent / 'nystrom_future_codec_adapter_20261005.py')
            completed[label] = sha(path)
            print('Actual typed-codec future case passed: ' + label, flush=True)
    finally:
        restore()
    for path, digest in inputs.items():
        assert sha(path) == digest, path
    create(RECOVERY / 'verification.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'all_four_actual_future_case_sha256': completed, 'input_sha256': inputs,
        'actual_corrected_future_cases': 2, 'all_runtime_bindings_restored': True,
        'original_failed_sources_logs_andpassed_partial_proofs_retained': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    create(OUT / 'verification.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_new_contexts_complete5635800_row_prior_output_andall8_metrics_exact': True,
        'all4_new_native_models_each_role_cold_prefix_controls_passed': True,
        'actual_standalone_branch_replacement_andindependent_composition_checks_passed': True,
        'actual_release_context_shared_causal_calibration_passed': True,
        'actual_new_future_helper_full1599600_row_baseline_CSV_byte_identical': True,
        'actual_changed_role_andnative_standalone_copied_model_future_CSV_andcold80_day_checks_passed': True,
        'candidate_verification_sha256': completed, 'parameter_replay_sha256': sha(parameters), 'input_sha256': inputs,
        'versioned_codec_recovery_evidence': str(RECOVERY / 'verification.json'),
        'versioned_codec_recovery_evidence_sha256': sha(RECOVERY / 'verification.json'),
        'new_quality_scores': 0, 'test_labels_read': False,
        'scope': 'Retained actual R29 parameter/calibration/baseline controls plus two completed typed Nyström future cases; actual R60/R61 quality searches remain required.'})
    print('Aggregate Nyström complete-scheme controls passed after versioned typed-codec recovery.', flush=True)


if __name__ == '__main__':
    main()
