"""Use already verified full FM fits after the qualified lightweight reference chain."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'


def create(name,text):
    path=A/name
    compile(text,str(path),'exec')
    with path.open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)


def renumber(text):
    mapping={81:83,82:84,**{n:n+7 for n in range(325,332)}}
    text=re.sub(r'\b(?:81|82|325|326|327|328|329|330|331)\b',lambda m:str(mapping[int(m[0])]),text)
    for old,new in mapping.items():
        text=text.replace(f'round{old}',f'round{new}')
        text=text.replace(f'wave{old}_',f'wave{new}_')
    return text


def main():
    replacements={
        'linear_leaf_reference66_search_engine_v2_20261005':'ready_fm_reference_search_engine_20261005',
        'predict_reference66_linear_leaf_scheme_v2_20261005':'predict_ready_fm_reference_scheme_20261005',
        'run_reference66_linear_leaf_round_v2_20261005':'run_ready_fm_reference_round_20261005',
        'check_reference66_linear_leaf_scheme_v2_20261005':'check_ready_fm_reference_scheme_20261005',
        'verify_reference66_linear_leaf_generators_v2_20261005':'verify_ready_fm_reference_generators_20261005',
        'reference66_linear_leaf_generator_preflight_v2_20261005':'ready_fm_reference_generator_preflight_20261005',
        'reference66_linear_leaf_execution_preflight_20261005':'ready_fm_reference_execution_preflight_20261005',
        'reference66_linear_leaf_complete_plan_20261005':'ready_fm_reference_complete_plan_20261005',
        'reference66_linear_leaf_quality_run_20261005':'ready_fm_reference_quality_run_20261005',
        'linear_leaf_scheme_runtime_20261005':'factorization_machine_scheme_runtime_v2_20261005',
        'linear_leaf_model_sources_20261005':'factorization_machine_model_sources_v2_20261005',
        'linear_leaf_future_codec_adapter_20261005':'factorization_machine_future_codec_adapter_20261005',
        'linear_leaf_future_qa_20261005':'factorization_machine_future_qa_v2_20261005',
        'linear_leaf_preflight_20261005':'factorization_machine_preflight_20261005',
        'linear_leaf_role_scheme_graph':'factorization_machine_role_scheme_graph',
        'linear_leaf_standalone_scheme_graph':'factorization_machine_standalone_scheme_graph',
        'previous_linear_leaf_bank_actual_annual_fits':'previous_factorization_machine_bank_actual_annual_fits',
        'linear_leaf_causal_checks.json':'factorization_machine_causal_checks.json',
        'linear_leaf_storage_20261005':'factorization_machine_storage_20261005',
        'passed_actual_linear_leaf_maturity_native_reload_and_prefix_controls':'passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls',
        'matched constant andlinear leaf complete graph':'matched factorization machine complete graph',
        '普通树叶与线性树叶模型三种用途对照':'因子分解机三种用途对照',
        '匹配参数的普通树叶与线性树叶LightGBM完整方案':'成熟原始特征因子分解机完整方案',
    }

    def convert(text):
        text=renumber(text)
        for old,new in replacements.items():text=text.replace(old,new)
        text=text.replace('parent_number=66 if number==83 else 83','parent_number=82 if number==83 else 83')
        text=text.replace('parent_number = 66 if number == 83 else 83','parent_number = 82 if number == 83 else 83')
        return text

    engine=convert((A/'linear_leaf_reference66_search_engine_v2_20261005.py').read_text(encoding='utf-8'))
    engine=engine.replace("f'optimize_training_round{parent_number}'","f'optimize_training_round{parent_number}_v2'")
    engine=engine.replace("'new_native_model_configurations':6", "'new_native_model_configurations':0,'existing_native_configurations_reused':6")
    engine=engine.replace("ROOT/'analysis/predict_linear_leaf_scheme_20261005.py'", "ROOT/'analysis/predict_factorization_machine_scheme_codec_v2_20261005.py'")
    engine=engine.replace("ROOT/'analysis/factorization_machine_future_codec_adapter_20261005.py',", "ROOT/'analysis/factorization_machine_future_codec_adapter_20261005.py',ROOT/'analysis/linear_leaf_ensemble_future_codec_adapter_20261005.py',ROOT/'analysis/linear_leaf_future_codec_adapter_20261005.py',ROOT/'analysis/predict_factorization_machine_scheme_codec_v2_20261005.py',")
    engine=engine.replace("ROOT/'analysis/ready_fm_reference_generator_preflight_20261005/verification.json']", "ROOT/'analysis/ready_fm_reference_generator_preflight_20261005/verification.json',ROOT/'analysis/factorization_machine_direct_router_preflight_v2_20261005/verification.json']")
    create('ready_fm_reference_search_engine_20261005.py',engine)
    driver=convert((A/'run_reference66_linear_leaf_round_v2_20261005.py').read_text(encoding='utf-8'))
    driver=driver.replace('waiting_for_actual30_annual6_final_fits_controls_and_full_predecessor','waiting_for_qualified_R82_R83_and_actual30_annual6_final32epoch_FM_controls')
    create('run_ready_fm_reference_round_20261005.py',driver)
    checks=convert((A/'check_reference66_linear_leaf_scheme_v2_20261005.py').read_text(encoding='utf-8'))
    create('check_ready_fm_reference_scheme_20261005.py',checks)
    predictor=convert((A/'predict_reference66_linear_leaf_scheme_v2_20261005.py').read_text(encoding='utf-8'))
    predictor=predictor.replace('from predict_linear_leaf_scheme_20261005 import predict as original','from predict_factorization_machine_scheme_codec_v2_20261005 import predict as original')
    # The actual predecessor factories must be retained as versioned sources;
    # a candidate must never fall back to the failed original R81 factory.
    predictor=predictor.replace("*(() if number==83 else ('optimize_training_round83_v2.py','finalize_training_round83_v2.py'))", "'optimize_training_round81_v2.py','optimize_training_round82_v2.py',\n        'linear_leaf_reference66_search_engine_v2_20261005.py',\n        *(() if number==83 else ('optimize_training_round83_v2.py','finalize_training_round83_v2.py'))")
    create('predict_ready_fm_reference_scheme_20261005.py',predictor)
    for number in (83,84):
        previous=82 if number==83 else 83
        create(f'optimize_training_round{number}_v2.py',
            f'import sys\nimport optimize_training_round{previous}_v2\nfrom ready_fm_reference_search_engine_20261005 import install\ninstall({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\n')
        create(f'optimize_training_round{number}.py',f'from optimize_training_round{number}_v2 import *\n')
        create(f'finalize_training_round{number}_v2.py',
            f'from explicit_parent_release_engine_v2_20261005 import install\ninstall({number},globals())\n')
        create(f'finalize_training_round{number}.py',f'from finalize_training_round{number}_v2 import *\n')
        create(f'run_training_round{number}_v2_pipeline.py',
            f'from run_ready_fm_reference_round_20261005 import main\nif __name__=="__main__":main({number})\n')
    generator=convert((A/'verify_reference66_linear_leaf_generators_v2_20261005.py').read_text(encoding='utf-8'))
    generator=generator.replace("A.glob('*reference66*20261005.py')","A.glob('*ready_fm*20261005.py')")
    generator=generator.replace("'actual_R66_and_R81_explicit_parent_checks_required_before_quality': True", "'actual_R82_and_R83_explicit_parent_checks_required_before_quality': True")
    generator=generator.replace("'actual_reference_round': 66", "'actual_reference_round':66,'reference_graph_for_generator_only_actual_R82_not_yet_qualified':True")
    create('verify_ready_fm_reference_generators_20261005.py',generator)
    plan={'status':'prospectively_declared_before_actual_quality','required_rounds':[83,84],
        'explicit_parent_rounds':{'83':82,'84':83},'prior_rounds67_through82_retained_and_required':True,
        'scored_records_prespecified':{'83':124,'84':138},'wave_arm_counts':{'83':[73,8,18,25],'84':[37,84,17]},
        'waves':{'83':[332,333,334,335],'84':[336,337,338]},
        'all6_native_rank_return_k0_k8_k32_full32epoch_FM_configurations_preserved':True,
        'existing_actual_annual_fits_required':30,'existing_actual_final_fits_required':6,
        'new_native_configurations':0,'new_native_fits':0,'baseline_score_not_set_until_actual_parent_qualified':True,
        'same_validation_rows':5635800,'continuous_days':1212,'years':[2020,2021,2022,2023,2024],
        'official_objective':'.4 ICmean + .3 annual_excess + .3 (1 - mean_turnover)',
        'all_role_combinations_weight_retention_UP_delta_and_standalone_refinements_preserved':True,
        'mature_past_return_mapping_complete_csv_and_causal_checks_required':True,
        'real1599600_future_model_reload_and_cold80_prefix_required':True,'scoring_workers':1,
        'worker_count_changes_execution_only_original_forecast_math_and_all_arms_preserved':True,
        'all_validation_years_reused_selection_bias_uncorrected':True,'test_labels_read':False,
        'only_git_publication_branch':'main','global_resource_exhaustion_not_claimed':True}
    with (A/'ready_fm_reference_complete_plan_20261005.json').open('x',encoding='utf-8') as stream:json.dump(plan,stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'created_complete_ready_FM_workflows','rounds':[83,84],'required_official_records':262}))


if __name__=='__main__':main()
