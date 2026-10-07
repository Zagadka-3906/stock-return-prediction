"""Fresh final-amplitude Ridge routes; original native training and codecs stay immutable."""
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def convert(text):
    changes={
      'nonflag_Ridge40_round121_full_registration_v1':'nonflag_RFF128StreamMid76_round129_full_registration_v1',
      'nonflag_RFF128Hi76_round127_full_registration_v1':'nonflag_EmpiricalBayes40_round130_full_registration_v1',
      'nonflag_RidgeFine52':'nonflag_RidgeMicro40',
      'nonflag_residual_RidgeFine49':'nonflag_residual_RidgeMicro37',
      'nonflag_residual_RidgeFine_compatible_parent':'nonflag_residual_RidgeMicro_compatible_parent',
      'predict_nonflag_residual_RidgeFine_complete_scheme':'predict_nonflag_residual_RidgeMicro_complete_scheme',
      '(112,121,127)':'(112,129,130)','(112, 121, 127)':'(112, 129, 130)',
      '((112,23),(121,32),(127,38))':'((112,23),(129,40),(130,41))',
      'round128':'round131','full128':'full131','actual128':'actual131','prospective128':'prospective131','_r128':'_r131',
      'qa39':'qa42','QA39':'QA42','qa_v39':'qa_v42',
      'NUMBER = 128':'NUMBER = 131','number == 128':'number == 131',
      'WAVES = (411,)':'WAVES = (414,)','wave=411':'wave=414','wave411_results':'wave414_results',
      "'waves': [411]":"'waves': [414]","'round':128":"'round':131","'round': 128":"'round': 131",
      '(128, 39, 52)':'(131, 42, 40)',"namespace['snapshot'](128)":"namespace['snapshot'](131)",
      'actual_complete_QA_version=39':'actual_complete_QA_version=42',"actual_full_QA_version': 39":"actual_full_QA_version': 42",
      'publish(128,':'publish(131,','lossless(128)':'lossless(131)',
      'passed_actual52':'passed_actual40','selected_anchor52':'selected_anchor40','selected_by_all52':'selected_by_all40',
      'actual_all52':'actual_all40','all52':'all40','official52':'official40',
      'passed_actual49':'passed_actual37','and147_cold_controls':'and111_cold_controls',
      'len(cases)==49':'len(cases)==37',"len(controls['controls'])==49":"len(controls['controls'])==37",
      "len(plan['weights'])==16":"len(plan['weights'])==12",
      "len(pilot['records'])==52":"len(pilot['records'])==40", "len(pilot['records']) == 52":"len(pilot['records']) == 40",
      'expected_scored_records=52':'expected_scored_records=40', "plan['expected_scored_records']==52":"plan['expected_scored_records']==40",
      "'expected_scored_records': 52":"'expected_scored_records': 40", "record['expected_scored_records'] == 52":"record['expected_scored_records'] == 40",
      "'scored_records':52":"'scored_records':40", "'scored_records': 52":"'scored_records': 40",
      "'new_quality_score_records':52":"'new_quality_score_records':40", "'new_quality_scores':52":"'new_quality_scores':40",
      "'actual_full_cases':49":"'actual_full_cases':37", "'actual_cold_cases':147":"'actual_cold_cases':111",
      "'expected_full_cases':49":"'expected_full_cases':37", "'expected_cold_controls':147":"'expected_cold_controls':111",
      "'actual_full_transform_controls':49":"'actual_full_transform_controls':37", "'actual_cold_prefix_controls':147":"'actual_cold_prefix_controls':111",
      "'actual_full_control_cases':49":"'actual_full_control_cases':37", "'actual_cold_prefix_cases':147":"'actual_cold_prefix_cases':111",
      '(49 if phase==\'controls\' else 52)':'(37 if phase==\'controls\' else 40)', '52 if phase':'40 if phase',
      "'expected_cases':52":"'expected_cases':40", 'all49_nonanchors':'all37_nonanchors',
      "'existing_actual_official_records': 52":"'existing_actual_official_records': 40", "len(record['ranking']) == 52":"len(record['ranking']) == 40",
      "manifest['scored_records'] == full['scored_records'] == 52":"manifest['scored_records'] == full['scored_records'] == 40",
      "'original_official_pilot_records_registered': 52":"'original_official_pilot_records_registered': 40",
      "'existing_official_scores_registered':52":"'existing_official_scores_registered':40",
      'actual_full_transform_controls=49':'actual_full_transform_controls=37','actual_cold_prefix_controls=147':'actual_cold_prefix_controls=111',
      '各16个新幅度':'各12个新幅度','49全量':'37全量','147冷前缀':'111冷前缀','完整128候选':'完整131候选',
      '112、121、127合格锚点':'112、129、130合格锚点','48项非涨停残差Ridge':'36项非涨停残差Ridge',
      '预定52项':'预定40项','三个合格锚点、48项':'三个合格锚点、36项',
    }
    result=substitute(text,changes)
    needle="graph.pop('nonflag_CPU_HGB_residual_CDF',None)"
    if needle in result:
        indent='            ' if '        if measured' in result else '        '
        result=result.replace(needle,needle+'\n'+indent+"graph.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)")
    result=result.replace("value.pop('nonflag_CPU_HGB_residual_CDF',None)",
      "value.pop('nonflag_CPU_HGB_residual_CDF',None)\n    value.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)")
    result=result.replace("('nonflag_cpu_hgb_','nonflag_cpu_ridge_'", "('nonflag_cpu_hgb_','nonflag_cpu_empirical_bayes64_','nonflag_cpu_ridge_'")
    result=result.replace("('nonflag_residual_hgb','nonflag_residual_ridge'", "('nonflag_residual_hgb','nonflag_residual_empirical_bayes64','nonflag_residual_ridge'")
    return result
