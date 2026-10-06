"""Lazy qualified R62 handoff to actual latest-graph joint scoring and delivery."""
from pathlib import Path
import argparse
import importlib
import json
import os
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main(probe=False):
    if probe:
        import psutil
        print(json.dumps({'round': 63, 'lazy_imports_only': not any(n in sys.modules for n in ('numpy', 'pandas', 'polars', 'torch')),
            'rss_bytes': psutil.Process().memory_info().rss, 'waits_for_full_qualified_round': 62,
            'new_model_fits': 0, 'new_quality_scores': 0}), flush=True)
        return
    path = ROOT / 'analysis/ongoing_optimization_r63_state.json'
    def state(stage, status='running', extra=None):
        value = {'round': 63, 'stage': stage, 'status': status,
            'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'continuous_optimization_authorized': True, 'test_labels_read': False, **(extra or {})}
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(value, ensure_ascii=False), flush=True)
    state('waiting_for_actual_complete_round62_scientific_and_scope_evidence')
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    while complete_round_evidence(62) is None:
        time.sleep(10)
    prepared = read(ROOT / 'analysis/latest_graph_joint_round63_source_preflight_20261005/verification.json')
    assert prepared['status'] == 'passed_pre_execution_source_and_lazy_dispatch_checks'
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, digest in prepared['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        os.environ[variable] = '8'
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    module = importlib.import_module('optimize_training_round63')
    release = importlib.import_module('finalize_training_round63')
    sources = [Path(__file__), ROOT / 'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT / 'analysis/locked_read_hash_cache_20261004.py',
        ROOT / 'analysis/latest_graph_joint_round63_source_preflight_20261005/verification.json']
    scope = FrozenProvenanceExecutionScope(module, sources, {
        'script': str(Path(__file__).resolve()), 'round': 63,
        'driver_source_sha256': fresh_sha(Path(__file__)),
        'original_r50_stage_math_reused_with_latest_actual_graph_axes': True,
        'previous_round_full_scientific_scope_required': True,
    }, ROOT / 'analysis').install()
    failure = None
    try:
        for stage in (module.freeze, module.build, module.independent, module.forward, module.reverse,
                      module.retention_refinement, module.temporal_refinement):
            state(stage.__name__)
            stage()
        from parallel_candidate_scoring_four_20261004 import shutdown
        shutdown('optimize_training_round63')
        for stage in (release.select, release.calibrate, release.predict):
            state('release.' + stage.__name__)
            stage()
        state('complete_scheme_causal_checks')
        from check_latest_joint_scheme_20261005 import main as checks
        checks()
        state('publication_andranking_qa')
        from publish_training_round import publish
        result = publish(63, '最新有效完整方案的全部有效权重轴联合复查', 'latest_joint_scheme_causal_checks.json',
            ('全部有效权重单轴对照', '正向权重顺序细搜', '逆向权重顺序细搜', '各历史成员留存细搜', '最终因果平滑细搜'))
        import build_all_model_rankings_20261003 as rankings
        import verify_all_model_rankings_20261003 as qa
        rankings.main()
        qa.main()
        state('round_complete_further_boundary_review_pending', 'completed',
            {'score': result['winner']['connected_final_score'], 'gain': result['score_gain'], 'continuous_goal_complete': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        state('failed', 'failed', {'traceback': traceback.format_exc()})
        raise
    finally:
        report = scope.close(failed=failure is not None)
        module.OUT.mkdir(exist_ok=True)
        with (module.OUT / 'provenance_scope_execution.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': 'passed' if failure is None else 'failed', 'failure': failure,
                'updated_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), **report,
                'new_model_fits': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe', action='store_true')
    main(parser.parse_args().probe)
