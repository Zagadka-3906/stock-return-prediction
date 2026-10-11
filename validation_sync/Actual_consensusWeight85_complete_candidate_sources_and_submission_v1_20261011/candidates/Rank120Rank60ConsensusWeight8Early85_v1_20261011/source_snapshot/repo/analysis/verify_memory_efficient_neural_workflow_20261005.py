"""Exercise actual execution bindings, source identities and live scheduling gates."""
from pathlib import Path
import hashlib
import importlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT),str(A)]
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    import train_memory_efficient_neural_bank_20261005 as bank
    import memory_efficient_mlp_20261005 as fitter
    import run_memory_efficient_neural_bank_20261005 as driver
    import verify_memory_efficient_neural_full_future_20261005 as future
    import publish_training_round as publication
    from run_memory_efficient_mlp_gpu_controls_v2_20261005 import owned_live
    out = A / 'memory_efficient_neural_workflow_preflight_20261005'
    assert not out.exists()
    out.mkdir()
    originals = read(A / 'neural16384_full_complete_search_plan_20261005.json')['model_configurations']
    original = next(iter(originals.values()))
    assert bank.engine.fit_arrays is fitter.fit_arrays
    assert len(bank.CONFIGS) == 3 and len(bank.YEARS) == 5
    for name,cfg in bank.CONFIGS.items():
        assert {k:v for k,v in cfg.items() if k in original} == original
        assert set(cfg)-set(original) == {'memory_mode','micro_batch_size'}
        assert cfg['memory_mode'] in ('accumulate','checkpoint','combined') and cfg['micro_batch_size'] == 4096
    assert future.OUT == A / 'memory_efficient_neural_future_qa_20261005'
    assert Path(bank.read(bank.STORAGE)['output_directory']).resolve() == bank.OUT.resolve()
    assert bank.OUT.drive.upper() in ('D:','E:')
    assert driver.dependencies_closed() is False
    GOSS = read(A / 'gradient_sampling_followups_20261005/verification.json')
    GPU = read(A / 'memory_efficient_mlp_gpu_recovery_v2_20261005/verification.json')['job']
    assert all(owned_live(job) for job in (GOSS['native'],GOSS['future'],GPU))
    generator = read(A / 'memory_efficient_neural_search_generator_preflight_20261005/verification.json')
    routes = read(A / 'memory_efficient_neural_direct_router_preflight_20261005/verification.json')
    assert generator['status'] == routes['status'] == 'passed'
    assert [row['generated_records'] for row in generator['controls']] == [88,78,78]
    assert routes['actual_checks'] == 40 and routes['all_direct_and_hooked_routes_bit_identical_and_original_codec_restored']
    for proof in (generator,routes):
        for source,digest in proof['source_sha256'].items():
            assert sha(source) == digest,source
    controls = []
    for number in (77,78):
        experiment = importlib.import_module(f'optimize_training_round{number}')
        release = importlib.import_module(f'finalize_training_round{number}')
        assert release.OUT == experiment.OUT == A / f'optimization_20261003_r{number}'
        assert release.PREVIOUS == experiment.PREVIOUS == A / f'optimization_20261003_r{number-1}'
        assert publication.importlib.import_module(f'optimize_training_round{number}') is experiment
        assert publication.importlib.import_module(f'finalize_training_round{number}') is release
        assert set(experiment.MODELS) == set(bank.CONFIGS)
        for name in ('selected','select','calibrate'):
            assert experiment in [cell.cell_contents for cell in getattr(release,name).__closure__]
        assert release.ReleaseContext.__bases__ == (experiment.Context,)
        assert release.selected in [cell.cell_contents for cell in release.ReleaseContext.__init__.__closure__]
        assert experiment.WAVES == ((311,312,313,314) if number == 77 else (315,316,317))
        assert not (experiment.OUT / 'protocol.json').exists()
        controls.append({'round':number,'actual_canonical_publication_module_and_release_closures':True,
            'actual_predecessor':number-1,'actual_configs':list(experiment.MODELS),
            'planned_complete_records':88 if number == 77 else 78})
    sources = [Path(__file__),Path(bank.__file__),Path(driver.__file__),Path(future.__file__),Path(fitter.__file__),
        A / 'memory_efficient_neural_storage_20261005.json',A / 'memory_efficient_neural_complete_search_plan_20261005.json',
        A / 'memory_efficient_neural_search_generator_preflight_20261005/verification.json',
        A / 'memory_efficient_neural_direct_router_preflight_20261005/verification.json']
    sources += [A / f'{prefix}{number}{suffix}.py' for number in (77,78)
        for prefix,suffix in (('optimize_training_round',''),('finalize_training_round',''),('run_training_round','_pipeline'))]
    sources += [A / 'run_memory_efficient_neural_round_20261005.py',A / 'predict_memory_efficient_neural_scheme_codec_20261005.py']
    with (out / 'verification.json').open('x',encoding='utf-8') as stream:
        json.dump({'status':'passed_actual_native_final_quality_dispatch_and_live_pending_gates',
            'source_sha256':{str(path):sha(path) for path in sources},'controls':controls,
            'actual_native_fitter_function_identity':True,'same_original_configuration_except_memory_layout':True,
            'actual_GPU_and_GOSS_work_alive_native_gate_returns_waiting':True,
            'expected_annual_fits':15,'expected_final_fits':3,'prototype_models_not_substituted_for_full_width':True,
            'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    print('Actual15 annual3 final native/quality dispatch and live scheduling gates passed',flush=True)


if __name__ == '__main__':
    main()
