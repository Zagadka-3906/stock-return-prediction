from pathlib import Path
import sys,runpy,types
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def execute(driver):
 from run_dependency_queue_v3_20261006 import read,sha
 from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
 assert allowed();d=read(A/'future191_207_current_authorized_main_index68_preflight_admission_v1_20261011.json');assert sha(d['guard'])==d['guard_sha256'];assert sha(d['actual_controls_proof'])==d['actual_controls_sha256']
 for name,info in d['modules'].items():
  q=Path(info['source']);assert sha(q)==info['sha256'];s=q.read_text(encoding='utf8');assert s.count(d['original_literal'])==1;m=types.ModuleType(name);m.__file__=str(q);exec(compile(s.replace(d['original_literal'],d['replacement']),str(q),'exec'),m.__dict__);sys.modules[name]=m
 import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as base
 original=base.closed
 base.closed=lambda n:original('recovery68_MixedRefined191_complete27_family_v1_20261011' if n=='recovery64_MixedRefined191_complete27_family_v1_20261011' else n)
 try:runpy.run_path(str(A/driver),run_name='__main__')
 finally:base.closed=original
