from pathlib import Path
import sys,ast
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import prepare_SparseAfter14829_round152_sources_v1_20261009 as g
for parent in (148,149,150,151):
 result=g.generate(parent)
 text=next(s for n,s in result.items() if n.startswith('register_'));tree=ast.parse(text)
 n=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
 print(parent,ast.unparse(n))
print(list(result))
