"""Add complete independent comparisons with an explicit qualified R66 parent."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(name, text):
    path = A / name
    compile(text, str(path), 'exec')
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)


def main():
    engine = (A / 'linear_leaf_search_engine_v2_20261005.py').read_text(encoding='utf-8')
    mapping = {'69': '81', '70': '82', **{str(n): str(n + 42) for n in range(283, 290)}}
    engine = re.sub(r'\b(?:69|70|283|284|285|286|287|288|289)\b', lambda m: mapping[m[0]], engine)
    engine = engine.replace("previous=importlib.import_module(f'optimize_training_round{number-1}')",
        "parent_number=66 if number==81 else 81\n    previous=importlib.import_module(f'optimize_training_round{parent_number}')")
    engine = engine.replace('{number-1}', '{parent_number}').replace('complete_round_evidence(number-1)', 'complete_round_evidence(parent_number)')
    engine = engine.replace('NUMBER=number,ROLES=', 'NUMBER=number,PREVIOUS_NUMBER=parent_number,ROLES=')
    engine = engine.replace('bank,empty_roles,append_role_layer,standalone_graph,AdaptiveGraphContext,',
        'bank,empty_roles,append_role_layer as original_append_role_layer,standalone_graph as original_standalone_graph,AdaptiveGraphContext,')
    engine = engine.replace('def install(number,namespace):',
        "def append_role_layer(graph):\n    return original_append_role_layer(graph,number=81)\n\n\ndef standalone_graph(graph,name,postprocessing,retention=.98,delta=.075):\n    return original_standalone_graph(graph,name,postprocessing,retention,delta,number=82)\n\n\ndef install(number,namespace):")
    replacements = {
        'nystrom_ridge_release_engine_20261004': 'explicit_parent_release_engine_20261005',
        'predict_linear_leaf_scheme_v2_20261005': 'predict_reference66_linear_leaf_scheme_20261005',
        'check_linear_leaf_scheme_20261005': 'check_reference66_linear_leaf_scheme_20261005',
        'parallel_candidate_scoring_four_20261004': 'parallel_candidate_scoring_one_20261005',
        'run_linear_leaf_round_v2_20261005': 'run_reference66_linear_leaf_round_20261005',
        'verify_linear_leaf_search_generators_v2_20261005': 'verify_reference66_linear_leaf_generators_20261005',
        'linear_leaf_search_generator_preflight_v2_20261005': 'reference66_linear_leaf_generator_preflight_20261005',
        'linear_leaf_complete_search_plan_20261005': 'reference66_linear_leaf_complete_plan_20261005',
        'optimize_training_round{number}_v2.py': 'optimize_training_round{number}.py',
        'run_training_round{number}_v2_pipeline.py': 'run_training_round{number}_pipeline.py',
        "'workers':4": "'workers':1",
    }
    for old, new in replacements.items():
        engine = engine.replace(old, new)
    engine = engine.replace("'starting_configuration':cfg,", "'explicit_parent_round':parent_number,'independent_comparison_branch':True,'starting_configuration':cfg,")
    create('linear_leaf_reference66_search_engine_20261005.py', engine)

    release = (A / 'nystrom_ridge_release_engine_20261004.py').read_text(encoding='utf-8')
    release = release.replace("ROOT=experiment.ROOT", "ROOT=experiment.ROOT\n    parent_number=experiment.PREVIOUS_NUMBER")
    release = release.replace('{number-1}', '{parent_number}')
    release = release.replace("'scored_records':len(rows),", "'explicit_parent_round':parent_number,'scored_records':len(rows),")
    create('explicit_parent_release_engine_20261005.py', release)

    publisher = (A / 'publish_training_round.py').read_text(encoding='utf-8')
    publisher = publisher.replace("selection=release.selected();", "parent_number=module.PREVIOUS_NUMBER\n    selection=release.selected();")
    publisher = publisher.replace("'round':number,", "'round':number,'explicit_parent_round':parent_number,'independent_comparison_branch':True,")
    publisher = publisher.replace('{number-1}', '{parent_number}')
    create('publish_explicit_parent_training_round_20261005.py', publisher)

    pool = (A / 'parallel_candidate_scoring_four_20261004.py').read_text(encoding='utf-8')
    pool = pool.replace('WORKERS=4', 'WORKERS=1').replace('in four isolated processes', 'in one isolated process')
    create('parallel_candidate_scoring_one_20261005.py', pool)

    checks = (A / 'check_linear_leaf_scheme_20261005.py').read_text(encoding='utf-8').replace('number == 69', 'number == 81')
    create('check_reference66_linear_leaf_scheme_20261005.py', checks)
    for number in (81, 82):
        header = 'import optimize_training_round81\n' if number == 82 else ''
        create(f'optimize_training_round{number}.py', header +
            f'from linear_leaf_reference66_search_engine_20261005 import install\ninstall({number},globals())\n')
        create(f'finalize_training_round{number}.py',
            f'from explicit_parent_release_engine_20261005 import install\ninstall({number},globals())\n')
        create(f'run_training_round{number}_pipeline.py',
            f'from run_reference66_linear_leaf_round_20261005 import main\nif __name__ == "__main__": main({number})\n')

    driver = (A / 'run_linear_leaf_round_v2_20261005.py').read_text(encoding='utf-8')
    driver = re.sub(r'\b(?:69|70)\b', lambda m: mapping[m[0]], driver)
    driver = driver.replace("state_path = ROOT /", "parent_number = 66 if number == 81 else 81\n    state_path = ROOT /")
    driver = driver.replace('number - 1', 'parent_number')
    for old, new in replacements.items():
        driver = driver.replace(old, new)
    driver = driver.replace('linear_leaf_quality_run_20261005', 'reference66_linear_leaf_quality_run_20261005')
    driver = driver.replace("f'optimize_training_round{number}_v2'", "f'optimize_training_round{number}'")
    driver = driver.replace("from publish_training_round import publish", "from publish_explicit_parent_training_round_20261005 import publish")
    driver = driver.replace("'round': number,", "'round': number,'explicit_parent_round':parent_number,")
    driver = driver.replace("'完整方案'", "'完整方案'")
    create('run_reference66_linear_leaf_round_20261005.py', driver)

    generator = (A / 'verify_linear_leaf_search_generators_v2_20261005.py').read_text(encoding='utf-8')
    generator = re.sub(r'\b(?:69|70)\b', lambda m: mapping[m[0]], generator)
    generator = generator.replace('optimization_20261003_r61', 'optimization_20261003_r66')
    generator = generator.replace("reference['nystrom_ridge_role_scheme_graph']", "reference['nystrom_tuning_standalone_scheme_graph']")
    generator = generator.replace("'actual_reference_round': 61", "'actual_reference_round': 66")
    generator = generator.replace('linear_leaf_search_generator_preflight_v2_20261005', 'reference66_linear_leaf_generator_preflight_20261005')
    generator = generator.replace('linear_leaf_complete_search_plan_20261005', 'reference66_linear_leaf_complete_plan_20261005')
    generator = generator.replace("from linear_leaf_scheme_runtime_20261005 import append_role_layer", "from linear_leaf_reference66_search_engine_20261005 import append_role_layer")
    generator = generator.replace("f'optimize_training_round{number}_v2'", "f'optimize_training_round{number}'")
    generator = generator.replace("('optimize_training_round', '_v2')", "('optimize_training_round', '')")
    generator = generator.replace("('run_training_round', '_v2_pipeline')", "('run_training_round', '_pipeline')")
    generator = generator.replace("'actual_R68_and_R69_full_predecessor_checks_required_before_quality': True", "'actual_R66_and_R81_explicit_parent_checks_required_before_quality': True")
    generator = generator.replace("sources += [p for p in (ROOT / 'analysis').glob('*linear_leaf*20261005.py')]", "sources += [p for p in A.glob('*reference66*20261005.py')]\n    sources += [A/name for name in ('explicit_parent_release_engine_20261005.py','publish_explicit_parent_training_round_20261005.py','parallel_candidate_scoring_one_20261005.py','predict_reference66_linear_leaf_scheme_20261005.py')]")
    generator = generator.replace("OUT = ROOT /", "A=ROOT/'analysis'\nOUT = ROOT /")
    create('verify_reference66_linear_leaf_generators_20261005.py', generator)

    selection = A / 'optimization_20261003_r66/selection.json'
    winner = json.loads(selection.read_text(encoding='utf-8'))['winner']
    plan = {'status':'prospectively_declared_before_new_official_scoring','explicit_parent_rounds':{'81':66,'82':81},
        'required_rounds':[81,82],'original_rounds67_through80_retained_and_required':True,
        'reference_selection_sha256':sha(selection),'reference_score':winner['connected_final_score'],
        'scored_records_prespecified':{'81':124,'82':138},'wave_arm_counts':{'81':[73,8,18,25],'82':[37,84,17]},
        'waves':{'81':[325,326,327,328],'82':[329,330,331]},
        'all6_original_linear_leaf_models_and_all_role_standalone_axes_preserved':True,
        'new_annual_model_fits':0,'new_final_model_fits':0,'existing_real_annual_fits_required':30,'existing_real_final_fits_required':6,
        'same_validation_rows':5635800,'continuous_days':1212,'years':[2020,2021,2022,2023,2024],
        'official_objective':'.4 ICmean + .3 annual_excess + .3 (1 - mean_turnover)',
        'mature_past_return_mapping_in_complete_csv_official_score':True,'native_reload_real_future_and_cold80_required':True,
        'parallel_candidate_workers':1,'worker_count_is_execution_layout_only_all_arms_and_forecast_math_preserved':True,
        'test_labels_read':False,'all_validation_years_reused_selection_bias_uncorrected':True,
        'not_global_method_or_resource_exhaustion':True,'only_publication_git_branch':'main'}
    with (A/'reference66_linear_leaf_complete_plan_20261005.json').open('x',encoding='utf-8') as stream:
        json.dump(plan,stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'created_explicit_parent_full_workflows','required_rounds':[81,82],'reference_score':plan['reference_score']}))


if __name__=='__main__':
    main()
