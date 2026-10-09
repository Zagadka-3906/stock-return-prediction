"""Keep full16384 native and final-output feasibility open until actual evidence closes it."""
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[1]
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
from locked_read_hash_cache_20261004 import fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    temporary = Path(path).with_suffix('.wide_boundary.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def main():
    import refresh_optimization_boundary_evidence_v3_20261005 as previous
    previous.main()
    cost = read(ROOT / 'analysis/optimization_fit_cost_evidence_20261004.json')
    storage = read(ROOT / 'analysis/neural16384_full_storage_20261005.json')
    bank = Path(storage['output_directory'])
    execution = bank / 'training_execution_scope.json'
    future = ROOT / 'analysis/neural16384_full_future_qa_20261005/verification.json'
    preflight = ROOT / 'analysis/neural16384_full_preflight_20261005/verification.json'
    generator = ROOT / 'analysis/neural16384_full_search_generator_preflight_v2_20261005/verification.json'
    assert read(preflight)['status'] == 'passed_actual_matched_instrumentation_and_architecture_controls'
    assert read(generator)['status'] == 'passed'
    completed = {n:complete_round_evidence(n) for n in (67,68)}
    entry = {'method':'Matched16384 width actual complete32epoch training and final-output evaluation',
        'required_official_rounds':[67,68], 'remaining_required_official_rounds':[n for n,v in completed.items() if v is None],
        'actual_completed_official_rounds':[n for n,v in completed.items() if v is not None],
        'scored_records_prespecified':{'67':64,'68':38},'expected_annual_fits':5,'expected_final_fits':1,
        'actual_annual_fits':cost['full16384_actual_annual_fits'],
        'actual_fulltraining_artifacts':cost['full16384_actual_fulltraining_artifacts'],
        'actual_annual_execution_status':read(execution)['status'] if execution.exists() else 'pending',
        'actual_native_future_status':read(future)['status'] if future.exists() else 'pending',
        'matched_instrumentation_preflight':str(preflight.relative_to(ROOT)), 'preflight_sha256':fresh_sha(preflight),
        'generator_proof_sha256':fresh_sha(generator),'no_one_step_substitution_for_complete_fits':True,
        'physical_gpu_total_bytes':12792037376,'allocator_reserved_is_not_resident_physical_VRAM':True,
        'training_resource_summary':str(execution),'RAM_reserve_is_scheduling_policy':True,
        'finite_matched_width_scope_not_global_resource_or_method_exhaustion':True,'test_labels_read':False}
    path=ROOT/'analysis/optimization_boundary_evidence_20261004.json'
    value=read(path)
    if entry['remaining_required_official_rounds']:
        value['open_feasible_directions'].append(entry)
    else:
        value['completed_declared_method_scopes'].append({'method':entry['method'],'rounds':[67,68],
            'evidence':completed,'finite_scope_only':True})
    value.update(full16384_coverage_evidence=entry,additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),
        additional_boundary_refresh_source_sha256=fresh_sha(Path(__file__)),
        updated_at_local=datetime.now().isoformat(timespec='seconds'),global_resource_exhaustion_established=False)
    write(path,value)
    path=ROOT/'analysis/next_experiment_directions_20261003.json'
    directions=read(path)
    directions['directions']=[row for row in directions['directions'] if row.get('priority')!=31]+[{
        'priority':31,**entry,'status':'actual_full_fits_native_future_and_quality_pending'
        if entry['remaining_required_official_rounds'] else 'completed_declared_full16384_quality_scope'}]
    write(path,directions)
