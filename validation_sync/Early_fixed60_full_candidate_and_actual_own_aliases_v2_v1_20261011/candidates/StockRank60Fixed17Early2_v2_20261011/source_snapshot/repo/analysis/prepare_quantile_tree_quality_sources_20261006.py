"""Derive complete four-model searches with explicit predecessor R90/R91."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        if isinstance(value, str):
            stream.write(value)
        else:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


def adapt(text):
    numbers = {88: 90, 89: 91, 90: 92, **{n: n + 7 for n in range(353, 360)}}
    text = re.sub(r'(?<!\d)(?:88|89|90|353|354|355|356|357|358|359)(?!\d)',
                  lambda m: str(numbers[int(m.group())]), text)
    text = text.replace('ready_classifier_consensus_reference_', 'quantile_tree_quality_')
    text = text.replace('classifier_consensus_scheme_runtime_20261006', 'quantile_tree_scheme_runtime_20261006')
    text = text.replace('classifier_consensus_model_sources_20261005', 'quantile_tree_model_sources_20261006')
    text = text.replace('build_classifier_consensus_bank_20261005', 'train_quantile_tree_bank_20261006')
    text = text.replace('classifier_consensus_future_codec_adapter_20261005', 'quantile_tree_future_codec_20261006')
    text = text.replace('classifier_consensus_preflight_20261005', 'quantile_tree_preflight_20261006')
    text = text.replace('classifier_consensus_future_qa_20261005', 'quantile_tree_future_qa_20261006')
    text = text.replace('classifier_consensus_storage_20261006', 'quantile_tree_storage_20261006')
    text = text.replace('classifier_consensus_direct_router_preflight_20261005', 'quantile_tree_codec_preflight_20261006')
    text = text.replace('classifier_consensus_role_scheme_graph', 'quantile_tree_role_scheme_graph')
    text = text.replace('classifier_consensus_standalone_scheme_graph', 'quantile_tree_standalone_scheme_graph')
    text = text.replace('classifier_consensus_augmentation', 'quantile_tree_augmentation')
    text = text.replace("'name':'classifier_consensus'", "'name':'quantile_tree'")
    text = text.replace('classifier_consensus_causal_checks.json', 'quantile_tree_causal_checks.json')
    text = text.replace('all6_fixed_composites', 'all4_native_quantile_models')
    text = text.replace('fixed classifier consensus', 'native quantile trees')
    return text


def replace_once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after)


def main():
    outputs = {}
    originals = {}
    for filename in ('classifier_consensus_scheme_runtime_20261006.py',
        'ready_classifier_consensus_reference_search_engine_v2_20261006.py',
        'run_ready_classifier_consensus_reference_round_v2_20261006.py',
        'predict_ready_classifier_consensus_reference_scheme_v2_20261006.py',
        'check_ready_classifier_consensus_reference_scheme_v2_20261006.py',
        'verify_ready_classifier_consensus_reference_generators_v2_20261006.py'):
        originals[filename] = sha(A / filename)
    runtime = adapt((A / 'classifier_consensus_scheme_runtime_20261006.py').read_text(encoding='utf-8'))
    runtime = replace_once(runtime,
        "source=ROOT/f'analysis/quantile_tree_future_qa_20261006/{name}.joblib'",
        "source=router.source_dir(name)/'model_2025.joblib'")
    outputs['quantile_tree_scheme_runtime_20261006.py'] = runtime
    outputs['quantile_tree_model_sources_20261006.py'] = (
        '"""Route full quantile models and preserve every ancestor family."""\n'
        'import classifier_consensus_model_sources_20261005 as previous\n'
        'import train_quantile_tree_bank_20261006 as native\n'
        'CONFIGS={**previous.CONFIGS,**native.CONFIGS}\nNEW_CONFIGS=native.CONFIGS\nYEARS=native.YEARS\n'
        'read,dump,sha,log=native.read,native.dump,native.sha,native.log\n'
        'def source_dir(name):\n    assert name in CONFIGS\n    return native.OUT/name if name in NEW_CONFIGS else previous.source_dir(name)\n'
        'def model_path(name,year):return source_dir(name)/f"model_{year}.joblib"\n'
        'def load_bundle(path):return native.engine.load_bundle(path)\n'
        'def predict_arrays(bundle,x,dates=None,valid=None):\n'
        '    if bundle.get("kind")=="lightgbm_quantile_tree":return native.predict_arrays(bundle,x)\n'
        '    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)\n')
    engine = adapt((A / 'ready_classifier_consensus_reference_search_engine_v2_20261006.py').read_text(encoding='utf-8'))
    engine = replace_once(engine,
        "previous=importlib.import_module(f'optimize_training_round{parent_number}_v3' if parent_number==91 else f'optimize_training_round{parent_number}_v2')",
        "previous=importlib.import_module(f'optimize_training_round{parent_number}_v3')")
    changes = {
        'passed_actual_native_parent_consensus_reload_and_prefix': 'passed_actual_quantile_native_maturity_reload_and_cold80_controls',
        "bank.OUT/'construction_execution_scope.json'": "bank.OUT/'training_execution_scope.json'",
        "['actual_virtual_annual_outputs']==30": "['actual_annual_fits']==20",
        "['actual_virtual_final_artifacts']==6": "['actual_full_final_fits']==4",
        "'expected_scored_records':124 if number==91 else 138": "'expected_scored_records':100 if number==91 else 98",
        "'wave_arm_counts':[73,8,18,25] if number==91 else [37,84,17]": "'wave_arm_counts':[49,8,18,25] if number==91 else [25,56,17]",
        "'reused_unique_native_classifier_annual_fits':20,'actual_virtual_annual_outputs':30,'new_native_model_configurations':0,'existing_native_configurations_reused':4,'new_fixed_composites':6":
            "'previous_quantile_bank_actual_annual_fits':20,'previous_quantile_bank_actual_final_fits':4,'new_native_model_configurations':4,'existing_full_native_configurations_reused':4,'new_fixed_composites':0",
    }
    for before, after in changes.items():
        engine = replace_once(engine, before, after)
    # All new inference and full-training implementation dependencies are frozen.
    engine = replace_once(engine, "sources=[Path(__file__),",
        "sources=[ROOT/'analysis/quantile_tree_candidate_20261006.py',ROOT/'analysis/quantile_tree_future_codec_20261006.py',ROOT/'analysis/train_quantile_tree_bank_20261006.py',ROOT/'analysis/verify_quantile_tree_full_future_20261006.py',Path(__file__),")
    outputs['quantile_tree_quality_search_engine_v2_20261006.py'] = engine
    driver = adapt((A / 'run_ready_classifier_consensus_reference_round_v2_20261006.py').read_text(encoding='utf-8'))
    driver = driver.replace('actual30_virtual_annual6_fullfuture_controls', 'actual20_annual4_fullfuture_quantile_controls')
    driver = replace_once(driver, "'fixed_composites': 6, 'new_native_fits': 0", "'native_quantile_configs': 4, 'previous_actual_annual_fits': 20, 'new_native_fits_by_quality': 0")
    driver = driver.replace('固定分类集成完整方案', '固定分位数损失树模型完整方案')
    driver = driver.replace('鲁棒线性回归模型三种用途对照', '分位数树模型三种用途对照')
    outputs['run_quantile_tree_quality_round_v2_20261006.py'] = driver
    checks = adapt((A / 'check_ready_classifier_consensus_reference_scheme_v2_20261006.py').read_text(encoding='utf-8'))
    outputs['check_quantile_tree_quality_scheme_v2_20261006.py'] = checks
    predictor = adapt((A / 'predict_ready_classifier_consensus_reference_scheme_v2_20261006.py').read_text(encoding='utf-8'))
    # Inherit all actual R90 inference dependencies, rather than a numeric-remapped R88 list.
    predictor = predictor.replace('from predict_ready_robust_reference_scheme_20261005 import source_names as inherited',
        'from predict_ready_classifier_consensus_reference_scheme_v2_20261006 import source_names as inherited')
    predictor = predictor.replace('train_quantile_tree_bank_20261006.py', 'quantile_tree_future_codec_20261006.py')
    predictor = predictor.replace("'quantile_tree_model_sources_20261006.py',", "'quantile_tree_candidate_20261006.py',")
    outputs['predict_quantile_tree_quality_scheme_v2_20261006.py'] = predictor
    preflight = adapt((A / 'verify_ready_classifier_consensus_reference_generators_v2_20261006.py').read_text(encoding='utf-8'))
    preflight = preflight.replace('[73, 8, 18, 25]', '[49, 8, 18, 25]').replace('[37, 84, 17]', '[25, 56, 17]')
    preflight = preflight.replace('(124 if number == 91 else 138)', '(100 if number == 91 else 98)')
    preflight = preflight.replace("glob('*ready_classifier_consensus*20261006.py')", "glob('*quantile_tree*20261006.py')")
    outputs['verify_quantile_tree_quality_generators_v2_20261006.py'] = preflight
    for number in (91, 92):
        outputs[f'optimize_training_round{number}_v3.py'] = (
            f'import sys\nimport optimize_training_round{number-1}_v3\n'
            'from quantile_tree_quality_search_engine_v2_20261006 import install\n'
            f'install({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\n')
        outputs[f'finalize_training_round{number}_v3.py'] = (
            'from explicit_parent_release_engine_v3_20261006 import install\n'
            f'install({number},globals())\n')
        outputs[f'run_training_round{number}_v3_pipeline.py'] = (
            'from run_quantile_tree_quality_round_v2_20261006 import main\n'
            f'if __name__=="__main__":main({number})\n')
    for name, text in outputs.items():
        compile(text, str(A / name), 'exec')
    # No partial output creation until every template transformation compiles.
    for name, text in outputs.items():
        create(A / name, text)
    plan = {'status': 'prespecified_full198_record_quantile_quality_grid_before_controls',
        'rounds': [91, 92], 'explicit_parent_rounds': {'91': 90, '92': 91},
        'model_count': 4, 'actual_full_annual_fits_required': 20, 'actual_full_final_fits_required': 4,
        'quality_records': {'91': 100, '92': 98}, 'wave_arm_counts': {'91': [49, 8, 18, 25], '92': [25, 56, 17]},
        'generator_controls_and_native_direct_codec_controls_still_required': True,
        'complete_five_year_official_scoring_still_pending': True,
        'all_full_scheme_freeze_causal_return_mapping_native_future_candidate_and_ranking_gates_required': True,
        'method_overlap': 'Historical XGBoost90% quantile is recorded in the catalog; this is a prespecified matched LightGBM rank-median and return.1/.5/.9 objective contrast, not a claim that quantile regression has never been tried.',
        'sole_gate': 'Actual official complete continuous return-mapped CSV S; ties use existing branch-count rule.',
        'selection_bias_uncorrected': True, 'test_labels_read': False, 'new_quality_scores': 0,
        'template_sha256': originals, 'generated_source_sha256': {name: sha(A / name) for name in outputs}}
    create(A / 'quantile_tree_quality_complete_plan_v2_20261006.json', plan)
    create(A / 'quantile_tree_quality_source_generation_20261006.json', {'status': 'generated_full198_record_sources_controls_pending',
        'template_sha256': originals, 'generated_sha256': plan['generated_source_sha256'],
        'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
