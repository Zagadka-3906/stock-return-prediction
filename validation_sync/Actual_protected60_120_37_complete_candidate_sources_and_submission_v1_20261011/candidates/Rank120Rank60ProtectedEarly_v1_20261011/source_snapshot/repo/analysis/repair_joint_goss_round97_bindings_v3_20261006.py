"""Fix dynamic version bindings; retain both intercepted failed launch attempts."""
from pathlib import Path
import json

A=Path(__file__).resolve().parent

def main():
    names=[
        'joint_goss_membership_search_engine_v2_20261006.py',
        'joint_goss_membership_release_engine_v2_20261006.py',
        'run_joint_goss_membership_round_v2_20261006.py',
        'check_joint_goss_membership_scheme_v2_20261006.py',
        'predict_joint_goss_membership_scheme_v2_20261006.py',
        'optimize_training_round97_v2.py','finalize_training_round97_v2.py','run_training_round97_v2_pipeline.py',
        'run_joint_goss_quality_qualified_workflow_v2_20261006.py',
        'run_joint_goss_quality_with_exact_rank_cache_v2_20261006.py',
        'verify_joint_goss_membership_generators_v2_20261006.py',
        'verify_joint_goss_round97_full_launcher_v2_20261006.py',
        'prepare_joint_goss_round97_queue_sources_v2_20261006.py',
    ]
    replacements={name:name.replace('_v2','_v3') for name in names}
    replacements.update({
        'joint_goss_membership_generator_preflight_v2_20261006':'joint_goss_membership_generator_preflight_v3_20261006',
        'joint_goss_round97_full_launcher_preflight_v2_20261006':'joint_goss_round97_full_launcher_preflight_v3_20261006',
        'joint_goss_membership_quality_run_v2_20261006.json':'joint_goss_membership_quality_run_v3_20261006.json',
        'joint_goss_membership_round97_previous_run_v2_20261006.json':'joint_goss_membership_round97_previous_run_v3_20261006.json',
        'joint_membership_retention_scope_20261006/planned_round97_v3.json':'joint_membership_retention_scope_20261006/planned_round97_v4.json',
        'run_dependency_queue_v9_20261006':'run_dependency_queue_v10_20261006',
        'monitor_actual_optimization_progress_v33':'monitor_actual_optimization_progress_v34',
        'progress_monitor_v33':'progress_monitor_v34',
        'actual_observer_version=33':'actual_observer_version=34',
        "'actual_observer_version': 33":"'actual_observer_version': 34",
        '(9, 8, 7, 6, 5, 4)':'(10, 9, 8, 7, 6, 5, 4)',
    })
    for name in names:
        text=(A/name).read_text(encoding='utf-8')
        for before,after in replacements.items():text=text.replace(before,after)
        for before,after in replacements.items():
            if before.endswith('.py'):text=text.replace(before[:-3],after[:-3])
        for stem in ('optimize_training_round','finalize_training_round','run_training_round'):
            text=text.replace(stem+'{number}_v1',stem+'{number}_v3')
        assert '{number}_v1' not in text
        if name.startswith('prepare_joint_goss_round97_queue'):
            text=text.replace('Frozen full round97 run and additive queue8/observer32 sources','Frozen full round97 run and additive queue10/observer34 sources')
        destination=A/replacements[name];compile(text,str(destination),'exec')
        with destination.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    p=A/'joint_membership_retention_scope_20261006/planned_round97_v3.json'
    value=json.loads(p.read_text(encoding='utf-8'))
    value.update(effective_source_version=3,original_dynamic_v1_factory_binding_failure_preserved=True,
        original_dynamic_factory_failure=str(A/'joint_goss_round97_full_launcher_preflight_v2_20261006/failure.json'),
        corrected_optimize_release_driver_and_frozen_source_dynamic_versions=3,
        scientific_grid_and_all151_records_unchanged=True,actual_pipeline_and_queue_adoption_pending=True)
    with (p.parent/'planned_round97_v4.json').open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
    print('Created v3 with explicit dynamic factory version3; prior failed controls preserved.',flush=True)

if __name__=='__main__':main()
