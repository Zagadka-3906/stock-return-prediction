"""Derive two complete six-composite searches from the verified explicit graph driver."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, data):
    with Path(path).open('x', encoding='utf-8') as stream:
        if isinstance(data, str):
            stream.write(data)
        else:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


def adapt(text):
    numbers = {86: 88, 87: 89, 88: 90, **{n: n+7 for n in range(346, 353)}}
    text = re.sub(r'\b(?:86|87|88|346|347|348|349|350|351|352)\b',
                  lambda match: str(numbers[int(match.group())]), text)
    text = text.replace('ready_robust_reference_', 'ready_classifier_consensus_reference_')
    text = re.sub(r'(ready_classifier_consensus_reference_[a-z_]+)_20261005', r'\1_20261006', text)
    text = text.replace('streaming_robust_regression_scheme_runtime_20261005', 'classifier_consensus_scheme_runtime_20261006')
    text = text.replace('streaming_robust_regression_', 'classifier_consensus_')
    text = text.replace('streaming_robust_regression', 'classifier_consensus')
    text = text.replace('train_classifier_consensus_bank_20261005', 'build_classifier_consensus_bank_20261005')
    return text


def main():
    originals = {name: sha(A / name) for name in (
        'streaming_robust_regression_scheme_runtime_20261005.py',
        'ready_robust_reference_search_engine_20261005.py',
        'run_ready_robust_reference_round_20261005.py',
        'check_ready_robust_reference_scheme_20261005.py')}
    outputs = {}
    runtime = adapt((A / 'streaming_robust_regression_scheme_runtime_20261005.py').read_text(encoding='utf-8'))
    runtime = runtime.replace('"""Extend orreplace explicit complete graphs with the Nyström kernel ridge models."""',
                              '"""Replay complete fixed-consensus graph roles and independent standalone outputs."""')
    outputs['classifier_consensus_scheme_runtime_20261006.py'] = runtime
    engine = adapt((A / 'ready_robust_reference_search_engine_20261005.py').read_text(encoding='utf-8'))
    engine = engine.replace("'passed_actual_streamed_robust_regression_maturity_native_reload_and_prefix_controls'",
                            "'passed_actual_native_parent_consensus_reload_and_prefix'")
    engine = engine.replace("'passed_actual_streamed_classifier_consensus_maturity_native_reload_and_prefix_controls'",
                            "'passed_actual_native_parent_consensus_reload_and_prefix'")
    engine = engine.replace("assert ns.read(path)['status']=='passed',path", "assert ns.read(path)['status']=='passed',path")
    engine = engine.replace("gates=[bank.OUT/'oof_audit.json',", "gates=[bank.OUT/'construction_execution_scope.json',bank.OUT/'oof_audit.json',")
    engine = engine.replace("for path in gates:assert ns.read(path)['status']=='passed',path",
        "for path in gates:assert ns.read(path)['status']=='passed',path\n"
        "        assert ns.read(bank.OUT/'oof_audit.json')['actual_virtual_annual_outputs']==30\n"
        "        assert ns.read(ROOT/'analysis/classifier_consensus_future_qa_20261005/verification.json')['actual_virtual_final_artifacts']==6")
    engine = engine.replace("'expected_scored_records':100 if number==89 else 98", "'expected_scored_records':124 if number==89 else 138")
    engine = engine.replace("'wave_arm_counts':[49,8,18,25] if number==89 else [25,56,17]", "'wave_arm_counts':[73,8,18,25] if number==89 else [37,84,17]")
    engine = engine.replace("'previous_classifier_consensus_bank_actual_annual_fits':20", "'reused_unique_native_classifier_annual_fits':20,'actual_virtual_annual_outputs':30")
    engine = engine.replace("'existing_native_configurations_reused':4", "'existing_native_configurations_reused':4,'new_fixed_composites':6")
    engine = engine.replace("cfg.get('kind')=='neural_ensemble'", "cfg.get('kind') in ('neural_ensemble','linear_leaf_ensemble','classifier_consensus')")
    engine = engine.replace('all4_new_native_models_cold_prefix_andpoisoning_controls', 'all6_fixed_composites_cold_prefix_andpoisoning_controls')
    engine = engine.replace('mature streamed regression complete graph', 'fixed classifier consensus complete graph')
    engine = engine.replace("ROOT/'analysis/classifier_consensus_20261005.py'", "ROOT/'analysis/streaming_rank_classification_v3_20261005.py'")
    outputs['ready_classifier_consensus_reference_search_engine_20261006.py'] = engine
    driver = adapt((A / 'run_ready_robust_reference_round_20261005.py').read_text(encoding='utf-8'))
    driver = driver.replace('waiting_for_qualified_R86_R87_and_actual20_annual4_final32pass_regression_controls',
                            'waiting_for_qualified_R88_R89_and_actual30_virtual_annual6_fullfuture_controls')
    driver = driver.replace('classifier_consensus_storage_20261005.json', 'classifier_consensus_storage_20261006.json')
    driver = driver.replace("'native_configs': 4", "'fixed_composites': 6, 'new_native_fits': 0")
    driver = driver.replace('成熟原始特征鲁棒线性回归模型完整方案', '固定分类集成完整方案')
    outputs['run_ready_classifier_consensus_reference_round_20261006.py'] = driver
    checks = adapt((A / 'check_ready_robust_reference_scheme_20261005.py').read_text(encoding='utf-8'))
    checks = checks.replace('all4_new_models_checked', 'all6_fixed_composites_checked')
    outputs['check_ready_classifier_consensus_reference_scheme_20261006.py'] = checks
    for number in (89, 90):
        outputs[f'optimize_training_round{number}_v2.py'] = (
            f'import sys\nimport optimize_training_round{number-1}_v2\n'
            'from ready_classifier_consensus_reference_search_engine_20261006 import install\n'
            f'install({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\n')
        outputs[f'finalize_training_round{number}_v2.py'] = (
            'from explicit_parent_release_engine_v2_20261005 import install\n'
            f'install({number},globals())\n')
        outputs[f'run_training_round{number}_v2_pipeline.py'] = (
            'from run_ready_classifier_consensus_reference_round_20261006 import main\n'
            f'if __name__ == "__main__":main({number})\n')
    for name, text in outputs.items():
        compile(text, str(A / name), 'exec')
        create(A / name, text)
    native_plan = json.loads((A / 'classifier_consensus_complete_search_plan_20261005.json').read_text(encoding='utf-8'))
    create(A / 'ready_classifier_consensus_reference_complete_plan_20261006.json', {
        **native_plan, 'quality_sources_implementation_and_preflight_still_pending': True,
        'quality_source_files_generated': list(outputs), 'generator_controls_still_required': True,
        'native_plan_sha256': sha(A / 'classifier_consensus_complete_search_plan_20261005.json'),
        'original_template_source_sha256': originals})
    create(A / 'classifier_consensus_storage_20261006.json', {
        'output_directory': str(A / 'classifier_consensus_bank_20261005'),
        'temporary_directory': str(ROOT / 'tmp/classifier_consensus_quality_20261006'),
        'new_project_files_D_or_E_only': True})
    create(A / 'classifier_consensus_quality_source_generation_20261006.json', {
        'status': 'generated_complete262_record_quality_sources_before_controls',
        'original_templates_sha256': originals,
        'generated_sha256': {name: sha(A / name) for name in outputs},
        'actual_official_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'generated_complete_quality_sources', 'rounds': [89, 90],
                      'source_files': len(outputs)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
