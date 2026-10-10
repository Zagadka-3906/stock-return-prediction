"""Predeclare signed local amplitudes, complete routes, and a fresh full37 causal control."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from nonflag_ReverseBayesFine40_round134_mapping_v1_20261008 import convert


def write_new(name, text):
    path = A / name
    compile(text, str(path), 'exec')
    assert not path.exists(), path
    path.write_text(text, encoding='utf8', newline='\n')
    return path


def main():
    deadline = read(A / 'actual_user_submission_deadline_and_priority_20261008.json')
    assert deadline['deadline_local'] == '2026-10-10T23:59:00+08:00'
    bank = A / 'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json'
    hook = A / 'nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007/verification.json'
    assert read(bank)['actual_native_fits'] == 10 and len(read(hook)['records']) == 3
    plan = read(A / 'nonflag_ReverseBayes40_plan_20261007.json')
    weights = [.008, .0085, .009, .0095, .00975, .01025, .0105, .011, .0115, .012, .0125, .013]
    assert len(weights) == len(set(weights)) == 12
    plan.update(status='frozen_new_finite_negative_Bayes_amplitude_grid_before_actual_controls_or_quality',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'), round=134, wave=417, after_round=133,
        qualified_anchor_rounds=[112, 132, 133], weights=weights,
        selection='highest_full_connected_official_score_after_actual133_closure_and_actual134_source_admission',
        full_future_candidate_native_replays_and_QA45_required=True,
        actual_historical_native3_hook_proof_reused=str(hook), actual_new_native_hook_calls=0,
        existing_native_bank='nonflag_residual_EmpiricalBayes64_bank10_20261007',
        parameter_family_graph_field_unchanged='nonflag_CPU_ReverseBayes64_residual_CDF',
        new_native_fits=0, test_labels_read=False)
    plan.pop('full_future_candidate_native_replays_and_QA43_required', None)
    plan_path = A / 'nonflag_ReverseBayesFine40_plan_20261007.json'
    create(plan_path, plan)
    control_plan = dict(plan)
    control_plan.update(status='frozen_new_negative_Bayes_fine_full37_control_before_execution')
    control_path = A / 'nonflag_ReverseBayesFine40_control_plan_20261007.json'
    create(control_path, control_plan)
    original_control = A / 'verify_nonflag_residual_ReverseBayes37_transform_20261007.py'
    control_source = A / 'verify_nonflag_residual_ReverseBayesFine37_transform_20261007.py'
    control_text = original_control.read_text(encoding='utf8').replace('nonflag_residual_ReverseBayes37_transform_preflight_20261007',
            'nonflag_residual_ReverseBayesFine37_transform_preflight_20261007').replace('nonflag_ReverseBayes40_control_plan_20261007.json',
            'nonflag_ReverseBayesFine40_control_plan_20261007.json').replace('full132_candidate', 'full134_candidate')
    sources = [Path(__file__), A / 'nonflag_ReverseBayesFine40_round134_mapping_v1_20261008.py',
        A / 'prepare_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py', bank, hook,
        plan_path, control_path, original_control, write_new(control_source.name, control_text),
        A / 'actual_user_submission_deadline_and_priority_20261008.json']
    pairs = {
        'run_nonflag_SparseGram40_official_comparison_v1_20261007.py': 'run_nonflag_ReverseBayesFine40_official_comparison_v1_20261007.py',
        'run_nonflag_SparseGram40_admitted_comparison_v1_20261007.py': 'run_nonflag_ReverseBayesFine40_admitted_comparison_v1_20261007.py',
        'prepare_nonflag_SparseGram40_selected_candidate_v1_20261007.py': 'prepare_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py',
        'seal_nonflag_SparseGram40_selected_candidate_v1_20261007.py': 'seal_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py',
        'nonflag_residual_SparseGram_compatible_parent_20261007.py': 'nonflag_residual_ReverseBayesFine_compatible_parent_20261007.py',
        'predict_nonflag_residual_SparseGram_complete_scheme_20261007.py': 'predict_nonflag_residual_ReverseBayesFine_complete_scheme_20261007.py',
        'verify_nonflag_SparseGram40_prospective_routes_v2_20261007.py': 'verify_nonflag_ReverseBayesFine40_prospective_routes_v2_20261007.py',
        'verify_nonflag_SparseGram40_round133_sources_v1_20261007.py': 'verify_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py',
        'run_nonflag_SparseGram40_round133_full_registration_v1_20261007.py': 'run_nonflag_ReverseBayesFine40_round134_full_registration_v1_20261007.py',
        'publish_nonflag_SparseGram40_evidence_v1_20261007.py': 'publish_nonflag_ReverseBayesFine40_evidence_v1_20261007.py',
    }
    for old_name, new_name in pairs.items():
        old = A / old_name
        text = convert(old.read_text(encoding='utf8'))
        if old_name.startswith('run_nonflag_SparseGram40_official'):
            marker = "    assert len(cases)==plan['expected_scored_records']==40"
            assert text.count(marker) == 1
            text = text.replace(marker, "    assert plan['residual_sign']==-1\n    for case in cases:\n        if case['model'] is not None:case['residual_sign']=-1\n" + marker)
            marker = "        prepared=prepare(reference,dates,flags,valid,plan['universe'])"
            assert text.count(marker) == 1
            text = text.replace(marker, "        head={name:-np.asarray(values) for name,values in head.items()}\n" + marker)
        if old_name.startswith('prepare_nonflag_SparseGram40_selected'):
            marker = "        selected=transform(raw,reference,dates,flags,valid,residual,cfg['weight'],cfg['universe'])"
            assert text.count(marker) == 1
            text = text.replace(marker, "        assert cfg['residual_sign']==-1\n        residual*=cfg['residual_sign']\n" + marker)
        if old_name.startswith('verify_'):
            text = text.replace("'universe':plan['universe']}", "'universe':plan['universe'],'residual_sign':-1}")
            text = text.replace("'nonflag_CPU_EmpiricalBayes64_residual_CDF','nonflag_CPU_ReverseBayes64_residual_CDF','nonflag_CPU_Ridge_residual_CDF'",
                                "'nonflag_CPU_EmpiricalBayes64_residual_CDF','nonflag_CPU_SparseGram64_residual_CDF','nonflag_CPU_Ridge_residual_CDF'")
            text = text.replace("assert 'nonflag_CPU_EmpiricalBayes64_residual_CDF' not in graph and 'nonflag_CPU_ReverseBayes64_residual_CDF' not in graph and",
                                "assert 'nonflag_CPU_EmpiricalBayes64_residual_CDF' not in graph and 'nonflag_CPU_SparseGram64_residual_CDF' not in graph and")
            text = text.replace("assert graph['nonflag_CPU_ReverseBayes64_residual_CDF']['ordered_equal_mean_components']==names",
                                "assert graph['nonflag_CPU_ReverseBayes64_residual_CDF']['ordered_equal_mean_components']==names and graph['nonflag_CPU_ReverseBayes64_residual_CDF']['residual_sign']==-1")
            if old_name.startswith('verify_nonflag_SparseGram40_prospective'):
                marker = '    graph_controls=[];generated_hashes={};path_controls=[];issues=[]'
                assert text.count(marker) == 1
                text = text.replace(marker, "    future |= {A/'github_validation_sync_main_20261005/round133_receipt.json'}\n" + marker)
        if old_name.startswith('predict_'):
            text = text.replace('actual_nonflag_residual_SparseGram64_native_independent_and_CDF_replay',
                                'actual_nonflag_residual_ReverseBayes64_native_independent_and_CDF_replay')
        if old_name.startswith('publish_'):
            text = text.replace("['actual_full_QA_version'] == 43", "['actual_full_QA_version'] == 44")
            text = text.replace("A / 'nonflag_SparseGram64_actual_native3_full37_cold111_controls_20261007.json'",
                                "A / 'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json'")
            text = text.replace("A / 'nonflag_ReverseBayesFine40_science_route_preparation_v1_20261007.json',",
                "A / 'nonflag_ReverseBayesFine40_science_route_preparation_v1_20261007.json',\n        A / 'actual_user_submission_deadline_and_priority_20261008.json',")
        sources.extend([old, write_new(new_name, text)])
    create(A / 'nonflag_ReverseBayesFine40_science_route_preparation_v1_20261007.json', {
        'status': 'compiled_fresh_negative_Bayes_fine40_complete134_routes_before_actual_controls_or_scores',
        'input_sha256': {str(p): sha(p) for p in sources}, 'actual_native10_and_signed_hook3_reused': True,
        'actual_new_full37_controls_pending': True, 'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    from verify_nonflag_ReverseBayesFine40_prospective_routes_v2_20261007 import main as prospective
    prospective()


if __name__ == '__main__': main()
