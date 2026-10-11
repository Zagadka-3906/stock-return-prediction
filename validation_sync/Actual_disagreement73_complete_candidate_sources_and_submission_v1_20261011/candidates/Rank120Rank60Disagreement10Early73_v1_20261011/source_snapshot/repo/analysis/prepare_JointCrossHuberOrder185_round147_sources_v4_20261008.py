"""Explicit comparison parent paths are fixed before quality; scientific134 stage graph stays unchanged."""
from pathlib import Path
import sys,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_JointCrossHuberOrder185_round147_sources_v3_20261008 as original
from prepare_JointCrossHuber147_explicit_report_paths_v4_20261008 import MAP
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 out=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 out += [Path(__file__),Path(original.__file__),A/'prepare_JointCrossHuber147_explicit_report_paths_v4_20261008.py',A/'JointCrossHuber147_explicit_report_paths_preparation_v4_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 result={}
 for n,s in ORIGINAL_GENERATE(parent).items():
  s=s.replace('prepare_JointCrossHuberOrder185_round147_sources_v3_20261008','prepare_JointCrossHuberOrder185_round147_sources_v4_20261008')
  if n=='optimize_training_round147.py':
   t=ast.parse(s);assignment=next(x for x in t.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PREVIOUS' for a in x.targets))
   literal=ast.get_source_segment(s,assignment.value.right);assert s.count(literal)==1
   s=s.replace(literal,repr('analysis/optimization_20261003_r'+str(parent)))
  compile(s,str(A/n),'exec');result[n]=s
 return result
def main():
 original.original.generate=generate
 original.original.main()
if __name__=='__main__':main()
