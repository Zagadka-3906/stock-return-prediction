"""Keep native linear-leaf and full official scheme checks open until actual evidence closes them."""
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[1]
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
from locked_read_hash_cache_20261004 import fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    temporary = Path(path).with_suffix('.linear_leaf_ensemble_boundary.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def main():
    import refresh_optimization_boundary_evidence_v5_20261005 as previous
    previous.main()
    cost = read(ROOT / 'analysis/optimization_fit_cost_evidence_20261004.json')
    storage = read(ROOT / 'analysis/linear_leaf_ensemble_storage_20261005.json')
    bank = Path(storage['output_directory'])
    execution = bank / 'construction_execution_scope.json'
    future = ROOT / 'analysis/linear_leaf_ensemble_future_qa_20261005/verification.json'
    preflight = ROOT / 'analysis/linear_leaf_ensemble_future_codec_preflight_20261005/verification.json'
    generator = ROOT / 'analysis/linear_leaf_ensemble_search_generator_preflight_v2_20261005/verification.json'
    assert read(preflight)['status'] == 'passed'
    assert read(generator)['status'] == 'passed'
    completed = {n:complete_round_evidence(n) for n in (71,72)}
    entry = {'method':'Fixed raw-score averages of mature same-target trees;40 virtual annual artifacts andcomplete official outputs',
        'required_official_rounds':[71,72], 'remaining_required_official_rounds':[n for n,v in completed.items() if v is None],
        'actual_completed_official_rounds':[n for n,v in completed.items() if v is not None],
        'scored_records_prespecified':{'71':148,'72':178},'expected_virtual_annual_outputs':40,'expected_new_annual_fits':0,'expected_virtual_final_bundles':8,'expected_new_final_fits':0,
        'actual_new_annual_fits':cost['linear_leaf_ensemble_actual_new_annual_fits'],'actual_virtual_annual_outputs':cost['linear_leaf_ensemble_actual_virtual_annual_outputs'],
        'actual_virtual_final_bundles':cost['linear_leaf_ensemble_actual_virtual_final_bundles'],'actual_new_final_fits':0,
        'actual_annual_execution_status':read(execution)['status'] if execution.exists() else 'pending',
        'actual_native_future_status':read(future)['status'] if future.exists() else 'pending',
        'matched_instrumentation_preflight':str(preflight.relative_to(ROOT)), 'preflight_sha256':fresh_sha(preflight),
        'generator_proof_sha256':fresh_sha(generator),'virtual_artifacts_do_not_double_count_real_parent_fits':True,
        'native_training_device':'cpu','GPU_capacity_not_relevant_to_this_native_family':True,
        'training_resource_summary':str(execution),'RAM_reserve_is_scheduling_policy':True,
        'finite_matched_leaf_scope_not_global_resource_or_method_exhaustion':True,'test_labels_read':False}
    path=ROOT/'analysis/optimization_boundary_evidence_20261004.json'
    value=read(path)
    if entry['remaining_required_official_rounds']:
        value['open_feasible_directions'].append(entry)
    else:
        value['completed_declared_method_scopes'].append({'method':entry['method'],'rounds':[71,72],
            'evidence':completed,'finite_scope_only':True})
    value.update(linear_leaf_ensemble_coverage_evidence=entry,additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),
        additional_boundary_refresh_source_sha256=fresh_sha(Path(__file__)),
        updated_at_local=datetime.now().isoformat(timespec='seconds'),global_resource_exhaustion_established=False)
    write(path,value)
    path=ROOT/'analysis/next_experiment_directions_20261003.json'
    directions=read(path)
    directions['directions']=[row for row in directions['directions'] if row.get('priority')!=33]+[{
        'priority':33,**entry,'status':'actual_virtual_outputs_native_fullfuture_and_quality_pending'
        if entry['remaining_required_official_rounds'] else 'completed_declared_linear_leaf_ensemble_quality_scope'}]
    write(path,directions)
