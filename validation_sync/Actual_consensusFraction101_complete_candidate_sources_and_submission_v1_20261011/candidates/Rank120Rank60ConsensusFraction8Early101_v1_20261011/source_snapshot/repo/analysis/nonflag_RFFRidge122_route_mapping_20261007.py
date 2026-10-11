"""Simultaneous substitutions preserve completed parent references in fresh round122 routes."""
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def mapping():
    stems=['run_nonflag_Ridge40_admitted_comparison','prepare_nonflag_Ridge40_round121_sources',
        'verify_nonflag_Ridge40_round121_sources','run_nonflag_Ridge40_round121_full_registration','publish_nonflag_Ridge40_evidence']
    m={stem+'_v2_20261007':stem.replace('nonflag_Ridge40','nonflag_RFFRidge40').replace('round121','round122')+'_v1_20261007' for stem in stems}
    m.update({
        'nonflag_residual_Ridge_native_bank10':'nonflag_residual_RFFRidge_native_bank10_v2',
        'nonflag_residual_Ridge37_transform_preflight_20261007':'nonflag_residual_RFFRidge37_transform_preflight_20261007',
        'nonflag_residual_Ridge37_transform_preflight':'nonflag_RFFRidge_actual_hook3_and_full37_controls',
        'nonflag_residual_Ridge_actual_hooks_and_main_after120':'nonflag_RFFRidge_actual_controls_main_after121',
        'quantile_HGB88_round119_full_registration_v6':'nonflag_HGB40_round120_full_registration_v4',
        'nonflag_HGB40_round120_full_registration_v4':'nonflag_Ridge40_round121_full_registration_v1',
        '(112,119,120)':'(112,120,121)','(112, 119, 120)':'(112, 120, 121)',
        '((112,23),(119,30),(120,31))':'((112,23),(120,31),(121,32))',
        'nonflag_Ridge40_prospective_routes_v2':'nonflag_RFFRidge40_prospective_routes_v1',
        'nonflag_Ridge40_science_route_preparation':'nonflag_RFFRidge40_science_route_preparation',
        'prepare_nonflag_Ridge40_science_routes':'prepare_nonflag_RFFRidge40_complete_routes',
        'prepare_nonflag_Ridge40_admission_and_publication':'prepare_nonflag_RFFRidge40_complete_routes',
        'nonflag_Ridge40_unadmitted_plan_metadata_correction_20261007.json':'RFFRidge_zero_fit_admission_label_correction_20261007.json',
        'nonflag_Ridge40':'nonflag_RFFRidge40','nonflag_residual_Ridge':'nonflag_residual_RFFRidge',
        'nonflag_CPU_Ridge':'nonflag_CPU_RFFRidge','nonflag_cpu_ridge_':'nonflag_cpu_rffridge_',
        'nonflag_Ridge':'nonflag_RFFRidge','independent_linear_state':'independent_random_fourier_linear_state',
        'round121':'round122','full121':'full122','actual121':'actual122','_r121':'_r122',
        'qa32':'qa33','QA32':'QA33','qa_v32':'qa_v33',
        'NUMBER = 121':'NUMBER = 122','number == 121':'number == 122',
        'WAVES = (404,)':'WAVES = (405,)','wave=404':'wave=405','wave404_results':'wave405_results',
        "'waves': [404]":"'waves': [405]","'round': 121":"'round': 122",
        '(121, 32, 40)':'(122, 33, 40)',"namespace['snapshot'](121)":"namespace['snapshot'](122)",
        'actual_complete_QA_version=32':'actual_complete_QA_version=33',"'actual_full_QA_version': 32":"'actual_full_QA_version': 33",
        'publish(121,':'publish(122,','lossless(121)':'lossless(122)',
        'prospective121':'prospective122','nonflag_residual_ridge':'nonflag_residual_rffridge'})
    return m

def convert(text):
    return substitute(text,mapping())
