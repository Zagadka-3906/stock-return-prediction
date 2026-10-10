"""Preserve proven latest graph semantics and extend complete searches to six trees."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'analysis'


def remap(text):
    text = text.replace('neural16384_full', 'linear_leaf')
    for old, new in ((67, 69), (68, 70), (276, 283), (277, 284), (278, 285),
                     (279, 286), (280, 287), (281, 288), (282, 289)):
        text = re.sub(r'(?<![0-9])' + str(old) + r'(?![0-9])', str(new), text)
    return text


def create(name, text):
    path = HERE / name
    compile(text, str(path), 'exec')
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)
    return str(path), hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    generated, originals = {}, {}
    pairs = [
        ('neural16384_full_scheme_runtime_20261005.py', 'linear_leaf_scheme_runtime_20261005.py'),
        ('neural16384_full_search_engine_v2_20261005.py', 'linear_leaf_search_engine_v2_20261005.py'),
        ('run_neural16384_full_round_v2_20261005.py', 'run_linear_leaf_round_v2_20261005.py'),
        ('predict_neural16384_full_scheme_20261005.py', 'predict_linear_leaf_scheme_20261005.py'),
        ('predict_neural16384_full_scheme_v2_20261005.py', 'predict_linear_leaf_scheme_v2_20261005.py'),
        ('check_neural16384_full_scheme_20261005.py', 'check_linear_leaf_scheme_20261005.py'),
        ('verify_neural16384_full_search_generators_v2_20261005.py', 'verify_linear_leaf_search_generators_v2_20261005.py')]
    for source, target in pairs:
        path = HERE / source
        data = path.read_bytes()
        originals[str(path)] = hashlib.sha256(data).hexdigest()
        text = remap(data.decode('utf-8'))
        if 'search_engine' in target:
            text = text.replace('passed_actual_matched_instrumentation_and_architecture_controls',
                'passed_actual_linear_leaf_maturity_native_reload_and_prefix_controls')
            text = text.replace('64 if number==69 else 38', '124 if number==69 else 138')
            text = text.replace('[13,8,18,25] if number==69 else [7,14,17]', '[73,8,18,25] if number==69 else [37,84,17]')
            text = text.replace("previous_linear_leaf_bank_actual_annual_fits':5", "previous_linear_leaf_bank_actual_annual_fits':30")
            text = text.replace("new_native_model_configurations':1", "new_native_model_configurations':6")
            text = text.replace('all1_new_native_model', 'all6_new_native_models')
            text = text.replace('expanded kernel complete graph', 'matched constant andlinear leaf complete graph')
            text = text.replace("ROOT/'analysis/nystrom_future_codec_adapter_20261005.py',",
                "ROOT/'analysis/nystrom_future_codec_adapter_20261005.py',ROOT/'analysis/linear_leaf_future_codec_adapter_20261005.py',")
        if 'run_linear_leaf_round' in target:
            text = text.replace('actual5_annual1_final', 'actual30_annual6_final')
            text = text.replace("'native_configs': 1", "'native_configs': 6")
            text = text.replace('16384宽度模型', '普通树叶与线性树叶模型')
            text = text.replace('匹配参数的16384宽度成熟样本神经网络完整方案', '匹配参数的普通树叶与线性树叶LightGBM完整方案')
        if target == 'predict_linear_leaf_scheme_20261005.py':
            text = text.replace('from nystrom_future_codec_adapter_20261005 import install',
                'from linear_leaf_future_codec_adapter_20261005 import install')
            text = text.replace("'agreement_gated_weights_20261005.py', 'nystrom_future_codec_adapter_20261005.py',",
                "'agreement_gated_weights_20261005.py', 'nystrom_future_codec_adapter_20261005.py', 'linear_leaf_future_codec_adapter_20261005.py',")
        if 'check_linear_leaf' in target:
            text = text.replace('all1_new_model_checked', 'all6_new_models_checked')
        if 'verify_linear_leaf_search_generators' in target:
            text = text.replace('[13, 8, 18, 25] if number == 69 else [7, 14, 17]', '[73, 8, 18, 25] if number == 69 else [37, 84, 17]')
            text = text.replace('64 if number == 69 else 38', '124 if number == 69 else 138')
            text = text.replace("'*neural16384*20261005.py'", "'*linear_leaf*20261005.py'")
            text = text.replace('actual_R64_and_R69', 'actual_R68_and_R69')
        generated.update([create(target, text)])
    router = '''"""Route matched LightGBM leaf models and every inherited native family."""
import neural16384_full_model_sources_20261005 as previous
import train_linear_leaf_bank_20261005 as native
CONFIGS={**previous.CONFIGS,**native.CONFIGS}
NEW_CONFIGS=native.CONFIGS
YEARS=native.YEARS
read,dump,sha,log=native.read,native.dump,native.sha,native.log
def source_dir(name):
    assert name in CONFIGS
    return native.OUT/name if name in NEW_CONFIGS else previous.source_dir(name)
def model_path(name,year):return source_dir(name)/f'model_{year}.joblib'
def train_one(name,year):return native.train_one(name,year) if name in NEW_CONFIGS else previous.train_one(name,year)
def load_bundle(path):return previous.load_bundle(path)
def predict_arrays(bundle,x,dates=None,valid=None):
    if bundle['kind']=='lightgbm_linear_leaf':return native.predict_arrays(bundle,x)
    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)
def ranker_source(name,output):return output/f'rankers/{name}.npy' if name in NEW_CONFIGS else previous.ranker_source(name,output)
def verify():
    previous.verify();native.verify()
    assert read(native.OUT/'oof_audit.json')['status']=='passed'
'''
    generated.update([create('linear_leaf_model_sources_20261005.py', router)])
    for number in (69, 70):
        previous = number - 1
        text = (f'import sys\nimport optimize_training_round{previous}_v2 as previous\n'
                f'sys.modules["optimize_training_round{previous}"] = previous\n'
                f'from linear_leaf_search_engine_v2_20261005 import install\ninstall({number}, globals())\n')
        generated.update([create(f'optimize_training_round{number}_v2.py', text)])
        generated.update([create(f'optimize_training_round{number}.py', f'from optimize_training_round{number}_v2 import *\n')])
        generated.update([create(f'run_training_round{number}_v2_pipeline.py',
            f'from run_linear_leaf_round_v2_20261005 import main\nif __name__ == "__main__": main({number})\n')])
        generated.update([create(f'finalize_training_round{number}.py',
            remap((HERE / f'finalize_training_round{number-2}.py').read_text(encoding='utf-8')))])
    import train_linear_leaf_bank_20261005 as bank
    plan = {'status': 'prespecified_actual_linear_leaf_fits_and_complete_quality_grid',
        'model_configurations': bank.CONFIGS, 'actual_previous_selection_required': {'69': 68, '70': 69},
        'expected_annual_fits': 30, 'expected_final_mature_fits': 6,
        'expected_total_records': {'69': 124, '70': 138},
        'wave_arm_counts': {'69': [73,8,18,25], '70': [37,84,17]},
        'waves': {'69': [283,284,285,286], '70': [287,288,289]},
        'matched_leaf_grid_only_no_validation_early_stopping': True,
        'preserves_actual_latest_graph_and_inherited_agreement_gates': True,
        'actual30_annual_and6_final_fits_not_replaced_by_pilots': True,
        'test_labels_read': False, 'all_years_reused_selection_bias_uncorrected': True,
        'global_resource_exhaustion_established': False}
    with (HERE / 'linear_leaf_complete_search_plan_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump(plan, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with (HERE / 'linear_leaf_source_generation_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'prepared_before_actual_complete_quality_checks',
            'original_sources_preserved_sha256': originals, 'generated_source_sha256': generated,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'prepared', 'new_sources': len(generated),
        'expected_official_quality_records': 262}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
