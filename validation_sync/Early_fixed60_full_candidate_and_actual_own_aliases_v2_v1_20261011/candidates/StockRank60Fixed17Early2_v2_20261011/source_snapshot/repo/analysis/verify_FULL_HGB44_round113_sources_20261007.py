"""Compile prospective routes; execute no score, inference, registration or QA."""
from pathlib import Path
import ast
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    p = A / 'prepare_CPU_FULL_HGB44_round113_sources_20261007.py'
    tree = ast.parse(p.read_text(encoding='utf-8'))
    setup = [n for n in tree.body if not isinstance(n, ast.If)
        and not (isinstance(n, ast.FunctionDef) and n.name == 'main')]
    ns = {'__file__': str(p), '__name__': 'prospective_HGB_source_routes'}
    exec(compile(ast.fix_missing_locations(ast.Module(body=setup, type_ignores=[])), str(p), 'exec'), ns)
    body = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main').body
    selected = []
    for node in body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id in ('common', 'generated') or
            isinstance(t, ast.Tuple) and any(isinstance(x, ast.Name) and x.id == 'generated' for x in t.elts)
            for t in node.targets):
            selected.append(node)
        elif isinstance(node, ast.For) and isinstance(node.target, ast.Tuple) and [x.id for x in node.target.elts] == ['old', 'new']:
            selected.append(node)
    exec(compile(ast.fix_missing_locations(ast.Module(body=selected, type_ignores=[])), str(p), 'exec'), ns)
    generated = ns['generated']
    assert len(generated) == 8
    for name, text in generated.items():
        ast.parse(text)
        assert not (A / name).exists(), name
    driver=ast.parse((A/'run_CPU_FULL_HGB44_round113_full_registration_20261007.py').read_text(encoding='utf-8'))
    for func in ('publish','lossless'):
        calls=[n for n in ast.walk(driver) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==func]
        assert len(calls)==1 and isinstance(calls[0].args[0],ast.Constant) and calls[0].args[0].value==113,func
    assert "'current_qualified_comparison_parent_round': 112" in (A/'run_CPU_FULL_HGB44_round113_full_registration_20261007.py').read_text(encoding='utf-8')
    assert "'full_universe_CPU_HGB_rank_CDF'" in generated['register_CPU_FULL_HGB44_round113_artifacts_20261007.py']
    assert 'first2020_identity' not in generated['register_CPU_FULL_HGB44_round113_artifacts_20261007.py']
    optimizer = generated['optimize_training_round113.py']
    assert 'NUMBER = 113' in optimizer and 'PREVIOUS_NUMBER = 112' in optimizer and 'WAVES = (396,)' in optimizer
    assert '== (113, 24, 44)' in generated['collect_full_lossless_round113_qa24_20261007.py']
    assert 'assert number == 113' in generated['lossless_ranking_runtime_adapter_round113_20261007.py']
    assert "namespace['snapshot'](113)" in generated['publish_CPU_FULL_HGB44_round113_full_validation_20261007.py']
    files = [Path(__file__), p, A / 'run_CPU_FULL_HGB44_round113_full_registration_20261007.py',
        *[A / name for name in ns['NAMES']]]
    proof = A / 'CPU_FULL_HGB44_round113_source_route_preflight_20261007.json'
    assert not proof.exists()
    create(proof, {'status': 'passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': {str(f): sha(f) for f in files},
        'generated_source_sha256': {n: hashlib.sha256(s.encode('utf-8')).hexdigest() for n, s in generated.items()},
        'routes': ns['routes'], 'original_QA_helper_reverse_bytes_checked_in_actual_generator_loop': True,
        'correct_original_collector_argument_assertion_checked': True,
        'full_candidate_inference_or_full_QA_not_executed': True,
        'new_fits': 0, 'new_official_scores': 0, 'test_labels_read': False})
    sources = [A / name for name in ('predict_full_universe_CPU_HGB_rank_CDF_scheme_20261007.py',
        'prepare_CPU_FULL_HGB_residual44_selected_candidate_20261007.py',
        'seal_CPU_FULL_HGB_residual44_selected_candidate_20261007.py')]
    selected_admission = A / 'CPU_FULL_HGB44_selected_candidate_source_admission_20261007.json'
    assert not selected_admission.exists()
    create(selected_admission, {'status': 'admitted_unexecuted_HGB44_selected_candidate_routes',
        'input_sha256': {str(f): sha(f) for f in sources}, 'actual_future_inferences_at_admission': 0,
        'only_actual_highest_complete44_score_selects_candidate': True, 'test_labels_read': False})
    admission = A / 'CPU_FULL_HGB44_round113_full_registration_admission_20261007.json'
    assert not admission.exists()
    create(admission, {'status': 'admitted_actual_score_gated_full_pool_HGB44_full113_QA24_registration_routes',
        'input_sha256': {str(f): sha(f) for f in files + [proof]},
        'prospective_generated_source_sha256': read(proof)['generated_source_sha256'],
        'new_fits': 0, 'new_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
