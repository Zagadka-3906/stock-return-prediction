"""Explicit round133 sparse-model identities and complete old-nonflag branch replacement."""
import re
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def convert(text):
    mapping = {
        'nonflag_residual_EmpiricalBayes37_transform_preflight_v3': 'nonflag_SparseGram64_actual_native3_full37_controls',
        'nonflag_RidgeFine52_round128_full_registration_v1': 'round131_preserved_QA42_main_publication_recovery_v3_20261008',
        'nonflag_RFF128StreamMid76_round129_full_registration_v1': 'nonflag_ReverseBayes40_round132_full_registration_v1',
        'nonflag_EmpiricalBayes40': 'nonflag_SparseGram40',
        'nonflag_residual_EmpiricalBayes37': 'nonflag_residual_SparseGram37',
        'nonflag_residual_EmpiricalBayes64': 'nonflag_residual_SparseGram64',
        'nonflag_residual_EmpiricalBayes_compatible_parent': 'nonflag_residual_SparseGram_compatible_parent',
        'predict_nonflag_residual_EmpiricalBayes_complete_scheme': 'predict_nonflag_residual_SparseGram_complete_scheme',
        'nonflag_empirical_Bayes64_codec': 'nonflag_sparse_Gram64_codec',
        'nonflag_CPU_EmpiricalBayes64_residual_CDF': 'nonflag_CPU_SparseGram64_residual_CDF',
        'nonflag_cpu_empirical_bayes64_': 'nonflag_cpu_sparse_gram64_',
        'remove_nonflag_EmpiricalBayes64': 'remove_nonflag_SparseGram64',
        'passed_actual_complete_parent_and_nonflag_EmpiricalBayes64': 'passed_actual_complete_parent_and_nonflag_SparseGram64',
        'passed_actual3_historical603_nonflag_EmpiricalBayes64': 'passed_actual3_historical603_nonflag_SparseGram64',
        'nonflag_residual_empirical_bayes64_equal_mean_two': 'nonflag_residual_sparseGram64_equal_mean_two',
        'nonflag_residual_empirical_bayes64_scalar': 'nonflag_residual_sparseGram64_L1',
        'nonflag_residual_empirical_bayes64_diagonal': 'nonflag_residual_sparseGram64_Elastic',
        "'empirical_bayes_centered_Gram64'": "'own_centered_Gram64_cyclic_coordinate_descent'",
        '(112,128,129)': '(112,131,132)', '(112, 128, 129)': '(112, 131, 132)',
        '((112,23),(128,39),(129,40))': '((112,23),(131,42),(132,43))',
        'round128_receipt.json': 'round131_receipt.json', 'round129_receipt.json': 'round132_receipt.json',
        'round130': 'round133', 'full130': 'full133', 'actual130': 'actual133',
        'prospective130': 'prospective133', '_r130': '_r133',
        'qa41': 'qa44', 'QA41': 'QA44', 'qa_v41': 'qa_v44',
        'NUMBER = 130': 'NUMBER = 133', 'number == 130': 'number == 133',
        'WAVES = (413,)': 'WAVES = (416,)', 'wave=413': 'wave=416',
        'wave413_results': 'wave416_results', "'waves': [413]": "'waves': [416]",
        "'round':130": "'round':133", "'round': 130": "'round': 133",
        '(130, 41, 40)': '(133, 44, 40)', "namespace['snapshot'](130)": "namespace['snapshot'](133)",
        'actual_complete_QA_version=41': 'actual_complete_QA_version=44',
        "actual_full_QA_version': 41": "actual_full_QA_version': 44",
        'publish(130,': 'publish(133,', 'lossless(130)': 'lossless(133)',
        'nonflag_SparseGram40_round130_mapping_20261007': 'nonflag_SparseGram40_round133_mapping_v1_20261008',
        'nonflag_EmpiricalBayes40_round130_mapping_20261007': 'nonflag_SparseGram40_round133_mapping_v1_20261008',
        'main_publisher_v7/native_launch.json': 'main_publisher_v8_20261008/native_launch.json',
    }
    result = substitute(text, mapping)
    # Every selected new graph must remove the previous positive and negative Bayesian stages.
    result = re.sub(r"(?m)^(\s*)graph\.pop\('nonflag_CPU_HGB_residual_CDF',None\)$",
        lambda m: m.group(0) + '\n' + m.group(1) + "graph.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)" +
                  '\n' + m.group(1) + "graph.pop('nonflag_CPU_ReverseBayes64_residual_CDF',None)", result)
    result = result.replace("'nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_sparse_gram64_'",
        "'nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_empirical_bayes64_','nonflag_cpu_reverse_bayes64_','nonflag_cpu_sparse_gram64_'")
    result = result.replace("'nonflag_residual_hgb','nonflag_residual_ridge','nonflag_residual_rffridge','nonflag_residual_rff128'",
        "'nonflag_residual_hgb','nonflag_residual_ridge','nonflag_residual_empirical_bayes64','nonflag_residual_sparseGram64','nonflag_residual_rffridge','nonflag_residual_rff128'")
    return result
