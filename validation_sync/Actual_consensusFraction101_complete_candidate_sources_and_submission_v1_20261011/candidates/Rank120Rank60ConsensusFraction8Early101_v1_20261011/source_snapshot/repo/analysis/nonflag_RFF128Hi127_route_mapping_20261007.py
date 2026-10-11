"""Fresh stronger-L2 round127 routes; use the already verified generic128 codec."""
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def convert(text):
    mapping = {
        'nonflag_residual_RFF128_native_stage_20261007': 'nonflag_residual_RFF128_native_stage_20261007',
        'nonflag_residual_RFF128_codec_20261007': 'nonflag_residual_RFF128_codec_20261007',
        'nonflag_residual_RFF128_compatible_parent_20261007': 'nonflag_residual_RFF128_compatible_parent_20261007',
        'nonflag_CPU_RFF128_residual_CDF': 'nonflag_CPU_RFF128_residual_CDF',
        'nonflag_residual_RFF128Low_native_bank10_v2': 'nonflag_residual_RFF128Hi_native_bank10',
        'nonflag_RFF128Low_actual_hook6_and_full73_controls_v2': 'nonflag_RFF128Hi_actual_hook6_and_full73_controls',
        'nonflag_RFF12876_round125_full_registration_v1': 'nonflag_RFF128Low76_round126_full_registration_v1',
        'RFF128Low_history_batched_main_recovery': 'nonflag_RFF128Low76_round126_full_registration_v1',
        'RFF128_actual_history_github_20261007/receipt.json': 'github_validation_sync_main_20261005/round126_receipt.json',
        'nonflag_RFF128Low126_route_mapping_20261007': 'nonflag_RFF128Hi127_route_mapping_20261007',
        'nonflag_residual_RFF128Low': 'nonflag_residual_RFF128Hi',
        'nonflag_residual_rff128low': 'nonflag_residual_rff128hi',
        'nonflag_cpu_rff128low_': 'nonflag_cpu_rff128hi_',
        'nonflag_RFF128Low76': 'nonflag_RFF128Hi76',
        'remove_nonflag_RFF128Low': 'remove_nonflag_RFF128Hi',
        'nonflag_RFF128Low76_science_route_preparation_20261007.json': 'nonflag_RFF128Hi76_science_route_preparation_v1_20261007.json',
        '(112,121,125)': '(112,121,126)', '(112, 121, 125)': '(112, 121, 126)',
        '(121,125)': '(121,126)', '((112,23),(121,32),(125,36))': '((112,23),(121,32),(126,37))',
        'round126': 'round127', 'full126': 'full127', 'actual126': 'actual127', '_r126': '_r127',
        'prospective126': 'prospective127', 'qa37': 'qa38', 'QA37': 'QA38', 'qa_v37': 'qa_v38',
        'NUMBER = 126': 'NUMBER = 127', 'number == 126': 'number == 127',
        'WAVES = (409,)': 'WAVES = (410,)', 'wave=409': 'wave=410', 'wave409_results': 'wave410_results',
        "'waves': [409]": "'waves': [410]", "'round': 126": "'round': 127",
        '(126, 37, 76)': '(127, 38, 76)', "namespace['snapshot'](126)": "namespace['snapshot'](127)",
        'actual_complete_QA_version=37': 'actual_complete_QA_version=38',
        "actual_full_QA_version': 37": "actual_full_QA_version': 38",
        'publish(126,': 'publish(127,', 'lossless(126)': 'lossless(127)',
        '112、121、125合格锚点': '112、121、126合格锚点',
        'passed_actual76_nonflag_RFFRidge_full_official_comparisons': 'passed_actual76_nonflag_RFF128Hi_full_official_comparisons',
        'passed_actual6_historical603_nonflag_RFF128Low_native_reload_decoder_CDF_and_whole_day_prefix_controls': 'passed_actual6_historical603_nonflag_RFF128Hi_native_reload_decoder_CDF_and_whole_day_prefix_controls',
        'info[\'parameters\'][\'alpha_per_training_row\']==.0025': 'info[\'parameters\'][\'alpha_per_training_row\']==.04',
        "info['training_rows']*.0025": "info['training_rows']*.04",
    }
    result = substitute(text, mapping)
    result = result.replace("'nonflag_cpu_rffridge_','nonflag_cpu_rff128_','nonflag_cpu_rff128hi_'",
                            "'nonflag_cpu_rffridge_','nonflag_cpu_rff128_','nonflag_cpu_rff128low_','nonflag_cpu_rff128hi_'")
    result = result.replace("'nonflag_residual_rffridge','nonflag_residual_rff128','nonflag_residual_rff128hi'",
                            "'nonflag_residual_rffridge','nonflag_residual_rff128','nonflag_residual_rff128low','nonflag_residual_rff128hi'")
    return result
