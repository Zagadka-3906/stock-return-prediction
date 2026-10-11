"""Bind actual148 prospective2 and preserve all242 mathematical configurations."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_AdaptiveJointCrossHuber242_round148_sources_v1_20261008 as original
from recover_AdaptiveJointCrossHuber148_prospective_literals_v2_20261008 import MAP
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 out=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 out += [Path(__file__),Path(original.__file__),A/'recover_AdaptiveJointCrossHuber148_prospective_literals_v2_20261008.py',A/'AdaptiveJointCrossHuber148_prospective_literal_recovery_v2_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 result={}
 for n,s in ORIGINAL_GENERATE(parent).items():
  s=s.replace('prepare_AdaptiveJointCrossHuber242_round148_sources_v1_20261008','prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008')
  compile(s,str(A/n),'exec');result[n]=s
 return result
def main():
 original.generate=generate
 original.main()
if __name__=='__main__':main()
