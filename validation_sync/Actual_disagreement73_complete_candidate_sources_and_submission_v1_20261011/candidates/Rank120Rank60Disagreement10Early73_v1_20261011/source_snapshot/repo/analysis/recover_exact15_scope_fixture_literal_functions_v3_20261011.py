from pathlib import Path
import sys,ast,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 source=A/'verify_shared_live_report_exact15_scope_controls_v2_20261011.py'
 text=source.read_text(encoding='utf8')
 changes={"exec('def run_variant(row): pass', namespace)":"exec('def main(): pass', namespace)",
  "import json\\ndef run_variant(row): return json.loads(TEXT)":"import json\\ndef main(): return json.loads(TEXT)",
  '共享榜对象精确15作用域控制_v2_20261011':'共享榜对象精确15作用域控制_v3_20261011'}
 for before,after in changes.items():assert text.count(before)==1;text=text.replace(before,after)
 target=A/'verify_shared_live_report_exact15_scope_controls_v3_20261011.py'
 ast.parse(text);assert not target.exists();target.write_text(text,encoding='utf8')
 assert allowed();runpy.run_path(str(target),run_name='__main__')
if __name__=='__main__':main()
