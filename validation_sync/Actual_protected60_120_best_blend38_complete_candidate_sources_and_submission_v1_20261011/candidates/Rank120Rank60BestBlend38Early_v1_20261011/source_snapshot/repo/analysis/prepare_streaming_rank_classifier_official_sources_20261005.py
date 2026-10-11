"""Prepare full classification role and standalone comparisons without old edits."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(path, body):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(body if isinstance(body, str) else json.dumps(body, ensure_ascii=False, indent=2)+'\n')


def transform(body):
    body = body.replace('memory_efficient_neural', 'streaming_rank_classifier')
    mapping = {77:79, 78:80, 311:318, 312:319, 313:320, 314:321, 315:322, 316:323, 317:324}
    body = re.sub(r'(?<!\d)(77|78|311|312|313|314|315|316|317)(?!\d)',
                  lambda match: str(mapping[int(match.group())]), body)
    body = body.replace('train_streaming_rank_classifier_bank_20261005', 'train_streaming_rank_classifier_bank_v3_20261005')
    body = body.replace('streaming_rank_classifier_future_qa_20261005', 'streaming_rank_classifier_future_qa_v3_20261005')
    body = body.replace('streaming_rank_classifier_storage_20261005', 'streaming_rank_classifier_storage_v3_20261005')
    body = body.replace('streaming_rank_classifier_complete_search_plan_20261005', 'streaming_rank_classifier_official_search_plan_20261005')
    body = body.replace('memory_efficient_mlp_preflight_20261005', 'streaming_rank_classification_preflight_v3_20261005')
    body = body.replace('memory_efficient_mlp_20261005', 'streaming_rank_classification_v3_20261005')
    body = body.replace('passed_actual_gradients_saved_tensors_and_mature_CPU_pilots',
                        'passed_actual_streamed_rank_classification_maturity_native_reload_and_prefix_controls')
    body = body.replace('actual15_annual3_final', 'actual20_annual4_final')
    body = body.replace("'native_configs': 3", "'native_configs': 4")
    body = body.replace("'previous_streaming_rank_classifier_bank_actual_annual_fits':15", "'previous_streaming_rank_classifier_bank_actual_annual_fits':20")
    body = body.replace("'new_native_model_configurations':3", "'new_native_model_configurations':4")
    body = body.replace('all3_new_native_models', 'all4_new_native_models').replace('all3_new_models_checked', 'all4_new_models_checked')
    body = body.replace('88 if number==79 else 78', '100 if number==79 else 98')
    body = body.replace('88 if number == 79 else 78', '100 if number == 79 else 98')
    body = body.replace('[37,8,18,25] if number==79 else [19,42,17]', '[49,8,18,25] if number==79 else [25,56,17]')
    body = body.replace('[37, 8, 18, 25] if number == 79 else [19, 42, 17]', '[49, 8, 18, 25] if number == 79 else [25, 56, 17]')
    body = body.replace('actual_R76_and_R79', 'actual_R78_and_R79')
    body = body.replace('16384宽度模型三种用途对照', '成熟排序分类模型三种用途对照')
    body = body.replace('匹配参数的匹配预算的16384宽度内存优化神经网络完整方案', '成熟排序分类及集成后处理完整方案')
    return body


def main():
    original = json.loads((A / 'streaming_rank_classifier_complete_search_plan_20261005.json').read_text(encoding='utf-8'))
    create(A / 'streaming_rank_classifier_official_search_plan_20261005.json', {
        'status': 'complete_official_sources_prepared_before_generator_and_route_controls',
        'original_prospective_plan_sha256': sha(A / 'streaming_rank_classifier_complete_search_plan_20261005.json'),
        'model_configurations': original['model_configurations'],
        'actual_complete_previous_round_required': {'79':78, '80':79},
        'expected_annual_fits': 20, 'expected_final_mature_fits': 4,
        'expected_total_records': {'79':100, '80':98},
        'wave_arm_counts': {'79':[49,8,18,25], '80':[25,56,17]},
        'waves': {'79':[318,319,320,321], '80':[322,323,324]},
        'classification_scores_mapped_to_one_day_returns_using_mature_past_only': True,
        'same5635800_rows1212_continuous_days_and_official_S_only': True,
        'reused_validation_years_selection_bias_uncorrected': True,
        'test_labels_read': False, 'new_quality_scores': 0,
        'global_resource_exhaustion_established': False})
    sources, templates = {}, {}
    for stem in ('scheme_runtime', 'search_engine', 'run_round', 'check_scheme', 'verify_search_generators'):
        old = {'run_round':'run_memory_efficient_neural_round_20261005.py',
               'check_scheme':'check_memory_efficient_neural_scheme_20261005.py',
               'verify_search_generators':'verify_memory_efficient_neural_search_generators_20261005.py'}.get(
                   stem, f'memory_efficient_neural_{stem}_20261005.py')
        target = old.replace('memory_efficient_neural', 'streaming_rank_classifier')
        templates[str(A / old)] = sha(A / old)
        body = transform((A / old).read_text(encoding='utf-8'))
        if stem == 'search_engine':
            body = body.replace("proof,*gates]", "proof,*gates,\n            ROOT/'analysis/streaming_rank_classifier_future_codec_adapter_20261005.py',\n            ROOT/'analysis/predict_streaming_rank_classifier_scheme_codec_20261005.py',\n            ROOT/'analysis/streaming_rank_classifier_quality_run_20261005.json',\n            ROOT/'analysis/streaming_rank_classifier_direct_router_preflight_20261005/verification.json',\n            ROOT/'analysis/streaming_rank_classifier_execution_source_preflight_20261005/verification.json']")
        sources[A / target] = body
    sources[A / 'streaming_rank_classifier_model_sources_20261005.py'] = '''"""Route all mature classifiers and preserve every inherited typed native model."""
import memory_efficient_neural_model_sources_20261005 as previous
import train_streaming_rank_classifier_bank_v3_20261005 as native
CONFIGS = {**previous.CONFIGS, **native.CONFIGS}
NEW_CONFIGS, YEARS = native.CONFIGS, native.YEARS
read, dump, sha, log = native.read, native.dump, native.sha, native.log
def source_dir(name):
    assert name in CONFIGS
    return native.OUT/name if name in NEW_CONFIGS else previous.source_dir(name)
def model_path(name, year): return source_dir(name)/f'model_{year}.joblib'
def train_one(name, year): return native.train_one(name,year) if name in NEW_CONFIGS else previous.train_one(name,year)
def load_bundle(path): return native.core.load_bundle(path)
def predict_arrays(bundle,x,dates=None,valid=None):
    if bundle.get('kind') == 'streaming_rank_classifier': return native.core.predict_arrays(bundle,x)
    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)
def ranker_source(name,output): return output/f'rankers/{name}.npy' if name in NEW_CONFIGS else previous.ranker_source(name,output)
def verify():
    previous.verify(); native.verify()
    assert read(native.OUT/'oof_audit.json')['status'] == 'passed'
'''
    sources[A / 'streaming_rank_classifier_future_codec_adapter_20261005.py'] = '''"""Install classification above all inherited complete future model codecs."""
def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import train_streaming_rank_classifier_bank_v3_20261005 as native
    from memory_efficient_neural_future_codec_adapter_20261005 import install as install_previous
    restore_previous = install_previous()
    original = legacy.predict_arrays
    def predict_arrays(bundle,x,dates=None,valid=None):
        if bundle.get('kind') == 'streaming_rank_classifier': return native.core.predict_arrays(bundle,x)
        return original(bundle,x,dates=dates,valid=valid)
    legacy.predict_arrays = predict_arrays
    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays = original
        restore_previous()
    return restore
'''
    sources[A / 'predict_streaming_rank_classifier_scheme_codec_20261005.py'] = '''"""Infer the complete mapped classification graph and retain actual entrypoints."""
from pathlib import Path
import hashlib
import json

def copy_actual_sources(ns,candidate):
    candidate = Path(candidate).resolve()
    assert candidate.drive.upper() in ('D:', 'E:') and ns.NUMBER in (79,80)
    assert not (candidate/'manifest.json').exists(), 'Published candidate is immutable.'
    names = ('agreement_gated_weights_20261005.py', 'nystrom_future_codec_adapter_20261005.py',
        'streaming_rank_classifier_future_codec_adapter_20261005.py',
        'streaming_rank_classifier_model_sources_20261005.py', 'streaming_rank_classifier_scheme_runtime_20261005.py',
        'streaming_rank_classifier_search_engine_20261005.py', 'predict_streaming_rank_classifier_scheme_20261005.py',
        'check_streaming_rank_classifier_scheme_20261005.py', f'optimize_training_round{ns.NUMBER}.py',
        f'finalize_training_round{ns.NUMBER}.py', f'run_training_round{ns.NUMBER}_pipeline.py',
        'run_streaming_rank_classifier_round_20261005.py', 'streaming_rank_classification_v3_20261005.py',
        'train_streaming_rank_classifier_bank_v3_20261005.py', 'run_streaming_rank_classifier_bank_v3_20261005.py',
        'verify_streaming_rank_classifier_full_future_v3_20261005.py', Path(__file__).name)
    candidate.mkdir(parents=True,exist_ok=True)
    files = {}
    for name in names:
        source = ns.ROOT/'analysis'/name
        data, target = source.read_bytes(), candidate/name
        if target.exists():
            assert target.read_bytes() == data, name
        else:
            with target.open('xb') as stream: stream.write(data)
        files[name] = {'project_source':str(source),'sha256':hashlib.sha256(data).hexdigest()}
    record = {'status':'passed','round':ns.NUMBER,'files':files,
        'actual_pipeline':f'run_training_round{ns.NUMBER}_pipeline.py',
        'actual_driver':'run_streaming_rank_classifier_round_20261005.py',
        'actual_canonical_release':f'finalize_training_round{ns.NUMBER}.py',
        'same_actual_pipeline_and_canonical_release':True,'test_labels_read':False}
    data = (json.dumps(record,ensure_ascii=False,indent=2)+'\\n').encode('utf-8')
    path = candidate/'actual_execution_sources.json'
    if path.exists(): assert path.read_bytes() == data
    else:
        with path.open('xb') as stream: stream.write(data)
    return record

def predict(ns,record,candidate_path=None,mapping_path=None):
    import whole_scheme_future_runtime_20261004 as runtime
    from predict_nystrom_ridge_scheme_20261004 import predict as original
    from streaming_rank_classifier_future_codec_adapter_20261005 import install
    from agreement_gated_weights_20261005 import context_weight
    candidate = Path(candidate_path) if candidate_path is not None else ns.ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    copy_actual_sources(ns,candidate)
    original_weights = runtime.FutureContext.weights_for
    restore = install()
    def weights_for(context,spec): return context_weight(context,spec,original_weights(context,spec))
    runtime.FutureContext.weights_for = weights_for
    try: original(ns,record,candidate_path=candidate,mapping_path=mapping_path)
    finally:
        runtime.FutureContext.weights_for = original_weights
        restore()
    assert runtime.FutureContext.weights_for is original_weights
    copy_actual_sources(ns,candidate)
'''
    sources[A / 'predict_streaming_rank_classifier_scheme_20261005.py'] = 'from predict_streaming_rank_classifier_scheme_codec_20261005 import predict\n'
    for number in (79,80):
        sources[A / f'optimize_training_round{number}.py'] = f'from streaming_rank_classifier_search_engine_20261005 import install\ninstall({number},globals())\n'
        sources[A / f'finalize_training_round{number}.py'] = f'''from nystrom_ridge_release_engine_20261004 import install
install({number},globals())

def predict():
    import optimize_training_round{number} as experiment
    from predict_streaming_rank_classifier_scheme_20261005 import predict as infer
    assert OUT == experiment.OUT
    assert read(OUT/'causal_validation.json')['status'] == read(OUT/'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment,selected())
'''
        sources[A / f'run_training_round{number}_pipeline.py'] = f'from run_streaming_rank_classifier_round_20261005 import main\nif __name__ == "__main__": main({number})\n'
    for path, body in sources.items():
        compile(body,str(path),'exec')
        create(path,body)
    create(A / 'streaming_rank_classifier_official_source_generation_20261005.json', {
        'status':'generated_actual_complete_scheme_sources_before_controls',
        'original_template_source_sha256':templates,
        'generated_source_sha256':{str(path):sha(path) for path in sources},
        'expected_total_records':{'79':100,'80':98},
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'status':'prepared','new_sources':len(sources),'planned_official_records':198}),flush=True)


if __name__ == '__main__':
    main()
