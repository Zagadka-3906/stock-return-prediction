"""Full declared quality rounds after actual native controls and predecessor closure."""
from pathlib import Path
import importlib
import json
import os
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main(number):
    assert number in (75, 76)
    state_path = ROOT / f'analysis/ongoing_optimization_r{number}_state.json'

    def state(stage, status='running', **extra):
        value = {'round': number, 'stage': stage, 'status': status,
            'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'continuous_optimization_authorized': True, 'test_labels_read': False, **extra}
        state_path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(value, ensure_ascii=False), flush=True)

    state('waiting_for_actual30_annual6_final300round_fits_controls_and_full_predecessor')
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    native = ROOT / 'analysis/gradient_sampling_future_qa_20261005/verification.json'
    generator = ROOT / 'analysis/gradient_sampling_search_generator_preflight_20261005/verification.json'
    run = ROOT / 'analysis/gradient_sampling_quality_run_20261005.json'
    while complete_round_evidence(number - 1) is None or not all(p.exists() for p in (native, generator, run)):
        time.sleep(10)
    from locked_read_hash_cache_20261004 import fresh_sha
    read = lambda path: json.loads(Path(path).read_text(encoding='utf-8-sig'))
    assert read(native)['status'] == read(generator)['status'] == 'passed'
    for source, digest in read(run)['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    storage = read(ROOT / 'analysis/gradient_sampling_storage_20261005.json')
    scratch = Path(storage['temporary_directory']) / f'round{number}'
    scratch.mkdir(parents=True, exist_ok=True)
    assert scratch.drive.upper() in ('D:', 'E:')
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[variable] = str(scratch)
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        os.environ[variable] = '8'
    module = importlib.import_module(f'optimize_training_round{number}')
    sys.modules[f'optimize_training_round{number}'] = module
    release = importlib.import_module(f'finalize_training_round{number}')
    assert release.OUT == module.OUT
    def infer_selected():
        from predict_gradient_sampling_scheme_20261005 import predict
        assert module.read(module.OUT/'causal_validation.json')['status'] == module.read(module.OUT/'calibrated_csv_official.json')['status'] == 'passed'
        predict(module,release.selected())
    release.predict = infer_selected
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    scope = FrozenProvenanceExecutionScope(module, [Path(__file__), run,
        ROOT / f'analysis/finalize_training_round{number}.py',
        ROOT / 'analysis/gradient_sampling_search_generator_preflight_20261005/verification.json',
        ROOT / 'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT / 'analysis/locked_read_hash_cache_20261004.py'], {
        'script': str(Path(__file__)), 'round': number,
        'driver_source_sha256': fresh_sha(Path(__file__)),
        'complete_predecessor_required': number - 1, 'native_configs': 6,
        'original_past_eligibility_and_inherited_gates_preserved': True}, ROOT / 'analysis').install()
    failure = None
    try:
        stages = (module.freeze, module.build, module.independent,
            *((module.combinations, module.refine_weights) if number == 75 else (module.model_refinement,)), module.refinement)
        for stage in stages:
            state(stage.__name__)
            stage()
        from parallel_candidate_scoring_four_20261004 import shutdown
        shutdown(module.__name__)
        for stage in (release.select, release.calibrate, release.predict):
            state('release.' + stage.__name__)
            stage()
        state('complete_scheme_causal_checks')
        from check_gradient_sampling_scheme_20261005 import main as checks
        checks(number)
        state('publication_andranking_qa')
        from publish_training_round import publish
        labels = ('因子分解模型三种用途对照', '最佳用途组合', '用途权重细搜', '留存与涨停偏移细搜') if number == 75 else ('独立完整主模型', '逐模型参数与留存细搜', '实际最高分方案细搜')
        result = publish(number, '匹配参数的成熟特征因子分解机完整方案',
                         'gradient_sampling_causal_checks.json', labels)
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        ranking.main()
        qa.main()
        state('completed_declared_grid_boundary_review_pending', 'completed',
            score=result['winner']['connected_final_score'], gain=result['score_gain'], continuous_goal_complete=False)
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        state('failed', 'failed', traceback=traceback.format_exc())
        raise
    finally:
        report = scope.close(failed=failure is not None)
        module.dump(module.OUT / 'provenance_scope_execution.json', {
            'status': 'passed' if failure is None else 'failed', 'failure': failure, **report,
            'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
