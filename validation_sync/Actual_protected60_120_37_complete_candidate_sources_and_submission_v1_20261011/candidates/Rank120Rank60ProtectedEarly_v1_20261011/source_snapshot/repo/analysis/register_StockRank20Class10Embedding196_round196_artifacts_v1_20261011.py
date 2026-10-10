"""Register340 measured residual schemes and alias their real sealed selected candidate."""
from pathlib import Path
from copy import deepcopy
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
OUT = A / 'optimization_20261003_r196'
READY = read(A / 'StockRank20Class10Embedding196_selected_release_v1_20261011/selected_candidate_ready_for_registration.json')
RELEASE = Path(READY['source_release'])
SOURCE_CANDIDATE = Path(READY['source_candidate'])
CANDIDATE = ROOT / 'candidates/optimization_20261003_r196'
GRAPH_FIELD = 'conditional_flag_residual_scheme_graph'


def main():
    from stock_rank20class10_embedding196_storage_v1_20261011 import empty
    empty(OUT)
    from stock_rank20class10_embedding196_storage_v1_20261011 import empty
    empty(CANDIDATE)
    pilot_path = Path('E:/赛题五_本机临时/stock_rank20class10_embedding19_selected_native14_v1_20261011/pilot19.json')
    pilot = read(pilot_path)
    actual = read(SOURCE_CANDIDATE / 'verification.json')
    selection_source = SOURCE_CANDIDATE / 'selection.json'
    original = read(selection_source)
    manifest_path = SOURCE_CANDIDATE / 'manifest.json'
    manifest = read(manifest_path)
    seal_path = RELEASE / 'source_package_verification.json'
    seal = read(seal_path)
    assert pilot['status'] == 'passed_normalized19_actual_TRAIN_official_records_selected_stage_and_full_inference_pending'
    assert len(pilot['records']) == 19
    assert seal['status'] == 'passed_sealed_actual_conditional_residual_candidate'
    assert sha(manifest_path) == seal['manifest_sha256'] and manifest['status'] == 'passed'
    assert actual['status'] == 'passed' and len(actual['models']) == READY['actual_saved_native_models']
    assert actual['rows'] == 1599600 and actual['model_reload_bit_identical'] and actual['cold80_day_prefix_bit_identical']
    assert not actual['test_labels_read']
    from prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011 import source_paths
    sources=source_paths()
    pins = {**read(RELEASE / 'protocol.json')['input_sha256'], **pilot['input_sha256'], str(pilot_path): sha(pilot_path),
        str(manifest_path): sha(manifest_path), str(seal_path): sha(seal_path),
        **{str(p): sha(p) for p in sources}}
    for relative, info in manifest['files'].items():
        assert sha(SOURCE_CANDIDATE / relative) == info['sha256'], relative
        pins[str(SOURCE_CANDIDATE / relative)] = info['sha256']
    records = []
    for measured in pilot['records']:
        cfg = measured['configuration']
        if cfg['stage_kind']=='anchor':
            assert measured['qualified_anchor_all8_metrics_exact']
            assert measured['metrics'] == read(A / f"optimization_20261003_r{cfg['anchor_round']}/calibrated_csv_official.json")['metrics']
        else:
            control=read(Path(measured['original_screen_record']).with_name(f"case{measured['original_screen_case']:03d}_controls.json"))
            assert sha(Path(measured['original_screen_record']).with_name(f"case{measured['original_screen_case']:03d}_controls.json"))==measured['control_sha256']
            assert control['full_independent_Pandas_exact'] and [p['days'] for p in control['prefix_controls']]==[80,260,975]
            assert control['numeric_sha256']==measured['prediction_numeric_bytes_sha256']
        capsule = Path(measured['official_score_cache']['official_metrics_source'])
        assert sha(capsule) == measured['official_metric_capsule_sha256']
        assert read(capsule)['metrics'] == measured['metrics']
        pins[str(capsule)] = sha(capsule)
        cfg = deepcopy(measured['configuration'])
        if measured['case'] == pilot['best']['case']:
            graph = deepcopy(actual['whole_scheme_graph'])
        elif cfg['stage_kind']=='anchor':
            graph = deepcopy(read(ROOT / f"candidates/optimization_20261003_r{cfg['anchor_round']}/verification.json")['whole_scheme_graph'])
        else:
            graph = deepcopy(read(ROOT / f"candidates/optimization_20261003_r{cfg['anchor_round']}/verification.json")['whole_scheme_graph'])
            from stock_rank20class10_embedding_after_complete_qualified_parent_native_stage_v1_20261011 import GRAPH_KEY
            assert GRAPH_KEY not in graph
            assert len(measured['ordered_native_components'])==1
            screen_original=read(measured['original_screen_record']);assert screen_original['metrics']==measured['metrics']
            graph[GRAPH_KEY]={**cfg,'position':'after_complete_qualified_parent','original_complete_parent_round':cfg['anchor_round'],'original_complete_parent_graph_preserved':True,'original_completed_train_only_screen_record':measured['original_screen_record'],'ordered_native_components':measured['ordered_native_components'],'native_bank_components':measured.get('native_bank_components',[]),'future_candidate_not_inferred_for_nonselected_comparison':True}
        row = deepcopy(original['winner'])
        row[GRAPH_FIELD] = graph
        row.update(wave=479, arm=f'conditional_residual_case_{measured["case"]:02d}',
            connected_final_score=measured['connected_final_score'], metrics=deepcopy(measured['metrics']),
            official_score_cache=deepcopy(measured['official_score_cache']),
            causal_return_mapping=deepcopy(measured.get('actual_return_mapping',read(A/f"optimization_20261003_r{cfg['anchor_round']}/selection.json")['winner']['causal_return_mapping'])),
            original_official_pilot_record=measured.get('original_screen_record',str(pilot_path)),
            original_numeric_prediction_sha256=measured['prediction_numeric_bytes_sha256'],
            original_official_metric_capsule_sha256=measured['official_metric_capsule_sha256'],
            actual_full_conditional_residual_control=deepcopy(measured), direct_rank_comparison_configuration=deepcopy(cfg), original_comparison_case=measured['case'])
        records.append(row)
    records.sort(key=lambda r: (-r['connected_final_score'], r['actual_full_conditional_residual_control']['expected_unique_native_models'], abs(r['direct_rank_comparison_configuration']['weight']), r['original_comparison_case']))
    winner = records[0]
    assert winner[GRAPH_FIELD] == actual['whole_scheme_graph']
    assert winner['metrics'] == original['winner']['metrics'] == pilot['best']['metrics']
    for path, digest in pins.items():
        assert sha(path) == digest, path
    for relative in manifest['files']:
        target_relative = 'original_inference_selection_round196.json' if relative == 'selection.json' else ('original_registry_alias_round196.json' if relative == 'registry_alias_verification.json' else relative)
        target = CANDIDATE / target_relative
        assert target.resolve().is_relative_to(CANDIDATE.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(SOURCE_CANDIDATE / relative, target)
    for source in sources:
        target = CANDIDATE / 'registration_sources' / 'round196_full_scope' / (source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(sha(source)+'_'+source.name))
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
    selection = deepcopy(original)
    comparison_baseline = read(A/'optimization_20261003_r195/selection.json')['winner']['metrics']['final_score']
    selection.update(winner=winner, ranking=records, scored_records=19, baseline_score=comparison_baseline, score_gain=winner['connected_final_score'] - comparison_baseline,
        explicit_comparison_parent_round=195, preserved_scheme_training_parent_round=106, actual_scheme_base_round=pilot['actual_scheme_base_round'],
        original_frozen_selection_source=str(selection_source), original_frozen_selection_sha256=sha(selection_source),
        registry_created_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        registration_only_of_existing_executed_validation=True,
        original_inference_parameter_authority=GRAPH_FIELD, registered_parameter_authority=GRAPH_FIELD)
    selection['frozen_sha256'].update({Path(p).relative_to(ROOT).as_posix(): digest for p, digest in pins.items() if Path(p).is_relative_to(ROOT)})
    selection['frozen_external_input_sha256'] = {p: digest for p, digest in pins.items() if not Path(p).is_relative_to(ROOT)}
    selection['all_external_inputs_still_in_absolute_protocol_Windows_read_locks_and_final_rehash'] = True
    create(OUT / 'selection.json', selection)
    create(CANDIDATE / 'selection.json', selection)
    create(CANDIDATE / 'registry_alias_verification.json', {
        'status': 'passed_exact_file_aliases_of_actual_sealed_selected_model_residual_candidate',
        'source_candidate': str(SOURCE_CANDIDATE), 'source_manifest_sha256': sha(manifest_path),
        'registered_graph_equals_actual_inferred_graph': True,
        'original_selection_freeze_timestamp_preserved': original['frozen_at_local'],
        'new_inference_claimed_for_aliases': False, 'new_quality_scores': 0, 'test_labels_read': False})
    create(OUT / 'protocol.json', {'status': 'registered_previously_executed_training_validation_scope',
        'registration_only_of_existing_executed_validation': True, 'expected_scored_records': 19,
        'waves': [479], 'explicit_parent_round': 195, 'new_model_training_by_registration': False,
        'existing_own_stock_rank20_rank_Huber_native_bank_fits': 6, 'saved_selected_parent_models': len(read(ROOT/f'candidates/optimization_20261003_r{pilot["actual_scheme_base_round"]}/verification.json')['models']), 'actual_new_native_fits_by_this_scope': 0, 'actual_new_parent_curve_fits': 0,
        'original_pre_scoring_protocols': [str(Path('E:/赛题五_本机临时')/(f['name']+'_screen_v1_20261010')/'frozen_before_any_new_controls_or_scores.json') for f in read(A/'stock_rank20class10_embedding_complete19_after195_selection_plan_v1_20261011.json')['families']],
        'original_pre_inference_selection': str(selection_source),
        'original_selection_frozen_at_local': original['frozen_at_local'],
        'input_sha256': pins, 'actual_rows_days_stocks': [5635800, 1212, 4650],
        'test_labels_read': False, 'global_feasible_direction_or_resource_exhaustion_claimed': False})
    create(OUT / 'wave479_results.json', {'status': 'complete', 'results': {r['arm']: r for r in records},
        'original_official_pilot_source': str(pilot_path), 'new_scores_by_registration': 0})
    create(OUT / 'component_audit.json', {'status': 'passed',
        'actual_full_parent100_source': str(A / 'optimization_20261003_r100/component_audit.json'),
        'actual52_native_bank_source': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),
        'actual_original64_anchor_bank_source': str(A / 'conditional_flag_residual_bank_20261006/verification.json'),
        'all19_full_numeric_and_original_official_capsules_verified': True,
        'actual_declared_model_ensembles': ['rank20_rank_tiny_and_protected17','rank20_rank_large29','qualified175','qualified195'],
        'actual6_BF16_wide_native_bank_source': str(Path('E:/赛题五_本机临时/stock_rank20class10_embedding19_selected_native14_v1_20261011/verification.json')),
        'actual_selected_candidate_reuse_confirmation': str(A / 'StockRank20Class10Embedding196_selected_release_v1_20261011/selected_candidate_ready_for_registration.json'),
        'selected_saved_native_storage_counts_unique_components_only': True,
        'all8_baseline_official_metrics_exact': True, 'test_labels_read': False})
    create(OUT / 'conditional_flag_residual_causal_checks.json', {'status': 'passed',
        'actual_source': str(pilot_path), 'actual_all19_controls': pilot['records'],
        'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(Path('E:/赛题五_本机临时/stock_rank20class10_embedding19_selected_native14_v1_20261011/verification.json')),
        'selected_reference40_native_and_codec_controls': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),
        'actual_full_selected_saved_models_and_independent_tree_and_curve_decoder': str(SOURCE_CANDIDATE / ('stock_rank20class10_embedding_complete_parent_native_replay_verification.json' if READY['new_inference_claimed'] else 'verification.json')),
        'complete_parent100_causal_checks': str(A / 'optimization_20261003_r100/cohort_rank_calibration_causal_checks.json'),
        'new_quality_scores': 0, 'test_labels_read': False})
    create(OUT / 'causal_validation.json', read(RELEASE / 'causal_validation.json'))
    create(OUT / 'calibrated_csv_official.json', {**read(RELEASE / 'calibrated_csv_official.json'),
        'original_selected_official_pilot': winner['original_official_pilot_record'],
        'registration_not_a_new_official_evaluation': True})
    os.link(RELEASE / 'selected_validation.npy', OUT / 'selected_validation.npy')
    create(OUT / 'actual_registration_preparation.json', {
        'status': 'passed_actual19_scores_controls_and_sealed_selected_model_candidate_registered',
        'original_pre_scoring_and_pre_inference_freezes_preserved': True,
        'existing_actual_official_records': 19, 'new_quality_scores_by_registration': 0,
        'full_ranking_QA_and_provenance_scope_pending': True, 'test_labels_read': False})
    return read(OUT / 'protocol.json')


if __name__ == '__main__':
    main()
