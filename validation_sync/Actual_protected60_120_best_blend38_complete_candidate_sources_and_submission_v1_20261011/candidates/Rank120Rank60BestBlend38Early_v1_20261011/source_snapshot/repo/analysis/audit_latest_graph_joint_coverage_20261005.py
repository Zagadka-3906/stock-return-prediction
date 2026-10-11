"""Audit real selected-graph coverage without fitting or scoring a new model."""
from pathlib import Path
from datetime import datetime
from copy import deepcopy
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from latest_graph_joint_axes_20261005 import active_axes, target, with_weight, retention_axes, expected_records, weight_values
from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    out = ROOT / 'analysis/latest_graph_joint_axes_scope_audit_20261005'
    out.mkdir(exist_ok=True)
    assert not (out / 'verification.json').exists()
    analysis = ROOT / 'analysis'
    latest = analysis / 'optimization_20261003_r59/selection.json'
    older = analysis / 'optimization_20261003_r50/protocol.json'
    sources = [Path(__file__), analysis / 'latest_graph_joint_axes_20261005.py',
               ROOT / '后续选模标准.md', latest, older,
               ROOT / 'results/optimization_20261003_r59.json',
               analysis / 'optimization_20261003_r59/provenance_scope_execution.json',
               analysis / 'round59_restart_recovery_20261005/verification.json',
               ROOT / 'candidates/optimization_20261003_r59/verification.json']
    bindings = {str(p.resolve()): fresh_sha(p) for p in sources}
    with LockedReadHashCache(bindings):
        graph = read(latest)['winner']['portfolio_surrogate_role_scheme_graph']
        axes = active_axes(graph)
        old_axes = read(older)['weight_axes']
        keys = lambda values: {(a['round'], a['group'], a['role'], a['model']) for a in values}
        missing = [axis for axis in axes if (axis['round'], axis['group'], axis['role'], axis['model']) not in keys(old_axes)]
        retired = [axis for axis in old_axes if (axis['round'], axis['group'], axis['role'], axis['model']) not in keys(axes)]
        routing = []
        for axis in axes:
            changed = with_weight(graph, axis, 0., axes)
            assert target(changed, axis)['weight'] == 0
            restored = with_weight(changed, axis, axis['anchor'], axes)
            assert restored == graph
            reference = deepcopy(graph)
            target(reference, axis)['weight'] = 0.
            assert changed == reference
            routing.append({'axis': axis, 'only_expected_weight_changed': True,
                            'zero_then_restore_original_graph_exact': True,
                            'declared_candidate_weights': weight_values(axis['anchor'])})
        assert len(axes) == len(old_axes) + len(missing) - len(retired)
        assert {axis['round'] for axis in missing} == {53, 55}
        plan = {'status': 'prepared_actual_complete_output_quality_and_inference_not_run',
            'prepared_at_local': datetime.now().isoformat(timespec='seconds'), 'planned_round': 63,
            'predecessor_round': 62, 'predecessor_must_pass_full_scientific_and_scoped_completion': True,
            'method': 'Recompute all actual active graph axes after the latest families; baseline, independent changes, forward and reverse coordinates, historical membership retention, final temporal grid.',
            'actual_axes_frozen_again_from_selected_r62_before_first_score': True,
            'current_r59_reference_axes': axes, 'current_reference_retention_axes': retention_axes(graph),
            'current_reference_expected_records': expected_records(graph),
            'actual_expected_records_formula': '1 + 18 * actual_active_weight_axes + 5 * actual_membership_retention_axes + 20',
            'weights': 'zero,half,anchor,double,anchor+0.0125,anchor+0.025; clipped[0,0.8]',
            'retentions': [0., .97, .98, .984, .99],
            'adaptive_coordinate_anchor_frozen_before_each_six_arm_evaluation': True,
            'same_validation': {'years': [2020, 2021, 2022, 2023, 2024], 'rows': 5635800, 'continuous_days': 1212},
            'selection': 'Highest actual complete official connected-output S; exact ties prefer fewer active model branches.',
            'all_previous_folds_preprocessing_and_maturity_preserved': True,
            'quality_gates': ['full baseline OOF output bit-identical to r62', 'all8 official baseline metrics exact',
                'baseline fullfuture CSV byte-identical', 'actual all-arm continuous official scoring',
                'complete scheme frozen before future inference', 'actual fullfuture reload and cold-prefix controls',
                'selected full-vector, cold-prefix and label-poisoning checks', 'full input end rehash and ranking QA'],
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'all_validation_years_previously_viewed': True, 'selection_bias_uncorrected': True,
            'global_resource_exhaustion_established': False,
            'finite_coordinate_grid_does_not_exhaust_all_possible_ensembles': True,
            'coverage_input_sha256': bindings}
        plan_path = analysis / 'latest_graph_joint_search_plan_20261005.json'
        create(plan_path, plan)
    create(out / 'verification.json', {'status': 'passed_actual_graph_routing_audit_only',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'actual_selected_r59_active_axes': len(axes), 'r50_joint_search_axes': len(old_axes),
        'current_cached_axis_metadata_count': len(graph['active_weight_axes']),
        'cached_axis_metadata_not_used_for_revised_axis_inventory': True,
        'not_covered_in_r50_joint_search': missing, 'previous_joint_axes_now_inactive': retired,
        'actual_graph_routing_controls': routing,
        'all_inputs_read_locked_and_fully_end_rehashed': True,
        'input_sha256': bindings, 'prepared_plan': str(plan_path), 'prepared_plan_sha256': fresh_sha(plan_path),
        'new_model_fits': 0, 'new_quality_scores': 0, 'future_candidate_inference_run': False,
        'all_new_quality_and_candidate_checks_pending': True, 'test_labels_read': False,
        'coverage_audit_does_not_establish_score_improvement_or_optimization_exhaustion': True})
    print(json.dumps({'status': 'passed_actual_graph_routing_audit_only', 'actual_active_axes': len(axes),
        'jointly_uncovered_later_axes': len(missing), 'conditional_reference_records': expected_records(graph),
        'new_quality_scores': 0}), flush=True)


if __name__ == '__main__':
    main()
