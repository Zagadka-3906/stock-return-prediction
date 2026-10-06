"""Freeze declared complete-output comparisons before any new model quality score."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    import no_dropout_seed_model_sources_20261004 as router
    path = ROOT / 'analysis/no_dropout_seed_complete_output_search_plan_20261004.json'
    assert not path.exists()
    sources = [Path(__file__), ROOT / '后续选模标准.md',
        ROOT / 'results/optimization_20261003_r31.json',
        router.native.OUT / 'protocol.json', router.virtual.OUT / 'protocol.json',
        ROOT / 'analysis/no_dropout_seed_preflight_20261004/verification.json',
        ROOT / 'analysis/no_dropout_seed_search_generator_preflight_20261004/verification.json',
        ROOT / 'analysis/no_dropout_seed_adapter_generation_20261004.json']
    router.dump(path, {'status': 'sources_andactual_generators_prepared_official_rounds_not_yet_queued',
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'model_configurations': router.NEW_CONFIGS, 'new_native_models': 4, 'new_virtual_models': 4,
        'new_annual_fits': 20, 'annual_forecast_artifacts': 40,
        'actual_previous_selection_required': {'53': 52, '54': 53},
        'waves': {'53': [226, 227, 228, 229], '54': [230, 231, 232]},
        'records_per_wave': {'53': [97, 8, 18, 25], '54': [49, 112, 17]},
        'expected_total_records': {'53': 148, '54': 178},
        'role_weights': [.005, .025, .075, .2], 'roles': ['membership', 'top', 'rest'],
        'role_floor_choices': [0., .97, .98, .984, .99], 'extra_limit_delta_choices': [-.04, -.02, 0., .02, .04],
        'standalone_initial_alpha_choices': [.8, .9, .95], 'standalone_initial_auxiliary_choices': [0., .25],
        'standalone_initial_bonus': .3, 'each_adaptive_coordinate_anchor_frozen_before_scoring': True,
        'actual_generator_control_status': 'passed',
        'complete5635800_row_validation_andcausal_calibration_required': True,
        'actual_previous1599600_row_future_CSV_byte_identity_required_before_quality_search': True,
        'new_role_inserted_before_frozen_final_temporal_transform': True,
        'standalone_replacement_discards_old_root_andall_old_role_layers': True,
        'scoring_target': '.4*IC_mean+.3*annual_excess+.3*(1-mean_turnover)',
        'same_continuous_validation_dates': '2020–2024;5635800 rows;1212 days;no year-boundary turnover reset',
        'forecast_calibration': 'Mature past-only; actual one-day-return CSV scored by original official evaluator',
        'new_quality_scores': 0, 'test_labels_read': False,
        'global_resource_exhaustion_established': False,
        'input_sha256': {str(p.resolve()): router.sha(p) for p in sources}}, immutable=True)
    print('No-dropout complete-output148/178-record plans frozen before new quality scores')


if __name__ == '__main__':
    main()
