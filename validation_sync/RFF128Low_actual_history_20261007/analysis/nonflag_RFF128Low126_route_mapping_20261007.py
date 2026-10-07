"""Fresh round126 routes; generic128 native decoder and ancestor sources stay unchanged."""
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def convert(text):
    mapping={
        'nonflag_residual_RFF128_native_stage_20261007':'nonflag_residual_RFF128_native_stage_20261007',
        'nonflag_residual_RFF128_codec_20261007':'nonflag_residual_RFF128_codec_20261007',
        'nonflag_residual_RFF128_compatible_parent_20261007':'nonflag_residual_RFF128_compatible_parent_20261007',
        'nonflag_CPU_RFF128_residual_CDF':'nonflag_CPU_RFF128_residual_CDF',
        'nonflag_residual_RFF128_native_bank10':'nonflag_residual_RFF128Low_native_bank10_v2',
        'nonflag_RFF128_actual_hook6_and_full73_controls':'nonflag_RFF128Low_actual_hook6_and_full73_controls_v2',
        'nonflag_reverse_Ridge40_round124_full_registration_v1':'nonflag_RFF12876_round125_full_registration_v1',
        'RFF128_actual_history_main_after124':'RFF128Low_actual_history_main_after125',
        'nonflag_RFF128125_route_mapping_20261007':'nonflag_RFF128Low126_route_mapping_20261007',
        'nonflag_residual_RFF128':'nonflag_residual_RFF128Low',
        'nonflag_residual_rff128':'nonflag_residual_rff128low',
        'nonflag_cpu_rff128_':'nonflag_cpu_rff128low_',
        'nonflag_RFF12876':'nonflag_RFF128Low76',
        'remove_nonflag_RFF128':'remove_nonflag_RFF128Low',
        'passed_actual73_full5635800_nonflag_residual_RFF128':'passed_actual73_full5635800_nonflag_residual_RFF128Low',
        'passed_actual6_historical603_nonflag_RFF128':'passed_actual6_historical603_nonflag_RFF128Low',
        '(112,121,124)':'(112,121,125)', '(112, 121, 124)':'(112, 121, 125)',
        '(121,124)':'(121,125)', '((112,23),(121,32),(124,35))':'((112,23),(121,32),(125,36))',
        'round125':'round126','full125':'full126','actual125':'actual126','_r125':'_r126',
        'prospective125':'prospective126','qa36':'qa37','QA36':'QA37','qa_v36':'qa_v37',
        'NUMBER = 125':'NUMBER = 126','number == 125':'number == 126',
        'WAVES = (408,)':'WAVES = (409,)','wave=408':'wave=409','wave408_results':'wave409_results',
        "'waves': [408]":"'waves': [409]","'round': 125":"'round': 126",
        '(125, 36, 76)':'(126, 37, 76)',"namespace['snapshot'](125)":"namespace['snapshot'](126)",
        'actual_complete_QA_version=36':'actual_complete_QA_version=37',
        "actual_full_QA_version': 36":"actual_full_QA_version': 37",
        'publish(125,':'publish(126,','lossless(125)':'lossless(126)',
        '112、121、124合格锚点':'112、121、125合格锚点',
    }
    text=substitute(text,mapping)
    # All inactive nonflag model families must be excluded from active native counts.
    text=text.replace("'nonflag_cpu_rffridge_','nonflag_cpu_rff128low_'",
                      "'nonflag_cpu_rffridge_','nonflag_cpu_rff128_','nonflag_cpu_rff128low_'")
    text=text.replace("'nonflag_residual_rffridge','nonflag_residual_rff128low'",
                      "'nonflag_residual_rffridge','nonflag_residual_rff128','nonflag_residual_rff128low'")
    return text
