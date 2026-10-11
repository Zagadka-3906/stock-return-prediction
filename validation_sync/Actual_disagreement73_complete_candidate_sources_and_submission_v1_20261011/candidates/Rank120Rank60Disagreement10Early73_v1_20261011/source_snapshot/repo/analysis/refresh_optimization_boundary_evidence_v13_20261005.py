"""Preserve previous coverage and add the actual unfinished full classifier scope."""
from pathlib import Path
from datetime import datetime
import json
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import refresh_optimization_boundary_evidence_v12_20261005 as previous
    import refresh_streaming_rank_classifier_cost_evidence_20261005 as cost_module
    from atomic_optimization_observer_writes_20261005 import operational_writes,write
    with operational_writes('refresh_optimization_boundary_evidence_v12_20261005'):previous.main()
    cost_module.main()
    cost=read(A/'optimization_fit_cost_evidence_20261004.json')
    bank=Path(read(A/'streaming_rank_classifier_storage_v3_20261005.json')['output_directory'])
    complete={number:complete_round_evidence(number) for number in (79,80)}
    entry={'method':'Mature supplied-rank binary/decile streamed native classification',
        'required_official_rounds':[79,80],'actual_completed_official_rounds':[n for n,e in complete.items() if e is not None],
        'remaining_required_official_rounds':[n for n,e in complete.items() if e is None],
        'scored_records_prespecified':{'79':100,'80':98},'expected_annual_fits':20,'expected_final_fits':4,
        'actual_annual_fits':cost['streaming_rank_classifier_actual_annual_fits'],
        'actual_fulltraining_artifacts':cost['streaming_rank_classifier_actual_fulltraining_artifacts'],
        'actual_native_execution_status':read(bank/'training_execution_scope.json')['status'] if (bank/'training_execution_scope.json').exists() else 'pending',
        'actual_future_status':read(A/'streaming_rank_classifier_future_qa_v3_20261005/verification.json')['status'] if (A/'streaming_rank_classifier_future_qa_v3_20261005/verification.json').exists() else 'pending',
        'actual_full1694259_readonly_key_regression_and16_small32pass_controls':'analysis/streaming_rank_classification_preflight_v3_20261005/verification.json',
        'actual44_native_and_inherited_routes':'analysis/streaming_rank_classifier_direct_router_preflight_20261005/verification.json',
        'actual_generator_controls':'analysis/streaming_rank_classifier_search_generator_preflight_v4_20261005/verification.json',
        'actual_driver_canonical_and_candidate_source_controls':'analysis/streaming_rank_classifier_execution_source_preflight_v4_20261005/verification.json',
        'actual_quality_waiters':'analysis/streaming_rank_classifier_quality_followups_v4_20261005/verification.json',
        'provided_rank_quantiles_fit_only_from_mature_past':True,'all_eligible_rows_exactly32_native_passes':True,
        'complete_output_official_score_mature_return_mapping_and_previous_qualification_required':True,
        'failed_full32pass_attempt_and_pilot_fits_excluded':True,
        'finite_grid_not_global_resource_exhaustion':True,'test_labels_read':False}
    path=A/'optimization_boundary_evidence_20261004.json'
    boundary=read(path)
    if entry['remaining_required_official_rounds']:boundary['open_feasible_directions'].append(entry)
    else:boundary['completed_declared_method_scopes'].append({'method':entry['method'],'rounds':[79,80],'evidence':complete,'finite_scope_only':True})
    boundary.update(streaming_rank_classifier_coverage_evidence=entry,updated_at_local=datetime.now().isoformat(timespec='seconds'),
        additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),global_resource_exhaustion_established=False)
    write(path,boundary)
    path=A/'next_experiment_directions_20261003.json'
    directions=read(path)
    directions['directions']=[row for row in directions['directions'] if row.get('priority')!=37]+[
        {'priority':37,**entry,'status':'actual_full_native_fits_and_complete_official_quality_pending'
         if entry['remaining_required_official_rounds'] else 'completed_declared_classifier_scope'}]
    write(path,directions)
