"""Preserve old coverage, then restore new costs before adding memory-layout scope."""
from pathlib import Path
from datetime import datetime
import json
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import refresh_optimization_boundary_evidence_v11_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes,write
    with operational_writes('refresh_optimization_boundary_evidence_v11_20261005'):
        previous.main()
    import refresh_memory_efficient_neural_cost_evidence_20261005 as cost_module
    with operational_writes('refresh_memory_efficient_neural_cost_evidence_20261005'):
        cost_module.main()
    plan=read(A/'memory_efficient_neural_complete_search_plan_20261005.json')
    cost=read(A/'optimization_fit_cost_evidence_20261004.json')
    bank=Path(read(A/'memory_efficient_neural_storage_20261005.json')['output_directory'])
    completed={n:complete_round_evidence(n) for n in (77,78)}
    GPU=Path(read(A/'memory_efficient_mlp_storage_20261005.json')['GPU_control_directory'])
    entry={'method':'Matched16384 memory-efficient MLP execution','required_official_rounds':[77,78],
        'actual_completed_official_rounds':[n for n,e in completed.items() if e is not None],
        'remaining_required_official_rounds':[n for n,e in completed.items() if e is None],
        'scored_records_prespecified':plan['expected_total_records'],'expected_annual_fits':15,'expected_final_fits':3,
        'actual_annual_fits':cost['memory_efficient_neural_actual_annual_fits'],
        'actual_fulltraining_artifacts':cost['memory_efficient_neural_actual_fulltraining_artifacts'],
        'actual_annual_execution_status':read(bank/'training_execution_scope.json')['status'] if (bank/'training_execution_scope.json').exists() else 'pending',
        'actual_native_future_status':read(A/'memory_efficient_neural_future_qa_20261005/verification.json')['status'] if (A/'memory_efficient_neural_future_qa_20261005/verification.json').exists() else 'pending',
        'actual_GPU_control_status':read(GPU/'execution_scope.json')['status'] if (GPU/'execution_scope.json').exists() else 'waiting_for_original_GPU_attempt_closure',
        'actual_CPU_control_proof':'analysis/memory_efficient_mlp_preflight_20261005/verification.json',
        'actual40_direct_and_inherited_codec_proof':'analysis/memory_efficient_neural_direct_router_preflight_20261005/verification.json',
        'actual_generator_controls':'analysis/memory_efficient_neural_search_generator_preflight_20261005/verification.json',
        'actual_pipeline_and_native_waiters':'analysis/memory_efficient_neural_followups_20261005/verification.json',
        'original_width32epochs_effective32768batch_and_AdamW_step_count_retained':True,
        'prototype_and_single_step_fits_not_counted_as_complete_annual_fits':True,
        'microbatch_roundoff_requires_actual_independent_official_quality':True,
        'native_bank_and_scratch_drive':bank.drive,'RAM_disk_reserves_are_scheduling_policy':True,
        'finite_grid_not_global_method_or_physical_resource_exhaustion':True,'test_labels_read':False}
    boundary_path=A/'optimization_boundary_evidence_20261004.json'
    boundary=read(boundary_path)
    if entry['remaining_required_official_rounds']:
        boundary['open_feasible_directions'].append(entry)
    else:
        boundary['completed_declared_method_scopes'].append({'method':entry['method'],'rounds':[77,78],'evidence':completed,'finite_scope_only':True})
    boundary.update(memory_efficient_neural_coverage_evidence=entry,updated_at_local=datetime.now().isoformat(timespec='seconds'),
        additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),global_resource_exhaustion_established=False)
    write(boundary_path,boundary)
    path=A/'next_experiment_directions_20261003.json'
    directions=read(path)
    directions['directions']=[row for row in directions['directions'] if row.get('priority')!=36]+[
        {'priority':36,**entry,'status':'actual_full_native_fits_and_complete_official_quality_pending'
            if entry['remaining_required_official_rounds'] else 'completed_declared_memory_layout_scope'}]
    directions['last_completed_round']=boundary['latest_completed_round']
    directions['validation_best_completed']=boundary['completed_best']
    write(path,directions)
