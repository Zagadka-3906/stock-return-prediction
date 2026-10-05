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
    temporary = Path(path).with_suffix('.factorization_machine_boundary.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def main():
    import refresh_optimization_boundary_evidence_v6_20261005 as previous
    previous.main()
    cost = read(ROOT / 'analysis/optimization_fit_cost_evidence_20261004.json')
    storage = read(ROOT / 'analysis/factorization_machine_storage_20261005.json')
    bank = Path(storage['output_directory'])
    execution = bank / 'training_execution_scope.json'
    future = ROOT / 'analysis/factorization_machine_future_qa_v2_20261005/verification.json'
    preflight = ROOT / 'analysis/factorization_machine_preflight_20261005/verification.json'
    generator = ROOT / 'analysis/factorization_machine_search_generator_preflight_v4_20261005/verification.json'
    assert read(preflight)['status'] == 'passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls'
    assert read(generator)['status'] == 'passed'
    completed = {n:complete_round_evidence(n) for n in (73,74)}
    entry = {'method':'First order andlow rank raw63 FM interactions;30 annual32epoch CPU fits andcomplete output evaluation',
        'required_official_rounds':[73,74], 'remaining_required_official_rounds':[n for n,v in completed.items() if v is None],
        'actual_completed_official_rounds':[n for n,v in completed.items() if v is not None],
        'scored_records_prespecified':{'73':124,'74':138},'expected_annual_fits':30,'expected_final_fits':6,
        'actual_annual_fits':cost['factorization_machine_actual_annual_fits'],
        'actual_fulltraining_artifacts':cost['factorization_machine_actual_fulltraining_artifacts'],
        'actual_annual_execution_status':read(execution)['status'] if execution.exists() else 'pending',
        'actual_native_future_status':read(future)['status'] if future.exists() else 'pending',
        'matched_instrumentation_preflight':str(preflight.relative_to(ROOT)), 'preflight_sha256':fresh_sha(preflight),
        'generator_proof_sha256':fresh_sha(generator),'no4_epoch_pilot_substitution_for_complete32epoch_fits':True,
        'native_training_device':'cpu','GPU_capacity_not_relevant_to_this_native_family':True,
        'training_resource_summary':str(execution),'RAM_reserve_is_scheduling_policy':True,
        'finite_matched_leaf_scope_not_global_resource_or_method_exhaustion':True,'test_labels_read':False}
    path=ROOT/'analysis/optimization_boundary_evidence_20261004.json'
    value=read(path)
    if entry['remaining_required_official_rounds']:
        value['open_feasible_directions'].append(entry)
    else:
        value['completed_declared_method_scopes'].append({'method':entry['method'],'rounds':[73,74],
            'evidence':completed,'finite_scope_only':True})
    value.update(factorization_machine_coverage_evidence=entry,additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),
        additional_boundary_refresh_source_sha256=fresh_sha(Path(__file__)),
        updated_at_local=datetime.now().isoformat(timespec='seconds'),global_resource_exhaustion_established=False)
    write(path,value)
    path=ROOT/'analysis/next_experiment_directions_20261003.json'
    directions=read(path)
    directions['directions']=[row for row in directions['directions'] if row.get('priority')!=34]+[{
        'priority':34,**entry,'status':'actual_full_fits_native_future_and_quality_pending'
        if entry['remaining_required_official_rounds'] else 'completed_declared_factorization_machine_quality_scope'}]
    write(path,directions)
