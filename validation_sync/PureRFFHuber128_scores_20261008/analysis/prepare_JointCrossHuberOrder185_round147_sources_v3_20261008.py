"""Bind the actual complete ordered185 source receiver after immutable legacy conversion."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_JointCrossHuberOrder185_round147_sources_v2_20261008 as original
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 out=[]
 for p in original.source_paths():
  if p.name=='run_JointCrossHuberOrder185_round147_full_registration_v3_20261008.py':p=A/'run_JointCrossHuberOrder185_round147_full_registration_v4_20261008.py'
  if p.name=='publish_JointCrossHuberOrder185_evidence_v2_20261008.py':p=A/'publish_JointCrossHuberOrder185_evidence_v3_20261008.py'
  out.append(p)
 out += [Path(__file__),Path(original.__file__),A/'bind_JointCrossHuber147_actual_generator_v3_20261008.py',A/'JointCrossHuber147_actual_generator_binding_v3_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 result={}
 for n,s in ORIGINAL_GENERATE(parent).items():
  for version in (1,2):s=s.replace('prepare_JointCrossHuberOrder185_round147_sources_v'+str(version)+'_20261008','prepare_JointCrossHuberOrder185_round147_sources_v3_20261008')
  compile(s,str(A/n),'exec');result[n]=s
 return result
def main():
 original.generate=generate
 original.main()
if __name__=='__main__':main()
