"""Generate full GOSS scheme workflows while preserving all frozen source versions."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def transform(text):
    text = text.replace('factorization_machine', 'gradient_sampling')
    for old, new in (
        ('gradient_sampling_scheme_runtime_v2_20261005', 'gradient_sampling_scheme_runtime_20261005'),
        ('gradient_sampling_model_sources_v2_20261005', 'gradient_sampling_model_sources_20261005'),
        ('gradient_sampling_future_qa_v2_20261005', 'gradient_sampling_future_qa_20261005'),
        ('gradient_sampling_search_engine_v4_20261005', 'gradient_sampling_search_engine_20261005'),
        ('predict_gradient_sampling_scheme_codec_v2_20261005', 'predict_gradient_sampling_scheme_codec_20261005'),
        ('predict_gradient_sampling_scheme_v4_20261005', 'predict_gradient_sampling_scheme_20261005'),
        ('verify_gradient_sampling_search_generators_v4_20261005', 'verify_gradient_sampling_search_generators_20261005'),
        ('gradient_sampling_search_generator_preflight_v4_20261005', 'gradient_sampling_search_generator_preflight_20261005'),
        ('gradient_sampling_direct_router_preflight_v2_20261005', 'gradient_sampling_direct_router_preflight_20261005'),
        ('run_gradient_sampling_round_v4_20261005', 'run_gradient_sampling_round_20261005'),
        ('run_gradient_sampling_round_v5_20261005', 'run_gradient_sampling_round_20261005'),
        ('gradient_sampling_quality_run_v5_20261005', 'gradient_sampling_quality_run_20261005'),
        ('gradient_sampling_release_dispatch_preflight_v5_20261005', 'gradient_sampling_search_generator_preflight_20261005'),
        ('passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls',
         'passed_actual_gradient_sampling_maturity_native_reload_and_prefix_controls')):
        text = text.replace(old, new)
    # Round identities and wave ids; the73 initial arms are a count, not a round.
    for old, new in ((73, 75), (74, 76), (297, 304), (298, 305), (299, 306),
                     (300, 307), (301, 308), (302, 309), (303, 310)):
        text = re.sub(rf'(?<!\d){old}(?!\d)', str(new), text)
    text = text.replace('[75,8,18,25]', '[73,8,18,25]').replace('[75, 8, 18, 25]', '[73, 8, 18, 25]')
    text = text.replace('optimize_training_round{number}_v4', 'optimize_training_round{number}')
    text = text.replace('finalize_training_round{number}_v5', 'finalize_training_round{number}')
    text = text.replace('run_training_round{number}_v4_pipeline', 'run_training_round{number}_pipeline')
    text = text.replace("('optimize_training_round', '_v4')", "('optimize_training_round', '')")
    text = text.replace("('run_training_round', '_v4_pipeline')", "('run_training_round', '_pipeline')")
    text = text.replace('actual30_annual6_final32epoch_fits', 'actual30_annual6_final300round_fits')
    return text


def main():
    templates = {
        'gradient_sampling_scheme_runtime_20261005.py': 'factorization_machine_scheme_runtime_v2_20261005.py',
        'gradient_sampling_search_engine_20261005.py': 'factorization_machine_search_engine_v4_20261005.py',
        'predict_gradient_sampling_scheme_codec_20261005.py': 'predict_factorization_machine_scheme_codec_v2_20261005.py',
        'check_gradient_sampling_scheme_20261005.py': 'check_factorization_machine_scheme_20261005.py',
        'run_gradient_sampling_round_20261005.py': 'run_factorization_machine_round_v5_20261005.py',
        'verify_gradient_sampling_search_generators_20261005.py': 'verify_factorization_machine_search_generators_v4_20261005.py'}
    sources = {A / output: transform((A / original).read_text(encoding='utf-8-sig'))
               for output, original in templates.items()}
    sources[A / 'gradient_sampling_model_sources_20261005.py'] = '''"""Directly route GOSS models and preserve all inherited native routes."""
import factorization_machine_model_sources_v2_20261005 as previous
import train_gradient_sampling_bank_20261005 as native
CONFIGS = {**previous.CONFIGS, **native.CONFIGS}
NEW_CONFIGS = native.CONFIGS
YEARS = native.YEARS
read, dump, sha, log = native.read, native.dump, native.sha, native.log
def source_dir(name):
    assert name in CONFIGS
    return native.OUT / name if name in NEW_CONFIGS else previous.source_dir(name)
def model_path(name, year): return source_dir(name) / f'model_{year}.joblib'
def train_one(name, year): return native.train_one(name, year) if name in NEW_CONFIGS else previous.train_one(name, year)
def load_bundle(path): return previous.load_bundle(path)
def predict_arrays(bundle, x, dates=None, valid=None):
    if bundle['kind'] == 'lightgbm_gradient_sampling': return native.predict_arrays(bundle, x)
    return previous.predict_arrays(bundle, x, dates=dates, valid=valid)
def ranker_source(name, output): return output / f'rankers/{name}.npy' if name in NEW_CONFIGS else previous.ranker_source(name, output)
def verify():
    previous.verify(); native.verify()
    assert read(native.OUT / 'oof_audit.json')['status'] == 'passed'
'''
    sources[A / 'gradient_sampling_future_codec_adapter_20261005.py'] = '''"""Add the actual GOSS saved kind above the inherited complete prediction codec."""
def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import train_gradient_sampling_bank_20261005 as native
    from factorization_machine_future_codec_adapter_20261005 import install as install_previous
    restore_previous = install_previous()
    original = legacy.predict_arrays
    def predict_arrays(bundle, x, dates=None, valid=None):
        if bundle['kind'] == 'lightgbm_gradient_sampling': return native.predict_arrays(bundle, x)
        return original(bundle, x, dates=dates, valid=valid)
    legacy.predict_arrays = predict_arrays
    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays = original
        restore_previous()
    return restore
'''
    sources[A / 'predict_gradient_sampling_scheme_20261005.py'] = '''"""Infer from the actual copied complete GOSS scheme and preserved source graph."""
from predict_gradient_sampling_scheme_codec_20261005 import predict
'''
    future = (A / 'verify_linear_leaf_full_future_20261005.py').read_text(encoding='utf-8-sig')
    future = future.replace('linear_leaf', 'gradient_sampling').replace('linear-leaf', 'GOSS')
    future = future.replace('gradient_sampling_actual_resource_sampler_20261005', 'linear_leaf_actual_resource_sampler_20261005')
    sources[A / 'verify_gradient_sampling_full_future_20261005.py'] = future
    for number in (75, 76):
        previous = 74 if number == 75 else 75
        previous_name = 'optimize_training_round74_v4' if number == 75 else 'optimize_training_round75'
        sources[A / f'optimize_training_round{number}.py'] = f'''import sys
import {previous_name} as previous
sys.modules['optimize_training_round{previous}'] = previous
from gradient_sampling_search_engine_20261005 import install
install({number}, globals())
'''
        sources[A / f'finalize_training_round{number}.py'] = f'''"""Freeze and infer the actual complete GOSS round{number}."""
from nystrom_ridge_release_engine_20261004 import install
install({number}, globals())

def predict():
    import optimize_training_round{number} as experiment
    from predict_gradient_sampling_scheme_20261005 import predict as infer
    assert OUT == experiment.OUT
    assert read(OUT / 'causal_validation.json')['status'] == read(OUT / 'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment, selected())
'''
        sources[A / f'run_training_round{number}_pipeline.py'] = f'from run_gradient_sampling_round_20261005 import main\nif __name__ == "__main__": main({number})\n'
    for path, text in sources.items():
        compile(text, str(path), 'exec')
        with path.open('x', encoding='utf-8', newline='') as stream:
            stream.write(text)
    with (A / 'gradient_sampling_workflow_source_generation_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'new_native_codec_and_complete_GOSS_scheme_sources_generated',
            'template_sha256': {str(A / p): hashlib.sha256((A / p).read_bytes()).hexdigest() for p in templates.values()},
            'generated_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'planned_rounds': [75, 76], 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print('Generated16 actual GOSS native/future/complete-scheme source files', flush=True)


if __name__ == '__main__':
    main()
