"""Preserve failed v1; correct candidate destination construction in v2."""
from pathlib import Path
import json
import hashlib

A=Path(__file__).resolve().parent

def main():
    names=[
        'joint_goss_membership_search_engine_v1_20261006.py',
        'joint_goss_membership_release_engine_v1_20261006.py',
        'run_joint_goss_membership_round_v1_20261006.py',
        'check_joint_goss_membership_scheme_v1_20261006.py',
        'predict_joint_goss_membership_scheme_v1_20261006.py',
        'optimize_training_round97_v1.py','finalize_training_round97_v1.py',
        'run_training_round97_v1_pipeline.py',
        'run_joint_goss_quality_qualified_workflow_v1_20261006.py',
        'run_joint_goss_quality_with_exact_rank_cache_v1_20261006.py',
        'verify_joint_goss_membership_generators_v1_20261006.py',
        'verify_joint_goss_round97_full_launcher_v1_20261006.py',
    ]
    replacements={name:name.replace('_v1','_v2') for name in names}
    replacements.update({
        'joint_goss_membership_generator_preflight_v1_20261006':'joint_goss_membership_generator_preflight_v2_20261006',
        'joint_goss_round97_full_launcher_preflight_v1_20261006':'joint_goss_round97_full_launcher_preflight_v2_20261006',
        'joint_goss_membership_quality_run_v1_20261006.json':'joint_goss_membership_quality_run_v2_20261006.json',
        'joint_goss_membership_round97_previous_run_v1_20261006.json':'joint_goss_membership_round97_previous_run_v2_20261006.json',
        'joint_membership_retention_scope_20261006/planned_round97_v2.json':'joint_membership_retention_scope_20261006/planned_round97_v3.json',
        'run_dependency_queue_v8_20261006':'run_dependency_queue_v9_20261006',
    })
    # Import statements omit .py, so replace both literal names and module names.
    module_replacements={old[:-3]:new[:-3] for old,new in replacements.items() if old.endswith('.py')}
    for name in names:
        text=(A/name).read_text(encoding='utf-8')
        for before,after in replacements.items():text=text.replace(before,after)
        for before,after in module_replacements.items():text=text.replace(before,after)
        if name=='predict_joint_goss_membership_scheme_v1_20261006.py':
            before="candidate/name[:-len(suffix)]+'.py'"
            assert text.count(before)==1
            text=text.replace(before,"candidate/(name[:-len(suffix)]+'.py')")
        if name=='verify_joint_goss_round97_full_launcher_v1_20261006.py':
            # Explicit assertions also carry filenames in .endswith strings.
            text=text.replace("'optimize_training_round97_v1.py'","'optimize_training_round97_v2.py'")
        destination=A/replacements[name]
        compile(text,str(destination),'exec')
        with destination.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    text=(A/'prepare_joint_goss_round97_queue_sources_v1_20261006.py').read_text(encoding='utf-8')
    for before,after in replacements.items():text=text.replace(before,after)
    for before,after in module_replacements.items():text=text.replace(before,after)
    text=text.replace('monitor_actual_optimization_progress_v32','monitor_actual_optimization_progress_v33')
    text=text.replace('progress_monitor_v32','progress_monitor_v33')
    text=text.replace('actual_observer_version=32','actual_observer_version=33').replace("'actual_observer_version': 32","'actual_observer_version': 33")
    text=text.replace('(8, 7, 6, 5, 4)','(9, 8, 7, 6, 5, 4)')
    text=text.replace('prepare_joint_goss_round97_queue_sources_v1_20261006.py','prepare_joint_goss_round97_queue_sources_v2_20261006.py')
    with (A/'prepare_joint_goss_round97_queue_sources_v2_20261006.py').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    plan=A/'joint_membership_retention_scope_20261006/planned_round97_v2.json'
    value=json.loads(plan.read_text(encoding='utf-8'))
    value.update(effective_source_version=2,original_candidate_copy_failure_preserved=True,
        original_failure=str(A/'joint_goss_round97_full_launcher_preflight_v1_20261006/failure.json'),
        candidate_copy_correction="candidate / (stem + '.py')",
        scientific_grid_and_all151_records_unchanged=True,
        actual_pipeline_and_queue_adoption_pending=True)
    with (plan.parent/'planned_round97_v3.json').open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
    print('Preserved v1 sources and failure; created isolated corrected v2 sources.',flush=True)

if __name__=='__main__':main()
