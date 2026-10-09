"""Register37 measured schemes and alias the sealed actual14-model candidate."""
from pathlib import Path
from copy import deepcopy
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
OUT = A / 'optimization_20261003_r101'
RELEASE = A / 'conditional_flag_rank_release_20261006'
SOURCE_CANDIDATE = ROOT / 'candidates/conditional_flag_rank_20261006'
CANDIDATE = ROOT / 'candidates/optimization_20261003_r101'
GRAPH_FIELD = 'conditional_flag_rank_scheme_graph'


def main():
    assert not OUT.exists() and not CANDIDATE.exists()
    pilot_path = A / 'conditional_flag_rank_official_comparison_v2_20261006/verification.json'
    pilot = read(pilot_path)
    actual = read(SOURCE_CANDIDATE / 'verification.json')
    selection_source = SOURCE_CANDIDATE / 'selection.json'
    original = read(selection_source)
    manifest_path = SOURCE_CANDIDATE / 'manifest.json'
    manifest = read(manifest_path)
    seal_path = RELEASE / 'source_package_verification.json'
    seal = read(seal_path)
    assert pilot['status'] == 'passed_actual37_conditional_flag_full_controls_and_original_official_scores'
    assert len(pilot['records']) == 37
    assert seal['status'] == 'passed_sealed_actual_conditional_native14_candidate'
    assert sha(manifest_path) == seal['manifest_sha256'] and manifest['status'] == 'passed'
    assert actual['status'] == 'passed' and len(actual['models']) == 14
    assert actual['rows'] == 1599600 and actual['model_reload_bit_identical'] and actual['cold80_day_prefix_bit_identical']
    assert not actual['test_labels_read']
    sources = [Path(__file__), A / 'optimize_training_round101.py', A / 'finalize_training_round101.py',
        A / 'run_conditional_flag_round101_full_registration_20261006.py',
        A / 'publish_conditional_flag_round101_full_validation_20261006.py',
        A / 'prepare_conditional_flag_round101_registration_20261006.py',
        A / 'conditional_flag_round101_registration_source_preparation_20261006.json',
        A / 'lossless_ranking_runtime_adapter_v9_20261006.py',
        A / 'build_lossless_ranking_display_v10_20261006.py',
        A / 'verify_lossless_ranking_display_v12_20261006.py',
        A / 'publish_explicit_parent_training_round_v2_20261005.py']
    pins = {**read(RELEASE / 'protocol.json')['input_sha256'], str(pilot_path): sha(pilot_path),
        str(manifest_path): sha(manifest_path), str(seal_path): sha(seal_path),
        **{str(p): sha(p) for p in sources}}
    for relative, info in manifest['files'].items():
        assert sha(SOURCE_CANDIDATE / relative) == info['sha256'], relative
        pins[str(SOURCE_CANDIDATE / relative)] = info['sha256']
    records = []
    for measured in pilot['records']:
        assert measured['all1212_nonflagged_orders_and_ties_exact'] and measured['actual_cold80_260_975_bits_exact']
        capsule = Path(measured['official_score_cache']['official_metrics_source'])
        assert sha(capsule) == measured['official_metric_capsule_sha256']
        assert read(capsule)['metrics'] == measured['metrics']
        pins[str(capsule)] = sha(capsule)
        cfg = deepcopy(measured['configuration'])
        graph = deepcopy(actual['whole_scheme_graph'])
        if measured['case'] != pilot['best']['case']:
            graph['conditional_flag_rank'] = {**cfg,
                'annual_common_curves_source': str(A / 'conditional_flag_rank_official_comparison_v2_20261006/annual_common_rank_curves.json'),
                'actual_annual_native_bank': measured['native_bank_source'],
                'future_common_curve': None, 'future_candidate_not_inferred_for_nonselected_comparison': True,
                'position': 'after_complete_qualified_parent99_graph_and_saved_cohort_curve'}
        row = deepcopy(original['winner'])
        row[GRAPH_FIELD] = graph
        row.update(wave=384, arm=f'conditional_flag_case_{measured["case"]:02d}',
            connected_final_score=measured['connected_final_score'], metrics=deepcopy(measured['metrics']),
            official_score_cache=deepcopy(measured['official_score_cache']),
            causal_return_mapping=deepcopy(measured['actual_return_mapping']),
            original_official_pilot_record=str(A / f'conditional_flag_rank_official_comparison_v2_20261006/case{measured["case"]:02d}_official.json'),
            original_numeric_prediction_sha256=measured['prediction_numeric_bytes_sha256'],
            original_official_metric_capsule_sha256=measured['official_metric_capsule_sha256'],
            actual_full_conditional_causal_control=deepcopy(measured))
        records.append(row)
    records.sort(key=lambda r: (-r['connected_final_score'], r[GRAPH_FIELD]['conditional_flag_rank']['weight'], r['arm']))
    winner = records[0]
    assert winner[GRAPH_FIELD] == actual['whole_scheme_graph']
    assert winner['metrics'] == original['winner']['metrics'] == pilot['best']['metrics']
    for path, digest in pins.items():
        assert sha(path) == digest, path
    OUT.mkdir()
    CANDIDATE.mkdir()
    for relative in manifest['files']:
        target_relative = 'original_inference_selection.json' if relative == 'selection.json' else relative
        target = CANDIDATE / target_relative
        assert target.resolve().is_relative_to(CANDIDATE.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(SOURCE_CANDIDATE / relative, target)
    for source in sources:
        target = CANDIDATE / 'registration_sources' / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
    selection = deepcopy(original)
    selection.update(winner=winner, ranking=records,
        original_frozen_selection_source=str(selection_source), original_frozen_selection_sha256=sha(selection_source),
        registry_created_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        registration_only_of_existing_executed_validation=True,
        original_inference_parameter_authority=GRAPH_FIELD, registered_parameter_authority=GRAPH_FIELD)
    selection['frozen_sha256'].update({Path(p).relative_to(ROOT).as_posix(): digest for p, digest in pins.items()})
    create(OUT / 'selection.json', selection)
    create(CANDIDATE / 'selection.json', selection)
    create(CANDIDATE / 'registry_alias_verification.json', {
        'status': 'passed_exact_file_aliases_of_actual_sealed14_model_candidate',
        'source_candidate': str(SOURCE_CANDIDATE), 'source_manifest_sha256': sha(manifest_path),
        'registered_graph_equals_actual_inferred_graph': True,
        'original_selection_freeze_timestamp_preserved': original['frozen_at_local'],
        'new_inference_claimed_for_aliases': False, 'new_quality_scores': 0, 'test_labels_read': False})
    create(OUT / 'protocol.json', {'status': 'registered_previously_executed_training_validation_scope',
        'registration_only_of_existing_executed_validation': True, 'expected_scored_records': 37,
        'waves': [384], 'explicit_parent_round': 99, 'new_model_training_by_registration': False,
        'actual_native_bank_fits': 18, 'actual_annual_common_pair_fits': 4, 'actual_final_common_pair_fits': 1,
        'original_pre_scoring_protocol': str(A / 'conditional_flag_rank_official_comparison_v2_20261006/frozen_before_actual_controls_and_official_scores.json'),
        'original_pre_inference_selection': str(selection_source),
        'original_selection_frozen_at_local': original['frozen_at_local'],
        'input_sha256': pins, 'actual_rows_days_stocks': [5635800, 1212, 4650],
        'test_labels_read': False, 'global_feasible_direction_or_resource_exhaustion_claimed': False})
    create(OUT / 'wave384_results.json', {'status': 'complete', 'results': {r['arm']: r for r in records},
        'original_official_pilot_source': str(pilot_path), 'new_scores_by_registration': 0})
    create(OUT / 'component_audit.json', {'status': 'passed',
        'actual_full_parent99_source': str(A / 'optimization_20261003_r99/component_audit.json'),
        'actual18_native_bank_source': str(A / 'conditional_flag_rank_bank_v2_20261006/verification.json'),
        'all37_full_numeric_and_original_official_capsules_verified': True,
        'all8_baseline_official_metrics_exact': True, 'test_labels_read': False})
    create(OUT / 'conditional_flag_rank_causal_checks.json', {'status': 'passed',
        'actual_source': str(pilot_path), 'actual_all37_controls': pilot['records'],
        'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A / 'conditional_flag_rank_bank_v2_20261006/verification.json'),
        'actual_full_future14_models_and_independent_tree_and_curve_decoder': str(SOURCE_CANDIDATE / 'conditional_native_replay_verification.json'),
        'complete_parent99_causal_checks': str(A / 'optimization_20261003_r99/cohort_rank_calibration_causal_checks.json'),
        'new_quality_scores': 0, 'test_labels_read': False})
    create(OUT / 'causal_validation.json', read(RELEASE / 'causal_validation.json'))
    create(OUT / 'calibrated_csv_official.json', {**read(RELEASE / 'calibrated_csv_official.json'),
        'original_selected_official_pilot': winner['original_official_pilot_record'],
        'registration_not_a_new_official_evaluation': True})
    os.link(RELEASE / 'selected_validation.npy', OUT / 'selected_validation.npy')
    create(OUT / 'actual_registration_preparation.json', {
        'status': 'passed_actual37_scores_controls_and_sealed14_model_candidate_registered',
        'original_pre_scoring_and_pre_inference_freezes_preserved': True,
        'existing_actual_official_records': 37, 'new_quality_scores_by_registration': 0,
        'full_ranking_QA_and_provenance_scope_pending': True, 'test_labels_read': False})
    return read(OUT / 'protocol.json')


if __name__ == '__main__':
    main()
