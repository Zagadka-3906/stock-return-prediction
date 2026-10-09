from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_PureRFFHuber128_round149_sources_v1_20261008 as original
from recover_Pure149_component_count_prospective_v2_20261008 import MAP
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 result=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 result += [Path(__file__),Path(original.__file__),A/'recover_Pure149_component_count_prospective_v2_20261008.py',A/'Pure149_component_count_prospective_recovery_v2_20261008.json']
 return list(dict.fromkeys(result))
def generate(parent):
 result={}
 for name,s in ORIGINAL_GENERATE(parent).items():
  s=s.replace('prepare_PureRFFHuber128_round149_sources_v1_20261008','prepare_PureRFFHuber128_round149_sources_v2_20261008')
  if name.startswith('register_'):
   needle="len(measured['ordered_native_components']) in (3,4,7)";assert s.count(needle)==1
   s=s.replace(needle,"len(measured['ordered_native_components']) in (2,3,5)")
  compile(s,str(A/name),'exec');result[name]=s
 return result
def main():
 original.generate=generate
 original.main()
if __name__=='__main__':main()
