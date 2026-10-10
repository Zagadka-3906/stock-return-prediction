"""Map the new 76-case round while preserving the actual completed ancestor routes."""
import re
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def mapping():
    m={
      'verify_nonflag_residual_RFFRidge37_transform_20261007':'verify_nonflag_residual_RFF12873_transform_20261007',
      'nonflag_Ridge40_round121_full_registration_v1':'nonflag_reverse_Ridge40_round124_full_registration_v1',
      'nonflag_HGB40_round120_full_registration_v4':'nonflag_Ridge40_round121_full_registration_v1',
      'nonflag_residual_RFFRidge_native_bank10_v2':'nonflag_residual_RFF128_native_bank10',
      'nonflag_RFFRidge_actual_controls_main_after121':'RFF128_actual_history_main_after124',
      'nonflag_RFFRidge_actual_hook3_and_full37_controls':'nonflag_RFF128_actual_hook6_and_full73_controls',
      'nonflag_residual_RFFRidge37_transform_preflight':'nonflag_residual_RFF12873_transform_preflight',
      'nonflag_residual_RFFRidge_native_hook3_preflight':'nonflag_residual_RFF128_native_hook6_preflight',
      'nonflag_RFFRidge40_prospective_routes_v2':'nonflag_RFF12876_prospective_routes_v1',
      'verify_nonflag_RFFRidge40_prospective_routes_v2':'verify_nonflag_RFF12876_prospective_routes_v1',
      'nonflag_RFFRidge40_round122_source_admission_v2':'nonflag_RFF12876_round125_source_admission_v1',
      'nonflag_RFFRidge122_route_mapping_20261007':'nonflag_RFF128125_route_mapping_20261007',
      'prepare_nonflag_RFFRidge40_complete_routes':'prepare_nonflag_RFF12876_complete_routes',
      'nonflag_residual_RFFRidge10_actual_controls_github':'RFF128_actual_history_github',
      'passed_actual37_full5635800_nonflag_residual_RFFRidge_independent_CDF_and111_cold_controls':'passed_actual73_full5635800_nonflag_residual_RFF128_independent_CDF_and219_cold_controls',
      'passed_actual3_historical603_nonflag_RFFRidge':'passed_actual6_historical603_nonflag_RFF128',
      'passed_actual37_controls_and24_prospective122':'passed_actual73_controls_and24_prospective125',
      'nonflag_residual_RFFRidge':'nonflag_residual_RFF128','nonflag_CPU_RFFRidge':'nonflag_CPU_RFF128',
      'nonflag_cpu_rffridge_':'nonflag_cpu_rff128_','nonflag_residual_rffridge':'nonflag_residual_rff128',
      'remove_nonflag_RFFRidge':'remove_nonflag_RFF128','nonflag_RFFRidge40':'nonflag_RFF12876',
      '(112,120,121)':'(112,121,124)','(112, 120, 121)':'(112, 121, 124)','(120,121)':'(121,124)',
      '((112,23),(120,31),(121,32))':'((112,23),(121,32),(124,35))',
      'round122':'round125','full122':'full125','actual122':'actual125','_r122':'_r125',
      'prospective122':'prospective125','qa33':'qa36','QA33':'QA36','qa_v33':'qa_v36',
      'NUMBER = 122':'NUMBER = 125','number == 122':'number == 125',
      'WAVES = (405,)':'WAVES = (408,)','wave=405':'wave=408','wave405_results':'wave408_results',
      "'waves': [405]":"'waves': [408]","'round': 122":"'round': 125",
      '(122, 33, 40)':'(125, 36, 76)',"namespace['snapshot'](122)":"namespace['snapshot'](125)",
      'actual_complete_QA_version=33':'actual_complete_QA_version=36',"actual_full_QA_version': 33":"actual_full_QA_version': 36",
      'publish(122,':'publish(125,','lossless(122)':'lossless(125)',
      '106_parent_percentile+weight*ordered_mean_raw_residual':'106_parent_percentile+residual_sign*weight*ordered_mean_raw_residual',
      'actual_full_transform_controls': 'actual_full_transform_controls'}
    for stem in ('run_nonflag_RFFRidge40_admitted_comparison','prepare_nonflag_RFFRidge40_round122_sources',
      'verify_nonflag_RFFRidge40_round122_sources','run_nonflag_RFFRidge40_round122_full_registration','publish_nonflag_RFFRidge40_evidence'):
        m[stem+'_v2_20261007']=stem.replace('nonflag_RFFRidge40','nonflag_RFF12876').replace('round122','round125')+'_v1_20261007'
    return m
def convert(text):
    text=substitute(text,mapping())
    text=re.sub(r'\b40\b','76',text)
    text=text.replace('actual40','actual76').replace('actual37','actual73').replace('all37','all73')
    return text
