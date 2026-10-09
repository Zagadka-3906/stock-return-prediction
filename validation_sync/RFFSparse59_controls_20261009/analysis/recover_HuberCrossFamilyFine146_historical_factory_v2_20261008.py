"""Keep the first preparation failure; admit Bayes' actual rows-only OOF schema."""
from pathlib import Path
import ast
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    old = A / 'prepare_HuberCrossFamilyFine146_historical_controls_v1_20261008.py'
    proposal = A / 'HuberCrossFamilyFine125_round146_proposal_v1_20261008.json'
    create(A / 'HuberCrossFamilyFine146_first_factory_failure_v1_20261008.json',
           {'status': 'failed_preserved_preparation_not_scientific_validation',
            'error': "KeyError: 'days' on existing Bayes rows-only OOF proof",
            'source_sha256': sha(old), 'proposal_sha256': sha(proposal),
            'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    text = old.read_text(encoding='utf-8-sig')
    tree = ast.parse(text)
    main_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    call = next(n for n in main_node.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                and isinstance(n.value.func, ast.Name) and n.value.func.id == 'create'
                and isinstance(n.value.args[0], ast.Name) and n.value.args[0].id == 'proposal')
    lines = text.splitlines(keepends=True)
    lines[call.lineno - 1:call.end_lineno] = [
        "    preserved = read(proposal)\n",
        "    assert preserved['new_cases'] == cases and preserved['heads'] == heads\n",
        "    assert preserved['scientific_stage_base_round'] == 136\n",
        "    assert preserved['actual139_official_winner']['score'] == winner['connected_final_score']\n"]
    text = ''.join(lines)
    before = "assert proof['rows'] == 5635800 and proof['days'] == 1212"
    assert text.count(before) == 1
    text = text.replace(before, "assert proof['rows'] == 5635800\n        if 'days' in proof: assert proof['days'] == 1212")
    target = A / 'prepare_HuberCrossFamilyFine146_historical_controls_v2_20261008.py'
    compile(text, str(target), 'exec')
    with target.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)
    namespace = {'__file__': str(target), '__name__': 'actual_fresh_fine146_historical_factory'}
    exec(compile(text, str(target), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
