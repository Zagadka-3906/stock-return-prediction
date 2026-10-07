"""Map only the new complete comparison routes; preserve the actual RFF native bank."""
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def mapping():
    m={
      'nonflag_Ridge40_round121_full_registration_v1':'nonflag_RFFRidge40_round122_full_registration_v1',
      'nonflag_HGB40_round120_full_registration_v4':'nonflag_Ridge40_round121_full_registration_v1',
      'nonflag_RFFRidge_actual_controls_main_after121':'RFFRidge122_actual_admission_history_main_after_full',
      'nonflag_RFFRidge_actual_hook3_and_full37_controls':'nonflag_reverse_RFF_actual_hook3_and_full37_controls',
      'nonflag_residual_RFFRidge37_transform_preflight_20261007':'nonflag_reverse_RFF37_transform_preflight_20261007',
      'nonflag_residual_RFFRidge_native_hook3_preflight_20261007':'nonflag_reverse_RFF_native_hook3_preflight_20261007',
      'nonflag_residual_HGB_CDF_transform_20261007':'nonflag_reverse_RFF_CDF_transform_20261007',
      'nonflag_residual_RFFRidge_native_stage_20261007':'nonflag_reverse_RFF_native_stage_20261007',
      'predict_nonflag_residual_RFFRidge_complete_scheme_20261007':'predict_nonflag_reverse_RFF_complete_scheme_20261007',
      'nonflag_residual_RFFRidge_native_replay_verification.json':'nonflag_reverse_RFF_native_replay_verification.json',
      'passed_actual_complete_parent_and_nonflag_RFFRidge_two_full_replays_independent_and_cold80':'passed_actual_complete_parent_and_nonflag_reverse_RFF_two_full_replays_independent_and_cold80',
      'passed_actual37_full5635800_nonflag_residual_RFFRidge':'passed_actual37_full5635800_nonflag_reverse_RFF',
      'passed_actual3_historical603_nonflag_RFFRidge':'passed_actual3_historical603_nonflag_reverse_RFF',
      'prepare_nonflag_RFFRidge40_complete_routes_20261007':'prepare_nonflag_reverse_RFF40_complete_routes_20261007',
      'nonflag_RFFRidge40_prospective_routes_v2':'nonflag_reverse_RFF40_prospective_routes_v1',
      'verify_nonflag_RFFRidge40_prospective_routes_v2':'verify_nonflag_reverse_RFF40_prospective_routes_v1',
      'nonflag_RFFRidge40_round122_source_admission_v2':'nonflag_reverse_RFF40_round123_source_admission_v1',
      '(112,120,121)':'(112,121,122)','(112, 120, 121)':'(112, 121, 122)',
      '(120,121)':'(121,122)',
      '((112,23),(120,31),(121,32))':'((112,23),(121,32),(122,33))',
      'round122':'round123','full122':'full123','actual122':'actual123','_r122':'_r123',
      'prospective122':'prospective123','qa33':'qa34','QA33':'QA34','qa_v33':'qa_v34',
      'NUMBER = 122':'NUMBER = 123','number == 122':'number == 123',
      'WAVES = (405,)':'WAVES = (406,)','wave=405':'wave=406','wave405_results':'wave406_results',
      "'waves': [405]":"'waves': [406]","'round': 122":"'round': 123",
      '(122, 33, 40)':'(123, 34, 40)',"namespace['snapshot'](122)":"namespace['snapshot'](123)",
      'actual_complete_QA_version=33':'actual_complete_QA_version=34',
      "actual_full_QA_version': 33":"actual_full_QA_version': 34",
      'publish(122,':'publish(123,','lossless(122)':'lossless(123)',
      '106_parent_percentile+weight*ordered_mean_raw_residual':'106_parent_percentile-weight*ordered_mean_raw_residual',
      'nonflag_RFFRidge40':'nonflag_reverse_RFF40'}
    for stem in ('run_nonflag_RFFRidge40_admitted_comparison','prepare_nonflag_RFFRidge40_round122_sources',
        'verify_nonflag_RFFRidge40_round122_sources','run_nonflag_RFFRidge40_round122_full_registration','publish_nonflag_RFFRidge40_evidence'):
        m[stem+'_v2_20261007']=stem.replace('nonflag_RFFRidge40','nonflag_reverse_RFF40').replace('round122','round123')+'_v1_20261007'
    return m
def convert(text):return substitute(text,mapping())
