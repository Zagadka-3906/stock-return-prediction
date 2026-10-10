"""Prepare full native future and complete scheme checks using proven graph engines."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'analysis'


def remap(text):
    text = text.replace('nystrom_tuning', 'neural16384_full')
    text = text.replace('train_neural16384_full_bank_20261005', 'train_neural16384_full_bank_20261005')
    for old, new in ((65, 67), (66, 68), (269, 276), (270, 277), (271, 278),
                     (272, 279), (273, 280), (274, 281), (275, 282)):
        text = re.sub(r'(?<![0-9])' + str(old) + r'(?![0-9])', str(new), text)
    return text


def create(name, text):
    path = HERE / name
    compile(text, str(path), 'exec')
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)
    return str(path), hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    generated = {}
    originals = {}
    pairs = [
        ('nystrom_tuning_scheme_runtime_20261005.py', 'neural16384_full_scheme_runtime_20261005.py'),
        ('nystrom_tuning_search_engine_v2_20261005.py', 'neural16384_full_search_engine_v2_20261005.py'),
        ('run_nystrom_tuning_round_v2_20261005.py', 'run_neural16384_full_round_v2_20261005.py'),
        ('predict_nystrom_tuning_scheme_20261005.py', 'predict_neural16384_full_scheme_20261005.py'),
        ('predict_nystrom_tuning_scheme_v2_20261005.py', 'predict_neural16384_full_scheme_v2_20261005.py'),
        ('check_nystrom_tuning_scheme_20261005.py', 'check_neural16384_full_scheme_20261005.py'),
        ('verify_nystrom_tuning_search_generators_v2_20261005.py', 'verify_neural16384_full_search_generators_v2_20261005.py')]
    for source, target in pairs:
        path = HERE / source
        data = path.read_bytes()
        originals[str(path)] = hashlib.sha256(data).hexdigest()
        text = remap(data.decode('utf-8'))
        if 'search_engine' in target:
            text = text.replace('passed_independent_numerical_and_actual_maturity_controls', 'passed_actual_matched_instrumentation_and_architecture_controls')
            text = text.replace('neural16384_full_preflight_20261005', 'neural16384_full_preflight_20261005')
            text = text.replace('172 if number==67 else 218', '64 if number==67 else 38')
            text = text.replace('[121,8,18,25] if number==67 else [61,140,17]', '[13,8,18,25] if number==67 else [7,14,17]')
            text = text.replace('previous_neural16384_full_bank_actual_annual_fits\':50', 'previous_neural16384_full_bank_actual_annual_fits\':5')
            text = text.replace('new_native_model_configurations\':10', 'new_native_model_configurations\':1')
            text = text.replace('all10_new_native_models', 'all1_new_native_model')
        if target == 'run_neural16384_full_round_v2_20261005.py':
            text = text.replace('actual50_annual10_final', 'actual5_annual1_final')
            text = text.replace("'native_configs': 10", "'native_configs': 1")
            text = text.replace('新增核模型', '16384宽度模型').replace('扩大核规模、长度尺度与正则强度的成熟样本Nyström核模型', '匹配参数的16384宽度成熟样本神经网络完整方案')
        if target == 'predict_neural16384_full_scheme_20261005.py':
            text = text.replace('neural16384_full_search_engine_20261005.py', 'neural16384_full_search_engine_v2_20261005.py')
        if target == 'check_neural16384_full_scheme_20261005.py':
            text = text.replace('all10_new_models_checked', 'all1_new_model_checked')
        if 'verify_neural16384_full_search_generators' in target:
            text = text.replace('[121, 8, 18, 25] if number == 67 else [61, 140, 17]', '[13, 8, 18, 25] if number == 67 else [7, 14, 17]')
            text = text.replace('172 if number == 67 else 218', '64 if number == 67 else 38')
            text = text.replace('actual_R64_and_R65', 'actual_R66_and_R67')
            text = text.replace("'*neural16384_full*.py'", "'*neural16384*20261005.py'")
        generated.update([create(target, text)])
    router = '''"""Route the one full16384 MLP and all earlier accepted native models."""
import nystrom_tuning_model_sources_20261005 as previous
import train_neural16384_full_bank_20261005 as native
CONFIGS={**previous.CONFIGS,**native.CONFIGS}
NEW_CONFIGS=native.CONFIGS
YEARS=native.YEARS
read,dump,sha,log=native.read,native.dump,native.sha,native.log
def source_dir(name):
    assert name in CONFIGS
    return native.OUT/name if name in NEW_CONFIGS else previous.source_dir(name)
def model_path(name,year):return source_dir(name)/f'model_{year}.joblib'
def train_one(name,year):return native.engine.train_one(name,year) if name in NEW_CONFIGS else previous.train_one(name,year)
def load_bundle(path):return previous.load_bundle(path)
def predict_arrays(bundle,x,dates=None,valid=None):
    if bundle.get('config',{}).get('hidden')==[16384,8192,4096]:return native.engine.predict_arrays(bundle,x)
    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)
def ranker_source(name,output):return output/f'rankers/{name}.npy' if name in NEW_CONFIGS else previous.ranker_source(name,output)
def verify():
    previous.verify();native.verify()
    assert read(native.OUT/'oof_audit.json')['status']=='passed'
'''
    generated.update([create('neural16384_full_model_sources_20261005.py', router)])
    generated.update([create('optimize_training_round67_v2.py', 'import sys\nimport optimize_training_round66_v2 as previous\nsys.modules["optimize_training_round66"] = previous\nfrom neural16384_full_search_engine_v2_20261005 import install\ninstall(67, globals())\n')])
    generated.update([create('optimize_training_round68_v2.py', 'import sys\nimport optimize_training_round67_v2 as previous\nsys.modules["optimize_training_round67"] = previous\nfrom neural16384_full_search_engine_v2_20261005 import install\ninstall(68, globals())\n')])
    for number in (67, 68):
        generated.update([create(f'optimize_training_round{number}.py', f'from optimize_training_round{number}_v2 import *\n')])
        generated.update([create(f'run_training_round{number}_v2_pipeline.py', f'from run_neural16384_full_round_v2_20261005 import main\nif __name__ == "__main__": main({number})\n')])
        text = remap((HERE / f'finalize_training_round{number-2}.py').read_text(encoding='utf-8'))
        generated.update([create(f'finalize_training_round{number}.py', text)])
    plan = {'status': 'prepared_actual_full16384_controls_required_before_official_quality',
        'model_configurations': {'rank16384_drop000_seed07_e32': {
            'kind': 'mlp', 'target': 'y_rank', 'batch_size': 32768, 'learning_rate': .001,
            'weight_decay': .0001, 'dropout': 0., 'hidden': [16384,8192,4096], 'epochs':32, 'seed':20261007}},
        'actual_previous_selection_required': {'67':66, '68':67}, 'expected_annual_fits':5,
        'expected_final_mature_fits':1, 'expected_total_records':{'67':64,'68':38},
        'wave_arm_counts':{'67':[13,8,18,25],'68':[7,14,17]},
        'waves':{'67':[276,277,278,279],'68':[280,281,282]},
        'preserves_actual_latest_graph_and_inherited_agreement_gates':True,
        'full_annual_fit_not_replaced_by_pilots':True,'test_labels_read':False,
        'all_years_reused_selection_bias_uncorrected':True,'global_resource_exhaustion_established':False}
    with (HERE / 'neural16384_full_complete_search_plan_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump(plan, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with (HERE / 'neural16384_full_source_generation_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump({'status':'sources_prepared_before_generator_and_actual_full_fit_checks',
            'original_sources_preserved_sha256':originals,'generated_source_sha256':generated,
            'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'prepared','new_sources':len(generated),'quality_records':102},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
