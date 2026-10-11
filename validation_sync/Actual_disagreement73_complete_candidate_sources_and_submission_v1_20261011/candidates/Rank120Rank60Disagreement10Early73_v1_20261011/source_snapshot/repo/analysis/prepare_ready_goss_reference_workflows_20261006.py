"""Declare independent full GOSS comparisons while retaining every original round."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def create(name, content):
    path = A / name
    compile(content, str(path), 'exec')
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(content)


def convert(content):
    numbers = {83: 95, 84: 96, **{n: n + 39 for n in range(332, 339)}}
    pattern = r'\b(?:' + '|'.join(map(str, numbers)) + r')\b'
    content = re.sub(pattern, lambda m: str(numbers[int(m[0])]), content)
    for old, new in numbers.items():
        content = content.replace(f'round{old}', f'round{new}')
        content = content.replace(f'wave{old}_', f'wave{new}_')
    replacements = {
        'ready_fm_reference': 'ready_goss_reference',
        'factorization_machine_scheme_runtime_v2_20261005': 'gradient_sampling_scheme_runtime_20261005',
        'factorization_machine_model_sources_v2_20261005': 'gradient_sampling_model_sources_20261005',
        'factorization_machine_future_qa_v2_20261005': 'gradient_sampling_future_qa_20261005',
        'factorization_machine_direct_router_preflight_v2_20261005': 'gradient_sampling_direct_router_preflight_20261005',
        'factorization_machine_preflight_20261005': 'gradient_sampling_preflight_20261005',
        'factorization_machine_future_codec_adapter_20261005': 'gradient_sampling_future_codec_adapter_20261005',
        'predict_factorization_machine_scheme_codec_v2_20261005': 'predict_gradient_sampling_scheme_codec_20261005',
        'factorization_machine_storage_20261005': 'gradient_sampling_storage_20261005',
        'factorization_machine_role_scheme_graph': 'gradient_sampling_reference_role_scheme_graph',
        'factorization_machine_standalone_scheme_graph': 'gradient_sampling_reference_standalone_scheme_graph',
        'previous_factorization_machine_bank_actual_annual_fits': 'previous_gradient_sampling_bank_actual_annual_fits',
        'factorization_machine_causal_checks.json': 'gradient_sampling_reference_causal_checks.json',
        'passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls': 'passed_actual_gradient_sampling_maturity_native_reload_and_prefix_controls',
        'matched factorization machine complete graph': 'matched GOSS complete graph',
        '因子分解机三种用途对照': 'GOSS三种用途对照',
        '成熟原始特征因子分解机完整方案': '成熟原始特征GOSS完整方案',
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    content = content.replace('parent_number=82 if number==95 else 95', 'parent_number=84 if number==95 else 95')
    content = content.replace('parent_number = 82 if number == 95 else 95', 'parent_number = 84 if number == 95 else 95')
    # Rename only the new family; inherited FM, leaf, and release sources stay versioned.
    content = re.sub(r'(ready_goss_reference[^\s\x27\x22/]*?)20261005', r'\g<1>20261006', content)
    return content


def main():
    assert not (A / 'optimize_training_round95_v2.py').exists()
    engine = convert((A / 'ready_fm_reference_search_engine_20261005.py').read_text(encoding='utf-8'))
    engine = engine.replace("cfg.get('kind')=='neural_ensemble'", "cfg.get('kind') in ('neural_ensemble','linear_leaf_ensemble')")
    engine = engine.replace("ROOT/'analysis/gradient_sampling_direct_router_preflight_20261005/verification.json']", "ROOT/'analysis/gradient_sampling_direct_router_preflight_20261005/verification.json',ROOT/'analysis/gradient_sampling_memmap_native_promotion_20261006/verification.json',ROOT/'analysis/ready_goss_reference_execution_preflight_20261006/verification.json']")
    engine = engine.replace("sources=[Path(__file__)", "sources=[ROOT/'analysis/gradient_sampling_memmap_complete_bank_v3_github_20261006/receipt.json',Path(__file__)")
    create('ready_goss_reference_search_engine_20261006.py', engine)
    driver = convert((A / 'run_ready_fm_reference_round_20261005.py').read_text(encoding='utf-8'))
    driver = driver.replace('waiting_for_qualified_R82_R83_and_actual30_annual6_final32epoch_FM_controls', 'waiting_for_qualified_R84_R95_and_actual30_annual6_final300tree_GOSS_controls')
    create('run_ready_goss_reference_round_20261006.py', driver)
    create('check_ready_goss_reference_scheme_20261006.py', convert((A / 'check_ready_fm_reference_scheme_20261005.py').read_text(encoding='utf-8')))
    predictor = convert((A / 'predict_ready_fm_reference_scheme_20261005.py').read_text(encoding='utf-8'))
    predictor = predictor.replace("'linear_leaf_reference66_search_engine_v2_20261005.py',", "'linear_leaf_reference66_search_engine_v2_20261005.py',\n        'optimize_training_round83_v2.py','finalize_training_round83_v2.py',\n        'optimize_training_round84_v2.py','finalize_training_round84_v2.py',\n        'ready_fm_reference_search_engine_20261005.py','run_ready_fm_reference_round_20261005.py',\n        'predict_ready_fm_reference_scheme_20261005.py','check_ready_fm_reference_scheme_20261005.py',")
    create('predict_ready_goss_reference_scheme_20261006.py', predictor)
    for number, parent in ((95, 84), (96, 95)):
        create(f'optimize_training_round{number}_v2.py', f'import sys\nimport optimize_training_round{parent}_v2\nfrom ready_goss_reference_search_engine_20261006 import install\ninstall({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\n')
        create(f'optimize_training_round{number}.py', f'from optimize_training_round{number}_v2 import *\n')
        create(f'finalize_training_round{number}_v2.py', f'from explicit_parent_release_engine_v2_20261005 import install\ninstall({number},globals())\n')
        create(f'finalize_training_round{number}.py', f'from finalize_training_round{number}_v2 import *\n')
        create(f'run_training_round{number}_v2_pipeline.py', f'from run_ready_goss_reference_round_20261006 import main\nif __name__=="__main__":main({number})\n')
    generator = convert((A / 'verify_ready_fm_reference_generators_20261005.py').read_text(encoding='utf-8'))
    generator = generator.replace('optimization_20261003_r66/selection.json', 'optimization_20261003_r84/selection.json')
    generator = generator.replace("reference['nystrom_tuning_standalone_scheme_graph']", "reference['factorization_machine_standalone_scheme_graph']")
    generator = generator.replace("A.glob('*ready_fm*20261005.py')", "A.glob('*ready_goss*20261006.py')")
    generator = generator.replace("'actual_reference_round':66,'reference_graph_for_generator_only_actual_R82_not_yet_qualified':True", "'actual_reference_round':84,'reference_graph_from_actual_qualified_R84':True")
    generator = generator.replace('actual_R82_and_R83_explicit_parent_checks_required_before_quality', 'actual_R84_and_R95_explicit_parent_checks_required_before_quality')
    create('verify_ready_goss_reference_generators_20261006.py', generator)
    execution = convert((A / 'verify_ready_fm_reference_execution_20261005.py').read_text(encoding='utf-8'))
    execution = execution.replace('module.PREVIOUS_NUMBER==number-1', 'module.PREVIOUS_NUMBER==(84 if number==95 else 95)')
    execution = execution.replace("f'optimize_training_round{number-1}_v2.py'", "f'optimize_training_round{84 if number==95 else 95}_v2.py'")
    execution = execution.replace("'explicit_parent_round':number-1", "'explicit_parent_round':84 if number==95 else 95")
    execution = execution.replace("cfg['kind']=='factorization_machine'", "cfg['kind']=='lightgbm_gradient_sampling'")
    execution = execution.replace("'native_kind':'factorization_machine'", "'native_kind':'lightgbm_gradient_sampling'")
    execution = execution.replace("candidate/'optimize_training_round82.py')==sha(A/'optimize_training_round82_v2.py'", "candidate/'optimize_training_round84.py')==sha(A/'optimize_training_round84_v2.py'")
    execution = execution.replace('actual_FM_native_dispatch_install_and_restore_checked', 'actual_GOSS_native_dispatch_install_and_restore_checked')
    execution = execution.replace('R82_and_R83_actual_qualification_required_before_quality', 'R84_and_R95_actual_qualification_required_before_quality')
    execution = execution.replace('passed_actual_FM_driver_source_and_dispatch_controls', 'passed_actual_GOSS_driver_source_and_dispatch_controls')
    create('verify_ready_goss_reference_execution_20261006.py', execution)
    plan = json.loads((A / 'ready_fm_reference_complete_plan_20261005.json').read_text(encoding='utf-8'))
    plan.update(required_rounds=[95,96], explicit_parent_rounds={'95':84,'96':95}, scored_records_prespecified={'95':124,'96':138}, wave_arm_counts={'95':[73,8,18,25],'96':[37,84,17]}, waves={'95':[371,372,373,374],'96':[375,376,377]}, original_required_rounds67_through94_retained=True, original_round75_parent74_and_round76_parent75_unchanged=True, additional_records_not_replacement=262)
    plan.pop('prior_rounds67_through82_retained_and_required')
    plan.pop('all6_native_rank_return_k0_k8_k32_full32epoch_FM_configurations_preserved')
    plan['all6_native_rank_return_low_medium_high_full300tree_GOSS_configurations_preserved'] = True
    with (A / 'ready_goss_reference_complete_plan_20261006.json').open('x',encoding='utf-8') as stream:
        json.dump(plan,stream,ensure_ascii=False,indent=2)
    files = sorted(A.glob('*ready_goss*20261006.py')) + [A / f'{p}{n}{s}.py' for n in (95,96) for p,s in (('optimize_training_round','_v2'),('finalize_training_round','_v2'),('run_training_round','_v2_pipeline'))]
    for path in files:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    record = {'status':'created_prospective_complete_GOSS_R95_R96_sources','original_scope_retained':list(range(67,95)),'additional_full_official_records':262,'sources_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False}
    with (A/'ready_goss_reference_source_generation_20261006.json').open('x',encoding='utf-8') as stream:
        json.dump(record,stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':record['status'],'new_rounds':[95,96],'prespecified_quality_records':262}),flush=True)


if __name__ == '__main__':
    main()
