"""Keep all previous searches required and add complete R66 comparison coverage."""
from pathlib import Path
import json
from datetime import datetime
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import refresh_optimization_boundary_evidence_v13_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes,write
    with operational_writes('refresh_optimization_boundary_evidence_v13_20261005'):previous.main()
    path=A/'optimization_boundary_evidence_20261004.json'
    boundary=read(path)
    qualified=[(int(p.stem.rsplit('_r',1)[1]),read(p)) for p in (ROOT/'results').glob('optimization_20261003_r*.json')]
    qualified=[row for row in qualified if row[0]<50 or complete_round_evidence(row[0]) is not None]
    best=max(qualified,key=lambda row:(row[1]['winner']['connected_final_score'],-row[0]))
    closed={n:complete_round_evidence(n) for n in (81,82)}
    entry={'method':'Complete fixed linear-leaf role and standalone grids against explicit qualified R66',
        'required_official_rounds':[81,82],'explicit_parent_rounds':{'81':66,'82':81},
        'actual_completed_official_rounds':[n for n,e in closed.items() if e is not None],
        'remaining_required_official_rounds':[n for n,e in closed.items() if e is None],
        'scored_records_prespecified':{'81':124,'82':138},'new_native_configurations':0,'new_native_fits':0,
        'all_original_rounds67_through80_retained_and_required':True,
        'same_5635800_rows_1212_continuous_days_and_original_official_scorer':True,
        'one_isolated_official_worker_changes_layout_only':True,'all264_generator_arms_counted_including_adaptive_refinements':False,
        'actual_generator_proof':'analysis/reference66_linear_leaf_generator_preflight_v2_20261005/verification.json',
        'actual_execution_source_controls':'analysis/reference66_linear_leaf_execution_preflight_20261005/verification.json',
        'finite_grid_not_global_method_or_resource_exhaustion':True,'test_labels_read':False}
    if entry['remaining_required_official_rounds']:boundary['open_feasible_directions'].append(entry)
    else:boundary['completed_declared_method_scopes'].append({'method':entry['method'],'rounds':[81,82],'evidence':closed,'finite_scope_only':True})
    boundary.update(reference66_linear_leaf_coverage_evidence=entry,
        completed_best=best[1]['winner']['connected_final_score'],best_completed_round=best[0],
        updated_at_local=datetime.now().isoformat(timespec='seconds'),
        additional_boundary_refresh_source=str(Path(__file__).relative_to(ROOT)),global_resource_exhaustion_established=False)
    write(path,boundary)
    path=A/'next_experiment_directions_20261003.json'
    directions=read(path)
    directions['directions']=[row for row in directions['directions'] if row.get('priority')!=38]+[
        {'priority':38,**entry,'status':'additional_complete_official_comparison_pending' if entry['remaining_required_official_rounds'] else 'completed_declared_reference_comparison_scope'}]
    directions.update(completed_best=best[1]['winner']['connected_final_score'],best_completed_round=best[0])
    write(path,directions)
