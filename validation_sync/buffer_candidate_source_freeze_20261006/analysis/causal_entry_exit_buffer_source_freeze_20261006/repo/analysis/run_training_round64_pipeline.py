"""Gated full evaluation, freeze, calibration, causal checks and publication."""
from pathlib import Path
import argparse
import json
import os
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
RUN = ROOT / 'analysis/agreement_gate_round64_run_20261005.json'


def main(probe=False):
    if probe:
        import psutil
        print(json.dumps({'round': 64, 'lazy_imports_only': not any(n in sys.modules for n in ('numpy', 'polars', 'pandas', 'torch')),
                          'waits_for_full_qualified_round': 63, 'rss_bytes': psutil.Process().memory_info().rss,
                          'new_model_fits': 0, 'new_quality_scores': 0}), flush=True)
        return
    state_path = ROOT / 'analysis/ongoing_optimization_r64_state.json'
    def state(stage, status='running', extra=None):
        value = {'round': 64, 'stage': stage, 'status': status,
                 'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                 'continuous_optimization_authorized': True, 'test_labels_read': False, **(extra or {})}
        state_path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(value, ensure_ascii=False), flush=True)
    state('waiting_for_full_qualified_round63_and_actual_gate_controls')
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    proof = ROOT / 'analysis/agreement_gate_preflight_v2_20261005/verification.json'
    while complete_round_evidence(63) is None or not proof.exists() or not RUN.exists():
        time.sleep(10)
    from locked_read_hash_cache_20261004 import fresh_sha
    read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
    assert read(proof)['status'] == 'passed_actual_mature_oof_gate_controls'
    job = read(RUN)
    for source, digest in job['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    scratch = ROOT / 'tmp/round64_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[variable] = str(scratch)
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        os.environ[variable] = '8'
    import optimize_training_round64 as module
    import finalize_training_round64 as release
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    sources = [Path(__file__), RUN, ROOT / 'analysis/frozen_provenance_execution_scope_20261004.py',
               ROOT / 'analysis/locked_read_hash_cache_20261004.py',
               ROOT / 'analysis/agreement_gate_round64_source_preflight_20261005/verification.json']
    scope = FrozenProvenanceExecutionScope(module, sources, {
        'script': str(Path(__file__)), 'round': 64, 'driver_source_sha256': fresh_sha(Path(__file__)),
        'same_day_model_agreement_and_diversity_gate': True, 'temporary_files_drive': 'D',
        'previous_full_scientific_scope_required': True}, ROOT / 'analysis').install()
    failure = None
    try:
        for stage in (module.freeze, module.build, module.independent, module.combinations, module.refinement):
            state(stage.__name__)
            stage()
        from parallel_candidate_scoring_four_20261004 import shutdown
        shutdown('optimize_training_round64')
        for stage in (release.select, release.calibrate, release.predict):
            state('release.' + stage.__name__)
            stage()
        state('complete_scheme_causal_checks')
        from check_agreement_scheme_20261005 import main as checks
        checks()
        state('publication_andranking_qa')
        from publish_training_round import publish
        result = publish(64, '有效模型同日意见分歧的自适应用途权重', 'agreement_gate_causal_checks.json',
                         ('全部有效用途单轴意见一致与分散对照', '最佳单轴门控顺序组合', '实际最高分方案门控强度细搜'))
        import build_all_model_rankings_20261003 as rankings
        import verify_all_model_rankings_20261003 as qa
        rankings.main()
        qa.main()
        state('round_complete_further_boundary_review_pending', 'completed',
              {'score': result['winner']['connected_final_score'], 'gain': result['score_gain'],
               'continuous_goal_complete': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        state('failed', 'failed', {'traceback': traceback.format_exc()})
        raise
    finally:
        report = scope.close(failed=failure is not None)
        module.dump(module.OUT / 'provenance_scope_execution.json', {
            'status': 'passed' if failure is None else 'failed', 'failure': failure, **report,
            'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'new_model_fits': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe', action='store_true')
    main(parser.parse_args().probe)
