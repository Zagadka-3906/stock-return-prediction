"""Preserve proven latest graph semantics and extend complete searches to six trees."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'analysis'


def remap(text):
    text = text.replace('neural16384_full', 'factorization_machine')
    for old, new in ((67, 73), (68, 74), (276, 297), (277, 298), (278, 299),
                     (279, 300), (280, 301), (281, 302), (282, 303)):
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
        ('neural16384_full_scheme_runtime_20261005.py', 'factorization_machine_scheme_runtime_20261005.py'),
        ('neural16384_full_search_engine_v2_20261005.py', 'factorization_machine_search_engine_v2_20261005.py'),
        ('run_neural16384_full_round_v2_20261005.py', 'run_factorization_machine_round_v2_20261005.py'),
        ('predict_neural16384_full_scheme_20261005.py', 'predict_factorization_machine_scheme_20261005.py'),
        ('predict_neural16384_full_scheme_v2_20261005.py', 'predict_factorization_machine_scheme_v2_20261005.py'),
        ('check_neural16384_full_scheme_20261005.py', 'check_factorization_machine_scheme_20261005.py'),
        ('verify_neural16384_full_search_generators_v2_20261005.py', 'verify_factorization_machine_search_generators_v2_20261005.py')]
    for source, target in pairs:
        path = HERE / source
        data = path.read_bytes()
        originals[str(path)] = hashlib.sha256(data).hexdigest()
        text = remap(data.decode('utf-8'))
        if 'search_engine' in target:
            text = text.replace('passed_actual_matched_instrumentation_and_architecture_controls',
                'passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls')
            text = text.replace('64 if number==73 else 38', '124 if number==73 else 138')
            text = text.replace('[13,8,18,25] if number==73 else [7,14,17]', '[73,8,18,25] if number==73 else [37,84,17]')
            text = text.replace("previous_factorization_machine_bank_actual_annual_fits':5", "previous_factorization_machine_bank_actual_annual_fits':30")
            text = text.replace("new_native_model_configurations':1", "new_native_model_configurations':6")
            text = text.replace('all1_new_native_model', 'all6_new_native_models')
            text = text.replace('expanded kernel complete graph', 'first order andlow rank feature interaction complete graph')
            text = text.replace("ROOT/'analysis/nystrom_future_codec_adapter_20261005.py',",
                "ROOT/'analysis/nystrom_future_codec_adapter_20261005.py',ROOT/'analysis/factorization_machine_future_codec_adapter_20261005.py',")
        if 'run_factorization_machine_round' in target:
            text = text.replace('actual5_annual1_final', 'actual30_annual6_final')
            text = text.replace("'native_configs': 1", "'native_configs': 6")
            text = text.replace('一阶与二阶因子分解模型', '一阶与二阶因子分解模型')
            text = text.replace('匹配参数的16384宽度成熟样本神经网络完整方案', '匹配参数的成熟特征因子分解机完整方案')
        if target == 'predict_factorization_machine_scheme_20261005.py':
            text = text.replace('from nystrom_future_codec_adapter_20261005 import install',
                'from factorization_machine_future_codec_adapter_20261005 import install')
            text = text.replace("'agreement_gated_weights_20261005.py', 'nystrom_future_codec_adapter_20261005.py',",
                "'agreement_gated_weights_20261005.py', 'nystrom_future_codec_adapter_20261005.py', 'factorization_machine_future_codec_adapter_20261005.py',")
        if 'check_factorization_machine' in target:
            text = text.replace('all1_new_model_checked', 'all6_new_models_checked')
        if 'verify_factorization_machine_search_generators' in target:
            text = text.replace('[13, 8, 18, 25] if number == 73 else [7, 14, 17]', '[73, 8, 18, 25] if number == 73 else [37, 84, 17]')
            text = text.replace('64 if number == 73 else 38', '124 if number == 73 else 138')
            text = text.replace("'*neural16384*20261005.py'", "'*factorization_machine*20261005.py'")
            text = text.replace('actual_R64_and_R73', 'actual_R72_and_R73')
        generated.update([create(target, text)])
    router = '''"""Route matched LightGBM leaf models and every inherited native family."""
import linear_leaf_ensemble_model_sources_20261005 as previous
import train_factorization_machine_bank_20261005 as native
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
    if bundle['kind']=='lightgbm_factorization_machine':return native.predict_arrays(bundle,x)
    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)
def ranker_source(name,output):return output/f'rankers/{name}.npy' if name in NEW_CONFIGS else previous.ranker_source(name,output)
def verify():
    previous.verify();native.verify()
    assert read(native.OUT/'oof_audit.json')['status']=='passed'
'''
    generated.update([create('factorization_machine_model_sources_20261005.py', router)])
    for number in (73, 74):
        previous = number - 1
        text = (f'import sys\nimport optimize_training_round{previous}_v2 as previous\n'
                f'sys.modules["optimize_training_round{previous}"] = previous\n'
                f'from factorization_machine_search_engine_v2_20261005 import install\ninstall({number}, globals())\n')
        generated.update([create(f'optimize_training_round{number}_v2.py', text)])
        generated.update([create(f'optimize_training_round{number}.py', f'from optimize_training_round{number}_v2 import *\n')])
        generated.update([create(f'run_training_round{number}_v2_pipeline.py',
            f'from run_factorization_machine_round_v2_20261005 import main\nif __name__ == "__main__": main({number})\n')])
        generated.update([create(f'finalize_training_round{number}.py',
            remap((HERE / f'finalize_training_round{number-2}.py').read_text(encoding='utf-8')))])
    import train_factorization_machine_bank_20261005 as bank
    plan = {'status': 'prespecified_actual_factorization_machine_fits_and_complete_quality_grid',
        'model_configurations': bank.CONFIGS, 'actual_previous_selection_required': {'73': 68, '74': 73},
        'expected_annual_fits': 30, 'expected_final_mature_fits': 6,
        'expected_total_records': {'73': 124, '74': 138},
        'wave_arm_counts': {'73': [73,8,18,25], '74': [37,84,17]},
        'waves': {'73': [297,298,299,300], '74': [301,302,303]},
        'matched_factor_rank_grid_only_no_validation_early_stopping': True,
        'preserves_actual_latest_graph_and_inherited_agreement_gates': True,
        'actual30_annual_and6_final32epoch_fits_not_replaced_by_pilots': True,
        'test_labels_read': False, 'all_years_reused_selection_bias_uncorrected': True,
        'global_resource_exhaustion_established': False}
    with (HERE / 'factorization_machine_complete_search_plan_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump(plan, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with (HERE / 'factorization_machine_source_generation_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'prepared_before_actual_complete_quality_checks',
            'original_sources_preserved_sha256': originals, 'generated_source_sha256': generated,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'prepared', 'new_sources': len(generated),
        'expected_official_quality_records': 262}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
