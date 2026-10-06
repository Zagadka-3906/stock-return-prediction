"""Prepare full native and official workflows; preserve every prior frozen source."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def transform(text):
    text = text.replace('neural16384_full', 'memory_efficient_neural')
    for old, new in ((67, 77), (68, 78), (276, 311), (277, 312), (278, 313),
        (279, 314), (280, 315), (281, 316), (282, 317)):
        text = re.sub(rf'(?<!\d){old}(?!\d)', str(new), text)
    text = text.replace('memory_efficient_neural_search_engine_v2_', 'memory_efficient_neural_search_engine_')
    text = text.replace('run_memory_efficient_neural_round_v2_', 'run_memory_efficient_neural_round_')
    text = text.replace('predict_memory_efficient_neural_scheme_v2_', 'predict_memory_efficient_neural_scheme_')
    text = text.replace('verify_memory_efficient_neural_search_generators_v2_', 'verify_memory_efficient_neural_search_generators_')
    text = text.replace('memory_efficient_neural_search_generator_preflight_v2_', 'memory_efficient_neural_search_generator_preflight_')
    text = text.replace('optimize_training_round{number}_v2', 'optimize_training_round{number}')
    text = text.replace('run_training_round{number}_v2_pipeline', 'run_training_round{number}_pipeline')
    text = text.replace('[13,8,18,25] if number==77 else [7,14,17]', '[37,8,18,25] if number==77 else [19,42,17]')
    text = text.replace('[13, 8, 18, 25] if number == 77 else [7, 14, 17]', '[37, 8, 18, 25] if number == 77 else [19, 42, 17]')
    text = text.replace('64 if number==77 else 38', '88 if number==77 else 78')
    text = text.replace('64 if number == 77 else 38', '88 if number == 77 else 78')
    text = text.replace('actual5_annual1_final', 'actual15_annual3_final')
    text = text.replace("'native_configs': 1", "'native_configs': 3")
    text = text.replace("'previous_memory_efficient_neural_bank_actual_annual_fits':5", "'previous_memory_efficient_neural_bank_actual_annual_fits':15")
    text = text.replace("'new_native_model_configurations':1", "'new_native_model_configurations':3")
    text = text.replace('all1_new_native_model', 'all3_new_native_models').replace('all1_new_model_checked', 'all3_new_models_checked')
    text = text.replace('passed_actual_matched_instrumentation_and_architecture_controls', 'passed_actual_gradients_saved_tensors_and_mature_CPU_pilots')
    text = text.replace('memory_efficient_neural_preflight_20261005', 'memory_efficient_mlp_preflight_20261005')
    return text


def main():
    original_plan = A / 'memory_efficient_mlp_complete_search_plan_20261005.json'
    config = json.loads(original_plan.read_text(encoding='utf-8'))['model_configurations']
    assert len(config) == 3 and all(c['epochs'] == 32 and c['batch_size'] == 32768 and c['hidden'] == [16384,8192,4096] for c in config.values())
    required_bytes = 20 * 2**30 + 8 * 2**30 + 25 * 168894465 * 4
    free_d = shutil.disk_usage('D:/').free
    output = A / 'memory_efficient_neural_bank_20261005'
    scratch = ROOT / 'tmp/memory_efficient_neural_20261005'
    if free_d < required_bytes:
        output = Path('E:/赛题五计算存储/memory_efficient_neural_bank_20261005')
        scratch = Path('E:/赛题五计算存储/tmp/memory_efficient_neural_20261005')
    assert output.resolve().drive.upper() in ('D:', 'E:') and scratch.resolve().drive.upper() in ('D:', 'E:')
    create(A / 'memory_efficient_neural_storage_20261005.json', {
        'output_directory': str(output), 'temporary_directory': str(scratch),
        'D_free_bytes_observed': free_d, 'conservative_full_artifact_and_scratch_reserve_bytes': required_bytes,
        '25_uncompressed_parameter_states_allowance_plus8GiB_scratch_and20GiB_reserve': True,
        'reserve_is_policy_not_physical_limit': True, 'D_primary_E_fallback': True})
    create(A / 'memory_efficient_neural_complete_search_plan_20261005.json', {
        'status': 'full_native_final_and_complete_official_workflows_prepared_before_controls',
        'model_configurations': config, 'expected_annual_fits': 15, 'expected_final_mature_fits': 3,
        'actual_previous_selection_required': {'77':76,'78':77}, 'expected_total_records': {'77':88,'78':78},
        'wave_arm_counts': {'77':[37,8,18,25],'78':[19,42,17]},
        'waves': {'77':[311,312,313,314],'78':[315,316,317]},
        'same_original63features_mature_windows_target_seed_and32epochs': True,
        'effective_batch32768_and_original_AdamW_update_count_retained': True,
        'full_training_not_replaced_by_GPU_or_CPU_pilots': True,
        'microbatch_roundoff_compared_by_official_complete_scheme_score': True,
        'same1212_days5635800_rows_continuous_official_validation': True,
        'all_validation_years_viewed_selection_bias_uncorrected': True,
        'test_labels_read': False, 'global_resource_exhaustion_established': False})
    sources, templates = {}, {}
    old = A / 'train_neural16384_full_bank_20261005.py'
    templates[str(old)] = sha(old)
    native = old.read_text(encoding='utf-8').replace('neural16384_full', 'memory_efficient_neural')
    native = native.replace('isolated_neural16384_full_20261005', 'isolated_memory_efficient_neural_20261005')
    begin, end = native.index('CONFIGS = '), native.index('engine.OUT, engine.CONFIGS')
    native = native[:begin] + "PLAN = ROOT / 'analysis/memory_efficient_neural_complete_search_plan_20261005.json'\nCONFIGS = read(PLAN)['model_configurations']\nfrom memory_efficient_mlp_20261005 import fit_arrays as memory_fit\nengine.fit_arrays = memory_fit\n" + native[end:]
    begin, end = native.index('def freeze():'), native.index('def all_oof():')
    freeze = '''def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'protocol.json').exists():
        verify(); return
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    assert complete_round_evidence(66) is not None
    GPU = Path(read(ROOT / 'analysis/memory_efficient_mlp_storage_20261005.json')['GPU_control_directory'])
    proof = read(GPU / 'verification.json')
    assert proof['status'] == 'passed' and proof['actual_matched16384_single_batch_control_fits'] == 4
    cpu = ROOT / 'analysis/memory_efficient_mlp_preflight_20261005/verification.json'
    assert read(cpu)['status'] == 'passed_actual_gradients_saved_tensors_and_mature_CPU_pilots'
    sources = [Path(__file__), SOURCE, STORAGE, PLAN, cpu, GPU / 'verification.json', GPU / 'execution_scope.json',
        ROOT / 'analysis/memory_efficient_mlp_20261005.py',
        ROOT / 'analysis/run_memory_efficient_neural_bank_20261005.py',
        ROOT / 'analysis/memory_efficient_neural_bank_run_20261005.json',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md',
        *[BASELINE / f'info_{year}.json' for year in YEARS]]
    dump(OUT / 'protocol.json', {'status':'frozen_before_actual_complete_memory_layout_annual_training',
        'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations':CONFIGS,
        'features':engine.feature_names(), 'years':YEARS, 'expected_annual_fits':15,
        'validation':'2020–2024 annual expanding OOF; original mature one-day label purge.',
        'matched_control':'Original16384/8192/4096 zero-dropout rank MLP, seed20261007,32epochs,effective batch32768.',
        'preprocessing':'Original past-only float32 mean/std and z clipping; provided rank target minus0.5.',
        'only_training_memory_layout_changes':True, 'microbatch_roundoff_requires_separate_official_quality':True,
        'actual15_annual3_final_fits_required_pilots_not_a_substitute':True,
        'minimum_available_host_RAM_before_each_fit_GiB':14.,
        'reserve_is_scheduling_policy_not_physical_boundary':True,
        'no_validation_early_stopping':True, 'selection_bias_uncorrected':True,
        'new_quality_scores':0, 'test_data_read':False,
        'input_sha256':{str(path.resolve()):sha(path) for path in sources}}, immutable=True)


'''
    native = native[:begin] + freeze + native[end:]
    native = native.replace("'actual_annual_fits': 5", "'actual_annual_fits': 15")
    sources[A / 'train_memory_efficient_neural_bank_20261005.py'] = native
    templates_to_transform = {
        'memory_efficient_neural_scheme_runtime_20261005.py': 'neural16384_full_scheme_runtime_20261005.py',
        'memory_efficient_neural_search_engine_20261005.py': 'neural16384_full_search_engine_v2_20261005.py',
        'run_memory_efficient_neural_round_20261005.py': 'run_neural16384_full_round_v2_20261005.py',
        'check_memory_efficient_neural_scheme_20261005.py': 'check_neural16384_full_scheme_20261005.py',
        'verify_memory_efficient_neural_search_generators_20261005.py': 'verify_neural16384_full_search_generators_v2_20261005.py',
        'verify_memory_efficient_neural_full_future_20261005.py': 'verify_neural16384_full_future_20261005.py'}
    for target, original in templates_to_transform.items():
        path = A / original
        templates[str(path)] = sha(path)
        text = transform(path.read_text(encoding='utf-8'))
        if 'search_generators' in target:
            text = text.replace("'*neural16384*20261005.py'", "'*memory_efficient*20261005.py'")
            text = text.replace("('optimize_training_round', '_v2')", "('optimize_training_round', '')")
            text = text.replace("('run_training_round', '_v2_pipeline')", "('run_training_round', '_pipeline')")
            text = text.replace('optimize_training_round{number}_v2', 'optimize_training_round{number}')
            text = text.replace('actual_R64_and_R77', 'actual_R76_and_R77')
        if 'full_future' in target:
            text = text.replace("['actual_annual_fits'] == 5", "['actual_annual_fits'] == 15")
            text = text.replace("'expected_final_fits': 1", "'expected_final_fits': 3")
            text = text.replace("'all1_model_fullfuture_reload_and_cold80_controls_passed': len(checks) == 1", "'all3_model_fullfuture_reload_and_cold80_controls_passed': len(checks) == 3")
        if 'run_memory_efficient_neural_round' in target:
            text = text.replace('16384宽度成熟样本神经网络完整方案', '匹配预算的16384宽度内存优化神经网络完整方案')
            text = text.replace("    release = importlib.import_module(f'finalize_training_round{number}')", "    release = importlib.import_module(f'finalize_training_round{number}')\n    assert release.OUT == module.OUT\n    sys.modules[f'finalize_training_round{number}'] = release")
        sources[A / target] = text
    router = (A / 'neural16384_full_model_sources_20261005.py').read_text(encoding='utf-8')
    router = router.replace('neural16384_full', 'memory_efficient_neural').replace('nystrom_tuning_model_sources_20261005', 'gradient_sampling_model_sources_20261005')
    router = router.replace("bundle.get('config',{}).get('hidden')==[16384,8192,4096]", "bundle.get('kind')=='mlp' and bundle.get('config',{}).get('memory_mode') in ('accumulate','checkpoint','combined')")
    sources[A / 'memory_efficient_neural_model_sources_20261005.py'] = router
    sources[A / 'memory_efficient_neural_future_codec_adapter_20261005.py'] = '''"""Route the memory-layout MLPs above the complete GOSS/inherited codec."""
def install():
    import fourier_tuning_model_sources_20261004 as legacy
    import train_memory_efficient_neural_bank_20261005 as native
    from gradient_sampling_future_codec_adapter_20261005 import install as install_previous
    restore_previous = install_previous()
    original = legacy.predict_arrays
    def predict_arrays(bundle,x,dates=None,valid=None):
        if bundle.get('kind')=='mlp' and bundle.get('config',{}).get('memory_mode') in ('accumulate','checkpoint','combined'):
            return native.engine.predict_arrays(bundle,x)
        return original(bundle,x,dates=dates,valid=valid)
    legacy.predict_arrays = predict_arrays
    def restore():
        assert legacy.predict_arrays is predict_arrays
        legacy.predict_arrays = original
        restore_previous()
    return restore
'''
    codec = (A / 'predict_gradient_sampling_scheme_codec_20261005.py').read_text(encoding='utf-8')
    codec = codec.replace('gradient_sampling', 'memory_efficient_neural')
    codec = codec.replace("    assert runtime.FutureContext.weights_for is original_weights", "    assert runtime.FutureContext.weights_for is original_weights\n    source_files = ('run_memory_efficient_neural_round_20261005.py',f'run_training_round{ns.NUMBER}_pipeline.py','memory_efficient_mlp_20261005.py','train_memory_efficient_neural_bank_20261005.py')\n    for name in source_files:\n        shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)\n    ns.dump(candidate/'actual_execution_sources.json',{'status':'passed','files':{name:{'project_source':str(ns.ROOT/'analysis'/name),'sha256':ns.sha(candidate/name)} for name in source_files},'same_actual_pipeline_and_canonical_release':True,'test_labels_read':False},immutable=True)")
    sources[A / 'predict_memory_efficient_neural_scheme_codec_20261005.py'] = codec
    sources[A / 'predict_memory_efficient_neural_scheme_20261005.py'] = 'from predict_memory_efficient_neural_scheme_codec_20261005 import predict\n'
    for number in (77, 78):
        sources[A / f'optimize_training_round{number}.py'] = f'from memory_efficient_neural_search_engine_20261005 import install\ninstall({number}, globals())\n'
        sources[A / f'finalize_training_round{number}.py'] = f'''from nystrom_ridge_release_engine_20261004 import install
install({number}, globals())

def predict():
    import optimize_training_round{number} as experiment
    from predict_memory_efficient_neural_scheme_20261005 import predict as infer
    assert OUT == experiment.OUT
    assert read(OUT/'causal_validation.json')['status'] == read(OUT/'calibrated_csv_official.json')['status'] == 'passed'
    infer(experiment,selected())
'''
        sources[A / f'run_training_round{number}_pipeline.py'] = f'from run_memory_efficient_neural_round_20261005 import main\nif __name__ == "__main__": main({number})\n'
    for path, text in sources.items():
        compile(text, str(path), 'exec')
        create(path, text)
    create(A / 'memory_efficient_neural_source_generation_20261005.json', {
        'status':'generated_before_actual_native_router_and_search_controls',
        'original_template_source_sha256':templates, 'generated_source_sha256':{str(p):sha(p) for p in sources},
        'model_configurations':config,'planned_complete_native_annual_fits':15,'planned_complete_final_fits':3,
        'planned_official_records':{'77':88,'78':78},'original_frozen_sources_preserved':True,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'status':'prepared','new_sources':len(sources),'bank_drive':output.drive,'planned_official_records':166}),flush=True)


if __name__ == '__main__':
    main()
