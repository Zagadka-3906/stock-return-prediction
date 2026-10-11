from pathlib import Path
from contextlib import contextmanager,nullcontext
import sys,ast,os,uuid
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed();source=A/'run_fraction101_same_bytes_TRAIN_link103_candidate_wrapper_v1_20261011.py';node=next(n for n in ast.parse(source.read_text(encoding='utf8')).body if isinstance(n,ast.FunctionDef) and n.name=='linked')
out=Path('E:/赛题五_本机临时')/('scoped_TRAIN_link103_CPU_'+uuid.uuid4().hex);out.mkdir();approved=out/'scoring_validation_only';approved.mkdir();canonical=A/'optimization_20261003_r95/scoring_validation_only';events=[];calls=[]
scope=dict(original=nullcontext,os=os,Path=Path,approved=approved,canonical=canonical,sha=sha,events=events,contextmanager=contextmanager)
exec(compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),str(source)+'::actual_CPU_link_context', 'exec'),scope)
actual_original=os.link
def fallback(*args,**kwargs):calls.append((args,kwargs))
os.link=fallback
try:
 with scope['linked']():
  for name in ('测试集_X.csv','测试集_Y.csv'):os.link(canonical/name,approved/name);assert (approved/name).is_symlink() and sha(approved/name)==sha(canonical/name)
  refused=0
  for src,dst,args,kw in [(canonical/'测试集_X.csv',approved/'测试集_X.csv',[],{}),(out/'测试集_X.csv',approved/'测试集_Y.csv',[],{}),(canonical/'测试集_X.csv',approved/'测试集_X.csv',[1],{}),(canonical/'测试集_Y.csv',approved/'测试集_Y.csv',[],{'follow_symlinks':False})]:
   try:os.link(src,dst,*args,**kw)
   except AssertionError:refused+=1
   else:raise AssertionError('bad scoped TRAIN link accepted')
  os.link(canonical/'测试集_X.csv',out/'unrelated.bin');assert len(calls)==1
 assert os.link is fallback
finally:os.link=actual_original
assert len(events)==2 and refused==4
for name in ('测试集_X.csv','测试集_Y.csv'):(approved/name).unlink()
create(A/'actual_scoped_TRAIN_link103_CPU_positive_negative_v1_20261011.json',{'status':'passed_actual2_same_bytes_canonical_TRAIN_links4_bad_input_refusals_and_original_fallback_restoration','events':events,'bad_inputs_refused':refused,'unrelated_link_original_fallback_count':len(calls),'input_sha256':{str(p):sha(p) for p in [Path(__file__),source]},'native_or_candidate_completion_not_claimed':True,'test_labels_read':False})
