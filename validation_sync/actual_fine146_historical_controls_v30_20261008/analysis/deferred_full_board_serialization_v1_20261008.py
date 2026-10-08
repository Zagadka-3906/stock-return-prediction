"""An isolated AST transformation; original ranking source stays unchanged."""
from pathlib import Path
import ast
import copy
import hashlib

SOURCE = Path(__file__).parent / 'build_all_model_rankings_20261003.py'
SOURCE_SHA = 'f36a0f08766169bd152a08f1ea70121b992451e16bcf9125b25fde9de6f2aaab'


def bodies():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    tree = ast.parse(raw.decode('utf-8-sig'))
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    start = next(i for i, n in enumerate(main.body)
                 if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'output_json' for t in n.targets))
    end = next(i for i, n in enumerate(main.body[start:], start)
               if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
               and isinstance(n.value.func, ast.Attribute) and isinstance(n.value.func.value, ast.Name)
               and n.value.func.value.id == 'output_html' and n.value.func.attr == 'write_text')
    segment = main.body[start:end + 1]
    original = copy.deepcopy(segment)
    branch = next(n for n in segment if isinstance(n, ast.If))
    assert 'validation_provenance_erratum_20261003.json' in ast.unparse(branch.test)
    initial_pretty, initial_compact = segment[2:4]
    final_pretty = next(n for n in branch.body if isinstance(n, ast.Expr)
                       and isinstance(n.value, ast.Call) and ast.unparse(n.value.func) == 'output_json.write_text')
    final_compact = next(n for n in branch.body if isinstance(n, ast.Assign)
                         and any(isinstance(t, ast.Name) and t.id == 'embedded' for t in n.targets))
    assert ast.dump(initial_pretty, include_attributes=False) == ast.dump(final_pretty, include_attributes=False)
    assert ast.dump(initial_compact, include_attributes=False) == ast.dump(final_compact, include_attributes=False)
    deferred = copy.deepcopy(segment)
    deferred[2:4] = [ast.If(test=ast.UnaryOp(op=ast.Not(), operand=copy.deepcopy(branch.test)),
                          body=copy.deepcopy([initial_pretty, initial_compact]), orelse=[])]
    return original, deferred, main, tree, start


def fragment(deferred):
    before, after, *_ = bodies()
    return compile(ast.fix_missing_locations(ast.Module(body=after if deferred else before, type_ignores=[])),
                   str(SOURCE), 'exec')


def prospective_whole_main():
    before, after, main, tree, start = bodies()
    main.body[start:start + len(before)] = after
    return compile(ast.fix_missing_locations(tree), str(SOURCE), 'exec')


def source_note():
    before, _, *_ = bodies()
    branch = next(n for n in before if isinstance(n, ast.If))
    append = next(n for n in branch.body if isinstance(n, ast.Expr)
                  and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
                  and n.value.func.attr == 'append')
    return ast.literal_eval(append.value.args[0])
