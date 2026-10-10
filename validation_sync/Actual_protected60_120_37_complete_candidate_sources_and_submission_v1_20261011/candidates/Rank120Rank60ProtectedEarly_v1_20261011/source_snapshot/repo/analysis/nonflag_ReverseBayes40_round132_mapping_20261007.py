"""Signed Bayes132 routes reuse the original immutable Bayesian bank and negative controls."""
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def convert(text):
    protected=[
      'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json','nonflag_EmpiricalBayes40_full_control_recovery_v3_20261007.json',
      'nonflag_EmpiricalBayes40_partial_preparation_failure_20261007.json','prepare_nonflag_EmpiricalBayes40_complete_routes_20261007.py',
      'prepare_nonflag_EmpiricalBayes40_complete_routes_v2_20261007.py','run_nonflag_EmpiricalBayes40_official_comparison_v2_20261007.py',
      'run_nonflag_EmpiricalBayes40_official_comparison_v3_20261007.py','prepare_nonflag_EmpiricalBayes40_selected_candidate_v2_20261007.py',
      'run_nonflag_EmpiricalBayes40_admitted_comparison_v4_20261007.py',
      'prepare_nonflag_EmpiricalBayes40_selected_candidate_v3_20261007.py','publish_nonflag_EmpiricalBayes40_evidence_v2_20261007.py',
      'publish_nonflag_EmpiricalBayes40_evidence_v3_20261007.py','run_nonflag_EmpiricalBayes40_actual_controls_v2_20261007.py',
      'run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_v2_20261007.py',
      'nonflag_EmpiricalBayes40_prospective_routes_v2_20261007.json','nonflag_EmpiricalBayes130_parent128_gate_recovery_v4_20261007.json',
      'recover_nonflag_EmpiricalBayes130_parent128_gate_v4_20261007.py','queue_nonflag_EmpiricalBayes130_after_actual129_v4_20261007.py']
    m={p:p for p in protected}
    m.update({
      'nonflag_RidgeFine52_round128_full_registration_v2':'nonflag_EmpiricalBayes40_round130_full_registration_v1',
      'nonflag_RidgeFine52_round128_full_registration_v1':'nonflag_EmpiricalBayes40_round130_full_registration_v1',
      'nonflag_RFF128StreamMid76_round129_full_registration_v1':'nonflag_RidgeMicro40_round131_full_registration_v1',
      'nonflag_residual_EmpiricalBayes37_transform_preflight_v3':'nonflag_ReverseBayes40_actual_native3_full37_controls',
      'nonflag_residual_EmpiricalBayes37_transform_preflight_20261007':'nonflag_residual_ReverseBayes37_transform_preflight_20261007',
      'verify_nonflag_residual_EmpiricalBayes37_transform_v3_20261007.py':'verify_nonflag_residual_ReverseBayes37_transform_20261007.py',
      'verify_nonflag_residual_EmpiricalBayes37_transform_20261007.py':'verify_nonflag_residual_ReverseBayes37_transform_20261007.py',
      'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007':'nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007',
      'nonflag_residual_EmpiricalBayes64_native_stage_20261007':'nonflag_residual_ReverseBayes64_native_stage_20261007',
      'nonflag_residual_EmpiricalBayes64_native_replay_verification.json':'nonflag_residual_ReverseBayes64_native_replay_verification.json',
      'nonflag_residual_EmpiricalBayes_compatible_parent':'nonflag_residual_ReverseBayes_compatible_parent',
      'predict_nonflag_residual_EmpiricalBayes_complete_scheme':'predict_nonflag_residual_ReverseBayes_complete_scheme',
      'run_nonflag_EmpiricalBayes40_official_comparison_v4_20261007.py':'run_nonflag_ReverseBayes40_official_comparison_v1_20261007.py',
      'run_nonflag_EmpiricalBayes40_admitted_comparison_v5_20261007.py':'run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py',
      'prepare_nonflag_EmpiricalBayes40_selected_candidate_v4_20261007.py':'prepare_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py',
      'publish_nonflag_EmpiricalBayes40_evidence_v4_20261007.py':'publish_nonflag_ReverseBayes40_evidence_v1_20261007.py',
      'verify_nonflag_EmpiricalBayes40_round130_sources_v4_20261007.py':'verify_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',
      'nonflag_EmpiricalBayes40_round130_source_admission_v4':'nonflag_ReverseBayes40_round132_source_admission_v1',
      'nonflag_EmpiricalBayes40_prospective_routes_v3_20261007':'nonflag_ReverseBayes40_prospective_routes_v1_20261007',
      'nonflag_EmpiricalBayes40':'nonflag_ReverseBayes40',
      'nonflag_CPU_EmpiricalBayes64_residual_CDF':'nonflag_CPU_ReverseBayes64_residual_CDF',
      'nonflag_cpu_empirical_bayes64_':'nonflag_cpu_reverse_bayes64_',
      'remove_nonflag_EmpiricalBayes64':'remove_nonflag_ReverseBayes64',
      'passed_actual3_historical603_nonflag_EmpiricalBayes64':'passed_actual3_historical603_nonflag_ReverseBayes64',
      'passed_actual37_full5635800_nonflag_residual_Ridge_independent_CDF_and111_cold_controls':'passed_actual37_full5635800_nonflag_ReverseBayes64_independent_CDF_and111_cold_controls',
      'passed_actual40_nonflag_Ridge_full_official_comparisons':'passed_actual40_nonflag_ReverseBayes64_full_official_comparisons',
      'passed_actual_complete_parent_and_nonflag_EmpiricalBayes64':'passed_actual_complete_parent_and_nonflag_ReverseBayes64',
      '(112,128,129)':'(112,130,131)','(112, 128, 129)':'(112, 130, 131)',
      '((112,23),(128,39),(129,40))':'((112,23),(130,41),(131,42))',
      'round130':'round132','full130':'full132','actual130':'actual132','prospective130':'prospective132','_r130':'_r132',
      'qa41':'qa43','QA41':'QA43','qa_v41':'qa_v43','NUMBER = 130':'NUMBER = 132','number == 130':'number == 132',
      'WAVES = (413,)':'WAVES = (415,)','wave=413':'wave=415','wave413_results':'wave415_results',
      "'waves': [413]":"'waves': [415]","'round':130":"'round':132","'round': 130":"'round': 132",
      '(130, 41, 40)':'(132, 43, 40)',"namespace['snapshot'](130)":"namespace['snapshot'](132)",
      'actual_complete_QA_version=41':'actual_complete_QA_version=43',"actual_full_QA_version': 41":"actual_full_QA_version': 43",
      'publish(130,':'publish(132,','lossless(130)':'lossless(132)',
      '106_parent_percentile+weight*ordered_mean_raw_residual':'106_parent_percentile+weight*residual_sign*ordered_mean_raw_residual',
      '完整父方案的非涨停残差Ridge补充':'完整父方案的反向自适应收缩融合',
      '预定52项完整官方比较：三个合格锚点、48项非涨停残差Ridge和一个消融':'预定40项完整官方比较：三个合格锚点、36项反向自适应收缩融合和一个消融',
    })
    result=substitute(text,m)
    needle="graph.pop('nonflag_CPU_HGB_residual_CDF',None)"
    if needle in result:
        indent='            ' if '        if measured' in result else '        '
        result=result.replace(needle,needle+'\n'+indent+"graph.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)")
    result=result.replace("value.pop('nonflag_CPU_HGB_residual_CDF',None)", "value.pop('nonflag_CPU_HGB_residual_CDF',None)\n    value.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)")
    result=result.replace("'nonflag_cpu_reverse_bayes64_'", "'nonflag_cpu_empirical_bayes64_','nonflag_cpu_reverse_bayes64_'") if 'if not key.startswith' in result else result
    result=result.replace("('nonflag_residual_hgb','nonflag_residual_ridge'", "('nonflag_residual_hgb','nonflag_residual_empirical_bayes64','nonflag_residual_ridge'")
    return result
