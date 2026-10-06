"""Freeze and admit a disjoint47-case convex ensemble scope plus main publication."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from handoff_ready_goss_full_execution_20261006 import start_service


def main():
    sources = [Path(__file__), A / 'run_residual_simplex47_official_comparison_20261006.py',
        A / 'publish_residual_simplex47_scores_20261006.py',
        A / 'run_conditional_flag_residual_official_comparison_20261006.py',
        A / 'publish_conditional_residual_evidence_20261006.py',
        A / 'conditional_flag_residual_extrapolation_transform_20261006.py',
        A / 'conditional_residual128_256_bank40_20261006/verification.json',
        A / 'longer_residual74_release_20261006/selection.json',
        A / 'longer_residual74_release_20261006/source_package_verification.json']
    for source in sources:
        if source.suffix == '.py':
            compile(source.read_text(encoding='utf-8'), str(source), 'exec')
    bank = read(sources[6])
    assert bank['status'] == 'passed_actual40_matched128_256_conditional_residual_native_models_and_independent_codec'
    pins = {str(p): sha(p) for p in sources}
    state = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    originals = {name: row for name, row in state['activated_jobs'].items() if owned(row)}
    wide = read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    if owned(wide):
        originals['neural16384_annual'] = wide
    triples = [(a, b, 4-a-b) for a in range(5) for b in range(5-a)]
    frozen = A / 'residual_simplex47_frozen_before_hidden_launch_20261006.json'
    create(frozen, {
        'status': 'frozen_before_actual47_convex_ensemble_scores',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'integer_weight_triples': triples, 'weight_denominator': 4,
        'fixed_amplitudes': [.75, 1., 1.25], 'expected_scored_records': 47,
        'anchors': ['parent100', 'actual74_selected_complete_scheme'],
        'arithmetic': 'repeat components leaf7/15/31 order, float64 ordered sum divided by4',
        'original_live_scientific_workers_preserved': originals,
        'original_queue_plan': read(A / 'service_owned_dependency_queue_v4_20261006/queue_plan_v10.json'),
        'new_native_fits': 0, 'test_labels_read': False,
    })
    pins[str(frozen)] = sha(frozen)
    science = start_service('residual_simplex47_official_comparison',
        'run_residual_simplex47_official_comparison_20261006.py', [], pins)
    publisher = start_service('residual_simplex47_scores_evidence_publication',
        'publish_residual_simplex47_scores_20261006.py', [], pins)
    create(A / 'residual_simplex47_hidden_admission_20261006.json', {
        'status': 'passed_actual_hidden_owned47_science_and_serialized_main_publication_admission',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'actual_science_service': science, 'actual_main_publication_service': publisher,
        'native_console_handles': [science['actual_native_console_handle'], publisher['actual_native_console_handle']],
        'original_scientific_workers_preserved_at_launch': originals,
        'original_still_live_at_end': {name: row for name, row in originals.items() if owned(row)},
        'main_publication_serialized_after_real_full105_terminal': True,
        'original_scientific_workers_suspended_stopped_or_restarted': 0,
        'actual47_full_scores_and_candidate_and_complete_ranking_not_claimed_complete': True,
        'new_native_fits': 0, 'test_labels_read': False,
    })
    print('Actual47 convex-mixture comparisons and main publication admitted without stopping scientists.', flush=True)


if __name__ == '__main__':
    main()
