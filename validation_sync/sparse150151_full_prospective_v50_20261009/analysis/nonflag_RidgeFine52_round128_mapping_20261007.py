"""Fresh fine-amplitude Ridge routes after complete127, retaining generic linear codecs."""
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def finalize(text):
    changes={
      'passed_actual49_controls_and24_prospective128':'passed_actual49_controls_and24_prospective128',
      '(37 if phase==\'controls\' else 40)':'(49 if phase==\'controls\' else 52)',
      "'actual_full_control_cases':49":"'actual_full_control_cases':49",
      "'actual_cold_prefix_cases':147":"'actual_cold_prefix_cases':147",
      "len(pilot['records']) == 52":"len(pilot['records']) == 52",
      "'expected_scored_records': 52":"'expected_scored_records': 52",
      "'existing_actual_official_records': 52":"'existing_actual_official_records': 52",
      "manifest['scored_records'] == full['scored_records'] == 52":"manifest['scored_records'] == full['scored_records'] == 52",
      "'scored_records': 52":"'scored_records': 52",
      "'original_official_pilot_records_registered': 52":"'original_official_pilot_records_registered': 52",
      "record['expected_scored_records'] == 52":"record['expected_scored_records'] == 52",
      "len(record['ranking']) == 52":"len(record['ranking']) == 52",
      "'existing_official_scores_registered':52":"'existing_official_scores_registered':52",
      'nonflag_RidgeFine52_round128':'nonflag_RidgeFine52_round128',
      'actual40_native_bank_source':'actual40_native_bank_source',
      '各16个新幅度':'各16个新幅度','49全量':'49全量','完整128候选':'完整128候选',
      '112、121、127合格锚点':'112、121、127合格锚点',
      '48项非涨停残差Ridge':'48项非涨停残差Ridge',
      'Register52 measured':'Register52 measured',
    }
    for old,new in changes.items():text=text.replace(old,new)
    return text

def convert(text):
    m={
      'nonflag_Ridge40_round121_full_registration_v1':'nonflag_RidgeFine52_round128_full_registration_v1',
      'quantile_HGB88_round119_full_registration_v6':'nonflag_Ridge40_round121_full_registration_v1',
      'nonflag_HGB40_round120_full_registration_v4':'nonflag_RFF128Hi76_round127_full_registration_v1',
      'nonflag_residual_Ridge37_transform_preflight':'nonflag_residual_RidgeFine49_transform_preflight',
      'verify_nonflag_residual_Ridge37_transform':'verify_nonflag_residual_RidgeFine49_transform',
      'nonflag_residual_Ridge_compatible_parent':'nonflag_residual_RidgeFine_compatible_parent',
      'predict_nonflag_residual_Ridge_complete_scheme':'predict_nonflag_residual_RidgeFine_complete_scheme',
      'nonflag_Ridge40':'nonflag_RidgeFine52',
      '(112,119,120)':'(112,121,127)', '(112, 119, 120)':'(112, 121, 127)',
      '((112,23),(119,30),(120,31))':'((112,23),(121,32),(127,38))',
      'round121':'round128','full121':'full128','actual121':'actual128','prospective121':'prospective128',
      '_r121':'_r128','qa32':'qa39','QA32':'QA39','qa_v32':'qa_v39',
      'NUMBER = 121':'NUMBER = 128','number == 121':'number == 128',
      'WAVES = (404,)':'WAVES = (411,)','wave=404':'wave=411','wave404_results':'wave411_results',
      "'waves': [404]":"'waves': [411]","'round':121":"'round':128","'round': 121":"'round': 128",
      '(121, 32, 40)':'(128, 39, 52)',"namespace['snapshot'](121)":"namespace['snapshot'](128)",
      'actual_complete_QA_version=32':'actual_complete_QA_version=39',"actual_full_QA_version': 32":"actual_full_QA_version': 39",
      'publish(121,':'publish(128,','lossless(121)':'lossless(128)',
      'passed_actual37':'passed_actual49','and111_cold_controls':'and147_cold_controls',
      'actual_full_cases=37':'actual_full_cases=49','actual_cold_cases=111':'actual_cold_cases=147',
      'len(controls[\'controls\'])==37':'len(controls[\'controls\'])==49',
      "actual_full_transform_controls':37":"actual_full_transform_controls':49",
      "actual_cold_prefix_controls':111":"actual_cold_prefix_controls':147",
      'passed_actual40':'passed_actual52','actual40':'actual52','all40':'all52','all5635800':'all5635800',
      'anchor40':'anchor52','by_all40':'by_all52','official40':'official52',
      "len(plan['weights'])==12":"len(plan['weights'])==16",
      "plan['expected_scored_records']==40":"plan['expected_scored_records']==52",
      "len(pilot['records'])==40":"len(pilot['records'])==52",
      'len(cases)==37':'len(cases)==49','len(cases)==plan[\'expected_scored_records\']==40':'len(cases)==plan[\'expected_scored_records\']==52',
      'expected_scored_records=40':'expected_scored_records=52',"'scored_records':40":"'scored_records':52",
      "'actual_full_cases':37":"'actual_full_cases':49","'actual_cold_cases':111":"'actual_cold_cases':147",
      "'expected_full_cases':37":"'expected_full_cases':49","'expected_cold_controls':111":"'expected_cold_controls':147",
      "'new_quality_score_records':40":"'new_quality_score_records':52",
      "'new_quality_scores':40":"'new_quality_scores':52",
      '40 if phase':'52 if phase','40项':'52项','乘12幅度':'乘16幅度',
      '37项5635800':'49项5635800','111冷前缀':'147冷前缀',
    }
    text=substitute(text,m)
    # New Ridge output replaces every older nonflag family. Generic linear math is unchanged.
    needle="graph.pop('nonflag_CPU_HGB_residual_CDF',None)"
    if needle in text:
        text=text.replace(needle,needle+"\n"+('            ' if '        if measured' in text else '        ')+
          "graph.pop('nonflag_CPU_RFFRidge_residual_CDF',None)\n"+
          ('            ' if '        if measured' in text else '        ')+"graph.pop('nonflag_CPU_RFF128_residual_CDF',None)")
    text=text.replace("('nonflag_cpu_hgb_','nonflag_cpu_ridge_')",
                      "('nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_rffridge_','nonflag_cpu_rff128_','nonflag_cpu_rff128low_','nonflag_cpu_rff128hi_')")
    text=text.replace("('nonflag_residual_hgb','nonflag_residual_ridge')",
                      "('nonflag_residual_hgb','nonflag_residual_ridge','nonflag_residual_rffridge','nonflag_residual_rff128')")
    return finalize(text)
