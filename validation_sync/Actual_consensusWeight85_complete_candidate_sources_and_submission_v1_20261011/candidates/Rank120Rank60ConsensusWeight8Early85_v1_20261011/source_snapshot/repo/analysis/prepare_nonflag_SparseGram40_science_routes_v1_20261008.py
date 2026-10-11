"""Build fresh sparse routes using existing measured native controls and exact prospective graphs."""
from pathlib import Path
import ast
import json
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from nonflag_SparseGram40_round133_mapping_v1_20261008 import convert


def write_new(name, text):
    path = A / name
    compile(text, str(path), 'exec')
    assert not path.exists(), path
    path.write_text(text, encoding='utf8', newline='\n')
    return path


def main():
    bank = A / 'nonflag_residual_SparseGram64_bank10_20261007/verification.json'
    assert read(bank)['actual_native_fits'] == 10
    full = A / 'nonflag_residual_SparseGram37_transform_preflight_20261007/verification.json'
    assert read(full)['status'] == 'passed_actual37_full5635800_nonflag_SparseGram64_independent_CDF_and111_cold_controls'
    native = A / 'nonflag_residual_SparseGram64_native_hook3_preflight_20261007/verification.json'
    assert len(read(native)['records']) == 3
    originals = {
        'run_nonflag_EmpiricalBayes40_official_comparison_v3_20261007.py': 'run_nonflag_SparseGram40_official_comparison_v1_20261007.py',
        'prepare_nonflag_EmpiricalBayes40_selected_candidate_v3_20261007.py': 'prepare_nonflag_SparseGram40_selected_candidate_v1_20261007.py',
        'seal_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py': 'seal_nonflag_SparseGram40_selected_candidate_v1_20261007.py',
        'nonflag_residual_EmpiricalBayes_compatible_parent_20261007.py': 'nonflag_residual_SparseGram_compatible_parent_20261007.py',
        'predict_nonflag_residual_EmpiricalBayes_complete_scheme_20261007.py': 'predict_nonflag_residual_SparseGram_complete_scheme_20261007.py',
        'verify_nonflag_EmpiricalBayes40_prospective_routes_v2_20261007.py': 'verify_nonflag_SparseGram40_prospective_routes_v2_20261007.py',
        'verify_nonflag_EmpiricalBayes40_round130_sources_v1_20261007.py': 'verify_nonflag_SparseGram40_round133_sources_v1_20261007.py',
        'run_nonflag_EmpiricalBayes40_round130_full_registration_v1_20261007.py': 'run_nonflag_SparseGram40_round133_full_registration_v1_20261007.py',
        'run_nonflag_EmpiricalBayes40_admitted_comparison_v1_20261007.py': 'run_nonflag_SparseGram40_admitted_comparison_v1_20261007.py',
    }
    sources = [Path(__file__), A / 'nonflag_SparseGram40_round133_mapping_v1_20261008.py',
               A / 'prepare_nonflag_SparseGram40_round133_sources_v1_20261007.py', bank, full, native,
               A / 'nonflag_sparse_Gram64_codec_20261007.py']
    for old_name, new_name in originals.items():
        old = A / old_name
        text = convert(old.read_text(encoding='utf8'))
        text = text.replace('passed_actual37_full5635800_nonflag_residual_Ridge_independent_CDF_and111_cold_controls',
                            'passed_actual37_full5635800_nonflag_SparseGram64_independent_CDF_and111_cold_controls')
        text = text.replace('passed_actual40_nonflag_Ridge_full_official_comparisons', 'passed_actual40_nonflag_SparseGram64_full_official_comparisons')
        if old_name.startswith('nonflag_residual_'):
            needle = "    value.pop('nonflag_CPU_SparseGram64_residual_CDF',None)"
            assert text.count(needle) == 1
            text = text.replace(needle, needle + "\n    value.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)\n    value.pop('nonflag_CPU_ReverseBayes64_residual_CDF',None)")
        if old_name.startswith('verify_'):
            text = text.replace("'nonflag_CPU_HGB_residual_CDF':{'old':'remove'}", "'nonflag_CPU_HGB_residual_CDF':{'old':'remove'},'nonflag_CPU_EmpiricalBayes64_residual_CDF':{'old':'remove'},'nonflag_CPU_ReverseBayes64_residual_CDF':{'old':'remove'}")
            text = text.replace("'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}", "'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_EmpiricalBayes64_residual_CDF':{'old':'remove'},'nonflag_CPU_ReverseBayes64_residual_CDF':{'old':'remove'}")
            text = text.replace("'nonflag_CPU_HGB_residual_CDF','nonflag_CPU_Ridge_residual_CDF'", "'nonflag_CPU_HGB_residual_CDF','nonflag_CPU_EmpiricalBayes64_residual_CDF','nonflag_CPU_ReverseBayes64_residual_CDF','nonflag_CPU_Ridge_residual_CDF'")
        if old_name.startswith('verify_nonflag_EmpiricalBayes40_round'):
            text = text.replace("'nonflag_residual_SparseGram64_native_bank10','nonflag_residual_SparseGram37_transform_preflight'", "'nonflag_residual_SparseGram64_native_bank10','nonflag_SparseGram64_actual_native3_full37_controls'")
            text = text.replace("assert 'nonflag_CPU_HGB_residual_CDF' not in graph and", "assert 'nonflag_CPU_EmpiricalBayes64_residual_CDF' not in graph and 'nonflag_CPU_ReverseBayes64_residual_CDF' not in graph and 'nonflag_CPU_HGB_residual_CDF' not in graph and")
            text = text.replace("'nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_sparse_gram64_'", "'nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_empirical_bayes64_','nonflag_cpu_reverse_bayes64_','nonflag_cpu_sparse_gram64_'")
        if old_name.startswith('run_nonflag_EmpiricalBayes40_round'):
            text = text.replace("'nonflag_ReverseBayes40_round132_full_registration_v1'", "'nonflag_ReverseBayes40_round132_full_registration_v1'")
            text = text.replace('反向自适应收缩融合', '稀疏L1和Elastic残差融合')
            text = text.replace('非涨停残差Ridge幅度加密', '非涨停稀疏L1和Elastic残差融合')
            text = text.replace("if __name__=='__main__':main()", "if __name__=='__main__':\n    from file_backed_hidden_git_runtime_20261007 import installed\n    with installed(A/'run_nonflag_SparseGram40_round133_full_registration_v1_file_IO_20261008'):main()")
        sources.extend([old, write_new(new_name, text)])
    plan = read(A / 'nonflag_EmpiricalBayes40_plan_20261007.json')
    heads = list(read(A / 'nonflag_residual_SparseGram6410_plan_20261007.json')['configurations'])
    plan.update(status='frozen_sparse_Gram40_before_actual_official_scoring', at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        round=133, wave=416, after_round=132, qualified_anchor_rounds=[112, 131, 132],
        single_native_heads=heads, ensembles={'nonflag_residual_sparseGram64_equal_mean_two': heads},
        existing_native_bank='nonflag_residual_SparseGram64_bank10_20261007', new_branch='nonflag_CPU_SparseGram64_residual_CDF',
        selection='highest_full_connected_official_score_after_actual132_closure_and_actual133_source_admission',
        training_solver_recipe='fixed8192_centered_Gram64_cyclic_ElasticNet_objective_v1',
        full_future_candidate_native_replays_and_QA44_required=True)
    plan.pop('full_future_candidate_native_replays_and_QA41_required', None)
    path = A / 'nonflag_SparseGram40_plan_20261007.json'
    create(path, plan)
    sources.append(path)
    create(A / 'nonflag_SparseGram40_science_route_preparation_v1_20261007.json', {
        'status': 'compiled_sparse_Gram40_complete133_science_routes_before_quality_scores',
        'input_sha256': {str(p): sha(p) for p in sources}, 'new_quality_scores': 0, 'test_labels_read': False})
    from verify_nonflag_SparseGram40_prospective_routes_v2_20261007 import main as prospective
    prospective()


if __name__ == '__main__': main()
