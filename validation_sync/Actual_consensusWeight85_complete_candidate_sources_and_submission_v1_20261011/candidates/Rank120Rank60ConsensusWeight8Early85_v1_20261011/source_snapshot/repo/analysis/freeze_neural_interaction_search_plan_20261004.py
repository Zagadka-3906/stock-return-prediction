"""Freeze actual four-model generator scope before any comparative quality."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]

def main():
    import neural_interaction_model_sources_20261004 as router
    proof=ROOT/'analysis/neural_interaction_search_generator_preflight_20261004/verification.json'
    assert router.read(proof)['status']=='passed'
    sources=[Path(__file__),ROOT/'后续选模标准.md',router.native.OUT/'protocol.json',proof,
        ROOT/'analysis/neural_interaction_preflight_20261004/verification.json',
        ROOT/'analysis/neural_interaction_adapter_generation_20261004.json',
        ROOT/'results/optimization_20261003_r31.json',ROOT/'results/optimization_20261003_r35.json']
    router.dump(ROOT/'analysis/neural_interaction_complete_output_search_plan_20261004.json',{
        'status':'prepared_official_rounds_not_yet_queued','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'model_configurations':router.NEW_CONFIGS,'new_native_models':4,'new_annual_fits':20,
        'actual_previous_selection_required':{'55':54,'56':55},
        'waves':{'55':[233,234,235,236],'56':[237,238,239]},
        'records_per_wave':{'55':[49,8,18,25],'56':[25,56,17]},
        'expected_total_records':{'55':100,'56':98},
        'roles':['membership','top','rest'],'role_weights':[.005,.025,.075,.2],
        'role_floor_choices':[0.,.97,.98,.984,.99],'extra_limit_delta_choices':[-.04,-.02,0.,.02,.04],
        'standalone_initial_alpha_choices':[.8,.9,.95],'standalone_initial_auxiliary_choices':[0.,.25],
        'standalone_initial_bonus':.3,'each_adaptive_coordinate_anchor_frozen_before_scoring':True,
        'actual_generator_control_status':'passed','complete5635800_row_validation_andcausal_calibration_required':True,
        'actual_previous1599600_row_future_CSV_byte_identity_required_before_quality_search':True,
        'new_role_inserted_before_frozen_final_temporal_transform':True,
        'standalone_replacement_discards_old_root_andall_old_role_layers':True,
        'scoring_target':'.4*IC_mean+.3*annual_excess+.3*(1-mean_turnover)',
        'same_continuous_validation_dates':'2020–2024;5635800 rows;1212 days;no year-boundary turnover reset',
        'forecast_calibration':'Mature past-only; actual one-day-return CSV scored by original official evaluator',
        'new_quality_scores':0,'test_labels_read':False,'global_resource_exhaustion_established':False,
        'input_sha256':{str(p.resolve()):router.sha(p) for p in sources}},immutable=True)
    print('Neural optimizer-interaction complete100/98-record plans frozen',flush=True)

if __name__=='__main__':main()
