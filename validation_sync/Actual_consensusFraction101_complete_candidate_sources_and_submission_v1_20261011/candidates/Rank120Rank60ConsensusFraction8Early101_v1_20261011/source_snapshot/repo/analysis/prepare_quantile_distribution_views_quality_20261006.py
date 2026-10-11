"""Preserve original grids while adding six virtual views as rounds93/94."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    templates = (
        'quantile_tree_scheme_runtime_20261006.py',
        'quantile_tree_quality_search_engine_v2_20261006.py',
        'run_quantile_tree_quality_round_v2_20261006.py',
        'predict_quantile_tree_quality_scheme_v2_20261006.py',
        'check_quantile_tree_quality_scheme_v2_20261006.py',
        'verify_quantile_tree_quality_generators_v2_20261006.py')
    outputs = {}
    for template in templates:
        text = (A / template).read_text(encoding='utf-8')
        text = text.replace('quantile_tree', 'quantile_distribution_views')
        text = text.replace('train_quantile_distribution_views_bank_20261006', 'build_quantile_distribution_views_bank_20261006')
        text = text.replace('quantile_distribution_views_candidate_20261006', 'quantile_distribution_views_20261006')
        text = text.replace('quantile_distribution_views_quality_quality_run', 'quantile_distribution_views_quality_run')
        text = text.replace('91', '93').replace('92', '94')
        text = text.replace('parent_number=90', 'parent_number=92').replace('parent_number = 90', 'parent_number = 92')
        for value in range(360, 367):
            text = text.replace(str(value), str(value + 40))
        text = text.replace('100 if number==93 else 98', '124 if number==93 else 138')
        text = text.replace('100 if number == 93 else 98', '124 if number == 93 else 138')
        text = text.replace('[49,8,18,25] if number==93 else [25,56,17]', '[73,8,18,25] if number==93 else [37,84,17]')
        text = text.replace('[49, 8, 18, 25] if number == 93 else [25, 56, 17]', '[73, 8, 18, 25] if number == 93 else [37, 84, 17]')
        if template.startswith('quantile_tree_quality_search'):
            text = text.replace("'classifier_consensus')", "'classifier_consensus','quantile_distribution_view')")
            text = text.replace("'passed_actual_quantile_native_maturity_reload_and_cold80_controls'", "'passed_actual_six_distribution_views_native_cold80_independent_codec_and_math_controls'")
            text = text.replace("bank.OUT/'training_execution_scope.json'", "bank.OUT/'execution_scope.json'")
            text = text.replace("ROOT/'analysis/quantile_distribution_views_codec_preflight_20261006/verification.json'", "ROOT/'analysis/quantile_distribution_views_preflight_20261006/execution_scope.json'")
            text = text.replace("['actual_annual_fits']==20", "['actual_virtual_annual_outputs']==30")
            text = text.replace("['actual_full_final_fits']==4", "['actual_full_future_views']==6")
            text = text.replace("'previous_quantile_bank_actual_annual_fits':20", "'previous_distribution_bank_actual_virtual_annual_outputs':30")
            text = text.replace("'previous_quantile_bank_actual_final_fits':4", "'previous_distribution_bank_actual_virtual_final_artifacts':6")
            text = text.replace("'new_native_model_configurations':4", "'new_native_model_configurations':0")
            text = text.replace("'existing_full_native_configurations_reused':4", "'existing_full_native_configurations_reused':3")
            text = text.replace("'new_fixed_composites':0", "'new_fixed_composites':6")
            text = text.replace("'quantile_distribution_views_native_maturity", "'quantile_distribution_views_virtual_maturity")
            text = text.replace('all4_native_quantile_models_cold_prefix_andpoisoning_controls', 'all6_virtual_distribution_views_cold_prefix_andpoisoning_controls')
            text = text.replace('native quantile trees complete graph', 'fixed quantile distribution views complete graph')
        if template.startswith('predict_'):
            text = text.replace('from predict_ready_classifier_consensus_reference_scheme_v2_20261006 import source_names as inherited', 'from predict_quantile_tree_quality_scheme_v2_20261006 import source_names as inherited')
            text = text.replace('inherited(90)', 'inherited(92)')
            insertion = "        'quantile_distribution_views_scheme_runtime_20261006.py',"
            assert insertion in text
            text = text.replace(insertion, insertion + "\n        'build_quantile_distribution_views_bank_20261006.py',\n        'quantile_distribution_views_model_sources_20261006.py',\n        'train_quantile_tree_memmap_bank_20261006.py',\n        'mature_training_memmap_20261006.py',")
        if template.startswith('check_'):
            text = text.replace('all4_native_quantile_models_checked', 'all6_fixed_distribution_views_checked')
        if template.startswith('run_'):
            text = text.replace('R90_R93_and_actual20_annual4_fullfuture_quantile_controls', 'R92_R93_and_actual30_virtual_annual6_fullfuture_distribution_controls')
            text = text.replace("'native_quantile_configs': 4, 'previous_actual_annual_fits': 20", "'fixed_distribution_views': 6, 'previous_actual_virtual_annual_outputs': 30")
            text = text.replace('固定分位数损失树模型完整方案', '固定分位数分布组合完整方案')
        if template.startswith('verify_'):
            text = text.replace('actual_R90_and_R93', 'actual_R92_and_R93')
            text = text.replace('actual_R90_not_yet_qualified', 'actual_R92_not_yet_qualified')
        destination = A / template.replace('quantile_tree', 'quantile_distribution_views')
        outputs[destination] = text
    for number, prior in ((93, 92), (94, 93)):
        outputs[A / f'optimize_training_round{number}_v3.py'] = (
            f'import sys\nimport optimize_training_round{prior}_v3\n'
            'from quantile_distribution_views_quality_search_engine_v2_20261006 import install\n'
            f'install({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\n')
        outputs[A / f'finalize_training_round{number}_v3.py'] = (
            'from explicit_parent_release_engine_v3_20261006 import install\n'
            f'install({number},globals())\n')
        outputs[A / f'run_training_round{number}_v3_pipeline.py'] = (
            'from run_quantile_distribution_views_quality_round_v2_20261006 import main\n'
            f'if __name__=="__main__":main({number})\n')
    for destination, text in outputs.items():
        assert not destination.exists()
        compile(text, str(destination), 'exec')
    for destination, text in outputs.items():
        with destination.open('x', encoding='utf-8') as stream:
            stream.write(text)
    plan = json.loads((A / 'quantile_distribution_views_complete_plan_20261006.json').read_text(encoding='utf-8'))
    plan.update(status='prespecified_full262_record_distribution_quality_grid_before_generator_controls',
        rounds=[93, 94], model_count=6,
        template_sha256={name: sha(A / name) for name in templates},
        generated_source_sha256={path.name: sha(path) for path in outputs})
    path = A / 'quantile_distribution_views_quality_complete_plan_v2_20261006.json'
    with path.open('x', encoding='utf-8') as stream:
        json.dump(plan, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'generated_all_quality_sources_without_modifying_original_grids',
        'quality_rounds': [93, 94], 'records': [124, 138], 'new_native_fits': 0}))


if __name__ == '__main__':
    main()
